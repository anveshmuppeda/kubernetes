# Readiness Probes  

### 1. What is a Readiness Probe?

In Kubernetes, a **readiness probe** is a mechanism to determine if a container is **ready** to accept traffic. If the readiness probe fails, Kubernetes will temporarily stop sending traffic to the container until it is considered "ready" again. This is crucial for preventing requests from being routed to a container that is not yet fully initialized or is currently in an unhealthy state.

**Key Difference from Liveness Probe**:
- **Liveness probe**: Detects if a container is alive and restarts it if it fails.
- **Readiness probe**: Detects if a container is ready to serve traffic, but does **not** restart it if it fails (it simply stops traffic from being routed to it).

Readiness probes are commonly used to wait for a service to become fully initialized before receiving traffic or to avoid sending traffic to a service that is temporarily unable to handle requests.

---

### 2. Types of Readiness Probes

Like liveness probes, readiness probes also support four types:
1. **HTTP (`httpGet`) Probe**
2. **TCP (`tcpSocket`) Probe**
3. **gRPC (`grpc`) Probe**
4. **Command Execution (`exec`) Probe**

Let's explore hands-on examples for each of these readiness probe types.

---

### 3. Readiness Probe Types, Hands-on Examples, and Best Practices

#### 1. HTTP (`httpGet`) Readiness Probe

**What it is doing**:
- The `httpGet` readiness probe sends an HTTP GET request to a specified path and port inside the container.
- If the container returns a valid HTTP status code (e.g., 200 OK), the probe is considered successful, indicating the container is ready to serve traffic.

**What it is checking**:
- It checks if the application is up and running and able to respond to HTTP requests.
- Typically, it checks for the presence of a `/healthz` or `/readiness` endpoint that confirms the application is fully initialized and ready to accept traffic.

**Example**: For an NGINX-based application

1. **Create the YAML File**: Save the following content as `httpget-readiness-deployment.yaml`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: httpget-readiness-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 10
```

2. **Deploy the YAML File**: Run the following command to deploy the NGINX application with the HTTP readiness probe.

```bash
kubectl apply -f httpget-readiness-deployment.yaml
```

**What it checks**:
- The readiness probe sends an HTTP GET request to the `/healthz` path on port `80` to check if the NGINX server is ready to serve traffic.
- After a 5-second delay, Kubernetes will start periodically checking the `/healthz` endpoint to confirm the container is ready to handle incoming traffic.

**Best Practices**:
- Use a dedicated `/readiness` or `/healthz` endpoint for readiness checks that only signals readiness once the application is fully initialized.
- Adjust the `initialDelaySeconds` and `periodSeconds` for services that take longer to start up.

---

#### 2. TCP (`tcpSocket`) Readiness Probe

**What it is doing**:
- The `tcpSocket` readiness probe attempts to open a TCP connection to a specified port inside the container.
- If the connection succeeds, it indicates that the container is ready to handle traffic.

**What it is checking**:
- It checks whether the container is actively listening for incoming traffic on the specified port.
- Unlike the `httpGet` probe, it doesn't check for any specific HTTP response, just whether the port is open and accepting TCP connections.

**Example**: For an NGINX-based application using TCP probe

1. **Create the YAML File**: Save the following content as `tcp-readiness-deployment.yaml`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tcp-readiness-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: tcp-nginx
  template:
    metadata:
      labels:
        app: tcp-nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
        readinessProbe:
          tcpSocket:
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 10
```

2. **Deploy the YAML File**: Run the following command to deploy the NGINX deployment with the TCP readiness probe.

```bash
kubectl apply -f tcp-readiness-deployment.yaml
```

**What it checks**:
- This probe checks whether the NGINX application is ready by attempting to establish a TCP connection to port `80`.
- If the application is listening on port `80`, the probe passes, and Kubernetes considers the container ready to serve traffic.

**Best Practices**:
- Use `tcpSocket` for applications that do not expose HTTP APIs but still need to listen for connections.
- Ensure the application is not only listening on the port but is also fully initialized.

---

#### 3. gRPC (`grpc`) Readiness Probe

