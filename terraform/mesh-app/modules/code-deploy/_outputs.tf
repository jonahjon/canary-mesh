output "code_deploy_app_name" {
  value = "${aws_codedeploy_app.application.name}"
}

output "code_deploy_deployment_group_name" {
  value = "${aws_codedeploy_deployment_group.deploy_group.deployment_group_name}"
}
