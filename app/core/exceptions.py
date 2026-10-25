class InterviewCopilotError(Exception):
    """Base error for expected application failures."""


class LLMProviderError(InterviewCopilotError):
    """Raised when the configured LLM provider cannot produce an answer."""

    def __init__(self, message: str = "The language model failed to generate an answer.") -> None:
        super().__init__(message)


class LLMTimeoutError(LLMProviderError):
    """Raised when the LLM provider exceeds the configured timeout."""

    def __init__(self, message: str = "The language model timed out.") -> None:
        super().__init__(message)
