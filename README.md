# RAG-Chatbot
# Flask-Based RAG Chatbot with FAISS and MySQL

This project implements a Retrieval-Augmented Generation (RAG) chatbot using Flask, FAISS for vector similarity search, and MySQL for chat history storage. It processes PDF documents, splits them into chunks, embeds the chunks, and retrieves relevant content to answer user queries.

---

## Features

- **Document Preprocessing**: Splits large PDF files into smaller chunks for efficient processing.
- **FAISS Vector Database**: Stores chunk embeddings for fast similarity-based retrieval.
- **RAG Chatbot**: Uses relevant chunks as context to answer user queries.
- **Chat History**: Stores user queries and system responses in a MySQL database.
- **API Endpoints**:
  - `POST /chat`: Accepts user queries and returns the generated answer.
  - `GET /history`: Retrieves chat history from the database.

---

## Requirements

- Python 3.8+
- MySQL database
- Required libraries (listed in `requirements.txt`)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Harsh6063/rag-chatbot.git
   cd rag-chatbot

2. Install dependicies
   
       pip install -r requirements.txt

3. Set up the MySQL database:

- Create a database with name of your choice
- Run the following SQL commands to create the chat_history table:
   ```bash
       CREATE TABLE chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(10) NOT NULL,
    content TEXT NOT NULL);

4. Add your PDF file(that you want to use the chatbot from): Place the PDF document you want to use in the project directory and update the pdf_file_path in the code.

   ## Usage

1. Start the Flask Server
Run the app(in terminal):
   ```bash
   python rag_chatbot.py
The server will start at http://127.0.0.1:5000.

2 . API Endpoints
- a) Chat Endpoint
- URL: POST /chat
   ```bash
   curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d "{\"query\": \"What is this document about?\"}"


- b) Chat History Endpoint
- URL: GET /history
   ```bash
   curl http://127.0.0.1:5000/history


## How It Works
-Document Preprocessing:

- Reads a PDF file.
- Cleans and splits the text into ~300-word chunks.
- Embedding:

- Generates embeddings for each chunk using the sentence-transformers library.
- Stores these embeddings in a FAISS vector database.
- Querying:

- User query is embedded and compared with stored embeddings in FAISS.
- Retrieves the top-k most relevant chunks.
- Answer Generation:
- Combines relevant chunks with the user query to generate an answer.
 - Chat History:

- Saves user queries and system answers in a MySQL database for future reference.


  

