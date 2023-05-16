# Scaling a Kubernetes Selenium Grid with KEDA 
### The Issue
If you have any experience with Selenium Grid and Kubernetes you will probably run into an issue with **scaling**. Kubernetes (K8S) works wonders for scaling up and down applications based on their CPU and Memory usage, but it is not so straightforward when it comes down to applications like Selenium Grid.  
  
The Horizontal Pod AutoScaler (**HPA**) that is built into Kubernetes checks (by default) for resource consumption to determine if a deployment needs to be scaled up or down. This becomes an issue for Selenium Grid for a couple reasons:
 1. The browser pods use a variable amount of resources depending on the demand of the current test. This means that all your browser pods may be in use but there isn’t enough CPU usage for the HPA to decide that a scale-up is needed, **leaving tests waiting in the queue unnecessarily**.
 2. When Kubernetes decides to **scale down a deployment** it does so (for the most part) at **random**. You could have 10 tests running on 20 pods and need to scale down. More than likely at least one of the pods asked to terminate will still have a test running, resulting in connection failures
