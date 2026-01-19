# --- Builder Stage: Download FluxCD CLI ---
FROM alpine:3.23 AS builder

# Versions (update these as needed)
ARG FLUX_VERSION=2.1.0

RUN apk add --no-cache curl bash
RUN curl -s https://raw.githubusercontent.com/fluxcd/flux2/main/install/flux.sh | FLUX_VERSION=${FLUX_VERSION} bash

# --- Final Stage: Runtime Image ---
FROM alpine:3.23

# 1. Create non-root user
RUN addgroup -S flux && adduser -S flux -G flux

# 2. Copy FluxCD binary and install bash
COPY --from=builder /usr/local/bin/flux /usr/local/bin/flux
RUN chown flux:flux /usr/local/bin/flux \
 && apk add --no-cache bash

# 3. Metadata and working directory
LABEL maintainer="Anvesh Muppeda" \
      version="${FLUX_VERSION}" \
      description="Interactive FluxCD CLI + bash shell"
WORKDIR /home/flux

# 4. Drop privileges
USER flux

# 5. Entry into bash by default; arguments forwarded for FluxCD CLI
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["flux version"]