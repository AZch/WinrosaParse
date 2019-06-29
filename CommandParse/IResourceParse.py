from abc import ABC, abstractmethod

class IResourceParse(ABC):
    @abstractmethod
    def makeLinkPicks(self, baseLink, data=None):
        pass

    @abstractmethod
    def makePreAction(self, requests, data=None):
        pass

    @abstractmethod
    def makeLinkArchive(self, baseLink, date=None):
        pass

    @abstractmethod
    def parsePicks(self, requests):
        pass

    @abstractmethod
    def parseArchive(self, requests, lastBet=None):
        pass

    @abstractmethod
    def generateLink(self, capper, resource):
        pass