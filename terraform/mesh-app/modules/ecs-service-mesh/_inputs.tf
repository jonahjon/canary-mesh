variable "service_name" {
  type        = string
  description = "The name to use for the service."
}

variable "aws_region" {
  type        = string
  description = ""
}

variable "environment" {
  description = "The name of the environment this configuration is for (e.g. stage, prod)"
}

variable "cluster_arn" {
  type        = string
  description = "The ECS cluster id to launch the service in."
}

variable "task_definition_template_file" {
  type        = string
  description = ""
}

variable "vpc_id" {
  type        = string
  description = "The ID of the VPC in which the nodes will be deployed."
}

variable "security_group_ids" {
  type = string
}


variable "private_subnet_ids" {
  type        = list(string)
  description = "The subnet IDs into which the EC2 Instances should be deployed."
}

variable "public_subnet_ids" {
  type        = list(string)
  description = "The subnet IDs into which the EC2 Instances should be deployed."
}

variable "desired_count" {
  type        = string
  description = "The desired task instance count for the service"
}

variable "container_port" {
  type        = number
  description = "Container port to allow in SG, and for the main listener to use"
}

variable "container_test_port" {
  type        = number
  description = "Container port to allow in SG, and for the test listener to use"
}

variable "lb_type" {
  type        = string
  description = "Which protocol of the load balancer to use"
}

variable "internal" {
  type        = string
  description = "Whether or not the load balancer is internal or external"
}

variable "health_check_path" {
  type        = string
  description = "Path of the target group health check back to the task"
}

variable "healthy_threshold" {
  type        = number
  description = "Amount of succusful health checks required before signalling a healthy service. The range is 2–10."
  default     = 3
}

variable "unhealthy_threshold" {
  type        = number
  description = "Amount of unsuccusful health checks required before signalling an unhealthy service. The range is 2–10."
  default     = 3
}

variable "health_check_interval" {
  type        = number
  description = "The approximate amount of time, in seconds, between health checks of an individual target. The range is 5–300 seconds."
  default     = 30
}

variable "protocol" {
  type        = string
  description = "Protocol for ALB listener"
}

variable "lb_name" {
  type        = string
  description = "Name for ALB resources"
}

variable "account_id" {
  type        = string
  description = "account ID"
}

variable "image" {
  type        = string
  description = "ECR image name"
}



##### MESH

variable "mesh_name" {
  type        = string
  description = "Name for App Mesh"
}

variable "virtual_router_name" {
  type        = string
  description = "Name for Virtual Router for the app mesh"
}

variable "virtual_node_name" {
  type        = string
  description = "Name for apps Virtual Node name"
}

variable "service_namespace" {
  type        = string
  description = "Name for Service Discovery Namespace"
}

variable "envoy_log_level" {
  type    = string
  default = "debug"
}

