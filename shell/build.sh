#! /bin/bash

export $(xargs <.env)
export $(xargs <tf.env)

cd app/

$(aws ecr get-login --no-include-email --region $DEFAULT_REGION)

: ${APP_NAME:=$MESH_NAME}

docker build -t demo-app . --build-arg APP_NAME=$APP_NAME
docker tag demo-app:latest $AWS_ACCOUNT_ID.dkr.ecr.$DEFAULT_REGION.amazonaws.com/$MESH_NAME:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$DEFAULT_REGION.amazonaws.com/$MESH_NAME:latest

echo "URL to check app"
echo "$dns_name"
