# bot.py - Bot interface for planning.py

import os
import discord
from discord.ext import commands

from dotenv import load_dotenv

PREFIX = "!"

# Setup token
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Setup bot
intents = discord.Intents.default()
intents.message_content = True

help_command = commands.DefaultHelpCommand(no_category = "Commands")

bot = commands.Bot(command_prefix=PREFIX, 
                   intents=intents,
                   help_command=help_command)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.command()
async def add(ctx, date: str):
    """Add <date> to database
    <date> format: day/month/year or day-month-year
    <date> can also be "today" or "yesterday" """
    pass

@bot.command()
async def remove(ctx):
    """Remove previous date entry"""
    pass

@bot.command()
async def predict(ctx):
    """Calculate and output prediction"""
    pass

@bot.command()
async def view(ctx):
    """List out entries and data stored in database"""
    pass

@bot.command()
async def whoami(ctx):
    """Show name and ID of caller"""
    await ctx.send(f"You are `{ctx.author.name}`, ID: `{ctx.author.id}`")
    
bot.run(TOKEN)