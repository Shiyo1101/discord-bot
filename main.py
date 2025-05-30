import os

import discord
from dotenv import load_dotenv

from lib.client import GenAIClient

load_dotenv()


def main():
    genai_client = GenAIClient(api_key=os.getenv("GENAI_API_KEY"))

    bot_token: str | None = os.getenv("DISCORD_TOKEN")
    if bot_token is None:
        raise ValueError("BOT_TOKEN environment variable not set")

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if message.content:
            res = genai_client.generate_content(message.content)
            await message.channel.send(f"{message.author.mention} {res}")

    client.run(bot_token)


if __name__ == "__main__":
    main()
