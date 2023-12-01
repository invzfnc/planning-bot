# bot.py - Bot interface for planning.py

import os
import discord
from discord.ext import commands

from dotenv import load_dotenv

from planning import *

PREFIX = "!"

# Setup token
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Setup bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

help_command = commands.DefaultHelpCommand(no_category = "Commands")

bot = commands.Bot(command_prefix=PREFIX, 
                   intents=intents,
                   help_command=help_command)

cached_data = {}

def retrieve_data(userid):
    """Get UserData instance from cache with user ID"""
    if not userid in cached_data:
        try:
            cached_data[userid] = UserData(userid)
        except FileNotFoundError:
            return False
    return cached_data[userid]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_shutdown():
    print("Logging out")
    for data in cached_data.values():
        data.save()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the permission to use this command.")
    
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("Invalid command.")

def is_guild_owner():
    async def predicate(ctx):
        return ctx.author == ctx.guild.owner
    
    return commands.check(predicate)

@bot.command()
@is_guild_owner()
async def kill(ctx):
    """Shutdown bot"""
    await ctx.send("Logging out.")
    res = await bot.close()

@bot.command()
@is_guild_owner()
async def saveall(ctx):
    """Save all changes to database"""
    for data in cached_data.values():
        data.save()
        await ctx.send(f"{data.userid} saved.")
    await ctx.send("Done.")

@bot.command()
async def add(ctx, date: str = commands.parameter(default=None, description="Date to be added")):
    """Add <date> to database
    <date> format: day/month/year or day-month-year
    <date> can also be "today" or "yesterday" """
    data = retrieve_data(str(ctx.author.id))
    if data:
        if not date:
            await ctx.send("Error: Please specify a date")
            return
        res = data.add(date)
        if res:
            await ctx.send(f"{res} added.")
        else:
            await ctx.send("Invalid date format!")
    else:
        await ctx.send("Profile not found. Please use `init` to setup profile.")

@bot.command()
async def remove(ctx):
    """Remove previous date entry"""
    data = retrieve_data(str(ctx.author.id))
    if data:
        res = data.remove_previous()
        if res:
            await ctx.send("Last date entry removed.")
        else:
            await ctx.send("Nothing to remove for now!")
    else:
        await ctx.send("Profile not found. Please use `init` to setup profile.")

@bot.command()
async def predict(ctx):
    """Calculate and output prediction"""
    data = retrieve_data(str(ctx.author.id))
    if data:
        prediction = data.predict()
        if prediction:
            await ctx.send(prediction)
        else:
            await ctx.send("Insufficient data for calculation!")
    else:
        await ctx.send("Profile not found. Please use `init` to setup profile.")

@bot.command()
async def view(ctx, length: int = commands.parameter(default=7, 
                    description="Number of entries to show. Set -1 for all entries.")):
    """List out entries and data stored in database"""
    data = retrieve_data(str(ctx.author.id))
    if data:
        res = data.display_data(length)
        if res:
            await ctx.send(f"```{res}```")
        else:
            await ctx.send("Nothing to see for now!")
    else:
        await ctx.send("Profile not found. Please use `init` to setup profile.")

@bot.command()
async def save(ctx):
    """Save changes to database"""
    data = retrieve_data(str(ctx.author.id))    
    if data:
        data.save()
        await ctx.send(f"Changes saved.")
    else:
        await ctx.send(f"Profile not found. Please use `init` to setup profile")

@bot.command()
async def init(ctx):
    """Setup your user profile and data for this program"""
    userid = str(ctx.author.id)
    if adduser(userid):
        await ctx.send(f"User `{userid}` initialized.")
    else:
        await ctx.send(f"User `{userid}` already exists.")

@bot.command()
async def whoami(ctx):
    """Show name and ID of caller"""
    await ctx.send(f"You are `{ctx.author.name}`, ID: `{ctx.author.id}`")


if __name__ == "__main__":
    setup()
    bot.run(TOKEN)