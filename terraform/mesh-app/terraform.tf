terraform {
  backend "s3" {
    bucket = "jonah-sam-bucket2222"
    key    = "yolo/terraform.tfstate"
    region = "us-west-2"
  }
}
