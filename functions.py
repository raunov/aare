import requests
import re
import json
from langchain.document_loaders import UnstructuredURLLoader
from langchain.chat_models import PromptLayerChatOpenAI
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import PromptLayerOpenAIChat, PromptLayerOpenAI
from dotenv import find_dotenv, load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

load_dotenv(find_dotenv())

def aastaaruanne(user_input, name="Aare"):
    # extract an url from user input
    url = re.search("(?P<url>https?://[^\s]+)", user_input).group("url")
    
    if url != "":
        # make a request to the url
        response = requests.get(url)
        # if the status code is not 200, return an error message
        if response.status_code != 200:
            return "Vabandust, aga ei suutnud aastaaruannet leida."
        # if the status code is 200, return a success message
        else:
            loader = UnstructuredURLLoader([url])
            documents = loader.load()
            chain = load_qa_chain(llm=PromptLayerOpenAI, chain_type="map_reduce")
            query="Millest on siin juttu?"
            chain.run(documents=documents, query=query)
            return json.dumps(chain.results, indent=4)
    else:
        return "Aastaaruannete analüüs on veel arendamisel."

def soovitus(user_input, name="Aare"):
    # Create a ChatOpenAI instance with the specified model_name and temperature
    chat = PromptLayerChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5)

    template = """
    Sa oled isiklik nõustaja, kes aitab leida lahendusi kliendi probleemidele või küsimustele. 
    Sinu eesmärk on aidata kasutajal kiiresti leida lahendus, mida ta otsib, ning seejärel veenvalt põhjendada oma soovitust.
    Ole konstruktiivne, lühike ja konkreetne, ära raiska aega tervitusteks, mine kohte asja juurde.
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    
    human_template = "Kasutaja päring, mis sisaldab küsimust, või probleemi, millele soovitust otsitakse: {user_input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    chain = LLMChain(llm=chat, prompt=chat_prompt)
    response = chain.run(user_input=user_input, name=name)
    return response

def analyze_stock(user_input, name="Aare"):
    # Create a ChatOpenAI instance with the specified model_name and temperature
    chat = PromptLayerChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    # Define a template string for the system message prompt
    template = """
    Sa oled investeerimisassistent, kes analüüsib aktsiaid. Sinu eesmärk on aidata kasutajal kiiresti analüüsida aktsiat ja anda esmalt soovitus, kas aktsiat osta või mitte, ning seejärel veenvalt põhjendada oma soovitust.
    Oled täpne, lühike ja konkreetne, ära raiska aega tervitusteks, mine kohte asja juurde.
    
    Tuvasta kasutaja päringust ettevõtte nime või aktsia sümboli, ning analüüsi tüübi (tehniline, fundamentaalne, konkurentsianalüüs, jne).
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

# history is in the following format:
# [('RaunoV', '@Aare millest me rääkisime?'), ('Aare', 'Ei mäleta')]
def chitchat(user_input, history, name="Aare"):
    # Create a ChatOpenAI instance with the specified model_name and temperature
    chat = PromptLayerChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.9)

    # Define a template string for the system message prompt
    template = """
    Sa oled lõbus vestluspartner nimega AARE, kes oskab suhelda erinevate inimestega. 
    Sinu eesmärk vestluskaaslast lõbustada jutustades lugusid, nalju, anekdoote, jne. 
    Sinu lood, naljad, anektoodid on investeerimise teemalised. Ära tervita, mine kohe asja juurde.
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    # convert the history to a string in the format: User: message\nUser: message\nUser: message
    history_txt = "\n".join([f"{user}: {message}" for user, message in history])
    
    human_template = "Eelnev vestlusajalugu: {history_txt}\n\nKasutaja sõnum, mille teemal vestelda: {user_input}"     
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    print("\nVestlusajalugu:"+history_txt)
    chain = LLMChain(llm=chat, prompt=chat_prompt)
    response = chain.run(user_input=user_input, history_txt=history_txt, name=name)
    
    return response
