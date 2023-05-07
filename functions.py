from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

load_dotenv(find_dotenv())

def aastaaruanne(user_input, name="Aare"):
    return "Aastaaruannete analüüs on veel arendamisel."

def soovitus(user_input, name="Aare"):
    # Create a ChatOpenAI instance with the specified model_name and temperature
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5)

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
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
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

def chitchat(user_input, name="Aare"):
    # Create a ChatOpenAI instance with the specified model_name and temperature
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.9)
    
    # Define a template string for the system message prompt
    template = """
    Sa oled lõbus vestluspartner, kes oskab suhelda erinevate inimestega. Sinu eesmärk vestluskaaslast lõbustada jutustades lugusid, nalju, anekdoote, jne. 
    Sinu lood, naljad, anektoodid on investeerimise teemalised. Iga sõnum lõpeta lausega: 
    Aga arutame midagi konkreetset, küsi näiteks midagi mis sisaldaks sõna *aktsia* või *soovitus*, või anna link mingi ettevõtte aastaaruandele.
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    
    human_template = "Kasutaja sõnum, mille teemal vestelda: {user_input}"     
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    chain = LLMChain(llm=chat, prompt=chat_prompt)
    response = chain.run(user_input=user_input, name=name)
    
    return response
