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
  
Create a `cluster.yaml` file with the below instructions and execute the given command.
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
