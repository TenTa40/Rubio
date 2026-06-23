"""
Rubio - Rubika Bot API Library
Webhook: helper to parse incoming webhook requests from Rubika
"""

from __future__ import annotations
import json
import logging
from typing import Union, Optional

from .models import Update, InlineMessage

logger = logging.getLogger("rubio")


def parse_webhook(body: Union[str, bytes, dict]) -> Optional[Union[Update, InlineMessage]]:
    """
    Parse an incoming webhook POST body from Rubika into a typed object.

    Handles both 'update' (receiveUpdate) and 'inline_message' (receiveInlineMessage) events.

    Args:
        body: Raw request body as str, bytes, or already-parsed dict

    Returns:
        Update or InlineMessage instance, or None if unrecognized

    Example (Flask)::

        from flask import Flask, request
        from rubio.webhook import parse_webhook

        app = Flask(__name__)

        @app.route("/webhook", methods=["POST"])
        def webhook():
            event = parse_webhook(request.data)
            if isinstance(event, Update):
                if event.new_message:
                    bot.send_message(event.chat_id, "دریافت شد!")
            return "ok"
    """
    if isinstance(body, (str, bytes)):
        try:
            data = json.loads(body)
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON in webhook body: %s", e)
            return None
    elif isinstance(body, dict):
        data = body
    else:
        logger.error("Unsupported body type: %s", type(body))
        return None

    if "update" in data:
        return Update.from_dict(data["update"])
    elif "inline_message" in data:
        return InlineMessage.from_dict(data["inline_message"])
    else:
        logger.warning("Unknown webhook payload keys: %s", list(data.keys()))
        return None
