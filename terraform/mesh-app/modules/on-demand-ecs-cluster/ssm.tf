resource "aws_iam_role_policy_attachment" "ssm-instance-attach" {
  role       = "${aws_iam_role.ecs.name}"
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}