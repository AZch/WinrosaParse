from Constants.FilterInterval import AllFilters, AllFiltersCode
from models import *


def getAllCapper():
    return Capper.select()


def getResourceByID(id):
    return Resource.select().where(Resource.id_resource == id)

def getUserForFilter(filter):
    return User.select(User)\
        .join(UserFilter)\
        .where(UserFilter.user_id_user == User.id_user,
               UserFilter.filter_id_filter == filter.id_filter)


def findWithName(name, baseClass, otherClass, msg):
    allBase = baseClass.select().where(baseClass.base_name == name)

    for base in allBase:
        if base.base_name == name:
            return base

    allOther = otherClass.select().where(otherClass.other_name == name)

    for other in allOther:
        if other.other_name == name:
            return other

    print(msg)
    data = baseClass.create(base_name=name)
    return data

    # return None


def getBase(baseClass, idBase, classRet, classRetForeigen):
    if classRet is not None:
        if not hasattr(classRet, classRetForeigen):
            return classRet
        else:
            return baseClass.select().where(idBase == getattr(classRet, classRetForeigen)).get()
    else:
        return None


def getBet(pick, capper, valForecast, forecastDB, bk, sport, ligue,
           teamHome, teamAway, nowCreate, descsBet):
    bet = Bet.select().where(Bet.percent == pick.getPercent(),
                             Bet.capper_id_capper == capper.id_capper,
                             Bet.val_forecast == valForecast,
                             Bet.forecast_id_forecast == forecastDB.id_forecast,
                             Bet.bookmaker_id_bookmaker == bk.id_bookmaker,
                             Bet.sport_id_sport == sport.id_sport,
                             Bet.ligue_id_ligue != -1 if ligue is None else Bet.ligue_id_ligue == ligue.id_ligue,
                             Bet.time_event == pick.getTimeEvent(),
                             Bet.time_input == pick.getTimeInput())

    try:
        bet = bet.get()
        if bet.id_bet != None:
            teamBets = TeamBet.select().where(TeamBet.bet_id_bet == bet.id_bet)
            descBet = DescBet.select().where(DescBet.bet_id_bet == bet.id_bet)
            if nowCreate and len(teamBets) == 0 and len(descBet) == 0:
                return bet
            for teamBet in teamBets:
                if teamBet.team_id_team != teamHome.id_team and \
                        teamBet.team_id_team != teamAway.id_team:
                    return bet
            for desc in descBet:
                isFind = False
                for descBase in descsBet:
                    if desc.desc_id_desc == descBase.id_desc:
                        isFind = True
                        break
                if not isFind:
                    return None
    except:
        pass
    return None


def getBetById(id):
    return Bet.select().where(Bet.id_bet == id).get()

def getLastInputResultBetForCupper(capper):
    try:
        betDate = Bet.select(fn.MAX(Bet.time_input)).where(Bet.capper_id_capper == capper.id_capper,
                                                            Bet.result != None)
        res = Bet.select().where(Bet.time_input == betDate, Bet.capper_id_capper == capper.id_capper,
                                                            Bet.result != None)
        return res.get()
    except:
        return None

def getDataById(id, Data, DataId):
    return Data.select().where(DataId == id).get()

