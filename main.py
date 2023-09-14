import discord
import os
from discord.ext import commands
from check_role import check_message_for_role
#from bump_reminder import check_bump

from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!',
                      intents=intents)  # Pass the intents argument

#keepBotAlive
from keep_alive import keep_alive
keep_alive()

#status
@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="IM NOT A CAT!!"))
  print("Ava is online and ready!")


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  content = message.content.lower()

  if content == 'hello':
    author_mention = message.author.mention
    await message.channel.send(f"Hey {author_mention}!")

  # Role checking logic
  await check_message_for_role(client, message)

  # Bump reminder logic
  #await check_bump(message)


#token
load_dotenv()
my_secret = os.environ['TOKEN']

client.run(my_secret)
 