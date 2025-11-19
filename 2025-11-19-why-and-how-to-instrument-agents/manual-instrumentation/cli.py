import argparse

MODEL_MAP = {
    "flash-lite": "gemini-2.5-flash-lite",
    "flash": "gemini-2.5-flash",
    "pro": "gemini-2.5-pro",
}


def get_model() -> str:
    parser = argparse.ArgumentParser(description="AI Agent CLI")
    parser.add_argument(
        "model",
        nargs="?",
        choices=["flash-lite", "flash", "pro"],
        default="flash",
        help="Model to use (default: flash)",
    )
    args = parser.parse_args()
    return MODEL_MAP[args.model]
