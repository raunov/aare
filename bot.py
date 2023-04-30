import discord
import responses

import os
from dotenv import load_dotenv

load_dotenv()

async def send_message(message, user_message, is_private):
    """
    Sends a response to a given message based on the user's input.

    Args:
        message: The original message object to reply to.
        user_message: The content of the user's message as a string.
        is_private: A boolean indicating whether the response should be sent privately or not.

    Returns:
        None
    """
    try:
        response = responses.get_response(user_message)

        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():
    """
    Starts the Discord bot using the token from the environment variable DISCORD_TOKEN.
    """

    TOKEN = os.getenv("DISCORD_TOKEN")
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)