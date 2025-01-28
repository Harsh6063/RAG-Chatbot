from flask import Flask, request, jsonify
import mysql.connector
import time
from Chatbot import (
    read_pdf, clean_text, split_into_chunks,
    embed_text, store_vectors_faiss, retrieve_chunks
)
import numpy as np
# Initialize Flask app
app = Flask(__name__)

# MySQL Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="6063",
    database="harsh"
)

cursor = db.cursor()

# Function to generate answers
def generate_answer(query, relevant_chunks):
    context = " ".join(relevant_chunks)
    return f"Answer based on context:\n\n{context}"

# Store chat in MySQL
def store_chat(role, content):
    sql = "INSERT INTO chat_history (role, content) VALUES (%s, %s)"
    cursor.execute(sql, (role, content))
    db.commit()

# Preprocess the document (Run once)
pdf_file_path = "harry-potter-sorcerers-stone.pdf"
pdf_text = read_pdf(pdf_file_path)
cleaned_text = clean_text(pdf_text)
chunks = split_into_chunks(cleaned_text)
embeddings, model = embed_text(chunks)
index = store_vectors_faiss(np.array(embeddings))

# Flask Endpoints
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query', '')

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    # Retrieve relevant chunks and generate answer
    relevant_chunks = retrieve_chunks(query, model, index, chunks, top_k=3)
    answer = generate_answer(query, relevant_chunks)

    # Store user query and system answer in the database
    store_chat("user", query)
    store_chat("system", answer)

    # Return response
    return jsonify({
        'query': query,
        'answer': answer,
        'relevant_chunks': relevant_chunks  # Optional debugging info
    })

@app.route('/history', methods=['GET'])
def history():
    cursor.execute("SELECT * FROM chat_history ORDER BY timestamp ASC")
    rows = cursor.fetchall()

    history = []
    for row in rows:
        history.append({
            'id': row[0],
            'timestamp': row[1].strftime('%Y-%m-%d %H:%M:%S'),
            'role': row[2],
            'content': row[3]
        })

    return jsonify(history)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
