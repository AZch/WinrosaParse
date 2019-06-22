db = 'mydb'
user = 'test'
password = 'Test_Test123'
host = 'localhost'
port = 3306

sql = "select distinct Sport.BaseName, Ligue.BaseName, Bet.TimeInput, Bet.TimeEvent, Team.BaseName, Bet.KF, Bet.Percent, Bet.result, Descs.BaseName, Bookmaker.BaseName, Forecast.BaseName, Bet.ValForecast, Bet.idBet from Bet, Forecast, TeamBet, Sport, Ligue, Bookmaker, DescBet, Descs, Team where Bet.Forecast_idForecast = Forecast.idForecast and Bet.idBet = TeamBet.bet_idBet and TeamBet.Team_idTeam = Team.idTeam and Bet.Sport_idSport = Sport.idSport and Bet.Ligue_idLigue = Ligue.idLigue and Bet.idBet = DescBet.bet_idBet and DescBet.Descs_idDescsBet = Descs.idDescsBet and Bet.Bookmaker_idBookmaker = Bookmaker.idBookmaker;"