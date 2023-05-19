# Import the 'os' module to interact with the operating system
import os
import re
# Import 'load_dotenv' function from the 'dotenv' package to load environment variables from a .env file
from dotenv import load_dotenv

# Import 'discord' library for creating and interacting with Discord bots
import discord
# Import 'responses' module containing functions to generate responses based on user input
import responses

# Load environment variables from the .env file
load_dotenv()

async def send_response(message, user_message, is_private):
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
        
        # set typing status on discord channel
        async with message.channel.typing():
            # fetch the 10 most recent messages from non-bots on the channel
            history = []
            async for msg in message.channel.history(limit=5):
                content = msg.content
                user_tags = re.findall(r'<@!?(\d+)>', content)

                for user_id in user_tags:
                    user = await message.guild.fetch_member(int(user_id))
                    if user:
                        content = content.replace(f'<@{user_id}>', user.name)
                        content = content.replace(f'<@!{user_id}>', user.name)

                history.append((msg.author.name, content))
            
            history.reverse()
            # Print the received message to the console
            print(f'{message.author.name} said: "{user_message}" ({message.channel})')
                       
            # Get the appropriate response based on the user's message and recent message history on the channel
            # user_message is the last message in the history, take it out from the history
            user_message = history.pop()[1]
            response = responses.get_response(user_message, history, message.author.name)
            
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

            # Print the received message to the console
            # print(f'{username} said: "{user_message}" ({channel})')

            # Remove the bot mention from the user_message
            user_message = user_message.replace(f'<@{client.user.id}>', username).strip()
            
            await send_response(message, user_message, is_private=False) # Send a response to the message

    # Start the Discord bot using the retrieved token
    client.run(TOKEN)
