import re

from BaseFunction import *
from CommandParse.IResourceParse import IResourceParse
from Constants.Words import *
from Picks import Pick
from Utils.TimeUtils import *


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

    def generateLink(self, capper, resource):
        return resource.url + "/" + ("" if capper.prev_data == "" else (capper.prev_data + "/")) + \
               capper.personal_data + \
               ("" if capper.post_data == "" else ("/" + capper.post_data)) + "/"

    def makePreAction(self, requests, data=None):
        if data is None or len(data) < 2 or \
                data[0] is None or data[1] is None:
            return None
        requests.sendKeysGetElem("//*[@id='user_name_id_module']", data[0])
        requests.sendKeysGetElem("//*[@id='user_password_id_module']", data[1])
        requests.getElem("//*[@class='auth_button']").submit()

    def makeLinkPicks(self, baseLink, data=None):
        return baseLink + self.picks + "/"

    def makeLinkArchive(self, baseLink, data=None):
        date = data[2]
        return baseLink + self.archive + "/" + str(date.year) + "-" + str(date.month) + "/"

    def setForecast(self, text, pick):
        numsForecast = re.findall(' \d+\.\d+| \d+| \+\d+\.\d+| \+\d+| -\d+\.\d+| -\d+', text)
        strVal = ("0" if len(numsForecast) == 0 else numsForecast[0]).strip()
        pick.setValForecast(strVal)
        pick.setForecast(text.replace(strVal, "").strip())
        return pick

    def parsePicks(self, requests):

        picks = list()
        pick = Pick()
        oldStyle = ''
        for elem in requests.getElems(self.xpathPicks):
            className = elem.get_attribute("class")
            if className == 'starts':
                pick, oldStyle = self.setPickData(self, "Событие:", "Введено:", pick, elem, requests, oldStyle, True)
            if className == 'sport tte soc':
                appendPick(pick, picks)
                pick = Pick()
                requests.moveToElem(elem)
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
                pick = self.setForecast(self=self, text=elem.text, pick=pick)
            elif className == 'stake':
                pick.setPercent(testFloat(elem.text[:-1]))
            elif className == 'odds':
                pick.setKF(testFloat(elem.text))
            elif className == 'book':
                pick.setBookmaker(elem.text)
            elif className == 'header_inactive':
                break
        appendPick(pick, picks)
        return picks

    def parseArchive(self, requests, lastBet=None):
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
                pick, oldStyle = self.setPickData(self, 'Началось:', 'Введено:', pick, elem, requests, oldStyle, True)
            else:
                if countColl == 0:
                    pick = Pick()
                    # pick.setEvent(elem.text)
                    countColl += 1
                elif countColl == 1:
                    requests.moveToElem(elem)
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
                    pick = self.setForecast(self=self, text=elem.text, pick=pick)
                    countColl += 1
                elif countColl == 4:
                    pick.setPercent(testFloat(elem.text[:-1]))
                    countColl += 1
                elif countColl == 5:
                    pick.setKF(testFloat(elem.text))
                    countColl += 1
                elif countColl == 6:
                    pick.setBookmaker(elem.text)
                    countColl += 1
                elif countColl == 7:
                    pick.setResult(testFloat(elem.text[:-1]))
                    countColl = 0
                    if lastBet is not None and pick.getSport() == lastBet.getSport() and \
                            compareDate(pick.getTimeEvent(), lastBet.getTimeEvent()) and \
                            compareDate(pick.getTimeInput(), lastBet.getTimeInput()) and \
                            compareTeam(pick.getFirstTeam(), lastBet) and \
                            compareTeam(pick.getSecondTeam(), lastBet):
                        break
                    appendPick(pick, picksBefore)
        return picksBefore

    def getDate(self, prevWord, baseStr):
        datePick = re.findall(prevWord + '(.*),', baseStr)[0].strip().split(' ')
        timePick = re.findall('\d+:\d+', baseStr)[0].strip().split(':')
        return self.makeDate(datePick, timePick)

    def waitDate(self, requests, oldStyle):
        elem = requests.getElem("//*[@id='tt_style']")
        while oldStyle == elem.get_attribute('style'): continue
        return elem.get_attribute('style')

    def setPickData(self, strEvent, strInput, pick, elem, requests, oldStyle, needWait):
        requests.moveToElem(elem)
        try:
            if needWait:
                oldStyle = self.waitDate(self=self, requests=requests, oldStyle=oldStyle)
                requests.moveToElem(elem)
            for dateElem in requests.getElems("//*[@class='date_hint']/table/tbody/tr"):
                dateText = dateElem.text
                if strInput in dateText:
                    pick.setTimeInput(self.getDate(self=self, prevWord=strInput, baseStr=dateText))
                elif strEvent in dateText:
                    pick.setTimeEvent(self.getDate(self=self, prevWord=strEvent, baseStr=dateText))
            if pick.getTimeEvent() is None or pick.getTimeInput() is None:
                return self.setPickData(self, strEvent, strInput, pick, elem, requests, oldStyle, False)
            return pick, oldStyle
        except:
            return self.setPickData(self, strEvent, strInput, pick, elem, requests, oldStyle, False)
