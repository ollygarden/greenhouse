from typing import Callable, Dict

from google import genai
from google.genai import types
from cli import get_model
from tools import read_file, read_tool, grep, grep_tool, list_directory, list_tool
from utils import get_function_calls, execute_tool

TOOL_DEFINITIONS: Dict[str, Callable[..., str]] = {
    "read": read_file,
    "grep": grep,
    "list": list_directory,
}

client = genai.Client()
tools = types.Tool(function_declarations=[read_tool, grep_tool, list_tool])
system_prompt = (
    "You are a helpful OpenTelemetry semantic conventions assistant with file system "
    "access. Actively use the available tools to explore files, search code, and provide "
    "accurate information. Always use tools when the user asks about code or files."
)
config = types.GenerateContentConfig(tools=[tools], system_instruction=system_prompt)

messages = []
model = get_model()

while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() in ["exit", "quit"]:
        break

    messages.append(types.Content(parts=[types.Part(text=user_input)], role="user"))

    # Agent processing loop
    while True:
        response = client.models.generate_content(
            model=model, contents=messages, config=config
        )

        # Check if model wants to use tools
        function_calls = get_function_calls(response)

        if function_calls:
            messages.append(response.candidates[0].content)

            for fc in function_calls:
                try:
                    result = execute_tool(fc.name, fc.args, TOOL_DEFINITIONS)
                except Exception as e:
                    result = f"Error: {str(e)}"

                messages.append(
                    types.Content(
                        parts=[
                            types.Part(
                                function_response=types.FunctionResponse(
                                    name=fc.name, response={"result": result}
                                )
                            )
                        ]
                    )
                )

        if not function_calls:
            print(f"\nAssistant: {response.text}\n")
            messages.append(response.candidates[0].content)
            break
