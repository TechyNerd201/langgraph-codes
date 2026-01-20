


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

generation_prompt = ChatPromptTemplate.from_messages([
    ("system" , "You are a twitter techie influencer assistant with writing excellene twitter posts.Generate the best twitter post possible for users requests. If the user provides critique, respond version of your previous attempts"),
    MessagesPlaceholder(variable_name="messages"),
])

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

reflection_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a viral twitter influencer grading a tweet. Generate critque and recomendation for the users tweet.Always provide detailed recommnendation and critique , including requests for length , virality ,style,etc"),
    MessagesPlaceholder(variable_name="messages"),
])

parser = StrOutputParser()

chain1 = generation_prompt | llm | parser
chain2 = reflection_prompt | llm | parser


