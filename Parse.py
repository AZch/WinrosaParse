import datetime
import time
import traceback

from Parsing.DynamicParse import DynamicParse
from Parsing.Requests import Requests
from Pickss import Datas

driver = '/home/az/ProjectsData/Drivers/chromedriver'


def testStr(data):
    return data if isinstance(str(data), str) else ""


def testFloat(data):
    return data if isinstance(float(data), float) else 0.0

def testInt(data):
    return data if isinstance(int(data), int) else 0

def parseHourMinute(data):
    if 'мин.' in data:
        day = 0
        hour = 0
        minute = testInt(data.split('мин.')[0].strip())
    else:
        day = 0
        hour = 0
        minute = 0
        splitDay = data.split('д.')
        if len(splitDay) > 1:
            day = testInt(splitDay[0].strip())
            hour = testInt(splitDay[1].split('ч.')[0].strip())
        else:
            splitHour = data.split('ч.')
            hour = testInt(splitHour[0].strip())
            minute = testInt(splitHour[1].split('м.')[0].strip())
    return day, hour, minute

picks = list()

def appendPick(pick):
    if pick.isValid():
        picks.append(pick)


if __name__ == '__main__':
    parse = DynamicParse(driver)
    parse.makeUnvisibleDriver()

    requests = Requests(parse.getDriver())

    requests.allwaysLoadPage("https://www.betonsuccess.ru/sub/104334/GalaxyBet21.T.L/picks/")

    xpath = "//*[@class='sport tte soc' or " \
            "@class='location' or " \
            "@class='event_main' or " \
            "@class='event_aux' or " \
            "@class='outcome tte' or " \
            "@class='stake' or " \
            "@class='odds' or " \
            "@class='book' or " \
            "@class='header_inactive']"

    pick = Datas()
    for elem in requests.getElems(xpath):
        className = elem.get_attribute("class")
        print(elem.text)
        if className == 'sport tte soc':
            appendPick(pick)
            pick = Datas()
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
    appendPick(pick)

    requests.allwaysLoadPage("https://www.betonsuccess.ru/sub/93783/buks-mak.SOC.L/picks_archive/")

    xpath = "//*[@class='subs_table_picks']/table/tbody/tr/td"
    countColl = 0

    picksBefore = list()
    pick = Datas()

    for elem in requests.getElems(xpath):
        if countColl == 0:
            pick = Datas()
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
            picksBefore.append(pick)

    time.sleep(5)
