import os, json, re, requests
from telethon import TelegramClient
from github import Github

# --- Telegram Setup ---
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
channel = os.getenv("TELEGRAM_CHANNEL")

client = TelegramClient("session", api_id, api_hash)

# --- GitHub Setup ---
gh = Github(os.getenv("GITHUB_TOKEN"))
repo = gh.get_repo(os.getenv("GITHUB_REPOSITORY"))

async def main():
    await client.start()

    # Get last message with .ipa
    async for msg in client.iter_messages(channel, limit=20):
        if msg.file and msg.file.name.endswith(".ipa"):
            filename = msg.file.name
            version_match = re.search(r"(\d+\.\d+\.\d+)", filename)
            version = version_match.group(1) if version_match else "1.0"
            path = f"./{filename}"

            print(f"Downloading {filename} ...")
            await msg.download_media(file=path)

            # Upload to GitHub Release
            release_tag = f"v{version}"
            try:
                release = repo.get_release(release_tag)
            except:
                release = repo.create_git_release(release_tag, f"Spotilife {version}", "Auto release")

            # Delete old assets
            for asset in release.get_assets():
                asset.delete_asset()

            release.upload_asset(path)

            # Update apps.json
            with open("apps.json") as f:
                data = json.load(f)

            ipa_url = f"https://github.com/{repo.full_name}/releases/download/{release_tag}/{filename}"
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

            with open("apps.json", "w") as f:
                json.dump(data, f, indent=2)

            print("✅ Updated apps.json")
            break

with client:
    client.loop.run_until_complete(main())
