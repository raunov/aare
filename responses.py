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
    
    #lowercase, strip and remove punctuation
    worker=gpt_functions.chat_dispatcher(p_message).strip().lower().replace(".","")
    
    if worker=="börsiuudiste nõunik":
        return gpt_functions.stocknews(p_message)
    elif worker=="aktsianalüütik":
        # use only 5 last messages in history
        return gpt_functions.analyze_stock(p_message, history[-5:], username)
    elif worker=="üldnõustaja":
        return gpt_functions.soovitus(p_message,username)
    else:
        return gpt_functions.chitchat(p_message, history, username)
    
# react to user's input with an appropriate emoji
def get_emoji(message: str) -> str:
    """
    Generates an emoji based on the given message.

    Args:
        message: The user's input message as a string.

    Returns:
        A string containing the generated emoji.
    """
    # Convert the message to lowercase for easier comparison
    p_message = message.lower()
    
    #lowercase, strip and remove punctuation
    worker=gpt_functions.chat_dispatcher(p_message).strip().lower().replace(".","")
    
    if worker=="börsiuudiste nõunik":
        return "📰"
    elif worker=="aktsianalüütik":
        return "📈"
    elif worker=="üldnõustaja":
        return "🤔"
    else:
        return "💬"