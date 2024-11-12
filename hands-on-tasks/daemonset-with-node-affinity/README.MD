### OBJECTIVE
 #  Deploy a DaemonSet that runs a monitoring agent (e.g., Fluentd) on     specific nodes based on node labels. Configure resource limits to control CPU and memory usage.

### What is a daemonset?


## In this example you have to use a cluster with at least two nodes that are not acting as control plane hosts

   # To determine the nodes run
```bash
kubectl get nodes
```

# After determinig the nodes , Add labels to nodes
  ```bash
  kubectl label nodes <node-name> <label-key>=<label-value>
  ```
# To know your labels has been set to your node run :
  ```bash
  kubectl get nodes --show-labels
  ```
# Once you set the label to the nodes create a daemon set and add labels (which you set in your node) in the nodeselector: field in daemonset spec section 
# This yaml file will create a daemonset with a monitoring agent fluentd to run on the nodes which have label agent:monitor and have a resource quota limit    
  
  ```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: my-daemonset
  namespace: default
spec:
  selector:
    matchLabels:
      app: my-daemon
  template:
    metadata:
      labels:
        app: my-daemon
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: agent
                operator: In
                values:
                - monitor
      containers:
      - name: monitoring-container
        image: fluentd
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```
## To implement this run:
 ```bash
   kubectl apply -f daemonset.yaml
   ```
## To check your pod is running on the nodes which have label agent:monitor run:
```bash
kubectl get pods -o wide
```
## The output shows you that your pod is running on the node with have label agent:monitor    

### Conclusion
 ## If you want to run monitoring agent on each node along side with your application container then daemonset is the best choice and if you set node affinity your monitoring agent will run only on those nodes which you have defined and set resource quota for containers how much cpu and memorey they have to use to complete their job