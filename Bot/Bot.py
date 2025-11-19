import random
import os
import discord
from discord.ext import commands


TARGET_USER_ID = 'replace with_target_user_id'  # Set the target user ID here as a string


Folder = "A:\Freetime_WORK\Log-on\Bot\content"
Discord_Token = os.getenv("") #set your bot token here as you please, i have it in environments so if you dont, remove it and put your token as a string



intents = discord.Intents.default()
intents.messages = True
intents.dm_messages = True
#dont forget to check discord bots permissions, enable "SERVER MEMBERS INTENT" in discord developer portal
bot = commands.Bot(command_prefix='!', intents=intents)


def get_content_from_file():
    try:
        # 1. Get list of files in the folder
        files = [f for f in os.listdir(Folder) if os.path.isfile(os.path.join(Folder, f))]
        
        if not files:
            return "Folder empty", None

        selected_file = random.choice(files)
        file_path = os.path.join(Folder, selected_file) 
        
        # 2. READ FILE CONTENT
        with open(file_path, 'r', encoding='utf-8') as File:
            content = File.read()
        
        return content, None

    except FileNotFoundError:
        return f"folder not found {Folder}", None
    except Exception as e:
        return f"Failed to read content {e}", None


@bot.event
async def on_ready():
    print(f'Logged as {bot.user} (ID: {bot.user.id})')
    
    # 1. Gets the function to read content from file into a message
    message_content, error_message = get_content_from_file()
    
    if error_message:
        print(error_message)
        await bot.close()
        return
    
    try:
        target_user = await bot.fetch_user(TARGET_USER_ID)
    except Exception as e:
        print(f"Error fetching user via API: {e}")
        target_user = None

    if target_user:
        try:
            # 3. Sends msg as DM and confirms
            await target_user.send(message_content)
            print(f"Msg sent successfully to {target_user.name}")

        except discord.Forbidden:
            # KORJAUS 3: Oikea virheenkäsittely
            print(f"No permissions to send a dm to {target_user.name}.")
            print("Is bot added or do you have a combined platform")

        except Exception as e:
            # Kaikki muut virheet lähetyksessä
            print(f"Other DM error: {e}")
            
    else:
        # Käsittelee nyt fetch_userin epäonnistumisen
        print(f"Error, User ID {TARGET_USER_ID} not accessible or found.")

    # 4. SAMMUTA BOTTI
    await bot.close()
    print("Bot off.")


# Käynnistetään botti tokenilla
if Discord_Token:
    try:
        bot.run(Discord_Token) 
    except Exception as e:
        print(f"Error, bot failed to launch. {e}")
else:
    print("Error, token not found")