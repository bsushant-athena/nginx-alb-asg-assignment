variable "ami_id" {
  description = "US-EAST1 AMI ID"
  default     = "ami-010c850ec0961e419"
}

variable "vpc_id" {
  description = "US-EAST1 VPC ID"
  default     = "vpc-2971b452"
}

variable "subnet_prv1a" {
  description = "Private Subnet 1a"
  default     = "subnet-20dc9e7d"
}

variable "subnet_prv1c" {
  description = "Private Subnet 1c"
  default     = "subnet-b093dd9f"
}

variable "subnet_pub1c" {
  description = "Public Subnet 1c"
  default     = "subnet-1993dd36"
}

variable "subnet_pub1a" {
  description = "Public Subnet 1a"
  default     = "subnet-49dc9e14"
}

variable "instance_type" {
  default     = "t2.micro"
  description = "AWS instance type"
}

variable "ssh_key" {
  description = "SSH key"
  default     = "prdsvc"
}

variable "region" {
	description = "AWS Region"
	default     = "us-east-1"
}

variable "asg_min" {
  description = "Minimum numbers of servers in ASG"
  default     = "1"
}

variable "asg_max" {
  description = "Maximum numbers of servers in ASG"
  default     = "3"
}

variable "asg_desired" {
  description = "Desired numbers of servers in ASG"
  default     = "1"
}