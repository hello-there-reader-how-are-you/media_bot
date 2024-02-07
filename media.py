import discord
from discord.ext import commands
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import io
from io import BytesIO
from discord import Intents
intents = Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
import requests
import tempfile
from PIL import Image
import os



# Discord bot token and Google Drive credentials file

from new_wave import *
# Initialize Discord bot

# Initialize Google Drive authentication
gauth = GoogleAuth()

# Try loading saved credentials
try:
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("mycreds.txt")
except Exception as e:
    print(f"Error loading/saving credentials: {e}")
    gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.event
async def on_message(message):
    if message.channel.id == TARGET_CHANNEL_ID:
        print(f'Message content: {message.content}')

    if message.channel.id == TARGET_CHANNEL_ID and message.attachments:
        for attachment in message.attachments:
            print("IMMAGINE!!!")
            if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']):
                print("Lennon")
                print(f'Detected image: {attachment.url}')
                await download_and_upload(attachment.url)
  



from PIL import Image

async def download_and_upload(url):
    print(f'Downloading image from: {url}')
    
    # Download the image
    response = requests.get(url)
    
    if response.status_code == 200:
        # Open the image using PIL
        img = Image.open(BytesIO(response.content))
        
        # Save the image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            img.save(temp_file.name, format="PNG")
        
        # Upload the image to Google Drive
        name = url[78:url.index("?ex")]
        file_drive = drive.CreateFile({'title': name, 'mimeType': 'image/png'})
        file_drive.SetContentFile(temp_file.name)
        file_drive['parents'] = [{'id': GOOGLE_DRIVE_FOLDER_ID}]
        file_drive.Upload()
        print("wrobber")
        # Clean up the temporary file
        #C:\Users\uuuuser\AppData\Local\Temp

        print(os.path.exists(temp_file.name))
        temp_file.close()
        try: os.unlink(temp_file.name)
        except: print("dirty")
        print(os.path.exists(temp_file.name))

    else:
        print(f"Failed to download image from {url}, status code: {response.status_code}")


if __name__ == '__main__':
    bot.run(TOKEN)
