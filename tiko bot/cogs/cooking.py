import discord
from discord.ext import commands
import sqlite3

class Cooking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Recipes
        self.recipes = {
            "fish_stew": {
                "ingredients": {
                    "small_fish": 1,
                    "carrot": 1
                },
                "value": 300
            },

            "golden_soup": {
                "ingredients": {
                    "gold_fish": 1,
                    "golden_apple": 1
                },
                "value": 1200
            },

            "farmer_meal": {
                "ingredients": {
                    "potato": 2,
                    "wheat": 1
                },
                "value": 500
            }
        }

    # COOK COMMAND
    @commands.command()
    async def cook(self, ctx, recipe_name):

        if recipe_name not in self.recipes:

            await ctx.send("❌ Invalid recipe.")
            return

        recipe = self.recipes[recipe_name]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Check ingredients
        for item, amount_needed in recipe["ingredients"].items():

            cursor.execute(
                "SELECT amount FROM inventory WHERE user_id = ? AND item = ?",
                (ctx.author.id, item)
            )

            result = cursor.fetchone()

            if result is None or result[0] < amount_needed:

                await ctx.send(
                    f"❌ You need `{amount_needed}` {item}."
                )

                conn.close()
                return

        # Remove ingredients
        for item, amount_needed in recipe["ingredients"].items():

            cursor.execute(
                "UPDATE inventory SET amount = amount - ? WHERE user_id = ? AND item = ?",
                (amount_needed, ctx.author.id, item)
            )

            # Delete if amount <= 0
            cursor.execute(
                "DELETE FROM inventory WHERE user_id = ? AND item = ? AND amount <= 0",
                (ctx.author.id, item)
            )

        # Add cooked item
        cursor.execute(
            "SELECT amount FROM inventory WHERE user_id = ? AND item = ?",
            (ctx.author.id, recipe_name)
        )

        existing = cursor.fetchone()

        if existing is None:

            cursor.execute(
                "INSERT INTO inventory (user_id, item, amount) VALUES (?, ?, ?)",
                (ctx.author.id, recipe_name, 1)
            )

        else:

            cursor.execute(
                "UPDATE inventory SET amount = amount + 1 WHERE user_id = ? AND item = ?",
                (ctx.author.id, recipe_name)
            )

        conn.commit()
        conn.close()

        await ctx.send(
            f"🍳 {ctx.author.mention} cooked `{recipe_name}`!"
        )

    # RECIPES COMMAND
    @commands.command()
    async def recipes(self, ctx):

        embed = discord.Embed(
            title="🍳 Recipes",
            color=discord.Color.orange()
        )

        for recipe_name, data in self.recipes.items():

            ingredients = "\n".join(
                [
                    f"{item} x{amount}"
                    for item, amount in data["ingredients"].items()
                ]
            )

            embed.add_field(
                name=recipe_name,
                value=f"{ingredients}\n💰 Value: {data['value']}",
                inline=False
            )

        await ctx.send(embed=embed)

    # SELL MEAL
    @commands.command()
    async def sellmeal(self, ctx, meal_name):

        if meal_name not in self.recipes:

            await ctx.send("❌ Invalid meal.")
            return

        value = self.recipes[meal_name]["value"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT amount FROM inventory WHERE user_id = ? AND item = ?",
            (ctx.author.id, meal_name)
        )

        meal = cursor.fetchone()

        if meal is None:

            await ctx.send(
                "❌ You don't have that meal."
            )

            conn.close()
            return

        amount = meal[0]
        total = amount * value

        # Remove meals
        cursor.execute(
            "DELETE FROM inventory WHERE user_id = ? AND item = ?",
            (ctx.author.id, meal_name)
        )

        # Add coins
        cursor.execute(
            "UPDATE economy SET coins = coins + ? WHERE user_id = ?",
            (total, ctx.author.id)
        )

        conn.commit()
        conn.close()

        await ctx.send(
            f"💰 Sold `{amount}` {meal_name} for `{total}` coins!"
        )

async def setup(bot):
    await bot.add_cog(Cooking(bot))
    