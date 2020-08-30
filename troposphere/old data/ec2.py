#
# ec2.py
#
# Generate a CloudFormation template that creates an EC2 instance in a
# subnet which was created previously by another template (learncf-subnet)
#
from __future__ import print_function

from troposphere import ec2
from troposphere import Tags, ImportValue
from troposphere import Template

# create the object that will generate our template
t = Template()

ec2 = ec2.Instance("ec2")
ec2.ImageId = "ami-010c850ec0961e419"                 
ec2.InstanceType = "t2.micro"
ec2.SubnetId = "subnet-20dc9e7d"
ec2.Tags = Tags(
        Name="Description",
        Comment="EC2 with CloudFormation and Troposphere")

t.add_resource(ec2)

# Finally, write the template to a file
with open('ec2.yaml', 'w') as f:
    f.write(t.to_yaml())