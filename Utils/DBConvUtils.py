from Constants.DBFunctions import getDataById
from Picks import Pick
from models import *

def BetToPick(bet):
    pick = None
    if bet is not None:
        pick = Pick()
        setBase = lambda data: data.base_name if data is not None else None
        pick.setTimeEvent(bet.time_event)
        pick.setTimeInput(bet.time_input)
        pick.setResult(bet.result)
        buf = getDataById(bet.bookmaker_id_bookmaker, Bookmaker, Bookmaker.id_bookmaker).get()
        pick.setBookmaker(setBase(buf))
        pick.setKF(bet.kf)
        pick.setPercent(bet.percent)
        forecast = getDataById(bet.forecast_id_forecast, Forecast, Forecast.id_forecast).get()
        pick.setForecast((forecast.base_name + bet.val_forecast) if forecast is not None else None)
        teamBets = TeamBet.select().where(TeamBet.bet_id_bet == bet.id_bet)
        buf = getDataById(teamBets[0].team_id_team, Team, Team.id_team).get()
        pick.setFirstTeam(setBase(buf))
        buf = getDataById(teamBets[1].team_id_team, Team, Team.id_team).get()
        pick.setSecondTeam(setBase(buf))
        buf = getDataById(bet.sport_id_sport, Sport, Sport.id_sport)
        pick.setSport(setBase(buf))
        buf = getDataById(bet.ligue_id_ligue, Ligue, Ligue.id_ligue)
        pick.setEvent(setBase(buf))
    return pick