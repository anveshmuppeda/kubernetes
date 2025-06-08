---
// filepath: /Users/anveshmuppeda/Desktop/anvesh/tech/git/kubernetes/docs/014-storage/002-ephemeral-cm.md
title: "Ephemeral Storage with ConfigMap, Secret, & Downward API"
description: "Understanding Ephemeral Storage in Kubernetes with ConfigMap, Secret, and Downward API"
sidebar_label: "Ephemeral Storage with ConfigMap, Secret, & Downward API"
sidebar_id: "ephemeral-cm"
sidebar_position: 1
---  

# Injecting Data Into Pods: `ConfigMap`, `Secret`, & `DownwardAPI` Explained

:::tip
Use the [manifest templates](https://github.com/anveshmuppeda/kubernetes/tree/feature/docs_update/docs/014-storage/manifests) to create your own Kubernetes resources which can be used in the examples below.
:::

Building container images is great for packaging your application, but what about its configuration? Hardcoding configuration is inflexible, and rebuilding an image for every environment is inefficient. Kubernetes solves this by letting you **inject** configuration and metadata into your Pods at runtime.

This guide covers the three primary ways to do this:
* **`ConfigMaps`**: For non-sensitive configuration data.
* **`Secrets`**: For sensitive data like passwords and API keys.
* **The `DownwardAPI`**: For exposing a Pod's own metadata to itself.

---

## `ConfigMap`: Managing Non-Sensitive Configuration 📄

A `ConfigMap` is a Kubernetes object used to store configuration data as key-value pairs. It's perfect for things like application endpoints, feature flags, or environment-specific settings.

There are two main ways to use `ConfigMap` data in a Pod: as environment variables or as mounted files.

### Example: Using a `ConfigMap`

#### Step 1: Create the `ConfigMap`

Let's create a `ConfigMap` with some application settings.

```bash
# Create a ConfigMap named 'app-config' with two key-value pairs
kubectl create configmap app-config \
  --from-literal=LOG_LEVEL=info \
  --from-literal=API_ENDPOINT=https://api.example.com/v1
```

#### Step 2: Inject as Environment Variables

This method is simple and direct. Create a file named `pod-cm-env.yaml`.

```yaml
# pod-cm-env.yaml
apiVersion: v1
kind: Pod
metadata:
  name: cm-env-pod
spec:
  containers:
  - name: main-app
    image: busybox
    command: ["/bin/sh", "-c", "echo 'Log level is $LOG_LEVEL' && echo 'API is at $API_ENDPOINT' && sleep 3600"]
    envFrom:
    - configMapRef:
        name: app-config # This injects all keys from the ConfigMap as environment variables
```

Deploy and check the logs:
```bash
kubectl apply -f pod-cm-env.yaml
kubectl logs cm-env-pod
```
**Output:**
```
Log level is info
API is at https://api.example.com/v1
```

#### Step 3: Mount as a Volume

Mounting a `ConfigMap` as a volume is more powerful, as it allows for live updates without restarting the Pod. Create a file named `pod-cm-volume.yaml`.

```yaml
# pod-cm-volume.yaml
apiVersion: v1
kind: Pod
metadata:
  name: cm-volume-pod
spec:
  containers:
  - name: main-app
    image: busybox
    command: ["/bin/sh", "-c", "sleep 3600"]
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config # Mount the volume at this path
  volumes:
  - name: config-volume
    configMap:
      name: app-config # Use the 'app-config' ConfigMap to create files in the volume
```
Deploy the Pod and check the mounted files:
```bash
kubectl apply -f pod-cm-volume.yaml
kubectl exec -it cm-volume-pod -- ls /etc/config
```
**Output:**
```
API_ENDPOINT
LOG_LEVEL
```
You can then `cat` these files to see their content.

---

## `Secret`: For Sensitive Data 🤫

A `Secret` is structurally identical to a `ConfigMap` but is intended for sensitive data. Kubernetes stores secrets as base64 encoded strings.

**Important:** By default, secrets are only encoded, **not encrypted**. For true security, you must enable encryption at rest for your etcd datastore.

### Example: Using a `Secret`

#### Step 1: Create the `Secret`

Let's create a secret for a database username and password.

```bash
kubectl create secret generic db-credentials \
  --from-literal=DB_USER=admin \
  --from-literal=DB_PASSWORD='S3cr3tP@ssw0rd!'
```

#### Step 2: Mount as a Volume (Recommended Method)

Mounting secrets as files is generally more secure than exposing them as environment variables, as it prevents accidental logging. Create a file named `pod-secret-volume.yaml`.

```yaml
# pod-secret-volume.yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-volume-pod
spec:
  containers:
  - name: main-app
    image: busybox
    command: ["/bin/sh", "-c", "sleep 3600"]
    volumeMounts:
    - name: secret-volume
      mountPath: /etc/secrets
      readOnly: true # Good practice for secrets
  volumes:
  - name: secret-volume
    secret:
      secretName: db-credentials
```
Deploy the Pod and inspect the files:
```bash
kubectl apply -f pod-secret-volume.yaml
kubectl exec -it secret-volume-pod -- cat /etc/secrets/DB_PASSWORD
```
**Output:**
```
S3cr3tP@ssw0rd!
```

---

## The `DownwardAPI`: Exposing Pod Metadata 👇

What if your application needs to know its own name, IP address, or the node it's running on? The `DownwardAPI` provides this "self-awareness" by exposing Pod and Node metadata to the containers running inside it.

The `DownwardAPI` doesn't require creating a separate object; you define it directly in the Pod spec.

### Example: Using the `DownwardAPI`

This example exposes the Pod's name, namespace, and labels as files inside the container. Create a file named `pod-downward.yaml`.

```yaml
# pod-downward.yaml
apiVersion: v1
kind: Pod
metadata:
  name: downward-api-pod
  labels:
    app: my-app
    version: v1.0
spec:
  containers:
  - name: main-app
    image: busybox
    command: ["/bin/sh", "-c", "sleep 3600"]
    volumeMounts:
    - name: pod-info
      mountPath: /etc/podinfo
  volumes:
  - name: pod-info
    downwardAPI:
      items:
        - path: "podName"         # Creates a file named 'podName'
          fieldRef:
            fieldPath: metadata.name
        - path: "namespace"       # Creates a file named 'namespace'
          fieldRef:
            fieldPath: metadata.namespace
        - path: "labels"          # Creates a file named 'labels'
          fieldRef:
            fieldPath: metadata.labels
```
Deploy the Pod and inspect the generated files:
```bash
kubectl apply -f pod-downward.yaml
kubectl exec -it downward-api-pod -- cat /etc/podinfo/labels
```
**Output:**
```
app="my-app"
version="v1.0"
```

---

## Choosing the Right Tool for the Job

* **Is it non-sensitive configuration data for your application?**
    * Use a **`ConfigMap`**.
* **Is it a password, token, or other sensitive data?**
    * Use a **`Secret`**.
* **Does your application need to know its own name, IP, labels, or resource limits?**
    * Use the **`DownwardAPI`**.

By mastering these three mechanisms, you can create flexible, decoupled, and environment-aware applications on Kubernetes.
