Terraform-nginx-behind-an-ALB-with-private-subnets-instances-with-ASG
VPC with 2 AZs with a public/private for each AZs

3 instances in private subnets behind a Application Load Balancer (ALB) with AutoScaling Group

A Terraform configuration to launch a cluster of EC2 instances. Each EC2 instance runs a single nginx. One EC2 instance is launched in each availability zone of the current region. The load balancer and EC2 instances are launched in a custom VPC, and use custom security groups.

Applying the configuration takes about 30 seconds (in US East), and another two or three minutes for the EC2 instances to become healthy and for the load balancer DNS record to propagate.

Files
provider.tf - AWS Provider.
alb.tf - Application load balancer (alb)
variables.tf - Used by other files, sets default AWS region, calculates availability zones, etc.
output.tf - Used to print the ALB DNS as an output
asg.tf - Auto Scaling group configuration file
backend.tf - Terraform starting point with s3 configuration for storing the state
Access credentials - add into credentials file with a saml profile
AWS access credentials must be supplied on the command line (see example below). This Terraform script was tested in my own AWS account with a user that has the AmazonEC2FullAccess and AmazonVPCFullAccess policies.

Installation
follow::https://medium.com/@krishsoftware1991/install-terraform-on-mac-machine-38eefd798555

Command Line Examples
To setup provisioner
$ terraform init

To launch the EC2 nginx cluster:
$ terraform apply 

To teardown the EC2 demo cluster:
$ terraform destroy

Regions
The default AWS region is US East Virginia (us-east-1). 

URL
Applying this Terraform configuration returns the load balancer's public URL on the last line of output. This URL can be used to view the default nginx homepage.