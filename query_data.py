import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from tools.embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the following questions as best you can. You have access to the following context:

{context}

Use the following format:

Question: the input question you must answer

Thought: you should always think about what to do

Action Input: the input to the action

Observation: the result of the action

... (this Thought/Action/Action Input/Observation can repeat N times)

Thought: I now know the final answer

Final Answer: the final answer to the original input question

Give as respond to user only Final Answer.

Begin!

Question: {question}
"""


def main():
    # Chat-like interaction: Prompt the user for input.
    while True:
        query_text = input("Please enter your query (or type 'exit' to quit): ")

        if query_text.lower() == 'exit':
            print("Goodbye!")
            break

        # Process the user's query
        response = query_rag(query_text)
        print(f"Response: {response}\n")


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=4)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = Ollama(model="llama3.1")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"{response_text}\nSources: {sources}"
    return formatted_response


if __name__ == "__main__":
    main()
