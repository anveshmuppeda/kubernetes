# nginx  

```minikube service <SERVICE_NAME> --url```  
this command which will give you a url where you can access the service. In order to open the exposed service, the  
```
minikube service <SERVICE_NAME>
```  
command can be used:  

```
$ kubectl run hello-minikube --image=gcr.io/google_containers/echoserver:1.4 --port=8080  
deployment "hello-minikube" created  
$ kubectl expose deployment hello-minikube --type=NodePort  
service "hello-minikube" exposed  
$ kubectl get svc  
NAME             CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE  
hello-minikube   10.0.0.102   <nodes>       8080/TCP   7s  
kubernetes       10.0.0.1     <none>        443/TCP    13m  

$ minikube service hello-minikube  
Opening kubernetes service default/hello-minikube in default browser...  
```  

This command will open the specified service in your default browser.   

There is also a --url option for printing the url of the service which is what gets opened in the browser:  

```$ minikube service hello-minikube --url
http://192.168.99.100:31167```   

## or  

As minikube is exposing access via nodeIP:nodePort and not on localhost:nodePort, you can get this working by using kubectl's port forwarding capability. For example, if you are running mongodb service:  

```kubectl port-forward svc/mongo 27017:27017```  

This would expose the service on localhost:27017, FWIW. Furthermore, you might want to figure out how to run this in background.  


