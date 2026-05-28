import discord
from discord.ext import commands
from groq import Groq
import json
import sqlite3
import random
import asyncio

# LOAD CONFIG
with open("config.json") as f:
    config = json.load(f)

GROQ_KEY = config["groq_api_key"]

client = Groq(api_key=GROQ_KEY)

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Emotion states
        self.emotions = [
            "happy",
            "playful",
            "excited",
            "caring",
            "curious",
            "protective",
            "chaotic",
            "sleepy",
            "friendly"
        ]

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        # =========================
        # MEMORY SAVE SYSTEM
        # =========================

        memory_keywords = [
            "i like",
            "i love",
            "my favorite",
            "i enjoy",
            "my hobby is",
            "i hate",
            "my dream is",
            "i want",
            "i am",
            "my birthday"
        ]

        content_lower = message.content.lower()

        if any(keyword in content_lower for keyword in memory_keywords):

            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                user_id INTEGER,
                fact TEXT
            )
            """)

            cursor.execute(
                "INSERT INTO memory (user_id, fact) VALUES (?, ?)",
                (message.author.id, message.content)
            )

            conn.commit()
            conn.close()

            await message.channel.send(
                "🧠 I'll remember that 😄"
            )

        # =========================
        # AI CHAT
        # =========================

        if self.bot.user in message.mentions:

            # Typing effect
            async with message.channel.typing():

                await asyncio.sleep(1)

                # Load memories
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()

                cursor.execute("""
                CREATE TABLE IF NOT EXISTS memory (
                    user_id INTEGER,
                    fact TEXT
                )
                """)

                cursor.execute(
                    """
                    SELECT fact FROM memory
                    WHERE user_id = ?
                    ORDER BY ROWID DESC
                    LIMIT 10
                    """,
                    (message.author.id,)
                )

                memories = cursor.fetchall()

                conn.close()

                memory_text = "\n".join(
                    [m[0] for m in memories]
                )

                # Random emotions
                emotion = random.choice(self.emotions)

                # Remove mention
                user_message = message.content.replace(
                    f"<@{self.bot.user.id}>",
                    ""
                )

                user_message = user_message.strip()

                try:

                    completion = client.chat.completions.create(

                        model="llama-3.1-8b-instant",

                        messages=[

                            {
                                "role": "system",

                                "content": f"""
You are a highly emotional, human-like Discord bot.

Your current emotion is: {emotion}

PERSONALITY:
-PERSONALITY:
- Talk naturally like a real online friend.
- Be expressive and emotional.
- Sometimes be goofy and chaotic.
- Sometimes be wholesome and caring.
- Love waffles, gaming, memes, and community.
- Use emojis naturally but not excessively.
- NEVER sound robotic.
- React emotionally depending on context.
- Keep replies short and natural.
- Usually reply in 1-4 lines.
- Talk like a real Discord user.
- Avoid long paragraphs unless needed.
- Sometimes use short casual messages.
- Be expressive but concise.
- Sometimes use lowercase texting.
- Sometimes say stuff casually like:
  "lmao"
  "😭"
  "fr"
  "nah"
  "yooo"

EMOTIONAL BEHAVIOR:
- If user is sad → comfort warmly.
- If user is excited → match their energy.
- If user is angry → stay calm and caring.
- If user jokes → joke back.
- If user talks daily → act familiar with them.
- If user compliments you → become happy/excited.

MEMORIES ABOUT USER:
{memory_text}

You remember users and reference memories naturally.

Reply like a REAL Discord friend.
"""
                            },

                            {
                                "role": "user",
                                "content": user_message
                            }
                        ],

                        temperature=0.9,
                        max_tokens=100
                    )

                    reply = completion.choices[0].message.content
                    # SERVER EMOJIS
                    guild_emojis = []
                    if message.guild:
                        for emoji in message.guild.emojis:
                            guild_emojis.append(str(emoji))
                    # Random emoji sometimes
                    if guild_emojis and random.randint(1, 3) == 1:
                        reply += " " + random.choice(guild_emojis)    
                    # Discord message limit
                    if len(reply) > 1900:
                        reply = reply[:1900]

                    await message.reply(reply)

                except Exception as e:

                    await message.channel.send(
                        f"⚠ AI Error: {e}"
                    )

async def setup(bot):
    await bot.add_cog(AI(bot))