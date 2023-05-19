import gpt_functions

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
    
    worker=gpt_functions.chat_dispatcher(p_message)
    
    if worker=="börsiuudiste_haldur":
        return gpt_functions.stocknews(p_message,username)
    elif worker=="aktsianalüütik":
        return gpt_functions.analyze_stock(p_message,username)
    elif worker=="üldnõustaja":
        return gpt_functions.soovitus(p_message,username)
    elif worker=="vestluskaaslane":
        return gpt_functions.chitchat(p_message, history, username)
    
    return worker + ": Ei oskagi nagu midagi kosta..."