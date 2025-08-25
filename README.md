# Multi-Agent Market Analysis Workflow

This project demonstrates a multi-agent workflow that automates the creation of comprehensive market analysis reports. It uses specialized AI agents, powered by local open-source LLMs, that collaborate to research a given topic and write a detailed report.

This project is built using **CrewAI**, a modern framework for orchestrating autonomous AI agents.

## Table of Contents

- [About The Project](#about-the-project)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Directory Structure](#directory-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Example Usage](#example-usage)
- [Future Improvements](#future-improvements)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## About The Project

The goal of this project is to provide a clear, runnable example of a multi-agent system. Instead of using a single, monolithic AI model, we delegate tasks to specialized agents, mimicking a real-world team:

*   **`ResearchAgent`**: This agent is responsible for browsing the internet to find the latest trends, news, and data related to a specific market topic.
*   **`WriterAgent`**: This agent takes the structured findings from the researcher and is responsible for composing a professional, well-structured, and insightful report.

This approach leads to higher quality results as each agent is fine-tuned for its specific role.

## How It Works

The workflow is orchestrated by `main.py` using the CrewAI framework:

1.  **Initialization**: The script initializes the agents (Researcher, Writer) and the tasks they need to perform.
2.  **User Input**: It prompts the user to specify a market topic to analyze.
3.  **Task Execution**: The crew begins its work in a sequential process:
    a. The `research_task` is assigned to the `ResearchAgent`. The agent uses the Tavily Search tool to gather information.
    b. The output of the `research_task` is automatically passed as context to the `writing_task`.
    c. The `writing_task` is assigned to the `WriterAgent`, who uses the research context to draft the final report.
4.  **Output**: The final, complete report is printed to the console and saved as a Markdown file in the `reports/` directory.

## Tech Stack

This project is built with a focus on open-source and free-tier tools:

*   **Orchestration Framework**: [CrewAI](https://github.com/joaomdmoura/crewAI)
*   **LLM (Large Language Model)**: [Ollama](https://ollama.com/) running a local model like `llama3:8b`.
*   **Web Search Tool**: [Tavily Search API](https://tavily.com/) (uses a generous free tier).
*   **Language**: Python 3.9+

## Directory Structure

Folder

```multi-agent-workflow/
├── .env # Stores API keys and configuration
├── README.md # This file
├── requirements.txt # Python dependencies
├── main.py # Main script to run the crew
├── agents/ # Agent definitions
│ └── market_analysis_agents.py
├── tasks/ # Task definitions
│ └── market_analysis_tasks.py
└── tools/ # Agent tools
└── search_tools.py

```

## Getting Started

Follow these steps to get the project running on your local machine.

### Prerequisites

1.  **Python 3.9+**: Ensure you have Python installed.
2.  **Ollama**: You must have Ollama installed and running. Follow the instructions on the [Ollama website](https://ollama.com/).
3.  **Tavily API Key**: Get a free API key from [Tavily AI](https://tavily.com/).

### Installation & Setup

1.  **Pull the LLM Model:**
    Open your terminal and run this command to download the `llama3:8b` model.
    ```bash
    ollama pull llama3:8b
    ```

2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/multi-agent-workflow.git
    cd multi-agent-workflow
    ```

3.  **Create a Virtual Environment:**
    It's highly recommended to use a virtual environment.
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set Up Environment Variables:**
    Create a `.env` file in the root of the project by copying the example and add your Tavily API key.
    ```bash
    cp example.env .env # If you provide an example file, or just create a new .env
    ```
    Your `.env` file should look like this:
    ```
    TAVILY_API_KEY="YOUR_TAVILY_API_KEY"
    OPENAI_API_BASE='http://localhost:11434/v1'
    OPENAI_MODEL_NAME='llama3:8b'
    OPENAI_API_KEY='NA'
    ```

## Running the Application

Execute the `main.py` script from the root directory:

```bash
python main.py
```

