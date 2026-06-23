"""
Rubio — کتابخانه رسمی Bot API روبیکا برای پایتون

ساده، سریع و کامل.

Example::

    from rubio import Bot, Button, Keypad, KeypadRow, BotCommand
    from rubio.enums import ButtonType, FileType

    bot = Bot("YOUR_TOKEN")

    # اطلاعات بات
    me = bot.get_me()
    print(me.username)

    # ارسال پیام ساده
    bot.send_message("u0abc...", "سلام دنیا!")

    # شروع polling
    def handle(bot, update):
        if update.new_message and update.new_message.text == "/start":
            bot.send_message(update.chat_id, "خوش آمدید!")

    bot.run_polling(handle)
"""

__version__ = "1.0.0"
__author__ = "Rubio Contributors"
__license__ = "MIT"

from .bot import Bot
from .models import (
    Chat,
    Message,
    Update,
    InlineMessage,
    Keypad,
    KeypadRow,
    Button,
    BotCommand,
    Metadata,
    MetadataPart,
    File,
    Location,
    Poll,
    ButtonSelection,
    ButtonSelectionItem,
    ButtonCalendar,
    ButtonNumberPicker,
    ButtonStringPicker,
    ButtonTextbox,
    ButtonLocation,
    AuxData,
    ForwardedFrom,
    Sticker,
    ContactMessage,
)
from .models import Bot as BotModel
from .enums import (
    ChatType,
    FileType,
    ButtonType,
    UpdateType,
    ChatKeypadType,
    MetadataType,
    UpdateEndpointType,
    PollStatus,
    ButtonCalendarType,
    ButtonLocationType,
    ButtonSelectionGet,
    ButtonSelectionSearch,
    ButtonSelectionType,
    ButtonTextboxTypeKeypad,
    ButtonTextboxTypeLine,
    ForwardedFrom as ForwardedFromEnum,
    MessageSender,
)
from .exceptions import (
    RubioError,
    APIError,
    NetworkError,
    TimeoutError,
    InvalidTokenError,
    FileUploadError,
)
from .webhook import parse_webhook

__all__ = [
    # Core
    "Bot",
    # Models
    "BotModel",
    "Chat",
    "Message",
    "Update",
    "InlineMessage",
    "Keypad",
    "KeypadRow",
    "Button",
    "BotCommand",
    "Metadata",
    "MetadataPart",
    "File",
    "Location",
    "Poll",
    "ButtonSelection",
    "ButtonSelectionItem",
    "ButtonCalendar",
    "ButtonNumberPicker",
    "ButtonStringPicker",
    "ButtonTextbox",
    "ButtonLocation",
    "AuxData",
    "ForwardedFrom",
    "Sticker",
    "ContactMessage",
    # Enums
    "ChatType",
    "FileType",
    "ButtonType",
    "UpdateType",
    "ChatKeypadType",
    "MetadataType",
    "UpdateEndpointType",
    "PollStatus",
    "ButtonCalendarType",
    "ButtonLocationType",
    "ButtonSelectionGet",
    "ButtonSelectionSearch",
    "ButtonSelectionType",
    "ButtonTextboxTypeKeypad",
    "ButtonTextboxTypeLine",
    "ForwardedFromEnum",
    "MessageSender",
    # Exceptions
    "RubioError",
    "APIError",
    "NetworkError",
    "TimeoutError",
    "InvalidTokenError",
    "FileUploadError",
    # Webhook
    "parse_webhook",
]
