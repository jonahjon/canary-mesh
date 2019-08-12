# get the current AWS-provided ecs-optimized AMI id (amazon-linux)
data "aws_ssm_parameter" "ecs_optimized_ami" {
  name = "/aws/service/ecs/optimized-ami/amazon-linux/recommended/image_id"
}

data "template_file" "ecs_instance_user_data" {
  template = "${file("${path.module}/templates/instance_user_data.tpl")}"

  vars = {
    ecs_log_drivers   = "${var.ecs_log_drivers}"
    cluster_name      = "${var.cluster_name}"
    environment       = "${var.environment}"
    cloudwatch_prefix = "${var.cloudwatch_prefix}"
  }
}

resource "aws_ecs_cluster" "ecs_cluster" {
  name = "${var.cluster_name}"

  # TODO apply this tag set/merge globally
  tags = "${local.default_tags}"
}

resource "aws_iam_instance_profile" "ecs" {
  name = "${var.cluster_name}-ecs-profile"
  role = "${aws_iam_role.ecs.name}"
}

# instance permissions (ECS)
# https://docs.aws.amazon.com/AmazonECS/latest/developerguide/instance_IAM_role.html
resource "aws_iam_role_policy" "ecs" {
  name = "${var.cluster_name}-ecs-policy"
  role = "${aws_iam_role.ecs.id}"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
              "ecs:DeregisterContainerInstance",
              "ecs:DiscoverPollEndpoint",
              "ecs:Poll",
              "ecs:RegisterContainerInstance",
              "ecs:StartTelemetrySession",
              "ecs:Submit*",
              "ecs:StartTask",
              "ecr:GetAuthorizationToken",
              "ecr:BatchCheckLayerAvailability",
              "ecr:GetDownloadUrlForLayer",
              "ecr:BatchGetImage",
              "logs:CreateLogStream",
              "logs:PutLogEvents"
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
        },
        {
          "Sid": "ALBRegisterPerms",
          "Effect": "Allow",
          "Action": [
            "ec2:AuthorizeSecurityGroupIngress",
            "ec2:Describe*",
            "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
            "elasticloadbalancing:DeregisterTargets",
            "elasticloadbalancing:Describe*",
            "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
            "elasticloadbalancing:RegisterTargets"
          ],
          "Resource": "*"
        }
    ]
}
EOF
}

# ecs service role
resource "aws_iam_role" "ecs" {
  name = "${var.cluster_name}-ecs-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "ecs" {
  role       = "${aws_iam_role.ecs.name}"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceRole"
}
