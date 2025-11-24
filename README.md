# ❤️ AI Relationship Analyst Agent ❤️(TOC 2025 Final Project)
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

## How to Run
### Prerequisites
* Python 3.8+
* An LLM API Key
### Installation
1. Clone the repository:
   ```text
   git clone https://github.com/pukyle/2025Theory_Of_Computation_Final_Project.git
   ```
2. Install dependencies:
   ```text
   pip install -r requirements.txt
   ```
3. Set up your API Key:
   Create a .env file or update config.py.
   ```text
   LLM_API_KEY = "your_key_here"
   ```
5. Run the Agent:
   ```text
   python main.py
   ```
## Project Structure
```text
.
├── data/                   # Sample chat logs
├── src/
│   ├── agent.py            # Main FSM implementation
│   ├── tools.py            # Psych & Conflict analysis tools
│   ├── llm_client.py       # API handling
│   └── utils.py            # Preprocessing & Chunking
├── report/                 # Generated HTML reports
├── main.py                 # Entry point
├── requirements.txt
└── README.md
```
### Note on Advanced Level Implementation
This project goes beyond the basic toy example by implementing:
* Complex State Transitions: Specifically the intermediate loop for handling token limits.
* Domain-Specific Prompts: Custom prompts engineered for psychological analysis (Gottman method).
* Dual-Tool Architecture: Separating individual attachment analysis from interaction pattern mining.
