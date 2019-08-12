resource "aws_ecr_repository" "repo" {
  name = local.service_name
}
