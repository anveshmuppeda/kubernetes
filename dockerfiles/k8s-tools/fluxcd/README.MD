# **K8s Tools Docker Images - FluxCD**

*Lightweight, Versioned FluxCD CLI Container for Seamless Kubernetes GitOps Management*

---

## Summary

This repository provides a Docker image under the `anvesh35/fluxcd-cli` namespace that packages the FluxCD CLI into a lightweight, self-contained container. This allows users to manage FluxCD GitOps workflows without installing the Flux CLI locally. The image is built using a multi-stage build process on Alpine Linux, ensuring a minimal footprint and secure execution.

---

## Image Naming Convention

All images are hosted on Docker Hub under the `anvesh35/fluxcd-cli` repository.  
Tags follow the pattern `<version>`, for example `v2.1.0`, to indicate the FluxCD CLI version included in the image.

---

## Build Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/anveshmuppeda/kubernetes.git
cd dockerfiles/k8s-tools/fluxcd
```

### 2. Build the Image
Replace `<version>` with the desired FluxCD CLI version (e.g., `2.1.0`):
```bash
docker build \
  --build-arg FLUX_VERSION=<version> \
  -t anvesh35/fluxcd-cli:<version> .
```

Example:
```bash
docker build \
  --build-arg FLUX_VERSION=2.1.0 \
  -t anvesh35/fluxcd-cli:v2.1.0 .
```

---

## Usage

### Pull the Image from Docker Hub
To use the pre-built image from Docker Hub, pull it using:
```bash
docker pull anvesh35/fluxcd-cli:<version>
```

Example:
```bash
docker pull anvesh35/fluxcd-cli:v2.1.0
```

---

### Interactive Shell
Run the container interactively with your kubeconfig mounted for cluster access:
```bash
docker run --rm -it \
  --network host \
  -v $HOME/.kube/config:/home/flux/.kube/config:ro \
  anvesh35/fluxcd-cli:<version> bash
```

This opens a Bash shell with the FluxCD CLI installed and ready to use.

---

### One-Off FluxCD Commands
Run FluxCD commands directly without entering the container:
```bash
docker run --rm \
  --network host \
  -v $HOME/.kube/config:/home/flux/.kube/config:ro \
  anvesh35/fluxcd-cli:<version> \
  flux check --pre
```

---

## Features

- **Multi-Stage Build**: Downloads and verifies the FluxCD CLI binary in a builder stage, then copies only the necessary files into the final image.
- **Minimal Alpine Base**: Uses Alpine Linux to keep the image size small (~9 MB).
- **Non-Root User**: Runs as a dedicated `flux` user to adhere to container security best practices.
- **Version-Pinned Binaries**: Ensures reproducible environments by using explicit semantic versions.
- **Flexible Tagging**: Supports version-specific tags (e.g., `v2.1.0`).

---

## Example Commands

### Check FluxCD Version
```bash
docker run --rm \
  anvesh35/fluxcd-cli:v2.1.0 \
  flux version
```

### Pre-Flight Checks
```bash
docker run --rm \
  --network host \
  -v $HOME/.kube/config:/home/flux/.kube/config:ro \
  anvesh35/fluxcd-cli:v2.1.0 \
  flux check --pre
```

---

## Contributing

Contributions are welcome via GitHub pull requests. Please follow multi-stage build patterns, use semantic versioning for new tool images, and adhere to lowercase, hyphenated naming conventions.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.