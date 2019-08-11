import re

from BaseFunction import testInt
from CommandParse.IResourceParse import IResourceParse
from Constants.Words import MonthEN_Little
from Picks import Pick
from Utils.TimeUtils import *


class BlogabetParse(IResourceParse):
    baseWord = 'blogabet.com'
    protocolWord = 'https://'
    xpathPick = "//*[@class='block media _feedPick feed-pick']"

    def generateLink(self, capper, resource):
        return resource.url

    def getTimeEventData(self, timeEventStr):
        timeEvent = timeEventStr.split('Kick off:')[1].strip()
        date = timeEvent.split(',')[0].strip().split(' ')
        time = timeEvent.split(',')[1].strip().split(':')
        return dateByDayMonthYearHourMinute(testInt(date[0]), MonthEN_Little[date[1]], testInt(date[2]),
                                            testInt(time[0]), testInt(time[1]))

    def getTimeInputData(self, timeInputStr):
        timeInput = timeInputStr.split(',')
        dayMonth = timeInput[1].strip()
        month = dayMonth.split(' ')[0].strip()
        day = dayMonth.split(' ')[1].strip()[:-2]
        year = timeInput[2].strip()
        time = timeInput[3].strip().split(':')
        return dateByDayMonthYearHourMinute(testInt(day), MonthEN_Little[month], testInt(year),
                                            testInt(time[0]), testInt(time[1]))

    def makePreAction(self, requests, data=None):
        requests.clickElem("//*[contains(text(), 'LOG IN')]")
        if data is None or len(data) < 2 or \
                data[0] is None or data[1] is None:
            return None
        requests.sendKeysGetElem("//*[@id='email']", data[0])
        requests.sendKeysGetElem("//*[@id='password']", data[1])
        requests.getElem("//*[contains(text(), ' Login')]").submit()

    def makeLinks(self, baseLink, data=None):
        if isinstance(data, str):
            return self.protocolWord + data + "." + baseLink.replace(self.protocolWord, "")
        else:
            return baseLink

    def makeLinkPicks(self, baseLink, data=None):
        return self.makeLinks(self=self, baseLink=baseLink, data=data[1])

    def makeLinkArchive(self, baseLink, data=None):
        return self.makeLinks(self=self, baseLink=baseLink, data=data[1])

    def parsePagePicks(self, strData):
        pick = Pick()
        elemTexts = strData.text.split('\n')
        pick.setTimeInput(self.getTimeInputData(self, elemTexts[1]))
        teams = elemTexts[2]
        pick.setFirstTeam(teams.split(' - ')[0])
        pick.setSecondTeam(teams.split(' - ')[1])
        forecast_kf = elemTexts[3]
        forecast = forecast_kf.split('@')[0]
        try:
            valForecast = re.findall(" \+\d+.\d+| \-\d+.\d+| \d+.\d+| \d+ | \+\d+| -\d+", forecast)[0].strip()
            forecast = forecast.replace(valForecast + " ", "").strip()
        except:
            valForecast = 0.0
        pick.setForecast(forecast)
        pick.setValForecast(valForecast)
        kf = forecast_kf.split('@')[1]
        pick.setKF(kf)
        del forecast_kf
        countBet_bk_result = elemTexts[4]
        countBet = float(countBet_bk_result.split(' ')[0].split('/')[0]) / 10
        pick.setPercent(5 * countBet)
        bk = countBet_bk_result.split(' ')[1]
        pick.setBookmaker(bk)
        result = float(countBet_bk_result.split(' ')[2])
        pick.setResult(result)
        del countBet_bk_result
        sport_ligue_timeEvent = elemTexts[5]
        sport = sport_ligue_timeEvent.split('/')[0]
        pick.setSport(sport)
        ligue = sport_ligue_timeEvent.split('/')[1]
        pick.setEvent(ligue)
        pick.setTimeEvent(self.getTimeEventData(self, sport_ligue_timeEvent.split('/')[2]))
        del sport_ligue_timeEvent
        return pick

    def parsePicks(self, requests):
        picks = list()
        dateNow = getDateTimeNow()
        for elem in requests.getElems(self.xpathPick):
            pick = self.parsePagePicks(self, elem)
            if pick.isValid():
                if dateNow < pick.getTimeEvent() and pick.getResult() == 0.0:
                    pick.setResult(None)
                    picks.append(pick)
                else:
                    break
        return picks

    def parseArchive(self, requests, lastBet=None):
        picks = list()
        dateNow = getDateTimeNow()
        dateNow += datetime.timedelta(hours=-12)
        for elem in requests.getElems(self.xpathPick):
            pick = self.parsePagePicks(self, elem)
            if pick.isValid():
                if dateNow > pick.getTimeEvent():
                    picks.append(pick)
                else:
                    break
        return picks