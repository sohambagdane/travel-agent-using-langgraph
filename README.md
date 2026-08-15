# Tool-Calling AI Agent

A Python-based AI agent that can understand user requests, decide which tool is required, execute the tool, and use the result to generate a final response.

This project demonstrates the basic architecture of a **tool-calling AI agent**, including LLM interaction, tool selection, iterative execution, error handling, and execution trace logging.

---

## 🚀 Features

* LLM-powered agent for understanding natural-language requests
* Automatic tool selection based on the user's query
* Multiple custom tools
* Iterative tool-calling loop
* Calculator tool for mathematical operations
* Country information tool using the Countries.dev API
* Secure file-reading tool with workspace restrictions
* Tool execution error handling
* Unknown-tool handling
* Invalid LLM response handling
* JSON trace logging for successful agent executions
* Modular project structure
* Environment-variable based API key configuration

---

## 🧠 How the Agent Works

The agent follows a simple reasoning and tool-execution workflow:

```text
User Query
    ↓
LLM
    ↓
Decide whether a tool is required
    ↓
Select Tool + Arguments
    ↓
Execute Tool
    ↓
Return Tool Result to LLM
    ↓
LLM decides next action
    ↓
Final Answer
```

The agent can perform multiple tool calls when required instead of being limited to a single tool execution.

---

## 🛠️ Available Tools

### 1. Calculator

The calculator tool performs mathematical calculations.

Example queries:

```text
Calculate 125 * 48
```

```text
What is (25 + 15) / 5?
```

The agent identifies that the calculator tool is required, executes it, and uses the result in the final response.

---

### 2. Country Information

The country API tool retrieves country information using the **Countries.dev API**.

Example queries:

```text
Tell me about India.
```

```text
What is the capital of Japan?
```

```text
Give me information about Norway.
```

The tool can retrieve information such as:

* Country name
* Capital
* Region
* Population
* Currency
* Languages
* Other available country information

---

### 3. Read File

The `read_file` tool allows the agent to read text files from the project's workspace directory.

Example:

```text
Read the contents of sample.txt
```

For security, file access is restricted to the configured workspace directory.

This prevents path traversal attempts from accessing arbitrary files outside the allowed workspace.

---

## 📁 Project Structure

```text
tool-calling-ai-agent/
│
├── agent.py
├── llm.py
├── config.py
├── prompts.py
├── requirements.txt
├── README.md
│
├── tools/
│   ├── __init__.py
│   ├── calculator.py
│   ├── country_api.py
│   └── read_file.py
│
├── workspace/
│   └── sample.txt
│
└── traces/
    └── ...
```

### File Description

| File / Directory       | Purpose                                         |
| ---------------------- | ----------------------------------------------- |
| `agent.py`             | Main agent loop and tool orchestration          |
| `llm.py`               | LLM configuration and communication             |
| `config.py`            | Project configuration and environment variables |
| `prompts.py`           | System prompts and tool-calling instructions    |
| `requirements.txt`     | Python dependencies                             |
| `tools/calculator.py`  | Calculator tool                                 |
| `tools/country_api.py` | Country information API tool                    |
| `tools/read_file.py`   | Secure file-reading tool                        |
| `workspace/`           | Allowed directory for files used by the agent   |
| `traces/`              | Stores successful agent execution traces        |
| `README.md`            | Project documentation                           |

---

## ⚙️ Requirements

Make sure you have:

* Python 3.10 or later
* pip
* Internet connection
* An API key for the configured LLM provider

---

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/sohambagdane/tool-calling-ai-agent.git
```

### 2. Navigate to the project

```bash
cd tool-calling-ai-agent
```

### 3. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 Install Dependencies

Install all required packages using:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory.

Example:

```env
GEMINI_API_KEY=your_api_key_here
```

Replace:

```text
your_api_key_here
```

with your actual API key.

### Important

Do not commit your `.env` file or expose your API key publicly.

Add `.env` to `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
```

---

## ▶️ Running the Agent

Run the main agent using:

```bash
python agent.py
```

The agent will accept a user query and determine whether one or more tools are required.

---

## 💡 Example Queries

### Calculator

```text
Calculate 125 * 48
```

Expected behavior:

```text
The agent selects the calculator tool,
executes the calculation,
and returns the result.
```

---

### Country API

```text
What is the capital of India?
```

Expected behavior:

```text
The agent selects the country_api tool,
retrieves the country information,
and generates the final answer.
```

---

### File Reading

Create a file:

```text
workspace/sample.txt
```

with some text inside it.

Then ask:

```text
Read sample.txt
```

The agent will use the `read_file` tool to retrieve the contents.

---

## 🔄 Iterative Tool Calling

One of the important features of this project is that the agent is not restricted to a single tool call.

The agent can follow an iterative process:

```text
Iteration 1
    ↓
