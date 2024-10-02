# Welcome to Kubectl cheatsheet [![GitHub](https://img.shields.io/github/license/anveshmuppeda/kubernetes?color=blue)](https://github.com/anveshmuppeda/kubernetes/blob/main/LICENSE)  

<p align="center">  
By Anvesh Muppeda & Sai Manasa Kota  
</p>   

🚀 Kubectl Helper: Your Ultimate Kubernetes Command Companion! 🌐  

Master the art of Kubernetes with our feature-packed Kubectl Cheatsheet! This comprehensive guide empowers beginners and seasoned professionals to navigate the Kubernetes landscape effortlessly. We've got you covered from cluster management and context switching to intricate pod manipulations. Say goodbye to command memorization and hello to streamlined operations!  

<a name="tableofcontents"></a>  

## Table of Contents   
1. [ Cluster ⎈ ](#Cluster)
2. [ Switching Between Contexts ⇢ ](#SwitchingBetweenContexts)
3. [ Rollout 🔄 ](#rollouts)
4. [ Labels 🏷️ ](#Labels )
5. [ Pod 🛡️ ](#Pod)
6. [ Nodes 💻 ](#Nodes) 
7. [ Troubleshooting With Logs 📊 ](#logs) 
8. [ Secrets Encode & Decode 🕵️ ](#certs) 
9. [ Taints & Tolerations 🔭 ](#taint) 
10. [ Patch 🛠️ ](#patch) 
11. [ Set ⚙️ ](#set_command) 
12. [ Port Forward ↔️ ](#portforward)  
13. [ Create Resources 🏗️ ](#create)
14. [ Delete Resources 🚮 ](#delete)
15. [ Contact Information 📧 ](#contact)
16. [ Feedback Welcome 🌟 ](#feedback)

---
<a name="Cluster"></a>  

## 1. Cluster  

### a. Listing all the resources in cluster
  ```sh
  kubectl api-resources
  ```  

### b. Listing all the api versions in cluster
  ```sh
  kubectl api-versions
  ```  

### c. Get the configurations of saved clusters  
  ```sh
  kubectl config view
  ```

### d. Get the Kubernetes version running on the client and server  
  ```sh
  kubectl version
  ```

### e. Get everything from the cluster  
  ```sh
  kubectl get all --all-namespaces
  ```  
### f. to Check Access   
```sh
kubectl auth can-i create deployments
kubectl auth can-i create pods
```  
### g. to check IP range for pods within the namespaces
```sh
kubectl cluster-info dump | grep -m 1 cluster-cidr
```  

---   
<p align="center">
  <a href="#tableofcontents">Go to Top ▲</a>
</p>

<a name="SwitchingBetweenContexts"></a>  

## 2. Switching between contexts  

### a. Get all preconfigured contexts and see which one is active:  
  ```sh
  kubectl config get-contexts
  ```  

### b. Get the current config name
  ```sh
  kubectl config current-context
  ```  

### c. Get the current config with more details
  ```sh
  kubectl config view --minify
  ```  

### d. Switch between the predefined contexts(Switch to a context/cluster)  
  ```sh
  kubectl config use-context <context-name>
  ```  

### e. Setting default namespace 
  The default namespace **default** is configured in your cluster's context. To change the default namespace, use the below command. Specify the desired namespace name that you want to set as the default.  
  ```sh
  kubectl config set-context --current --namespace=<NAMESPACE-NAME>
  ```  
  For example, to set the namespace kube-system as your default, you would run the following command  
  ```sh
  kubectl config set-context --current --namespace=kube-system
  ```  
---  
<p align="center">
  <a href="#tableofcontents">Go to Top ▲</a>
</p> 
<a name="rollouts"></a>  

## 3. Rollout  
The `kubectl rollout` command is primarily used with Kubernetes **Deployments**, **Statefulsets** and **DaemonSets**.  

### a. kubectl rollout syntax  
  ```sh 
  kubectl rollout <COMMAND> 
  ```  
  **COMMAND** can be one of the following:  
  1. status  
  2. history  
  3. restart  
  4. pause  
  5. resume  
  6. undo  

### b. To check the rollout status  
 ```sh
  kubectl rollout status <resource-type>/<resource-name>
  ```  

### c. To get the rollout history  
  ```sh
  kubectl rollout status <resource-type>/<resource-name>
  ```  

### d. To restart the deployment  
  ```sh 
  kubectl restart status <resource-type>/<resource-name> 
  ```  
  
### e. To pause the deployment updates  
  ```sh 
  kubectl rollout pause <resource-type>/<resource-name>
  ```  

### f. To resume the deployment updates  
  ```sh
  kubectl rollout resume <resource-type>/<resource-name>
  ```  

### g. To undo the deployment updates to previous revision  
  ```sh
  kubectl rollout undo <resource-type>/<resource-name>
  ```   
  > [!TIP]  
  > Here you can use **Deployments**, **Statefulsets** and **DaemonSets** in place of <resource-type>.

---
<p align="center">
  <a href="#tableofcontents">Go to Top ▲</a>
</p>  
<a name="Labels"></a>  

## 4. Labels  

### a. Adding a label to a specific resource  
  ```bash
  kubectl label <resource-type> <resource-name> <label-key>=<label-value>
  ```
### b. Removing a label to a specific resource
  ```bash
  kubectl label <resource-type> <resource-name> <label-key>-
  ```
### c. List all the labels from a resource  
  ```bash
  kubectl get <resource-type> <resource-name> --show-labels 
  ```  
### d. Overwrite the resource label  
  ```bash
  kubectl label --overwrite <resource-type> <resource-name> <label-key>=<label-new-value>  
  ```  

---  
<p align="center">
  <a href="#tableofcontents">Go to Top ▲</a>
</p>  
<a name="Pod"></a>

## 5. Pod  
### a. To list the pods in specific namespace  
  ```bash 
  kubectl get pods -n <namespace> 
  ```  
### b. To list all pods in all namespaces  
  ```bash  
  kubectl get pods -A
  ```  
### c. Exec into a pod  
##### bash 
  ```bash 
  kubectl -n <namespace> exec -it <pod-name> //bin//bash
  ```  
##### sh  
  ```sh 
  kubectl -n <namespace> exec -it <pod-name> //bin//sh
  ```  
#### In windows   
##### bash 
  ```bash
  winpty kubectl -n <namespace> exec -it <pod-name> //bin//bash
  ```  
##### sh  
  ```sh
  winpty kubectl -n <namespace> exec -it <pod-name> //bin//sh
  ```  
### d. Watch a pod status 
  ```sh
  kubectl -n <namespace> get <pods/deployments>  -w
  kubectl -n <namespace> get <pods/deployments> --watch
  ```  
### e. Print env variables of a pod
  ```bash
  kubectl -n <namespace> exec <pod-name> -- printenv
  ```

### f. To make a curl to a pod  
##### sh
  ```sh 
  kubectl -n <namespace> exec -it <pod-name> -- /bin/sh -c "curl http://example.com"
  ``` 
##### bash  
  ```bash 
  kubectl -n <namespace> exec -it <pod-name> -- /bin/bash -c "curl http://example.com"
  ```

### g. Delete all pods which are evicted with namespace wise  
  ```bash
  kubectl get pod -n <namespace> | grep Evicted | awk '{print $1}' | xargs kubectl delete pod -n <namespace>
  ```
### h. To get the pod definition in YAML format  
  ```bash
  kubectl -n <namespace> get pod pod-name -o yaml > pod.yaml
  ```
### i. To get pod definition possible options  
  ```bash
  kubectl explain pods --recursive | less
  ``` 
### j. Get the pod deatils with wide options
  ```bash
  kubectl get pods -o wide
  ```  
### k. View detailed information about a pod  
  ```bash 
  kubectl -n <namespace> describe pod <podname>
  ```  
### l. Create or apply a pod configuration  
  ```bash 
  kubectl -n <namespace> apply -f <pod-definition.yaml>
  ```  
### m. Delete a pod  
#### Delete a specific pod  
  ```bash 
  kubectl -n <namespace> delete pod <pod-name>
  ``` 
#### Delete all pods  
  ```bash
  kubectl -n <namespace> delete pods --all
  ```  
### n. Execute a command in a running pod  
  ```bash
  kubectl exec -it <pod-name> -- <command> 
  ```
### o. Copy files to/from a pod  
#### Copy a file from your local machine to a pod  
  ```bash
  kubectl -n <namespace> cp <local-file> <pod-name>:<destination-path>
  ```  
#### Copy a file from a pod to your local machine  
  ```bash 
  kubectl -n <namespace> cp <pod-name>:<source-path> <local-destination>
  ```  
### p. Get pod events  
  ```bash  
  kubectl get events 
  ```  
### q. Get resource usage  
  ```bash 
  kubectl -n <namespace> top pod
  ```  
---
<p align="center">
  <a href="#tableofcontents">Go to Top ▲</a>
</p>  

<a name="Nodes"></a>

## 6. Nodes 
### a. List nodes  
  ```bash
  kubectl get pods 
  ```  
### b. List nodes with the resource usage
  ```bash
  kubectl top node
  ```  
### c. Get node details  
  ```bash
  kubectl describe node <nodename>
  ```  
### d. Cordon a node  
  Mark a node as unschedulable, preventing new pods from being scheduled. 
  ```bash 
  kubectl cordon node <nodename> 
  ```
### e. Uncordon a node  
  Mark a node as schedulable, allowing new pods to be scheduled.  
  ```bash
  kubectl uncordon node <nodename>
  ```  
### f. Drain Nodes  
  Evict pods from a node, moving them to other nodes. The `--ignore-daemonsets` flag is used to ignore DaemonSet managed pods.  
  ```bash 
  kubectl drain <nodename> --ignore-daemonsets
  ```  
### g. Get the kubelet version for a specific node.  
  ```bash
  kubectl get node <nodename> -o jsonpath='{.status.nodeInfo.kubeletVersion}
  ``` 

---
<p align="center">
  <a href="#tableofcontents">Go to Top ▲</a>
</p>   

<a name="logs"></a> 

## 7. Streaming With Logs 
### a. Get logs from a pod 
  ```bash
  kubectl -n <namespace> logs <podname>
  ```  
### b. Stream Logs in Real-time  
  ```bash 
  kubectl -n <namespace> -f logs <podname> 
  ``` 
### c. Specify Container in Multi-container Pods
  ```bash 
  kubectl -n <namespace> logs <podname> -c <containerName>  
  ``` 
### d. Retrieve Previous Container Logs  
  ```bash 
  kubectl -n <namespace> logs --previous <pod-name>
  ``` 
### e. Tail the Logs with a Specific Number of Lines  
  ```bash
  kubectl logs <pod-name> --tail=<lines>
  ```  
### f. Filter the logs based on a time window  
  ```bash
  kubectl logs --since=<time-period> <pod-name>
  ```  
  > [!TIP]  
  > Here you can mention **10s**, **10m**, **10h**, and **10d** in place of <time-period>(Just an exmaple).  

### g. Add timestamps in the Logs  
  ```bash 
  kubectl -n <namespace> logs <pod-name> --timestamps  
  ```  
### h. Deployment, Statefulset, Daemonset, and Job logs 
  ```bash
  kubectl -n <namespace> logs <resource-type>/<resource-name> 
  ``` 
  > [!TIP]  
  > Here you can use **Deployments**, **Statefulsets**, **DaemonSets**, and **Jobs** in place of <resource-type>. 
---

<p align="center">
  <a href="#tableofcontents">Go to Top ▲</a>
</p>  


<a name="certs"></a>

## 8. certs  
### a. Encode your secret  
  ```bash
  echo -n 'your-secret' | base64
  ```  
### b. Decode your secret  
  ```bash
  echo -n 'your-string' | base64 --decode
  ```  
--- 

<p align="center">
  <a href="#tableofcontents">Go to Top ▲</a>
</p>  
<a name="taint"></a> 

## 9. Taints & Tolerations  
### a. View Taints on a Node  
  ```bash
  kubectl describe node <node-name> | grep Taints
  ``` 
### b. Add a Taint to a node  
  ```bash 
  kubectl taint nodes <nodename> <key>=<value>:<effect>  
  ``` 
  > [!TIP]  
  > Here you can use **NoSchedule**, **NoExecute**, and **NoSchedule** in place of <effect>.  

### c. Remove a Taint from a Node 
  ```bash
  kubectl taint nodes <nodename> <key>-
  ```  
### d. Adding tolerations to a pod YAML  
  Add the following section to your pod YAML  
  ```yaml
  tolerations:
  - key: "<key>"
    operator: "Equal"
    value: "<value>"
    effect: "<effect>"
  ```  
### e. Get Toleration in a Running Pod  
  ```bash
  kubectl get pod <pod-name> -o=jsonpath='{.spec.tolerations}'
  ```  
---
<p align="center">
  <a href="#tableofcontents">Go to Top ▲</a>
</p>  
<a name="patch"></a>  

## 10 Patch  
### a. Patch using a file  
  ```bash
  kubectl patch <resource <resource-name> --patch-file patch-file.yaml  
  ```  
#### patch file looks like:  
  ```yaml
  spec:
    template:
      spec:
        containers:
        - name: patch-demo-ctr-3
          image: gcr.io/google-samples/node-hello:1.0
  ```  

### c. Patch using a string
  ```bash
  kubectl patch <resource> <resource-name> -p '<pathcing-string>'
  ```  
#### Example  
  ```bash
  kubectl patch deployment sampledeploy -p '{"spec": {"replicas": 2}}'
  ``` 
---

<p align="center">
  <a href="#tableofcontents">Go to Top ▲</a>
</p>  
<a name="set_command"></a> 

## 11. Set Command  
### a. Set a resource with specific option   
  ```bash
  kubectl set <resource-type> <resource-name> [options]
  ``` 
#### Example  
  ```bash 
  kubectl set deployment sampledeploy --replicas=3  
  ```
---

<p align="center">
  <a href="#tableofcontents">Go to Top ▲</a>
</p>  
<a name="portforward"></a> 

## 12. Port Forward  
  kubectl port-forward forwards connections to a local port to a port on a pod. Compared to kubectl proxy, kubectl port-forward is more generic as it can forward TCP traffic while kubectl proxy can only forward HTTP traffic.  
kubectl port-forward is useful for testing/debugging purposes so you can access your service locally without exposing it.   

### a. Syntax 
```bash
kubectl port-forward -n <namespace> <resource-type>/<resource-name> <localhost-port>:<pod-port>
``` 
#### Example
```bash 
kubectl port-forward -n default deploy/sampledeploy 8080:80
```  
Once the connection is succesfull from local port to target resource port, then we can test local connection using curl to the end point or we can access the end point using `localhost:8080`

#### Testing
```bash
curl -X GET -s http://localhost:80/
curl -X GET -s http://localhost:80/_cluster/health  
```
---  
<p align="center">
  <a href="#tableofcontents">Go to Top ▲</a>
</p>   
<a name="create"></a> 

## 13. Create a Resource  
### a. Create a resource in imperative way.  
```bash 
kubectl create <resource-type> <resource-name> --PARAMETER1=VALUE1
```  
#### Example 
```bash
kubectl create deployment sampledeploy --image=sampleimage
```  
#### For Pod  
```bash 
kubectl run samplepod --image=sampleimage
```  
### b. Create a resource in declarative way  
```bash
kubectl create -f manifest-file.yaml 
```  
### c. Create/update resource  
```bash 
kubectl apply -f manifest-file.yaml
```  
### d. Create resources from all manifest files in a directory  
```bash
kubectl create -f ./directory
```  
### e. Create resources from a link  
```bash
kubectl create -f 'URL'
```  
### f. Edit and update the resources  
```bash
kubectl edit <resource-type> <resource-name>
```
---  
<p align="center">
  <a href="#tableofcontents">Go to Top ▲</a>
</p>   
<a name="delete"></a>  

## 14. Delete a Resource 
### a. Delete a resource by name  
```bash
kubectl -n <namespace> delete <resource-type> <resource-name>
```  
### b. Delete a resource using a manifest file  
```bash 
kubectl delete -f manifest-file.yaml
```  
### d. Deleting resources with a label selector 
```bash
kubectl delete <resource-type> --selector=<key>=<value>
kubectl delete <resource-type> --selector=<key>
```  
> [!CAUTION]
> PLEASE DOUBLE CHECK BEFORE RUNNING THESE COMMANDS!!
### e. Deleting all resources in current namespace  
```bash 
kubectl delete all --all
```  
### f. Deleting all resources in specific namespace  
```bash 
kubectl -n <namespace> delete all --all
```  
### g. Deleting all resources matching a label selector 
```bash 
kubectl delete all --selector=<key>=<value>
kubectl delete all --selector=<key>
```
--- 

<p align="center">
  <a href="#tableofcontents">Go to Top ▲</a>
</p>  

<a name="blogs"></a>    


## Contact Information  
If you have any questions or feedback, feel free to reach out:  

- Email: muppedaanvesh@gmail.com 📧  
- LinkedIn: [@Anvesh](https://www.linkedin.com/in/anvesh-muppeda-5a0a83167) & [@Manasa](https://www.linkedin.com/in/sai-manasa-51882b156) 🌐  
- GitHub Issues: [Project Issues](https://github.com/anveshmuppeda/kubernetes/issues) 🚀 

--- 
<p align="center">
  <a href="#tableofcontents">Go to Top ▲</a>
</p>  
<a name="feedback"></a>   

## Feedback Welcome!  

We welcome your feedback and suggestions! If you encounter any issues or have ideas for improvements, please open an issue on our [GitHub repository](https://github.com/anveshmuppeda/kubernetes/issues). 🚀   

---
