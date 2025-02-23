# **A Comprehensive Guide to Creating an Amazon EKS Cluster with Self-Managed Worker Nodes**  
## **Step-by-Step Tutorial with Troubleshooting Tips**  

Medium Blog Link: [⎈ Hands-On Guide to Creating an Amazon EKS Cluster with Self-Managed Worker Nodes ⎈](https://medium.com/@muppedaanvesh/hands-on-guide-to-creating-an-amazon-eks-cluster-with-self-managed-worker-nodes-fad026c34482)
---

### **Introduction**  
Amazon Elastic Kubernetes Service (EKS) simplifies Kubernetes cluster management on AWS. While EKS handles the control plane, **self-managed worker nodes** give you flexibility to customize node configurations. In this guide, you’ll learn to:  
1. Create an EKS cluster.  
2. Deploy self-managed worker nodes.  
3. Fix common "Unauthorized" errors.  

---

### **Prerequisites**  
1. **AWS CLI**: Installed and configured with `aws configure`.  
2. **kubectl**: For interacting with Kubernetes ([installation guide](https://kubernetes.io/docs/tasks/tools/)).  
3. **Basic AWS Knowledge**: Familiarity with IAM, VPC, and EC2.  

---

### **Step 1: Create an IAM Role for the EKS Cluster**  
**Why?** The EKS control plane needs permissions to manage AWS resources.  

1. **Create a trust policy file** (`cluster-trust-policy.json`):  
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": { "Service": "eks.amazonaws.com" },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   ```  
   *Explanation*: This allows the EKS service to assume the role.  

2. **Create the IAM role**:  
   ```bash
   # General Command
   aws iam create-role \
     --role-name <Cluster-Role-Name> \
     --assume-role-policy-document file://cluster-trust-policy.json

   # Example
   aws iam create-role \
     --role-name EKSClusterRole \
     --assume-role-policy-document file://cluster-trust-policy.json
   ```  

3. **Attach the EKS cluster policy**:  
   ```bash
   # General Command
   aws iam attach-role-policy \
     --role-name <Cluster-Role-Name> \
     --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy

   # Example
   aws iam attach-role-policy \
     --role-name EKSClusterRole \
     --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
   ```  

---

### **Step 2: Create the EKS Cluster**  
**Why?** The cluster is the Kubernetes control plane managed by AWS.  

1. **Run the cluster creation command**:  
   ```bash
   # General Command
   aws eks create-cluster \
     --name <Cluster-Name> \
     --role-arn arn:aws:iam::<AWS-Account-ID>:role/<Cluster-Role-Name> \
     --resources-vpc-config subnetIds=<Subnet-ID-1>,<Subnet-ID-2>

   # Example
   aws eks create-cluster \
     --name my-eks-cluster \
     --role-arn arn:aws:iam::123456789012:role/EKSClusterRole \
     --resources-vpc-config subnetIds=subnet-12345678,subnet-87654321
   ```  
   - Replace `<AWS-Account-ID>` with your account ID (find it via `aws sts get-caller-identity`).  
   - Use **public subnets** from your VPC.  

2. **Wait for the cluster to activate** (10-15 mins):  
   ```bash
   aws eks describe-cluster --name my-eks-cluster --query "cluster.status"
   ```  
   *Expected Output*: `"ACTIVE"`.  

---

### **Step 3: Configure kubectl to Access the Cluster**  
**Why?** To interact with the cluster using `kubectl`.  

1. **Update kubeconfig**:  
   ```bash
   aws eks update-kubeconfig --name my-eks-cluster --region us-east-1
   ```  

2. **Verify access**:  
   ```bash
   kubectl get nodes
   ```  
   *Output*: `No resources found` (no nodes yet).  

#### Retrieve Cluster Details  
3.1 Get Cluster API Endpoint  
```bash
EKS_CLUSTER_API=$(aws eks describe-cluster --name UnManagedNodeGroup-Demo --query "cluster.endpoint" --output text)
```
3.2 Get Cluster CA Certificate  
```bash
EKS_CLUSTER_CA=$(aws eks describe-cluster --name UnManagedNodeGroup-Demo --query "cluster.certificateAuthority.data" --output text)
```
3.3 Get Kubernetes Service kubedns/coredns IP  
fetch the kubedns/coredns IP as per your cluster from the service running in the kube-system namespace , in my cluster it was 172.20.0.10.


---

### **Step 4: Create an IAM Role for Worker Nodes**  
**Why?** Nodes need permissions to join the cluster and pull container images.  

1. **Create a node trust policy file** (`node-trust-policy.json`):  
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": { "Service": "ec2.amazonaws.com" },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   ```  

2. **Create the IAM role**:  
   ```bash
   # General Command
   aws iam create-role \
     --role-name <Node-Role-Name> \
     --assume-role-policy-document file://node-trust-policy.json

   # Example
   aws iam create-role \
     --role-name EKSNodeRole \
     --assume-role-policy-document file://node-trust-policy.json
   ```  

3. **Attach required policies**:  
   ```bash
   # Attach worker node policy
   aws iam attach-role-policy \
     --role-name EKSNodeRole \
     --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy

   # Attach CNI policy (for networking)
   aws iam attach-role-policy \
     --role-name EKSNodeRole \
     --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy

   # Attach ECR read-only access
   aws iam attach-role-policy \
     --role-name EKSNodeRole \
     --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
   ```  

---

### **Step 5: Launch Self-Managed Worker Nodes**  
**Why?** Worker nodes run your Kubernetes pods.  

1. **Create an instance profile**:  
   ```bash
   # General Command
   aws iam create-instance-profile \
     --instance-profile-name <Instance-Profile-Name>

   # Example
   aws iam create-instance-profile \
     --instance-profile-name EKSNodeInstanceProfile

   # Link role to profile
   aws iam add-role-to-instance-profile \
     --instance-profile-name EKSNodeInstanceProfile \
     --role-name EKSNodeRole
   ```  

2. **Get the EKS-optimized AMI ID**:  
   ```bash
   AMI_ID=$(aws ssm get-parameter \
     --name /aws/service/eks/optimized-ami/1.30/amazon-linux-2/recommended/image_id \
     --query "Parameter.Value" --output text)
   ```  

3. **Generate User Data for Worker Nodes**  
Create userdata.tx  
```sh
cat <<EOF | base64 -w0 > userdata.txt
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="==UserDataEnd=="

--==UserDataEnd==
Content-Type: text/x-shellscript; charset="us-ascii"

#!/bin/bash

set -ex

EKS_CLUSTER_API="Value of EKS_CLUSTER_API"
EKS_CLUSTER_CA="value of EKS_CLUSTER_CA"
EKS_CLUSTER_DNS_IP="172.20.0.10 or update with your ip"

/etc/eks/bootstrap.sh UnManagedNodeGroup-Demo \\
  --apiserver-endpoint "\$EKS_CLUSTER_API" \\
  --b64-cluster-ca "\$EKS_CLUSTER_CA" \\
  --dns-cluster-ip "\$EKS_CLUSTER_DNS_IP" \\
  --container-runtime containerd \\
  --kubelet-extra-args '--max-pods=17' \\
  --use-max-pods false

--==UserDataEnd==--
EOF
```  
4. **Create a LaunchTemplate.json:**  
```sh
cat <<EOF > launch-template.json
{
    "ImageId": "Update AMI ID which from above section",
    "InstanceType": "t3.medium or other",
    "UserData": "value from above userdata.txt file",
    "SecurityGroupIds": ["<Worker Node SG ID which we created above>"],
    "KeyName": "eksWorkerKey to ssh into workers",
    "IamInstanceProfile": {
        "Name": "UnManagedNodeGroup_EKS_Instance_Profile or update with your profilename"
    },
    "PrivateDnsNameOptions": {
        "EnableResourceNameDnsARecord": true
    },
    "Monitoring": {
        "Enabled": true
    }
}
EOF
``` 
Note: Update all the value and run the above to create launchTemplate.json file  

5. **Now create the launch template using the above json file**:  
    ```bash
    # General Command
    aws ec2 create-launch-template \
    --launch-template-name <launch template name> \
    --launch-template-data file://<filename.json> \
    --tag-specifications "ResourceType=launch-template,Tags=[{Key=<keyname>,Value=<keyvalue>}]"  

    # Example
    aws ec2 create-launch-template \
    --launch-template-name EKS_UnManagedNodeGroup_Launch_Template \
    --launch-template-data file://launchTemplate.json \
    --tag-specifications "ResourceType=launch-template,Tags=[{Key=Application,Value=UnManagedWorkerNodeApp}]"
    ```  

6. **Create an Auto Scaling Group (ASG)**:  
    ```bash
    # General Command
    aws autoscaling create-auto-scaling-group \
    --auto-scaling-group-name <ASG-Name> \
    --launch-template LaunchTemplateName=<Launch-Template-Name>,Version=1 \
    --vpc-zone-identifier "<Subnet-ID-1>,<Subnet-ID-2>" \
    --tags Key=<keyname>,Value=<keyvalue>,PropagateAtLaunch=true \
    --health-check-grace-period 15 \
    --new-instances-protected-from-scale-in \
    --capacity-rebalance \
    --min-size <min number of nodes> \
    --max-size <max number of nodes> \
    --desired-capacity <desired number of nodes>

    # Example
    aws autoscaling create-auto-scaling-group \
    --auto-scaling-group-name EKS_UnManagedNodeGroup_ASG \
    --launch-template LaunchTemplateName=EKS_UnManagedNodeGroup_Launch_Template,Version=1 \
    --vpc-zone-identifier subnet-12345678,subnet-87654321, \
    --tags Key=Application,Value=UnManagedWorkerNodeApp,PropagateAtLaunch=true \
    --health-check-grace-period 15 \
    --new-instances-protected-from-scale-in \
    --capacity-rebalance \
    --min-size 1 \
    --max-size 2 \
    --desired-capacity 1
    ```  

   

---

### **Step 6: Allow Nodes to Join the Cluster**  
**Why?** Nodes need RBAC permissions to register with the control plane.  

1. **Update the `aws-auth` ConfigMap**:  
   ```bash
   kubectl apply -f - <<EOF
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: aws-auth
     namespace: kube-system
   data:
     mapRoles: |
       - rolearn: arn:aws:iam::<AWS-Account-ID>:role/<Node-Role-Name>
         username: system:node:{{EC2PrivateDNSName}}
         groups:
           - system:bootstrappers
           - system:nodes
   EOF
   ```  

   **Example**:  
   ```bash
   kubectl apply -f - <<EOF
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: aws-auth
     namespace: kube-system
   data:
     mapRoles: |
       - rolearn: arn:aws:iam::123456789012:role/EKSNodeRole
         username: system:node:{{EC2PrivateDNSName}}
         groups:
           - system:bootstrappers
           - system:nodes
   EOF
   ```  

2. **Verify nodes join the cluster**:  
   ```bash
   kubectl get nodes
   ```  
   *Expected Output*:  
   ```
   NAME                           STATUS   ROLES    AGE   VERSION
   ip-192-168-1-1.ec2.internal   Ready    <none>   2m    v1.30.0-eks-xxxxxxx
   ```  

---

### **Troubleshooting: Fixing “Unauthorized” Errors**  
If nodes don’t appear:  

1. **Check IAM Trust Policies**:  
   - **Cluster Role**: Must trust `eks.amazonaws.com`.  
     ```json
     // Correct Trust Policy for Cluster Role
     {
       "Principal": { "Service": "eks.amazonaws.com" }
     }
     ```  
   - **Node Role**: Must trust `ec2.amazonaws.com`.  

2. **Verify the `aws-auth` ConfigMap**:  
   ```bash
   kubectl describe configmap aws-auth -n kube-system
   ```  
   Ensure the node role ARN matches your IAM role.  

3. **Check Security Groups**:  
   - **Worker Nodes**: Allow **outbound traffic** to the EKS API (port 443).  
   - **Control Plane**: Allow **inbound traffic** from worker node security groups.  

4. **Terminate and Replace Nodes**:  
   ```bash
   # Terminate instances in the ASG
   aws autoscaling terminate-instance-in-auto-scaling-group \
     --instance-id <Instance-ID> \
     --should-decrement-desired-capacity
   ```  

---

### **Cleanup**  
Avoid unnecessary charges by deleting resources:  
```bash
# Delete the EKS cluster
aws eks delete-cluster --name my-eks-cluster

# Delete the Auto Scaling Group
aws autoscaling delete-auto-scaling-group --auto-scaling-group-name EKSWorkerASG

# Delete IAM roles
aws iam delete-role --role-name EKSClusterRole
aws iam delete-role --role-name EKSNodeRole
```  

---

### **Conclusion**  
You’ve successfully created an EKS cluster with self-managed worker nodes! Key takeaways:  
1. **IAM Roles**: Ensure correct trust policies and permissions.  
2. **Security Groups**: Configure inbound/outbound rules properly.  
3. **`aws-auth` ConfigMap**: Critical for node authentication.  

**Next Steps**:  
- Deploy a sample app: `kubectl create deployment nginx --image=nginx`  
- Explore [Managed Node Groups](https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html) for automated node management.  
- Set up monitoring with [Prometheus and Grafana](https://docs.aws.amazon.com/eks/latest/userguide/prometheus.html).  

Got questions or facing issues? Let me know in the comments! 👇  

--- 

**Additional Resources**:  
- [AWS EKS Documentation](https://docs.aws.amazon.com/eks/latest/userguide/)  
- [Troubleshooting EKS Nodes](https://docs.aws.amazon.com/eks/latest/userguide/troubleshooting.html)