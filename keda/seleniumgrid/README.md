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
- An active Amazon AWS account along with the AWS EKS cluster.
---
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
![image](https://github.com/anveshmuppeda/kubernetes/assets/115966808/e08b57df-1e07-479d-967c-746dccee7af0)

As you can see our hub is listening on http://192.168.38.237:4444  
To get ip of service run the below command: 
```
k describe svc <svc-name>-n selenium in our case it would be
k describe svc selenium-hub-svc -n selenium
```
To test whether our hub is ready to register for new node, run the below commands by login to the pod and curl within the pod.
```
winpty kubectl exec -it <selenium-hub-pod> -n selenium //bin//sh 
curl http://192.168.38.237:4444 /wd/hub/status
```

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
Here Some points about the scaledobject definition:
1. **namespace** should be the namespace that your selenium browser pods exist in.
2. **deploymentName** are the name of your browser deployment.
3. **name** (within spec) is also the name of your browser deployment
4. **url** is the url of your selenium grid.
5. **browserName** is the name of the browser you are using.  
6. **minReplicaCount** and **maxReplicaCount** are the min and maximum pod count you want to have.
7. **triggers** This specification describes the selenium-grid trigger that scales browser nodes based on number of requests in session queue and the max sessions per grid.

More details about KEDA selenium grid scaler can be found [here](https://keda.sh/docs/2.8/scalers/selenium-grid-scaler/).

To see whether scaled objects are deployed or not. Run the command
```
kubect get so -n selenium
```

## Results  
### Deployments 
![image](https://github.com/anveshmuppeda/kubernetes/assets/115966808/fb5d46e9-6617-4fc5-a1ef-050fe106308e)
### Services 
![image](https://github.com/anveshmuppeda/kubernetes/assets/115966808/ba9416e1-3edf-4ca4-a7bf-855d1add2a2f)
### All pods
![image](https://github.com/anveshmuppeda/kubernetes/assets/115966808/001c0452-c3a5-4426-8872-7a5fd3fe16d5)
### Scaled Objects
![image](https://github.com/anveshmuppeda/kubernetes/assets/115966808/2c74f3f1-457d-41e5-a858-da8736ecf109)
### Selenium Grid(Before increasing queue size)
![image](https://github.com/anveshmuppeda/kubernetes/assets/115966808/ed51bf31-24a8-44ca-8f99-17704a1c4c51)
### Selenium Grid(After increasing queue size)
![image](https://github.com/anveshmuppeda/kubernetes/assets/115966808/8e05da6e-6ef6-4930-b41f-4bdc58487cad)
### Pods(After increasing the queue size)
![image](https://github.com/anveshmuppeda/kubernetes/assets/115966808/58f7a2ef-557d-4598-9667-aca448f29a7d)
