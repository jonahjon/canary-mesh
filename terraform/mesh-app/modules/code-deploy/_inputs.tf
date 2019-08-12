#### ALB Listeners #####
variable "prod_traffic_listener" {
  type        = list(string)
  description = "The ALB listener serving production traffic"
}
variable "test_traffic_listener" {
  type        = list(string)
  description = "The ALB listener spun up to test traffic"
}

#### ALB Target Groups #####
variable "target_group_1" {
  type        = string
  description = "The 1st TG used by Codedeploy for BG"
}
variable "target_group_2" {
  type        = string
  description = "The 2nd TG used by Codedeploy for BG"
}

#### ECS Information #####
variable "cluster_name" {
  type        = string
  description = "The ECS cluster name used by codedeploy"
}
variable "service_name" {
  type        = string
  description = "The ECS service name used by codedeploy"
}

##### VPC ID ######
variable "vpc_id" {
  type        = string
  description = "The ID of the VPC in which the nodes will be deployed."
}
