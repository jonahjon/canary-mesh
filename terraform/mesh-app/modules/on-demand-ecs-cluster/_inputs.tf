# ---------------------------------------------------------------------------------------------------------------------
# REQUIRED PARAMETERS
# These parameters must be set.
# ---------------------------------------------------------------------------------------------------------------------
variable "cluster_name" {
  description = "The name to use for the ECS cluster."
}

variable "environment" {
  description = "The name of the environment this configuration is for (e.g. stage, prod)"
}

variable "cloudwatch_prefix" {
  description = "Prefix to be used for CloudWatch log aggregation"
}

variable "vpc_id" {
  description = "The ID of the VPC in which the nodes will be deployed."
}

variable "high_memory_threshold" {
  description = "CPU utilization above this percentage will initiate scaling out/up (larger)"
}

variable "low_memory_threshold" {
  description = "CPU utilization above this percentage will initiate scaling in/down (smaller)"
}

variable "scaling_adjustment" {
  description = "Percentage of cluster to scale by"
}

variable "subnet_ids" {
  description = "The subnet IDs into which the EC2 Instances should be deployed."
  type        = "list"
}

# ---------------------------------------------------------------------------------------------------------------------
# OPTIONAL PARAMETERS
# These parameters have reasonable defaults, but may be explicitly set if desired.
# ---------------------------------------------------------------------------------------------------------------------

variable "security_group_ids" {
  description = "The IDs of the security group to allow connection from for EC2 instances."
  type        = "list"
  default     = []
}

variable "ami_id" {
  description = "The ID of the AMI to run in the cluster. If the default value is used, we will look up the latest AMI automatically."
  default     = ""
}

variable "ecs_log_drivers" {
  description = "Log drivers to enable for ECS container tasks"
  default     = "[\"json-file\",\"splunk\",\"awslogs\"]"
}

variable "volume_type" {
  description = "Type of root volume to provision for spot/on-demand instances"
  default     = "gp2"
}

variable "volume_size" {
  description = "Size of root volume to provision for spot/on-demand instances"
  default     = "30" # GB
}

variable "on_demand_instance_type" {
  description = "Instance type to use for on-demand portion of cluster"
  default     = "c4.2xlarge"
}

variable "on_demand_desired" {
  description = "Desired (starting) number of on-demand instances"
  default     = "3"
}

variable "on_demand_min" {
  description = "Minimum number of on-demand instances"
  default     = "3"
}

variable "on_demand_max" {
  description = "Maximum number of on-demand instances"
  default     = "5"
}
