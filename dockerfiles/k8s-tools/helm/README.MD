# **K8s Tools Docker Images - Helm**  

*Lightweight, Versioned Helm CLI Container for Seamless Kubernetes Management*

---

## Summary

This repository provides a Docker image under the `anvesh35/helm-cli` namespace that packages the Helm CLI into a lightweight, self-contained container. This allows users to manage Kubernetes clusters without installing Helm locally. The image is built using a multi-stage build process on Alpine Linux, ensuring a minimal footprint and secure execution.

---

## Image Naming Convention

All images are hosted on Docker Hub under the `anvesh35/helm-cli` repository.  
Tags follow the pattern `<version>`, for example `v3.12.3`, to indicate the Helm version included in the image.

---

## Build Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/anveshmuppeda/kubernetes.git
cd dockerfiles/k8s-tools/helm
```

### 2. Build the Image
Replace `<version>` with the desired Helm version (e.g., `v3.12.3`):
```bash
docker build \
  --build-arg HELM_VERSION=<version> \
  -t anvesh35/helm-cli:<version> .
```

Example:
```bash
docker build \
  --build-arg HELM_VERSION=v3.12.3 \
  -t anvesh35/helm-cli:v3.12.3 .
```

---

## Usage

### Pull the Image from Docker Hub
To use the pre-built image from Docker Hub, pull it using:
```bash
docker pull anvesh35/helm-cli:<version>
```

Example:
```bash
docker pull anvesh35/helm-cli:v3.12.3
```

---

### Interactive Shell
Run the container interactively with your kubeconfig mounted for cluster access:
```bash
docker run --rm -it \
  --network host \
  -v $HOME/.kube/config:/home/helm/.kube/config:ro \
  anvesh35/helm-cli:<version> bash
```

This opens a Bash shell with Helm installed and ready to use.

---

### One-Off Helm Commands
Run Helm commands directly without entering the container:
```bash
docker run --rm \
  --network host \
  -v $HOME/.kube/config:/home/helm/.kube/config:ro \
  anvesh35/helm-cli:<version> \
  helm ls
```

### Interactive Shell with TTY
```bash
docker run --rm -it \
  --network host \
  -v $HOME/.kube/config:/home/helm/.kube/config:ro \
  anvesh35/helm-cli:<version> bash
```
This opens a TTY session with Helm installed and ready to use.

---

## Features

- **Multi-Stage Build**: Downloads and verifies the Helm binary in a builder stage, then copies only the necessary files into the final image.
- **Minimal Alpine Base**: Uses Alpine Linux to keep the image size small (~9 MB).
- **Non-Root User**: Runs as a dedicated `helm` user to adhere to container security best practices.
- **Version-Pinned Binaries**: Ensures reproducible environments by using explicit semantic versions.
- **Flexible Tagging**: Supports version-specific tags (e.g., `v3.12.3`).

---

## Example Commands

### Check Helm Version
```bash
docker run --rm \
  anvesh35/helm-cli:v3.12.3 \
  helm version
```

### List All Helm Releases
```bash
docker run --rm \
  --network host \
  -v $HOME/.kube/config:/home/helm/.kube/config:ro \
  anvesh35/helm-cli:v3.12.3 \
  helm ls -A
```

---

## Contributing

Contributions are welcome via GitHub pull requests. Please follow multi-stage build patterns, use semantic versioning for new tool images, and adhere to lowercase, hyphenated naming conventions.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.