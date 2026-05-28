import asyncio
import discord
from discord.ext import commands

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ticket(self, ctx):

        guild = ctx.guild

        # Check if category exists
        category = discord.utils.get(
            guild.categories,
            name="Tickets"
        )

        if category is None:

            category = await guild.create_category(
                "Tickets"
            )

        # Create channel name
        channel_name = f"ticket-{ctx.author.name}"

        # Prevent duplicates
        existing = discord.utils.get(
            guild.channels,
            name=channel_name
        )

        if existing:
            await ctx.send(
                "❌ You already have an open ticket."
            )
            return

        # Permissions
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                read_messages=False
            ),

            ctx.author: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True
            ),

            guild.me: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True
            )
        }

        # Create ticket channel
        channel = await guild.create_text_channel(
            channel_name,
            category=category,
            overwrites=overwrites
        )

        await channel.send(
            f"🎫 Welcome {ctx.author.mention}!\n"
            "Support will be with you shortly."
        )

        await ctx.send(
            f"✅ Ticket created: {channel.mention}"
        )

    # CLOSE COMMAND
    @commands.command()
    async def close(self, ctx):

        if "ticket-" in ctx.channel.name:

            await ctx.send(
                "🔒 Closing ticket in 5 seconds..."
            )

            await asyncio.sleep(5)

            await ctx.channel.delete()

async def setup(bot):
    await bot.add_cog(Tickets(bot))