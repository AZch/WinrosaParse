import random

from DynamicWebParse.DynamicWebParse import DynamicWebParse
from DynamicWebParse.Requests import Requests

from Constants.CommandsParse import *
from Constants.DBFunctions import *
from Constants.FilterInterval import *
from Utils.DBConvUtils import BetToPick

driver = '/home/az/ProjectsData/Drivers/chromedriver'

def getTypeByNameResource(resourceName):
    for name in resourceNames:
        if name['name'] == resourceName:
            return name['class']
    return None

if __name__ == '__main__':
    parse = DynamicWebParse(driver)
    parse.makeUnvisibleDriver()
    oldClassGet = None

    requests = Requests(parse.getDriver())
    filters = ''

    while True:

        cappers = getAllCapper()
        for capper in cappers:
            filters = getFiltersForCapper(capper)
            filtersData = list()
            for filter in filters:
                filter.users = getUserForFilter(filter)

            resource = getResourceByID(capper.resource_id_resource)[0]

            ClassGet = getTypeByNameResource(resource.name)
            link = ClassGet.generateLink(ClassGet, capper, resource)

            # uncomment if you need to login
            # if type(ClassGet) != type(oldClassGet):
            #     requests.allwaysLoadPage(link)
            #     ClassGet.makePreAction(ClassGet, requests, (resource.login, resource.password))

            requests.allwaysLoadPage(ClassGet.makeLinkPicks(ClassGet, link, [capper.prev_data, capper.post_data]))

            startTrackTime()
            for pick in ClassGet.parsePicks(self=ClassGet, requests=requests):
                addBet(capper, pick, False, filters)
            print("End parse current: " + str(endTrackTime()))

            requests.allwaysLoadPage(ClassGet.makeLinkArchive(ClassGet, link, [capper.prev_data, capper.post_data, getDateTimeNow()]))

            startTrackTime()
            for pick in ClassGet.parseArchive(self=ClassGet, requests=requests, lastBet=BetToPick(getLastInputResultBetForCupper(capper))):
                addBet(capper, pick, True)
            print("End parse archive: " + str(endTrackTime()))

            #oldClassGet = ClassGet
        print("TIME WORK: " + str(getTimeWork()))
        time.sleep(random.randint(15, 20) * 60)
