# app.py
import streamlit as st
import json
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage, SystemMessage

from utils.database import list_tables, get_table_schema, run_sql_query

load_dotenv()

@tool
def get_tables() -> list[str]:
    """Use this tool to get a list of all table names in the database."""
    return list_tables()

@tool
def get_schema(table_name: str) -> str:
    """Use this tool to get the schema (column names and types) for a specific table."""
    return get_table_schema(table_name)

@tool
def run_query(query: str) -> str:
    """
    Use this tool to execute a read-only SQL SELECT query on the database.
    Only SELECT statements are allowed.
    Returns the query result as a JSON string.
    """
    return run_sql_query(query)

st.set_page_config(page_title="Dynamic AI Database Agent", page_icon="🧠")
st.title("🧠 Dynamic AI Database Agent")
st.caption("I can answer questions about any connected .db file.")

try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite")
    llm_with_tools = llm.bind_tools([get_tables, get_schema, run_query])
except Exception as e:
    st.error(
        f"Error initializing the model: {e}. Please ensure your GOOGLE_API_KEY is set."
    )
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I can answer questions about the connected database. What would you like to know?",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("e.g., Who is the lead engineer?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        history_for_model = [
            SystemMessage(
                content="""
                You are a powerful AI database assistant. Your goal is to answer user questions by querying the database.
                You must follow this sequence:
                1. First, use the `get_tables` tool to see what tables are available.
                2. Next, use the `get_schema` tool to understand the columns of the relevant tables.
                3. Finally, construct a precise SQL `SELECT` query and execute it using the `run_query` tool to get the answer.
                Do not make assumptions about the schema. Always inspect it first.
            """
            )
        ]
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                history_for_model.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                # This needs to handle both simple text and AIMessages with tool calls
                if isinstance(msg.get("content"), str):
                    history_for_model.append(AIMessage(content=msg["content"]))
                elif msg.get("tool_calls"):
                    history_for_model.append(AIMessage(tool_calls=msg["tool_calls"]))
        while True:
            ai_msg = llm_with_tools.invoke(history_for_model)

            if not ai_msg.tool_calls:
                response_content = ai_msg.content
                break 

            history_for_model.append(ai_msg)

            for tool_call in ai_msg.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                if tool_name == "get_tables":
                    tool_output = get_tables.invoke(tool_args)
                elif tool_name == "get_schema":
                    tool_output = get_schema.invoke(tool_args)
                elif tool_name == "run_query":
                    tool_output = run_query.invoke(tool_args)
                else:
                    tool_output = "Error: Unknown tool."

                tool_message = ToolMessage(
                    content=str(tool_output), tool_call_id=tool_call["id"]
                )
                history_for_model.append(tool_message)

        message_placeholder.markdown(response_content)
        st.session_state.messages.append(
            {"role": "assistant", "content": response_content}
        )
