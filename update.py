import os
import json
from telethon import TelegramClient
from telethon.tl.types import MessageMediaDocument

# === CONFIGURATION ===
API_ID = int(os.environ.get("TELEGRAM_API_ID"))
API_HASH = os.environ.get("TELEGRAM_API_HASH")
SESSION_B64 = os.environ.get("TELEGRAM_SESSION_B64")
CHANNEL = os.environ.get("TELEGRAM_CHANNEL", "SpotilifeIPAs")
DOWNLOAD_FOLDER = "downloads"
APPS_JSON = "apps.json"
MESSAGE_LIMIT = 50  # number of latest messages to process

# Ensure download folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Load existing apps.json or create default
if os.path.exists(APPS_JSON):
    with open(APPS_JSON, "r", encoding="utf-8") as f:
        apps_data = json.load(f)
else:
    apps_data = {
        "name": "Spotilife Repo",
        "identifier": "com.spotilife.repo",
        "apps": []
    }

# === TELEGRAM CLIENT SETUP ===
client = TelegramClient(
    session=SESSION_B64,
    api_id=API_ID,
    api_hash=API_HASH
)

async def main():
    await client.start()
    print("✅ Bot logged in successfully")

    async for msg in client.iter_messages(CHANNEL, limit=MESSAGE_LIMIT):
        # Only process messages with files
        if msg.media and isinstance(msg.media, MessageMediaDocument):
            file_name = msg.file.name or f"{msg.id}.ipa"
            file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
            
            if not os.path.exists(file_path):
                await msg.download_media(file_path)
                print(f"Downloaded {file_name}")

            # Attempt to extract metadata from filename
            # Example filename: AppName_v1.2.3.ipa
            if file_name.endswith(".ipa"):
                base = file_name[:-4]  # remove ".ipa"
                if "_v" in base:
                    app_name, app_version = base.rsplit("_v", 1)
                else:
                    app_name = base
                    app_version = "Unknown"

                # Add app info if not already in apps.json
                if not any(app["name"] == app_name for app in apps_data["apps"]):
                    apps_data["apps"].append({
                        "name": app_name,
                        "bundleId": f"com.spotilife.{app_name.lower()}",
                        "version": app_version,
                        "url": f"./{DOWNLOAD_FOLDER}/{file_name}"
                    })
                    print(f"Added {app_name} v{app_version} to apps.json")

    # Save updated apps.json
    with open(APPS_JSON, "w", encoding="utf-8") as f:
        json.dump(apps_data, f, indent=2, ensure_ascii=False)
    print("✅ apps.json updated")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
