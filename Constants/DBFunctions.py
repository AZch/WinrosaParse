import datetime

from models import *
import re


def getAllCapper():
    return Capper.select()


def getResourceByID(id):
    return Resource.select().where(Resource.id_resource == id)


def getAllCommandResource(id):
    return ResourceCommand.select().where(ResourceCommand.resource_id_resource == id)


def getCommandResourceByName(resource, command):
    return ResourceCommand.select().where(ResourceCommand.resource_id_resource == resource.id_resource \
                                          and ResourceCommand.desc == command)


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
        test1 = type(baseClass)
        test1 = type(classRet)
        if type(baseClass) == type(classRet):
            return classRet
        else:
            return baseClass.select().where(idBase == classRetForeigen)[0]
    else:
        return None


def getBet(pick, capper, valForecast, forecastDB, bk, sport, ligue,
           teamHome, teamAway, nowCreate):
    bet = Bet.select().where(Bet.percent == pick.getPercent(),
                             Bet.kf == pick.getKF(),
                             Bet.result == pick.getResult(),
                             Bet.capper_id_capper == capper.id_capper,
                             Bet.val_forecast == valForecast,
                             Bet.forecast_id_forecast == forecastDB.id_forecast,
                             Bet.bookmaker_id_bookmaker == bk.id_bookmaker,
                             Bet.sport_id_sport == sport.id_sport,
                             Bet.ligue_id_ligue == ligue.id_ligue)

    try:
        bet = bet[0]
        if bet.id_bet != None:
            teamBets = TeamBet.select().where(TeamBet.bet_id_bet == bet.id_bet)
            if nowCreate and len(teamBets) == 0:
                return bet
            for teamBet in teamBets:
                if teamBet.team_id_team != teamHome.id_team and \
                        teamBet.team_id_team != teamAway.id_team:
                    return bet
    except:
        pass
    return None


def addBet(capper, pick):
    sport = findWithName(pick.getSport(), Sport, SportNames,
                         "CANT FIND SPORT: " + pick.getSport())
    try:
        sport = getBase(Sport, Sport.id_sport, sport, sport.sport_id_sport)
    except:
        pass

    ligue = findWithName(pick.getEvent(), Ligue, LigueNames,
                         "CANT FIND LIGUE: " + pick.getEvent())
    try:
        ligue = getBase(Ligue, Ligue.id_ligue, ligue, ligue.ligue_id_ligue)
    except:
        pass

    teamHome = findWithName(pick.getFirstTeam(), Team, TeamNames,
                            "CANT FIND TEAM: " + pick.getFirstTeam())
    try:
        teamHome = getBase(Team, Team.id_team, teamHome, teamHome.team_id_team)
    except:
        pass

    teamAway = findWithName(pick.getSecondTeam(), Team, TeamNames,
                            "CANT FIND TEAM: " + pick.getSecondTeam())
    try:
        teamAway = getBase(Team, Team.id_team, teamAway, teamAway.team_id_team)
    except:
        pass

    bk = findWithName(pick.getBookmaker(), Bookmaker, BookMakerNames,
                      "CANT FIND BK: " + pick.getBookmaker())
    try:
        bk = getBase(Bookmaker, Bookmaker.id_bookmaker, bk, bk.bookmaker_id_bookmaker)
    except:
        pass

    forecastDB = findWithName("".join(re.findall('[a-zA-Zа-яА-Я]+', pick.getForecast())),
                              Forecast, ForecastNames, "CANT FIND FORECAST: " + pick.getForecast(), )
    try:
        forecastDB = getBase(Forecast, Forecast.id_forecast, forecastDB, forecastDB.forecast_id_forecast)
    except:
        pass

    valForecast = re.findall('\d+\.\d+|\d+', pick.getForecast())[0]

    bet = getBet(pick, capper, valForecast, forecastDB, bk, sport, ligue, teamHome, teamAway, False)

    if bet == None:
        now = datetime.datetime.now()
        Bet.create(percent=float(pick.getPercent()), kf=pick.getKF(), result=pick.getResult(),
                   capper_id_capper=capper.id_capper, val_forecast=valForecast,
                   forecast_id_forecast=forecastDB.id_forecast, bookmaker_id_bookmaker=bk.id_bookmaker,
                   sport_id_sport=sport.id_sport, ligue_id_ligue=ligue.id_ligue,
                   capper_resource_id_resource=capper.resource_id_resource)
        bet = getBet(pick, capper, valForecast, forecastDB, bk, sport, ligue, teamHome, teamAway, True)
        TeamBet.create(team_id_team=teamHome.id_team, bet_id_bet=bet.id_bet)
        TeamBet.create(team_id_team=teamAway.id_team, bet_id_bet=bet.id_bet)
    return bet
