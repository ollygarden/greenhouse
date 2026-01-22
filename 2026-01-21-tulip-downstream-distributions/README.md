# Tulip: Creating Downstream Distributions

Live session demonstrating how to create downstream OpenTelemetry Collector distributions using Tulip.

## What you'll learn

- What Tulip is and how it enables downstream distributions
- How to create a custom collector distribution
- Adding components beyond the base distribution
- Running and testing your distribution in production-like environments

## Bonsai: Example Downstream Distribution

**Bonsai** is a demo OpenTelemetry Collector distribution that extends Tulip with additional components. It demonstrates how organizations can create their own distributions tailored to their needs.

| Directory | Description |
|-----------|-------------|
| [**distributions/bonsai**](distributions/bonsai) | Collector manifest and configuration |

### Components

- **Base**: Tulip 25.11 (based on OTel Collector 0.137.0)
- **Extensions**: Adds `hostmetrics` receiver to demonstrate extensibility

See [distributions/bonsai/manifest.yaml](distributions/bonsai/manifest.yaml) for the full component list.

## Prerequisites

- Docker & Docker Compose
- (Optional) Go 1.24+ for local building

## Running the Demo

Start the entire environment:

```bash
docker-compose up
```

This starts:
1. **Bonsai Collector**: Ports 4317 (gRPC) and 4318 (HTTP)
2. **LGTM**: Grafana/Loki/Tempo stack (UI on port 3000)
3. **Telemetrygen**: Sends synthetic trace data
4. **PostgreSQL**: Database on port 5432

### Explore Data

Access Grafana at **http://localhost:3000**

- **Traces**: Explore -> Tempo datasource
- **Metrics**: Explore -> Prometheus datasource, query `system.cpu.time`

## Local Development

Build the collector binary locally:

```bash
make build
```

## License

Apache-2.0
