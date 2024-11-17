# Startup Probe  

### 1. What is a Startup Probe?

In Kubernetes, a **startup probe** is used to determine if a container has started successfully. It’s designed to help with containers that have long initialization times. If the startup probe fails, the container will be restarted. However, unlike the liveness probe, which checks the health of a running container, the startup probe only checks if the container has successfully started up. If the startup probe fails, Kubernetes will attempt to restart the container.

**When to use a startup probe**:
- For applications that take a long time to initialize before they can serve traffic, you would use a startup probe to ensure Kubernetes doesn't prematurely consider the container as unhealthy during this startup phase.
- For containers that require a specific amount of time or resources to be ready before they can run correctly.

**Key difference from other probes**:
- **Startup probe** is used to monitor the startup phase of a container.
- **Liveness probe** checks if the container is still running after startup.
- **Readiness probe** checks if the container is ready to accept traffic after it has started.

---

### 2. Types of Startup Probes

Just like with liveness and readiness probes, Kubernetes supports multiple types of startup probes:

1. **HTTP (`httpGet`) Probe**
2. **TCP (`tcpSocket`) Probe**
3. **gRPC (`grpc`) Probe**
4. **Command Execution (`exec`) Probe**

Let's explore hands-on examples for each of these startup probe types.

---

### 3. Startup Probe Types, Hands-on Examples, and Best Practices

#### 1. HTTP (`httpGet`) Startup Probe

**What it is doing**:
- The `httpGet` startup probe sends an HTTP GET request to a specified path and port within the container to check if the container has successfully started.
- If the application responds with a valid HTTP status code (e.g., 200 OK), it indicates the container has started successfully.

**What it is checking**:
- It checks if the application is serving HTTP requests on the specified path.
- Typically, you can use a custom endpoint like `/healthz` that the application exposes to confirm that it has started correctly.

**Example**: For an NGINX-based application

1. **Create the YAML File**: Save the following content as `httpget-startup-deployment.yaml`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: httpget-startup-deployment
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
        startupProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 10
          periodSeconds: 5
          failureThreshold: 5
```

2. **Deploy the YAML File**: Run the following command to deploy the NGINX application with the HTTP startup probe.

```bash
kubectl apply -f httpget-startup-deployment.yaml
```

**What it checks**:
- The startup probe sends an HTTP GET request to the `/healthz` path on port `80`.
- If the NGINX container responds successfully with a 200 OK HTTP status, Kubernetes considers the container as successfully started.

**Best Practices**:
- Use a dedicated `/healthz` or `/startup` endpoint for startup checks, distinct from readiness and liveness endpoints.
- Use `failureThreshold` to control how many consecutive failures are allowed before considering the container failed.
- Set appropriate `initialDelaySeconds` to give your container enough time to initialize.

---

#### 2. TCP (`tcpSocket`) Startup Probe

**What it is doing**:
- The `tcpSocket` startup probe attempts to establish a TCP connection to a specified port inside the container.
- If the connection is successful, it indicates that the container has successfully started.

**What it is checking**:
- It checks whether the container is listening for incoming TCP connections on the specified port, which can indicate the application is initialized and ready to handle traffic.

**Example**: For an NGINX-based application using TCP probe

1. **Create the YAML File**: Save the following content as `tcp-startup-deployment.yaml`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tcp-startup-deployment
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
        startupProbe:
          tcpSocket:
            port: 80
          initialDelaySeconds: 10
          periodSeconds: 5
          failureThreshold: 5
```

2. **Deploy the YAML File**: Run the following command to deploy the NGINX application with the TCP startup probe.

```bash
kubectl apply -f tcp-startup-deployment.yaml
```

**What it checks**:
- The probe attempts to establish a TCP connection to port `80` on the container.
- If the NGINX container is listening and the connection is established, the probe will consider the container started.

**Best Practices**:
- Use `tcpSocket` probes when the application doesn't expose an HTTP API but still requires a connection to a specific port to function properly.
- Set `failureThreshold` to control how many connection attempts should be made before the container is considered failed.

---

#### 3. gRPC (`grpc`) Startup Probe

**What it is doing**:
- The `grpc` startup probe sends a health check request over the gRPC protocol to a specified service inside the container.
- If the service responds with a healthy status, the probe will consider the container as successfully started.

**What it is checking**:
- It checks whether the gRPC service inside the container is up and running and ready to accept traffic.

**Example**: For an `etcd` service using gRPC

1. **Create the YAML File**: Save the following content as `grpc-startup-deployment.yaml`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grpc-startup-deployment
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
        startupProbe:
          grpc:
            port: 2379
          initialDelaySeconds: 10
          periodSeconds: 5
          failureThreshold: 5
```

2. **Deploy the YAML File**: Run the following command to deploy the `etcd` service with the gRPC startup probe.

```bash
kubectl apply -f grpc-startup-deployment.yaml
```

**What it checks**:
- The probe checks whether the `etcd` service is reachable via gRPC on port `2379`.
- Once `etcd` responds positively, Kubernetes considers the container started.

**Best Practices**:
- Use `grpc` probes for gRPC-based services.
- Ensure that your gRPC service exposes a health-check endpoint that can confirm its readiness.

---

#### 4. Command Execution (`exec`) Startup Probe

**What it is doing**:
- The `exec` startup probe runs a command inside the container to verify if it has started successfully.
- If the command exits with a status code of `0`, the container is considered to have successfully started.

**What it is checking**:
- It checks custom initialization logic or conditions that need to be met before the container is considered started.

**Example**: For a BusyBox-based application

1. **Create the YAML File**: Save the following content as `exec-startup-deployment.yaml`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: exec-startup-deployment
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
          touch /tmp/startup; sleep 10; rm -f /tmp/startup; sleep 600
        startupProbe:
          exec:
            command:
            - cat
            - /tmp/startup
          initialDelaySeconds: 5
          periodSeconds: 10
          failureThreshold: 5
```

2. **Deploy the YAML File**: Run the following command to deploy the BusyBox application with the exec startup probe.

```bash
kubectl apply -f exec-startup-deployment.yaml
```

**What it checks**:
- The `exec

` probe checks for the existence of the `/tmp/startup` file.
- If the file exists, it indicates that the container has successfully started.

**Best Practices**:
- Use `exec` probes for custom or complex startup checks that can't be easily handled by HTTP, TCP, or gRPC probes.
- Ensure that the command used in the probe is efficient and quick to avoid unnecessary delays.

---

### 4. General Best Practices for Startup Probes

- **Use Only When Necessary**: Startup probes are useful for containers that have long initialization times. If your container starts up quickly, a liveness or readiness probe might suffice.
- **Avoid Resource-Heavy Commands**: Like liveness and readiness probes, keep commands in `exec` probes lightweight to avoid overloading the container.
- **Adjust Time Delays**: Set appropriate `initialDelaySeconds`, `failureThreshold`, and `periodSeconds` to ensure the startup probe doesn’t fail prematurely.
- **Separate Logic for Initialization**: Use dedicated endpoints or files for startup checks to keep things simple and avoid confusion with readiness or liveness checks.

By carefully using startup probes, you can ensure that Kubernetes waits long enough for your container to initialize fully, providing a more resilient and stable environment for your applications.