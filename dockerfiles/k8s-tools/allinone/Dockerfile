# Stage 1: Build environment
FROM alpine:3.19 as downloader

# Versions (update these as needed)
ARG KUBECTL_VERSION=1.29.3
ARG HELM_VERSION=3.14.4
ARG VELERO_VERSION=1.12.2
ARG ARGOCD_VERSION=2.8.3
ARG FLUX_VERSION=2.1.0
ARG EKSCTL_VERSION=0.150.0

# Download binaries
RUN apk add --no-cache curl tar gzip bash && \
    mkdir /downloads && \
    # kubectl
    curl -Lo /downloads/kubectl "https://dl.k8s.io/release/v${KUBECTL_VERSION}/bin/linux/amd64/kubectl" && \
    # Helm
    curl -Lo /downloads/helm.tar.gz "https://get.helm.sh/helm-v${HELM_VERSION}-linux-amd64.tar.gz" && \
    # Velero
    curl -Lo /downloads/velero.tar.gz "https://github.com/vmware-tanzu/velero/releases/download/v${VELERO_VERSION}/velero-v${VELERO_VERSION}-linux-amd64.tar.gz" && \
    # ArgoCD
    curl -Lo /downloads/argocd "https://github.com/argoproj/argo-cd/releases/download/v${ARGOCD_VERSION}/argocd-linux-amd64" && \
    # FluxCD (using the official installation script)
    curl -s https://raw.githubusercontent.com/fluxcd/flux2/main/install/flux.sh | FLUX_VERSION=${FLUX_VERSION} bash && \
    mv /usr/local/bin/flux /downloads/flux && \
    # eksctl
    curl -Lo /downloads/eksctl.tar.gz "https://github.com/weaveworks/eksctl/releases/download/v${EKSCTL_VERSION}/eksctl_Linux_amd64.tar.gz"

# Stage 2: Final image
FROM debian:bullseye-slim

# Install required tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates tar gzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy binaries
COPY --from=downloader /downloads /tmp

# Install tools
RUN install -m 0755 /tmp/kubectl /usr/local/bin/kubectl && \
    tar -zxvf /tmp/helm.tar.gz -C /tmp && \
    install -m 0755 /tmp/linux-amd64/helm /usr/local/bin/helm && \
    tar -zxvf /tmp/velero.tar.gz -C /tmp && \
    install -m 0755 /tmp/velero-v*-linux-amd64/velero /usr/local/bin/velero && \
    install -m 0755 /tmp/argocd /usr/local/bin/argocd && \
    install -m 0755 /tmp/flux /usr/local/bin/flux && \
    tar -zxvf /tmp/eksctl.tar.gz -C /tmp && \
    install -m 0755 /tmp/eksctl /usr/local/bin/eksctl && \
    rm -rf /tmp/*

# Set non-root user
RUN useradd -m -s /bin/bash nonroot
USER nonroot

# Default command
CMD ["kubectl", "version", "--client"]