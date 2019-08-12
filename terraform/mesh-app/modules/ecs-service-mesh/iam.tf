resource "aws_iam_role" "task_role" {
  name               = "${var.service_name}_task_role"
  assume_role_policy = "${data.aws_iam_policy_document.task_assume_policy.json}"
}

data "aws_iam_policy_document" "task_assume_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  role       = aws_iam_role.task_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}
