import time

from Picks import Pick
from BaseFunction import *


class Beton():
    picks = 'picks'
    archive = 'archive'
    xpathPicks = "//*[@class='sport tte soc' or " \
                "@class='location' or " \
                "@class='event_main' or " \
                "@class='event_aux' or " \
                "@class='outcome tte' or " \
                "@class='stake' or " \
                "@class='odds' or " \
                "@class='book' or " \
                "@class='header_inactive']"
    xpathArchive = "//*[@class='subs_table_picks']/table/tbody/tr/td"

    def parsePicks(self, requests):
        timeStart = time.time()
        picks = list()
        pick = Pick()
        for elem in requests.getElems(self.xpathPicks):
            className = elem.get_attribute("class")
            print(elem.text)
            if className == 'sport tte soc':
                appendPick(pick, picks)
                pick = Pick()
                pick.setSport(elem.text)
            elif className == 'location':
                listData = elem.text.split('\n')
                timeData = listData[0].split('    ')
                if len(timeData) == 1:
                    day, hour, minute = parseHourMinute(timeData[0])
                    pick.setTimeEvent(int(day), int(hour), int(minute))
                else:
                    day, hour, minute = parseHourMinute(timeData[0])
                    pick.setTimeInput(int(day), int(hour), int(minute))
                    day, hour, minute = parseHourMinute(timeData[1])
                    pick.setTimeEvent(int(day), int(hour), int(minute))
                pick.setEvent(listData[1])
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

        for elem in requests.getElems(self.xpathArchive):
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

resourceNames = [{'name': 'betonsuccess.ru', 'class': Beton}]