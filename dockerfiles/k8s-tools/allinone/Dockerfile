# Stage 1: Build environment
FROM alpine:3.19 as downloader

# Versions (update these as needed)
ARG KUBECTL_VERSION=1.29.3
ARG HELM_VERSION=3.14.4
ARG VELERO_VERSION=1.12.2

# Download binaries
RUN apk add --no-cache curl tar gzip && \
    mkdir /downloads && \
    # kubectl
    curl -LO "https://dl.k8s.io/release/v${KUBECTL_VERSION}/bin/linux/amd64/kubectl" -o /downloads/kubectl && \
    # Helm
    curl -LO "https://get.helm.sh/helm-v${HELM_VERSION}-linux-amd64.tar.gz" -o /downloads/helm.tar.gz && \
    # Velero
    curl -LO "https://github.com/vmware-tanzu/velero/releases/download/v${VELERO_VERSION}/velero-v${VELERO_VERSION}-linux-amd64.tar.gz" -o /downloads/velero.tar.gz

# Stage 2: Final image
FROM gcr.io/distroless/base-debian12:nonroot

# Copy binaries
COPY --from=downloader /downloads /tmp

# Install tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    # Install kubectl
    install -m 0755 /tmp/kubectl /usr/local/bin/kubectl && \
    # Install Helm
    tar -zxvf /tmp/helm.tar.gz -C /tmp && \
    install -m 0755 /tmp/linux-amd64/helm /usr/local/bin/helm && \
    # Install Velero
    tar -zxvf /tmp/velero.tar.gz -C /tmp && \
    install -m 0755 /tmp/velero-v*-linux-amd64/velero /usr/local/bin/velero && \
    # Cleanup
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/*

# Use the nonroot user from base image (uid: 65532, gid: 65532)
USER nonroot:nonroot

# Verify installations
CMD ["kubectl", "version", "--client"]