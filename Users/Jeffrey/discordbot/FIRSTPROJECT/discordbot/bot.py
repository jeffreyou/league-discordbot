import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
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

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot logged in as {bot.user}")

# Run the bot
bot.run("MTM3OTY1MTI2NTE2ODAxNTQ4MQ.Gn_15W.ihSHysBhByyNLN4082-agYUac9Wq6YrSHHR0k0")
