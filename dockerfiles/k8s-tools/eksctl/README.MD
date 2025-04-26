# **K8s Tools Docker Images - eksctl**

*Lightweight, Versioned eksctl CLI Container for Seamless Amazon EKS Cluster Management*

---

## Summary

This repository provides a Docker image under the `anvesh35/eksctl-cli` namespace that packages the eksctl CLI into a lightweight, self-contained container. This allows users to manage Amazon EKS clusters without installing the eksctl CLI locally. The image is built using a multi-stage build process on Alpine Linux, ensuring a minimal footprint and secure execution.

---

## Image Naming Convention

All images are hosted on Docker Hub under the `anvesh35/eksctl-cli` repository.  
Tags follow the pattern `<version>`, for example `v0.150.0`, to indicate the eksctl CLI version included in the image.

---

## Build Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/anveshmuppeda/kubernetes.git
cd dockerfiles/k8s-tools/eksctl
```

### 2. Build the Image
Replace `<version>` with the desired eksctl CLI version (e.g., `v0.150.0`):
```bash
docker build \
  --build-arg EKSCTL_VERSION=<version> \
  -t anvesh35/eksctl-cli:<version> .
```

Example:
```bash
docker build \
  --build-arg EKSCTL_VERSION=v0.150.0 \
  -t anvesh35/eksctl-cli:v0.150.0 .
```

---

## Usage

### Pull the Image from Docker Hub
To use the pre-built image from Docker Hub, pull it using:
```bash
docker pull anvesh35/eksctl-cli:<version>
```

Example:
```bash
docker pull anvesh35/eksctl-cli:v0.150.0
```

---

### Interactive Shell
Run the container interactively with your kubeconfig mounted for cluster access:
```bash
docker run --rm -it \
  --network host \
  -v $HOME/.kube/config:/home/eksctl/.kube/config:ro \
  anvesh35/eksctl-cli:<version> bash
```

This opens a Bash shell with the eksctl CLI installed and ready to use.

---

### One-Off eksctl Commands
Run eksctl commands directly without entering the container:
```bash
docker run --rm \
  --network host \
  -v $HOME/.kube/config:/home/eksctl/.kube/config:ro \
  anvesh35/eksctl-cli:<version> \
  eksctl get cluster
```

---

## Features

- **Multi-Stage Build**: Downloads and verifies the eksctl CLI binary in a builder stage, then copies only the necessary files into the final image.
- **Minimal Alpine Base**: Uses Alpine Linux to keep the image size small (~9 MB).
- **Non-Root User**: Runs as a dedicated `eksctl` user to adhere to container security best practices.
- **Version-Pinned Binaries**: Ensures reproducible environments by using explicit semantic versions.
- **Flexible Tagging**: Supports version-specific tags (e.g., `v0.150.0`).

---

## Example Commands

### Check eksctl Version
```bash
docker run --rm \
  anvesh35/eksctl-cli:v0.150.0 \
  eksctl version
```

### List All Clusters
```bash
docker run --rm \
  --network host \
  -v $HOME/.kube/config:/home/eksctl/.kube/config:ro \
  anvesh35/eksctl-cli:v0.150.0 \
  eksctl get cluster
```

---

## Contributing

Contributions are welcome via GitHub pull requests. Please follow multi-stage build patterns, use semantic versioning for new tool images, and adhere to lowercase, hyphenated naming conventions.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.