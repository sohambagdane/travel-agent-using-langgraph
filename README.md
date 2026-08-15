# ✈️ AI Travel Planner — Multi-Agent LangGraph System

A multi-agent AI travel planning application built with **LangGraph**, **Groq/LLaMA 3.3 70B**, **Tavily**, **AviationStack**, **PostgreSQL**, and **Streamlit**.

The system decomposes travel planning into specialized agents that collect flight information, research accommodation, generate an itinerary, and synthesize a final trip plan.

## ✨ Features

- Multi-agent workflow orchestrated with LangGraph
- Flight data integration through AviationStack
- Web research through Tavily
- LLM-powered itinerary and final-response generation with Groq
- PostgreSQL-backed LangGraph checkpointing and conversation history
- Streamlit interface with live agent progress
- Downloadable Markdown travel plans
- In-memory fallback when PostgreSQL is unavailable
- Secure environment-variable based API configuration

## 🧠 Architecture

```text
User Request
     │
     ▼
┌─────────────────┐
│  Flight Agent   │ ──► AviationStack
└────────┬────────┘
         ▼
┌─────────────────┐
│   Hotel Agent   │ ──► Tavily
└────────┬────────┘
         ▼
┌─────────────────┐
│ Itinerary Agent │ ──► Groq / LLaMA
└────────┬────────┘
         ▼
┌─────────────────┐
│  Final Agent    │ ──► Groq / LLaMA
└────────┬────────┘
         ▼
   PostgreSQL Checkpoint
```

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Agent orchestration | LangGraph |
| LLM | Groq / LLaMA 3.3 70B |
| Web research | Tavily |
| Flight data | AviationStack |
| Persistent memory | PostgreSQL + LangGraph PostgresSaver |
| Frontend | Streamlit |
| Language | Python 3.12 |

## 📁 Project Structure

```text
.
├── tools/
│   ├── flight_tool.py
│   └── tavily_tool.py
├── travel_plans/
├── .env.example
├── .gitignore
├── frontend.py
├── main.py
└── requirements.txt
```

## 🚀 Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/sohambagdane/travel-agent-using-langgraph.git
cd travel-agent-using-langgraph
```

### 2. Create a virtual environment

```bash
python -m venv langgraph_env3
```

Windows PowerShell:

```powershell
.\langgraph_env3\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and add your own API credentials.

```env
GROQ_API_KEY=...
TAVILY_API_KEY=...
AVIATIONSTACK_API_KEY=...
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/langgraph_memory_demo
```

**Never commit `.env` or API keys.**

### 5. PostgreSQL

Create a PostgreSQL database named:

```text
langgraph_memory_demo
```

The application expects PostgreSQL on the local server. Adjust the connection string if your installation uses a different host or port.

### 6. Run

Terminal mode:

```bash
python main.py
```

Streamlit interface:

```bash
streamlit run frontend.py
```

Then open the local URL shown by Streamlit, normally:

```text
http://localhost:8501
```

## 💬 Example Prompt

```text
Plan a 7-day Japan trip including flights, hotels and sightseeing under ₹2 lakhs.
```

## 🔐 Security

API credentials are loaded from `.env` using `python-dotenv`.

The repository intentionally excludes:

- `.env`
- virtual environments
- Python caches
- generated travel-plan files

Use `.env.example` as the configuration template.

## 🎯 Engineering Highlights

This project demonstrates:

- stateful multi-agent orchestration
- typed graph state with `TypedDict`
- sequential agent execution
- external API/tool integration
- LLM fallback handling
- persistent checkpointing
- streaming graph updates to a frontend
- environment-based secret management

## 📌 Attribution

This repository was developed as a personal learning and portfolio adaptation of an existing public LangGraph travel-planning implementation. The upstream project was used as a starting reference; this repository contains local configuration, cleanup, documentation, and application-level adaptations.

## 📄 License

See the repository's `LICENSE` file for the applicable license information.
