from abc import ABC, abstractmethod

from BaseFunction import *
from Utils.TimeUtils import *


class interval(ABC):
    __start__ = None
    __end__ = None

    @abstractmethod
    def __init__(self, start, end):
        self.__start__ = self.convert(start)
        self.__end__ = self.convert(end)

    @abstractmethod
    def convert(self, val):
        pass

    @abstractmethod
    def calc(self, val):
        pass


class DateTimeInterval(interval):
    def __init__(self, start, end):
        interval.__init__(self, start, end)

    def convert(self, val):
        return dateTimeByStr(val)

    def calc(self, val):
        val = self.convert(val)
        if self.__end__ is not None and \
                self.__end__ <= val:
            return False
        if self.__start__ is not None and \
                self.__start__ >= val:
            return False
        return True

class FloatInterval(interval):
    def __init__(self, start, end):
        interval.__init__(self, start, end)

    def convert(self, val):
        return testFloat(val)

    def calc(self, val):
        val = self.convert(val)
        if self.__end__ is not None and \
                self.__end__ <= val:
            return False
        if self.__start__ is not None and \
                self.__start__ >= val:
            return False
        return True

class IntInterval(interval):
    def __init__(self, start, end):
        interval.__init__(self, start, end)

    def convert(self, val):
        return testInt(val)

    def calc(self, val):
        val = self.convert(val)
        if self.__end__ is not None and \
                self.__end__ <= val:
            return False
        if self.__start__ is not None and \
                self.__start__ >= val:
            return False
        return True

AllFiltersCode = [
    'TimeEvent',
    'TimeInput',
    'KF',
    'Percent'
]

AllFilters = {
    AllFiltersCode[0]: DateTimeInterval,
    AllFiltersCode[1]: DateTimeInterval,
    AllFiltersCode[2]: FloatInterval,
    AllFiltersCode[3]: FloatInterval
}
