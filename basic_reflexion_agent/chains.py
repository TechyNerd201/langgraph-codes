from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
import datetime
from models import AnswerQuestion , ReviseAnswer
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()



actor_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are expert AI recercher
    Current TIme: {time}

    1. {first_instruction}
    2. Reflect and critique your answer. Be severe to maximize improvement.
    3. After the reflection. Do not include them inside the reflection.
    """,
    ),
    (MessagesPlaceholder(variable_name="messages")),
    ("system", "Answer the user's question above using the required format ."),


]).partial(time=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

first_responder_prompt_template =  actor_prompt_template.partial(first_instruction="provide a detailed 250 word answer to the user's question")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

first_responder_chain = first_responder_prompt_template | llm.with_structured_output(AnswerQuestion)

# res =first_responder_chain.invoke({'messages': [{"role": "user", "content": "the weather of nagpur"}]})
# print(res)

revise_instructions = """ 
Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
    -You must include numerical citations in your revised answer to ensure it can be verified.
    - Add a "References" section to the bottom of your answer (which does not count towards the word itself) . In form of:
        -1. https://exmaple.com
        -2. https://example.com
    - You should use the previous critque to remove superfluous information from your answer and make Sure it is not more than 250 words.
    """

parser2 = PydanticOutputParser(pydantic_object=ReviseAnswer)
revisor_prompt = actor_prompt_template.partial(first_instruction=revise_instructions) 

revisor_chain = revisor_prompt   | llm.with_structured_output(ReviseAnswer) 

# res =chain2.invoke({"messages": [{"role": "user", "content": "the weather of nagpur"}]})
# print(res)

