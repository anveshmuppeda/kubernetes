# --- Builder Stage: Download eksctl CLI ---
FROM alpine:3.19 AS builder

# Versions (update these as needed)
ARG EKSCTL_VERSION=v0.150.0

RUN apk add --no-cache curl bash
RUN curl -Lo /usr/local/bin/eksctl \
      "https://github.com/weaveworks/eksctl/releases/download/${EKSCTL_VERSION}/eksctl_Linux_amd64.tar.gz" \
    && tar -zxvf /usr/local/bin/eksctl -C /usr/local/bin \
    && chmod +x /usr/local/bin/eksctl

# --- Final Stage: Runtime Image ---
FROM alpine:3.19

# 1. Create non-root user
RUN addgroup -S eksctl && adduser -S eksctl -G eksctl

# 2. Copy eksctl binary and install bash
COPY --from=builder /usr/local/bin/eksctl /usr/local/bin/eksctl
RUN chown eksctl:eksctl /usr/local/bin/eksctl \
 && apk add --no-cache bash

# 3. Metadata and working directory
LABEL maintainer="Anvesh Muppeda" \
      version="${EKSCTL_VERSION}" \
      description="Interactive eksctl CLI + bash shell"
WORKDIR /home/eksctl

# 4. Drop privileges
USER eksctl

# 5. Entry into bash by default; arguments forwarded for eksctl CLI
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["eksctl version"]