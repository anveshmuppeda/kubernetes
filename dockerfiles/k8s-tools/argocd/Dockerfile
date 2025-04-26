# --- Builder Stage: Download ArgoCD CLI ---
FROM alpine:3.19 AS builder

# Versions (update these as needed)
ARG ARGOCD_VERSION=v2.8.3

RUN apk add --no-cache curl bash tar gzip
RUN curl -Lo /usr/local/bin/argocd \
      "https://github.com/argoproj/argo-cd/releases/download/${ARGOCD_VERSION}/argocd-linux-amd64" \
    && chmod +x /usr/local/bin/argocd

# --- Final Stage: Runtime Image ---
FROM alpine:3.19

# 1. Create non-root user
RUN addgroup -S argocd && adduser -S argocd -G argocd

# 2. Copy ArgoCD binary and install bash
COPY --from=builder /usr/local/bin/argocd /usr/local/bin/argocd
RUN chown argocd:argocd /usr/local/bin/argocd \
 && apk add --no-cache bash

# 3. Metadata and working directory
LABEL maintainer="Anvesh Muppeda" \
      version="${ARGOCD_VERSION}" \
      description="Interactive ArgoCD CLI + bash shell"
WORKDIR /home/argocd

# 4. Drop privileges
USER argocd

# 5. Entry into bash by default; arguments forwarded for ArgoCD CLI
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["argocd version"]