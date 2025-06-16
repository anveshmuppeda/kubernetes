---
// filepath: kubernetes/docs/eks/007-kubecost.md
sidebar_label: "Kubecost"
sidebar_position: 7
---  

# Amazon EKS Kubecost: A Hands-On Guide
#### *Monitor and optimize your Kubernetes costs with step-by-step instructions.*

This guide covering what Kubecost is, why you’d use it, and exactly how to install, access, and uninstall it on Amazon EKS (without mentioning specific version numbers).

![Kubecost](./img/kubecost.gif)

### **Summary**  
[Kubecost](https://github.com/kubecost) is an open‑core tool that provides real‑time visibility into your Kubernetes spending—breaking down costs by cluster, namespace, pod, node, and label—to help teams allocate, optimize, and continuously reduce cloud costs. You can deploy it on Amazon EKS either as an AWS‑managed add‑on or via Helm, then port‑forward or expose its dashboard to visualize and manage your spend. When you’re done, you can remove it cleanly with a single CLI command or Helm uninstall sequence.

## What is Kubecost and Why Use It

Kubecost provides real‑time cost visibility and insights for teams running Kubernetes, helping you continuously reduce your cloud spend by surfacing where costs occur and suggesting optimizations.
It breaks down your bill by cluster, namespace, pod, node, persistent volume, and custom labels—enabling charge‑back, show‑back, and right‑sizing across teams or projects.

## Installing Kubecost

### 1. As an Amazon EKS Add‑on

**Prerequisites**

* Subscribe to “[Kubecost – Amazon EKS cost monitoring](https://aws.amazon.com/marketplace/seller-profile?id=983de668-2731-4c99-a7e2-74f27d796173)” in the AWS Marketplace.
* Have `kubectl`, the AWS CLI, and access to your EKS cluster. 

**Install using AWS CLI**

```bash
aws eks create-addon \
  --addon-name kubecost_kubecost \
  --cluster-name YOUR_CLUSTER_NAME \
  --region YOUR_REGION
```
![Kubecost EKS Add-on](./img/kubecost-addon.png)

**Install using CFT**

Use the [AWS CloudFormation template - Kubecost](./cloudformation/eks-kubecost.yaml) to deploy the 
IBM Kubecost - Amazon EKS cost monitoring add‑on. 


This deploys the AWS‑optimized Kubecost bundle, complete with built‑in Prometheus and kube‑state‑metrics.

### 2. With Helm

**Prerequisites**

* Install `kubectl`, Helm 3+, and access to your EKS cluster (plus the Amazon EBS CSI driver). 

**Install**

1. Add the Kubecost Helm repo

   ```bash
   helm repo add kubecost https://kubecost.github.io/cost-analyzer/
   helm repo update
   ```
2. Install the Kubecost Helm chart

   ```bash
   helm install kubecost kubecost/cost-analyzer -n kubecost --create-namespace \
    --set kubecostToken="aGVsbUBrdWJlY29zdC5jb20=xm343yadf98"
   ```
   kubecostToken, it is generated at http://kubecost.com/install, used for alerts tracking and free trials. 
   Or you can use the following command to install the latest version of Kubecost:

    ```bash
    helm upgrade -i kubecost \
        oci://public.ecr.aws/kubecost/cost-analyzer \
        --namespace kubecost --create-namespace \
        -f https://raw.githubusercontent.com/kubecost/cost-analyzer-helm-chart/develop/cost-analyzer/values-eks-cost-monitoring.yaml
    ```

This drops in Kubecost along with its required dependencies; you can further customize via additional Helm values.

## Using Kubecost

1. **Verify pods are running**

   ```bash
   > kubectl get pods -n kubecost
    NAME                                         READY   STATUS    RESTARTS   AGE
    kubecost-cost-analyzer-ff44d778f-lsgrh       4/4     Running   0          5m16s
    kubecost-forecasting-56475fdf55-jwb26        1/1     Running   0          5m16s
    kubecost-prometheus-server-bb875b789-zd6d9   1/1     Running   0          5m16s
   ```
2. **Expose the dashboard**

   ```bash
   > kubectl port-forward --namespace kubecost deployment/kubecost-cost-analyzer 9090
    Forwarding from 127.0.0.1:9090 -> 9090
    Forwarding from [::1]:9090 -> 9090
    Handling connection for 9090
    Handling connection for 9090 
   ```
3. **Browse the UI**
   Open [http://localhost:9090](http://localhost:9090) in your browser to view cost allocations, asset spend, and efficiency insights .

## Uninstalling Kubecost

### Remove the EKS Add‑On

```bash
aws eks delete-addon \
  --addon-name kubecost_kubecost \
  --cluster-name YOUR_CLUSTER_NAME \
  --region YOUR_REGION
``` 

### Remove the CloudFormation Stack

```bash
aws cloudformation delete-stack \
  --stack-name YOUR_STACK_NAME
```
This removes the Kubecost add‑on and all associated resources.

### Uninstall the Helm Release  
```bash
helm uninstall kubecost --namespace kubecost
kubectl delete namespace kubecost
```

---

With this guide, you can quickly set up Kubecost for cost visibility in your EKS clusters, explore your spending through a live dashboard, and remove it cleanly when it’s no longer needed.  

---
## Additional Resources
* [Kubecost Documentation](https://docs.kubecost.com/)
* [Kubecost GitHub](https://github.com/kubecost)
* [Kubecost on AWS Marketplace](https://aws.amazon.com/marketplace/seller-profile?id=983de668-2731-4c99-a7e2-74f27d796173)
* [Kubecost on AWS Blog](https://docs.aws.amazon.com/eks/latest/userguide/cost-monitoring-kubecost.html)