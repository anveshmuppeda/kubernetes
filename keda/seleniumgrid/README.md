# How to Deploy Selenium grid on AWS / Amazon EKS 
  Selenium Grid is good for parallel execution but maintenance is a nightmare in an era where you see a frequent upgrades to browsers and corresponding drivers. No sooner the usage of automation framework / selenium grid increases, scalability and maintenance becomes a challenge. To address such issues, we do have solutions based on dockers, docker swarm etc. Having said that, there are some caveats in scaling, managing container health etc.

Below solution would try to address most of them. Major chunks of the solution include **Selenium, Zalenium, Docker, Kubernetes and Amazon EKS**.

This article would outline the process of deploying **Selenium grid(Zalenium) on AWS (Amazon EKS) using Kubernetes and Helm**.

### What do we achieve with this setup..?
- Scalability: EKS can scale the nodes and pods as per the given configuration.
- Visibility: Zalenium provides a feature to view the live executions on the containers.
- Availability: Amazon EKS cluster makes selenium grid available all the time.
- Maintenance: Low maintenance as the containers are destroyed after each execution.
### Pre-requisites:
- An active Amazon AWS account.
- IAM user is created in AWS account
- AWS CLI is connected to AWS account providing the user credentials using local powershell or any terminal  
                                                            OR
- Use AWS cloudshell which is automatically connected to logged in account.
- Install AWS CLI (for local terminal), kubectl, helm in the given order.

### Lets Get Started!
Once the above pre-requisites are met, next task to deploy any application on kubernetes is **to create a kubernetes cluster**. There are different ways to create a cluster on AWS, I'll brief couple of ways to achieve the same.

### First, Create cluster from AWS GUI.

1. Create master node or cluster 
  - Open Amazon EKS console
  - Choose Create Cluster
  - Provide details like cluster name, k8s version, role
  - Select VPC, security groups, endpoint access
  - Further steps as shown on GUI which will make 'master' ready.
2. Create worker nodes and connect to the above created cluster.
- Create Node Group (Amazon EC2) instances.
- Choose the cluster, to which the above node group should get attached.
- Select security group, resources etc.,
- Define min and max number no. of nodes.

### Second, Create cluster using eksctl (The official CLI for Amazon EKS)
1. Install eksctl using brew, chocolatey, scoop or curl.
2. Run the below command to create cluster.

```eksctl create cluster --name sel --region ap-south-1 --nodegroup-name selnodegrp-1 --node-type t2.micro --nodes 2```  
 OR  
Create a cluster.yaml file with the below instructions and execute the given command.
```
apiVersion: eksctl.io/vlaplha5
kind: ClusterConfig
metadata:
  name: sel-cluster
  region: ap-south-east-1
nodeGroups:
  - name: senodegrp-1
    instanceType: t2.medium
    desiredCapacity: 2
```
```eksctl create cluster -f cluster.yaml```


> **_NOTE:_**  It takes around 5-10min to complete the whole task of creating a cluster (master) and EC2 instances (worker) nodes and attach nodes to the master.

  
### Now the kubernetes cluster is ready, let us deploy the Selenium grid with the below series of commands.

> **_NOTE:_**  I will be deploying all the resources in selenium namespace.   

Create a namespace 'selenium'
```
kubectl create namespace selenium
```

## Selenium Hub 

First of all we will we creating the deployment file for selenium hub and creating a service for the same.  
To apply the changes run the below command.  
```
kubectl apply -f hub.yml -n selenium
```  
As a results of this one deployment and service will get created in selenium namespace. To check service run below command:  
```
kubectl get svc -n selenium
```  
To get a deployment run below command   
```
kubectl get deploy -n selenium
```
Now to see the created pod run below command  
```
kubectl get pods -n selenium
```  
To test whether our service and deployment are deployed correctly let’s try to log the pod. Run the below command
```
kubectl logs <hub-podname> -n selenium
```  
As you can see our hub is listening on http://192.168.194.81:4444  
To get ip of service run the below command: 
```
k describe svc <svc-name>-n selenium in our case it would be
k describe svc selenium-hub-svc -n selenium
```
To test whether our hub is ready to register for new node, run the below command by attaching the session to selenium hub pod.
```
kubectl exec -it selenium-hub-b4bb44946-xthvr -n selenium — curl http://192.168.194.81:4444/wd/hub/status
```

If we get the above output then our HUB is deployed successfully.

## Browser Nodes
### Let’s create the chrome node first.

To deploy the Chrome node, run the below command
```
kubectl apply -f chrome-deploy.yml -n selenium
```
To see the deployed resource run the below command
```
kubectl get deployment selenium-node-chrome -n selenium
```
### Let’s create the firefox node.

To deploy the Firefox node, run the below command
```
kubectl apply -f firefox-deploy.yml -n selenium
```
To see the deployed resource run the below command
```
kubectl get deployment selenium-node-firefox -n selenium
```
### Let’s install the Selenium Grid Scaler in our cluster:  
```
kubectl apply -f https://github.com/kedacore/keda/releases/download/v2.8.0/keda-2.8.0.yaml
```
Now let’s create our browser scale deployment files for Chrome and Firefox: 
To deploy the Chrome ScaledObject Deployment file run the below command:
```
kubectl apply -f chrome-scaledObject.yml -n selenium
```   
To deploy the Forefox ScaledObject Deployment file run the below command:
```
kubectl apply -f firefox-scaledObject.yml -n selenium
```   
To see whether scaled objects are deployed or not. Run the command
``
kubect get so -n selenium
```
