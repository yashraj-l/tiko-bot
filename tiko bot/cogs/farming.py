import discord
from discord.ext import commands
import sqlite3
import random

class Farming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.crops = [
            ("wheat", 50),
            ("carrot", 80),
            ("potato", 100),
            ("golden_apple", 500),
            ("pumpkin", 150)
        ]

    # FARM COMMAND
    @commands.command()
    async def farm(self, ctx):

        crop = random.choice(self.crops)

        crop_name = crop[0]
        crop_value = crop[1]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Check inventory
        cursor.execute(
            "SELECT amount FROM inventory WHERE user_id = ? AND item = ?",
            (ctx.author.id, crop_name)
        )

        existing = cursor.fetchone()

        if existing is None:

            cursor.execute(
                "INSERT INTO inventory (user_id, item, amount) VALUES (?, ?, ?)",
                (ctx.author.id, crop_name, 1)
            )

        else:

            cursor.execute(
                "UPDATE inventory SET amount = amount + 1 WHERE user_id = ? AND item = ?",
                (ctx.author.id, crop_name)
            )

        conn.commit()
        conn.close()

        await ctx.send(
            f"🌾 {ctx.author.mention} harvested `{crop_name}`!\n"
            f"💰 Value: `{crop_value}` coins"
        )

    # SELL CROP
    @commands.command()
    async def sellcrop(self, ctx, crop_name):

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        crop_prices = dict(self.crops)

        if crop_name not in crop_prices:

            await ctx.send("❌ Invalid crop.")
            conn.close()
            return

        cursor.execute(
            "SELECT amount FROM inventory WHERE user_id = ? AND item = ?",
            (ctx.author.id, crop_name)
        )

        crop = cursor.fetchone()

        if crop is None:

            await ctx.send(
                "❌ You don't have that crop."
            )

            conn.close()
            return

        amount = crop[0]
        value = crop_prices[crop_name] * amount

        # Remove crops
        cursor.execute(
            "DELETE FROM inventory WHERE user_id = ? AND item = ?",
            (ctx.author.id, crop_name)
        )

        # Add coins
        cursor.execute(
            "UPDATE economy SET coins = coins + ? WHERE user_id = ?",
            (value, ctx.author.id)
        )

        conn.commit()
        conn.close()

        await ctx.send(
            f"💰 Sold `{amount}` {crop_name} for `{value}` coins!"
        )

async def setup(bot):
    await bot.add_cog(Farming(bot))
    