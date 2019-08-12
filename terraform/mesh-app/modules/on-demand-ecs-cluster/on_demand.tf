resource "aws_launch_configuration" "on_demand_launch_config" {
  name_prefix   = "${var.cluster_name}_on_demand_launch_config"
  image_id      = "${data.aws_ssm_parameter.ecs_optimized_ami.value}"
  instance_type = "${var.on_demand_instance_type}"

  iam_instance_profile = "${aws_iam_instance_profile.ecs.arn}"
  security_groups      = var.security_group_ids
  user_data            = "${data.template_file.ecs_instance_user_data.rendered}"

  root_block_device {
    volume_type = "${var.volume_type}"
    volume_size = "${var.volume_size}"
  }

  lifecycle {
    create_before_destroy = true
  }
}
