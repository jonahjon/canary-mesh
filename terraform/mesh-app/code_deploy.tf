module "codedeploy_bluegreen" {
  source                = "./modules/code-deploy"
  prod_traffic_listener = [module.mesh.prod_traffic_listener]
  test_traffic_listener = [module.mesh.test_traffic_listener]
  target_group_1        = module.mesh.target_group_1
  target_group_2        = module.mesh.target_group_2
  cluster_name          = local.cluster_name
  service_name          = module.mesh.service_name
  vpc_id                = module.sample_vpc.vpc_id
}
