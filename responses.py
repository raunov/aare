# Import the 'random' module to generate random numbers
import random

def get_response(message: str) -> str:
    """
    Generates a response based on the given message.

    Args:
        message: The user's input message as a string.

    Returns:
        A string containing the generated response.
    """

    # Convert the message to lowercase for easier comparison
    p_message = message.lower()

    # Check if the message is "hello" and return a greeting
    if p_message == 'hello':
        return 'Hey there!'

    # Check if the message is "roll" and return a random number between 1 and 6 (inclusive)
    if message == 'roll':
        return str(random.randint(1, 6))

    # Check if the message is "!help" and return a help message
    if p_message == '!help':
        return '`This is a help message that you can modify.`'

    # If none of the above conditions are met, return a default message indicating the bot didn't understand the input
    return 'I didn\'t understand what you wrote. Try typing "!help".'
