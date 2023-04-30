# Import the 'os' module to interact with the operating system
import os
# Import 'load_dotenv' function from the 'dotenv' package to load environment variables from a .env file
from dotenv import load_dotenv

# Import 'discord' library for creating and interacting with Discord bots
import discord
# Import 'responses' module containing functions to generate responses based on user input
import responses

# Load environment variables from the .env file
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
        # Get the appropriate response based on the user's message
        response = responses.get_response(user_message)

        # Send the response either privately or in the same channel, depending on the 'is_private' flag
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        # Print any exceptions that occur while sending the message
        print(e)

def run_discord_bot():
    """
    Starts the Discord bot using the token from the environment variable DISCORD_TOKEN.
    """

    # Get the Discord bot token from the environment variable
    TOKEN = os.getenv("DISCORD_TOKEN")
    # Set up intents for the Discord bot
    intents = discord.Intents.default()
    intents.message_content = True
    # Create a new Discord client instance with the specified intents
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        # Print a message when the bot is ready and running
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        # Ignore messages sent by the bot itself
        if message.author == client.user:
            return

        # Check if the bot is mentioned in the message
        if client.user in message.mentions:
            # Extract information from the message object
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)

            # Print the received message to the console
            print(f'{username} said: "{user_message}" ({channel})')

            # Remove the bot mention from the user_message
            user_message = user_message.replace(f'<@{client.user.id}>', '').strip()
            
            # Check if the message starts with a '?' (indicating a private response)
            if user_message.startswith('?'):
                user_message = user_message[1:]
                await send_message(message, user_message, is_private=True)
            else:
                await send_message(message, user_message, is_private=False)

    # Start the Discord bot using the retrieved token
    client.run(TOKEN)
