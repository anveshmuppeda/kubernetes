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
---
### Now the kubernetes cluster is ready, let us deploy the Selenium grid with the below series of commands.

> **_NOTE:_**  I will be deploying all the resources in selenium namespace. 
> And all the deployments are present under [deploy](https://github.com/anveshmuppeda/kubernetes/tree/main/keda/seleniumgrid/deployments) directory in this same location.   

Create a namespace 'selenium'
```
kubectl create namespace selenium
```

## Selenium Hub 

First of all we will we creating the deployment file for selenium hub and creating a service for the same.  
To apply the changes run the below command.  
```
kubectl apply -f selenium-hub-deploy.yaml -n selenium
kubectl apply -f https://raw.githubusercontent.com/anveshmuppeda/kubernetes/d5bd70c183010e222eda6590da76f6948a12a36f/keda/seleniumgrid/deployments/selenium-hub-deploy.yaml -n selenium
```
```
kubectl apply -f selenium-hub-service.yaml -n selenium
kubectl apply -f https://raw.githubusercontent.com/anveshmuppeda/kubernetes/d5bd70c183010e222eda6590da76f6948a12a36f/keda/seleniumgrid/deployments/selenium-hub-service.yaml -n selenium
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

---
## Browser Nodes
### Let’s create the chrome node first.

To deploy the Chrome node, run the below command
```
kubectl apply -f selenium-node-chrome -n selenium
kubectl apply -f https://raw.githubusercontent.com/anveshmuppeda/kubernetes/d5bd70c183010e222eda6590da76f6948a12a36f/keda/seleniumgrid/deployments/chrome-deploy.yaml -n selenium
```
To see the deployed resource run the below command
```
kubectl get deployment selenium-node-chrome -n selenium
```
### Let’s create the firefox node.

To deploy the Firefox node, run the below command
```
kubectl apply -f firefox-deploy.yml -n selenium  
kubectl apply -f https://raw.githubusercontent.com/anveshmuppeda/kubernetes/d5bd70c183010e222eda6590da76f6948a12a36f/keda/seleniumgrid/deployments/firefox-deploy.yaml -n selenium
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
kubectl apply -f https://raw.githubusercontent.com/anveshmuppeda/kubernetes/d5bd70c183010e222eda6590da76f6948a12a36f/keda/seleniumgrid/deployments/chorme-scaledObject.yaml -n selenium
```   
To deploy the Forefox ScaledObject Deployment file run the below command:
```
kubectl apply -f firefox-scaledObject.yml -n selenium
kubectl apply -f https://raw.githubusercontent.com/anveshmuppeda/kubernetes/d5bd70c183010e222eda6590da76f6948a12a36f/keda/seleniumgrid/deployments/firefox-scaledObject.yaml -n selenium
```   
To see whether scaled objects are deployed or not. Run the command
```
kubect get so -n selenium
```
