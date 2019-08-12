output "cluster_id" {
  value = "${aws_ecs_cluster.ecs_cluster.id}"
}

# Cluster.name is not a supported syntax currerntly https://www.terraform.io/docs/providers/aws/r/ecs_cluster.html
output "cluster_name" {
  value = "${var.cluster_name}"
}

output "autoscaling_group_name" {
  value = "${aws_autoscaling_group.on_demand_asg.name}"
}
