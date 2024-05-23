# Kubernetes  
Kuberntes Complete Notes.  

## Here is a List of My Blog Posts on Kubernetes  
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

### Kubernetes Icons Set   
https://github.com/kubernetes/community/blob/master/icons/README.md  

### Use below link to run the K8's objects  
https://kubernetes.io/docs/tutorials/hello-minikube/  
https://labs.play-with-k8s.com/  
https://killercoda.com/playgrounds/scenario/kubernetes  

### Example code and execution for each k8's objects can be found under below path  
```examples\<object-name>```

## Kubernetes Architecture and It's Components
![image](https://user-images.githubusercontent.com/115966808/227559209-95505f77-2017-4266-8d47-14bb273e490b.png)
### 1. etcd
#### Install etcd
1. Download Binaries   
``` curl -L https://github.com/etcd-io/etcd/releases/download/v3.3.11/etcdv3.3.11-linux-amd64.tar.gz -o etcd-v3.3.11-linux-amd64.tar.gz``` 
2. Extract  
```tar xzvf etcd-v3.3.11-linux-amd64.tar.gz``` 
3. Run etcd service  
```tar xzvf etcd-v3.3.11-linux-amd64.tar.gz```
4. Assign key values.  
```./etcdctl set key1 value1```
5. Get the key value.  
```./etcdctl get key1``` 
### 2. Kube-API server. 
#### Functionalities of Kube-API server.  
1. Authenticate User.  
2. Validate Request.  
3. Retrieve Data. 
4. Update ETCD. 
5. Communicate with Scheduler. 
6. Communicate with kubelet.  
### 3. Kube Controller Manager.  
#### Functionalities of Kube-Controller Manager  
1. Watch Status  
2. Remidiate Situation   
#### Default Values  
```
Node Monitor Period = 5s
Node Monitor Grace Period = 40s
POD Eviction Timeout = 5m
```
### 4. Kube-Scheduler  
#### Installing kube-scheduler   
```wget https://storage.googleapis.com/kubernetes-release/release/v1.13.0/bin/linux/amd64/kube-scheduler```  
#### View kube-scheduler options - kubeadm   
```cat /etc/kubernetes/manifests/kube-scheduler.yaml```  

### 5. Kubelet  
#### Functionalities  
* Register Node  
* Create PODs  
* Monitor Node & PODs  
#### Installing  
```wget https://storage.googleapis.com/kubernetes-release/release/v1.13.0/bin/linux/amd64/kubelet```
#### Kubelet options  
```ps -aux | grep kubelet``` 
### 6. Kubeproxy  
 #### Installing  
```wget https://storage.googleapis.com/kubernetes-release/release/v1.13.0/bin/linux/amd64/kube-proxy``` 

***

## Kubernetes Objects 
### Container
### Pod  
Command to check the pod details node wise:  
```kubectl get pods -o wide```  

### Replicaset  
Command to override the existing definitions:  
```kubectl replace -f replicaset.yamml```  

### Deployment
### Daemonset
### Statefulset
### Labels and Selector 
As their name suggests, label selectors allow you to identify the objects you have tagged with particular labels. Label selectors can either be equality-based or set-based. Equality-based label selectors work by specifying an exact value that you want to match against. If you provide multiple selectors, all of them must be satisfied to qualify as a match.   
```
metadata:
  name: label-demo
  labels:
    environment: production
    app: nginx
```
```
kubectl get pods --selector app=nginx  
kubectl get pods --l app=nginx  
```
To add a label to an existing resource, you can use the following command:  
```
# this will create a label “group” with a value of “main”  
kubectl label pod/metadata-demo group=main  
```
You can also remove the label using this command:
```
# remove the “group” label from the resource  
kubectl label pod/metadata-demo group-  
```
### Taints and Tolerations
Update the taints on one or more nodes.
A taint consists of a key, value, and effect. As an argument here, it is expressed as key=value:effect.  

If a pod has tolerations that match the taints on a node, the scheduler will place the pod on that node. If there are no taints on the node, then any pod with or without tolerations can be scheduled on the node.  

The effect must be 
* NoSchedule
* PreferNoSchedule
* NoExecute  

Currently taint can only apply to node.  

**USAGE**  
```
$ kubectl taint NODE NAME KEY_1=VAL_1:TAINT_EFFECT_1
$ kubectl taint nodes nodename dedicated=special-user:NoSchedule
```
For Untaint  
```
$ kubectl taint nodes nodename dedicated=special-user:NoSchedule-
```
You specify a toleration for a pod in the PodSpec. Both of the following tolerations "match" the taint created by the kubectl taint line above, and thus a pod with either toleration would be able to schedule onto node1.  
```
tolerations:
- key: "dedicated"
  operator: "Equal"
  value: "special-user"
  effect: "NoSchedule"
```
The default value for operator is **Equal**.  
A toleration "matches" a taint if the keys are the same and the effects are the same, and:  
* the operator is **Exists** (in which case no value should be specified). 
* the operator is **Equal** and the values are equal.  

### Node Selector  
This node selector helpful to schedule the pods on to specific node.  
First we need to add the labels to the required node.  
```
kubectl label nodes nodename size=t2micro
```
Then we need to add the below code into the definition file.   
```
nodeSelector:
    size: t2micro
```

***

## Commands  
 Generate POD Manifest YAML file (-o yaml). Don't create it(--dry-run)  

```kubectl run nginx --image=nginx --dry-run=client -o yaml``` 
 
