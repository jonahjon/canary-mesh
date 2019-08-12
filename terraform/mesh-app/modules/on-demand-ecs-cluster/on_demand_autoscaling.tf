# On-demand EC2 portion of ECS cluster (launched via 'static' auto-scaling group)
resource "aws_autoscaling_group" "on_demand_asg" {
  name_prefix          = "${var.cluster_name}-"
  vpc_zone_identifier  = "${var.subnet_ids}"
  launch_configuration = "${aws_launch_configuration.on_demand_launch_config.name}"
  desired_capacity     = "${var.on_demand_desired}"
  min_size             = "${var.on_demand_min}"
  max_size             = "${var.on_demand_max}"

  lifecycle {
    create_before_destroy = true
    ignore_changes        = ["desired_capacity"]
  }

  tags = "${data.null_data_source.asg_tags.*.outputs}"
}
