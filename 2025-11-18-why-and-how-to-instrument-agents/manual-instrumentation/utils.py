from typing import List, Dict, Any, Callable
from google.genai import types


def get_function_calls(
    response: types.GenerateContentResponse,
) -> List[types.FunctionCall]:
    """Extract all function calls from the response."""
    function_calls: List[types.FunctionCall] = []
    for part in response.candidates[0].content.parts:
        if part.function_call:
            function_calls.append(part.function_call)
    return function_calls


def execute_tool(
    name: str, args: Dict[str, Any], tool_definitions: Dict[str, Callable[..., str]]
) -> str:
    """Generic tool executor that dispatches to the correct function."""
    try:
        if name not in tool_definitions:
            return f"Error: Unknown tool '{name}'"
        return tool_definitions[name](**args)
    except Exception as e:
        return f"Error executing {name}: {type(e).__name__}: {str(e)}"
