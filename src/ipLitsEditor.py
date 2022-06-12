import boto3
import json
from botocore.exceptions import ClientError
from utils import ComputerInfo

class IpListUpdator():
    def __init__(self, aws_profile):
        self._client = boto3.session.Session(profile_name=aws_profile)
        self._waf = self._client.client('wafv2')

    
    def UpdateIpSet(self, srcfile, name, newip, ipName, ipSetId):
        ips = ComputerInfo.RetrieveOldIp(srcfile)
        self.ChengedIpSet(newip, ipName, ipSetId, oldIP=ips[name])
        ips[name] = newip
        ComputerInfo.WriteToJasonFile(srcfile, ips)

    def ChengedIpSet(self, newIp, ipName, ipSetId, scope='CLOUDFRONT', oldIP=""):
        
        ipSet = self.GetIpSet(ipName, ipSetId, scope)
        token = ipSet["LockToken"]
        addresses = ipSet["IPSet"]["Addresses"]

        if oldIP:
            try: 
                addresses.remove(oldIP)
            except ValueError as e:
                print(e)
        addresses.append(newIp)

        with open('addresses.txt', 'w') as f:
            for item in addresses:
                f.write("%s\n" % item)

        response = self._waf.update_ip_set(
            Name=ipName,
            Scope=scope,
            Id=ipSetId,
            Description=ipSet["IPSet"]["Description"],
            Addresses=addresses,
            LockToken=token
            )

        parsed = json.dumps(response, indent = 4) 
        print("ip response")
        print(parsed) 

# {
#     'IPSet': {
#         'Name': 'string',
#         'Id': 'string',
#         'ARN': 'string',
#         'Description': 'string',
#         'IPAddressVersion': 'IPV4'|'IPV6',
#         'Addresses': [
#             'string',
#         ]
#     },
#     'LockToken': 'string'
# }

    def GetIpSet(self, name, ipSetId, scope='CLOUDFRONT'):
        return self._waf.get_ip_set(Name=name, Scope=scope, Id=ipSetId)

    def ListIp(self):
        response = self._waf.list_ip_sets(Scope='CLOUDFRONT')
        return response