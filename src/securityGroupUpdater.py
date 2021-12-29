import boto3
import json
from botocore.exceptions import ClientError
from src.utils import ComputerInfo

class UpdateSecurityGroupIp():
    def __init__(self, aws_profile, newIp=None):
        self._client = boto3.session.Session(profile_name=aws_profile)
        self._ec2 = self._client.client('ec2')
        self._ip = newIp or ComputerInfo.GetMyIp()
        
    def SearchInRule(self, rule, name):
        return ("Description" in rule) and (rule["Description"] == name)

    def IndexOfFirst(self, lst, pred, *args):
        for i,v in enumerate(lst["IpRanges"]):
            if pred(v, *args):
                return True, i
        return False, 0

    def SearchRule(self, permissions ,name):
        return self.IndexOfFirst(permissions, self.SearchInRule, name)
    
    def GetIpPremissionIndex(self, sg, name):
        ruleGroup = 0
        for rule in sg:
            found, ruleIndex = self.SearchRule(rule, name)
            if found:
                return ruleIndex, ruleGroup
            ruleGroup += 1
        return None, None

    def GetSecurityGroup(self, sg_id):
        response = ""
        try:
            response = self._ec2.describe_security_groups(GroupIds=[sg_id])
        except ClientError as e:
            print("GetSecurityGroup fails")
            print(e)
            return ""
        return response

    def ChangeRule(self, name, sg):
        ingressIp = sg[0]["IpPermissions"]
        print("old permmision for sg: {}".format(sg[0]["GroupId"]))
        print(json.dumps(ingressIp, indent = 4))

        ruleIndex, ruleGroup = self.GetIpPremissionIndex(ingressIp, name)
        newIpRule = list()
        if ruleIndex != None:
            newIpRule.append(ingressIp[ruleGroup])
            try:
                response = self._ec2.revoke_security_group_ingress(GroupId=sg[0]["GroupId"], IpPermissions=newIpRule)
            except ClientError as e:
                print("Revoke rule fails")
                print(e)
                return
        else:
            print("no old permission found, program exits")
            return

        newIpRule[0]["IpRanges"][ruleIndex]["CidrIp"] = self._ip
        
        try:
            response = self._ec2.authorize_security_group_ingress(GroupId=sg[0]["GroupId"], IpPermissions=newIpRule)
        except ClientError as e:
            print("ChangeRule fails")
            print(e)
            return 

        if (response["ResponseMetadata"]["HTTPStatusCode"] == 200):
            print("Security group {} updated".format(sg[0]["GroupId"]))
        else:
            print("Updating failed, response message:")
            parsed = json.dumps(response, indent = 4) 
            print(parsed) 


