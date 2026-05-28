import discord
from discord.ext import commands
import sqlite3
import random
from datetime import datetime, timedelta

cooldowns = {}

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Get user
    def get_user(self, user_id):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM economy WHERE user_id = ?",
            (user_id,)
        )

        user = cursor.fetchone()

        if user is None:
            cursor.execute(
                "INSERT INTO economy (user_id, coins, xp, level) VALUES (?, ?, ?, ?)",
                (user_id, 0, 0, 1)
            )
            conn.commit()

            cursor.execute(
                "SELECT * FROM economy WHERE user_id = ?",
                (user_id,)
            )

            user = cursor.fetchone()

        conn.close()
        return user

    # BALANCE COMMAND
    @commands.command()
    async def balance(self, ctx):
        user = self.get_user(ctx.author.id)

        await ctx.send(
            f"💰 {ctx.author.mention}, you have `{user[1]}` coins."
        )

    # DAILY COMMAND
    @commands.command()
    async def daily(self, ctx):

        user_id = ctx.author.id

        if user_id in cooldowns:
            remaining = cooldowns[user_id] - datetime.now()

            if remaining.total_seconds() > 0:
                hours = int(remaining.total_seconds() // 3600)

                await ctx.send(
                    f"⏳ Come back in {hours} hours."
                )
                return

        reward = random.randint(100, 500)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        self.get_user(user_id)

        cursor.execute(
            "UPDATE economy SET coins = coins + ? WHERE user_id = ?",
            (reward, user_id)
        )

        conn.commit()
        conn.close()

        cooldowns[user_id] = datetime.now() + timedelta(hours=24)

        await ctx.send(
            f"🎁 {ctx.author.mention} got `{reward}` coins!"
        )

    # LEADERBOARD
    @commands.command()
    async def leaderboard(self, ctx):

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT user_id, coins FROM economy ORDER BY coins DESC LIMIT 10"
        )

        users = cursor.fetchall()

        conn.close()

        embed = discord.Embed(
            title="🏆 Richest Players",
            color=discord.Color.gold()
        )

        for i, user in enumerate(users, start=1):

            member = ctx.guild.get_member(user[0])

            if member:
                embed.add_field(
                    name=f"{i}. {member.name}",
                    value=f"💰 {user[1]} coins",
                    inline=False
                )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))