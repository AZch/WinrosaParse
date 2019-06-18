import datetime


class Pick():
    def __init__(self):
        self.__sport = ""
        self.__event = ""
        self.__firstTeam = ""
        self.__secondTeam = ""
        self.__forecast = ""
        self.__percent = 0.0
        self.__kf = 0.0
        self.__bookmaker = ""
        self.__timeInput = None
        self.__timeEvent = None
        self.__descs = list()
        self.__result = 0.0

    def isValid(self):
        return self.__sport != "" and \
                self.__event != "" and \
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
        self.__percent = percent

    def setKF(self, kf):
        self.__kf = kf

    def getTimeFromNow(self, day, hour, minute, isBefore):
        if isBefore:
            return datetime.datetime.now() - datetime.timedelta(days=day) - datetime.timedelta(hours=hour) - datetime.timedelta(minutes=minute)
        else:
            return datetime.datetime.now() + datetime.timedelta(days=day) + datetime.timedelta(hours=hour) + datetime.timedelta(minutes=minute)

    def setTimeInput(self, day, hour, minute):
        self.__timeInput = self.getTimeFromNow(day, hour, minute, True)

    def setTimeEvent(self, day, hour, minute):
        self.__timeEvent = self.getTimeFromNow(day, hour, minute, False)

    def addDesc(self, desc):
        if isinstance(desc, str):
            self.__descs.append(desc)