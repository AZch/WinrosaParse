

def appendPick(pick, picks):
    if pick.isValid():
        picks.append(pick)

def testStr(data):
    try:
        return str(data)
    except:
        return ""

def testFloat(data):
    try:
        return float(data)
    except:
        return 0.0

def testInt(data):
    try:
        return int(data)
    except:
        return 0


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