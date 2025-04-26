# **K8s Tools Docker Images - All-in-One**

*Lightweight, Combined CLI Container for Seamless Kubernetes Management*

---

## Summary

This repository provides a Docker image under the `anvesh35/k8s-tools` namespace that packages multiple Kubernetes CLI tools into a single, lightweight, self-contained container. This allows users to manage Kubernetes clusters and workflows without installing these tools locally. The image is built using a multi-stage build process on Alpine Linux and Debian Slim, ensuring a minimal footprint and secure execution.

---

## Included Tools

The following CLI tools are included in this image:

- **kubectl**: Kubernetes command-line tool for managing clusters.
- **Helm**: Kubernetes package manager.
- **Velero**: Backup and restore tool for Kubernetes.
- **ArgoCD**: Continuous delivery tool for Kubernetes.
- **FluxCD**: GitOps tool for Kubernetes.
- **eksctl**: CLI for Amazon EKS cluster management.

---

## Image Naming Convention

All images are hosted on Docker Hub under the `anvesh35/k8s-tools` repository.  
Tags follow the pattern `allinone:<version>` to indicate the combined tools version.

---

## Build Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/anveshmuppeda/kubernetes.git
cd dockerfiles/k8s-tools/allinone
```

### 2. Build the Image
Replace the versions as needed for the CLI tools:
```bash
docker build \
  --build-arg KUBECTL_VERSION=<kubectl_version> \
  --build-arg HELM_VERSION=<helm_version> \
  --build-arg VELERO_VERSION=<velero_version> \
  --build-arg ARGOCD_VERSION=<argocd_version> \
  --build-arg FLUX_VERSION=<flux_version> \
  --build-arg EKSCTL_VERSION=<eksctl_version> \
  -t anvesh35/k8s-tools:allinone .
```

Example:
```bash
docker build \
  --build-arg KUBECTL_VERSION=1.29.3 \
  --build-arg HELM_VERSION=3.14.4 \
  --build-arg VELERO_VERSION=1.12.2 \
  --build-arg ARGOCD_VERSION=2.8.3 \
  --build-arg FLUX_VERSION=2.1.0 \
  --build-arg EKSCTL_VERSION=0.150.0 \
  -t anvesh35/k8s-tools:allinone .
```

---

## Usage

### Pull the Image from Docker Hub
To use the pre-built image from Docker Hub, pull it using:
```bash
docker pull anvesh35/k8s-tools:allinone
```

---

### Interactive Shell
Run the container interactively with your kubeconfig mounted for cluster access:
```bash
docker run --rm -it \
  --network host \
  -v $HOME/.kube/config:/home/nonroot/.kube/config:ro \
  anvesh35/k8s-tools:allinone bash
```

This opens a Bash shell with all the CLI tools installed and ready to use.

---

### One-Off Commands
Run commands directly without entering the container:

#### kubectl
```bash
docker run --rm \
  -v $HOME/.kube/config:/home/nonroot/.kube/config:ro \
  anvesh35/k8s-tools:allinone \
  kubectl get nodes
```

#### Helm
```bash
docker run --rm \
  anvesh35/k8s-tools:allinone \
  helm version
```

#### Velero
```bash
docker run --rm \
  anvesh35/k8s-tools:allinone \
  velero version
```

#### ArgoCD
```bash
docker run --rm \
  anvesh35/k8s-tools:allinone \
  argocd version
```

#### FluxCD
```bash
docker run --rm \
  anvesh35/k8s-tools:allinone \
  flux version
```

#### eksctl
```bash
docker run --rm \
  anvesh35/k8s-tools:allinone \
  eksctl version
```

---

## Features

- **Multi-Stage Build**: Downloads and verifies all CLI binaries in a builder stage, then copies only the necessary files into the final image.
- **Minimal Debian Slim Base**: Uses Debian Slim to keep the image size small while providing essential tools.
- **Non-Root User**: Runs as a dedicated `nonroot` user to adhere to container security best practices.
- **Version-Pinned Binaries**: Ensures reproducible environments by using explicit semantic versions.
- **Flexible Tagging**: Supports version-specific tags for the combined tools.

---

## Example Commands

### Check All Tool Versions
```bash
docker run --rm anvesh35/k8s-tools:allinone kubectl version --client
docker run --rm anvesh35/k8s-tools:allinone helm version
docker run --rm anvesh35/k8s-tools:allinone velero version
docker run --rm anvesh35/k8s-tools:allinone argocd version
docker run --rm anvesh35/k8s-tools:allinone flux version
docker run --rm anvesh35/k8s-tools:allinone eksctl version
```

---

## Contributing

Contributions are welcome via GitHub pull requests. Please follow multi-stage build patterns, use semantic versioning for new tool images, and adhere to lowercase, hyphenated naming conventions.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.