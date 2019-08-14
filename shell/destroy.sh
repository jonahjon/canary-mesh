#! /bin/bash

export $(xargs <.env)

cd terraform/mesh-app

export TF_VAR_appname=$MESH_NAME
export TF_VAR_aws_region=$DEFAULT_REGION

# Delete the terraform stack
terraform init
terraform get
terraform plan -out plan -destroy
terraform apply plan

# Delete any emphemral items created related to this deployment including the state bucket
rm -rf .terraform/
rm -rf ../../tf.env
rm -rf terraform.tf && cp terraform.tf.old terraform.tf
aws s3 rb s3://${AWS_STATE_BUCKET} --force  