**What it is doing**:
- The `grpc` readiness probe sends a health check request via the gRPC protocol to a specified gRPC service endpoint.
- If the service responds with a successful health status (typically “Serving”), the probe considers the container ready.

**What it is checking**:
- It checks whether the gRPC service is fully initialized and able to handle incoming requests.
- This is particularly useful for microservices using gRPC.

**Example**: For a gRPC-based `etcd` service

1. **Create the YAML File**: Save the following content as `grpc-readiness-deployment.yaml`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grpc-readiness-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grpc-app
  template:
    metadata:
      labels:
        app: grpc-app
    spec:
      containers:
      - name: etcd
        image: registry.k8s.io/etcd:3.5.1-0
        command: [ "/usr/local/bin/etcd", "--data-dir",  "/var/lib/etcd", "--listen-client-urls", "http://0.0.0.0:2379", "--advertise-client-urls", "http://127.0.0.1:2379", "--log-level", "debug"]
        ports:
        - containerPort: 2379
        readinessProbe:
          grpc:
            port: 2379
          initialDelaySeconds: 10
```

2. **Deploy the YAML File**: Run the following command to deploy the `etcd` service with the gRPC readiness probe.

```bash
kubectl apply -f grpc-readiness-deployment.yaml
```

**What it checks**:
- This probe checks whether the `etcd` service is ready to handle requests via the gRPC protocol by connecting to the service’s gRPC endpoint at port `2379`.
- If the `etcd` service responds with a successful status, the probe considers the container ready to receive traffic.

**Best Practices**:
- Use the gRPC readiness probe for services that implement gRPC and expose a health-check endpoint via the protocol.
- Ensure that the gRPC service responds correctly to health check requests.

---

#### 4. Command Execution (`exec`) Readiness Probe

**What it is doing**:
- The `exec` readiness probe runs a command inside the container to determine if it is ready.
- If the command exits with a status code of `0`, the container is considered ready. If the command fails (non-zero exit code), it indicates the container is not yet ready.

**What it is checking**:
- It checks for custom logic inside the container that can verify if the container is ready to handle traffic.
- This can be useful for more complex readiness checks, such as checking if required files are present or if specific internal processes are running.

**Example**: For a simple BusyBox-based application

1. **Create the YAML File**: Save the following content as `exec-readiness-deployment.yaml`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: exec-readiness-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: exec-app
  template:
    metadata:
      labels:
        app: exec-app
    spec:
      containers:
      - name: exec-app
        image: busybox
        args:
        - /bin/sh
        - -c
        - |
          touch /tmp/ready; sleep 10; rm -f /tmp/ready; sleep 600
        readinessProbe:
          exec:
            command:
            - cat
            - /tmp/ready
          initialDelaySeconds: 5
          periodSeconds: 10
```

2. **Deploy the YAML File**: Run the following command to deploy the BusyBox application with the exec

 readiness probe.

```bash
kubectl apply -f exec-readiness-deployment.yaml
```

**What it checks**:
- This readiness probe checks for the existence of the `/tmp/ready` file inside the container. If the file is present (after `sleep 10`), the container is considered ready.
- Once the file is removed, the readiness probe will fail until the file is created again.

**Best Practices**:
- Use `exec` for complex readiness checks that involve custom logic.
- Ensure that the command used in the `exec` probe is lightweight and fast to avoid unnecessary overhead.

---

### 4. General Best Practices for Readiness Probes

- **Start Simple**: Begin with basic checks and gradually refine your readiness probe as your application evolves.
- **Use Dedicated Endpoints**: For HTTP and gRPC probes, use a dedicated `/readiness` endpoint that is separate from liveness and other health checks.
- **Avoid Heavy Commands**: Use lightweight, non-blocking commands in `exec` probes to minimize the impact on container performance.
- **Adjust Delays and Periods**: Use `initialDelaySeconds`, `periodSeconds`, and `failureThreshold` to account for startup time and performance characteristics of your application.
- **Avoid Overloading**: Too frequent probes or resource-heavy commands can cause unnecessary load or slowdowns.

By choosing the right readiness probe for your application, you can ensure better traffic management and a smoother user experience, especially for microservices or services that take time to start or initialize fully.