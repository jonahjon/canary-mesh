data "aws_vpc" "current" {
  id = "${var.vpc_id}"
}

# Define common tags to be used for all (supported) resources
locals {
  common_tags = {
    BuiltWith = "terraform"
  }

  service_prefix = "${var.cluster_name}-${var.service_name}"
}
