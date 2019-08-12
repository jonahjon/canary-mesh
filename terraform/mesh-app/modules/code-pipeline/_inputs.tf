variable "name" {
  description = "Name of the Codepipeline, and codebuild jobs"
}

variable "cluster_name" {
  type        = string
  description = "The ECS cluster name to scale during codepipeline deployment"
}

variable "repository" {
  description = "Name of the ECR to trigger the pipeline on"
}

variable "artifact_bucket_prefix" {
  description = "Prefix name of S3 bucket to store any build artifacts in (unique suffix appended automatically)"
}

variable "code_deploy_app_name" {
  description = "Code Deploy Application Name"
}

variable "code_deploy_deployment_group_name" {
  description = "Code Deploy Deployment Group Name"
}

variable "image_tag" {
  description = "Image tag to trigger pipeline on push to"
  default     = "latest"
}
