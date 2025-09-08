
# 🧠 TalkWithDB -  AI Database Agent

###  [Preview Link](https://talkwithdb.streamlit.app/) : Here you can upload your own .db file and add you own gemini key.

This project is an **AI-powered Streamlit app** that connects to a **SQLite3 database (`company.db`)** and allows you to ask natural language questions about its data.  
The agent uses **Google Gemini (via LangChain)** along with custom database tools to automatically:
1. Inspect available tables.
2. Fetch table schemas.
3. Generate SQL queries.
4. Run the queries and return results.

---

## 🚀 Features
- Natural language Q&A over any connected `.db` file.
- Automatic schema inspection before query generation.
- Built with **Streamlit + LangChain + Gemini API**.
- Modular tools for `get_tables`, `get_schema`, and `run_query`.

![Screenshot of chat](https://github.com/user-attachments/assets/4364b7d9-2a5c-4c7c-9f7d-b9ff8ceef3fb)

---

## 📂 Project Structure
````
.
├── main.py                    # Main Streamlit app
├── utils/database.py          # Database utility functions
├── database/company.db        # SQLite3 database
├── pyproject.toml             # uv-managed dependencies
├── uv.lock                    # Lockfile for reproducibility
└── README.md                  # Project documentation

````

---

## 🔧 Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/TalkWithDB-AI-Agent.git
cd TalkWithDB-AI-Agent
````

### 2️⃣ Install dependencies using [uv](https://github.com/astral-sh/uv)

If not installed, install `uv`:

```bash
pip install uv
```

Install project dependencies from `pyproject.toml`:

```bash
uv sync
```

Or, if you want to install from `requirements.txt`:

```bash
uv pip install -r requirements.txt
```

---

### 3️⃣ Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

> 🔑 You need a valid Google Gemini API key.
> Get one from [Google AI Studio](https://aistudio.google.com/).

---

### 4️⃣ Run the Streamlit app

```bash
uv run streamlit run main.py
```

This will launch the app in your browser at:

```
http://localhost:8501
```

---

## 🗄️ Database

The app connects to `company.db` (SQLite3).
Make sure the file exists in the root directory.
You can swap it with your own `.db` file — the AI will automatically detect new tables and schemas.

---

## ✅ Example Usage

1. Start the app.
2. Ask questions like:

   * *"Show me all employees in the Engineering department."*
   * *"What are the salaries of managers?"*
   * *"List all tables in the database."*

The agent will:

* Inspect available tables.
* Get schema details.
* Construct and run a safe SQL `SELECT` query.
* Return the results in a readable format.

---

## 🛠️ Development Notes

* Dependencies are tracked in `pyproject.toml` via `uv`.
* Use `uv export --format requirements.txt --no-hashes -o requirements.txt` if you need a `requirements.txt`.
* Dev-only packages can be added with:

  ```bash
  uv add --dev pytest black
  ```

---

## 📜 License

`
MIT License – feel free to use and adapt.
`

Temp

