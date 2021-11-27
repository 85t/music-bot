import discord
import json
import youtube_dl
from discord.ext import commands

with open("config.json") as f:
    jsda = json.load(f)
    token = jsda["TOKEN"]
    prefix = jsda["PREFIX"]

client = commands.Bot(command_prefix=prefix)

@client.event
async def on_ready():
    print(f"""
    
MUSIC BOT

Tag: {client.user}
Prefix: {client.command_prefix}
    
Commands:
{client.command_prefix}play <youtube_url>
{client.command_prefix}pause
{client.command_prefix}resume
    
made by github.com/85t

OUTPUT:
    """)

@client.command()
async def play(ctx,url):
    if ctx.author.voice is None:
        print("You arent in the voice channel!")
    else:
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
            print(f"Joined to {ctx.author.voice.channel.name}!")
        else:
            await ctx.voice_client.move_to(ctx.author.voice.channel)
            print(f"Joined to {ctx.author.voice.channel.name}!")

        print(f"Loading {url} ...")

        with youtube_dl.YoutubeDL({
            'format': "bestaudio"
        }) as ydl:
            info = ydl.extract_info(url,download=False)
            url2 = info["formats"][0]["url"]
            source = await discord.FFmpegOpusAudio.from_probe(url2,**{
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
            })
            ctx.voice_client.play(source)
            print(f"Now playing: {url}")

@client.command()
async def pause(ctx):
    ctx.voice_client.pause()
    print("Paused!")

@client.command()
async def resume(ctx):
    ctx.voice_client.resume()
    print("Resumed!")

if __name__ == "__main__":
    client.run(token)
