# react_agents.py
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_ollama import ChatOllama
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from common import query_rag

def use_pdf_context(question, chat_history):
    model = ChatOllama(model="llama3.1")

    template = """
    Answer the following question to the best of your ability. You have access to the following tools:

    1. Query PDF Context: Use this to get relevant information from the PDF.

    Chat History:
    {chat_history}

    Use the following format to respond:

    1. Thought: Analyze the query and determine if an action (like querying the document database) is necessary.
    2. Action: If needed, specify the action to take. If no action is needed, skip to the final answer.
    3. Action Input: Provide the necessary input for the action (e.g., the query text for searching the database).
    4. Observation: Record the result or output of the action (e.g., the documents retrieved from the database).
    5. Thought: Process the observation and determine the final answer.
    6. Final Answer: Provide the final answer to the user's question.

    Question: {question}
    """

    prompt_template = PromptTemplate(
        template=template,
        input_variables=["chat_history", "question"]
    )

    tools_for_agent = [
        Tool(
            name="Query PDF Context",
            func=query_rag,
            description="Use this to get relevant information from the PDF.",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=model,
        tools=tools_for_agent,
        prompt=react_prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools_for_agent,
        verbose=True,
        handle_parsing_errors=True
    )

    formatted_prompt = prompt_template.format_prompt(
        chat_history=chat_history,
        question=question
    )

    result = agent_executor.invoke(
        input={"input": formatted_prompt}
    )

    output = result["output"]
    return output