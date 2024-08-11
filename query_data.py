from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from tools.embedding_function import get_embedding_function
from PyPDF2 import PdfReader
import os

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

def extract_text_from_pdf(file_path):
    """
    Extract text from the given PDF file.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF file: {e}")
    return text

def query_rag(query_text: str, file_name: str = None) -> str:
    """
    Process the user's query and return the response, optionally using an uploaded PDF file.

    Args:
        query_text (str): The query text to be processed.
        file_name (str): The name of the PDF file to be processed.

    Returns:
        str: The formatted response with sources.
    """
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Extract text from the PDF if a file name is provided
    context_text = ""
    if file_name:
        file_path = os.path.join(CHROMA_PATH, file_name)
        context_text = extract_text_from_pdf(file_path)

    # If there's additional context from the database, combine it
    if not context_text:
        results = db.similarity_search_with_score(query_text, k=4)
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # Prepare the prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Invoke the model
    model = Ollama(model="llama3.1")
    response_text = model.invoke(prompt)

    # Collect sources if available
    sources = [doc.metadata.get("id", None) for doc, _score in results] if not file_name else []
    formatted_response = f"{response_text}\nSources: {sources}"
    return formatted_response
