# Kubernetes  
Kuberntes Complete Notes.  

## Table of Contents
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

## Introduction
Kubernetes, also known as K8s, is an open-source container orchestration platform designed to automate the deployment, scaling, and management of containerized applications. It groups containers into logical units for easy management and discovery, ensuring high availability and scalability.

## My Blogs On Kubernetes  
### Here is a List of My Blog Posts on Kubernetes   
1. [A Hands-on Guide to Kubernetes Custom Resource Definitions (CRDs) with a Practical Example](https://medium.com/@muppedaanvesh/a-hand-on-guide-to-kubernetes-custom-resource-definitions-crds-with-a-practical-example-%EF%B8%8F-84094861e90b)
2. [A Hands-on Guide to Vault in Kubernetes](https://medium.com/@muppedaanvesh/a-hand-on-guide-to-vault-in-kubernetes-%EF%B8%8F-1daf73f331bd)
3. [A Hands-on Guide to Kubernetes Resource Quotas & Limit Ranges](https://medium.com/@muppedaanvesh/a-hand-on-guide-to-kubernetes-resource-quotas-limit-ranges-%EF%B8%8F-8b9f8cc770c5)
4. [Rolling Update & Recreate Deployment Strategies in Kubernetes](https://medium.com/@muppedaanvesh/rolling-update-recreate-deployment-strategies-in-kubernetes-%EF%B8%8F-327b59f27202)
5. [Blue-Green Deployment in Kubernetes](https://medium.com/@muppedaanvesh/blue-green-deployment-in-kubernetes-76f9153e0805)
6. [A Hands-on Guide to Kubernetes Volumes](https://medium.com/@muppedaanvesh/a-hand-on-guide-to-kubernetes-volumes-%EF%B8%8F-b59d4d4e347f)
7. [A Hands-on Guide to Kubernetes RBAC with a User Creation](https://medium.com/@muppedaanvesh/a-hand-on-guide-to-kubernetes-rbac-with-a-user-creation-%EF%B8%8F-1ad9aa3cafb1)
8. [Implementing Canary Deployment in Kubernetes](https://medium.com/@muppedaanvesh/implementing-canary-deployment-in-kubernetes-0be4bc1e1aca)
9. [A Hands-on Guide to Kubernetes Pod Disruption Budget (PDB)](https://medium.com/@muppedaanvesh/a-hand-on-guide-to-kubernetes-pod-disruption-budget-pdb-%EF%B8%8F-ebe3155a4b7c)
10. [A Hands-on Guide to Kubernetes CronJobs](https://medium.com/@muppedaanvesh/a-hand-on-guide-to-kubernetes-cronjobs-%EF%B8%8F-47393a98716d)
11. [A Hands-on Guide to Kubernetes Jobs](https://medium.com/@muppedaanvesh/a-hand-on-guide-to-kubernetes-jobs-%EF%B8%8F-aa2edbb061ea)
12. [Mastering Kubernetes Backups with Velero](https://medium.com/@muppedaanvesh/%EF%B8%8F-mastering-kubernetes-backups-with-velero-60cf05e6d9a1)
13. [Kubernetes Ingress: Transitioning to HTTPS with Self-Signed Certificates](https://medium.com/@muppedaanvesh/%EF%B8%8F-kubernetes-ingress-transitioning-to-https-with-self-signed-certificates-0c7ab0231e76)
14. [Mastering Kubernetes ConfigMaps](https://medium.com/@muppedaanvesh/%EF%B8%8F-mastering-kubernetes-configmaps-accced50e69a)
15. [Secure Your Kubernetes Apps: Hands-On Basic Authentication with Ingress](https://medium.com/@muppedaanvesh/secure-your-kubernetes-apps-hands-on-basic-authentication-with-ingress-55bc6dfeb1e5)
16. [Migrating Angular .NET Docker Environment to Kubernetes](https://medium.com/@muppedaanvesh/migrating-angular-net-docker-environment-to-kubernetes-8f010b597b91)
17. [Exploring Types of Routing-Based Ingresses in Kubernetes](https://medium.com/@muppedaanvesh/%EF%B8%8F-exploring-types-of-routing-based-ingresses-in-kubernetes-da56f51b3a6b)
18. [A Hands-On Guide to Kubernetes Ingress Nginx](https://medium.com/@muppedaanvesh/a-hands-on-guide-to-kubernetes-ingress-nginx-7c4c5b45eb89)
19. [Mastering Kubernetes Ingress](https://medium.com/@muppedaanvesh/mastering-kubernetes-ingress-2c86ae412e79)
20. [From Docker to Kubernetes: Elevating Our Login App](https://aws.plainenglish.io/from-docker-to-kubernetes-elevating-our-login-app-a95506e9320a)
21. [Kubernetes Taints & Tolerations](https://medium.com/@muppedaanvesh/kubernetes-taints-tolerations-b0e0ed076cad)
22. [Azure DevOps Self-Hosted Agents on Kubernetes: Part 3](https://medium.com/@muppedaanvesh/azure-devops-self-hosted-agents-on-kubernetes-part-3-6658d741b369)
23. [Azure DevOps Self-Hosted Agents on Kubernetes: Part 2](https://medium.com/@muppedaanvesh/azure-devops-self-hosted-agents-on-kubernetes-part-2-b0297eb94c1f)
24. [Azure DevOps Self-Hosted Agents on Kubernetes: Part 1](https://medium.com/@muppedaanvesh/azure-devops-self-hosted-agents-on-kubernetes-part-1-aa91e7912f79)
25. [Understanding Kubernetes Pod Fields](https://medium.com/@muppedaanvesh/understanding-kubernetes-pod-fields-2192cc850fdb)
26. [kubectl Helper: Your Ultimate Kubernetes Command Companion](https://medium.com/@muppedaanvesh/kubectl-helper-your-ultimate-kubernetes-command-companion-bf9351caf824)
27. [Exploring Container Types in Kubernetes: Beyond Init and Sidecar Containers](https://medium.com/@muppedaanvesh/exploring-container-types-in-kubernetes-beyond-init-and-sidecar-containers-3c1001bb7a85)
28. [Deploying NGINX on Kubernetes: A Quick Guide](https://medium.com/@muppedaanvesh/deploying-nginx-on-kubernetes-a-quick-guide-04d533414967)
29. [Setting Up an Amazon EKS Cluster and Node Group Using eksctl](https://medium.com/@muppedaanvesh/setting-up-an-amazon-eks-cluster-and-node-group-using-eksctl-52acc808eb83)
30. [Jump Box Setup on EKS Cluster](https://medium.com/@muppedaanvesh/jump-box-setup-on-eks-cluster-383ca92f51ef)  

## Architecture

![image](https://user-images.githubusercontent.com/115966808/227559209-95505f77-2017-4266-8d47-14bb273e490b.png)  

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

