import discord
from discord.ext import commands
import requests

class Actions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_action(self, ctx, member, action):

        url = f"https://nekos.best/api/v2/{action}"

        response = requests.get(url).json()

        gif = response["results"][0]["url"]

        embed = discord.Embed(
            description=f"✨ {ctx.author.mention} {action}s {member.mention}!",
            color=discord.Color.purple()
        )

        embed.set_image(url=gif)

        await ctx.send(embed=embed)

    # HUG
    @commands.command()
    async def hug(self, ctx, member: discord.Member):

        await self.send_action(ctx, member, "hug")

    # KISS
    @commands.command()
    async def kiss(self, ctx, member: discord.Member):

        await self.send_action(ctx, member, "kiss")

    # SLAP
    @commands.command()
    async def slap(self, ctx, member: discord.Member):

        await self.send_action(ctx, member, "slap")

    # PAT
    @commands.command()
    async def pat(self, ctx, member: discord.Member):

        await self.send_action(ctx, member, "pat")

    # POKE
    @commands.command()
    async def poke(self, ctx, member: discord.Member):

        await self.send_action(ctx, member, "poke")

    # HIGHFIVE
    @commands.command()
    async def highfive(self, ctx, member: discord.Member):

        await self.send_action(ctx, member, "highfive")

    # CUDDLE
    @commands.command()
    async def cuddle(self, ctx, member: discord.Member):

        await self.send_action(ctx, member, "cuddle")

    # BITE
    @commands.command()
    async def bite(self, ctx, member: discord.Member):

        await self.send_action(ctx, member, "bite")

    # FEED
    @commands.command()
    async def feed(self, ctx, member: discord.Member):

        await self.send_action(ctx, member, "feed")

    # WAVE/BYE
    @commands.command()
    async def bye(self, ctx, member: discord.Member):

        await self.send_action(ctx, member, "wave")

async def setup(bot):
    await bot.add_cog(Actions(bot))