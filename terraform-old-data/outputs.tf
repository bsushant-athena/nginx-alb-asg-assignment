output "alb_name" {
  value = aws_lb.nginx-elb.dns_name
}