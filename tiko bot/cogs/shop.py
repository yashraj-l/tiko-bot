import discord
from discord.ext import commands
import sqlite3

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # SHOP COMMAND
    @commands.command()
    async def shop(self, ctx):

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT item, price FROM shop"
        )

        items = cursor.fetchall()

        conn.close()

        embed = discord.Embed(
            title="🛒 Bot Shop",
            color=discord.Color.gold()
        )

        for item in items:

            embed.add_field(
                name=item[0],
                value=f"💰 {item[1]} coins",
                inline=False
            )

        await ctx.send(embed=embed)

    # BUY COMMAND
    @commands.command()
    async def buy(self, ctx, item_name):

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Check shop item
        cursor.execute(
            "SELECT price FROM shop WHERE item = ?",
            (item_name,)
        )

        item = cursor.fetchone()

        if item is None:
            await ctx.send("❌ Item not found.")
            conn.close()
            return

        price = item[0]

        # Check balance
        cursor.execute(
            "SELECT coins FROM economy WHERE user_id = ?",
            (ctx.author.id,)
        )

        user = cursor.fetchone()

        if user is None or user[0] < price:

            await ctx.send(
                "💸 You don't have enough coins."
            )

            conn.close()
            return

        # Remove coins
        cursor.execute(
            "UPDATE economy SET coins = coins - ? WHERE user_id = ?",
            (price, ctx.author.id)
        )

        # Add item to inventory
        cursor.execute(
            "SELECT amount FROM inventory WHERE user_id = ? AND item = ?",
            (ctx.author.id, item_name)
        )

        existing = cursor.fetchone()

        if existing is None:

            cursor.execute(
                "INSERT INTO inventory (user_id, item, amount) VALUES (?, ?, ?)",
                (ctx.author.id, item_name, 1)
            )

        else:

            cursor.execute(
                "UPDATE inventory SET amount = amount + 1 WHERE user_id = ? AND item = ?",
                (ctx.author.id, item_name)
            )

        conn.commit()
        conn.close()

        await ctx.send(
            f"🛒 {ctx.author.mention} bought `{item_name}` for `{price}` coins!"
        )

async def setup(bot):
    await bot.add_cog(Shop(bot))