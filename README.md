# AI Relationship Analyst Agent (TOC 2025 Final Project)
An intelligent agent capable of analyzing chat logs to identify attachment styles and conflict patterns based on Gottman & EFT psychological models.

## Project Description
This project implements an AI Agent that acts as a relationship counselor. Unlike simple chatbots, this agent uses a State Machine workflow to process long conversation histories, identifies psychological features (Anxious/Avoidant attachment), detects vicious conflict cycles, and generates a comprehensive Relationship Health Report.

The system demonstrates advanced LLM usage, including Function Calling, Token Chunking, and Structured Output Generation.

## Key Features
* Psychological Profiling: Automatically extracts keywords to determine Attachment Styles (Secure, Anxious, Avoidant).
* Conflict Pattern Mining: Identifies negative interaction cycles (e.g., "Pursue-Withdraw" patterns).
* Intelligent Workflow: Uses an FSM to handle large datasets via chunking (intermediate state) rather than simple linear processing.
* Tool Usage: The LLM dynamically decides whether to perform psychological analysis or conflict mining based on context.

## System Architecture
### System Flow Chart (DAG)
<img width="2133" height="693" alt="TOC_flow_chart" src="https://github.com/user-attachments/assets/210470c3-6596-4942-90fd-8ed45d846a4b" />

### Finite State Machine (FSM)
<img width="1686" height="508" alt="TOC_FSM-2025-11-24-082639" src="https://github.com/user-attachments/assets/c7d192da-142e-4424-8d59-04719ed8d2e8" />

## Quick Start (Online Demo)

If you prefer not to set up the local environment, you can try our deployed online version immediately.

👉 **Try it here: [AI Relationship Analyst Agent (Render Online)](https://two025theory-of-computation-final-svz3.onrender.com/)**

---

### Important Note (Please Read)

This project is hosted on Render's free tier. If the website is inactive for **15 minutes**, the server will automatically go to sleep to conserve resources.

**When you visit the link, you may see a loading screen similar to the image below. Please be patient and wait for about 30 seconds to 1 minute for the server to wake up.**

<img width="1906" height="808" alt="530450654-ce6891df-d117-4821-a7d1-edce5ef8fb8f" src="https://github.com/user-attachments/assets/276a33e9-c9dd-43e8-8ba8-ee7654889bc9" />




---

### Dual Mode Features

Once the site loads, you can switch between two modes using the buttons in the top-right corner:

### 1. Consultation Mode 📖 
This mode provides in-depth analysis. Please describe your relationship issue and provide actual chat logs. The system will use built-in psychological models to generate a detailed emotional analysis report for you.

<img width="1918" height="992" alt="image" src="https://github.com/user-attachments/assets/647b2ad4-15f9-4dcc-9049-afd9428a1ebf" />

### 2. Conversation Mode 💬 
This mode offers real-time interaction. You can chat with the AI companion for immediate responses and emotional support, just like talking to a friend.

<img width="1918" height="983" alt="image" src="https://github.com/user-attachments/assets/3f7c5deb-fb92-4179-b9b4-8729f481be3d" />

<br>

## How to Run
### Prerequisites
* Python 3.8+
* An LLM API Key
### Installation
1. Clone the repository:
   ```text
   git clone https://github.com/JKaiWang/2025Theory_Of_Computation_Final_Project.git
   ```
2. Install dependencies:
   ```text
   pip install -r requirements.txt
   ```
3. Set up your API Key:
   Create a API.txt file or update config.py.
   ```text
   LLM_API_KEY = "your_key_here"
   ```
5. Run the Agent:
   ```text
   python main.py
   ```
   or
   ```text
   uvicorn web.app:app --reload
   ```
   
6. Open your browser
   ```text
   http://localhost:8000
   ```

## Project Structure
```text
2025Theory_Of_Computation_Final_Project/
│
├── chat_sessions/          # [Data Storage] Stores user-saved chat histories (.json)
│
├── src/                    # [Core Logic] Main source code directory for the AI Agent
│   ├── interface/          # Interface integration modules (e.g., WebAgent wrapper)
│   ├── agent.py            # Agent state machine and core decision-making logic
│   ├── config.py           # Configuration (environment variables, parameters)
│   ├── knowledge.py        # Psychological knowledge base (Gottman/EFT models)
│   ├── llm_client.py       # LLM API client wrapper
│   └── prompts.py          # System prompts and instruction management
│
├── tools/                  # [Utilities] Helper scripts for testing or development
│
├── web/                    # [Web App] FastAPI backend and frontend assets
│   ├── static/             # Static assets directory (Frontend Core)
│   │   ├── index.html      # Main HTML: 3D book UI, cover, and forms
│   │   ├── script.js       # Frontend logic: Animations, API calls, report rendering
│   │   ├── style.css       # Stylesheets: 3D book effects, hard cover, RWD layout
│   │   └── wood.jpg        # Asset: Background texture image
│   │
│   └── app.py              # FastAPI Backend: Routes, analysis logic, file downloads
│
├── web_reports/            # [Output] Stores generated analysis reports (.md)
│
├── .env                    # Environment variables (API keys, secrets)
├── .gitignore              # Git ignore configuration
├── main.py                 # Main entry point (CLI mode or integration testing)
├── README.md               # Project documentation
└── requirements.txt        # Python dependency list
```
### Note on Advanced Level Implementation
This project goes beyond the basic toy example by implementing:
* Complex State Transitions: Specifically the intermediate loop for handling token limits.
* Domain-Specific Prompts: Custom prompts engineered for psychological analysis (Gottman method).
* Dual-Tool Architecture: Separating individual attachment analysis from interaction pattern mining.

## How to Use Save Chat History and Load Chat History (Web UI)

### Save Chat History
1. Fill in the form: Your Name, Partner's Name, Context, and Chat Logs.
2. Click **Save Chat History**. The current chat session will be saved as a JSON file on the server.
3. A **Download Chat** button will appear. Click it to download the chat history (`.json` file) to your computer.

### Load Chat History
1. Click **Load Chat History**. A file picker will appear.
2. Select a previously saved chat history JSON file (e.g., `chat_xxx.json`).
3. The form will be automatically filled with the loaded chat data.
4. You can add new messages to the **Chat Logs** field.
5. Click **Save Chat History** again to save the updated chat session (it will create a new JSON file).

This workflow allows you to archive, reload, and append new messages to your chat sessions easily.
