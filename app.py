from flask import Flask, request, jsonify
from flask_cors import CORS

# Set Root folder
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import required modules
from vectordb import store_chunks, query_chunks, read_pdf, content_to_chunks
from llm import answer_question

app = Flask(__name__)
CORS(app)  


# Upload files
@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        url = data.get('url')
        pdf_content = read_pdf(url)
        chunks  = content_to_chunks(pdf_content)
        store_chunks(chunks)
        return jsonify({'response': 'PDF uploaded successfully'}), 200
    except:
        return jsonify({'response': 'Error while uploading'})

# Handle user chat
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    rel_chunks = query_chunks(user_message, top_n=10)

    response = answer_question(user_message, " ".join(rel_chunks))
    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(debug=True)