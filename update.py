import os
import json
import re
import asyncio
from telethon import TelegramClient
from github import Github

# -----------------------------
# Environment variables
# -----------------------------
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
channel = os.getenv("TELEGRAM_CHANNEL", "SpotilifeIPAs")
github_repo = os.getenv("GITHUB_REPOSITORY")  # e.g., username/altstore-spotilife

apps_json_path = "apps.json"

# -----------------------------
# Initialize Telegram client
# -----------------------------
client = TelegramClient('bot', api_id, api_hash)

# -----------------------------
# Initialize GitHub client
# -----------------------------
gh = Github(os.getenv("GITHUB_TOKEN"))
repo = gh.get_repo(github_repo)

# -----------------------------
# Main async function
# -----------------------------
async def main():
    await client.connect()
    if not await client.is_user_authorized():
        await client.start(bot_token=bot_token)
    print("✅ Bot logged in successfully")

    # Fetch the latest IPA message
    async for msg in client.iter_messages(channel, limit=20):
        if msg.file and msg.file.name.endswith(".ipa"):
            filename = msg.file.name
            version_match = re.search(r"(\d+\.\d+\.\d+)", filename)
            version = version_match.group(1) if version_match else "1.0"
            local_path = f"./{filename}"

            # Download IPA
            print(f"📥 Downloading {filename} ...")
            await msg.download_media(file=local_path)

            # Upload to GitHub Release
            release_tag = f"v{version}"
            try:
                release = repo.get_release(release_tag)
            except:
                release = repo.create_git_release(
                    tag=release_tag,
                    name=f"Spotilife {version}",
                    message=f"Auto release for Spotilife v{version}"
                )

            # Delete old assets if any
            for asset in release.get_assets():
                asset.delete_asset()

            release.upload_asset(local_path)
            ipa_url = f"https://github.com/{repo.full_name}/releases/download/{release_tag}/{filename}"
            print(f"✅ Uploaded {filename} to GitHub Releases")

            # Update apps.json
            if os.path.exists(apps_json_path):
                with open(apps_json_path, "r") as f:
                    data = json.load(f)
            else:
                data = {
                    "name": "Spotilife Repo",
                    "identifier": "com.spotilife.repo",
                    "apps": []
                }

            app_entry = {
                "name": "EeveeSpotify",
                "bundleIdentifier": "com.spotify.client",
                "developerName": "Spotilife",
                "subtitle": "Spotify with Spotilife patches",
                "version": version,
                "versionDate": msg.date.strftime("%Y-%m-%d"),
                "versionDescription": f"Auto-updated to {version}",
                "downloadURL": ipa_url,
                "localizedDescription": "Modified Spotify IPA.",
                "iconURL": "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg",
                "tintColor": "1DB954",
                "screenshotURLs": []
            }

            data["apps"] = [app_entry]

            with open(apps_json_path, "w") as f:
                json.dump(data, f, indent=2)

            print("✅ apps.json updated")
            break  # Only process the latest IPA

    await client.disconnect()

# -----------------------------
# Run the async main function
# -----------------------------
asyncio.run(main())
