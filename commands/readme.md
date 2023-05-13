# Welcome to Kubectl cheatsheet  

1. [ Description. ](#desc)
2. [ Usage tips. ](#usage)

<a name="desc"></a>

sometext

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
### to Check Access  
```
kuebctl auth can-i create deployments
kubectl auth can-i create pods
```
### to check IP range for pods within the namespaces
```
kubectl cluster-info dump | grep -m 1 cluster-cidr
```
---
## Switching Between Contexts
### to list all preconfigured contexts and see which one is active:
```
kubectl config get-contexts
```
### prints the current config name
```
kubectl config current-context
```
### to switch between the predefined contexts(Switch to a context/cluster):
```
kubectl config use-context NikTest
```
---
## Labels & Selectors 
### labeling a node
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
---
## Container 

### to login inside docker container
```
docker exec -it <container name> /bin/bash
```
---
## Pod
### to curl to a pod 
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
### to get the pod definition
```
kubectl get pod pod-name -o yaml > pod.yaml
```
### to get pod definition possible options
```
kubectl explain pods --recursive | less
```
### to delete the pods which are Evicted State
```
kubectl get pod -n <namespace> | grep Evicted | awk '{print $1}' | xargs kubectl delete pod -n <name-space>
```
### to login into pod
```
winpty kubectl exec -it -n <namespace> <pod-name> sh 
```  
### to view logs from containers
```
kubectl exec <pod-name> -- cat /log/app.log
```
### to get the pod deatils with wide options
```
kubectl get pods -o wide
```
---
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
### mark node03 as unschedulable but do not remove any apps currently running on it .
```
kubectl cordon node03
```
### to drain the node01 (Empty the node of all applications and mark it unschedulable.)
```
kubectl drain node01 --ignore-daemonsets
```
### Configure the node to be schedulable again
```
kubectl uncordon node01
```

---
<a name="usage"></a>
## 2. Usage tips
## Logs
### to get the pod logs
```
kubectl -n <n-s> logs -f <pod> --tail=10
kubectl -n namespace-name logs pod-name
kubectl logs -n namespace container-name --since 10m
kubectl logs -n namespace container-name --tail=1000
kubectl logs --selector=run=hello-world --tail 1
```
### to get the pod logs for particular directory
```
kubectl -n elastic-stack exec -it app cat /log/app.log
kubectl logs myapp-pod -c init-myservice # Inspect the first init container
kubectl logs myapp-pod -c init-mydb      # Inspect the second init container
```
