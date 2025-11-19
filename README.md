TOC 2025 Final Project

Intelligent Agents with Large Language Models (LLMs)

📌 Overview

This project implements an intelligent agent capable of interacting with a Large Language Model (LLM) through API-based communication. The agent is designed to understand user tasks, generate structured prompts, interpret LLM outputs, and execute follow-up actions according to the system’s internal logic.

The goal of this project is to demonstrate the design of autonomous or semi-autonomous AI agents with clear workflow modeling, robust system logic, and practical applications.

🎯 Project Objectives

Build an agent that communicates with a provided LLM API.

Design a well-structured workflow using a State Machine Diagram or DAG.

Implement an end-to-end pipeline including task understanding, prompt generation, API interaction, and action execution.

Deliver a working prototype, live demo, and project report.

🔧 Features

LLM API Integration

Uses the teacher-assigned API key.

Sends structured prompts and receives responses from the LLM.

API usage follows security and responsible-use guidelines.

Agent Workflow Automation

Understands user queries.

Executes logic based on internal states or task type.

Produces actionable outputs (text, summaries, retrieval results, etc.).

Workflow Logic Diagram

A State Machine or DAG illustrating:

Input processing

LLM query construction

Response interpretation

Execution of actions

Terminal or looping state transitions

Extendable Architecture

The project is built with modular components, allowing future expansion into RAG, scheduling, multi-agent interaction, or personalized assistants.

📂 Repository Structure (example)
project-root/
│── src/
│   ├── agent.py
│   ├── llm_api.py
│   ├── pipeline.py
│   └── utils/
│── diagrams/
│   └── state_machine.png
│── data/
│── README.md
│── requirements.txt
│── report.pdf

🛠 Technologies

No programming language restrictions.
(Example below—modify as needed.)

Python 3.x

Requests / HTTP client for API calls

Matplotlib (optional visualization)

JSON for structured data

Any framework or library based on project needs

🧪 How to Run the Project

Clone this repository:

git clone <your_repo_url>
cd <your_repo>


Install dependencies:

pip install -r requirements.txt


Add your API key (provided by TA).

Option A: Create .env

Option B: Export environment variable

export TOC_API_KEY="your_key"


Run the agent:

python src/agent.py

📝 State Machine / DAG

Your project includes a system diagram (example):

State 1 — Receive Input

State 2 — Task Classification

State 3 — Prompt Construction

State 4 — LLM API Call

State 5 — Response Parsing

State 6 — Execute Action

State 7 — Output to User / Loop / Terminate

Diagram located in:
/diagrams/state_machine.png

📊 Evaluation Criteria

As defined by the course:

✔ Essential Requirements (must pass)

Uses the provided LLM API.

Working demo with code accessible on GitHub.

Includes a State Machine Diagram or DAG.

⭐ Encouragement Level (50 pts)

Implements the TA’s toy example or similar baseline.

🚀 Advanced Level (50–100 pts)

Creativity, innovation, and unique features.

Clear and effective presentation.

Clean code with good structure and documentation.

💡 Example Project Ideas (from course)

RAG Agent

Study Helper

Personal Diary Agent (LINE chatbot integration)

Any innovative multi-step reasoning or tool-using agent

👥 Team Information

Team Size: 1–3

All members receive the same score.

(Fill below as needed)

Name	Student ID	Role
		
📌 Demo Information

Demos are held around week 17.

TA will provide the sign-up sheet.

TA reserves the right to adjust schedules.
