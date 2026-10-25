import logging
import sys


class RedactingFormatter(logging.Formatter):
    """Formatter that strips configured secrets (e.g. Gemini API key) from log output."""

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        secrets: list[str] | None = None,
    ) -> None:
        super().__init__(fmt=fmt, datefmt=datefmt)
        self._secrets = [secret for secret in (secrets or []) if secret]

    def format(self, record: logging.LogRecord) -> str:
        formatted = super().format(record)
        for secret in self._secrets:
            formatted = formatted.replace(secret, "***REDACTED***")
        return formatted


def configure_logging(level: str, secrets: list[str] | None = None) -> None:
    """Configure process-wide stdlib logging once at startup."""

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        RedactingFormatter(
            fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
            secrets=secrets,
        )
    )
    logging.basicConfig(
        level=level.upper(),
        handlers=[handler],
        force=True,
    )
