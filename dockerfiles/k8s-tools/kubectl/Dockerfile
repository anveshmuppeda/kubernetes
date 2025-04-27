# --- Builder Stage: Download kubectl ---
FROM alpine:3.21 AS builder

# Versions (update these as needed)
ARG KUBECTL_VERSION=v1.29.3

RUN apk add --no-cache curl bash
RUN curl -Lo /usr/local/bin/kubectl \
      "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl" \
    && chmod +x /usr/local/bin/kubectl

# --- Final Stage: Runtime Image ---
FROM alpine:3.21

# 1. Create non-root user
RUN addgroup -S kube && adduser -S kube -G kube

# 2. Copy kubectl and install bash
COPY --from=builder /usr/local/bin/kubectl /usr/local/bin/kubectl
RUN chown kube:kube /usr/local/bin/kubectl \
 && apk add --no-cache bash

# 3. Metadata and working directory
LABEL maintainer="Anvesh Muppeda" \
      version="${KUBECTL_VERSION}" \
      description="Interactive kubectl + bash shell"
WORKDIR /home/kube

# 4. Drop privileges
USER kube

# 5. Entry into bash by default; arguments forwarded for kubectl
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["kubectl version --client"]