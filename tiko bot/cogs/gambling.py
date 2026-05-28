import discord
from discord.ext import commands
import sqlite3
import random
import asyncio

class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # COINFLIP
    # =========================
    @commands.command()
    async def coinflip(self, ctx, bet: int, choice):

        choice = choice.lower()

        if choice not in ["heads", "tails"]:

            await ctx.send(
                "❌ Choose `heads` or `tails`."
            )

            return

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT coins FROM economy WHERE user_id = ?",
            (ctx.author.id,)
        )

        user = cursor.fetchone()

        if user is None or user[0] < bet:

            await ctx.send(
                "💸 You don't have enough coins."
            )

            conn.close()
            return

        result = random.choice(["heads", "tails"])

        # WIN
        if choice == result:

            winnings = bet

            cursor.execute(
                "UPDATE economy SET coins = coins + ? WHERE user_id = ?",
                (winnings, ctx.author.id)
            )

            await ctx.send(
                f"🪙 It landed on **{result}**!\n"
                f"🎉 You won `{winnings}` coins!"
            )

        # LOSE
        else:

            cursor.execute(
                "UPDATE economy SET coins = coins - ? WHERE user_id = ?",
                (bet, ctx.author.id)
            )

            await ctx.send(
                f"💀 It landed on **{result}**!\n"
                f"💸 You lost `{bet}` coins."
            )

        conn.commit()
        conn.close()

    # =========================
    # SLOT MACHINE
    # =========================
    @commands.command()
    async def slots(self, ctx, bet: int):

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT coins FROM economy WHERE user_id = ?",
            (ctx.author.id,)
        )

        user = cursor.fetchone()

        if user is None or user[0] < bet:

            await ctx.send(
                "💸 You don't have enough coins."
            )

            conn.close()
            return

        emojis = ["🍒", "🍋", "🍉", "⭐", "💎"]

        slot1 = random.choice(emojis)
        slot2 = random.choice(emojis)
        slot3 = random.choice(emojis)

        result = f"{slot1} | {slot2} | {slot3}"

        # JACKPOT
        if slot1 == slot2 == slot3:

            winnings = bet * 4

            cursor.execute(
                "UPDATE economy SET coins = coins + ? WHERE user_id = ?",
                (winnings, ctx.author.id)
            )

            await ctx.send(
                f"🎰 {result}\n"
                f"💎 JACKPOT!\n"
                f"🎉 You won `{winnings}` coins!"
            )

        else:

            cursor.execute(
                "UPDATE economy SET coins = coins - ? WHERE user_id = ?",
                (bet, ctx.author.id)
            )

            await ctx.send(
                f"🎰 {result}\n"
                f"💀 You lost `{bet}` coins."
            )

        conn.commit()
        conn.close()

    # =========================
    # DICE
    # =========================
    @commands.command()
    async def dice(self, ctx, bet: int):

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT coins FROM economy WHERE user_id = ?",
            (ctx.author.id,)
        )

        user = cursor.fetchone()

        if user is None or user[0] < bet:

            await ctx.send(
                "💸 You don't have enough coins."
            )

            conn.close()
            return

        player_roll = random.randint(1, 6)
        bot_roll = random.randint(1, 6)

        # WIN
        if player_roll > bot_roll:

            winnings = bet * 2

            cursor.execute(
                "UPDATE economy SET coins = coins + ? WHERE user_id = ?",
                (winnings, ctx.author.id)
            )

            await ctx.send(
                f"🎲 You rolled `{player_roll}`\n"
                f"🤖 Bot rolled `{bot_roll}`\n"
                f"🎉 You won `{winnings}` coins!"
            )

        # LOSE
        elif player_roll < bot_roll:

            cursor.execute(
                "UPDATE economy SET coins = coins - ? WHERE user_id = ?",
                (bet, ctx.author.id)
            )

            await ctx.send(
                f"🎲 You rolled `{player_roll}`\n"
                f"🤖 Bot rolled `{bot_roll}`\n"
                f"💀 You lost `{bet}` coins."
            )

        # TIE
        else:

            await ctx.send(
                f"🎲 Both rolled `{player_roll}`!\n"
                f"😮 It's a tie."
            )

        conn.commit()
        conn.close()

    # =========================
    # RUSSIAN ROULETTE
    # =========================
    @commands.command()
    async def roulette(self, ctx, bet: int):

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT coins FROM economy WHERE user_id = ?",
            (ctx.author.id,)
        )

        user = cursor.fetchone()

        if user is None or user[0] < bet:

            await ctx.send(
                "💸 You don't have enough coins."
            )

            conn.close()
            return

        dramatic_messages = [
            "😨 spinning the chamber...",
            "🔫 loading the revolver...",
            "💀 this could go very wrong...",
            "👀 everyone watches silently...",
            "😰 tension fills the room..."
        ]

        await ctx.send(
            random.choice(dramatic_messages)
        )

        await asyncio.sleep(2)

        # 1/6 chance
        bullet = random.randint(1, 6)

        # LOSE
        if bullet == 1:

            cursor.execute(
                "UPDATE economy SET coins = coins - ? WHERE user_id = ?",
                (bet, ctx.author.id)
            )

            await ctx.send(
                f"💥 BANG!\n"
                f"💀 {ctx.author.mention} lost `{bet}` coins..."
            )

        # WIN
        else:

            winnings = bet * 3

            cursor.execute(
                "UPDATE economy SET coins = coins + ? WHERE user_id = ?",
                (winnings, ctx.author.id)
            )

            await ctx.send(
                f"😮 CLICK...\n"
                f"🎉 {ctx.author.mention} survived and won `{winnings}` coins!"
            )

        conn.commit()
        conn.close()

async def setup(bot):
    await bot.add_cog(Gambling(bot))