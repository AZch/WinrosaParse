import datetime
import time

timeStart = time.time()
trackTimeStart = time.time()

def getTimeWork(roundNum=1):
    return round(time.time() - timeStart, roundNum)

def startTrackTime():
    global trackTimeStart
    trackTimeStart = time.time()

def endTrackTime():
    return time.time() - trackTimeStart

def getDateTimeNow():
    return datetime.datetime.now()

def dateTimeByStr(string):
    return datetime.datetime(string)

def dateByDayMonthYearHourMinute(day, month, year, hour, minute):
    return datetime.datetime(year, month, day, hour, minute)

def sleepBySecond(second=0.1):
    time.sleep(second)