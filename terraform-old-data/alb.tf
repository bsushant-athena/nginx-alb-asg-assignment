locals {
  this_alb_name = "nginx-elb"
  this_tg       = "nginx-tg"
}

# using ALB - instances in private subnets
resource "aws_lb" "nginx-elb" {
  name               = local.this_alb_name
  internal           = false
  load_balancer_type = "application"
  subnets            = [var.subnet_pub1c, var.subnet_pub1a]
  security_groups    = [aws_security_group.nginx-elb-sg.id]
  tags = {
    Name = "nginx-elb"
  }
}

# listener
resource "aws_lb_listener" "nginx-listener" {
  load_balancer_arn  = aws_lb.nginx-elb.arn
  port               = "80"
  protocol           = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.nginx-tg.arn
  }
}
  
# alb target group
resource "aws_lb_target_group" "nginx-tg" {
  name        = "nginx-tg"
  port        = 80
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = var.vpc_id
  health_check {
    path = "/"
    port = 80
  }
}

# security group for application load balancer
resource "aws_security_group" "nginx-elb-sg" {
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