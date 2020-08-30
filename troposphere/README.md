This is setup will allow you to deploy autoscalable nginx server with ALB in front. Python code generates the cloudformation template in yaml format which can be used to create a cfn stack.


Technology used:
1) Python package Troposphere - because it is easy to configure and deploy aws resources and it supports most of the aws services
https://github.com/cloudtools/troposphere
2) AWS CLI allows us to deploy cloudformation stack using the cfn template file generate by python code. Here we can see the logs and also allows to delete all the resources at one click.


Directories:
1) All python code is available in file Autoscaling.py under troposphere directory 
2) 'terraform-old-data' folder contains terraform template file to deploy the same setup using only terraform.


Assumption:
There is already an aws account available with basic vpc , networking setup etc.


Installation:
1) Install python 3.7
2) Install aws cli
3) Install the required python packages
4) Create an ec2 key-pair in aws
5) Create an IAM user in aws and save the credential under ~/.aws/credentials file with a profile name, here I'm using a saml role which has full administrator access to an aws account 
7) Make sure you setup the region through 'aws configure' command
6) Run the python code as 'python3 Autoscaling.py' ; this will generate the yaml file in same directory
7) Now follow instructions.txt file for further steps.