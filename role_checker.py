import discord
import asyncio

warning_limit = 3  # Number of warnings before kicking the user
log_channel_id = 1119652152521015386  # Replace with your desired log channel ID
ignored_users = set()  # Set to store ignored user IDs
ignore_join_time = 5  # Ignore join events for 10 seconds
delete_delay = 5  # Delay in seconds before deleting the bot's warning message

warnings = {}  # Dictionary to store user warnings

async def check_message_for_role(client, message):
    if message.author.bot or message.author.id in ignored_users:
        return

    role_ids = [1119652240681078835, 1119652300290543636, 1119652348323700857, 1119652402446995538]  # Replace with your desired role IDs

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
        warning_message = await send_warning_message(message.channel, author_mention, remaining_warnings)

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
    await user.kick(reason="Reached warning limit")  # Kicks the user from the server

    guild = user.guild
    log_channel = discord.utils.get(guild.text_channels, id=log_channel_id)
    if log_channel:
        await log_channel.send(f"{user.mention} has been kicked due to reaching the warning limit!")
    else:
        print("Log channel not found. Please check the provided log channel ID.")

async def send_warning_message(channel, author_mention, remaining_warnings):
    warning_message = await channel.send(f"{author_mention}, you don't have the required role! You have {remaining_warnings} warning(s) remaining.")
    return warning_message

async def delete_message_after_delay(message, delay):
    await asyncio.sleep(delay)
    await message.delete()
