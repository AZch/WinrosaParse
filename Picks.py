import datetime


class Pick():
    def __init__(self):
        self.__sport = ""
        self.__event = ""
        self.__firstTeam = ""
        self.__secondTeam = ""
        self.__forecast = ""
        self.__valForecast = 0.0
        self.__percent = 0.0
        self.__kf = 0.0
        self.__bookmaker = ""
        self.__timeInput = None
        self.__timeEvent = None
        self.__descs = list()
        self.__result = None

    def getValForecast(self):
        return self.__valForecast

    def getDescs(self):
        return self.__descs

    def getBookmaker(self):
        return self.__bookmaker

    def getForecast(self):
        return self.__forecast

    def getSport(self):
        return self.__sport

    def getEvent(self):
        return self.__event

    def getFirstTeam(self):
        return self.__firstTeam

    def getSecondTeam(self):
        return self.__secondTeam

    def getForecast(self):
        return self.__forecast

    def getPercent(self):
        return self.__percent

    def getKF(self):
        return self.__kf

    def getTimeInput(self):
        return self.__timeInput

    def getTimeEvent(self):
        return self.__timeEvent

    def getResult(self):
        return self.__result

    def isValid(self):
        return self.__sport != "" and \
                self.__firstTeam != "" and \
                self.__secondTeam != "" and \
                self.__forecast != "" and \
                self.__percent != 0.0 and \
                self.__kf != 0.0 and \
                self.__bookmaker != ""

    def setSport(self, sport):
        self.__sport = sport

    def setResult(self, result):
        self.__result = result

    def setEvent(self, event):
        self.__event = event

    def setFirstTeam(self, team):
        self.__firstTeam = team

    def setSecondTeam(self, team):
        self.__secondTeam = team

    def setForecast(self, forecast):
        self.__forecast = forecast

    def setBookmaker(self, bookmaker):
        self.__bookmaker = bookmaker

    def setPercent(self, percent):
        self.__percent = float(percent)

    def setKF(self, kf):
        self.__kf = float(kf)

    def getTimeFromNow(self, day, hour, minute, isBefore):
        if isBefore:
            return datetime.datetime.now() - datetime.timedelta(days=day) - datetime.timedelta(hours=hour) - datetime.timedelta(minutes=minute)
        else:
            return datetime.datetime.now() + datetime.timedelta(days=day) + datetime.timedelta(hours=hour) + datetime.timedelta(minutes=minute)

    def setTimeInput(self, date):
        self.__timeInput = date

    def setValForecast(self, val):
        self.__valForecast = float(val)

    def setTimeEvent(self, date):
        self.__timeEvent = date

    def addDesc(self, desc):
        if isinstance(desc, str):
            self.__descs.append(desc)