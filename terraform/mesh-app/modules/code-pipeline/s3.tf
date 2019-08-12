resource "aws_s3_bucket" "codepipeline" {
  bucket_prefix = "${var.artifact_bucket_prefix}"
  acl           = "private"
  force_destroy = true
}
