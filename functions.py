from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

load_dotenv(find_dotenv())


def analyze_stock(user_input, name="Aare"):
    # Create a ChatOpenAI instance with the specified model_name and temperature
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5)
    
    # Define a template string for the system message prompt
    template = """
    Sa oled investeerimisassistent, kes analüüsib aktsiaid. Sinu eesmärk on aidata kasutajal kiiresti analüüsida aktsiat ja anda soovitus, kas aktsiat osta või mitte.
    
    Esmalt pead tuvastama kasutaja päringust ettevõtte nime või aktsia sümboli, ning analüüsi tüübi (tehniline, fundamentaalne, konkurentsianalüüs, jne).
    
    Seejärel pead koostama lühikese ja konkreetse analüüsi ja ostu või müügisoovituse.
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    
    human_template = "Kasutaja päring, mis sisaldab analüüsitava ettevõtte nime või tickerit ning muid juhiseid: {user_input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    chain = LLMChain(llm=chat, prompt=chat_prompt)
    response = chain.run(user_input=user_input, name=name)
    
    return response