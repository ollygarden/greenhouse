FROM golang:1.24-alpine AS builder
WORKDIR /app
COPY . .

# Download OCB
ARG OCB_VERSION=0.137.0
RUN wget -qO /usr/bin/builder "https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/cmd%2Fbuilder%2Fv${OCB_VERSION}/ocb_${OCB_VERSION}_linux_amd64" && \
    chmod +x /usr/bin/builder

# Build the distribution
WORKDIR /app/distributions/bonsai
RUN CGO_ENABLED=0 builder --config=manifest.yaml

FROM alpine:latest

ARG USER_UID=10001
USER ${USER_UID}

COPY --from=builder /app/distributions/bonsai/build/bonsai /bonsai
COPY --from=builder /app/distributions/bonsai/config.yaml /etc/bonsai/config.yaml

ENTRYPOINT ["/bonsai"]
CMD ["--config", "/etc/bonsai/config.yaml"]
EXPOSE 4317 4318
