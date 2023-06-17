import discord
import os
from discord.ext import commands

from dotenv import load_dotenv
from role_checker import check_message_for_role

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)  # Pass the intents argument

@client.event
async def on_ready():
    print("Ava is online and ready!")

@client.event
async def on_message(message):
    if message.author == client.user: #checks if the message send by a bot or not
        return

    content = message.content.lower()

    if content == 'Hello':
        author_mention = message.author.mention
        await message.channel.send(f"Hey {author_mention}!")

    #role_checker.py
    await check_message_for_role(client, message)
    return  # Stop further processing of the message

load_dotenv()
token = os.getenv("TOKEN")
client.run(token)
