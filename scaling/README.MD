# Auto Scaling in Kubernetes  

## Metric Server Setup  
Before testing Horizontal Pod Autoscaler (HPA) and Vertical Pod Autoscaler (VPA), it's essential to have the Metrics Server installed in your Kubernetes cluster. The Metrics Server collects resource usage metrics from the cluster's nodes and pods, which are necessary for autoscaling decisions.
You can install the Metrics Server using either a YAML manifest or the official Helm chart.   
To install the latest release of the Metrics Server from the YAML manifest, follow these steps:  
Download the Components Manifest: Use kubectl apply to download and apply the Components manifest directly from the latest release of the Metrics Server:  
```bash
$ kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml  
```  

This command fetches the YAML manifest for the latest release of the Metrics Server from its GitHub repository and applies it to your Kubernetes cluster.  

2. Verify Installation: After applying the manifest, verify that the Metrics Server pods are running successfully. You can check the pods in the kube-system namespace:  
```bash
kubectl get pods -n kube-system | grep metrics-server
```  
You should see pods related to the Metrics Server running and ready.  

3. Confirm Metrics Collection: Once the Metrics Server is up and running, you can confirm that it's collecting metrics by querying the API. For example, you can retrieve the CPU and memory usage metrics for nodes and pods:  
```bash
$ kubectl top nodes kubectl top pods --all-namespaces
```  
If the Metrics Server is properly installed and functioning, you should see CPU and memory usage metrics for nodes and pods in your cluster.  
