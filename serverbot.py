import subprocess
import discord
from discord.ext import commands
from discord import app_commands

import json
import os
import re
import time
import aiohttp
from typing import Optional, Literal
import shutil
import time

##################################################################################################################
# BEGINNING OF SETUP VARIABLES
##################################################################################################################

    # 1)
# Change number to your discord server's ID
GUILD_ID = 123

    # 2)
# Change number to ID assigned to server owner's role
OWNER_ROLE_ID = 123

    # 3)
# Change number to ID assigned to admin role
ADMIN_ROLE_ID = 123

    # 4)
# Change to false to allow both admin and owner roles to whitelist users
WHITELISTING_OWNER_ONLY = True

    # 5)
# Change to false to allow both admin and owner roles to manually start server
STARTING_OWNER_ONLY = True

    # 6)
# Change to false to allow both admin and owner roles to manually restart server
RESTARTING_OWNER_ONLY = True

    # 7)
# Input absolute path to your server's whitelist file
WHITELIST_FILE = ""

    # 8)
# Input your bot token
TOKEN = ""

    # 9)
'''
1) Create a .sh file that runs the command that starts your server
2) Open the terminal in your server's directory and run the following command (replace FILE_NAME with the name of your newly created .sh file): 
    chmod +x FILE_NAME.sh
'''

    # 10)
# Input the server starting file name here
START_FILE = ""
'''
# Example of what the inside of your start.sh file should look like (the "#!/bin/bash" line at the top is required for bash to execute the command in the file):

# File name = start.sh
# File contents:

#!/bin/bash
java -Xms1G -Xmx6G -jar fabric-server-mc.1.21.10-loader.0.17.3-launcher.1.1.0.jar nogui
'''

    # 11)
# Input directory that your .sh file is located in (DO NOT INCLUDE FILE NAME)
START_DIR = ""

##################################################################################################################
# END OF SETUP VARIABLES
##################################################################################################################





##################################################################################################################
# BOT CODE
##################################################################################################################

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
print("Loaded commands at startup:", bot.tree.get_commands())


def is_whitelisted(username: str):
    if not os.path.exists(WHITELIST_FILE):
        return False
    try:
        with open(WHITELIST_FILE, "r") as f:
            data = json.load(f)
        for entry in data:
            if entry.get("name", "").lower() == username.lower():
                return True
    except:
        pass
    return False

async def get_uuid(username: str):
    """Returns UUID string if username exists, otherwise None."""
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("id") 
            return None

def send_to_server(cmd: str):
    subprocess.run(["mcrcon", "-H", "127.0.0.1", "-P", "25575", "-p", "4630", f"{cmd}"])

async def is_owner(interaction: discord.Interaction):
    user_role_ids = [role.id for role in interaction.user.roles]
    if OWNER_ROLE_ID not in user_role_ids:
        await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)
        return

async def is_owner_and_admin(interaction: discord.Interaction):
    user_role_ids = [role.id for role in interaction.user.roles]
    if OWNER_ROLE_ID not in user_role_ids and ADMIN_ROLE_ID not in user_role_ids:
        await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)
        return

##################################################################################################################
# SLASH COMMANDS
##################################################################################################################
# WHITELIST ADD COMMAND
@bot.tree.command(name="whitelist", description="Add a Minecraft username to the whitelist")
@app_commands.describe(username="Whitelist username")
async def whitelist(interaction: discord.Interaction, username: str):

    if not WHITELISTING_OWNER_ONLY:
        is_owner_and_admin()
    else:
        is_owner()

    uuid = await get_uuid(username)
    if uuid is None:
        return await interaction.response.send_message(f"Couldn't find a profile with the name: **{username}**", ephemeral=True)

    if is_whitelisted(username):
        return await interaction.response.send_message(f"**{username}** is already whitelisted.", ephemeral=True)

    send_to_server(f"whitelist add {username}")
    await interaction.response.send_message(f"Added **{username}** to the whitelist.")

# START SERVER COMMAND
@bot.tree.command(name="start", description="Start the Minecraft server")
async def start(interaction: discord.Interaction):
    if not STARTING_OWNER_ONLY:
        is_owner_and_admin()
    else:
        is_owner()

    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send("Starting server...", ephemeral=True)
    subprocess.Popen(["/bin/bash", "./start.sh"], cwd="/home/noahshinar/minecraft_servers/server1")

# RESTART COMMAND
@bot.tree.command(name="restart", description="restarts the server")
async def restart(interaction: discord.Integration):
    if not RESTARTING_OWNER_ONLY:
        is_owner_and_admin()
    else:
        is_owner()

    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send("Stopping server...", ephemeral=True)
    send_to_server(f"stop")
    await interaction.followup.send("Starting server...", ephemeral=True)
    subprocess.Popen(["/bin/bash", START_FILE], cwd=START_DIR)

##################################################################################################################
# STARTUP EVENTS
##################################################################################################################
@bot.event
async def on_ready():
    print("Auto-starting Minecraft server...")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands globally.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

##################################################################################################################
# BOT TOKEN
##################################################################################################################
bot.run(TOKEN)
##################################################################################################################
# BOT TOKEN
##################################################################################################################


