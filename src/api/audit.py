"""
Audit logging for API requests.

Logs all API calls to JSON files locally (production will use DynamoDB).
"""

import json
import logging
import time
from collections.abc import Callable
from datetime import UTC, datetime
from functools import wraps
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Audit log directory
AUDIT_LOG_DIR = Path(__file__).parent.parent.parent / "data" / "audit_logs"
AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)


class AuditLogger:
    """Audit logger for API requests."""

    def __init__(self):
        self.log_dir = AUDIT_LOG_DIR

    def log_request(
        self,
        endpoint: str,
        method: str,
        request_data: dict[str, Any],
        response_data: dict[str, Any],
        duration_seconds: float,
        status_code: int,
        user: str = "anonymous",
    ):
        """
        Log an API request to JSON file.

        Args:
            endpoint: API endpoint path
            method: HTTP method (GET, POST, etc.)
            request_data: Request payload
            response_data: Response payload (summary only)
            duration_seconds: Request duration
            status_code: HTTP status code
            user: User identifier (for future auth)
        """
        log_entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "endpoint": endpoint,
            "method": method,
            "user": user,
            "request": request_data,
            "response_summary": self._summarize_response(response_data),
            "duration_seconds": round(duration_seconds, 3),
            "status_code": status_code,
        }

        # Write to daily log file
        log_file = self._get_log_file()

        try:
            # Append to file
            with open(log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")

    def _summarize_response(self, response: dict[str, Any]) -> dict[str, Any]:
        """
        Create summary of response (avoid logging huge SOW text).

        Args:
            response: Full response data

        Returns:
            Summarized response
        """
        summary = {}

        for key, value in response.items():
            if key == "sow_text" and isinstance(value, str):
                # Summarize SOW text
                summary[key] = f"<{len(value)} characters>"
            elif isinstance(value, str) and len(value) > 500:
                # Truncate long strings
                summary[key] = value[:500] + "..."
            else:
                summary[key] = value

        return summary

    def _get_log_file(self) -> Path:
        """Get today's log file path."""
        today = datetime.now(UTC).strftime("%Y-%m-%d")
        from typing import cast

        return cast(Path, self.log_dir / f"audit_{today}.jsonl")


# Global audit logger instance
audit_logger = AuditLogger()


def audit_endpoint(endpoint_name: str):
    """
    Decorator to audit API endpoint calls.

    Usage:
        @router.post("/api/v1/sow/create")
        @audit_endpoint("sow_create")
        async def create_sow(...):
            ...

    Args:
        endpoint_name: Descriptive name for the endpoint
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            status_code = 200
            response_data = {}

            try:
                # Call the actual endpoint
                result = await func(*args, **kwargs)

                # Convert Pydantic model to dict if needed
                if hasattr(result, "model_dump"):
                    response_data = result.model_dump()
                else:
                    response_data = result

                return result

            except Exception as e:
                status_code = 500
                response_data = {"error": str(e)}
                raise

            finally:
                duration = time.time() - start_time

                # Extract request data from kwargs
                request_data = {}
                if "request" in kwargs:
                    req = kwargs["request"]
                    if hasattr(req, "model_dump"):
                        request_data = req.model_dump()
                    else:
                        request_data = {"body": str(req)}

                # Log the request
                audit_logger.log_request(
                    endpoint=endpoint_name,
                    method="POST",  # Most endpoints are POST
                    request_data=request_data,
                    response_data=response_data,
                    duration_seconds=duration,
                    status_code=status_code,
                )

        return wrapper

    return decorator
