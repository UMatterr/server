#!/bin/bash

set -e

AWS_ECR_HOST=$(echo $AWS_ECR_HOST)

docker build -t ${AWS_ECR_HOST}:latest .

docker push ${AWS_ECR_HOST}:latest 
