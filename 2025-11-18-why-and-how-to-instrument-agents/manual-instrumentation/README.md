# Manual Instrumentation

## Files

- [`main.py`](main.py) — Instrumented agent loop
- [`agent.py`](agent.py) — Span helpers & telemetry recording
- [`otel.py`](otel.py) — OTLP exporter setup
- [`tools.py`](tools.py) — File system tools
- [`cli.py`](cli.py) — Model selection
- [`utils.py`](utils.py) — Tool execution

## Run

```bash
pip install -r requirements.txt
cp .env.example .env.local  # Configure environment variables
source .env.local
python main.py
```