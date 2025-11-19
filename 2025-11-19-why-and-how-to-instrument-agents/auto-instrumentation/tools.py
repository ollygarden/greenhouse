import subprocess
import os


def read_file(file_path: str) -> str:
    """Actual implementation of the read tool."""
    with open(file_path, "r") as f:
        return f.read()


def grep(pattern: str, path: str = ".") -> str:
    """Actual implementation of the grep tool using ripgrep."""
    result = subprocess.run(["rg", pattern, path], capture_output=True, text=True)
    return result.stdout if result.stdout else result.stderr


def list_directory(path: str = ".") -> str:
    """Lists contents of a directory with / suffix for directories."""
    entries = os.listdir(path)
    formatted = []
    for entry in sorted(entries):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            formatted.append(f"{entry}/")
        else:
            formatted.append(entry)
    return "\n".join(formatted)


read_tool = {
    "name": "read",
    "description": "Reads the contents of a file from the filesystem.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The absolute path to the file to read.",
            },
        },
        "required": ["file_path"],
    },
}

grep_tool = {
    "name": "grep",
    "description": "Searches for a pattern in files using ripgrep.",
    "parameters": {
        "type": "object",
        "properties": {
            "pattern": {
                "type": "string",
                "description": "The pattern to search for.",
            },
            "path": {
                "type": "string",
                "description": "The path to search in (file or directory). Defaults to current directory.",
            },
        },
        "required": ["pattern"],
    },
}

list_tool = {
    "name": "list",
    "description": "Lists contents of a directory. Directories are marked with / suffix.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The directory path to list. Defaults to current directory.",
            },
        },
        "required": [],
    },
}
