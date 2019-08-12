output "alb_dns_name" {
  value = module.mesh.alb_dns_name
}
output "service_name" {
  value = module.mesh.service_name
}
output "containerPort" {
  value = var.containerPort
}
output "aws_log_group" {
  value = module.mesh.aws_log_group
}
output "aws_region" {
  value = var.aws_region
}
output "mesh_name" {
  value = module.mesh.mesh_name
}
output "virtual_node_name" {
  value = module.mesh.virtual_node_name
}
output "envoy_log_level" {
  value = module.mesh.envoy_log_level
}
output "artifact_bucket_name" {
  value = module.code_pipeline.artifact_bucket_name
}
