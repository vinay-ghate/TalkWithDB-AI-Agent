import streamlit as st
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage, SystemMessage

from utils.database import list_tables, get_table_schema, run_sql_query
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

load_dotenv()

st.set_page_config(page_title="Dynamic AI Database Agent", page_icon="🧠", layout="wide")

with st.sidebar:
    st.title("⚙️ Configuration")
    
    api_key = st.text_input("Enter your Google Gemini API Key", type="password", key="api_key_input")
    uploaded_file = st.file_uploader("Upload your SQLite Database (.db)", type=["db"], key="db_uploader")

    st.markdown("---")
    
    st.title("📝 SQL History")
    query_display_area = st.container()


if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! Configure me in the sidebar to get started."}]
if "db_path" not in st.session_state:
    st.session_state.db_path = None
if "sql_queries" not in st.session_state:
    st.session_state.sql_queries = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if uploaded_file and api_key:
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    db_path = os.path.join(temp_dir, uploaded_file.name)
    with open(db_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.session_state.db_path = db_path
    
    @tool
    def get_tables() -> list[str]:
        """Use this tool to get a list of all table names in the database."""
        logger.info(f"Tool: get_tables called")
        return list_tables(st.session_state.db_path)

    @tool
    def get_schema(table_name: str) -> str:
        """Use this tool to get the schema (column names and types) for a specific table."""
        logger.info(f"Tool: get_schema called for table: {table_name}")
        return get_table_schema(st.session_state.db_path, table_name)

    @tool
    def run_query(query: str) -> str:
        """
        Use this tool to execute a read-only SQL SELECT query on the database.
        Returns the query result as a JSON string.
        """
        logger.info(f"Tool: run_query called with query: {query}")
        st.session_state.sql_queries.append(query)
        return run_sql_query(st.session_state.db_path, query)

    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", google_api_key=api_key)
        llm_with_tools = llm.bind_tools([get_tables, get_schema, run_query])
    except Exception as e:
        st.error(f"Error initializing the model: {e}")
        st.stop()
    
    if prompt := st.chat_input("Ask a question about your database..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("🧠 Thinking..."):
                history_for_model = [
                    SystemMessage(content="""
                        You are a powerful AI database assistant. Your goal is to answer user questions by querying the database.
                        You must follow this sequence:
                        1. First, use the `get_tables` tool to see what tables are available.
                        2. Next, use the `get_schema` tool to understand the columns of the relevant tables.
                        3. Finally, construct a precise SQL `SELECT` query and execute it using the `run_query` tool to get the answer.
                        Do not make assumptions about the schema. Always inspect it first.
                        Provide a final, user-friendly answer based on the query results.
                    """)
                ]
                for msg in st.session_state.messages:
                    if msg["role"] == "user":
                        history_for_model.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        if isinstance(msg.get("content"), str):
                             history_for_model.append(AIMessage(content=msg["content"]))

                while True:
                    ai_msg = llm_with_tools.invoke(history_for_model)

                    if not ai_msg.tool_calls:
                        response_content = ai_msg.content
                        break 
                    
                    history_for_model.append(ai_msg)
                    
                    for tool_call in ai_msg.tool_calls:
                        tool_map = {"get_tables": get_tables, "get_schema": get_schema, "run_query": run_query}
                        tool_name = tool_call["name"]
                        
                        if tool_name in tool_map:
                            selected_tool = tool_map[tool_name]
                            tool_output = selected_tool.invoke(tool_call["args"])
                        else:
                            tool_output = f"Error: Unknown tool {tool_name}."

                        history_for_model.append(ToolMessage(content=str(tool_output), tool_call_id=tool_call["id"]))

            message_placeholder.markdown(response_content)
            st.session_state.messages.append({"role": "assistant", "content": response_content})

else:
    st.info("⬆️ Please upload a database file and enter your API key to activate the chat.")

with query_display_area:
    if st.session_state.sql_queries:
        for i, q in enumerate(reversed(st.session_state.sql_queries)):
            with st.expander(f"Query {len(st.session_state.sql_queries) - i}", expanded=False):
                st.code(q, language="sql")
    else:
        st.write("No queries have been run yet.")