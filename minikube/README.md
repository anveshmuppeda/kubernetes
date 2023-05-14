# Mac. 
Follow https://minikube.sigs.k8s.io/docs/start/. 

## Drivers. 
Follow https://minikube.sigs.k8s.io/docs/drivers/.  
Here I used qemu as a driver.  
```brew install qemu```  

### Start your cluster using below command. 
```minikube start```.  

### Check the status of the minikube   
```minikube status```  

### To stop the minikube cluster   
```minikube stop```  

### For top command
```
minikube addons enable metrics-server
```
Ref: https://stackoverflow.com/questions/52694238/kubectl-top-node-error-metrics-not-available-yet-using-metrics-server-as-he

## Connecting to the EKS cluster: 
```
aws sts get-caller-identity
aws eks --region us-east-2 update-kubeconfig --name anvesh-eks-cluster
```
Refe: https://repost.aws/knowledge-center/eks-cluster-connection
