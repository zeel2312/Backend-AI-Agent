# AI Agent for Backend System Operation Using Natural Language

## Project Overview
This project introduces an AI agent that enables users to interact with a backend system using natural language. By bridging the gap between human communication and database manipulation, it simplifies backend operations for non-technical users, allowing them to perform database tasks such as **insert**, **update**, and **delete** through an intuitive web-based interface.

---

## Key Features

- **Natural Language Processing (NLP):**
  - Utilizes OpenAI's ChatGPT-4 model for interpreting user inputs.
  - Translates natural language queries into structured commands for backend operations.
  - Supports synonyms and diverse phrasing for improved flexibility and usability.

- **Backend Key-Value Store:**
  - Built with **Supabase** for a dynamic database structure.
  - Supports core functionalities: `insert`, `update`, and `delete`.
  - Tracks changes with a timestamp-based audit trail.

- **User Interface:**
  - A responsive web-based interface for seamless interaction.
  - Displays database state and provides real-time feedback on operations.

- **Integration Layer:**
  - Manages communication between user inputs, LLM processing, and database execution.
  - Ensures accurate interpretation of user intentions.

---

## Implementation Highlights

- Designed prompts for ChatGPT-4 to process natural language queries accurately.
- Used Supabase for a robust key-value store with timestamp tracking.
- Developed a responsive React-based web interface for real-time interaction.
- Validated the system with extensive testing for reliability and accuracy.

---

## Key Achievements

- Enabled seamless translation of natural language commands into backend operations using ChatGPT-4.
- Enhanced usability by recognizing synonyms and flexible phrasing.
- Implemented an audit trail to track all database changes.
- Simplified backend operations for non-technical users with an intuitive interface.

---

## Future Enhancements

- Expand NLP capabilities for handling more nuanced and complex queries.
- Integrate machine learning for continuous improvement in natural language understanding.
- Add support for more backend databases and APIs.
- Enhance the interface with advanced visualization and reporting tools.

---

## Getting Started

### Steps to Clone and Run the Project

1. **Clone the Repository**
   git clone https://github.com/<your-username>/Backend-AI-Agent.git
   cd Backend-AI-Agent
2. **Install Dependencies**
  - Navigate to the frontend directory (React app) and install the required dependencies:
    cd src
    npm install
3. **Set Up the Database**
    - Create an account at Supabase.
    - Create a new database and a table with the following fields:
      Key (String)
	    Value (String)
	    Created At (Timestamp)
	    Updated At (Timestamp)
4. **4.	Run the Servers**
    - npm start
    - python app.py

## Technologies Used
  - Frontend: React.js
  - Backend: Python
  - Database: Supabase
  - AI: OpenAI’s ChatGPT-4 for NLP
  - Tools: npm, Python
