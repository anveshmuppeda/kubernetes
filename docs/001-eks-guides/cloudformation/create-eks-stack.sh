aws cloudformation create-stack \
  --region us-east-1 \
  --stack-name my-eks-fargate-cluster \
  --capabilities CAPABILITY_NAMED_IAM \
  --template-body file://eks-fargate-cft.yaml 
