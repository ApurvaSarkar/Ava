

import discord
import asyncio

bump_channel_id = 947359201288671303 
general_channel_id = 837386985638985829 
disboard_bot_id = 302050872383242240
sleep_time = 7200  #2hr


async def check_bump(message):
  if isinstance(message, discord.Message):
    if message.channel.id == bump_channel_id and message.author.id == disboard_bot_id:
      if len(message.embeds) > 0:
        embed = message.embeds[0]  
        if "Bump done! :thumbsup:" in embed.description:
          
          print("Bot is matched")
          bump_channel = message.guild.get_channel(bump_channel_id)
          general_channel = message.guild.get_channel(general_channel_id)

          if bump_channel and general_channel:
            if message.reference is not None and message.reference.resolved:
              interaction_user = message.reference.resolved.author  
              await general_channel.send(
                f"Thank you {interaction_user.mention} for bumping!")
            else:
              print(
                "Unable to determine the user who used the application command."
              )

            

      # Delete the messages in general channel
      async for msg in general_channel.history():
        if msg.author == message.guild.me and msg.content == "Server is ready to be bumped!":
          await msg.delete()
          break

      # Delete the messages in bump channel
      async for msg in bump_channel.history():
        if msg.author == message.guild.me and msg.content == "Use `/bump` to bump the server!":
          await msg.delete()
          break

      # Replace the emojis one after the other
      check_mark_emoji = "✅"
      cross_mark_emoji = "❌"
      channel_name = "✵-𝑫𝒊𝒔𝒃𝒐𝒂𝒓𝒅-✵"

      await bump_channel.edit(name=f"{check_mark_emoji} {channel_name}")
      await asyncio.sleep(sleep_time)  # Delay for 2 hours
      await bump_channel.edit(name=f"{cross_mark_emoji} {channel_name}")

      await general_channel.send("Server is ready to be bumped!")
      await bump_channel.send("Use `/bump` to bump the server!")

    
