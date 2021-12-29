from src.securityGroupUpdater import UpdateSecurityGroupIp

g_security_groups_to_update = [""]
g_aws_computer_profile = "deafult"
g_sg_rule_description = ""

if __name__ == '__main__':

    sg_updater = UpdateSecurityGroupIp(g_aws_computer_profile)
    for sg in g_security_groups_to_update:
        sg_info = sg_updater.GetSecurityGroup(sg)
        sg_updater.ChangeRule(g_sg_rule_description, sg_info["SecurityGroups"])