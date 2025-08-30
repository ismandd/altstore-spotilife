import os
import re
from telethon import TelegramClient, events
from github import Github

# Your Telegram API credentials from the app configuration
API_ID = 27090201
API_HASH = 'acc2efd321fdff9e45eb84a7c5d283d0'
CHANNEL = 'SpotilifeIPAs'

# Initialize Telegram client
client = TelegramClient('session_name', API_ID, API_HASH)

async def main():
    # Get the latest message from the channel
    async for message in client.iter_messages(CHANNEL, limit=1):
        if message.text:
            # Extract IPA link using regex
            ipa_links = re.findall(r'https?://[^\s]+\.ipa', message.text)
            if ipa_links:
                latest_ipa = ipa_links[0]
                
                # Update GitHub repository description
                g = Github(os.environ['GITHUB_TOKEN'])
                repo = g.get_repo('your-username/altstore-spotilife')  # Replace with your repo
                repo.edit(description=f"Latest Spotilife IPA: {latest_ipa}")
                
                print(f"Updated repository with latest IPA: {latest_ipa}")
                return
    
    print("No IPA link found in the latest message")

# Run the script
if __name__ == '__main__':
    import asyncio
    
    # Use bot token if available, otherwise use existing session
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if bot_token:
        # Use bot authentication (recommended for CI/CD)
        with client:
            client.loop.run_until_complete(main())
    else:
        # Try to use existing session file
        try:
            with client:
                client.loop.run_until_complete(main())
        except Exception as e:
            print(f"Error: {e}")
            print("Please set TELEGRAM_BOT_TOKEN environment variable")
            exit(1)
