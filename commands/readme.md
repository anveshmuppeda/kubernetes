# Welcome to Kubectl cheatsheet  

## Cluster 

### listing all the resources in cluster
```
k api-resources
```
### decode and encode of data for k8's to use in secrets
```
echo -n "anvesh" | base64
echo -n "" | base64 --decode
```
### To Check Access  
```
kuebctl auth can-i create deployments
kubectl auth can-i create pods
```
Switching Between Contexts


## Labels & Selectors 
### Labeling a node
```
kubectl label node <nodename> <labelname>
```

### remove Label from a node
```
kubectl label node <nodename> <labelname>-
```

### to list nodes with the labels
```
kubectl get nodes --show-labels
```

## Container 

### to login inside docker container
```
docker exec -it <container name> /bin/bash
```

## Pod
### To curl to a pod 
```
kubectl exec -it selenium-hub-b4bb44946-xthvr -n selenium — curl http://192.168.194.81:4444/wd/hub/status
```
### to list all pods in a cluster
```
kubectl get pods -A
```
### to print env variables of a pod
```
kubectl exec <pod-name> -- printenv
```
### to login inside pod  
```
winpty kubectl exec -it -n <n-s> <pod> sh
```
### to delete all pods which are evicted with namespace wise
```
kubectl get pod -n <name-space> | grep Evicted | awk '{print $1}' | xargs kubectl delete pod -n <name-space>
```

## Nodes 
### to list nodes with the resource usage
```
kubectl top node
```
### to remove a taint from node
```
kubectl taint nodes node1 key1=value1:NoSchedule-
kubectl taint nodes node1 key1=value1:NoExecute-
kubectl taint nodes node1 key2=value2:NoSchedule-
```
### taint a node with key and value and taint effect
```
kubectl taint nodes node1 key1=value1:NoSchedule
kubectl taint nodes node1 key1=value1:NoExecute
kubectl taint nodes node1 key2=value2:NoSchedule
```
