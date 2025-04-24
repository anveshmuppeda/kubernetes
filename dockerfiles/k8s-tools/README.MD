# **K8s Tools Docker Images**  
*Lightweight, Versioned Kubernetes CLI Containers for Seamless Cluster Management*  

## Summary  
This repository provides Docker images under the `anvesh35/k8s-tools` namespace that package Kubernetes CLI tools—including `kubectl`, `helm`, `velero`, and `flux`—into lightweight, self-contained containers so users can manage clusters without installing binaries locally. Each image employs a multi-stage build on Alpine Linux, runs as a non-root user, and includes only the necessary binaries to keep the footprint minimal (~9 MB) and secure.

## Introduction  
Users often need different versions of Kubernetes tools across projects, leading to local dependency conflicts and manual installations.  
This repository solves that by offering pre-built Docker images for each CLI, letting you simply `docker run` to enter a shell with your tool of choice ready to use.  

## Image Naming Convention  
All images live in the `anvesh35/k8s-tools` Docker Hub repository .  
Tags follow the pattern `<toolname>-<version>`, for example `kubectl-1.29.3`, using lowercase letters and hyphens to comply with Docker naming rules.  
An optional `allinone-latest` tag bundles multiple CLIs into a single image for quick setups.  

## Build Instructions  
1. **Clone the repo**  
   ```bash
   git clone https://github.com/anveshmuppeda/kubernetes.git
   cd dockerfiles/k8s-tools/<toolname>
   ```  
2. **Build the image**  
   ex: kubectl  
   ```bash
   docker build \
     --build-arg KUBECTL_VERSION=v1.29.3 \
     -t anvesh35/k8s-tools:kubectl-1.29.3 .
   ```  

## Usage  

### Interactive Shell  
```bash
docker run --rm -it \
  --network host \
  -v $HOME/.kube/config:/home/kube/.kube/config:ro \
  anvesh35/k8s-tools:kubectl-1.29.3
```  
This opens a Bash shell in `/home/kube` with the specified CLI in your `PATH`

### One-Off Commands  
```bash
docker run --rm \
  --network host \
  -v $HOME/.kube/config:/home/kube/.kube/config:ro \
  anvesh35/k8s-tools:kubectl-1.29.3 \
  kubectl get pods
```  
Mounting your kubeconfig read-only ensures safe cluster access without local installations .

## Features  
- **Multi-Stage Builds**: Downloads and verifies each CLI binary in a builder stage, then copies only the needed files into the final image.
- **Minimal Alpine Base**: Uses Alpine Linux to keep image sizes small (~9 MB). 
- **Non-Root User**: Runs as a dedicated `kube` user to adhere to container security best practices.
- **Version-Pinned Binaries**: Ensures reproducible environments and avoids “latest” ambiguities by using explicit semantic versions .  
- **Flexible Tagging**: Supports both per-tool tags (`kubectl-1.29.3`) and an `allinone-latest` aggregate image.

## Contributing  
Contributions are welcome via GitHub pull requests. Please follow multi-stage build patterns, use semantic versioning for new tool images, and adhere to lowercase, hyphenated naming conventions.