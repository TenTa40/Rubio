"""
Rubio - Rubika Bot API Library
Core HTTP client: handles all API requests with retry + timeout logic
"""

from __future__ import annotations
import time
import logging
from typing import Any, Dict, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import APIError, NetworkError, TimeoutError, InvalidTokenError

logger = logging.getLogger("rubio")

BASE_URL = "https://botapi.rubika.ir/v3"
DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3


def _build_session(retries: int = DEFAULT_RETRIES) -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


class RubioClient:
    """
    Low-level HTTP client for the Rubika Bot API.
    You usually use `Bot` instead of this directly.
    """

    def __init__(
        self,
        token: str,
        timeout: int = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
    ):
        if not token or not isinstance(token, str):
            raise InvalidTokenError("Token must be a non-empty string.")
        self.token = token
        self.timeout = timeout
        self._session = _build_session(retries)
        self._base = f"{BASE_URL}/{token}"

    def call(self, method: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a POST request to the API.

        Args:
            method: API method name (e.g. 'sendMessage')
            data: JSON payload

        Returns:
            Parsed response data dict

        Raises:
            APIError, NetworkError, TimeoutError
        """
        url = f"{self._base}/{method}"
        payload = data or {}

        try:
            logger.debug("POST %s | payload: %s", method, payload)
            resp = self._session.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Request to '{method}' timed out after {self.timeout}s.")
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"Connection error on '{method}': {e}")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Request error on '{method}': {e}")

        try:
            result = resp.json()
        except Exception:
            raise NetworkError(f"Invalid JSON response from '{method}': {resp.text[:200]}")

        status = result.get("status", "")
        if status not in ("OK", "ok", ""):
            raise APIError(
                status=status,
                message=result.get("status_det", result.get("message", "")),
                data=result,
            )

        return result.get("data", result)

    def upload_file(self, upload_url: str, file_bytes: bytes, filename: str = "file") -> str:
        """
        Upload a file to the given upload_url.
        Returns the file_id.
        """
        try:
            resp = self._session.post(
                upload_url,
                files={"file": (filename, file_bytes)},
                timeout=self.timeout,
            )
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"File upload error: {e}")

        try:
            result = resp.json()
        except Exception:
            raise NetworkError(f"Invalid JSON from upload endpoint: {resp.text[:200]}")

        file_id = result.get("file_id") or result.get("data", {}).get("file_id")
        if not file_id:
            raise APIError(status="upload_error", message=str(result))
        return file_id

    def close(self):
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
