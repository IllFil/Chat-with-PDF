from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from tools.embedding_function import get_embedding_function
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain

CHROMA_PATH = "chroma"

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the user's questions based on the context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])

def create_chain():
    model = ChatOllama(model="llama3.1")

    chain = create_stuff_documents_chain(
        llm=model,
        prompt=prompt
    )

    retriever_prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user",
         "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])

    retriever = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()).as_retriever()

    history_aware_retriever = create_history_aware_retriever(
        llm=model,
        retriever=retriever,
        prompt=retriever_prompt
    )

    retrieval_chain = create_retrieval_chain(
        history_aware_retriever,
        chain
    )

    return retrieval_chain

def process_chat(chain, question, chat_history):
    response = chain.invoke({
        "chat_history": chat_history,
        "input": question,
    })
    return response["answer"]

def main(user_input, chat_history):
    chain = create_chain()
    response = process_chat(chain, user_input, chat_history)
    new_chat_history = chat_history + [HumanMessage(content=user_input), AIMessage(content=response)]
    print("Assistant:", response)
    return response, new_chat_history

def process_chat(chain, question, chat_history):
    response = chain.invoke({
        "chat_history": chat_history,
        "input": question,
    })
    return response["answer"]

if __name__ == "__main__":
    main()