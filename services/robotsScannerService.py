import requests
from core.service import IService
from helpers.requestHelper import RobotsHelper
from models.RobotsTxt import RobotsTxt


class RobotsReaderService(IService):

    def __init__(self, logger) -> None:
        super().__init__(logger)
        self.__text = ""
        self.__injectedRobotsPath = ""
        self.__robotsObject = RobotsTxt()
        self.__current_user = ""
        self.__current_disallow_rule = ""
        self.__current_allow_rule = ""

    def InjectRobotPath(self, url: str):
        self.__injectedRobotsPath = f'{url} + /robots.txt'
        self.__text = ""

    def __ReadPath(self):
        pass

    def __ConvertTextToObject(self, text: str):
        lines = text.split('\n')
        for line in lines:
            if line.startswith('User-agent:'):
                self.__current_user = line.split(': ')[1]
            elif line.startswith('Disallow'):
                self.__current_disallow_rule = line.split(': ')[1:]
                self.__robotsObject.AddRule(self.__current_user, self.__current_disallow_rule, None)
            elif line.startswith('Allow:'):
                self.__current_allow_rule = line.split(': ')[1:]
                self.__robotsObject.AddRule(self.__current_user, None, self.__current_allow_rule)
            elif line.startswith('Crawl-delay:'):
                self.__robotsObject.set_rate_limit(line.split(': ')[1:])
            elif line.startswith('Sitemap:'):
                self.__robotsObject.add_sitemap(line.split(': ')[1:])

        print(self.__robotsObject.get_data())

    def ExecuteOperation(self):
        try:
            if self.__injectedRobotsPath is not None or "":
                self.__text = RobotsHelper.ReadRobots(self.__injectedRobotsPath)
                self.__ConvertTextToObject(self.__text)
        except Exception as e:
            print(e)
            pass
        pass

    def ReturnObject(self):
        return self.__robotsObject

    def ReturnText(self):
        return self.__text
