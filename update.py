import os
import base64
import asyncio
from telethon import TelegramClient

# Load secrets from environment
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
session_b64 = os.getenv("TELEGRAM_SESSION_B64")
channel_username = os.getenv("TELEGRAM_CHANNEL", "SpotilifeIPAs")

# Decode session
session_bytes = base64.b64decode(session_b64)
session_file = "session.session"
with open(session_file, "wb") as f:
    f.write(session_bytes)

client = TelegramClient(session_file, api_id, api_hash)

async def main():
    async with client:
        print("✅ Logged in successfully")
        async for msg in client.iter_messages(channel_username, limit=20):
            print(f"{msg.id}: {msg.text}")

if __name__ == "__main__":
    asyncio.run(main())
