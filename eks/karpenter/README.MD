# Hands‑On Guide to Karpenter on AWS EKS

## Introduction

Karpenter is a modern Kubernetes node autoscaler designed for ease of use, performance, and flexibility. It streamlines node provisioning on AWS EKS by monitoring unschedulable pods and automatically launching or terminating EC2 instances based on real‑time demand. This guide will walk you through setting up an EKS cluster, configuring the required IAM permissions, deploying Karpenter via Helm, and testing node autoscaling with a sample application. Whether you prefer a programmatic approach using **eksctl** or the simplicity of CloudFormation templates, you’ll find clear and concise instructions below.

---

## Compatibility Matrix

Before you begin, make sure your cluster’s Kubernetes version is compatible with the version of Karpenter you plan to use. Here is the compatibility matrix:

| **Kubernetes Version** | **Minimum Karpenter Version Required** |
|------------------------|------------------------------------------|
| 1.26                   | >= 0.28                                  |
| 1.27                   | >= 0.28                                  |
| 1.28                   | >= 0.31                                  |
| 1.29                   | >= 0.34                                  |
| 1.30                   | >= 0.37                                  |
| 1.31                   | >= 1.0.5                                 |
| 1.32                   | >= 1.2                                   |

*Note:* If you prefer to set up the EKS cluster and the required IAM permissions using a CloudFormation template, skip steps 1 and 2 in the detailed instructions below. Instead, deploy the provided CloudFormation file (e.g., `karpenter.cft.yaml`) as follows:

```bash
aws cloudformation deploy \
  --stack-name "Karpenter-${CLUSTER_NAME}" \
  --template-file "file://karpenter.yaml" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides "ClusterName=${CLUSTER_NAME}"
```

---

## Prerequisites

- **AWS CLI** configured with sufficient privileges.
- **kubectl** installed and configured.
- **eksctl** (version >= v0.202.0 recommended).
- **Helm** (for installing Karpenter).
- An active AWS account and a working VPC (and subnets/security groups tagged accordingly).

---

## Step‑By‑Step Guide

### 1. Set Environment Variables

Export necessary variables. Adjust values as needed:

```bash
export KARPENTER_NAMESPACE="kube-system"     # Namespace for Karpenter (default is kube-system)
export KARPENTER_VERSION="1.3.3"              # Desired Karpenter version
export K8S_VERSION="1.32"                     # Kubernetes version

export AWS_PARTITION="aws"                    # or aws-cn/aws-us-gov if applicable
export CLUSTER_NAME="karpenter-demo-cluster"  # Name of your EKS cluster
export AWS_DEFAULT_REGION="us-west-2"
export AWS_ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
```

*Additional Variables:*  
If you plan to use dynamic AMI selection for your node classes, export extra variables such as `ALIAS_VERSION` (determined by querying SSM for your chosen Kubernetes version).

### 2. Create the EKS Cluster

Using **eksctl**, create your cluster with a configuration file. The following snippet demonstrates a minimal configuration. Note that tagging the cluster (using `karpenter.sh/discovery`) is critical for resource discovery by Karpenter:

```yaml
eksctl create cluster -f - <<EOF
---
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: ${CLUSTER_NAME}
  region: ${AWS_DEFAULT_REGION}
  version: "${K8S_VERSION}"
  tags:
    karpenter.sh/discovery: ${CLUSTER_NAME}
iam:
  withOIDC: true
  serviceAccounts:
  - metadata:
      name: karpenter
      namespace: "${KARPENTER_NAMESPACE}"
    roleName: ${CLUSTER_NAME}-karpenter
    attachPolicyARNs:
    - arn:${AWS_PARTITION}:iam::${AWS_ACCOUNT_ID}:policy/KarpenterControllerPolicy-${CLUSTER_NAME}
    roleOnly: true
iamIdentityMappings:
- arn: "arn:${AWS_PARTITION}:iam::${AWS_ACCOUNT_ID}:role/KarpenterNodeRole-${CLUSTER_NAME}"
  username: system:node:{{EC2PrivateDNSName}}
  groups:
  - system:bootstrappers
  - system:nodes
managedNodeGroups:
- instanceType: m5.large
  amiFamily: AmazonLinux2
  name: ${CLUSTER_NAME}-ng
  desiredCapacity: 2
  minSize: 1
  maxSize: 10
EOF
```

*Tip:* If using CloudFormation (as noted earlier), skip this step.

### 3. Create Dependent IAM Permissions (if not using CFT)

If you’re not using the CloudFormation template, download and deploy the IAM permissions file:

```bash
curl -L "https://raw.githubusercontent.com/aws/karpenter-provider-aws/v${KARPENTER_VERSION}/website/content/en/preview/getting-started/getting-started-with-karpenter/karpenter-iam-permissions.yaml" -o karpenter-iam-permissions.yaml

aws cloudformation deploy \
  --stack-name "Karpenter-${CLUSTER_NAME}" \
  --template-file "file://karpenter-iam-permissions.yaml" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides "ClusterName=${CLUSTER_NAME}"
```

### 4. Install Karpenter via Helm

Logout from the Helm registry and install the chart:

