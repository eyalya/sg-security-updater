### Security Group Updater

Use aws cli to update security groups that in the list from terminal. 

## Instructions: 
3 variables should be set on main.py. 
1. g_security_groups_to_update = List of security groups you would like to update
2. g_aws_computer_profile = Shoudl be set to "default" unless aws condfigured with a diferent profile in ~/.aws/credentials
3. g_sg_rule_description = Should conatain the description of the security groups rule of which you want to update.

For Example: 
g_security_groups_to_update = ["sg-1223456789"]
g_aws_computer_profile = "default"
g_sg_rule_description = "john_do"

## IAM User
IAM user should have permissions to change the security group. 
An example for a security permision which allow the updating of security group sg-123456789

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:RevokeSecurityGroupIngress",
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:RevokeSecurityGroupEgress",
                "ec2:DeleteSecurityGroup",
                "ec2:ModifySecurityGroupRules"
            ],
            "Resource": "arn:aws:ec2:*:*:security-group/sg-123456789"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "ec2:RevokeSecurityGroupIngress",
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:RevokeSecurityGroupEgress",
                "ec2:DeleteSecurityGroup",
                "ec2:ModifySecurityGroupRules"
            ],
            "Resource": "arn:aws:ec2:*:*:security-group/sg-123456789"
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeSecurityGroupRules",
                "ec2:DescribeSecurityGroupReferences",
                "ec2:DescribeVpcs",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeStaleSecurityGroups"
            ],
            "Resource": "*"
        }
    ]
}