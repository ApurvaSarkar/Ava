import discord
import asyncio

warning_limit = 3  # Number of warnings before kicking the user
log_channel_id = 948160684896681994  # Replace with desired log channel ID
ignored_users = set()  # Set to store ignored user IDs
ignore_join_time = 5  # Ignore join events for 10 seconds
delete_delay = 30  # Delay in seconds before deleting the bot's warning message

warnings = {}  # Dictionary to store user warnings


async def check_message_for_role(client, message):
  if message.author.bot or message.author.id in ignored_users:
    return

  role_ids = [
    1118045469516505201, 1118045651213746237, 1118045706108813394,
    1118045751260499978, 1118045793354530876, 1118045874283610172,
    1118045930218860594, 1118045980114305155
  ]

  # Check if user joined within the ignore join time
  if not has_ignore_join_expired(message.author):
    return

  await asyncio.sleep(ignore_join_time)  # Delay for ignore join time

  has_required_role = False
  for role_id in role_ids:
    has_role = any(role.id == role_id for role in message.author.roles)
    if has_role:
      has_required_role = True
      break

  if not has_required_role:
    author_mention = message.author.mention
    user_warnings = get_user_warnings(message.author)
    remaining_warnings = warning_limit - user_warnings
    warning_message = await send_warning_message(message.channel,
                                                 author_mention,
                                                 remaining_warnings)

    if user_warnings >= warning_limit:
      await kick_user(message.author)
      reset_user_warnings(message.author)  # Reset warnings when user is kicked
    else:
      increment_user_warnings(message.author)

    await delete_message_after_delay(warning_message, delete_delay)


def get_user_warnings(user):
  # Retrieve the number of warnings for the user from the warnings dictionary
  # Return 0 if no warnings found
  return warnings.get(user.id, 0)


def increment_user_warnings(user):
  # Increment the number of warnings for the user in the warnings dictionary
  warnings[user.id] = get_user_warnings(user) + 1


def reset_user_warnings(user):
  # Reset the user's warnings in the warnings dictionary
  if user.id in warnings:
    del warnings[user.id]


def has_ignore_join_expired(user):
  # Check if the user joined more than ignore_join_time seconds ago
  # Replace this logic with your own implementation
  return True


async def kick_user(user):
  invite_link = await user.guild.text_channels[0].create_invite(
    reason="Kicked user rejoin", max_uses=1)

  try:
    await user.send(
      f"You have been kicked from the server. If it was a mistake, you can rejoin using the following invite link: {invite_link}"
    )
  except discord.Forbidden:
    print(f"Failed to send a private message to {user} (ID: {user.id}).")

  await user.kick(reason="Reached warning limit"
                  )  # Kicks the user from the server

  guild = user.guild
  log_channel = discord.utils.get(guild.text_channels, id=log_channel_id)
  if log_channel:
    await log_channel.send(
      f"{user.mention} has been kicked due to reaching the warning limit!")
  else:
    print("Log channel not found. Please check the provided log channel ID.")


async def send_warning_message(channel, author_mention, remaining_warnings):
  warning_message = await channel.send(
    f"{author_mention}, you don't have Age-role! Take it from <#952278616803274772>. You have {remaining_warnings} warning(s) remaining."
  )
  return warning_message

async def delete_message_after_delay(message, delay):
  await asyncio.sleep(delay)
  await message.delete()
