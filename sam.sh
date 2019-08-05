#! /bin/bash

set -eo pipefail
while getopts f: option
do
case "${option}"
in
f) FAIL=${OPTARG};;
esac
done

block_text () {
    message="$1"

    echo "--------------------------------------------"
    echo " "
    echo $message
    echo " "
    echo "---------------------------------------------"
}


source .env

: ${AWS_DEFAULT_REGION:=$DEFAULT_REGION}
: ${S3BUCKET:=$S3BUCKET}

cd canary/

pip install -t dist .

block_text $S3BUCKET

sam package \
    --output-template-file packaged.yaml \
    --s3-bucket $S3BUCKET

sam deploy \
    --template-file packaged.yaml \
    --stack-name canary-sam \
    --capabilities CAPABILITY_IAM \
    --region $AWS_DEFAULT_REGION

function_arn=$(aws cloudformation describe-stacks --stack-name dd-sam \
    --query 'Stacks[0].Outputs[?OutputKey==`HelloWorldFunction`].OutputValue' \
    --output text)

block_text $function_arn

rm -rf packaged.yaml