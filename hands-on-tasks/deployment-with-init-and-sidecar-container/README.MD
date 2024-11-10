### In this simple example you will learn how to create a deployment with init and sidecar container

### What is init conatiner?
 An init container in Kubernetes is a special type of container that runs before the main containers in a pod. Init containers are used to perform initialization tasks that need to happen before the main application containers start. init containers are ephemiral in nature after the work is completed container shuts down

### What is sidecar container?
 A sidecar container is a secondary container that runs along side  with the main application container in the same pod in Kubernetes cluster. Sidecar containers are typically used to provide supporting functionality to the main application, such as logging, monitoring, networking, or proxying, without altering the main container's functionality. 

### Example:

Here is a simple yaml file which craetes a deployment with side car and init container and a main application container (runnig simple nginx web server) ,init container will sleep for 5 seconds before the main container starts and sidecar container will log date after every 10 seconds

```yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      initContainers:
        - name: init-container
          image: busybox
          command: ["sh", "-c", " sleep 5"]
          volumeMounts:
            - name: shared-data
              mountPath: /mnt/data
      containers:
        - name: app-container
          image: nginx
          ports:
            - containerPort: 80
          volumeMounts:
            - name: shared-data
              mountPath: /usr/share/nginx/html
        - name: sidecar-container
          image: busybox
          command: ["sh", "-c", "while true; do date; sleep 10; done"]
          volumeMounts:
            - name: shared-data
              mountPath: /mnt/data
      volumes:
        - name: shared-data
          emptyDir: {}
  ```
To simulate this deployment,run:
 ```bash
  kubectl apply -f deployment.yaml
  ```

### Conclusion
 The uasge of sidecar and init containers in your deployment can be usefull in many use cases ,both will provide extraa functionality without affecting the main application container           