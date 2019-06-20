import datetime
import re
import time

from selenium.webdriver.common.keys import Keys

from Picks import Pick
from BaseFunction import *
from Constants.Words import *


class Beton():
    baseWord = 'betonsuccess.ru'
    picks = 'picks'
    archive = 'picks_archive'
    xpathPicks = "//*[@class='sport tte soc' or " \
                "@class='location' or " \
                "@class='event_main' or " \
                "@class='event_aux' or " \
                "@class='outcome tte' or " \
                "@class='stake' or " \
                "@class='odds' or " \
                "@class='book' or " \
                "@class='header_inactive' or " \
                "@class='starts']"
    xpathArchive = "//*[@class='subs_table_picks']/table/tbody/tr/td|" \
                   "//*[@class='subs_table_picks']/table/tbody/tr/td/*[@class='tte']"
    makeDate = lambda dateList, timeList: datetime.datetime(int(dateList[-1]), MonthRU[dateList[-2]], int(dateList[-3]),
                                                            int(timeList[0]), int(timeList[1]))

    def makePreAction(self, requests, data):
        requests.sendKeysGetElem("//*[@id='user_name_id_module']", data[0])
        requests.sendKeysGetElem("//*[@id='user_password_id_module']", data[1])
        requests.getElem("//*[@class='auth_button']").submit()

    def makeLinkPicks(self, baseLink):
        return baseLink + self.picks + "/"

    def makeLinkArchive(self, baseLink, date):
        return baseLink + self.archive + "/" + str(date.year) + "-" + str(date.month) + "/"

    def getDate(self, prevWord, baseStr):
        datePick = re.findall(prevWord+ '(.*),', baseStr)[0].strip().split(' ')
        timePick = re.findall('\d+:\d+', baseStr)[0].strip().split(':')
        return self.makeDate(datePick, timePick)

    def waitDate(self, requests, oldStyle):
        elem = requests.getElem("//*[@id='tt_style']")
        while oldStyle == elem.get_attribute('style'): continue
        return elem.get_attribute('style')

    def setPickData(self, strEvent, strInput, pick, elem, requests, oldStyle):
        requests.moveToElem(elem)
        oldStyle = self.waitDate(self, requests, oldStyle)
        for dateElem in requests.getElems("//*[@class='date_hint']/table/tbody/tr"):
            dateText = dateElem.text
            if strInput in dateText:
                pick.setTimeInput(self.getDate(self, strInput, dateText))
            elif strEvent in dateText:
                pick.setTimeEvent(self.getDate(self, strEvent, dateText))
        return pick, oldStyle

    def parsePicks(self, requests):
        timeStart = time.time()
        picks = list()
        pick = Pick()
        oldStyle = ''
        for elem in requests.getElems(self.xpathPicks):
            className = elem.get_attribute("class")
            print(elem.text)
            if className == 'starts':
                pick, oldStyle = self.setPickData(self, "Событие:", "Введено:", pick, elem, requests, oldStyle)
            if className == 'sport tte soc':
                appendPick(pick, picks)
                pick = Pick()
                pick.setSport(elem.text)
            elif className == 'location':
                pick.setEvent(elem.text.split('\n')[1])
            elif className == 'event_main':
                teams = elem.text.split(' - ')
                pick.setFirstTeam(testStr(teams[0].strip()))
                pick.setSecondTeam(testStr(teams[1].strip()))
            elif className == 'event_aux':
                pick.addDesc(elem.text)
            elif className == 'outcome tte':
                pick.setForecast(elem.text)
            elif className == 'stake':
                pick.setPercent(elem.text[:-1])
            elif className == 'odds':
                pick.setKF(elem.text)
            elif className == 'book':
                pick.setBookmaker(elem.text)
            elif className == 'header_inactive':
                break
        appendPick(pick, picks)
        print("Parse time: " + str(time.time() - timeStart))
        return picks

    def parseArchive(self, requests):
        timeStart = time.time()
        countColl = 0

        picksBefore = list()
        pick = Pick()
        oldStyle = ''
        for elem in requests.getElems(self.xpathArchive):
            if elem.get_attribute("class") == 'tte':
                pick, oldStyle = self.setPickData(self, 'Началось:', 'Введено:', pick, elem, requests, oldStyle)
            else :
                if countColl == 0:
                    pick = Pick()
                    pick.setEvent(elem.text)
                    countColl += 1
                elif countColl == 1:
                    pick.setSport(elem.text)
                    countColl += 1
                elif countColl == 2:
                    listData = elem.text.split('\n')
                    teams = listData[0].split(' - ')
                    pick.setFirstTeam(testStr(teams[0].strip()))
                    pick.setSecondTeam(testStr(teams[1].strip()))
                    if len(listData) > 1:
                        pick.addDesc(listData[1])
                    countColl += 1
                elif countColl == 3:
                    pick.setForecast(elem.text)
                    countColl += 1
                elif countColl == 4:
                    pick.setPercent(elem.text[:-1])
                    countColl += 1
                elif countColl == 5:
                    pick.setKF(elem.text)
                    countColl += 1
                elif countColl == 6:
                    pick.setBookmaker(elem.text)
                    countColl += 1
                elif countColl == 7:
                    pick.setResult(elem.text[:-1])
                    countColl = 0
                    appendPick(pick, picksBefore)
        print("Parse time: " + str(time.time() - timeStart))
        return picksBefore

resourceNames = [{'name': Beton.baseWord, 'class': Beton}]