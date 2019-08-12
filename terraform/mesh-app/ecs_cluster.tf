module "ecs_cluster" {
  source = "./modules/on-demand-ecs-cluster"

  cluster_name      = "${local.cluster_name}"
  environment       = "${local.environment}"
  cloudwatch_prefix = "${local.cluster_name}"

  vpc_id     = "${module.sample_vpc.vpc_id}"
  subnet_ids = "${module.sample_vpc.private_subnets}"

  # allow service load-balancers to talk to cluster instances
  security_group_ids = [
    aws_security_group.instance.id
  ]

  high_memory_threshold = 75
  low_memory_threshold  = 25
  scaling_adjustment    = 40

  on_demand_desired = 3
  on_demand_min     = 3
  on_demand_max     = 3
}


resource "aws_security_group" "instance" {
  description = "ECS EC2 instance security group"
  vpc_id      = module.sample_vpc.vpc_id
  name        = "${local.cluster_name}-instance-sg"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
