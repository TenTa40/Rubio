# Rubio 🤖

**کتابخانه پایتون برای Bot API روبیکا — ساده، سریع و کامل**

[![PyPI version](https://badge.fury.io/py/rubio.svg)](https://pypi.org/project/rubio/)
[![Python](https://img.shields.io/pypi/pyversions/rubio)](https://pypi.org/project/rubio/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## نصب

```bash
pip install rubio
```

---

## شروع سریع

```python
from rubio import Bot

bot = Bot("YOUR_TOKEN")

# اطلاعات بات
me = bot.get_me()
print(f"Bot: @{me.username}")

# ارسال پیام ساده
bot.send_message("u0abc123...", "سلام! 👋")
```

---

## دریافت آپدیت‌ها

### روش ۱ — Long Polling (ساده‌ترین روش)

```python
from rubio import Bot

bot = Bot("YOUR_TOKEN")

def handle(bot, update):
    if update.new_message:
        msg = update.new_message
        if msg.text == "/start":
            bot.send_message(update.chat_id, "خوش آمدید! 🎉")
        else:
            bot.send_message(update.chat_id, f"گفتی: {msg.text}")

bot.run_polling(handle)
```

### روش ۲ — Webhook (برای production)

```python
# Flask example
from flask import Flask, request
from rubio import Bot
from rubio.webhook import parse_webhook
from rubio.models import Update

app = Flask(__name__)
bot = Bot("YOUR_TOKEN")

# Register webhook
bot.update_bot_endpoint("https://yourdomain.com/webhook", UpdateEndpointType.RECEIVE_UPDATE)

@app.route("/webhook", methods=["POST"])
def webhook():
    event = parse_webhook(request.data)
    if isinstance(event, Update) and event.new_message:
        bot.send_message(event.chat_id, "پیام دریافت شد!")
    return "ok"
```

---

## ارسال پیام با دکمه‌ها

### Inline Keypad (دکمه زیر پیام)

```python
from rubio import Bot, Keypad, KeypadRow, Button
from rubio.enums import ButtonType

bot = Bot("YOUR_TOKEN")

keypad = Keypad(rows=[
    KeypadRow(buttons=[
        Button(id="btn_yes", type=ButtonType.SIMPLE, button_text="✅ بله"),
        Button(id="btn_no",  type=ButtonType.SIMPLE, button_text="❌ خیر"),
    ]),
])

bot.send_message(
    chat_id="u0abc...",
    text="آیا موافقید؟",
    inline_keypad=keypad,
)
```

### Chat Keypad (دکمه پایین چت)

```python
from rubio.enums import ChatKeypadType

keypad = Keypad(rows=[
    KeypadRow(buttons=[
        Button(id="1", type=ButtonType.SIMPLE, button_text="📋 لیست"),
        Button(id="2", type=ButtonType.SIMPLE, button_text="⚙️ تنظیمات"),
    ]),
    KeypadRow(buttons=[
        Button(id="3", type=ButtonType.SIMPLE, button_text="❓ راهنما"),
    ]),
], resize_keyboard=True)

bot.send_message(
    chat_id="u0abc...",
    text="منوی اصلی:",
    chat_keypad=keypad,
    chat_keypad_type=ChatKeypadType.NEW,
)
```

---

## فرمت‌بندی متن (Metadata)

```python
from rubio import Bot, Metadata, MetadataPart
from rubio.enums import MetadataType

bot = Bot("YOUR_TOKEN")

text = "سلام کاربر عزیز!"
meta = Metadata(meta_data_parts=[
    MetadataPart(type=MetadataType.BOLD,   from_index=0, length=4),   # "سلام" — bold
    MetadataPart(type=MetadataType.ITALIC, from_index=5, length=5),   # "کاربر" — italic
])

bot.send_message("u0abc...", text, metadata=meta)
```

انواع فرمت‌بندی پشتیبانی‌شده:

| نوع | توضیح |
|-----|-------|
| `Bold` | **متن برجسته** |
| `Italic` | *متن کج* |
| `Underline` | متن زیرخط‌دار |
| `Strike` | ~~خط‌خورده~~ |
| `Mono` | `تک‌فاصله` |
| `Spoiler` | اسپویلر |
| `Link` | لینک قابل کلیک |
| `MentionText` | منشن کاربر |
| `Pre` | بلاک کد |
| `Quote` | نقل‌قول |

---

## ارسال فایل

```python
from rubio.enums import FileType

# آپلود و ارسال عکس
file_id = bot.upload_file(FileType.IMAGE, file_path="photo.jpg")
bot.send_file(chat_id="u0abc...", file_id=file_id, text="عکس جدید!")

# دانلود فایل دریافتی
if update.new_message and update.new_message.file:
    url = bot.get_file(update.new_message.file.file_id)
    print("دانلود از:", url)
```

---

## ارسال نظرسنجی

```python
bot.send_poll(
    chat_id="u0abc...",
    question="بهترین زبان برنامه‌نویسی؟",
    options=["Python 🐍", "JavaScript", "Go", "Rust"],
)
```

---

## مدیریت گروه و کانال

```python
# مسدود کردن کاربر
bot.ban_chat_member(chat_id="g0abc...", user_id="u0xyz...")

# رفع مسدودیت
bot.unban_chat_member(chat_id="g0abc...", user_id="u0xyz...")

# حذف پیام
bot.delete_message(chat_id="g0abc...", message_id="12345")

# فوروارد پیام
bot.forward_message(
    from_chat_id="g0abc...",
    message_id="12345",
    to_chat_id="u0xyz...",
)
```

---

## تنظیم دستورات بات

```python
from rubio import BotCommand

bot.set_commands([
    BotCommand(command="start",   description="شروع کار با بات"),
    BotCommand(command="help",    description="راهنما"),
    BotCommand(command="settings", description="تنظیمات"),
])
```

---

## مدیریت خطا

```python
from rubio.exceptions import APIError, NetworkError, TimeoutError

try:
    bot.send_message("u0abc...", "سلام!")
except APIError as e:
    print(f"خطای API: {e.status} — {e.message}")
except TimeoutError:
    print("اتصال به سرور time out شد")
except NetworkError as e:
    print(f"خطای شبکه: {e}")
```

---

## Context Manager

```python
with Bot("YOUR_TOKEN") as bot:
    bot.send_message("u0abc...", "سلام!")
# session automatically closed
```

---

## دکمه‌های پیشرفته

### دکمه انتخاب از لیست (Selection)

```python
from rubio import ButtonSelection, ButtonSelectionItem
from rubio.enums import ButtonType, ButtonSelectionGet, ButtonSelectionSearch, ButtonSelectionType

selection = ButtonSelection(
    selection_id="city_select",
    get_type=ButtonSelectionGet.LOCAL,
    search_type=ButtonSelectionSearch.LOCAL,
    items=[
        ButtonSelectionItem(text="تهران", type=ButtonSelectionType.TEXT_ONLY),
        ButtonSelectionItem(text="اصفهان", type=ButtonSelectionType.TEXT_ONLY),
        ButtonSelectionItem(text="شیراز", type=ButtonSelectionType.TEXT_ONLY),
    ],
    title="شهر خود را انتخاب کنید",
)

btn = Button(id="city", type=ButtonType.SELECTION, button_text="انتخاب شهر", button_selection=selection)
```

### تقویم

```python
from rubio import ButtonCalendar
from rubio.enums import ButtonCalendarType, ButtonType

cal = ButtonCalendar(type=ButtonCalendarType.DATE_PERSIAN, min_year="1400", max_year="1410")
btn = Button(id="date", type=ButtonType.CALENDAR, button_text="انتخاب تاریخ", button_calendar=cal)
```

### درخواست موقعیت مکانی

```python
btn = Button(id="loc", type=ButtonType.ASK_MY_LOCATION, button_text="📍 موقعیت من")
```

### درخواست شماره تلفن

```python
btn = Button(id="phone", type=ButtonType.ASK_MY_PHONE_NUMBER, button_text="📞 شماره من")
```

---

## ساختار پروژه

```
rubio/
├── rubio/
│   ├── __init__.py      # Public API
│   ├── bot.py           # Bot class — all API methods
│   ├── client.py        # HTTP client with retry logic
│   ├── models.py        # Dataclass models for all API objects
│   ├── enums.py         # All official API enums
│   ├── webhook.py       # Webhook parser helper
│   └── exceptions.py    # Custom exceptions
├── examples/
│   ├── echo_bot.py
│   ├── keypad_bot.py
│   └── file_bot.py
├── tests/
│   └── test_bot.py
├── pyproject.toml
└── README.md
```

---

## مجوز

MIT License — آزادانه استفاده کنید.
