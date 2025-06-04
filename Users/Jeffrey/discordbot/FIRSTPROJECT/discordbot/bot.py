from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("C:/Users/Jeffrey/discordbot/FIRSTPROJECT/discordbot/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Set up bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Register slash command (discord.py 2.0+)
@bot.tree.command(name="register", description="Link your Riot ID to your Discord account")
async def register(interaction: discord.Interaction, riot_id: str):
    user_id = str(interaction.user.id)

    # Store Riot ID in Firestore
    db.collection("users").document(user_id).set({
        "riot_id": riot_id,
        "username": str(interaction.user)
    })

    await interaction.response.send_message(f"✅ Riot ID '{riot_id}' has been registered to your account.", ephemeral=True)

# /getriotid implementation, simply returns associated riot id if provided
@bot.tree.command(name="getriotid", description="Display the currently linked Riot ID to your Discord account")
async def getriotid(interaction: discord.Interaction):
    # access firebase database for corresponding id
    user_id = str(interaction.user.id)
    user_ref = db.collection("users").document(user_id) # userid may not exist
    user_contents = user_ref.get()

    if user_contents.exists:  # checks if existing 
        await interaction.response.send_message(f"Riot ID: {user_contents.to_dict()['riot_id']}, Associated Discord account: {user_contents.to_dict()['username']}", ephemeral=True)
    else:
        await interaction.response.send_message(f"Your Riot ID is not registered! Please use the command /register [riot_id] example: /register krysa#0919")


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot logged in as {bot.user}")

# Run the bot
import os
bot.run(os.getenv("DISCORD_TOKEN"))  # avoid leaking discord token

