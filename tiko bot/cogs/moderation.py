import discord
from discord.ext import commands
import sqlite3

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # KICK
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):

        await member.kick(reason=reason)

        await ctx.send(
            f"👢 {member.mention} was kicked.\nReason: {reason}"
        )

    # BAN
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):

        await member.ban(reason=reason)

        await ctx.send(
            f"🔨 {member.mention} was banned.\nReason: {reason}"
        )

    # TIMEOUT / MUTE
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int):

        await member.timeout(
            discord.utils.utcnow() + discord.timedelta(minutes=minutes)
        )

        await ctx.send(
            f"🔇 {member.mention} muted for {minutes} minutes."
        )

    # WARN
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason"):

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO warnings VALUES (?, ?, ?)",
            (member.id, ctx.author.id, reason)
        )

        conn.commit()
        conn.close()

        await ctx.send(
            f"⚠ {member.mention} warned.\nReason: {reason}"
        )

    # WARNINGS
    @commands.command()
    async def warnings(self, ctx, member: discord.Member):

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT reason FROM warnings WHERE user_id = ?",
            (member.id,)
        )

        warns = cursor.fetchall()

        conn.close()

        if not warns:
            await ctx.send("No warnings.")
            return

        embed = discord.Embed(
            title=f"{member.name}'s Warnings",
            color=discord.Color.red()
        )

        for i, warn in enumerate(warns, start=1):

            embed.add_field(
                name=f"Warning {i}",
                value=warn[0],
                inline=False
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))