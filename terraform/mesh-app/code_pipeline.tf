module "code_pipeline" {
  source                            = "./modules/code-pipeline"
  name                              = "${module.mesh.service_name}"
  cluster_name                      = module.ecs_cluster.cluster_name
  repository                        = aws_ecr_repository.repo.name
  artifact_bucket_prefix            = local.service_name
  image_tag                         = "latest"
  code_deploy_app_name              = module.codedeploy_bluegreen.code_deploy_app_name
  code_deploy_deployment_group_name = module.codedeploy_bluegreen.code_deploy_deployment_group_name
}
