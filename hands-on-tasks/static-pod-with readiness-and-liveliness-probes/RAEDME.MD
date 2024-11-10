### What is a static pod ?
A static pod is a type of Kubernetes pod that is not managed by the Kubernetes control plane ,static pod is managed by kubelet  

### How to define static pods?
A static pod is defined using a YAML or JSON manifest file, which typically resides in a directory : /etc/kubernetes/manifests on the node. This file contains the configuration for the pod

### Here is an example of configuring a  static pod with readiness and liveliness probes
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: static-pod
  labels:
    app: static-pod-demo
spec:
  containers:
  - name: my-container
    image: nginx
    ports:
      - containerPort: 80
    livenessProbe:
      httpGet:
        path: /healthz
        port: 80
        scheme: HTTP
      initialDelaySeconds: 5
      periodSeconds: 10
      timeoutSeconds: 2
      failureThreshold: 3
    readinessProbe:
      httpGet:
        path: /readiness
        port: 80
        scheme: HTTP
      initialDelaySeconds: 5
      periodSeconds: 10
      timeoutSeconds: 2
      failureThreshold: 3
```

 This file would be placed in /etc/kubernetes/manifests/static-pod.yaml on the node where you want the static pod to run.
  
### Conclusion
   Static pods are often used for the essential system components that must always run, such as the kube-apiserver, etcd, and other internal services in a Kubernetes cluster. 
