import os
import time
import requests

from core import bot, ADMIN_ID, FORCE_JOIN_CHANNELS, NOTIFICATION_CHANNEL, BOT_TOKEN
import handlers  # noqa: F401 - registers all bot handlers on import


def run_polling():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not configured")

    skip_pending = os.environ.get("SKIP_PENDING_UPDATES", "true").strip().lower() in {"1", "true", "yes", "on"}

    while True:
        try:
            print("Bot is polling...")
            bot.infinity_polling(
                timeout=30,
                long_polling_timeout=20,
                allowed_updates=["message", "callback_query"],
                skip_pending=skip_pending,
            )
        except KeyboardInterrupt:
            print("Polling stopped by operator.")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Polling network error: {e}")
            time.sleep(5)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    print("=" * 50)
    print("  UPI Loot Pay Bot Starting...")
    print(f"  Admin ID: {ADMIN_ID}")
    print(f"  Force Join: {FORCE_JOIN_CHANNELS}")
    print(f"  Notification Channel: {NOTIFICATION_CHANNEL}")
    print("=" * 50)
    run_polling()
