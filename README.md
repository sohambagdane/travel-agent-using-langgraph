**# ✈️ AI Travel Planner — Multi-Agent LangGraph System**



**An AI-powered multi-agent travel planning application built with \*\*LangGraph\*\*, \*\*Groq / LLaMA 3.3 70B\*\*, \*\*Tavily\*\*, \*\*AviationStack\*\*, \*\*PostgreSQL\*\*, and \*\*Streamlit\*\*.**



**The application breaks travel planning into specialized agents that research flights, investigate accommodation options, generate an itinerary, and synthesize the collected information into a final travel plan.**



**---**



**## 🚀 Features**



**- 🤖 Multi-agent workflow orchestrated with \*\*LangGraph\*\***

**- ✈️ Flight research using \*\*AviationStack\*\***

**- 🔎 Web research using \*\*Tavily\*\***

**- 🧠 AI-powered itinerary generation using \*\*Groq / LLaMA 3.3 70B\*\***

**- 🧠 AI-powered final response synthesis**

**- 🐘 PostgreSQL-backed LangGraph checkpointing**

**- 💾 Persistent conversation/workflow state**

**- 📊 Streamlit web interface**

**- ⚡ Live agent pipeline progress in the UI**

**- 📄 Automatically generated Markdown travel plans**

**- 🔄 In-memory fallback when PostgreSQL is unavailable**

**- 🔐 API credentials loaded through environment variables**

**- 🧩 Modular tool-based architecture**



**---**



**## 🏗️ Architecture**



**The application follows a sequential multi-agent workflow:**



**```text**

&#x20;                        **USER REQUEST**

&#x20;                             **│**

&#x20;                             **▼**

&#x20;                    **┌─────────────────┐**

&#x20;                    **│  Flight Agent   │**

&#x20;                    **└────────┬────────┘**

&#x20;                             **│**

&#x20;                             **▼**

&#x20;                      **AviationStack**

&#x20;                             **│**

&#x20;                             **▼**

&#x20;                    **┌─────────────────┐**

&#x20;                    **│   Hotel Agent   │**

&#x20;                    **└────────┬────────┘**

&#x20;                             **│**

&#x20;                             **▼**

&#x20;                          **Tavily**

&#x20;                             **│**

&#x20;                             **▼**

&#x20;                  **┌─────────────────────┐**

&#x20;                  **│  Itinerary Agent    │**

&#x20;                  **└──────────┬──────────┘**

&#x20;                             **│**

&#x20;                             **▼**

&#x20;                      **Groq / LLaMA**

&#x20;                             **│**

&#x20;                             **▼**

&#x20;                  **┌─────────────────────┐**

&#x20;                  **│    Final Agent      │**

&#x20;                  **└──────────┬──────────┘**

&#x20;                             **│**

&#x20;                             **▼**

&#x20;                      **Groq / LLaMA**

&#x20;                             **│**

&#x20;                             **▼**

&#x20;                 **┌──────────────────────┐**

&#x20;                 **│    Final Travel Plan │**

&#x20;                 **└──────────┬───────────┘**

&#x20;                            **│**

&#x20;                            **▼**

&#x20;                   **PostgreSQL Checkpoint**

&#x20;                            **│**

&#x20;                            **▼**

&#x20;                    **Markdown Output**

**```**



**### Agent Responsibilities**



**| Agent | Responsibility | Technology |**

**|---|---|---|**

**| ✈️ Flight Agent | Retrieves flight information | AviationStack |**

**| 🏨 Hotel Agent | Researches hotels and accommodation | Tavily |**

**| 🗺️ Itinerary Agent | Creates a day-by-day itinerary | Groq / LLaMA 3.3 70B |**

**| 🧠 Final Agent | Synthesizes research and itinerary | Groq / LLaMA 3.3 70B |**



**---**



**## 🔄 Workflow**



**When a user submits a travel request:**



**1. The \*\*Flight Agent\*\* receives the request and retrieves flight information.**

**2. The \*\*Hotel Agent\*\* researches accommodation and destination information through Tavily.**

**3. The \*\*Itinerary Agent\*\* combines the user request, flight research, and hotel research to create an itinerary.**

**4. The \*\*Final Agent\*\* synthesizes the collected information into a concise final travel plan.**

