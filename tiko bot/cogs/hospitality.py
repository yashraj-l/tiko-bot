import discord
from discord.ext import commands
import sqlite3

class Hospitality(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # WELCOME MESSAGE
    @commands.Cog.listener()
    async def on_member_join(self, member):

        channel = discord.utils.get(
            member.guild.text_channels,
            name="general"
        )

        if channel:

            await channel.send(
                f"🎉 Welcome {member.mention} to the server!\n"
                "Everyone say hello 😄"
            )

    # GREETING DETECTION
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        greetings = [
            "welcome",
            "hello",
            "hi",
            "hey"
        ]

        # Check if someone mentioned a user
        if message.mentions:

            content = message.content.lower()

            if any(word in content for word in greetings):

                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()

                # Check hospitality data
                cursor.execute(
                    "SELECT * FROM hospitality WHERE user_id = ?",
                    (message.author.id,)
                )

                user = cursor.fetchone()

                if user is None:

                    cursor.execute(
                        "INSERT INTO hospitality (user_id, points) VALUES (?, ?)",
                        (message.author.id, 1)
                    )

                else:

                    cursor.execute(
                        "UPDATE hospitality SET points = points + 1 WHERE user_id = ?",
                        (message.author.id,)
                    )

                # Reward economy coins
                cursor.execute(
                    "UPDATE economy SET coins = coins + 50 WHERE user_id = ?",
                    (message.author.id,)
                )

                conn.commit()
                conn.close()

                await message.channel.send(
                    f"🏨 {message.author.mention} earned hospitality rewards!\n"
                    "💰 +50 coins"
                )

    # HOSPITALITY COMMAND
    @commands.command()
    async def hospitality(self, ctx):

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT points FROM hospitality WHERE user_id = ?",
            (ctx.author.id,)
        )

        user = cursor.fetchone()

        conn.close()

        points = 0 if user is None else user[0]

        embed = discord.Embed(
            title=f"{ctx.author.name}'s Hospitality",
            description=f"🏨 Points: {points}",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Hospitality(bot))