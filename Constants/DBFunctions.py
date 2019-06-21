import datetime

from models import *
from peewee import fn
from Picks import Pick
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
        if type(baseClass) == type(classRet):
            return classRet
        else:
            return baseClass.select().where(idBase == classRetForeigen).get()
    else:
        return None


def getBet(pick, capper, valForecast, forecastDB, bk, sport, ligue,
           teamHome, teamAway, nowCreate, descsBet):
    bet = Bet.select().where(Bet.percent == float(pick.getPercent()),
                             Bet.capper_id_capper == capper.id_capper,
                             Bet.val_forecast == float(valForecast),
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
        betResults = Bet.select().where(Bet.capper_id_capper == capper.id_capper,
                                        Bet.result is not None)
        betDate = Bet.select(fn.MAX(Bet.time_input)).where(Bet.id_bet == betResults)
        return Bet.select().where(Bet.time_input == betDate, Bet.id_bet == betResults).get()
    except:
        return None

def getDataById(id, Data, DataId):
    return Data.select().where(DataId == id)

def addBet(capper, pick):
    sport = findWithName(pick.getSport(), Sport, SportNames,
                         "CANT FIND SPORT: " + pick.getSport())
    try:
        sport = getBase(Sport, Sport.id_sport, sport, sport.sport_id_sport)
    except:
        pass

    if pick.getEvent() != '':
        ligue = findWithName(pick.getEvent(), Ligue, LigueNames,
                             "CANT FIND LIGUE: " + pick.getEvent())
        try:
            ligue = getBase(Ligue, Ligue.id_ligue, ligue, ligue.ligue_id_ligue)
        except:
            pass
    else:
        ligue = None

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

    numsForecast = re.findall('\d+\.\d+|\d+', pick.getForecast())
    valForecast = -1 if len(numsForecast) == 0 else numsForecast[0]

    descsBet = list()
    for desc in pick.getDescs():
        descBet = findWithName(desc, Descs, DescsNames,
                          "CANT FIND DESC: " + desc)
        try:
            descBet = getBase(Descs, Descs.id_descs_bet, descBet, descBet.descs_id_descs_bet)
        except:
            pass
        descsBet.append(descBet)

    bet = getBet(pick, capper, valForecast, forecastDB, bk, sport, ligue, teamHome, teamAway, False, descsBet)

    if bet is None and ligue is not None:
        bet = getBetById(Bet.insert(percent=float(pick.getPercent()), kf=float(pick.getKF()),
                                    capper_id_capper=capper.id_capper, val_forecast=float(valForecast),
                                    forecast_id_forecast=forecastDB.id_forecast, bookmaker_id_bookmaker=bk.id_bookmaker,
                                    sport_id_sport=sport.id_sport, ligue_id_ligue=ligue.id_ligue,
                                    time_event=pick.getTimeEvent(), time_input=pick.getTimeInput()).execute())

        TeamBet.create(team_id_team=teamHome.id_team, bet_id_bet=bet.id_bet)
        TeamBet.create(team_id_team=teamAway.id_team, bet_id_bet=bet.id_bet)
        for desc in descsBet:
            DescBet.create(bet_id_bet=bet.id_bet, descs_id_descs_bet=desc.id_descs_bet)
    elif bet is not None:
        if bet.result is None and pick.getResult() is not None:
            query = Bet.update(result=pick.getResult()).where(Bet.id_bet == bet.id_bet)
            query.execute()
    return bet
