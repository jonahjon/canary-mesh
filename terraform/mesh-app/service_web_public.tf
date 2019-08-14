module "mesh" {
  source = "./modules/ecs-service-mesh"

  # App Mesh
  mesh_name           = local.mesh_name
  virtual_router_name = local.service_name
  virtual_node_name   = local.service_name

  # ServiceDiscovery
  service_namespace = "service"

  # ECS Service Settings
  cluster_arn                   = module.ecs_cluster.cluster_id
  service_name                  = local.service_name
  environment                   = local.environment
  aws_region                    = data.aws_region.current.name
  account_id                    = data.aws_caller_identity.current.account_id
  image                         = local.service_name
  task_definition_template_file = "${file("files/mesh.json")}"
  desired_count                 = 3

  #### LB Settings ####
  lb_name             = local.service_name
  protocol            = "HTTP"
  container_port      = var.containerPort
  container_test_port = 9000
  lb_type             = "application"
  internal            = "false"
  health_check_path   = "/"

  #### Security Groups and Networking
  security_group_ids = aws_security_group.instance.id
  vpc_id             = module.sample_vpc.vpc_id
  public_subnet_ids  = module.sample_vpc.public_subnets
  private_subnet_ids = module.sample_vpc.private_subnets
}
