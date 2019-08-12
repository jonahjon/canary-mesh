module "sample_vpc" {
  source                 = "terraform-aws-modules/vpc/aws"
  version                = "2.7.0"
  name                   = "sample_vpc"
  azs                    = ["us-west-2a", "us-west-2b", "us-west-2c"]
  cidr                   = "10.10.0.0/19"                                      # 8,192
  private_subnets        = ["10.10.0.0/22", "10.10.4.0/22", "10.10.8.0/22"]    # 1,024 each
  public_subnets         = ["10.10.28.0/24", "10.10.29.0/24", "10.10.30.0/24"] # 256 each
  enable_nat_gateway     = true
  single_nat_gateway     = false
  one_nat_gateway_per_az = false
  enable_vpn_gateway     = false
  enable_dns_hostnames   = true
  enable_s3_endpoint     = true
}
