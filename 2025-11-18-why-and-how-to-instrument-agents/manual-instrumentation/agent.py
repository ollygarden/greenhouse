from typing import Optional, Dict, Any
from contextlib import contextmanager
from dataclasses import dataclass
import os
from opentelemetry.trace import Span, StatusCode, SpanKind
from otel import tracer


def should_capture_content() -> bool:
    """Check if message content should be captured based on environment variable."""
    return (
        os.getenv("OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT", "false").lower()
        == "true"
    )


@contextmanager
def start_agent(
    agent_name: str = "agent",
    provider: str = "google",
    custom_attributes: Optional[Dict[str, str]] = None,
):
    """Creates a span for agent interactions."""
    operation_name = "invoke_agent"
    with tracer.start_as_current_span(
        f"{operation_name} {agent_name}", kind=SpanKind.INTERNAL
    ) as span:
        span.set_attribute("gen_ai.operation.name", operation_name)
        span.set_attribute("gen_ai.provider.name", provider)

        if custom_attributes:
            for k, v in custom_attributes.items():
                span.set_attribute(k, v)

        yield span


@contextmanager
def start_llm_generation(
    model_name: str, input_text: str, custom_attributes: Optional[Dict[str, str]] = None
):
    """Creates a span for LLM generation."""
    operation_name = "generate_content"
    with tracer.start_as_current_span(
        f"{operation_name} {model_name}", kind=SpanKind.CLIENT
    ) as span:
        # Mandatory attributes
        if should_capture_content():
            span.set_attribute("gen_ai.input.messages", input_text)
        span.set_attribute("gen_ai.operation.name", operation_name)
        span.set_attribute("gen_ai.provider.name", "google")
        span.set_attribute("gen_ai.model.name", model_name)

        # Custom attributes if provided
        if custom_attributes:
            for k, v in custom_attributes.items():
                span.set_attribute(k, v)

        yield span


@contextmanager
def start_tool_execution(
    tool_name: str,
    tool_args: Optional[Dict[str, Any]] = None,
    custom_attributes: Optional[Dict[str, str]] = None,
):
    """Creates a span for tool execution."""
    operation_name = "execute_tool"
    with tracer.start_as_current_span(
        f"{operation_name} {tool_name}", kind=SpanKind.INTERNAL
    ) as span:
        span.set_attribute("gen_ai.operation.name", operation_name)
        span.set_attribute("gen_ai.tool.name", tool_name)

        # Add input if provided
        if should_capture_content() and tool_args:
            span.set_attribute("gen_ai.tool.call.arguments", str(tool_args))

        # Custom attributes if provided
        if custom_attributes:
            for k, v in custom_attributes.items():
                span.set_attribute(k, v)

        yield span


@dataclass
class TokenUsage:
    """Token usage tracking for cost monitoring."""

    # Billable
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = (
        0  # contains tool, thinking, system prompt, etc. (not cached tokens)
    )

    # Non Billable
    cached_tokens: int = (
        0  # tokens that were cached from the model - not counted towards cost
    )


def record_token_usage(span: Span, token_usage: TokenUsage) -> None:
    """Records token usage for the span to monitor costs."""
    if (
        token_usage.input_tokens == 0
        and token_usage.output_tokens == 0
        and token_usage.total_tokens == 0
    ):
        return

    # Standard semconv attributes
    if token_usage.input_tokens > 0:
        span.set_attribute("gen_ai.usage.input_tokens", token_usage.input_tokens)
    if token_usage.output_tokens > 0:
        span.set_attribute("gen_ai.usage.output_tokens", token_usage.output_tokens)

    # Non-standard but useful attributes
    if token_usage.total_tokens > 0:
        span.set_attribute("gen_ai.usage.total_tokens", token_usage.total_tokens)
    if token_usage.cached_tokens > 0:
        span.set_attribute("gen_ai.usage.cached_tokens", token_usage.cached_tokens)


def record_warning(
    span: Span, warning: str, token_usage: Optional[TokenUsage] = None
) -> None:
    """Records a warning in the span. Use for tool calls that might fail but get retried."""
    # No "warning" status in OTel, so we use custom attribute
    span.set_attribute("observation.level", "WARNING")
    span.set_attribute("observation.status_message", warning)

    if token_usage:
        record_token_usage(span, token_usage)


def record_error(
    span: Span, error: Exception, token_usage: Optional[TokenUsage] = None
) -> None:
    """Records an error in the span with proper attributes."""
    span.record_exception(error)
    span.set_status(StatusCode.ERROR, str(error))
    span.set_attribute("error.type", type(error).__name__)

    if token_usage:
        record_token_usage(span, token_usage)


def record_response(
    span: Span,
    token_usage: Optional[TokenUsage] = None,
    response_model: Optional[str] = None,
    response_id: Optional[str] = None,
    finish_reasons: Optional[list[str]] = None,
    output_text: Optional[str] = None,
) -> None:
    """Records LLM response metadata including token usage, model info, and output."""
    # Token usage
    if token_usage:
        record_token_usage(span, token_usage)

    # Response metadata
    if response_model:
        span.set_attribute("gen_ai.response.model", response_model)
    if response_id:
        span.set_attribute("gen_ai.response.id", response_id)
    if finish_reasons:
        span.set_attribute("gen_ai.response.finish_reasons", finish_reasons)

    # Output content (conditional on environment variable)
    if output_text and should_capture_content():
        span.set_attribute("gen_ai.output.messages", output_text)


def record_tool_result(span: Span, result: str) -> None:
    """Records tool execution result (conditional on environment variable)."""
    if should_capture_content():
        span.set_attribute("gen_ai.tool.call.result", result)
