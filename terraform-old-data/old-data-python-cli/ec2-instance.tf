resource "aws_instance" "nginx" {
   ami = var.ami_id
   subnet_id = var.subnet_prv1a
   instance_type = var.ec2isntance_type
   count = var.ec2instance_count
   key_name = var.ssh_key
   # Our Security group to allow HTTP and SSH access
   vpc_security_group_ids = [aws_security_group.nginx-ec2-sg.id]
}

resource "aws_security_group" "nginx-ec2-sg" {
  name        = "nginx_elb_security_group"
  description = "Used in the nginx"
  vpc_id      = var.vpc_id

  # SSH access within corporate
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }

  # HTTP access from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # outbound internet access
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}