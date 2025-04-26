# Kubernetes Complete Hands‑On Guides 
<div align="center"> 
  <img src="https://awesome.re/badge.svg" alt="Awesome"/>
  <img src="https://img.shields.io/github/license/anveshmuppeda/kubernetes" alt="GitHub License"/>
  <img src="https://img.shields.io/github/contributors/anveshmuppeda/kubernetes" alt="GitHub contributors"/>
  <img src="https://img.shields.io/github/issues/anveshmuppeda/kubernetes" alt="Open Issues"/>
  <img src="https://img.shields.io/github/issues-pr-raw/anveshmuppeda/kubernetes" alt="Open PRs"/>
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" alt="PRs Welcome"/>
  <img src="https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99" alt="Star Badge"/>
</div>

<!-- 
[![Awesome](https://awesome.re/badge.svg)](https://awesome.re) 
[![GitHub License](https://img.shields.io/github/license/anveshmuppeda/kubernetes?color=blue)](https://github.com/anveshmuppeda/kubernetes/blob/main/LICENSE) 
[![GitHub contributors](https://img.shields.io/github/contributors/anveshmuppeda/kubernetes)](https://github.com/anveshmuppeda/kubernetes/graphs/contributors) 
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/anveshmuppeda/kubernetes/pulls) 
[![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99)](https://github.com/anveshmuppeda/kubernetes)
<img src="https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99" alt="Star Badge"/> 

-->  

</div>

### **Author**: [Anvesh Muppeda ![Profile Pic](https://avatars.githubusercontent.com/u/115966808?v=4&s=20)](https://github.com/anveshmuppeda)  

[![GitHub](https://img.shields.io/badge/GitHub-Profile-blue?logo=github&style=flat)](https://github.com/anveshmuppeda)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin&style=flat)](https://www.linkedin.com/in/anveshmuppeda/)
[![Twitter](https://img.shields.io/badge/Twitter-Follow-blue?logo=twitter&style=flat)](https://twitter.com/Anvesh66743877)
[![Medium](https://img.shields.io/badge/Medium-Blog-black?logo=medium&style=flat)](https://medium.com/@muppedaanvesh)
[![Email](https://img.shields.io/badge/Email-Contact%20Me-red?logo=gmail&style=flat)](mailto:muppedaanvesh@gmail.com)
[![DockerHub](https://img.shields.io/badge/DockerHub-Profile-blue?logo=docker&style=flat)](https://hub.docker.com/u/anvesh35)

---

🚀 **Community-Driven Knowledge Hub**  
*We welcome contributions to build the most comprehensive Kubernetes hands-on resource!*

📢 **How You Can Help**:
- 🐛 [Report Issues](https://github.com/anveshmuppeda/kubernetes/issues)
- 💡 [Suggest New Guides](https://github.com/anveshmuppeda/kubernetes/discussions)
- ✍️ [Submit Article Improvements](https://github.com/anveshmuppeda/kubernetes/pulls)
- 📚 [Add Missing Concepts](CONTRIBUTING.md#adding-content)
- ✅ [Review Open PRs](https://github.com/anveshmuppeda/kubernetes/pulls)

[![Open Issues](https://img.shields.io/github/issues-raw/anveshmuppeda/kubernetes)](https://github.com/anveshmuppeda/kubernetes/issues)
[![Good First Issues](https://img.shields.io/github/issues/anveshmuppeda/kubernetes/good%20first%20issue)](https://github.com/anveshmuppeda/kubernetes/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22)
[![Open PRs](https://img.shields.io/github/issues-pr-raw/anveshmuppeda/kubernetes)](https://github.com/anveshmuppeda/kubernetes/pulls)

---

## Table of Contents
- [Why These Guides?](#why-these-guides)
- [Introduction](#introduction)
- [My Blogs On Kubernetes](#my-blogs-on-kubernetes)
- [Architecture](#architecture)
  - [Master Node Components](#master-node-components)
  - [Worker Node Components](#worker-node-components)
- [Basic Concepts](#basic-concepts)
  - [Pods](#pods)
  - [Services](#services)
  - [Volumes](#volumes)
  - [Namespaces](#namespaces)
  - [Deployments](#deployments)
- [Conclusion](#conclusion)
- [References](#references)

## Why These Guides? 💡
✅ **Battle-Tested Content** - Lessons from managing 1000+ pods in production  
✅ **Cloud-Agnostic** - Works on AWS EKS, GCP GKE, Azure AKS, and bare metal  
✅ **Version Current** - Updated for Kubernetes 1.32+ features  
✅ **Zero Fluff** - Direct executable examples with explanations  

## Introduction
Kubernetes, also known as K8s, is an open-source container orchestration platform designed to automate the deployment, scaling, and management of containerized applications. It groups containers into logical units for easy management and discovery, ensuring high availability and scalability.

## My Blogs On Kubernetes  
### Here is a List of My Blog Posts on Kubernetes   

<!-- BLOG-POST-LIST:START -->  
| No. | Date       | Title |  
| --- | ---------- | ----- |  
| 1   | N/A | [A Hands-on Guide to Kubernetes Custom Resource Definitions (CRDs) with a Practical Example](https://medium.com/@muppedaanvesh/a-hand-on-guide-to-kubernetes-custom-resource-definitions-crds-with-a-practical-example-%EF%B8%8F-84094861e90b) |
| 2   | N/A | [A Hands-on Guide to Vault in Kubernetes](https://medium.com/@muppedaanvesh/a-hand-on-guide-to-vault-in-kubernetes-%EF%B8%8F-1daf73f331bd) |
| 3   | N/A | [A Hands-on Guide to Kubernetes Resource Quotas & Limit Ranges](https://medium.com/@muppedaanvesh/a-hand-on-guide-to-kubernetes-resource-quotas-limit-ranges-%EF%B8%8F-8b9f8cc770c5) |
| 4   | N/A | [Rolling Update & Recreate Deployment Strategies in Kubernetes](https://medium.com/@muppedaanvesh/rolling-update-recreate-deployment-strategies-in-kubernetes-%EF%B8%8F-327b59f27202)
| 5   | N/A | [Blue-Green Deployment in Kubernetes](https://medium.com/@muppedaanvesh/blue-green-deployment-in-kubernetes-76f9153e0805)
| 6   | N/A | [A Hands-on Guide to Kubernetes Volumes](https://medium.com/@muppedaanvesh/a-hand-on-guide-to-kubernetes-volumes-%EF%B8%8F-b59d4d4e347f)
| 7   | N/A | [A Hands-on Guide to Kubernetes RBAC with a User Creation](https://medium.com/@muppedaanvesh/a-hand-on-guide-to-kubernetes-rbac-with-a-user-creation-%EF%B8%8F-1ad9aa3cafb1)
| 8   | N/A | [Implementing Canary Deployment in Kubernetes](https://medium.com/@muppedaanvesh/implementing-canary-deployment-in-kubernetes-0be4bc1e1aca)
| 9   | N/A | [A Hands-on Guide to Kubernetes Pod Disruption Budget (PDB)](https://medium.com/@muppedaanvesh/a-hand-on-guide-to-kubernetes-pod-disruption-budget-pdb-%EF%B8%8F-ebe3155a4b7c)
| 10   | N/A | [A Hands-on Guide to Kubernetes CronJobs](https://medium.com/@muppedaanvesh/a-hand-on-guide-to-kubernetes-cronjobs-%EF%B8%8F-47393a98716d)
| 11   | N/A | [A Hands-on Guide to Kubernetes Jobs](https://medium.com/@muppedaanvesh/a-hand-on-guide-to-kubernetes-jobs-%EF%B8%8F-aa2edbb061ea)
| 12   | N/A | [Mastering Kubernetes Backups with Velero](https://medium.com/@muppedaanvesh/%EF%B8%8F-mastering-kubernetes-backups-with-velero-60cf05e6d9a1)
| 13   | N/A | [Kubernetes Ingress: Transitioning to HTTPS with Self-Signed Certificates](https://medium.com/@muppedaanvesh/%EF%B8%8F-kubernetes-ingress-transitioning-to-https-with-self-signed-certificates-0c7ab0231e76)
| 14   | N/A | [Mastering Kubernetes ConfigMaps](https://medium.com/@muppedaanvesh/%EF%B8%8F-mastering-kubernetes-configmaps-accced50e69a)
| 15   | N/A | [Secure Your Kubernetes Apps: Hands-On Basic Authentication with Ingress](https://medium.com/@muppedaanvesh/secure-your-kubernetes-apps-hands-on-basic-authentication-with-ingress-55bc6dfeb1e5)
| 16   | N/A | [Migrating Angular .NET Docker Environment to Kubernetes](https://medium.com/@muppedaanvesh/migrating-angular-net-docker-environment-to-kubernetes-8f010b597b91)
| 17   | N/A | [Exploring Types of Routing-Based Ingresses in Kubernetes](https://medium.com/@muppedaanvesh/%EF%B8%8F-exploring-types-of-routing-based-ingresses-in-kubernetes-da56f51b3a6b)
| 18   | N/A | [A Hands-On Guide to Kubernetes Ingress Nginx](https://medium.com/@muppedaanvesh/a-hands-on-guide-to-kubernetes-ingress-nginx-7c4c5b45eb89)
| 19   | N/A | [Mastering Kubernetes Ingress](https://medium.com/@muppedaanvesh/mastering-kubernetes-ingress-2c86ae412e79)
| 20   | N/A | [From Docker to Kubernetes: Elevating Our Login App](https://aws.plainenglish.io/from-docker-to-kubernetes-elevating-our-login-app-a95506e9320a)
| 21   | N/A | [Kubernetes Taints & Tolerations](https://medium.com/@muppedaanvesh/kubernetes-taints-tolerations-b0e0ed076cad)
| 22   | N/A | [Azure DevOps Self-Hosted Agents on Kubernetes: Part 3](https://medium.com/@muppedaanvesh/azure-devops-self-hosted-agents-on-kubernetes-part-3-6658d741b369)
| 23   | N/A | [Azure DevOps Self-Hosted Agents on Kubernetes: Part 2](https://medium.com/@muppedaanvesh/azure-devops-self-hosted-agents-on-kubernetes-part-2-b0297eb94c1f)
| 24   | N/A | [Azure DevOps Self-Hosted Agents on Kubernetes: Part 1](https://medium.com/@muppedaanvesh/azure-devops-self-hosted-agents-on-kubernetes-part-1-aa91e7912f79)
| 25   | N/A | [Understanding Kubernetes Pod Fields](https://medium.com/@muppedaanvesh/understanding-kubernetes-pod-fields-2192cc850fdb)
| 26   | N/A | [kubectl Helper: Your Ultimate Kubernetes Command Companion](https://medium.com/@muppedaanvesh/kubectl-helper-your-ultimate-kubernetes-command-companion-bf9351caf824)
| 27   | N/A | [Exploring Container Types in Kubernetes: Beyond Init and Sidecar Containers](https://medium.com/@muppedaanvesh/exploring-container-types-in-kubernetes-beyond-init-and-sidecar-containers-3c1001bb7a85)
| 28   | N/A | [Deploying NGINX on Kubernetes: A Quick Guide](https://medium.com/@muppedaanvesh/deploying-nginx-on-kubernetes-a-quick-guide-04d533414967)
| 29   | N/A | [Setting Up an Amazon EKS Cluster and Node Group Using eksctl](https://medium.com/@muppedaanvesh/setting-up-an-amazon-eks-cluster-and-node-group-using-eksctl-52acc808eb83)
| 30   | N/A | [Jump Box Setup on EKS Cluster](https://medium.com/@muppedaanvesh/jump-box-setup-on-eks-cluster-383ca92f51ef)  
| 31   | N/A | [⎈ A Hands-On Guide to Kubernetes External Secrets Operator 🛠️](https://medium.com/@muppedaanvesh/a-hands-on-guide-to-kubernetes-external-secrets-operator-%EF%B8%8F-6e630c2da25e)
| 32   | N/A | [⎈ A Hands-On Guide to Kubernetes Priority Classes 🛠️](https://medium.com/@muppedaanvesh/a-hands-on-guide-to-kubernetes-priority-classes-%EF%B8%8F-e4d37d789311)  
| 33   | N/A | [⎈ A Hands-On Guide to Kubernetes Horizontal & Vertical Pod Autoscalers 🛠️](https://medium.com/@muppedaanvesh/a-hands-on-guide-to-kubernetes-horizontal-vertical-pod-autoscalers-%EF%B8%8F-58903382ef71) 
| 34   | N/A | [⎈ A Hands-On Guide to Kubernetes QoS Classes🛠️](https://medium.com/@muppedaanvesh/a-hands-on-guide-to-kubernetes-qos-classes-%EF%B8%8F-571b5f8f7e58)
| 35   | N/A | [⎈ A Hands-On Guide to Kubernetes Endpoints & EndpointSlices 🛠️](https://medium.com/@muppedaanvesh/a-hands-on-guide-to-kubernetes-endpoints-endpointslices-%EF%B8%8F-1375dfc9075c)
| 36 | 2025-04-14 | [⎈ AWS EKS Pod Identity vs IRSA ️](https://medium.com/@muppedaanvesh/aws-eks-pod-identity-vs-irsa-%EF%B8%8F-3f2464df1a94?source=rss-15b2de10f77d------2) |
| 37 | 2025-04-14 | [⎈ Karpenter + EKS: The Smart Way to Scale ️](https://medium.com/@muppedaanvesh/karpenter-eks-the-smart-way-to-scale-%EF%B8%8F-cec53ab48260?source=rss-15b2de10f77d------2) |
| 38 | 2025-04-08 | [⎈ A Hands-On Guide to AWS EKS IAM Roles for Service Accounts (IRSA) ️](https://medium.com/@muppedaanvesh/a-hands-on-guide-to-aws-eks-iam-roles-for-service-accounts-irsa-%EF%B8%8F-558c7a3e7c69?source=rss-15b2de10f77d------2) |
| 39 | 2025-04-07 | [⎈ A Hands-On Guide to AWS EKS Pod Identity ️](https://medium.com/@muppedaanvesh/a-hands-on-guide-to-aws-eks-pod-identity-%EF%B8%8F-8e236b779d1a?source=rss-15b2de10f77d------2) |
| 40 | 2025-03-31 | [EKS Debug with AI Assistant ️](https://medium.com/@muppedaanvesh/eks-debug-with-ai-assistant-%EF%B8%8F-7e235c46cace?source=rss-15b2de10f77d------2) |
| 41 | 2025-02-24 | [⎈ A Hands-On Guide to AWS EKS Fargate Cluster ️](https://medium.com/@muppedaanvesh/a-hands-on-guide-to-aws-eks-fargate-cluster-%EF%B8%8F-2172934fff94?source=rss-15b2de10f77d------2) |
| 42 | 2025-02-24 | [⎈ Hands-On Guide to Creating an Amazon EKS Cluster with Managed Node Groups⎈](https://medium.com/@muppedaanvesh/hands-on-guide-to-creating-an-amazon-eks-cluster-with-managed-worker-nodes-1bd983e0fcbd?source=rss-15b2de10f77d------2) |
| 43 | 2025-02-23 | [⎈ Hands-On Guide to Creating an Amazon EKS Cluster with Self-Managed Worker Nodes ⎈](https://medium.com/@muppedaanvesh/hands-on-guide-to-creating-an-amazon-eks-cluster-with-self-managed-worker-nodes-fad026c34482?source=rss-15b2de10f77d------2) |
| 44 | 2025-04-21 | [⎈ Hands-On FluxCD: GitOps for Kubernetes at Scale ️](https://medium.com/@muppedaanvesh/hands-on-fluxcd-gitops-for-kubernetes-at-scale-%EF%B8%8F-7e3d06ed4c35?source=rss-15b2de10f77d------2) |

















<!-- BLOG-POST-LIST:END -->

## Architecture

![Kubernetes Architecture](./assets/kubernetes-architecture.png)  

### Master Node Components
The master node is responsible for managing the Kubernetes cluster. It oversees the nodes and the pods running within the cluster. Key components of the master node include:

- **API Server:** Exposes the Kubernetes API, acting as the front end for the Kubernetes control plane.
- **Etcd:** A consistent and highly-available key-value store used for all cluster data.
- **Scheduler:** Assigns workloads to the worker nodes based on resource availability.
- **Controller Manager:** Runs controller processes to regulate the state of the cluster, handling tasks like node failures and endpoint management.
- **Cloud Controller Manager:** Manages cloud-specific controller processes.

### Worker Node Components
Worker nodes run the applications and handle the containerized workloads. Each worker node has its own set of components:

- **Kubelet:** Ensures that containers are running in a pod by communicating with the master node.
- **Kube-proxy:** Maintains network rules and handles network communication within and outside the cluster.
- **Container Runtime:** Runs the containers. Common runtimes include Docker, containerd, and CRI-O.

## Basic Concepts

### Pods
Pods are the smallest deployable units in Kubernetes, representing a single instance of a running process. They encapsulate one or more containers, storage resources, a unique network IP, and options for how the containers should run.

### Services
Services provide stable endpoints for accessing the running pods. They enable communication between different parts of an application and can expose the application to external traffic.

### Volumes
Volumes offer persistent storage that pods can use. Unlike containers, which are ephemeral, volumes retain data even after a pod is terminated.

### Namespaces
Namespaces are a way to divide cluster resources between multiple users. They provide scope for names, allowing for resource management and access control.

### Deployments
Deployments define the desired state for application deployment, specifying the number of replicas, the container image to use, and update strategies. They enable declarative updates to applications and rollbacks if necessary.

## Conclusion
Kubernetes provides a robust platform for managing containerized applications, offering powerful abstractions to ensure applications are scalable, resilient, and easy to manage. Understanding the basic architecture and concepts is essential for effectively leveraging Kubernetes in your projects.

## References
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Kubernetes GitHub Repository](https://github.com/kubernetes/kubernetes)
- [Kubernetes API Reference](https://kubernetes.io/docs/reference/)  
- [Kubernetes Icon Set](https://github.com/kubernetes/community/blob/master/icons/README.md)
- [Minikube Play Ground](https://kubernetes.io/docs/tutorials/hello-minikube/)
- [K8s Labs](https://labs.play-with-k8s.com/)  
- [Killercoda Play Ground](https://killercoda.com/playgrounds/scenario/kubernetes)  

<a name="contributing"></a>  
## Project Maintainers & Contributors  
<table>
  <tr>
    <td align="center"><a href="https://anveshmuppeda.github.io/profile/"><img src="https://avatars.githubusercontent.com/u/115966808?v=4" width="100px;" alt=""/><br /><sub><b>Anvesh Muppeda</b></sub></a></td>
    <td align="center"><a href="https://github.com/saimanasak"><img src="https://avatars.githubusercontent.com/u/47205414?v=4" width="100px;" alt=""/><br /><sub><b>Sai Manasa Kota</b></sub></a></td>  
    <td align="center"><a href="https://github.com/Rohinigundala2019"><img src="https://avatars.githubusercontent.com/u/181216819?v=4" width="100px;" alt=""/><br /><sub><b>Rohini Gundala</b></sub></a></td> 
  </tr>
</table>  

## License
This project is licensed under the GNU License - see the [LICENSE](https://github.com/anveshmuppeda/kubernetes/blob/main/LICENSE) file for details.  

## Stargazers over time
[![Stargazers over time](https://starchart.cc/anveshmuppeda/kubernetes.svg?variant=adaptive)](https://starchart.cc/anveshmuppeda/kubernetes)  