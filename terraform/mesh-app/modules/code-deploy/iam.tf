
resource "aws_iam_role" "codedeploy" {
  name = "${local.service_prefix}-codedeploy"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "codedeploy.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# CodeDeploy permissions
# combination of https://docs.aws.amazon.com/AmazonECS/latest/developerguide/codedeploy_IAM_role.html
# https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html
# and additional permissions to enable lambda-based custom CodeDeploy hooks for Jenkins integration
resource "aws_iam_role_policy" "codedeploy" {
  name = "${local.service_prefix}-codedeploy"
  role = "${aws_iam_role.codedeploy.id}"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
              "ecs:*",
              "elasticloadbalancing:*",
              "iam:PassRole",
              "ecr:GetAuthorizationToken",
              "ecr:BatchCheckLayerAvailability",
              "ecr:GetDownloadUrlForLayer",
              "ecr:BatchGetImage",
              "logs:CreateLogStream",
              "logs:PutLogEvents",
              "s3:ListBucket",
              "s3:PutObject",
              "s3:GetObject",
              "lambda:ListFunctions",
              "lambda:ListTags",
              "lambda:GetEventSourceMapping",
              "lambda:ListEventSourceMappings",
              "lambda:InvokeFunction"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:DescribeLogStreams"
            ],
            "Resource": [
                "arn:aws:logs:*:*:*"
            ]
        }
    ]
}
EOF
}
