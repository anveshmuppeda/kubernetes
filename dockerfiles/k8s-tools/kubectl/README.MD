# **K8s Tools Docker Images - kubectl**

*Lightweight, Versioned `kubectl` CLI Container for Seamless Kubernetes Cluster Management*

---

## Summary

This repository provides a Docker image under the `anvesh35/kubectl-cli` namespace that packages the `kubectl` CLI into a lightweight, self-contained container. This allows users to manage Kubernetes clusters without installing the `kubectl` CLI locally. The image is built using a multi-stage build process on Alpine Linux, ensuring a minimal footprint and secure execution.

---

## Image Naming Convention

All images are hosted on Docker Hub under the `anvesh35/kubectl-cli` repository.  
Tags follow the pattern `<version>`, for example `v1.29.3`, to indicate the `kubectl` CLI version included in the image.

---

## Build Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/anveshmuppeda/kubernetes.git
cd dockerfiles/k8s-tools/kubectl
```

### 2. Build the Image
Replace `<version>` with the desired `kubectl` CLI version (e.g., `v1.29.3`):
```bash
docker build \
  --build-arg KUBECTL_VERSION=<version> \
  -t anvesh35/kubectl-cli:<version> .
```
Example:
```bash
docker build \
  --build-arg KUBECTL_VERSION=v1.29.3 \
  -t anvesh35/kubectl-cli:v1.29.3 .
```
---
## Usage
### Pull the Image from Docker Hub
To use the pre-built image from Docker Hub, pull it using:
```bash
docker pull anvesh35/kubectl-cli:<version>
```
Example:
```bash
docker pull anvesh35/kubectl-cli:v1.29.3
```

---

## Interactive Shell
To start an interactive shell session with the `kubectl` CLI, run:
```bash
docker run --rm -it \
  --network host \
  -v $HOME/.kube/config:/root/.kube/config:ro \
  anvesh35/kubectl-cli:<version> bash
```
This opens a Bash shell with the kubectl CLI installed and ready to use.

---

## One-Off Commands
Run kubectl commands directly without entering the container:  
```bash
docker run --rm \
  --network host \
  -v $HOME/.kube/config:/root/.kube/config:ro \
  anvesh35/kubectl-cli:<version> \
  kubectl get nodes
  ```  

This command retrieves the list of nodes in your Kubernetes cluster.
You can replace `kubectl get nodes` with any other `kubectl` command you wish

---  

## Features
1. Multi-Stage Build: Downloads and verifies the kubectl CLI binary in a builder stage, then copies only the necessary files into the final image.
2. Minimal Alpine Base: Uses Alpine Linux to keep the image size small (~9 MB).
3. Version-Pinned Binaries: Ensures reproducible environments by using explicit semantic versions.
4. Flexible Tagging: Supports version-specific tags (e.g., v1.29.3).

---  
## Example Commands
#### Check kubectl Version  
```bash
docker run --rm \
  --network host \
  -v $HOME/.kube/config:/root/.kube/config:ro \
  anvesh35/kubectl-cli:<version> \
  kubectl version --client
```
#### List All Nodes  
```bash
docker run --rm \
  --network host \
  -v $HOME/.kube/config:/root/.kube/config:ro \
  anvesh35/kubectl-cli:<version> \
  kubectl get nodes
```

--- 

## Contributing
Contributions are welcome via GitHub pull requests. Please follow multi-stage build patterns, use semantic versioning for new tool images, and adhere to lowercase, hyphenated naming conventions.

