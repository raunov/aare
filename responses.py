from functions import analyze_stock, soovitus, chitchat, aastaaruanne


# Define a function to generate a response based on the user's input, including the user's name in the response
def get_response(message: str, history:str, username:str) -> str:
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
    
    if 'https' in p_message:
        return aastaaruanne(p_message)
    
    # Check if the message is "!help" and return a help message
    if p_message == '!abi':
        return 'Proovi näiteks: `@aare, palun analüüsi Tallinna Kaubamaaja ja tema konkurentide aktsiaid'

    # If none of the above conditions are met, return a default message indicating the bot didn't understand the input
    #return history
    return chitchat(p_message, history)
