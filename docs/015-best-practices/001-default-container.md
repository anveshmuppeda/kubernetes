---
// filepath: docs/015-best-practices/001-default-container.md
title: "CSI Ephemeral Storage"
description: "Understanding Ephemeral Storage in Kubernetes"
sidebar_label: "CSI Ephemeral Storage"
sidebar_id: "csi-ephemeral-storage"
sidebar_position: 1
---  

# Setting a Default Container in Kubernetes

**A quick and easy fix to streamline your `kubectl` commands for multi-container pods.**

![Default Container Annotation](./img/default-container.png)

When working with Kubernetes, you've likely encountered pods running multiple containers. This is a common and powerful pattern, often used for sidecars that handle tasks like logging, monitoring, or service mesh proxying. However, this setup can introduce a small but persistent annoyance: `kubectl` commands like `logs` and `exec` require you to specify which container you want to target.

If you forget the `-c` or `--container` flag, `kubectl` simply defaults to the first container defined in the pod's manifest. This might not be the container you're interested in, leading to repeated command corrections and a clunky workflow.

Fortunately, there's a simple and elegant solution to this problem: the `kubectl.kubernetes.io/default-container` annotation.

---

## The Fix: A Simple Annotation

By adding this annotation to your pod's metadata, you can explicitly declare which container should be the default for `kubectl` commands. This eliminates the need to constantly specify the container name, making your interactions with multi-container pods much smoother.

The annotation is a key-value pair:

* **Key:** `kubectl.kubernetes.io/default-container`
* **Value:** The name of the container you want to set as the default.

You can apply this annotation in a few ways:

* **During Pod Creation:** Include the annotation directly in your pod's YAML manifest.
* **To an Existing Pod:** Use the `kubectl annotate` command to add or update the annotation on a running pod.

---

## Hands-On Example

Let's walk through a practical example to see how this works.

### 1. The Problem: A Pod with Two Containers

First, let's create a pod with two containers: a main application container and a sidecar container.

Create a file named `multi-container-pod.yaml` with the following content:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  containers:
  - name: sidecar-container
    image: busybox
    command: ["/bin/sh", "-c", "while true; do echo 'I am a sidecar'; sleep 10; done"]
  - name: main-container
    image: nginx
    ports:
    - containerPort: 80
```

Now, create the pod using `kubectl`:

```bash
kubectl apply -f multi-container-pod.yaml
```

If you try to get the logs from this pod without specifying a container, `kubectl` will default to the first one listed in the manifest, which is `sidecar-container`:

```bash
kubectl logs my-app
```

You'll see the output from the sidecar:

```
I am a sidecar
```

To see the logs for the `main-container` (the NGINX container), you would need to explicitly specify it:

```bash
kubectl logs my-app -c main-container
```

### 2. The Solution: Applying the Annotation

Now, let's fix this by adding the `kubectl.kubernetes.io/default-container` annotation to our pod. We'll set `main-container` as the default.

#### Option A: Editing the Manifest

You can add the annotation directly to your `multi-container-pod.yaml` file:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  annotations:
    kubectl.kubernetes.io/default-container: "main-container"
spec:
  containers:
  - name: sidecar-container
    image: busybox
    command: ["/bin/sh", "-c", "while true; do echo 'I am a sidecar'; sleep 10; done"]
  - name: main-container
    image: nginx
    ports:
    - containerPort: 80
```

Then, apply the changes:

```bash
kubectl apply -f multi-container-pod.yaml
```

#### Option B: Using `kubectl annotate`

If the pod is already running, you can add the annotation using the `kubectl annotate` command:

```bash
kubectl annotate pod my-app kubectl.kubernetes.io/default-container="main-container"
```

### 3. The Result: Simplified Commands

Now that the annotation is in place, try running the `kubectl logs` command again without specifying a container:

```bash
kubectl logs my-app
```

This time, you'll see the logs from the `main-container` by default, as you intended. Similarly, if you were to use `kubectl exec`, you would be dropped into the `main-container`.

By taking a moment to add this simple annotation, you can save yourself and your team a lot of time and frustration in the long run. It's a small change that can significantly improve your daily Kubernetes workflow.
