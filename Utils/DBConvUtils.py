from BaseFunction import testFloat
from Constants.DBFunctions import getDataById
from Picks import Pick
from models import *
setBase = lambda data: data.base_name if data is not None else None

def BetToPick(bet):
    pick = None
    if bet is not None:
        pick = Pick()
        pick.setTimeEvent(bet.time_event)
        pick.setTimeInput(bet.time_input)

        pick.setResult(testFloat(bet.result))

        buf = getDataById(bet.bookmaker_id_bookmaker, Bookmaker, Bookmaker.id_bookmaker)
        pick.setBookmaker(setBase(buf))

        pick.setKF(testFloat(bet.kf))
        pick.setPercent(testFloat(bet.percent))
        forecast = getDataById(bet.forecast_id_forecast, Forecast, Forecast.id_forecast)
        pick.setForecast((forecast.base_name + bet.val_forecast) if forecast is not None else None)
        teamBets = TeamBet.select().where(TeamBet.bet_id_bet == bet.id_bet)
        buf = getDataById(teamBets[0].team_id_team, Team, Team.id_team)
        pick.setFirstTeam(setBase(buf))
        buf = getDataById(teamBets[1].team_id_team, Team, Team.id_team)
        pick.setSecondTeam(setBase(buf))
        buf = getDataById(bet.sport_id_sport, Sport, Sport.id_sport)
        pick.setSport(setBase(buf))
        buf = getDataById(bet.ligue_id_ligue, Ligue, Ligue.id_ligue)
        pick.setEvent(setBase(buf))
    return pick