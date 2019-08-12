provider "aws" {
  version = "~> 2.22.0"
  region  = "us-west-2"
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

locals {
  cluster_name = var.app_name
  service_name = var.app_name
  mesh_name    = var.app_name
  environment  = "dev"
}