```bash
helm registry logout public.ecr.aws

helm upgrade --install karpenter oci://public.ecr.aws/karpenter/karpenter \
  --version "${KARPENTER_VERSION}" \
  --namespace "${KARPENTER_NAMESPACE}" --create-namespace \
  --set "settings.clusterName=${CLUSTER_NAME}" \
  --set "settings.interruptionQueue=${CLUSTER_NAME}" \
  --set controller.resources.requests.cpu=1 \
  --set controller.resources.requests.memory=1Gi \
  --set controller.resources.limits.cpu=1 \
  --set controller.resources.limits.memory=1Gi \
  --set "serviceAccount.annotations.eks\.amazonaws\.com/role-arn=${KARPENTER_IAM_ROLE_ARN}" \
  --wait
```

Ensure that IRSA is properly configured and your service account is associated with the correct IAM role.

### 5. Create a NodePool

Define a NodePool that details the scheduling requirements and capacity limits:

```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: default
spec:
  template:
    spec:
      requirements:
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64"]
        - key: kubernetes.io/os
          operator: In
          values: ["linux"]
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["on-demand"]
        - key: karpenter.k8s.aws/instance-category
          operator: In
          values: ["c", "m", "r"]
        - key: karpenter.k8s.aws/instance-generation
          operator: Gt
          values: ["2"]
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: default
      expireAfter: 720h   # Automatically expire nodes after 30 days
  limits:
    cpu: 1000
  disruption:
    consolidationPolicy: WhenEmptyOrUnderutilized
    consolidateAfter: 1m
```

### 6. Create an EC2NodeClass

This custom resource defines the AWS settings (such as the role, AMI selection, subnets, security groups, and block device mappings) for node provisioning:

```bash
cat <<EOF | envsubst | kubectl apply -f -
apiVersion: karpenter.k8s.aws/v1
kind: EC2NodeClass
metadata:
  name: default
spec:
  role: "KarpenterNodeRole-${CLUSTER_NAME}"  # Ensure this matches the node role created earlier
  amiSelectorTerms:
    - alias: "al2023@${ALIAS_VERSION}"
  subnetSelectorTerms:
    - tags:
        karpenter.sh/discovery: "${CLUSTER_NAME}"
  securityGroupSelectorTerms:
    - tags:
        karpenter.sh/discovery: "${CLUSTER_NAME}"
EOF
```

*Note:* For private EKS clusters (with no outbound internet access) you can supply a pre‑created instance profile ARN using the `spec.instanceProfile` field.

### 7. Deploy a Sample Application

Deploy a simple application (using the Kubernetes pause image) that starts with zero replicas. This allows you to test that Karpenter provisions nodes when you scale up:

```bash
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: inflate
spec:
  replicas: 0
  selector:
    matchLabels:
      app: inflate
  template:
    metadata:
      labels:
        app: inflate
    spec:
      terminationGracePeriodSeconds: 0
      securityContext:
        runAsUser: 1000
        runAsGroup: 3000
        fsGroup: 2000
      containers:
      - name: inflate
        image: public.ecr.aws/eks-distro/kubernetes/pause:3.7
        resources:
          requests:
            cpu: 1
        securityContext:
          allowPrivilegeEscalation: false
EOF
```

### 8. Scale Up the Deployment

Trigger node provisioning by scaling the deployment:

```bash
kubectl scale deployment inflate --replicas 5
```

Monitor the Karpenter logs and check your node list:

```bash
kubectl logs -f -n "${KARPENTER_NAMESPACE}" -l app.kubernetes.io/name=karpenter -c controller
kubectl get nodes
```

### 9. Scale Down and Consolidate

Delete the deployment to allow Karpenter to consolidate unneeded nodes:

```bash
kubectl delete deployment inflate
```

You can also manually delete a node if needed:

```bash
kubectl delete node "${NODE_NAME}"
```

### 10. Clean Up Your Resources

When finished, uninstall Karpenter and delete your cluster resources:

1. **Uninstall Karpenter:**

   ```bash
   helm uninstall karpenter --namespace "${KARPENTER_NAMESPACE}"
   ```

2. **Delete the CloudFormation Stack (if used):**

   ```bash
   aws cloudformation delete-stack --stack-name "Karpenter-${CLUSTER_NAME}"
   ```

3. **Delete EC2 Launch Templates (if applicable):**

   ```bash
   aws ec2 describe-launch-templates --filters "Name=tag:karpenter.k8s.aws/cluster,Values=${CLUSTER_NAME}" \
     | jq -r ".LaunchTemplates[].LaunchTemplateName" \
     | xargs -I{} aws ec2 delete-launch-template --launch-template-name {}
   ```

4. **Delete the EKS Cluster:**

   ```bash
   eksctl delete cluster --name "${CLUSTER_NAME}"
   ```

---

## Conclusion

This guide detailed each step in deploying Karpenter on an AWS EKS cluster—from setting up the cluster and configuring IAM permissions (or using a CloudFormation template) to deploying Karpenter, provisioning nodes via NodePool and EC2NodeClass, and finally testing autoscaling with a sample deployment. With a clear compatibility matrix, straightforward commands, and well-documented steps, you now have a blueprint to enable dynamic, cost‑efficient autoscaling for your Kubernetes workloads.

Be sure to test all changes in lower environments before moving to production. Keep abreast of updates via the official [Karpenter documentation](https://karpenter.sh/docs) and upgrade guides for any breaking changes.

Happy scaling!

