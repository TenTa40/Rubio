"""
Keypad Bot — نمونه کامل با دکمه‌های inline و chat keypad
"""

from rubio import Bot, Keypad, KeypadRow, Button, BotCommand
from rubio.enums import ButtonType, ChatKeypadType

bot = Bot("YOUR_TOKEN_HERE")

# ─── Keypads ───────────────────────────────────────────────────────────────

MAIN_MENU = Keypad(
    rows=[
        KeypadRow(buttons=[
            Button(id="orders", type=ButtonType.SIMPLE, button_text="📋 سفارشات"),
            Button(id="account", type=ButtonType.SIMPLE, button_text="👤 حساب"),
        ]),
        KeypadRow(buttons=[
            Button(id="support", type=ButtonType.SIMPLE, button_text="💬 پشتیبانی"),
            Button(id="settings", type=ButtonType.SIMPLE, button_text="⚙️ تنظیمات"),
        ]),
    ],
    resize_keyboard=True,
)

CONFIRM_INLINE = Keypad(rows=[
    KeypadRow(buttons=[
        Button(id="confirm_yes", type=ButtonType.SIMPLE, button_text="✅ تایید"),
        Button(id="confirm_no",  type=ButtonType.SIMPLE, button_text="❌ انصراف"),
    ]),
])


def handle(bot, update):
    if not update.new_message:
        return

    msg = update.new_message
    chat_id = update.chat_id
    text = msg.text or ""
    button_id = msg.aux_data.button_id if msg.aux_data else None

    # ─── Commands ──────────────────────────────────────────────────────────
    if text == "/start":
        bot.send_message(
            chat_id=chat_id,
            text="سلام! به ربات خوش آمدید 🎉\nیکی از گزینه‌های زیر را انتخاب کنید:",
            chat_keypad=MAIN_MENU,
            chat_keypad_type=ChatKeypadType.NEW,
        )

    # ─── Chat Keypad Buttons ────────────────────────────────────────────────
    elif text == "📋 سفارشات":
        bot.send_message(
            chat_id=chat_id,
            text="آیا می‌خواهید سفارش جدید ثبت کنید؟",
            inline_keypad=CONFIRM_INLINE,
        )

    elif text == "💬 پشتیبانی":
        bot.send_message(chat_id=chat_id, text="تیم پشتیبانی در خدمت شماست! 🙏")

    # ─── Inline Button Callbacks ────────────────────────────────────────────
    elif button_id == "confirm_yes":
        bot.send_message(chat_id=chat_id, text="سفارش شما ثبت شد ✅")
    elif button_id == "confirm_no":
        bot.send_message(chat_id=chat_id, text="عملیات لغو شد.")


if __name__ == "__main__":
    # Set bot commands
    bot.set_commands([
        BotCommand(command="start", description="شروع"),
    ])
    print("Keypad bot started...")
    bot.run_polling(handle)
