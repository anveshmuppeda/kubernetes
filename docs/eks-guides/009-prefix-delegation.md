---
// filepath: /Users/anveshmuppeda/Desktop/anvesh/tech/git/kubernetes/docs/eks/008-prefix-delegation.md
sidebar_label: "EKS Prefix Delegation"
sidebar_position: 9
---  

# EKS Pod Density with Prefix Delegation: A Complete Guide

*Struggling with IP address limitations in your EKS clusters? Prefix delegation might be the game-changer you've been looking for.*

If you've ever hit the wall with pod density limitations in Amazon EKS, you're not alone. The traditional approach of assigning individual IP addresses to pods can quickly become a bottleneck, especially when you're trying to maximize resource utilization on your worker nodes. Enter **EKS Prefix Delegation** – a powerful feature that can dramatically increase your pod density and streamline IP management.

![flow chart of procedure for assigning IP to pod](./img/prefix-delegation2.jpeg)

## What is EKS Prefix Delegation?

EKS Prefix Delegation is a networking enhancement that allows the Amazon VPC CNI to assign entire IP address prefixes (blocks of IP addresses) to network interfaces instead of individual IP addresses. Think of it as getting a whole street of house numbers instead of just one address at a time.

Here's the magic: instead of assigning individual IPv4 addresses to network interface slots, the VPC CNI assigns `/28` prefixes (which contain 16 IP addresses each). This approach significantly increases the number of pods you can run on each worker node.

![illustration of two worker subnets](./img/prefix-delegation.png)

### The Numbers Don't Lie

Let's look at a concrete example with a `t3.medium` instance:
- **Without prefix delegation**: Maximum of 17 pods per node
- **With prefix delegation**: Maximum of 110 pods per node

That's more than a **6x increase** in pod density!

## How Does It Work Under the Hood?

The process is elegantly simple:

1. **Initial Setup**: During worker node initialization, the VPC CNI assigns one or more prefixes to the primary Elastic Network Interface (ENI)
2. **Smart Pre-allocation**: The CNI maintains a "warm pool" of prefixes for faster pod startup times
3. **Dynamic Scaling**: As more pods are scheduled, additional prefixes are requested for existing ENIs
4. **Efficient Resource Usage**: New ENIs are only attached when existing ones reach capacity

The system uses three key environment variables to manage the warm pool:
- `WARM_PREFIX_TARGET`: Number of prefixes to keep in reserve
- `WARM_IP_TARGET`: Number of IP addresses to keep available
- `MINIMUM_IP_TARGET`: Minimum IP addresses available at any time

## When Should You Use Prefix Delegation?

### Perfect Scenarios ✅

**Pod Density Challenges**: If you're consistently hitting pod limits on your worker nodes, prefix delegation is your solution.

**CNI Custom Networking**: Particularly beneficial when the primary ENI isn't used for pods, as you can still attach more IPs on nearly every Nitro instance type.

**Resource Optimization**: When you want to maximize the utilization of your EC2 instances and reduce infrastructure costs.

### When to Avoid ❌

**Fragmented Subnets**: If your subnet is heavily fragmented with scattered IP addresses, creating contiguous `/28` blocks might fail.

**Strict Security Requirements**: In prefix mode, security groups are shared between the worker node and pods. Consider using Security Groups for Pods if you need granular network security.

## Step-by-Step Implementation Guide

### Prerequisites
- EKS cluster with VPC CNI version 1.9.0 or later
- Sufficient contiguous IP address space in your subnets

### Step 1: Enable Prefix Delegation

First, verify your current VPC CNI setup:

```bash
# Check if VPC CNI is running
> kubectl get pods --selector=k8s-app=aws-node -n kube-system
NAME             READY   STATUS    RESTARTS   AGE
aws-node-dfvbw   2/2     Running   0          73m
aws-node-hf9tk   2/2     Running   0          73m

# Verify CNI version (must be 1.9.0+)
kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
amazon-k8s-cni-init:v1.19.2-eksbuild.5
amazon-k8s-cni:v1.19.2-eksbuild.5
```

Enable prefix delegation:

```bash
kubectl set env daemonset aws-node -n kube-system ENABLE_PREFIX_DELEGATION=true
```

Alternatively, if you're using CloudFormation, include this in your EKS addon configuration:

```yaml
MyEksAddonVpcCni:
  Type: AWS::EKS::Addon
  Properties:
    AddonName: vpc-cni
    AddonVersion: v1.19.2-eksbuild.5
    ClusterName: !Ref EKSClusterName
    ConfigurationValues: |
      {
        "env": {
          "ENABLE_PREFIX_DELEGATION": "true"
        }
      }
```
#### Without Prefix Delegation
![Without prefix delegation Mode ](./img/without-prefix-delegation.png)
#### With Prefix Delegation
![With prefix delegation Mode ](./img/with-prefix-delegation.png)

