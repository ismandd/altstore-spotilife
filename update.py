import os
import json
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError

# === ENVIRONMENT VARIABLES ===
API_ID = int(os.environ.get("TELEGRAM_API_ID"))
API_HASH = os.environ.get("TELEGRAM_API_HASH")
SESSION_B64 = os.environ.get("TELEGRAM_SESSION_B64")
CHANNEL = os.environ.get("TELEGRAM_CHANNEL", "SpotilifeIPAs")

OUTPUT_FILE = "apps.json"

# === TELEGRAM CLIENT SETUP ===
client = TelegramClient(StringSession(SESSION_B64), API_ID, API_HASH)

async def main():
    await client.start()
    print("✅ Bot logged in successfully")

    apps_data = {
        "name": "Spotilife Repo",
        "identifier": "com.spotilife.repo",
        "apps": []
    }

    # Fetch last 50 messages from the channel
    async for msg in client.iter_messages(CHANNEL, limit=50):
        if msg.media and msg.file:
            app_entry = {
                "name": msg.file.name if msg.file.name else f"App {msg.id}",
                "url": f"https://t.me/{CHANNEL}/{msg.id}"
            }
            apps_data["apps"].append(app_entry)
            print(f"Added: {app_entry['name']}")

    # Save to apps.json
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(apps_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved {len(apps_data['apps'])} apps to {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())