LLM selects a tool
    ↓
Tool executes
    ↓
Tool result returned to LLM
    ↓
Iteration 2
    ↓
LLM decides whether another tool is required
    ↓
...
    ↓
Final response
```

A maximum iteration limit is used to prevent the agent from running indefinitely.

---

## 🧩 Error Handling

The agent includes handling for several failure scenarios.

### Unknown Tool

If the LLM requests a tool that does not exist, the agent returns an appropriate error instead of crashing.

### Tool Execution Error

If a tool fails during execution, the error is captured and returned to the agent.

### Invalid LLM Response

If the LLM returns an unexpected or invalid response format, the agent handles it gracefully.

### Maximum Iterations

The agent stops after reaching the configured maximum number of iterations.

This prevents infinite tool-calling loops.

---

## 📊 Execution Traces

Successful agent executions can be stored as JSON trace files inside:

```text
traces/
```

These traces can be used to understand how the agent processed a request.

A trace can contain information such as:

```text
User query
↓
LLM decision
↓
Selected tool
↓
Tool arguments
↓
Tool result
↓
Next LLM decision
↓
Final response
```

This makes the project easier to debug, test, and evaluate.

---

## 🔒 Security Considerations

The `read_file` tool is designed to prevent unauthorized file access.

Instead of allowing arbitrary filesystem paths, file access is restricted to the configured workspace directory.

For example, requests attempting to access files outside the workspace should not be permitted.

This provides basic protection against:

* Path traversal
* Unauthorized filesystem access
* Reading sensitive files outside the project workspace

API keys are also stored through environment variables rather than directly inside source code.

---

## 🏗️ Architecture

The project is divided into separate components.

```text
                ┌─────────────────┐
                │    User Query   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │    Agent        │
                │   agent.py      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │      LLM        │
                │     llm.py      │
                └────────┬────────┘
                         │
                  Tool Selection
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
   ┌────────────┐ ┌─────────────┐ ┌────────────┐
   │ Calculator │ │ Country API │ │ Read File  │
   └─────┬──────┘ └──────┬──────┘ └─────┬──────┘
         │               │              │
         └───────────────┼──────────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Tool Result   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │      LLM        │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Final Answer   │
                └─────────────────┘
```

---

## 🧪 Testing

The individual tools can be tested independently before running the complete agent.

For example, test the calculator:

```bash
python tools/calculator.py
```

Test the country API:

```bash
python tools/country_api.py
```

Test the file reader:

```bash
python tools/read_file.py
```

The complete system can then be tested through:

```bash
python agent.py
```

---

## 🌐 API Used

The country information tool uses:

**Countries.dev**

The API is used to retrieve country-related information dynamically rather than maintaining a static country database inside the project.

---

## 📌 Key Concepts Demonstrated

This project demonstrates several important concepts used in modern AI-agent systems:

* Large Language Models (LLMs)
* Tool Calling
* Function Calling
* Agent Loops
* Prompt Engineering
* API Integration
* Structured Tool Inputs
* Tool Execution
* Error Handling
* Iterative Reasoning
* Secure File Access
* Environment Variables
* JSON Logging
* Modular Python Architecture

---

## 🚀 Future Improvements

The project can be extended with additional capabilities such as:

* More tools
* Database querying
* Web search
* Email automation
* Weather information
* Calendar integration
* Authentication
* Streaming responses
* Better tool validation
* Persistent conversation memory
* Agent evaluation framework
* Web-based user interface
* Docker deployment

---

## 🎯 Project Objective

The main objective of this project is to demonstrate how an AI system can move beyond simply generating text and instead **interact with external tools to perform real tasks**.

The project provides a basic but extensible foundation for building more advanced AI agents.

---

## 👨‍💻 Author

**Soham Bagdane**

B.Tech – Artificial Intelligence & Data Science

GitHub:
https://github.com/sohambagdane

---

## 📄 License

This project is intended for educational and demonstration purposes.
