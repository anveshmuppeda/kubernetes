# Karpeneter

# Logout of helm registry to perform an unauthenticated pull against the public ECR
helm registry logout public.ecr.aws

export CLUSTER_NAME=karpenter-demo-cluster
export KARPENTER_VERSION=1.3.3
export KARPENTER_NAMESPACE="kube-system"
export KARPENTER_IAM_ROLE_ARN="arn:aws:iam::463470985368:role/EKSIAMRoleforServiceAccount-CF-karpenter-stack"

helm upgrade --install karpenter oci://public.ecr.aws/karpenter/karpenter --version "${KARPENTER_VERSION}" --namespace "${KARPENTER_NAMESPACE}" --create-namespace \
  --set "settings.clusterName=${CLUSTER_NAME}" \
  --set "settings.interruptionQueue=${CLUSTER_NAME}" \
  --set controller.resources.requests.cpu=1 \
  --set controller.resources.requests.memory=1Gi \
  --set controller.resources.limits.cpu=1 \
  --set controller.resources.limits.memory=1Gi \
  --set "serviceAccount.annotations.eks\.amazonaws\.com/role-arn=${KARPENTER_IAM_ROLE_ARN}" \
  --wait



