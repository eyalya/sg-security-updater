import boto3
from botocore.exceptions import ClientError

class Session():
    def __init__(self, aws_profile, serial_number=None):
        self._client = boto3.session.Session(profile_name=aws_profile)
        self._sts = self._client.client('sts')
        self._sn = serial_number 
        
    def MFALogin(self, token_code):
        res = self._sts.get_session_token(SerialNumber=self._sn, TokenCode=str(token_code))
        self._client = boto3.session.Session(
            aws_access_key_id=res["Credentials"]["AccessKeyId"],
            aws_secret_access_key=res["Credentials"]["SecretAccessKey"],
            aws_session_token=res["Credentials"]["SessionToken"]
        )

    def GetSession(self):
        return self._client
    