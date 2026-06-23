"""
Rubio - Rubika Bot API Library
Bot: high-level interface for all Rubika Bot API methods
"""

from __future__ import annotations
import os
import logging
from typing import List, Optional, Union

from .client import RubioClient
from .models import (
    Bot as BotModel, Chat, Message, Update, InlineMessage,
    Keypad, Metadata, BotCommand, File, Location
)
from .enums import FileType, ChatKeypadType, UpdateEndpointType

logger = logging.getLogger("rubio")


class Bot:
    """
    Main interface for the Rubika Bot API.

    Example::

        from rubio import Bot

        bot = Bot("YOUR_TOKEN")

        # Send a message
        msg = bot.send_message(chat_id="u0abc...", text="سلام!")
        print(msg.message_id)
    """

    def __init__(
        self,
        token: str,
        timeout: int = 30,
        retries: int = 3,
    ):
        """
        Args:
            token: Bot token from @BotFather on Rubika
            timeout: HTTP request timeout in seconds (default 30)
            retries: Number of automatic retries on failure (default 3)
        """
        self._client = RubioClient(token=token, timeout=timeout, retries=retries)
        self.token = token

    # ─── Bot Info ────────────────────────────────────────────────────────────

    def get_me(self) -> BotModel:
        """
        Get basic information about this bot.

        Returns:
            Bot model with id, title, username, etc.
        """
        data = self._client.call("getMe")
        return BotModel.from_dict(data.get("bot", data))

    # ─── Messaging ───────────────────────────────────────────────────────────

    def send_message(
        self,
        chat_id: str,
        text: str,
        *,
        reply_to_message_id: Optional[str] = None,
        disable_notification: bool = False,
        inline_keypad: Optional[Keypad] = None,
        chat_keypad: Optional[Keypad] = None,
        chat_keypad_type: ChatKeypadType = ChatKeypadType.NONE,
        metadata: Optional[Metadata] = None,
    ) -> Message:
        """
        Send a text message (optionally with keypads or metadata formatting).

        Args:
            chat_id: Target chat ID
            text: Message text
            reply_to_message_id: Reply to a specific message
            disable_notification: Suppress push notification
            inline_keypad: Inline buttons (glass buttons below message)
            chat_keypad: Chat keyboard (buttons at bottom of chat)
            chat_keypad_type: 'New' to show keypad, 'Remove' to hide
            metadata: Text formatting (bold, italic, mention, links...)

        Returns:
            Sent Message with message_id
        """
        payload: dict = {"chat_id": chat_id, "text": text}
        if reply_to_message_id:
            payload["reply_to_message_id"] = reply_to_message_id
        if disable_notification:
            payload["disable_notification"] = True
        if inline_keypad:
            payload["inline_keypad"] = inline_keypad.to_dict()
        if chat_keypad:
            payload["chat_keypad"] = chat_keypad.to_dict()
        if chat_keypad_type != ChatKeypadType.NONE:
            payload["chat_keypad_type"] = chat_keypad_type.value
        if metadata:
            payload["metadata"] = metadata.to_dict()

        data = self._client.call("sendMessage", payload)
        return Message(message_id=data.get("message_id", ""), text=text)

    def send_poll(
        self,
        chat_id: str,
        question: str,
        options: List[str],
    ) -> Message:
        """
        Send a poll to a chat.

        Args:
            chat_id: Target chat ID
            question: Poll question
            options: List of option strings

        Returns:
            Message with message_id
        """
        data = self._client.call("sendPoll", {
            "chat_id": chat_id,
            "question": question,
            "options": options,
        })
        return Message(message_id=data.get("message_id", ""))

    def send_location(
        self,
        chat_id: str,
        latitude: str,
        longitude: str,
        *,
        reply_to_message_id: Optional[str] = None,
        disable_notification: bool = False,
        inline_keypad: Optional[Keypad] = None,
        chat_keypad: Optional[Keypad] = None,
        chat_keypad_type: ChatKeypadType = ChatKeypadType.NONE,
    ) -> Message:
        """
        Send a geographic location.

        Args:
            chat_id: Target chat ID
            latitude: Latitude string
            longitude: Longitude string

        Returns:
            Message with message_id
        """
        payload = {
            "chat_id": chat_id,
            "latitude": latitude,
            "longitude": longitude,
        }
        if reply_to_message_id:
            payload["reply_to_message_id"] = reply_to_message_id
        if disable_notification:
            payload["disable_notification"] = disable_notification
        if inline_keypad:
            payload["inline_keypad"] = inline_keypad.to_dict()
        if chat_keypad:
            payload["chat_keypad"] = chat_keypad.to_dict()
        if chat_keypad_type != ChatKeypadType.NONE:
            payload["chat_keypad_type"] = chat_keypad_type.value

        data = self._client.call("sendLocation", payload)
        return Message(message_id=data.get("message_id", ""))

    def send_contact(
        self,
        chat_id: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        *,
        reply_to_message_id: Optional[str] = None,
        disable_notification: bool = False,
        inline_keypad: Optional[Keypad] = None,
        chat_keypad: Optional[Keypad] = None,
        chat_keypad_type: ChatKeypadType = ChatKeypadType.NONE,
    ) -> Message:
        """
        Send a contact card.

        Returns:
            Message with message_id
        """
        payload = {
            "chat_id": chat_id,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
        }
        if reply_to_message_id:
            payload["reply_to_message_id"] = reply_to_message_id
        if disable_notification:
            payload["disable_notification"] = disable_notification
        if inline_keypad:
            payload["inline_keypad"] = inline_keypad.to_dict()
        if chat_keypad:
            payload["chat_keypad"] = chat_keypad.to_dict()
        if chat_keypad_type != ChatKeypadType.NONE:
            payload["chat_keypad_type"] = chat_keypad_type.value

        data = self._client.call("sendContact", payload)
        return Message(message_id=data.get("message_id", ""))

    # ─── Message Management ──────────────────────────────────────────────────

    def edit_message_text(
        self,
        chat_id: str,
        message_id: str,
        text: str,
    ) -> bool:
        """
        Edit the text of a previously sent message.

        Returns:
            True on success
        """
        self._client.call("editMessageText", {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
        })
        return True

    def edit_inline_keypad(
        self,
        chat_id: str,
        message_id: str,
        inline_keypad: Keypad,
    ) -> bool:
        """
        Replace the inline keypad of a message.

        Returns:
            True on success
        """
        self._client.call("editInlineKeypad", {
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_keypad": inline_keypad.to_dict(),
        })
        return True

    def edit_chat_keypad(
        self,
        chat_id: str,
        chat_keypad_type: ChatKeypadType,
        chat_keypad: Optional[Keypad] = None,
    ) -> bool:
        """
        Add, update or remove a chat keypad.

        Args:
            chat_id: Target chat ID
            chat_keypad_type: 'New' to add/update, 'Remove' to delete
            chat_keypad: New keypad data (required when type is 'New')

        Returns:
            True on success
        """
        payload: dict = {
            "chat_id": chat_id,
            "chat_keypad_type": chat_keypad_type.value,
        }
        if chat_keypad:
            payload["chat_keypad"] = chat_keypad.to_dict()
        self._client.call("editChatKeypad", payload)
        return True

    def delete_message(self, chat_id: str, message_id: str) -> bool:
        """
        Delete a message.

        Returns:
            True on success
        """
        self._client.call("deleteMessage", {
            "chat_id": chat_id,
            "message_id": message_id,
        })
        return True

    def forward_message(
        self,
        from_chat_id: str,
        message_id: str,
        to_chat_id: str,
        *,
        disable_notification: bool = False,
    ) -> str:
        """
        Forward a message from one chat to another.

        Returns:
            new_message_id of the forwarded message
        """
        payload = {
            "from_chat_id": from_chat_id,
            "message_id": message_id,
            "to_chat_id": to_chat_id,
        }
        if disable_notification:
            payload["disable_notification"] = True
        data = self._client.call("forwardMessage", payload)
        return data.get("new_message_id", "")

    # ─── File Operations ─────────────────────────────────────────────────────

    def get_file(self, file_id: str) -> str:
        """
        Get the download URL for a file.

        Args:
            file_id: File ID

        Returns:
            Download URL string
        """
        data = self._client.call("getFile", {"file_id": file_id})
        return data.get("download_url", "")

    def request_send_file(self, file_type: FileType) -> str:
        """
        Request an upload URL for a given file type.

        Args:
            file_type: FileType enum value

        Returns:
            Upload URL string
        """
        data = self._client.call("requestSendFile", {"type": file_type.value})
        return data.get("upload_url", "")

    def upload_file(
        self,
        file_type: FileType,
        file_path: Optional[str] = None,
        file_bytes: Optional[bytes] = None,
        filename: Optional[str] = None,
    ) -> str:
        """
        Upload a file and return its file_id for use in send_file().

        Provide either `file_path` (local path) or `file_bytes`.

        Args:
            file_type: Type of file (Image, Video, etc.)
            file_path: Path to local file
            file_bytes: Raw bytes of file content
            filename: Optional filename for the upload

        Returns:
            file_id string
        """
        upload_url = self.request_send_file(file_type)

        if file_path:
            with open(file_path, "rb") as f:
                data = f.read()
            fname = filename or os.path.basename(file_path)
        elif file_bytes is not None:
            data = file_bytes
            fname = filename or "file"
        else:
            raise ValueError("Provide either file_path or file_bytes.")

        return self._client.upload_file(upload_url, data, fname)

    def send_file(
        self,
        chat_id: str,
        file_id: str,
        *,
        text: Optional[str] = None,
        reply_to_message_id: Optional[str] = None,
        disable_notification: bool = False,
        inline_keypad: Optional[Keypad] = None,
        chat_keypad: Optional[Keypad] = None,
        chat_keypad_type: ChatKeypadType = ChatKeypadType.NONE,
    ) -> Message:
        """
        Send an already-uploaded file to a chat.

        Returns:
            Message with message_id
        """
        payload: dict = {"chat_id": chat_id, "file_id": file_id}
        if text:
            payload["text"] = text
        if reply_to_message_id:
            payload["reply_to_message_id"] = reply_to_message_id
        if disable_notification:
            payload["disable_notification"] = disable_notification
        if inline_keypad:
            payload["inline_keypad"] = inline_keypad.to_dict()
        if chat_keypad:
            payload["chat_keypad"] = chat_keypad.to_dict()
        if chat_keypad_type != ChatKeypadType.NONE:
            payload["chat_keypad_type"] = chat_keypad_type.value

        data = self._client.call("sendFile", payload)
        return Message(message_id=data.get("message_id", ""))

    # ─── Chat Management ──────────────────────────────────────────────────────

    def get_chat(self, chat_id: str) -> Chat:
        """
        Get info about a chat (private, group, or channel).

        Returns:
            Chat model
        """
        data = self._client.call("getChat", {"chat_id": chat_id})
        return Chat.from_dict(data.get("chat", data))

    def ban_chat_member(self, chat_id: str, user_id: str) -> bool:
        """
        Ban a user from a group or channel.

        Returns:
            True on success
        """
        self._client.call("banChatMember", {
            "chat_id": chat_id,
            "user_id": user_id,
        })
        return True

    def unban_chat_member(self, chat_id: str, user_id: str) -> bool:
        """
        Unban a previously banned user.

        Returns:
            True on success
        """
        self._client.call("unbanChatMember", {
            "chat_id": chat_id,
            "user_id": user_id,
        })
        return True

    # ─── Updates ─────────────────────────────────────────────────────────────

    def get_updates(
        self,
        offset_id: Optional[str] = None,
        limit: int = 50,
    ) -> tuple[List[Update], Optional[str]]:
        """
        Poll for new updates (Long Polling mode).

        Args:
            offset_id: Pagination cursor from previous call's next_offset_id
            limit: Max updates to fetch (default 50)

        Returns:
            Tuple of (list of Update, next_offset_id)
        """
        payload: dict = {"limit": limit}
        if offset_id:
            payload["offset_id"] = offset_id

        data = self._client.call("getUpdates", payload)
        updates = [Update.from_dict(u) for u in data.get("updates", [])]
        next_offset = data.get("next_offset_id")
        return updates, next_offset

    # ─── Commands & Endpoints ─────────────────────────────────────────────────

    def set_commands(self, commands: List[BotCommand]) -> bool:
        """
        Set the list of commands shown in the bot menu.

        Args:
            commands: List of BotCommand objects

        Returns:
            True on success
        """
        self._client.call("setCommands", {
            "bot_commands": [c.to_dict() for c in commands],
        })
        return True

    def update_bot_endpoint(self, url: str, endpoint_type: UpdateEndpointType) -> bool:
        """
        Register or update a webhook endpoint for a specific event type.

        Args:
            url: HTTPS URL of your endpoint
            endpoint_type: Type of events this endpoint handles

        Returns:
            True on success
        """
        self._client.call("updateBotEndpoints", {
            "url": url,
            "type": endpoint_type.value,
        })
        return True

    # ─── Polling Loop ─────────────────────────────────────────────────────────

    def run_polling(
        self,
        on_update,
        *,
        interval: float = 1.0,
        limit: int = 50,
        error_handler=None,
    ):
        """
        Start a long-polling loop. Blocks forever until KeyboardInterrupt.

        Args:
            on_update: Callable(bot, update) called for each new Update
            interval: Seconds to wait between polls (default 1.0)
            limit: Max updates per request (default 50)
            error_handler: Optional callable(exception) for error logging

        Example::

            def handle(bot, update):
                if update.new_message:
                    bot.send_message(update.chat_id, "پیام دریافت شد!")

            bot.run_polling(handle)
        """
        import time
        logger.info("Rubio polling started.")
        offset = None
        while True:
            try:
                updates, offset = self.get_updates(offset_id=offset, limit=limit)
                for update in updates:
                    try:
                        on_update(self, update)
                    except Exception as e:
                        logger.error("Error in on_update handler: %s", e)
                        if error_handler:
                            error_handler(e)
            except Exception as e:
                logger.error("Polling error: %s", e)
                if error_handler:
                    error_handler(e)
                time.sleep(interval * 5)
            time.sleep(interval)

    # ─── Lifecycle ────────────────────────────────────────────────────────────

    def close(self):
        """Close the underlying HTTP session."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __repr__(self):
        return f"<Bot token={self.token[:8]}...>"
