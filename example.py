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

prompt_for_chat = ChatPromptTemplate.from_messages([
    ("system", "Answer the user's questions based on the context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])

prompt_for_name_of_the_chat = ChatPromptTemplate.from_messages([
    ("system", "Make a name for the chat based on chat history and return only chat name and nothing else"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "Make a chat name 3-4 words")
])


def create_chain_for_chat_name():
    model = ChatOllama(model="llama3.1")

    # Create a RunnableSequence instead of LLMChain
    chain = prompt_for_name_of_the_chat | model

    return chain


def generate_chat_name(chain, chat_history):
    try:
        response = chain.invoke({"chat_history": chat_history})
        return response.content.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def chat_history_name(chat_history):
    if len(chat_history) > 0:  # Generate chat name if there's chat history
        name_chain = create_chain_for_chat_name()
        chat_name = generate_chat_name(name_chain, chat_history)
        return chat_name
    else:
        return "New Chat"  # Default name for empty chat history

def create_chain_for_chat():
    model = ChatOllama(model="llama3.1")

    chain = create_stuff_documents_chain(
        llm=model,
        prompt=prompt_for_chat
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
    chain = create_chain_for_chat()
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
    chat_history = [
        HumanMessage(content="What is the weather like today?"),
        AIMessage(content="The weather is sunny with a chance of showers later in the day.")
    ]
    chat_name = chat_history_name(chat_history)
    print(chat_name)