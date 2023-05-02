from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

load_dotenv(find_dotenv())


def draft_email(user_input, name="Rauno"):
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5)

    template = """
    
    Sa oled abistav assistent, kes koostab uue e-kirja põhjal vastuse.
    
    Sinu eesmärk on aidata kasutajal kiiresti luua täiuslik vastus.
    
    Hoia oma vastus lühike ja konkreetne ning jäljenda e-kirja stiili, et vastata sarnasel viisil ja sobituda tooniga.
    
    Alusta oma vastust öeldes: "Tere {name}, siin on sinu vastuse mustand:". Ja siis jätkake vastusega uuel real. 
    Vastus ümbritse kindlasti <code> märkidega ja allkirjasta vastus {signature}.
    
    """

    signature = f"Tervitades, \n\{name}"
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template = "Siin on e-kiri, millele on vaja vastata ja võta vastuse koostamisel arvesse ka kasutaja muud kommentaare: {user_input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    response = chain.run(user_input=user_input, signature=signature, name=name)

    return response