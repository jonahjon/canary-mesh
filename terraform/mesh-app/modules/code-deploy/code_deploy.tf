# CODE DEPLOY

resource "aws_codedeploy_app" "application" {
  compute_platform = "ECS"
  name             = "${local.service_prefix}"
}

resource "aws_codedeploy_deployment_group" "deploy_group" {
  app_name               = "${aws_codedeploy_app.application.name}"
  deployment_config_name = "CodeDeployDefault.ECSAllAtOnce"
  deployment_group_name  = "${local.service_prefix}"
  service_role_arn       = "${aws_iam_role.codedeploy.arn}"

  auto_rollback_configuration {
    enabled = true
    events  = ["DEPLOYMENT_FAILURE"]
  }

  blue_green_deployment_config {
    # NOTE due to https://github.com/terraform-providers/terraform-provider-aws/issues/7128 changes to this block
    # require recreation of the deploy group resource
    # e.g. terraform taint -module service1 aws_codedeploy_deployment_group.deploy_group
    deployment_ready_option {
      action_on_timeout    = "STOP_DEPLOYMENT"
      wait_time_in_minutes = 120
    }

    terminate_blue_instances_on_deployment_success {
      action                           = "TERMINATE"
      termination_wait_time_in_minutes = 60
    }
  }

  deployment_style {
    deployment_option = "WITH_TRAFFIC_CONTROL"
    deployment_type   = "BLUE_GREEN"
  }

  ecs_service {
    cluster_name = var.cluster_name
    service_name = var.service_name
  }

  load_balancer_info {
    target_group_pair_info {
      prod_traffic_route {
        listener_arns = var.prod_traffic_listener
      }

      test_traffic_route {
        listener_arns = var.test_traffic_listener
      }

      target_group {
        name = var.target_group_1
      }

      target_group {
        name = var.target_group_2
      }
    }
  }
}
