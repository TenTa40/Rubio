"""
Echo Bot — ساده‌ترین مثال Rubio
هر چیزی که کاربر بفرستد را برمی‌گرداند.
"""

from rubio import Bot

bot = Bot("YOUR_TOKEN_HERE")


def handle(bot, update):
    if update.new_message:
        msg = update.new_message
        if msg.text:
            bot.send_message(
                chat_id=update.chat_id,
                text=f"🔁 {msg.text}",
                reply_to_message_id=msg.message_id,
            )


if __name__ == "__main__":
    print("Echo bot started...")
    bot.run_polling(handle, interval=1.0)
