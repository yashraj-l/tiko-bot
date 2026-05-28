import discord
from discord.ext import commands
import sqlite3
import random

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return
        if message.channel.name != "𓏼﹒𝐋eveling﹒﹒ᯓ✮ˎˊ˗":
            return
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Check user
        cursor.execute(
            "SELECT * FROM economy WHERE user_id = ?",
            (message.author.id,)
        )

        user = cursor.fetchone()

        if user is None:
            cursor.execute(
                "INSERT INTO economy (user_id, coins, xp, level) VALUES (?, ?, ?, ?)",
                (message.author.id, 0, 0, 1)
            )
            conn.commit()

            cursor.execute(
                "SELECT * FROM economy WHERE user_id = ?",
                (message.author.id,)
            )

            user = cursor.fetchone()

        # Give XP
        xp_gain = random.randint(5, 15)

        new_xp = user[2] + xp_gain
        current_level = user[3]

        # Level formula
        required_xp = current_level * 100

        # Level up
        if new_xp >= required_xp:

            new_level = current_level + 1
            reward = new_level * 100

            cursor.execute(
                "UPDATE economy SET level = ?, xp = 0, coins = coins + ? WHERE user_id = ?",
                (new_level, reward, message.author.id)
            )

            await message.channel.send(
                f"🎉 {message.author.mention} leveled up to **Level {new_level}**!\n"
                f"💰 Reward: `{reward}` coins"
            )

        else:
            cursor.execute(
                "UPDATE economy SET xp = ? WHERE user_id = ?",
                (new_xp, message.author.id)
            )

        conn.commit()
        conn.close()

    # RANK COMMAND
    @commands.command()
    async def rank(self, ctx):

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT coins, xp, level FROM economy WHERE user_id = ?",
            (ctx.author.id,)
        )

        user = cursor.fetchone()

        conn.close()

        if user is None:
            await ctx.send("No data found.")
            return

        embed = discord.Embed(
            title=f"{ctx.author.name}'s Rank",
            color=discord.Color.blue()
        )

        embed.add_field(name="💰 Coins", value=user[0])
        embed.add_field(name="⭐ XP", value=user[1])
        embed.add_field(name="⬆ Level", value=user[2])

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Levels(bot))
    