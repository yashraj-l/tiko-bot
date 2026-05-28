import discord
from discord.ext import commands, tasks
import sqlite3
import random

class Waffles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.waffle_drop.start()

    # AUTO WAFFLE DROP
    @tasks.loop(minutes=5)
    async def waffle_drop(self):

        for guild in self.bot.guilds:

            for channel in guild.text_channels:

                if channel.name == "general":

                    await channel.send(
                        "🧇 A fresh batch of waffles appeared!\nUse `!collect` to grab one!"
                    )

                    break

    # COLLECT WAFFLE
    @commands.command()
    async def collect(self, ctx):

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # check inventory
        cursor.execute(
            "SELECT amount FROM inventory WHERE user_id = ? AND item = ?",
            (ctx.author.id, "waffle")
        )

        item = cursor.fetchone()

        if item is None:

            cursor.execute(
                "INSERT INTO inventory (user_id, item, amount) VALUES (?, ?, ?)",
                (ctx.author.id, "waffle", 1)
            )

        else:

            cursor.execute(
                "UPDATE inventory SET amount = amount + 1 WHERE user_id = ? AND item = ?",
                (ctx.author.id, "waffle")
            )

        conn.commit()
        conn.close()

        await ctx.send(
            f"🧇 {ctx.author.mention} collected a waffle!"
        )

    # INVENTORY COMMAND
    @commands.command()
    async def inventory(self, ctx):

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT item, amount FROM inventory WHERE user_id = ?",
            (ctx.author.id,)
        )

        items = cursor.fetchall()

        conn.close()

        if not items:
            await ctx.send("🎒 Your inventory is empty.")
            return

        embed = discord.Embed(
            title=f"{ctx.author.name}'s Inventory",
            color=discord.Color.orange()
        )

        for item in items:

            embed.add_field(
                name=item[0],
                value=f"x{item[1]}",
                inline=False
            )

        await ctx.send(embed=embed)

    # SELL WAFFLES
    @commands.command()
    async def sellwaffles(self, ctx):

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT amount FROM inventory WHERE user_id = ? AND item = ?",
            (ctx.author.id, "waffle")
        )

        waffles = cursor.fetchone()

        if waffles is None:

            await ctx.send("❌ You have no waffles.")
            conn.close()
            return

        amount = waffles[0]
        coins_earned = amount * 50

        # remove waffles
        cursor.execute(
            "DELETE FROM inventory WHERE user_id = ? AND item = ?",
            (ctx.author.id, "waffle")
        )

        # add coins
        cursor.execute(
            "UPDATE economy SET coins = coins + ? WHERE user_id = ?",
            (coins_earned, ctx.author.id)
        )

        conn.commit()
        conn.close()

        await ctx.send(
            f"💰 Sold `{amount}` waffles for `{coins_earned}` coins!"
        )

async def setup(bot):
    await bot.add_cog(Waffles(bot))