def addBet(capper, pick, isArchive, filters=None):
    sport = getBase(Sport, Sport.id_sport, findWithName(pick.getSport(), Sport, SportNames,
                     "CANT FIND SPORT: " + pick.getSport()), "sport_id_sport")

    if pick.getEvent() != '':
        ligue = getBase(Ligue, Ligue.id_ligue, findWithName(pick.getEvent(), Ligue, LigueNames,
                         "CANT FIND LIGUE: " + pick.getEvent()), "ligue_id_ligue")
    else:
        ligue = None

    teamHome = getBase(Team, Team.id_team, findWithName(pick.getFirstTeam(), Team, TeamNames,
                        "CANT FIND TEAM: " + pick.getFirstTeam()), "team_id_team")

    teamAway = getBase(Team, Team.id_team, findWithName(pick.getSecondTeam(), Team, TeamNames,
                        "CANT FIND TEAM: " + pick.getSecondTeam()), "team_id_team")

    bk = getBase(Bookmaker, Bookmaker.id_bookmaker, findWithName(pick.getBookmaker(), Bookmaker, BookMakerNames,
                  "CANT FIND BK: " + pick.getBookmaker()), "bookmaker_id_bookmaker")

    forecastDB = getBase(Forecast, Forecast.id_forecast, findWithName(pick.getForecast(), Forecast, ForecastNames,
                                                                      "CANT FIND FORECAST: " + pick.getForecast()),
                         "forecast_id_forecast")

    valForecast = pick.getValForecast()

    descsBet = list()
    for desc in pick.getDescs():
        descBet = getBase(Descs, Descs.id_descs_bet, findWithName(desc, Descs, DescsNames,
                      "CANT FIND DESC: " + desc), "descs_id_descs_bet")
        descsBet.append(descBet)

    bet = getBet(pick, capper, valForecast, forecastDB, bk, sport, ligue, teamHome, teamAway, False, descsBet)
    

    if bet is None and not isArchive:
        bet = getBetById(Bet.insert(percent=pick.getPercent(), kf=pick.getKF(),
                                    capper_id_capper=capper.id_capper, val_forecast=valForecast,
                                    forecast_id_forecast=forecastDB.id_forecast, bookmaker_id_bookmaker=bk.id_bookmaker,
                                    sport_id_sport=sport.id_sport, ligue_id_ligue=ligue.id_ligue,
                                    time_event=pick.getTimeEvent(), time_input=pick.getTimeInput()).execute())

        TeamBet.create(team_id_team=teamHome.id_team, bet_id_bet=bet.id_bet)
        TeamBet.create(team_id_team=teamAway.id_team, bet_id_bet=bet.id_bet)
        calcDataFilter = lambda classType, start, end, val: classType(start, end).calc(val)
        for desc in descsBet:
            DescBet.create(bet_id_bet=bet.id_bet, descs_id_descs_bet=desc.id_descs_bet)
        for filter in filters:
            if len(getFilterData(filter, FilterBookmaker, FilterBookmaker.bookmaker_id_bookmaker,
                                         Bookmaker, Bookmaker.id_bookmaker)) > 0 and \
                    len(getFilterDataForId(filter, FilterBookmaker, FilterBookmaker.bookmaker_id_bookmaker,
                                         Bookmaker, Bookmaker.id_bookmaker, bk.id_bookmaker)) == 0:
                continue
            if len(getFilterData(filter, FilterSport, FilterSport.sport_id_sport,
                                                Sport, Sport.id_sport)) > 0 and  \
                    len(getFilterDataForId(filter, FilterSport, FilterSport.sport_id_sport,
                                                Sport, Sport.id_sport, sport.id_sport)) == 0:
                continue
            if len(getFilterData(filter, FilterForecast, FilterForecast.filter_id_filter,
                                                Forecast, Forecast.id_forecast)) > 0 and \
                    len(getFilterDataForId(filter, FilterForecast, FilterForecast.filter_id_filter,
                                                Forecast, Forecast.id_forecast, forecastDB.id_forecast)) == 0:
                continue
            if len(getFilterData(filter, FilterLigue, FilterLigue.ligue_id_ligue,
                                             Ligue, Ligue.id_ligue)) > 0 and \
                    len(getFilterDataForId(filter, FilterLigue, FilterLigue.ligue_id_ligue,
                                             Ligue, Ligue.id_ligue, ligue.id_ligue)) == 0:
                continue
            if len(getFilterData(filter, FilterTeam, FilterTeam.team_id_team,
                                            Team, Team.id_team)) > 0 and \
                    len(getFilterDataForId(filter, FilterTeam, FilterTeam.team_id_team,
                                            Team, Team.id_team)) == 0:
                continue
            isSend = True
            for data in filter.dataFilter:
                dataFilter = getDataById(data.type_data_bet_id_type_data_bet,
                                              TypeDataBet,
                                              TypeDataBet.id_type_data_bet)
                for code in AllFiltersCode:
                    if dataFilter.type_code == code:
                        if not calcDataFilter(AllFilters[dataFilter.type_code],
                                              data.start, data.end,
                                              pick.getDataForCode(code)):
                            isSend = False
                            break
                if not isSend:
                    break
            if not isSend:
                continue
            #
            # ОТПРАВКА СООБЩЕНИЯ
            for userFilter in UserFilter.select().where(UserFilter.filter_id_filter == filter.id_filter):
                filterCapper = FilterCapper.select().where(FilterCapper.user_filter_id_user_filter == userFilter.id_user_filter,
                                                           FilterCapper.capper_id_capper == capper.id_capper).get()
                print(filterCapper.channel)
                UserBet.create(bet_id_bet=bet.id_bet,
                               filter_capper_id_filter_capper=filterCapper.id_filter_capper)
            #

    elif bet is not None:
        if bet.result is None and pick.getResult() is not None and pick.getKF() is not None:
            query = Bet.update(result=pick.getResult(), kf=pick.getKF()).where(Bet.id_bet == bet.id_bet)
            query.execute()
            print(bet)
            userBets = UserBet.select().where(UserBet.bet_id_bet == bet.id_bet)
            for userBet in userBets:
                userFilter = UserFilter\
                    .select()\
                    .join(FilterCapper)\
                    .where(FilterCapper.user_filter_id_user_filter == UserFilter.id_user_filter,
                           userBet.filter_capper_id_filter_capper == FilterCapper.id_filter_capper)
                # отправка данных результата userBet есть и userFilter тоже
                print("RESULT:", str(len(userFilter)), str(userFilter.get().channel))
    return bet

def getFilterDataForId(filter, DataFilter, DataFilterId, Data, DataId, idSearch):
    return Data.select(Data)\
        .join(DataFilter)\
        .where(DataFilter.filter_id_filter == filter.id_filter,
               DataFilterId == DataId,
               DataId == idSearch)

def getFilterData(filter, DataFilter, DataFilterId, Data, DataId):
    return Data.select(Data)\
        .join(DataFilter)\
        .where(DataFilter.filter_id_filter == filter.id_filter,
               DataFilterId == DataId)

def getFiltersForCapper(capper):
    return Filter.select(Filter)\
        .join(UserFilter)\
        .join(FilterCapper)\
        .where(
            FilterCapper.capper_id_capper == capper.id_capper,
            FilterCapper.user_filter_id_user_filter == UserFilter.id_user_filter,
            UserFilter.filter_id_filter == Filter.id_filter)
