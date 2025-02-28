from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from utils import (
    set_env,
    unzip_database_file,
    retrive_chroma_collection,
    get_similar_data,
)

# Set environment variable
set_env()
# Unzip the database
unzip_database_file("./chroma.zip", "./chroma.db")

# Chat template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a fashion assistant helping a user with fashion advice.\
            The user will ask you for fashion advice, and you must respond\
            based on the query, context and your general understanding of fashion.\
            Think step-by-step before answering.\
            Do not include anything about the context and you in the response.\
            Format the output content in markdown.",
        ),
        ("user", "{query} <context>{context}</context>"),
    ]
)


# Define the LLM
llm = ChatGroq(
    model="gemma2-9b-it",
)

# Create the chain
chain = prompt | llm


def main(query):
    # Retrieve chromadb collection
    collection = retrive_chroma_collection("./chroma.db")

    # Retrieve context
    context = get_similar_data(collection, query, top_k=1)

    # Get LLM response
    response = chain.invoke({"query": query, "context": context})
    return response.content
