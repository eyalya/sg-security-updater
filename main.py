from src.securityGroupUpdater import UpdateSecurityGroupIp
from src.session import Session

g_security_groups_to_update = ["sg-12345678"]
g_aws_computer_profile      = "default"
g_sg_rule_description       = ""
g_new_ip                    = None
g_mfa_serial                = None
g_mfa_token                 = None

if __name__ == '__main__':

    session = Session(g_aws_computer_profile, g_mfa_serial)
    if g_mfa_serial:
        session.MFALogin(g_mfa_token)

    sg_updater = UpdateSecurityGroupIp(session.GetSession(), newIp=g_new_ip)
    for sg in g_security_groups_to_update:
        sg_info = sg_updater.GetSecurityGroup(sg)
        sg_updater.ChangeRule(g_sg_rule_description, sg_info["SecurityGroups"]) 