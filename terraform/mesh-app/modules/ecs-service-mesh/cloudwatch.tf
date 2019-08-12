resource "aws_cloudwatch_log_group" "service" {
  name              = "/ecs/${var.service_name}"
  retention_in_days = 90
}

resource "aws_cloudwatch_log_group" "service_envoy" {
  name              = "/ecs/${var.service_name}-envoy"
  retention_in_days = 90
}

resource "aws_cloudwatch_log_group" "service_xray" {
  name              = "/ecs/${var.service_name}-xray"
  retention_in_days = 90
}

resource "aws_iam_role_policy" "task_role_policies" {
  name   = "${var.service_name}_task_role_policies"
  role   = "${aws_iam_role.task_role.id}"
  policy = "${data.aws_iam_policy_document.task_role_policies.json}"
}

data "aws_iam_policy_document" "task_role_policies" {
  statement {
    sid = "LogToCloudWatch"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["*"]
  }
}
