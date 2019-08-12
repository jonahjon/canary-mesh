output "ecs_task_iam_role_name" {
  value       = aws_iam_role.task_role.name
  description = "Name of the IAM task role created"
}

output "prod_traffic_listener" {
  value       = aws_lb_listener.prod_listener.arn
  description = "ARN of the IAM task role created"
}

output "test_traffic_listener" {
  value       = aws_lb_listener.test_listener.arn
  description = "ARN of the IAM task role created"
}

output "target_group_1" {
  value       = aws_lb_target_group.tg1.name
  description = "ARN of the IAM task role created"
}

output "target_group_2" {
  value       = aws_lb_target_group.tg2.name
  description = "ARN of the IAM task role created"
}

output "service_name" {
  value       = aws_ecs_service.service.name
  description = "ARN of the IAM task role created"
}

output "security_group_id" {
  value = "${aws_security_group.lb.id}"
}

output "alb_dns_name" {
  value = aws_lb.lb.dns_name
}

output "aws_log_group" {
  value = "/ecs/${var.service_name}"
}

output "envoy_log_level" {
  value = var.envoy_log_level
}

output "mesh_name" {
  value = aws_appmesh_mesh.mesh.name
}

output "virtual_node_name" {
  value = aws_appmesh_virtual_node.service.name
}
