"""
Rubio — Unit Tests
"""

import pytest
import responses as resp_mock
import requests

from rubio import Bot, Keypad, KeypadRow, Button, Metadata, MetadataPart
from rubio.enums import ButtonType, MetadataType, FileType, ChatKeypadType
from rubio.exceptions import APIError, NetworkError, InvalidTokenError
from rubio.webhook import parse_webhook
from rubio.models import Update, InlineMessage


BASE = "https://botapi.rubika.ir/v3/TEST_TOKEN"


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def bot():
    return Bot("TEST_TOKEN")


# ─── Token Validation ─────────────────────────────────────────────────────────

def test_invalid_token_raises():
    with pytest.raises(InvalidTokenError):
        Bot("")

    with pytest.raises(InvalidTokenError):
        Bot(None)


# ─── get_me ──────────────────────────────────────────────────────────────────

@resp_mock.activate
def test_get_me(bot):
    resp_mock.add(
        resp_mock.POST,
        f"{BASE}/getMe",
        json={"status": "OK", "data": {"bot": {"bot_id": "b0abc", "username": "mybot"}}},
    )
    me = bot.get_me()
    assert me.bot_id == "b0abc"
    assert me.username == "mybot"


# ─── send_message ────────────────────────────────────────────────────────────

@resp_mock.activate
def test_send_message(bot):
    resp_mock.add(
        resp_mock.POST,
        f"{BASE}/sendMessage",
        json={"status": "OK", "data": {"message_id": "12345"}},
    )
    msg = bot.send_message("u0abc", "سلام!")
    assert msg.message_id == "12345"


@resp_mock.activate
def test_send_message_with_inline_keypad(bot):
    resp_mock.add(
        resp_mock.POST,
        f"{BASE}/sendMessage",
        json={"status": "OK", "data": {"message_id": "99"}},
    )
    keypad = Keypad(rows=[
        KeypadRow(buttons=[Button(id="1", type=ButtonType.SIMPLE, button_text="OK")])
    ])
    msg = bot.send_message("u0abc", "انتخاب کن:", inline_keypad=keypad)
    assert msg.message_id == "99"


# ─── API Error ───────────────────────────────────────────────────────────────

@resp_mock.activate
def test_api_error_raises(bot):
    resp_mock.add(
        resp_mock.POST,
        f"{BASE}/sendMessage",
        json={"status": "ERROR_INVALID_INPUT", "status_det": "chat_id invalid"},
    )
    with pytest.raises(APIError) as exc:
        bot.send_message("BAD_ID", "test")
    assert "ERROR_INVALID_INPUT" in str(exc.value)


# ─── delete_message ──────────────────────────────────────────────────────────

@resp_mock.activate
def test_delete_message(bot):
    resp_mock.add(
        resp_mock.POST,
        f"{BASE}/deleteMessage",
        json={"status": "OK", "data": {}},
    )
    result = bot.delete_message("u0abc", "12345")
    assert result is True


# ─── get_updates ─────────────────────────────────────────────────────────────

@resp_mock.activate
def test_get_updates(bot):
    resp_mock.add(
        resp_mock.POST,
        f"{BASE}/getUpdates",
        json={
            "status": "OK",
            "data": {
                "updates": [
                    {
                        "type": "NewMessage",
                        "chat_id": "u0abc",
                        "new_message": {
                            "message_id": "1",
                            "text": "hello",
                            "time": 1700000000,
                            "is_edited": False,
                            "sender_type": "User",
                            "sender_id": "u0xyz",
                        }
                    }
                ],
                "next_offset_id": "2"
            }
        },
    )
    updates, next_id = bot.get_updates()
    assert len(updates) == 1
    assert updates[0].chat_id == "u0abc"
    assert updates[0].new_message.text == "hello"
    assert next_id == "2"


# ─── Webhook Parser ──────────────────────────────────────────────────────────

def test_parse_webhook_update():
    body = '{"update": {"type": "NewMessage", "chat_id": "u0abc", "new_message": {"message_id": "1", "text": "hi", "time": 1700000000, "is_edited": false, "sender_type": "User", "sender_id": "u0xyz"}}}'
    event = parse_webhook(body)
    assert isinstance(event, Update)
    assert event.chat_id == "u0abc"
    assert event.new_message.text == "hi"


def test_parse_webhook_inline_message():
    body = '{"inline_message": {"sender_id": "u0xyz", "text": "click", "location": null, "aux_data": {"start_id": null, "button_id": "btn1"}, "message_id": "5", "chat_id": "u0abc"}}'
    event = parse_webhook(body)
    assert isinstance(event, InlineMessage)
    assert event.sender_id == "u0xyz"
    assert event.aux_data.button_id == "btn1"


def test_parse_webhook_invalid_json():
    event = parse_webhook("not json")
    assert event is None


# ─── Models ──────────────────────────────────────────────────────────────────

def test_keypad_to_dict():
    keypad = Keypad(rows=[
        KeypadRow(buttons=[
            Button(id="1", type=ButtonType.SIMPLE, button_text="Click me"),
        ])
    ], resize_keyboard=True)
    d = keypad.to_dict()
    assert d["rows"][0]["buttons"][0]["button_text"] == "Click me"
    assert d["resize_keyboard"] is True


def test_metadata_to_dict():
    meta = Metadata(meta_data_parts=[
        MetadataPart(type=MetadataType.BOLD, from_index=0, length=5),
    ])
    d = meta.to_dict()
    assert d["meta_data_parts"][0]["type"] == "Bold"
    assert d["meta_data_parts"][0]["length"] == 5
