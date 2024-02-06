import datetime
import os
from discord.ext import commands, tasks
import discord
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
Channel_ID = 1204237105048588298
MAX_SESSION_TIME = 30

@dataclass
class MySession:
    is_active: bool = False
    start_time: int = 0

bot = commands.Bot(command_prefix = ".", intents=discord.Intents.all())
session = MySession()

@bot.event
async def on_ready():
    print("Hello! Bot is ready to work!")
    channel = bot.get_channel(Channel_ID)
    await channel.send("Hello! I am ready!")

@tasks.loop(minutes=MAX_SESSION_TIME, count=2)
async def break_reminder():

    #ignoring first execution
    if break_reminder.current_loop==0:
        return
    
    channel = bot.get_channel(Channel_ID)
    await channel.send(f"**Take a break!!** Your session has been running for {MAX_SESSION} minutes.")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! How can I help you? \n"
                   "To know what commands I know, type '.command'")
    
@bot.command()
async def command(ctx):
    await ctx.send("add: to add numbers \n"
                   "start: to start a session")
    

@bot.command()
async def add(ctx, *arr):
    result = 0
    for i in arr:
        result += int(i)

@bot.command()
async def start (ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return
    
    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime ("%H:%M:%S")
    break_reminder.start()
    await ctx.send(f"New session started at {human_readable_time}")

@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("No session is active!")
        return
    
    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    break_reminder.stop()
    await ctx.send(f"Session ended after {human_readable_duration}")



bot.run(TOKEN)
