# --- Builder Stage: Download Velero ---
FROM alpine:3.19 AS builder

# Versions (update these as needed)
ARG VELERO_VERSION=v1.11.0

RUN apk add --no-cache curl bash tar gzip
RUN curl -Lo velero.tar.gz \
      "https://github.com/vmware-tanzu/velero/releases/download/${VELERO_VERSION}/velero-${VELERO_VERSION}-linux-amd64.tar.gz" \
    && tar -zxvf velero.tar.gz --strip-components=1 -C /usr/local/bin velero-${VELERO_VERSION}-linux-amd64/velero \
    && chmod +x /usr/local/bin/velero

# --- Final Stage: Runtime Image ---
FROM alpine:3.19

# 1. Create non-root user
RUN addgroup -S velero && adduser -S velero -G velero

# 2. Copy Velero binary and install bash
COPY --from=builder /usr/local/bin/velero /usr/local/bin/velero
RUN chown velero:velero /usr/local/bin/velero \
 && apk add --no-cache bash

# 3. Metadata and working directory
LABEL maintainer="Anvesh Muppeda" \
      version="${VELERO_VERSION}" \
      description="Interactive Velero + bash shell"
WORKDIR /home/velero

# 4. Drop privileges
USER velero

# 5. Entry into bash by default; arguments forwarded for Velero
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["velero version"]