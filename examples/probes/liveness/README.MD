# Liveness Probe  

### 1. What is a Liveness Probe?  

In Kubernetes, a **liveness probe** is a mechanism to periodically check whether a container is still running as expected. If the liveness probe fails, Kubernetes will automatically restart the container to try to restore it to a healthy state. This helps maintain application availability by recovering from failures without manual intervention.

---

### 2. Types of Liveness Probes

Kubernetes supports four types of liveness probes:
1. **HTTP (`httpGet`) Probe**
2. **TCP (`tcpSocket`) Probe**
3. **gRPC (`grpc`) Probe**
4. **Command Execution (`exec`) Probe**

Each type is suitable for different kinds of applications. Let’s explore hands-on examples for each probe, explaining what they are doing and what exactly is being checked.

---

### 3. Liveness Probe Types, Hands-on Examples, and Best Practices

#### 1. HTTP (`httpGet`) Probe

**What it is doing**:
- The `httpGet` probe sends an HTTP GET request to a specific URL and port inside the container.
- The probe checks if the container responds with an HTTP status code in the 200-399 range, which indicates that the container is healthy.

**What it is checking**:
- It checks if the container is running and responding to HTTP requests correctly.
- It expects a valid response (e.g., a 200 OK status) from the specified URL path.

**Example**: For an NGINX-based application

1. **Create the YAML File**: Save the following content as `httpget-deployment.yaml`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: httpget-deployment
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
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 10
```

2. **Deploy the YAML File**: Run the following command to deploy the NGINX deployment with the HTTP liveness probe.

```bash
kubectl apply -f httpget-deployment.yaml
```

**What it checks**:
- This `httpGet` probe checks whether the NGINX server responds to requests on the `/` path.
- After an initial delay of 5 seconds, it sends an HTTP request every 10 seconds to check the health of the NGINX server.
- If the NGINX server returns a 200-series status code (indicating a successful response), the probe passes. Otherwise, it fails.

**Best Practices**:
- **Health Endpoint**: Set up a lightweight `/healthz` endpoint for health checks to avoid performance overhead.
- **Time-sensitive**: Adjust `timeoutSeconds` to ensure that probes do not wait too long before determining failure.

---

#### 2. TCP (`tcpSocket`) Probe

**What it is doing**:
- The `tcpSocket` probe attempts to establish a TCP connection to the specified port inside the container.
- If the connection succeeds, the probe passes. If the connection fails (i.e., no service is listening on the port), the probe fails.

**What it is checking**:
- It checks whether the application is actively listening on the specified TCP port.
- Unlike `httpGet`, it does not check the content of the response, just whether the port is open and accepting connections.

**Example**: For an NGINX application using TCP probe

1. **Create the YAML File**: Save the following content as `tcp-nginx-deployment.yaml`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tcp-nginx-deployment
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
        livenessProbe:
          tcpSocket:
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 10
```

2. **Deploy the YAML File**: Run the following command to deploy the NGINX deployment with the TCP liveness probe.

```bash
kubectl apply -f tcp-nginx-deployment.yaml
```

**What it checks**:
- The probe checks if the NGINX application is listening on port `80` by attempting to open a TCP connection to that port.
- If the port is open and the application is accepting connections, the probe will pass.
- If no service is listening on the port, the probe fails, triggering a container restart.

**Best Practices**:
- Use TCP probes for simple applications that don’t provide HTTP APIs but require ports to be open.
- Ensure the application is truly ready and not just listening on the port (i.e., avoid false positives).

---

#### 3. gRPC (`grpc`) Probe

**What it is doing**:
- The `grpc` probe sends a gRPC health-check request to a specified gRPC service endpoint.
- It uses the gRPC protocol to check if the service responds correctly to health-check messages.

**What it is checking**:
- It checks whether the gRPC service is running and responds with a success code (typically a "Serving" status in gRPC health checks).
- This probe is typically used in microservices built with gRPC.

**Example**: For an `etcd` service

1. **Create the YAML File**: Save the following content as `grpc-deployment.yaml`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grpc-deployment
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
        livenessProbe:
          grpc:
            port: 2379
          initialDelaySeconds: 10
```

2. **Deploy the YAML File**: Run the following command to deploy the `etcd` deployment with the gRPC liveness probe.

```bash
kubectl apply -f grpc-deployment.yaml
```

**What it checks**:
- The probe checks whether the `etcd` service is responsive and healthy by connecting to the gRPC endpoint at port `2379`.
- If the gRPC service returns a healthy status, the probe passes. If it does not, the probe fails, and Kubernetes will attempt to restart the container.

**Best Practices**:
- Use for microservices or applications that expose health checks via gRPC.
- Ensure that the gRPC service correctly implements the health-check protocol for the probe to work.

---

#### 4. Command Execution (`exec`) Probe

**What it is doing**:
- The `exec` probe runs a command inside the container.
- If the command exits with a status code of `0` (indicating success), the probe passes. If the command exits with any other code, the probe fails.

**What it is checking**:
- It checks if the command (e.g., `cat /tmp/healthy`) runs successfully. This can be used for more custom checks inside the container.

**Example**: For a simple BusyBox application

1. **Create the YAML File**: Save the following content as `exec-deployment.yaml`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: exec-deployment
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
          touch /tmp/healthy; sleep 10; rm -f /tmp/healthy; sleep 600
        livenessProbe:
          exec:
            command:
            - cat
            - /tmp/healthy
          initialDelaySeconds: 5
          periodSeconds: 10
```

2. **Deploy the YAML File**: Run the following command to deploy the BusyBox deployment with the exec liveness probe.

```bash
kubectl apply -f exec-deployment.yaml
```

**What it checks**:
- The `exec` probe checks whether the `cat /tmp/healthy` command inside the container can run successfully.
- The command attempts to read the `/tmp/healthy` file. If the file exists, the probe succeeds; if it doesn't, it fails.
- The `/tmp/healthy` file is created and deleted as part of a basic health-check mechanism in this example.

**Best Practices**:
- Keep `exec` commands lightweight to avoid unnecessary resource consumption.
- Use for custom health-check logic or simple file existence checks that don't require HTTP or TCP endpoints.

---

### 4. General Best Practices for Liveness Probes

- **Start Simple**: Begin with basic health checks and then expand as your application’s needs grow.
- **Avoid Heavy Checks**: Liveness probes should be lightweight to avoid consuming excessive CPU or memory.
- **Set Sensible Intervals and Thresholds**: Adjust `initialDelaySeconds`, `timeoutSeconds`, `failureThreshold`, and `periodSeconds` according to your application’s performance and stability characteristics.
- **Monitor and Refine**: Continuously monitor probe failures and adjust settings if the application is being restarted too frequently.

Each type of probe is intended for specific scenarios, so choose the one that best matches your application’s needs. Proper configuration and usage of liveness probes can significantly enhance the stability and availability of your applications on Kubernetes.