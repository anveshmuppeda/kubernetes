# ** Hands-On Guide  to Creating an Amazon EKS Cluster with Managed Node Groups**  
## **Simplify Kubernetes Operations with AWS-Managed Worker Nodes**  

Medium Blog Link: [⎈ Hands-On Guide to Creating an Amazon EKS Cluster with Self-Managed Worker Nodes ⎈](https://medium.com/@muppedaanvesh/hands-on-guide-to-creating-an-amazon-eks-cluster-with-self-managed-worker-nodes-fad026c34482)

![EKS Managed Worker Nodes](./eks.managedworkers.png)
---

### **Introduction**  
Amazon EKS Managed Node Groups automate the provisioning, scaling, and lifecycle management of worker nodes, reducing operational overhead. 

In this guide, you’ll learn to:  
1. Create an EKS cluster.  
2. Deploy Managed Worker Node Group.  

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
     --role-name ManagedEKSClusterRole \
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
     --role-name ManagedEKSClusterRole \
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
     --name Manged-EKS-Cluster-Demo \
     --role-arn arn:aws:iam::463470985368:role/ManagedEKSClusterRole \
     --resources-vpc-config subnetIds=subnet-07c52409a81459e92,subnet-02403219a42dbe1ea
   ```  
   - Replace `<AWS-Account-ID>` with your account ID (find it via `aws sts get-caller-identity`).  
   - Use **public subnets** from your VPC.  

2. **Wait for the cluster to activate** (10-15 mins):  
   ```bash
   aws eks describe-cluster --name Manged-EKS-Cluster-Demo --query "cluster.status"
   ```  
   *Expected Output*: `"ACTIVE"`.  

---

### **Step 3: Configure kubectl to Access the Cluster**  
**Why?** To interact with the cluster using `kubectl`.  

1. **Update kubeconfig**:  
   ```bash
   aws eks update-kubeconfig --name Manged-EKS-Cluster-Demo --region us-east-1
   ```  

2. **Verify access**:  
   ```bash
   kubectl get nodes
   ```  
   *Output*: `No resources found` (no nodes yet).  

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
     --role-name ManagedEKSNodeGroupRole \
     --assume-role-policy-document file://node-trust-policy.json
   ```  

3. **Attach required policies**:  
   ```bash
   # Attach worker node policy
   aws iam attach-role-policy \
     --role-name ManagedEKSNodeGroupRole \
     --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy

   # Attach CNI policy (for networking)
   aws iam attach-role-policy \
     --role-name ManagedEKSNodeGroupRole \
     --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy

   # Attach ECR read-only access
   aws iam attach-role-policy \
     --role-name ManagedEKSNodeGroupRole \
     --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
   ```  

---

### **Step 5: Launch SManaged Worker Nodes**  
**Why?** Worker nodes run your Kubernetes pods.  

6. **Create an Cluster Node Group**:  
    ```bash
    # General Command
    > aws eks create-nodegroup \
    --cluster-name <EKS Cluster Name> \
    --nodegroup-name <NodeGroupName>> \
    --scaling-config minSize=1,maxSize=2,desiredSize=1 \
    --subnets <Subnet-ID-1>,<Subnet-ID-2> \
    --node-role arn:aws:iam::<account-id>:role/<nodegroup role name> \
    --remote-access ec2SshKey=<SSH Key Name> \
    --instance-types <Instance Type>> \
    --ami-type <AMI Type> \
    --capacity-type ON_DEMAND|Spot \
    --update-config maxUnavailable=1 \
    --labels node.kubernetes.io/scope=system \
    --tags <Key>=<Value>
    

    # Example
    aws eks create-nodegroup \
    --cluster-name Manged-EKS-Cluster-Demo \
    --nodegroup-name MangedWorkerNodeGroup \
    --scaling-config minSize=1,maxSize=2,desiredSize=1 \
    --subnets subnet-12345678 subnet-12345678 \
    --node-role arn:aws:iam::1234567890:role/ManagedEKSNodeGroupRole \
    --remote-access ec2SshKey=eksWorkerKey \
    --instance-types t3.medium \
    --ami-type AL2_x86_64 \
    --capacity-type ON_DEMAND \
    --update-config maxUnavailable=1 \
    --labels node.kubernetes.io/scope=system \
    --tags Application=ManagedNodeGroupApp
    ```  
    Or you can use eksctl as well, to create cluster and node groups

---

### **Step 6: AVerify Node Group Status**  
**Why?** Nodes need RBAC permissions to register with the control plane.  

1. **Verify the `aws-auth` ConfigMap**:  
  Above node group creation command automatically added our Worker Node Role to aws-auth configmap.
  ```yaml
  > kubectl get cm aws-auth -n kube-system -o yaml
  apiVersion: v1
  data:
    mapRoles: |
      - groups:
        - system:bootstrappers
        - system:nodes
        rolearn: arn:aws:iam::463470985368:role/ManagedEKSNodeGroupRole
        username: system:node:{{EC2PrivateDNSName}}
  kind: ConfigMap
  metadata:
    creationTimestamp: "2025-02-24T00:17:04Z"
    name: aws-auth
    namespace: kube-system
    resourceVersion: "5156"
    uid: 5ef2e2d0-a9bc-4344-9441-d6c7c95e6a93
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

### **Troubleshooting**
  1. **Node Group Fails to Create**
  IAM Permissions: Ensure the node role has AmazonEKSWorkerNodePolicy, AmazonEC2ContainerRegistryReadOnly, and AmazonEKS_CNI_Policy.

  Subnets: Use private subnets if nodes don’t need public IPs.

  2. **Nodes Not Joining the Cluster**
  Check aws-auth ConfigMap (auto-created for managed node groups):
  ```bash
  kubectl describe configmap aws-auth -n kube-system
  ```
  Security Groups: Ensure nodes can communicate with the EKS API (port 443).

  3. **SSH Access Issues**
  Ensure the key pair (my-keypair) exists in your AWS region.

### **Cleanup**  
Avoid unnecessary charges by deleting resources:  
  ```bash
  # Delete the EKS cluster
  aws eks delete-cluster --name Manged-EKS-Cluster-Demo

  # Delete the Node Group
  aws eks delete-nodegroup --nodegroup-name MangedWorkerNodeGroup --cluster-name Manged-EKS-Cluster-Demo

  # Delete IAM roles
  aws iam delete-role --role-name ManagedEKSClusterRole
  aws iam delete-role --role-name ManagedEKSNodeGroupRole
  ```  

---

### **Conclusion**  
Managed node groups simplify Kubernetes operations by automating node provisioning, scaling, and updates. By following this guide, you’ve learned to:

1. Create an EKS cluster. 
2. Deploy managed nodes with AWS-optimized configurations. 
3. Troubleshoot common issues. 

You’ve successfully created an EKS cluster with self-managed worker nodes! Key takeaways:  
1. **IAM Roles**: Ensure correct trust policies and permissions.  
2. **Security Groups**: Configure inbound/outbound rules properly.  
3. **`aws-auth` ConfigMap**: Critical for node authentication.  

**Next Steps**:  
  Explore [EKS Add-ons](https://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html) for logging, monitoring, and security.
  Configure [Cluster Autoscaler](https://docs.aws.amazon.com/eks/latest/userguide/autoscaling.html) for dynamic scaling.

Got questions or facing issues? Let me know in the comments! 👇  

---  

**Additional Resources**:  
- [AWS EKS Documentation](https://docs.aws.amazon.com/eks/latest/userguide/)  
- [Troubleshooting EKS Nodes](https://docs.aws.amazon.com/eks/latest/userguide/troubleshooting.html)