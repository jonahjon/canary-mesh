data "aws_region" "current" {}

data "aws_vpc" "current" {
  id = "${var.vpc_id}"
}

# Define common tags to be used for all (supported) resources
locals {
  common_tags = {
    BuiltWith = "terraform"
  }

  default_tags = "${merge(
    local.common_tags,
    map(
      "Name", "${var.cluster_name}",
      "Environment", "${var.environment}"
    )
  )}"
}

# Special case for ASG tags (https://github.com/hashicorp/terraform/issues/15226)
data "null_data_source" "asg_tags" {
  count = "${length(keys(local.default_tags))}"

  inputs = {
    key                 = "${element(keys(local.default_tags), count.index)}"
    value               = "${element(values(local.default_tags), count.index)}"
    propagate_at_launch = "true"
  }
}
