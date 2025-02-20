# Use a minimal Debian-based image
FROM debian:stable-slim

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    ca-certificates \
    && apt-get clean

# Set architecture variables
ARG ARCH
ENV ARCH=${ARCH:-amd64}

# Manually fetch latest stable kubectl version (workaround for curl issue)
RUN KUBECTL_VERSION=$(curl -sL https://dl.k8s.io/release/stable.txt) && \
    curl -LO "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${ARCH}/kubectl" && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/

# Verify installation
RUN kubectl version --client && curl --version && jq --version

# Set default entrypoint
ENTRYPOINT ["/bin/sh"]