### Step 2: Verify Configuration

Check if prefix delegation is properly configured:

```bash
> kubectl get ds aws-node -o yaml -n kube-system | yq '.spec.template.spec.containers[].env'
[...]
- name: ENABLE_PREFIX_DELEGATION
  value: "true"
[...]
```

Look for `ENABLE_PREFIX_DELEGATION: "true"` in the output.

### Step 3: Test with a Sample Deployment

Create a deployment to test the increased pod density:

```bash
kubectl create deployment nginx-test --image=nginx --replicas=100
```

Monitor the pods and their IP assignments:

```bash
kubectl get pods -o wide
```

### Step 4: Verify Prefix Assignment

Check the prefixes assigned to your worker nodes:

```bash
aws ec2 describe-instances --filters "Name=tag-key,Values=eks:cluster-name" \
  "Name=tag-value,Values=${EKS_CLUSTER_NAME}" \
  --query 'Reservations[*].Instances[].{InstanceId: InstanceId, Prefixes: NetworkInterfaces[].Ipv4Prefixes[]}'
```
```bash
# Example output
- InstanceId: i-0788d2a31f7cbb6be
  Prefixes:
  - Ipv4Prefix: 10.0.131.160/28
  - Ipv4Prefix: 10.0.132.0/28
  - Ipv4Prefix: 10.0.174.128/28
  - Ipv4Prefix: 10.0.174.80/28
  - Ipv4Prefix: 10.0.166.32/28
  - Ipv4Prefix: 10.0.128.80/28
  - Ipv4Prefix: 10.0.131.224/28
- InstanceId: i-0f5b5ef7576231e4c
  Prefixes:
  - Ipv4Prefix: 10.0.128.16/28
  - Ipv4Prefix: 10.0.129.80/28
  - Ipv4Prefix: 10.0.175.64/28
  - Ipv4Prefix: 10.0.176.192/28
  - Ipv4Prefix: 10.0.180.112/28
  - Ipv4Prefix: 10.0.167.0/28
  - Ipv4Prefix: 10.0.189.96/28
```

You should see `/28` prefixes assigned to your instances.

So, here you can see that each worker node has 7 `/28` prefixes assigned, which means each node can support up to 110 pods (7 prefixes * 16 IPs per prefix = 112 IPs, minus a few reserved for system use). And 110 pods are maximum pods that can be assigned to a t3.medium instance with prefix delegation enabled.

## Pro Tips for Success

### Calculate Maximum Pod Capacity

Use [Amazon's official script](https://github.com/awslabs/amazon-eks-ami/blob/main/templates/al2/runtime/max-pods-calculator.sh) to determine the maximum pod capacity for your instance types:

```bash
> curl -O https://raw.githubusercontent.com/awslabs/amazon-eks-ami/refs/heads/main/templates/al2/runtime/max-pods-calculator.sh
> chmod +x max-pods-calculator.sh
```

```bash
# Example command to calculate max pods for t3.medium with prefix delegation enabled
> ./max-pods-calculator.sh --instance-type t3.medium --cni-version 1.9.0-eksbuild.1 --cni-prefix-delegation-enabled
110
```

### Optimize Your Configuration

1. **Use Similar Instance Types**: Keep instance types consistent within node groups to maximize efficiency
2. **Configure WARM_PREFIX_TARGET**: The default value of 1 usually provides the best balance
3. **Plan Your Subnets**: Use subnet reservations to avoid fragmentation issues
4. **Replace Nodes Gradually**: Create new node groups instead of doing rolling updates when transitioning

### Avoid Common Pitfalls

- **Never downgrade** VPC CNI below version 1.9.0 once prefix delegation is enabled
- **Plan for contiguous IP space** in your subnets to avoid allocation failures
- **Consider security implications** as pods share the worker node's security group

## Real-World Impact

Organizations implementing prefix delegation typically see:
- **60-80% reduction** in the number of worker nodes needed
- **Faster pod startup times** due to pre-allocated IP pools
- **Significant cost savings** from improved resource utilization
- **Simplified network management** with fewer ENIs to manage

## Conclusion

EKS Prefix Delegation is more than just a networking feature – it's a pathway to more efficient, cost-effective Kubernetes operations. By allowing you to pack significantly more pods onto each worker node, it can transform how you think about cluster scaling and resource utilization.

The implementation is straightforward, the benefits are substantial, and the operational overhead is minimal. If you're running production EKS clusters and haven't explored prefix delegation yet, it's time to give it a try.

Ready to supercharge your pod density? Start with a test cluster, run through the implementation steps, and see the difference for yourself. Your infrastructure costs (and your operations team) will thank you.

---

*Have you implemented prefix delegation in your EKS clusters? Share your experiences and results in the comments below!*