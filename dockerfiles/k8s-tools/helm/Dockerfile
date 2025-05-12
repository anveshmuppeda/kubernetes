# --- Builder Stage: Download Helm ---
FROM alpine:3.21 AS builder

# Versions (update these as needed)
ARG HELM_VERSION=v3.12.3

RUN apk add --no-cache curl bash tar gzip
RUN curl -Lo helm.tar.gz \
      "https://get.helm.sh/helm-${HELM_VERSION}-linux-amd64.tar.gz" \
    && tar -zxvf helm.tar.gz --strip-components=1 -C /usr/local/bin linux-amd64/helm \
    && chmod +x /usr/local/bin/helm

# --- Final Stage: Runtime Image ---
FROM alpine:3.21

# 1. Create non-root user
RUN addgroup -S helm && adduser -S helm -G helm

# 2. Copy Helm binary and install bash
COPY --from=builder /usr/local/bin/helm /usr/local/bin/helm
RUN chown helm:helm /usr/local/bin/helm \
 && apk add --no-cache bash

# 3. Metadata and working directory
LABEL maintainer="Anvesh Muppeda" \
      version="${HELM_VERSION}" \
      description="Interactive Helm + bash shell"
WORKDIR /home/helm

# 4. Drop privileges
USER helm

# 5. Entry into bash by default; arguments forwarded for Helm
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["helm version"]