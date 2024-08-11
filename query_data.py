from langchain_chroma import Chroma
from langchain_core.tools import Tool
from langchain_ollama import ChatOllama
from tools.embedding_function import get_embedding_function
from langchain.prompts.prompt import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer

Thought: you should always think about what to do

Action: the action to take, should be one of [{tool_names}]

Action Input: the input to the action

Observation: the result of the action

... (this Thought/Action/Action Input/Observation can repeat N times)

Thought: I now know the final answer
Action: Form a final answer to the original input question. 
Final Answer: Give a final answer

Begin!

Question: {input}

Thought: {agent_scratchpad}
"""

def pdf_tool_func(query_text: str, chat_history: list):
    return query_rag(query_text, chat_history)

def regular_tool_func(query_text: str, chat_history: list):
    return "Use your general knowledge to answer the question."
def decide_response_method(query_text: str, chat_history: list):
    model = ChatOllama(model="llama3.1")

    tools = [
        Tool(
            name="Regular Response",
            func=lambda x: "Use your general knowledge to answer the question.",
            description="Use this for general questions not requiring specific PDF context."
        ),
        Tool(
            name="PDF Context Query",
            func=lambda x: query_rag(x, chat_history),
            description="Use this when the query  mentions or requires information from a PDF file or any context "
                        "that you are not aware."
        )
    ]

    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)

    react_agent = create_react_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=react_agent, tools=tools, verbose=True, handle_parsing_errors=True)

    try:
        result = agent_executor.invoke({"input": query_text, "chat_history": chat_history})
        return result.get("output", "No output from the model.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Sorry, I couldn't process the request."

def format_chat_history(chat_history):
    return "\n".join([f"User: {q}\nAI: {r}" for q, r in chat_history[-10:]])

def main(query_text):
    chat_history = []
    response = decide_response_method(query_text, chat_history)
    chat_history.append((query_text, response))
    return response

def print_chat_history(chat_history):
    print("\nChat History:")
    for i, (query, response) in enumerate(chat_history, 1):
        print(f"{i}. User: {query}")
        print(f"   AI: {response}\n")


def query_rag(query_text: str, chat_history: list):
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    results = db.similarity_search_with_score(query_text, k=4)

    if not results:
        return "No relevant information found in the PDF."

    context_text = "\n\n---\n\n".join([doc.page_content for doc, *score in results])
    return context_text


if __name__ == "__main__":
    main()
