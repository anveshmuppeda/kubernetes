# **K8s Tools Docker Images - Velero**

*Lightweight, Versioned Velero CLI Container for Seamless Kubernetes Backup and Restore Management*

---

## Summary

This repository provides a Docker image under the `anvesh35/velero-cli` namespace that packages the Velero CLI into a lightweight, self-contained container. This allows users to manage Kubernetes backups and restores without installing Velero locally. The image is built using a multi-stage build process on Alpine Linux, ensuring a minimal footprint and secure execution.

---

## Image Naming Convention

All images are hosted on Docker Hub under the `anvesh35/velero-cli` repository.  
Tags follow the pattern `<version>`, for example `v1.11.0`, to indicate the Velero version included in the image.

---

## Build Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/anveshmuppeda/kubernetes.git
cd dockerfiles/k8s-tools/velero
```

### 2. Build the Image
Replace `<version>` with the desired Velero version (e.g., `v1.11.0`):
```bash
docker build \
  --build-arg VELERO_VERSION=<version> \
  -t anvesh35/velero-cli:<version> .
```

Example:
```bash
docker build \
  --build-arg VELERO_VERSION=v1.11.0 \
  -t anvesh35/velero-cli:v1.11.0 .
```

---

## Usage

### Pull the Image from Docker Hub
To use the pre-built image from Docker Hub, pull it using:
```bash
docker pull anvesh35/velero-cli:<version>
```

Example:
```bash
docker pull anvesh35/velero-cli:v1.11.0
```

---

### Interactive Shell
Run the container interactively with your kubeconfig mounted for cluster access:
```bash
docker run --rm -it \
  --network host \
  -v $HOME/.kube/config:/home/velero/.kube/config:ro \
  anvesh35/velero-cli:<version> bash
```

This opens a Bash shell with Velero installed and ready to use.

---

### One-Off Velero Commands
Run Velero commands directly without entering the container:
```bash
docker run --rm \
  --network host \
  -v $HOME/.kube/config:/home/velero/.kube/config:ro \
  anvesh35/velero-cli:<version> \
  velero backup get
```

---

## Features

- **Multi-Stage Build**: Downloads and verifies the Velero binary in a builder stage, then copies only the necessary files into the final image.
- **Minimal Alpine Base**: Uses Alpine Linux to keep the image size small (~9 MB).
- **Non-Root User**: Runs as a dedicated `velero` user to adhere to container security best practices.
- **Version-Pinned Binaries**: Ensures reproducible environments by using explicit semantic versions.
- **Flexible Tagging**: Supports version-specific tags (e.g., `v1.11.0`).

---

## Example Commands

### Check Velero Version
```bash
docker run --rm \
  anvesh35/velero-cli:v1.11.0 \
  velero version
```

### List All Backups
```bash
docker run --rm \
  --network host \
  -v $HOME/.kube/config:/home/velero/.kube/config:ro \
  anvesh35/velero-cli:v1.11.0 \
  velero backup get
```

---

## Contributing

Contributions are welcome via GitHub pull requests. Please follow multi-stage build patterns, use semantic versioning for new tool images, and adhere to lowercase, hyphenated naming conventions.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.