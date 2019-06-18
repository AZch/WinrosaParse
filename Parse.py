import datetime
import time
import traceback

from Picks import Pick
from DynamicWebParse.DynamicWebParse import DynamicWebParse
from DynamicWebParse.Requests import Requests
from models import *
from Constants.CommandsParse import *

driver = '/home/az/ProjectsData/Drivers/chromedriver'

def getAllCapper():
    return Capper.select()

def getResourceByID(id):
    return Resource.select().where(Resource.id_resource == id)

def getAllCommandResource(id):
    return ResourceCommand.select().where(ResourceCommand.resource_id_resource == id)

def getCommandResourceByName(resource, command):
    return ResourceCommand.select().where(ResourceCommand.resource_id_resource == resource.id_resource \
                                          and ResourceCommand.desc == command)

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

def generateLink(capper, resource):
    return resource.url + "/" + ("" if capper.prev_data == "" else (capper.prev_data + "/")) + \
                                                                capper.personal_data + \
                              ("" if capper.post_data == "" else ("/" + capper.post_data)) + "/"

def getTypeByNameResource(resourceName):
    for name in resourceNames:
        if name['name'] == resourceName:
            return name['class']
    return None

if __name__ == '__main__':
    parse = DynamicWebParse(driver)
    parse.makeVisibleDriver()

    requests = Requests(parse.getDriver())

    cappers = getAllCapper()
    for capper in cappers:
        resource = getResourceByID(capper.resource_id_resource)[0]
        link = generateLink(capper, resource)

        ClassGet = getTypeByNameResource(resource.name)

        resourceCommand = getCommandResourceByName(resource, ClassGet.picks)[0]
        requests.allwaysLoadPage(link + resourceCommand.data + "/")

        pick = Pick()
        for elem in requests.getElems(ClassGet.xpathPicks):
            className = elem.get_attribute("class")
            print(elem.text)
            if className == 'sport tte soc':
                appendPick(pick)
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
        appendPick(pick)

        resourceCommand = getCommandResourceByName(resource, ClassGet.archive)[0]
        requests.allwaysLoadPage(link + resourceCommand.data + "/" + str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "/")

        countColl = 0

        picksBefore = list()
        pick = Pick()

        for elem in requests.getElems(ClassGet.xpathArchive):
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
                picksBefore.append(pick)

    parse.__del__()
