#! /bin/bash

export $(xargs <.env)

# Check for the existance, and then create if needed our Terraform state bucket
bucketstatus=$(aws s3api head-bucket --bucket ${AWS_STATE_BUCKET} 2>&1)
if echo ${bucketstatus} | grep 'Not Found';
then
  echo "TF state Bucket: $AWS_STATE_BUCKET doesn't exist creating bucket";
  aws s3 mb s3://$AWS_STATE_BUCKET
elif echo ${bucketstatus} | grep 'Forbidden';
then
  echo "Bucket exists but not owned"
elif echo ${bucketstatus} | grep 'Bad Request';
then
  echo "Bucket name specified is less than 3 or greater than 63 characters"
else
  echo "TF state Bucket: $AWS_STATE_BUCKET owned and exists";
fi


cd terraform/mesh-app

# Edit your remote state file to be unique
gsed -i "s/REPLACEBUCKET/$AWS_STATE_BUCKET/g" terraform.tf
gsed -i "s/REPLACEKEY/$MESH_NAME/g" terraform.tf
gsed -i "s/us-west-2/$DEFAULT_REGION/g" terraform.tf

# Pass variables into our terraform run
export TF_VAR_app_name=$MESH_NAME
export TF_VAR_aws_region=$DEFAULT_REGION

# Run the terraform
terraform init
terraform get
terraform plan -out plan
terraform apply plan

# output our terraform to a tf.env file, which gets used by our deployment configurations
alb_dns=$(terraform output alb_dns_name) && echo "dns_name=$alb_dns" > tf.env
service_name=$(terraform output service_name) && echo "service_name=$service_name" >> tf.env
containerPort=$(terraform output containerPort) && echo "containerPort=$containerPort" >> tf.env
aws_log_group=$(terraform output aws_log_group) && echo "aws_log_group=$aws_log_group" >> tf.env
aws_region=$(terraform output aws_region) && echo "aws_region=$aws_region" >> tf.env
mesh_name=$(terraform output mesh_name) && echo "mesh_name=$mesh_name" >> tf.env
virtual_node_name=$(terraform output virtual_node_name) && echo "virtual_node_name=$virtual_node_name" >> tf.env
envoy_log_level=$(terraform output envoy_log_level) && echo "envoy_log_level=$envoy_log_level" >> tf.env
artifact_bucket_name=$(terraform output artifact_bucket_name) && echo "artifact_bucket_name=$artifact_bucket_name" >> tf.env

# move the tf.env file, and delete the plan that was executed
mv ./tf.env ../..
rm -rf plan
