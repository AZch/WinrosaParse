import datetime

from DynamicWebParse.DynamicWebParse import DynamicWebParse
from DynamicWebParse.Requests import Requests
from Constants.CommandsParse import *
from Constants.DBFunctions import *

driver = '/home/az/ProjectsData/Drivers/chromedriver'

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
    parse.makeUnvisibleDriver()

    requests = Requests(parse.getDriver())

    cappers = getAllCapper()
    for capper in cappers:
        resource = getResourceByID(capper.resource_id_resource)[0]
        link = generateLink(capper, resource)

        ClassGet = getTypeByNameResource(resource.name)

        resourceCommand = getCommandResourceByName(resource, ClassGet.picks)[0]
        requests.allwaysLoadPage(link + resourceCommand.data + "/")

        picks = ClassGet.parsePicks(self=ClassGet, requests=requests)
        for pick in picks:
            addBet(capper, pick)

        resourceCommand = getCommandResourceByName(resource, ClassGet.archive)[0]
        requests.allwaysLoadPage(link + resourceCommand.data + "/" + str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "/")

        ClassGet.parseArchive(self=ClassGet, requests=requests)
