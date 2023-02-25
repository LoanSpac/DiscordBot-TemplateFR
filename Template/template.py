import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import asyncio

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

print("Lancement du bot...")
bot.remove_command("help")

@bot.event
async def on_ready():
    print("Bot lancé!")
    await bot.change_presence(status=discord.Status.online)
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="help")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message("Voici la commande help.", ephemeral=True)
    user = interaction.user
    embed = discord.Embed(title = "Help", description = f"{user.mention}, voici la liste des commands slash :\n> hello\n> ping\n> test_button\n> fruts_dropdown", color = 0xffffff)
    embed.set_footer(text = "Template Bot")
    await interaction.channel.send(embed=embed)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Heyyy", ephemeral=True)

@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong !\n> **{round(bot.latency *1000)}** ms", ephemeral=True)

class TestButton(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="📌 Test", style=discord.ButtonStyle.red)
    async def testBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Vous avez appuyez !", ephemeral=True)

@bot.tree.command(name="test_button")
async def fruts_dropdown(interaction: discord.Interaction):
    await interaction.response.send_message("Boutton créé !", ephemeral=True)
    await interaction.channel.send("Test boutton 📌", view=TestButton())

class frutsDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="🍎 Pomme", description='Tu es team pomme ?'),
            discord.SelectOption(label="🍓 Fraise", description='Tu es team fraise ?'),
            discord.SelectOption(label="🍌 Banane", description='Tu es team banane ?'),
        ]

        super().__init__(placeholder="🍍 Choisi ton fruit !", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Vous avez choisi la team {self.values[0]} !", ephemeral=True)
  
class frutsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(frutsDropdown())

@bot.tree.command(name="fruts_dropdown")
async def fruts_dropdown(interaction: discord.Interaction):
    await interaction.response.send_message("Dropdown créé !", ephemeral=True)
    await interaction.channel.send("Choisi ton fruit 🍍 :", view=frutsView())

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)