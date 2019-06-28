import random

from DynamicWebParse.DynamicWebParse import DynamicWebParse
from DynamicWebParse.Requests import Requests

from Constants.CommandsParse import *
from Constants.DBFunctions import *
from Constants.FilterInterval import *
from Utils.DBConvUtils import BetToPick

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

class AllFilterData():
    users = list()
    filtersData = list()
    filterBk = list()
    filterSport = list()
    filterLigue = list()
    filterForecast = list()
    filterTeam = list()

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
                filterData = AllFilterData()
                for bk in getFilterData(filter, FilterBookmaker, FilterBookmaker.bookmaker_id_bookmaker,
                                         Bookmaker, Bookmaker.id_bookmaker):
                    filterData.filterBk.append(IntInterval(bk.id_bookmaker, bk.id_bookmaker))
                for sport in getFilterData(filter, FilterSport, FilterSport.sport_id_sport,
                                                Sport, Sport.id_sport):
                    filterData.filterSport.append(IntInterval(sport.id_sport, sport.id_sport))
                for forecast in getFilterData(filter, FilterForecast, FilterForecast.filter_id_filter,
                                                Forecast, Forecast.id_forecast):
                    filterData.filterForecast.append(IntInterval(forecast.id_forecast, forecast.id_forecast))
                for ligue in getFilterData(filter, FilterLigue, FilterLigue.ligue_id_ligue,
                                             Ligue, Ligue.id_ligue):
                    filterData.filterLigue.append(IntInterval(ligue.id_ligue, ligue.id_ligue))

                for team in getFilterData(filter, FilterTeam, FilterTeam.team_id_team,
                                            Team, Team.id_team):
                    filterData.filterTeam.append(IntInterval(team.id_team, team.id_team))

                filter.dataFilter = getFilterData(filter, FilterData, FilterData.data_bet_id_data_bet,
                                                  DataBet, DataBet.id_data_bet)
                for data in filter.dataFilter:
                    filterData.filtersData.append(AllFilters[getDataById(data.type_data_bet_id_type_data_bet,
                                                  TypeDataBet,
                                                  TypeDataBet.id_type_data_bet).type_code](data.start, data.end))

            resource = getResourceByID(capper.resource_id_resource)[0]
            link = generateLink(capper, resource)

            ClassGet = getTypeByNameResource(resource.name)

            requests.allwaysLoadPage(link)

            # if type(ClassGet) != type(oldClassGet):
            #     ClassGet.makePreAction(ClassGet, requests, (resource.login, resource.password))

            requests.allwaysLoadPage(ClassGet.makeLinkPicks(ClassGet, link))

            startTrackTime()
            for pick in ClassGet.parsePicks(self=ClassGet, requests=requests):
                addBet(capper, pick, False, filters)
            print("End parse current: " + str(endTrackTime()))

            requests.allwaysLoadPage(ClassGet.makeLinkArchive(ClassGet, link, getDateTimeNow()))

            startTrackTime()
            for pick in ClassGet.parseArchive(self=ClassGet, requests=requests, lastBet=BetToPick(getLastInputResultBetForCupper(capper))):
                addBet(capper, pick, True)
            print("End parse archive: " + str(endTrackTime()))

            #oldClassGet = ClassGet
        print("TIME WORK: " + str(getTimeWork()))
        time.sleep(random.randint(15, 20) * 60)
