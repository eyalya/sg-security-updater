import json
from requests import get

class ComputerInfo():
        
    @classmethod
    def GetMyIp(cls):
            ip = get('https://api.ipify.org').text
            ip += "/32"   
            return ip