**5. \*\*LangGraph\*\* manages the state and execution flow between agents.**

**6. \*\*PostgreSQL\*\* stores LangGraph checkpoint/state information when configured.**

**7. The generated travel plan can be saved as a Markdown file.**



**---**



**## 🧠 Why LangGraph?**



**LangGraph is used to model the travel planner as a structured stateful workflow.**



**The application maintains a shared state containing:**



**```text**

**user\_query**

**flight\_results**

**hotel\_results**

**itinerary**

**messages**

**llm\_calls**

**```**



**Each agent reads relevant information from the shared state and returns new information for the next stage of the workflow.**



**This makes the application easier to extend with additional agents or tools in the future.**



**---**



**## 🐘 PostgreSQL Persistence**



**PostgreSQL is used with LangGraph's PostgreSQL checkpointer to provide persistent workflow state.**



**This allows the application to maintain state across executions when PostgreSQL is available.**



**The application also includes an \*\*in-memory fallback\*\*, allowing the application to continue operating when PostgreSQL is unavailable.**



**PostgreSQL is therefore used for \*\*workflow/checkpoint persistence\*\*, rather than as the database for flight or hotel data.**



**---**



**## 🛠️ Tech Stack**



**| Category | Technology |**

**|---|---|**

**| Programming Language | Python 3.12 |**

**| Agent Orchestration | LangGraph |**

**| LLM | Groq / LLaMA 3.3 70B |**

**| Flight Data | AviationStack |**

**| Web Research | Tavily |**

**| Persistence | PostgreSQL |**

**| Frontend | Streamlit |**

**| Environment Management | python-dotenv |**

**| HTTP Requests | Requests |**

**| Database Driver | Psycopg |**



**---**



**## 📁 Project Structure**



**```text**

**travel-agent-using-langgraph/**

**│**

**├── tools/**

**│   ├── \_\_init\_\_.py**

**│   ├── flight\_tool.py**

**│   └── tavily\_tool.py**

**│**

**├── travel\_plans/**

**│   └── .gitkeep**

**│**

**├── .env.example**

**├── .gitignore**

**├── frontend.py**

**├── main.py**

**├── README.md**

**└── requirements.txt**

**```**



**### Important Files**



**\*\*`main.py`\*\***



**Contains the LangGraph workflow, agent definitions, shared state, LLM integration, and PostgreSQL checkpoint configuration.**



**\*\*`frontend.py`\*\***



**Contains the Streamlit interface and displays the agent pipeline and final travel plan.**



**\*\*`tools/flight\_tool.py`\*\***



**Handles flight research through AviationStack.**



**\*\*`tools/tavily\_tool.py`\*\***



**Handles web research through Tavily.**



**\*\*`travel\_plans/`\*\***



**Stores generated Markdown travel plans locally.**



**---**



**# ⚙️ Local Setup**



**## 1. Clone the Repository**



**```bash**

**git clone https://github.com/sohambagdane/travel-agent-using-langgraph.git**

**cd travel-agent-using-langgraph**

**```**



**## 2. Create a Virtual Environment**



**```bash**

**python -m venv langgraph\_env3**

**```**



**### Windows PowerShell**



**```powershell**

**.\\langgraph\_env3\\Scripts\\Activate.ps1**

**```**



**## 3. Install Dependencies**



**```bash**

**pip install -r requirements.txt**

**```**



**---**



**## 4. Configure Environment Variables**



**Create a `.env` file in the project root.**



**You can use `.env.example` as a template.**



**```env**

**GROQ\_API\_KEY=your\_groq\_api\_key**

**TAVILY\_API\_KEY=your\_tavily\_api\_key**

**AVIATIONSTACK\_API\_KEY=your\_aviationstack\_api\_key**

**DATABASE\_URL=postgresql://postgres:your\_password@localhost:5432/langgraph\_memory\_demo**

**```**



**### Security**



**\*\*Never commit your `.env` file or API keys to GitHub.\*\***



**The repository includes `.gitignore` configuration to keep local secrets and virtual environments out of version control.**



**---**



**# 🐘 PostgreSQL Setup**



**Create a PostgreSQL database named:**



**```text**

**langgraph\_memory\_demo**

**```**



