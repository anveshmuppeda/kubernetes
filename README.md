# kubernetes
Kuberntes Complete Notes. 

### Use below link to run the K8's objects  
https://kubernetes.io/docs/tutorials/hello-minikube/

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
 
