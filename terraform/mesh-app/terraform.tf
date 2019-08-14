terraform {
  backend "s3" {
    bucket = "REPLACEBUCKET"
    key    = "REPLACEKEY/terraform.tfstate"
    region = "us-west-2"
  }
}
