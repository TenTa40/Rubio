"""
Rubio - Rubika Bot API Library
Custom exceptions
"""


class RubioError(Exception):
    """Base exception for all Rubio errors."""
    pass


class APIError(RubioError):
    """Raised when the Rubika API returns an error response."""

    def __init__(self, status: str, message: str = "", data: dict = None):
        self.status = status
        self.message = message
        self.data = data or {}
        super().__init__(f"[{status}] {message}")


class NetworkError(RubioError):
    """Raised when a network/connection error occurs."""
    pass


class TimeoutError(NetworkError):
    """Raised when a request times out."""
    pass


class InvalidTokenError(RubioError):
    """Raised when the bot token is invalid or missing."""
    pass


class FileUploadError(RubioError):
    """Raised when a file upload fails."""
    pass
