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
        if self.__end__ is not None and \
                self.__end__ < val:
            return False
        if self.__start__ is not None and \
                self.__start__ > val:
            return False
        return True

class FloatInterval(interval):
    def __init__(self, start, end):
        interval.__init__(self, start, end)

    def convert(self, val):
        return testFloat(val)

    def calc(self, val):
        if self.__end__ is not None and \
                self.__end__ < val:
            return False
        if self.__start__ is not None and \
                self.__start__ > val:
            return False
        return True

AllFilters = {
    'TimeEvent': DateTimeInterval,
    'TimeInput': DateTimeInterval,
    'KF': FloatInterval,
    'Percent': FloatInterval
}
