resource "aws_security_group" "lb" {
  vpc_id      = var.vpc_id
  name        = "${var.lb_name}-lb-sg"
  description = "allow http to ${var.lb_name}"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

}

resource "aws_lb" "lb" {
  name               = "${var.lb_name}-lb"
  internal           = var.internal
  load_balancer_type = var.lb_type == "application" ? "application" : "network"
  security_groups    = [aws_security_group.lb.id]

  subnets = var.public_subnet_ids

  tags = "${merge(
    local.common_tags,
    map(
      "Name", var.lb_name
    )
  )}"
}

resource "aws_lb_target_group" "tg1" {
  name        = "${var.lb_name}-tg1"
  port        = var.container_port
  protocol    = var.protocol
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    healthy_threshold   = var.healthy_threshold
    unhealthy_threshold = var.unhealthy_threshold
    interval            = var.health_check_interval
    path                = var.lb_type == "application" ? var.health_check_path : ""
    protocol            = var.protocol
    matcher             = var.lb_type == "application" ? 200 : ""
  }

  tags = "${merge(
    local.common_tags,
    map(
      "Name", var.lb_name
    )
  )}"

  depends_on = [aws_lb.lb]
}

resource "aws_lb_target_group" "tg2" {
  name        = "${var.lb_name}-tg2"
  port        = var.container_port
  protocol    = var.protocol
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    healthy_threshold   = var.healthy_threshold
    unhealthy_threshold = var.unhealthy_threshold
    interval            = var.health_check_interval
    path                = var.lb_type == "application" ? var.health_check_path : ""
    protocol            = var.protocol
    matcher             = var.lb_type == "application" ? 200 : ""
  }

  tags = "${merge(
    local.common_tags,
    map(
      "Name", var.lb_name
    )
  )}"

  depends_on = [aws_lb.lb]
}

# Define listeners
resource "aws_lb_listener" "prod_listener" {
  load_balancer_arn = aws_lb.lb.arn
  port              = var.container_port
  protocol          = var.protocol

  default_action {
    target_group_arn = aws_lb_target_group.tg1.arn
    type             = "forward"
  }

  lifecycle {
    ignore_changes = [
      "default_action",
    ]
  }
}

resource "aws_lb_listener" "test_listener" {
  load_balancer_arn = aws_lb.lb.arn
  port              = var.container_test_port
  protocol          = var.protocol

  default_action {
    target_group_arn = aws_lb_target_group.tg1.arn
    type             = "forward"
  }

  lifecycle {
    ignore_changes = [
      "default_action",
    ]
  }
}
