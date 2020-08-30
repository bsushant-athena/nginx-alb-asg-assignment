output "instance_ip_addr" {
  value       = aws_instance.nginx[0].private_ip
  description = "The private IP address of the main server instance."
}