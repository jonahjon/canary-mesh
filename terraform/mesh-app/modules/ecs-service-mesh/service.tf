data "template_file" "task_definition" {
  template = var.task_definition_template_file

  vars = {
    aws_region           = var.aws_region
    service_name         = var.service_name
    cloudwatch_log_group = "/ecs/${var.service_name}"
    account_id           = var.account_id
    image                = var.image
    meshName             = aws_appmesh_mesh.mesh.id
    virtualNodeName      = aws_appmesh_virtual_node.blue.name
    envoy_log_level      = var.envoy_log_level

  }
}

resource "aws_ecs_task_definition" "initial_task_definition" {
  depends_on            = [aws_cloudwatch_log_group.service]
  family                = var.service_name
  container_definitions = data.template_file.task_definition.rendered
  task_role_arn         = aws_iam_role.task_role.id
  network_mode          = "awsvpc"
  proxy_configuration {
    type           = "APPMESH"
    container_name = "envoy"
    properties = {
      AppPorts         = "80"
      EgressIgnoredIPs = "169.254.170.2,169.254.169.254"
      IgnoredUID       = "1337"
      ProxyEgressPort  = 15001
      ProxyIngressPort = 15000
    }
  }
}

resource "aws_ecs_service" "service" {
  task_definition = "${aws_ecs_task_definition.initial_task_definition.arn}"

  name          = var.service_name
  cluster       = var.cluster_arn
  desired_count = var.desired_count

  load_balancer {
    target_group_arn = aws_lb_target_group.tg1.arn
    container_name   = var.service_name
    container_port   = var.container_port
  }

  deployment_controller {
    type = "CODE_DEPLOY"
  }

  network_configuration {
    subnets         = var.private_subnet_ids
    security_groups = [var.security_group_ids]
  }

  service_registries {
    registry_arn = aws_service_discovery_service.discovery_service.arn
  }

  depends_on = [aws_lb_target_group.tg1]

  lifecycle {
    ignore_changes = [
      "task_definition",
      "desired_count",
      "load_balancer",
    ]
  }
}
