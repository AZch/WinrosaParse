import datetime
import re
import time

from Picks import Pick
from BaseFunction import *
from Constants.Words import *
from CommandParse.IResourceParse import IResourceParse


class BetonParse(IResourceParse):
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

    def makePreAction(self, requests, data=None):
        if data is None or len(data) < 2 or \
                data[0] is None or data[1] is None:
            return None
        requests.sendKeysGetElem("//*[@id='user_name_id_module']", data[0])
        requests.sendKeysGetElem("//*[@id='user_password_id_module']", data[1])
        requests.getElem("//*[@class='auth_button']").submit()

    def makeLinkPicks(self, baseLink):
        return baseLink + self.picks + "/"

    def makeLinkArchive(self, baseLink, date=None):
        return baseLink + self.archive + "/" + str(date.year) + "-" + str(date.month) + "/"

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
                if len(teams) > 1:
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

    def parseArchive(self, requests, lastBet=None):
        timeStart = time.time()
        countColl = 0

        picksBefore = list()
        pick = Pick()
        compareDate = lambda dateFirst, dateSec: dateFirst is not None and dateSec is not None and \
                                                 dateFirst.replace() == dateSec.replace()
        compareTeam = lambda team, pickCompare: pickCompare is not None and \
                                                pickCompare.getFirstTeam() is not None and \
                                                pickCompare.getSecondTeam() is not None and \
                                                (team.strip() == pickCompare.getFirstTeam().strip() or
                                                 team.strip() == pickCompare.getSecondTeam().strip())
        oldStyle = ''
        for elem in requests.getElems(self.xpathArchive):
            if elem.get_attribute("class") == 'tte':
                pick, oldStyle = self.setPickData(self, 'Началось:', 'Введено:', pick, elem, requests, oldStyle)
            else:
                if countColl == 0:
                    pick = Pick()
                    # pick.setEvent(elem.text)
                    countColl += 1
                elif countColl == 1:
                    pick.setSport(elem.text)
                    countColl += 1
                elif countColl == 2:
                    countColl += 1
                    listData = elem.text.split('\n')
                    for data in listData:
                        if len(data.split(' - ')) > 1:
                            teams = data.split(' - ')
                            break
                    else:
                        continue
                    pick.setFirstTeam(testStr(teams[0].strip()))
                    pick.setSecondTeam(testStr(teams[1].strip()))
                    if len(listData) > 1:
                        pick.addDesc(listData[1])

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
                    if lastBet is not None and pick.getSport() == lastBet.getSport() and \
                            compareDate(pick.getTimeEvent(), lastBet.getTimeEvent()) and \
                            compareDate(pick.getTimeInput(), lastBet.getTimeInput()) and \
                            compareTeam(pick.getFirstTeam(), lastBet) and \
                            compareTeam(pick.getSecondTeam(), lastBet):
                        break
                    appendPick(pick, picksBefore)
        print("Parse time: " + str(time.time() - timeStart))
        return picksBefore

    def getDate(self, prevWord, baseStr):
        datePick = re.findall(prevWord + '(.*),', baseStr)[0].strip().split(' ')
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