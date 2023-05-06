from functions import analyze_stock, soovitus

def debug_response(text):
    """
    Custom function to process the text and return a response.
    In this example, the function converts the input text to uppercase.

    Args:
        text (str): The input text to process.

    Returns:
        str: The processed text.
    """
    response = text.upper() + ' ... eeh, ei saanud aru. Proovi `!abi`'
    return response

# Define a function to generate a response based on the user's input, including the user's name in the response
def get_response(message: str, username:str) -> str:
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
    if p_message == 'tere':
        return 'Tervist, ' + username + '!'
    
    if 'aktsia' in p_message:
        return analyze_stock(p_message)
    
    if 'soovitus' in p_message:
        return soovitus(p_message)
    
    # Check if the message is "!help" and return a help message
    if p_message == '!abi':
        return 'Proovi näiteks: `@aare, palun analüüsi Tallinna Kaubamaaja ja tema konkurentide aktsiaid'

    # If none of the above conditions are met, return a default message indicating the bot didn't understand the input
    return debug_response(p_message)
