import asyncio
import os

import discord
from dotenv import load_dotenv

from lib.client import GenAIClient, VoiceVoxClient
from lib.context import load_context
from lib.server import keep_alive

load_dotenv()
keep_alive()


def main():
    context = load_context()
    genai_client = GenAIClient(api_key=os.getenv("GENAI_API_KEY"), context=context)
    voicevox_client = VoiceVoxClient(
        api_url=os.getenv("VOICEVOX_API_URL"),
        api_key=os.getenv("VOICEVOX_API_KEY"),
    )

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

        # ずんだもんがメンションされた場合に応答する
        if client.user in message.mentions and message.content:
            res = genai_client.generate_content(user_input=message.content)
            await message.channel.send(f"{message.author.mention} {res}")

            # VCに参加して再生
            if message.author.voice and message.author.voice.channel:
                # 音声合成のリクエスト
                voice_data = voicevox_client.generate_speech(
                    text=res,
                    speaker_id=1,
                )
                if not voice_data:
                    await message.channel.send("☠️音声の生成に失敗したのだ。")
                    raise RuntimeError("Failed to generate voice data")

                # 一時的なファイルとして保存
                filename = "output.wav"
                with open(filename, "wb") as f:
                    f.write(voice_data)

                channel = message.author.voice.channel

                try:
                    vc = await channel.connect()
                except discord.ClientException:
                    vc = message.guild.voice_client
                    await message.channel.send(
                        "⚠️すでにボイスチャンネルに参加しているのだ。"
                    )
                    raise RuntimeError("Already connected to voice channel")

                if vc and vc.is_connected():
                    vc.play(discord.FFmpegOpusAudio(filename))

                    while vc.is_playing():
                        await asyncio.sleep(1)
                    await vc.disconnect()
                else:
                    await message.channel.send(
                        "☠️ボイスチャンネルの接続に失敗したのだ。"
                    )
                    raise RuntimeError("Failed to connect to voice channel")
            else:
                await message.channel.send(
                    "※ボイスチャンネルに参加していると、ずんだもんがしゃべるのだ。"
                )

            return

    client.run(bot_token)


if __name__ == "__main__":
    main()
