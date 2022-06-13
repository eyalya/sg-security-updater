import json
from requests import get

class ComputerInfo():
        
    @classmethod
    def GetMyIp(cls):
            ip = get('https://api.ipify.org').text
            ip += "/32"   
            return ip

    @classmethod
    def RetrieveOldIp(cls, file):
        with open(file) as json_file:
            data = json.load(json_file)
            return data
    
    @classmethod
    def WriteToJasonFile(cls, file, data):
        with open(file, 'w') as outfile:
            json.dump(data, outfile)