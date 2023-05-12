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

Now the kubernetes cluster is ready, let us deploy the Zalenium grid with the below series of commands.

Create a namespace 'zalenium'
```
kubectl create namespace zalenium
```

Add the zalenium repository from git onto cluster.
```
helm repo add zalenium-github https://raw.githubusercontent.com/zalando/zalenium/master/charts/zalenium
```
> **_NOTE:_** "zalenium-github" - repo name (can be changed as needed)

Search and confirm if the repo is created.
```
helm search repo zalenium
```
Install zalenium onto kubernetes cluster with the given configuration.
```
helm install my-grid --namespace zalenium zalenium-github/zalenium --set hub.serviceType="LoadBalancer" --set hub.basicAuth.enabled="true" --set hub.basicAuth.username="seluser" --set hub.basicAuth.password="Selpwd" kubectl get service my-grid-zalenium --namespace="zalenium"
```
> **_NOTE:_** "my-grid" - Helm's release name (can be changed as needed)

Verify if the service is created and up
```
kubectl get service my-grid-zalenium --namespace="zalenium"
```

That's it! Zalenium Grid is up & accessible over the given external ip.

Validate the below URLs are accessible & then start the execution.
(Provide the credentials when prompted for)

Zalenium Dashboard for test recordings: http://<ExternalIP>/dashboard

Live Preview of Test Executions: http://<ExternalIP>/grid/admin/live

Grid Console: http://<ExternalIP>/grid/console

Grid Url, authenticated with basic auth: http://seluser:Selpwd@<ExternalIP>/wd/hub

---
> **_NOTE:_**
Cluster & nodes created from eksctl can be deleted similarly with a single command 
```eksctl delete cluster --name sel-cluster```
---
