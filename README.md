# 🧠 TalkWithDB - AI Database Agent

[](https://talkwithdb.streamlit.app/)

Chat with any SQLite database using natural language. No setup required—just upload your `.db` file, add your Gemini API key, and start asking questions.

### 🔗 **[Try the Live Demo Here\!](https://talkwithdb.streamlit.app/)**

This project is an AI-powered agent that lets you have a conversation with your data. The agent uses **Google Gemini** and **LangChain** to understand your questions, inspect the database you provide, write SQL queries, and give you back answers in plain English.

-----

## 🚀 Key Features

  - **Bring Your Own Database**: Upload your own SQLite `.db` file directly in the browser.
  - **User-Provided API Key**: Securely use your own Google Gemini API key.
  - **Live SQL Query Display**: See the SQL queries the AI generates in real-time in the sidebar.
  - **Natural Language Q\&A**: Ask complex questions without writing a single line of SQL.
  - **Automatic Schema Detection**: The agent automatically inspects table structures to write accurate queries.
  - **Built with**: **Streamlit** + **LangChain** + **Google Gemini**.

-----

## 💡 How to Use the Live App

Get started in seconds with the hosted Streamlit application.

1.  **Open the App**: Navigate to **[TalkWithDB on Streamlit](https://talkwithdb.streamlit.app/)**.
2.  **Configure**: In the sidebar, enter your **Google Gemini API Key**.
3.  **Upload**: Upload your SQLite (`.db`) database file.
4.  **Chat**: Once configured, the chat window will activate. Start asking questions\!

**Example Questions:**

  * *"Show me all employees in the Engineering department."*
  * *"What are the salaries of managers?"*
  * *"How many users signed up last week?"*

-----

## 🔧 Local Development Setup

Want to run the app locally or contribute? Follow these steps.

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/TalkWithDB-AI-Agent.git
cd TalkWithDB-AI-Agent
```

### 2️⃣ Install Dependencies using [uv](https://github.com/astral-sh/uv)

This project uses `uv` for fast dependency management. First, install `uv`:

```bash
pip install uv
```

Then, sync the project dependencies:

```bash
uv sync
```

### 3️⃣ Run the Streamlit App

```bash
uv run streamlit run app.py
```

This will launch the app in your browser, typically at `http://localhost:8501`.

-----

## 📂 Project Structure

```
.
├── app.py                 # The main Streamlit application
├── utils/database.py      # Database utility functions (list_tables, get_schema, etc.)
├── temp/                  # Directory for temporarily storing uploaded .db files
├── pyproject.toml         # uv-managed project dependencies
├── uv.lock                # Lockfile for reproducible builds
└── README.md              # You are here!
```

-----

## 📜 License

This project is licensed under the **MIT License**.