**The default connection string is:**



**```text**

**postgresql://postgres:your\_password@localhost:5432/langgraph\_memory\_demo**

**```**



**If your PostgreSQL installation uses a different username, password, host, port, or database name, update `DATABASE\_URL` accordingly.**



**The application automatically initializes the LangGraph PostgreSQL checkpointer when a valid PostgreSQL connection is available.**



**---**



**# ▶️ Running the Application**



**## Terminal Mode**



**Run:**



**```bash**

**python main.py**

**```**



**You will be prompted to enter a travel request.**



**Example:**



**```text**

**Plan a 5-day Paris trip from Mumbai under ₹1.5 lakh.**

**```**



**---**



**## 🌐 Streamlit Web Interface**



**Run:**



**```bash**

**streamlit run frontend.py**

**```**



**Streamlit will provide a local URL, normally:**



**```text**

**http://localhost:8501**

**```**



**Open the URL in your browser to use the graphical interface.**



**---**



**# 💬 Example Prompts**



**### Example 1**



**```text**

**Plan a 7-day Japan trip from Mumbai under ₹2 lakhs including flights, hotels and sightseeing.**

**```**



**### Example 2**



**```text**

**Plan a 5-day Paris trip from Mumbai under ₹1.5 lakhs.**

**```**



**### Example 3**



**```text**

**Plan a weekend trip to Dubai with accommodation and sightseeing recommendations.**

**```**



**---**



**# 📊 Example Workflow Output**



**A typical request produces information from multiple stages:**



**```text**

**Flight Agent**

&#x20;   **↓**

**Flight research**



**Hotel Agent**

&#x20;   **↓**

**Accommodation research**



**Itinerary Agent**

&#x20;   **↓**

**Day-by-day itinerary**



**Final Agent**

&#x20;   **↓**

**Consolidated travel plan**

**```**



**The final plan can be saved as a Markdown file inside:**



**```text**

**travel\_plans/**

**```**



**---**



**# ⚠️ Data and API Limitations**



**This project is intended as an AI travel-planning demonstration.**



**- Flight information depends on the AviationStack API and its available data.**

**- Web research depends on Tavily search results.**

**- Prices and availability should be independently verified before booking.**

**- AI-generated recommendations may require human verification.**

**- API availability and rate limits depend on the respective services.**

**- The application does not guarantee real-time booking availability or final travel prices.**



**Always verify flight schedules, accommodation availability, visa requirements, and travel regulations before making a booking.**



**---**



**# 🔐 Environment Variables**



**| Variable | Purpose |**

**|---|---|**

**| `GROQ\_API\_KEY` | Access to the Groq LLM |**

**| `TAVILY\_API\_KEY` | Web research |**

**| `AVIATIONSTACK\_API\_KEY` | Flight information |**

**| `DATABASE\_URL` | PostgreSQL connection |**



**---**



**# 🎯 Project Goals**



**This project demonstrates how multiple AI agents and external tools can be combined into a structured workflow.**



**The main concepts demonstrated include:**



**- Multi-agent AI systems**

**- LangGraph state management**

**- LLM-based reasoning**

**- Tool/API integration**

**- Web research**

**- Persistent workflow state**

**- PostgreSQL checkpointing**

**- Streamlit application development**

**- Modular Python architecture**



**---**



**# 🔮 Future Improvements**



**Potential future enhancements include:**



**- Real-time flight price comparison**

**- More precise date and route extraction**

**- Additional hotel APIs**

**- Budget optimization**

**- Weather integration**

**- Currency conversion**

**- Visa requirement research**

**- Map integration**

**- Parallel agent execution**

**- More specialized travel agents**

**- User preference memory**

**- Deployment to a cloud platform**



**---**



**# 👤 Author**



**\*\*Soham Bagdane\*\***



**B.Tech — Artificial Intelligence \& Data Science**



**Interested in:**



**- Artificial Intelligence**

**- Machine Learning**

**- Generative AI**

**- Multi-Agent Systems**

**- Data Science**

**- Software Development**



**---**



**## ⭐ Project**



**If you find this project useful or interesting, consider giving the repository a star.**



**\*\*GitHub:\*\***  

**https://github.com/sohambagdane/travel-agent-using-langgraph**

