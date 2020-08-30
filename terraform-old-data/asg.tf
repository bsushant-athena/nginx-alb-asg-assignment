
# creating autoscaling group
resource "aws_autoscaling_group" "nginx-asg" {
  vpc_zone_identifier  = [var.subnet_prv1c, var.subnet_prv1a]
  name                 = "nginx-example-asg"
  max_size             = var.asg_max
  min_size             = var.asg_min
  desired_capacity     = var.asg_desired
  force_delete         = true
  launch_configuration = aws_launch_configuration.nginx-lc.name
  health_check_type    = "ELB"
  # Required to redeploy without an outage.
  lifecycle {
    create_before_destroy = true
  }
  tag {
    key                 = "Name"
    value               = "nginx-asg"
    propagate_at_launch = "true"
  }
}

# creating launch configuration
resource "aws_launch_configuration" "nginx-lc" {
  name                        = "nginx-example-lc"
  image_id                    = var.ami_id
  instance_type               = var.instance_type
  # Security group
  security_groups             = [aws_security_group.nginx-elb-sg.id]
  associate_public_ip_address = false
  user_data                   = file("userdata.sh")
  key_name                    = var.ssh_key
  lifecycle {
    create_before_destroy = true
  }
}

# autoscaling attachment  
resource "aws_autoscaling_attachment" "nginx_asg_attachment" { 
  alb_target_group_arn   = aws_lb_target_group.nginx-tg.arn
  autoscaling_group_name = aws_autoscaling_group.nginx-asg.id
}
