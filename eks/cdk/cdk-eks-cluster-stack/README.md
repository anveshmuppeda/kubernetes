# EKS Cluster CDK Stack

A generalized AWS CDK stack for deploying Amazon EKS clusters with best practices and demo configurations.

## Overview

This CDK stack creates a production-ready EKS cluster with:
- ✅ Managed node groups
- ✅ Essential EKS addons (VPC CNI, CoreDNS, Kube Proxy, EBS CSI Driver)
- ✅ Pod Identity Association for secure AWS service access
- ✅ Proper IAM roles and security configurations
- ✅ CloudWatch logging enabled

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   VPC Stack     │───▶│   EKS Cluster    │───▶│  Node Groups    │
│  (Network)      │    │     Stack        │    │   (Workers)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │ Pod Identity     │
                       │ Association      │
                       └──────────────────┘
```

## Prerequisites

- AWS CLI configured with appropriate permissions
- Python 3.8 or later
- Node.js 14.x or later
- AWS CDK v2 installed (`npm install -g aws-cdk`)

## Setup Instructions

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd cdk-eks-cluster-stack

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate.bat

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Update the configuration in `app.py`:

```python
# app.py
app_prefix = \"your-project-name\"  # Change this to your project name
aws_account = \"123456789012\"      # Your AWS account ID
aws_region = \"us-east-1\"          # Your preferred region
```

### 3. Deploy the Network Stack (if not exists)

If you don't have an existing VPC, deploy the network stack first:

```bash
# Deploy network infrastructure
cdk deploy NetworkStack
```

### 4. Deploy the EKS Cluster

```bash
# Bootstrap CDK (first time only)
cdk bootstrap

# Synthesize CloudFormation template
cdk synth EksClusterStack

# Deploy the EKS cluster
cdk deploy EksClusterStack
```

## Stack Components

### IAM Roles

1. **EKS Service Role**: For EKS cluster operations
2. **Node Group Role**: For worker nodes with required policies
3. **Demo Pod Role**: Example role for Pod Identity Association

### EKS Cluster Configuration

- **Kubernetes Version**: 1.32 (latest)
- **Endpoint Access**: Public and Private
- **Logging**: All control plane logs enabled
- **Addons**: VPC CNI, CoreDNS, Kube Proxy, EBS CSI Driver, Pod Identity Agent

### Node Group Configuration

- **Instance Type**: t3.medium (configurable)
- **Capacity**: 1-5 nodes (2 desired)
- **AMI Type**: Amazon Linux 2
- **Disk Size**: 100GB

### Pod Identity Association

Demo configuration for secure AWS service access:
- **Namespace**: default
- **Service Account**: demo-service-account
- **Permissions**: S3 read-only, Secrets Manager, SSM Parameter Store

## Usage Examples

### 1. Configure kubectl

```bash
# Update kubeconfig
aws eks update-kubeconfig --region <region> --name <cluster-name>

# Verify connection
kubectl get nodes
```

### 2. Create Service Account for Pod Identity

```yaml
# demo-service-account.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: demo-service-account
  namespace: default
```

```bash
kubectl apply -f demo-service-account.yaml
```

### 3. Deploy Test Pod with Pod Identity

```yaml
# test-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
  namespace: default
spec:
  serviceAccountName: demo-service-account
  containers:
  - name: aws-cli
    image: amazon/aws-cli:latest
    command: [\"sleep\", \"3600\"]
    resources:
      requests:
        cpu: \"100m\"
        memory: \"128Mi\"
      limits:
        cpu: \"500m\"
        memory: \"512Mi\"
```

```bash
kubectl apply -f test-pod.yaml

# Test AWS access
kubectl exec -it test-pod -- aws s3 ls
kubectl exec -it test-pod -- aws sts get-caller-identity
```

### 4. Deploy Sample Application

```yaml
# sample-app.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-app
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: sample-app
  template:
    metadata:
      labels:
        app: sample-app
    spec:
      serviceAccountName: demo-service-account
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: \"100m\"
            memory: \"128Mi\"
          limits:
            cpu: \"500m\"
            memory: \"512Mi\"
---
apiVersion: v1
kind: Service
metadata:
  name: sample-app-service
  namespace: default
spec:
  selector:
    app: sample-app
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer
```

## Customization

### Modify Instance Types

```python
# In eks_cluster_stack.py
instance_type_name = \"t3.large\"  # Change as needed
```

### Add Custom Policies to Pod Role

```python
# In __create_iam_roles method
self.demo_pod_role.add_to_policy(
    iam.PolicyStatement(
        effect=iam.Effect.ALLOW,
        actions=[\"your-custom-actions\"],
        resources=[\"your-resources\"]
    )
)
```

### Configure Different Node Group Settings

```python
# In __add_nodegroup method
min_size=2,      # Minimum nodes
max_size=10,     # Maximum nodes  
desired_size=3,  # Desired nodes
disk_size=200,   # Disk size in GB
```

## Monitoring and Logging

### View Cluster Logs

```bash
# View control plane logs in CloudWatch
aws logs describe-log-groups --log-group-name-prefix \"/aws/eks\"

# Stream logs
aws logs tail /aws/eks/<cluster-name>/cluster --follow
```

### Monitor Node Health

```bash
# Check node status
kubectl get nodes -o wide

# Check node conditions
kubectl describe nodes

# View node metrics
kubectl top nodes
```

## Troubleshooting

### Common Issues

1. **Cluster Creation Fails**
   ```bash
   # Check CloudFormation events
   aws cloudformation describe-stack-events --stack-name EksClusterStack
   ```

2. **Nodes Not Joining**
   ```bash
   # Check node group status
   aws eks describe-nodegroup --cluster-name <cluster> --nodegroup-name <nodegroup>
   ```

3. **Pod Identity Not Working**
   ```bash
   # Verify pod identity association
   aws eks list-pod-identity-associations --cluster-name <cluster>
   
   # Check service account
   kubectl describe sa demo-service-account
   ```

### Useful Commands

```bash
# List all stacks
cdk ls

# Show differences
cdk diff EksClusterStack

# Destroy stack (careful!)
cdk destroy EksClusterStack

# View synthesized template
cdk synth EksClusterStack > template.yaml
```

## Security Considerations

- ✅ Least privilege IAM roles
- ✅ Private endpoint access enabled
- ✅ Network security groups configured
- ✅ Pod Identity for secure AWS access
- ✅ No hardcoded credentials

## Cost Optimization

- Use Spot instances for non-production workloads
- Enable cluster autoscaler
- Monitor resource usage with AWS Cost Explorer
- Consider Fargate for serverless workloads

## Cleanup

```bash
# Delete all Kubernetes resources first
kubectl delete all --all --all-namespaces

# Destroy the CDK stack
cdk destroy EksClusterStack

# Optionally destroy network stack
cdk destroy NetworkStack
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue in the repository
- Check AWS EKS documentation
- Review CDK documentation

---

**Author**: [Anvesh Muppeda](https://github.com/anveshmuppeda)  
**Repository**: [kubernetes](https://github.com/anveshmuppeda/kubernetes)