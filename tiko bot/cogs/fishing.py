import discord
from discord.ext import commands
import sqlite3
import random

class Fishing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.fishes = [
            ("small_fish", 50),
            ("gold_fish", 150),
            ("shark", 500),
            ("boot", 10),
            ("legendary_fish", 1000)
        ]

    # FISH COMMAND
    @commands.command()
    async def fish(self, ctx):

        caught = random.choice(self.fishes)

        fish_name = caught[0]
        fish_value = caught[1]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Check inventory
        cursor.execute(
            "SELECT amount FROM inventory WHERE user_id = ? AND item = ?",
            (ctx.author.id, fish_name)
        )

        existing = cursor.fetchone()

        if existing is None:

            cursor.execute(
                "INSERT INTO inventory (user_id, item, amount) VALUES (?, ?, ?)",
                (ctx.author.id, fish_name, 1)
            )

        else:

            cursor.execute(
                "UPDATE inventory SET amount = amount + 1 WHERE user_id = ? AND item = ?",
                (ctx.author.id, fish_name)
            )

        conn.commit()
        conn.close()

        await ctx.send(
            f"🎣 {ctx.author.mention} caught `{fish_name}`!\n"
            f"💰 Value: `{fish_value}` coins"
        )

    # SELL FISH
    @commands.command()
    async def sellfish(self, ctx, fish_name):

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Fish prices
        fish_prices = dict(self.fishes)

        if fish_name not in fish_prices:

            await ctx.send("❌ Invalid fish.")
            conn.close()
            return

        cursor.execute(
            "SELECT amount FROM inventory WHERE user_id = ? AND item = ?",
            (ctx.author.id, fish_name)
        )

        fish = cursor.fetchone()

        if fish is None:

            await ctx.send(
                "❌ You don't have that fish."
            )

            conn.close()
            return

        amount = fish[0]
        value = fish_prices[fish_name] * amount

        # Remove fish
        cursor.execute(
            "DELETE FROM inventory WHERE user_id = ? AND item = ?",
            (ctx.author.id, fish_name)
        )

        # Add coins
        cursor.execute(
            "UPDATE economy SET coins = coins + ? WHERE user_id = ?",
            (value, ctx.author.id)
        )

        conn.commit()
        conn.close()

        await ctx.send(
            f"💰 Sold `{amount}` {fish_name} for `{value}` coins!"
        )

async def setup(bot):
    await bot.add_cog(Fishing(bot))