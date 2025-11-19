from typing import Callable, Dict

from google import genai
from google.genai import types
from cli import get_model
from tools import read_file, read_tool, grep, grep_tool, list_directory, list_tool
from utils import get_function_calls, execute_tool
from agent import (
    start_agent, start_llm_generation, start_tool_execution,
    record_response, record_tool_result, record_error, TokenUsage
)

TOOL_DEFINITIONS: Dict[str, Callable[..., str]] = {
    "read": read_file,
    "grep": grep,
    "list": list_directory,
}

client = genai.Client()
tools = types.Tool(function_declarations=[read_tool, grep_tool, list_tool])
system_prompt = "You are a helpful OpenTelemetry semantic conventions assistant with file system access. Actively use the available tools to explore files, search code, and provide accurate information. Always use tools when the user asks about code or files."
config = types.GenerateContentConfig(
    tools=[tools],
    system_instruction=system_prompt
)

messages = []
model = get_model()

with start_agent("semconv_assistant", provider="google"):
    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            break

        messages.append(types.Content(
            parts=[types.Part(text=user_input)],
            role="user"
        ))

        # Agent processing loop
        while True:
            input_text = "\n".join([
                msg.parts[0].text for msg in messages
                if msg.parts and getattr(msg.parts[0], 'text', None)
            ])

            with start_llm_generation(model, input_text) as gen_span:
                try:
                    response = client.models.generate_content(
                        model=model,
                        contents=messages,
                        config=config
                    )

                    usage_meta = response.usage_metadata
                    token_usage = TokenUsage(
                        input_tokens=usage_meta.prompt_token_count,
                        output_tokens=usage_meta.candidates_token_count,
                        total_tokens=usage_meta.total_token_count,
                        cached_tokens=getattr(usage_meta, 'cached_content_token_count', 0) or 0
                    )

                    # Check if model wants to use tools
                    function_calls = get_function_calls(response)

                    record_response(
                        gen_span,
                        token_usage=token_usage,
                        response_model=model,
                        finish_reasons=[c.finish_reason.name for c in response.candidates],
                        output_text=response.text if not function_calls else None
                    )

                    if function_calls:
                        messages.append(response.candidates[0].content)

                        for fc in function_calls:
                            with start_tool_execution(fc.name, fc.args) as tool_span:
                                try:
                                    result = execute_tool(fc.name, fc.args, TOOL_DEFINITIONS)
                                    record_tool_result(tool_span, result)
                                except Exception as e:
                                    record_error(tool_span, e)
                                    result = f"Error: {str(e)}"

                            messages.append(types.Content(
                                parts=[types.Part(function_response=types.FunctionResponse(
                                    name=fc.name,
                                    response={"result": result}
                                ))]
                            ))

                except Exception as e:
                    record_error(gen_span, e)
                    raise

            if not function_calls:
                print(f"\nAssistant: {response.text}\n")
                messages.append(response.candidates[0].content)
                break
