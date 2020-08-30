from troposphere import Base64, FindInMap, GetAtt, Join, Output
from troposphere import Parameter, Ref, Template
from troposphere import cloudformation, autoscaling
from troposphere.autoscaling import AutoScalingGroup, Tag
from troposphere.autoscaling import LaunchConfiguration
from troposphere.policies import (
    AutoScalingReplacingUpdate, AutoScalingRollingUpdate, UpdatePolicy
)
import troposphere.ec2 as ec2
import troposphere.elasticloadbalancingv2 as elb

def main():
    # Initialize template
    template = Template()
    template.set_version("2010-09-09")
    template.set_description("""\
    Configures autoscaling group for nginx app""")

    # Collect template properties through parameters
    InstanceType = template.add_parameter(Parameter(
        "InstanceType",
        Type="String",
        Description="WebServer EC2 instance type",
        Default="t2.small",
        AllowedValues=[
            "t2.micro", "t2.small", "t2.medium", "t2.large", "t2.xlarge"
        ],
        ConstraintDescription="Must be a valid EC2 instance type.",
    ))

    KeyName = template.add_parameter(Parameter(
        "KeyName",
        Type="String",
        Description="Name of an existing EC2 KeyPair to enable SSH access",
        MinLength="1",
        AllowedPattern="[\x20-\x7E]*",
        MaxLength="255",
        ConstraintDescription="Can contain only ASCII characters.",
    ))

    ScaleCapacity = template.add_parameter(Parameter(
        "ScaleCapacity",
        Default="1",
        Type="String",
        Description="Number of nginx servers to run",
    ))

    PublicSubnet1 = template.add_parameter(Parameter(
        "PublicSubnet1",
        Type="String",
        Description="A public VPC subnet ID for the nginx app load balancer.",
    ))

    PublicSubnet2 = template.add_parameter(Parameter(
        "PublicSubnet2",
        Type="String",
        Description="A public VPC subnet ID for the nginx load balancer.",
    ))

    VPCAvailabilityZone2 = template.add_parameter(Parameter(
        "VPCAvailabilityZone2",
        MinLength="1",
        Type="String",
        Description="Second availability zone",
        MaxLength="255",
    ))

    VPCAvailabilityZone1 = template.add_parameter(Parameter(
        "VPCAvailabilityZone1",
        MinLength="1",
        Type="String",
        Description="First availability zone",
        MaxLength="255",
    ))

    NginxSubnet2 = template.add_parameter(Parameter(
        "NginxSubnet2",
        Type="String",
        Description="Second private VPC subnet ID for the nginx app.",
    ))

    NginxSubnet1 = template.add_parameter(Parameter(
        "NginxSubnet1",
        Type="String",
        Description="First private VPC subnet ID for the nginx app.",
    ))

    VpcId = template.add_parameter(Parameter(
        "VpcId",
        Type="String",
        Default="vpc-2971b452",
        Description="VPC Id.",
    ))

    AmiId = template.add_parameter(Parameter(
        "AmiId",
        Type="String",
        Default="ami-e262039d",
        Description="AMI Id.",
    ))

    StackName = template.add_parameter(Parameter(
        "StackName",
        Type="String",
        Default="nginx-example",
        Description="StackName used for tagging resources.",
    ))

    # Create a common security group
    NginxInstanceSG = template.add_resource(
        ec2.SecurityGroup(
            "InstanceSecurityGroup",
            GroupDescription="Enable SSH and HTTP access on the inbound port",
            SecurityGroupIngress=[
                ec2.SecurityGroupRule(
                    IpProtocol="tcp",
                    FromPort="22",
                    ToPort="22",
                    CidrIp="10.0.0.0/8",
                ),
                ec2.SecurityGroupRule(
                    IpProtocol="tcp",
                    FromPort="80",
                    ToPort="80",
                    CidrIp="0.0.0.0/0",
                )
            ],
            VpcId=Ref(VpcId),
            Tags=[
                Tag("Name", Join(Ref(StackName),'-sg'), True)
            ]
        )
    )

    # Add the application LB
    ApplicationElasticLB = template.add_resource(elb.LoadBalancer(
        "ApplicationElasticLB",
        Name="ApplicationElasticLB",
        Scheme="internet-facing",
        Subnets=[Ref(PublicSubnet1), Ref(PublicSubnet2)],
        SecurityGroups=[Ref(NginxInstanceSG)],
        Tags=[
            Tag("Name", Join(Ref(StackName),'-lb'), True)
        ]
    ))
    
    # Add Target Group for the ALB
    TargetGroupNginx = template.add_resource(elb.TargetGroup(
        "TargetGroupNginx",
        HealthCheckIntervalSeconds="30",
        HealthCheckProtocol="HTTP",
        HealthCheckTimeoutSeconds="10",
        HealthyThresholdCount="4",
        Matcher=elb.Matcher(
            HttpCode="200"),
        Name="NginxTarget",
        Port="80",
        Protocol="HTTP",
        UnhealthyThresholdCount="3",
        VpcId=Ref(VpcId),
        Tags=[
            Tag("Name", Join(Ref(StackName),'-tg'), True)
        ]
    ))

    # Add ALB listener
    Listener = template.add_resource(elb.Listener(
        "Listener",
        Port="80",
        Protocol="HTTP",
        LoadBalancerArn=Ref(ApplicationElasticLB),
        DefaultActions=[elb.Action(
            Type="forward",
            TargetGroupArn=Ref(TargetGroupNginx)
        )]
    ))

    # Add launch configuration for auto scaling
    LaunchConfig = template.add_resource(LaunchConfiguration(
        "LaunchConfiguration",
        ImageId=Ref(AmiId),
        KeyName=Ref(KeyName),
        AssociatePublicIpAddress="False",
        LaunchConfigurationName=Join(Ref(StackName),'-lc')
        UserData=Base64(Join('', [
            "#!/bin/bash\n",
            "yum update\n",
            "yum -y install nginx\n",
            "curl http://169.254.169.254/latest/meta-data/local-ipv4\n",
            "chkconfig nginx on\n",
            "service nginx start"
        ])),
        SecurityGroups=[Ref(NginxInstanceSG)],
        InstanceType=Ref(InstanceType)
    ))

    # Add auto scaling group 
    AutoscalingGroup = template.add_resource(AutoScalingGroup(
        "AutoscalingGroup",
        DesiredCapacity=Ref(ScaleCapacity),
        Tags=[
            Tag("Name", Join(Ref(StackName),'-asg'), True)
        ],
        LaunchConfigurationName=Ref(LaunchConfig),
        MinSize=Ref(ScaleCapacity),
        TargetGroupARNs=[Ref(TargetGroupNginx)],
        MaxSize=Ref(ScaleCapacity),
        VPCZoneIdentifier=[Ref(NginxSubnet1), Ref(NginxSubnet2)],
        AvailabilityZones=[Ref(VPCAvailabilityZone1), Ref(VPCAvailabilityZone2)],
        HealthCheckType="EC2"
    ))

    template.add_output(Output(
        "URL",
        Description="URL of the sample website",
        Value=Join("", ["http://", GetAtt(ApplicationElasticLB, "DNSName")])
    ))

    #print(template.to_json())

    with open('AutoScaling.yaml', 'w') as f:
        f.write(template.to_yaml())

if __name__ == '__main__':
    main()