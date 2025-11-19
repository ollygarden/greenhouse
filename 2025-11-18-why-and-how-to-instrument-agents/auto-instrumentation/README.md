# Auto-instrumentation

## Files

- [`main.py`](main.py) — Basic agent loop
- [`tools.py`](tools.py) — File system tools (read, grep, list)
- [`cli.py`](cli.py) — Model selection
- [`utils.py`](utils.py) — Tool execution helpers

## Run

```bash
pip install -r requirements.txt
cp .env.example .env  # Configure environment variables
dotenv run -- opentelemetry-instrument python main.py
```
