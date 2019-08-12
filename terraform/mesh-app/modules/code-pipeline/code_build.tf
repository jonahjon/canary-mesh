resource "aws_codebuild_project" "fetch_templates" {
  name          = "${var.name}"
  description   = "Gets task definition and appspec template files from S3 (pushed by upstream CI system e.g. Jenkins)"
  build_timeout = "5"
  service_role  = "${aws_iam_role.codebuild.arn}"

  artifacts {
    type                = "CODEPIPELINE"
    name                = "Fetch_Templates"
    packaging           = "NONE"
    encryption_disabled = false
  }

  cache {
    type = "NO_CACHE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:2.0"
    type                        = "LINUX_CONTAINER"
    privileged_mode             = false
    image_pull_credentials_type = "CODEBUILD"
  }

  source {
    type         = "CODEPIPELINE"
    buildspec    = "${data.template_file.fetch_templates_buildspec.rendered}"
    insecure_ssl = false
  }
}

data "template_file" "fetch_templates_buildspec" {
  template = "${file("${path.module}/templates/fetch_templates_buildspec.yml")}"

  vars = {
    service_name = var.name
    bucket_name  = aws_s3_bucket.codepipeline.bucket
  }
}
