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