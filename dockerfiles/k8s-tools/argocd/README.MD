# **K8s Tools Docker Images - ArgoCD**

*Lightweight, Versioned ArgoCD CLI Container for Seamless Kubernetes Application Management*

---

## Summary

This repository provides a Docker image under the `anvesh35/argocd-cli` namespace that packages the ArgoCD CLI into a lightweight, self-contained container. This allows users to manage ArgoCD applications and clusters without installing the ArgoCD CLI locally. The image is built using a multi-stage build process on Alpine Linux, ensuring a minimal footprint and secure execution.

---

## Image Naming Convention

All images are hosted on Docker Hub under the `anvesh35/argocd-cli` repository.  
Tags follow the pattern `<version>`, for example `v2.8.3`, to indicate the ArgoCD CLI version included in the image.

---

## Build Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/anveshmuppeda/kubernetes.git
cd dockerfiles/k8s-tools/argocd
```

### 2. Build the Image
Replace `<version>` with the desired ArgoCD CLI version (e.g., `v2.8.3`):
```bash
docker build \
  --build-arg ARGOCD_VERSION=<version> \
  -t anvesh35/argocd-cli:<version> .
```

Example:
```bash
docker build \
  --build-arg ARGOCD_VERSION=v2.8.3 \
  -t anvesh35/argocd-cli:v2.8.3 .
```

---

## Usage

### Pull the Image from Docker Hub
To use the pre-built image from Docker Hub, pull it using:
```bash
docker pull anvesh35/argocd-cli:<version>
```

Example:
```bash
docker pull anvesh35/argocd-cli:v2.8.3
```

---

### Interactive Shell
Run the container interactively with your kubeconfig mounted for cluster access:
```bash
docker run --rm -it \
  --network host \
  -v $HOME/.kube/config:/home/argocd/.kube/config:ro \
  anvesh35/argocd-cli:<version> bash
```

This opens a Bash shell with the ArgoCD CLI installed and ready to use.

---

### One-Off ArgoCD Commands
Run ArgoCD commands directly without entering the container:
```bash
docker run --rm \
  --network host \
  -v $HOME/.kube/config:/home/argocd/.kube/config:ro \
  anvesh35/argocd-cli:<version> \
  argocd app list
```

---

## Features

- **Multi-Stage Build**: Downloads and verifies the ArgoCD CLI binary in a builder stage, then copies only the necessary files into the final image.
- **Minimal Alpine Base**: Uses Alpine Linux to keep the image size small (~9 MB).
- **Non-Root User**: Runs as a dedicated `argocd` user to adhere to container security best practices.
- **Version-Pinned Binaries**: Ensures reproducible environments by using explicit semantic versions.
- **Flexible Tagging**: Supports version-specific tags (e.g., `v2.8.3`).

---

## Example Commands

### Check ArgoCD Version
```bash
docker run --rm \
  anvesh35/argocd-cli:v2.8.3 \
  argocd version
```

### List All Applications
```bash
docker run --rm \
  --network host \
  -v $HOME/.kube/config:/home/argocd/.kube/config:ro \
  anvesh35/argocd-cli:v2.8.3 \
  argocd app list
```

---

## Contributing

Contributions are welcome via GitHub pull requests. Please follow multi-stage build patterns, use semantic versioning for new tool images, and adhere to lowercase, hyphenated naming conventions.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.