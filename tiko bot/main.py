import discord
from discord.ext import commands
import json
import os
import database

# Load config
with open("config.json","r") as f:
    config = json.load(f)

TOKEN = config["token"]
PREFIX = config["prefix"]

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents
)

# Load cogs
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())