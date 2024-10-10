from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import os
from main import PurduePrepBackend

app = Flask(__name__)
CORS(app)  # allow Cross-Origin requests, required for communication between frontend and backend
input_str = None  # global variable for use in both API routes (input and output)

# API route for receiving input
@app.route('/api/receive-text', methods=['POST'])
def receive_text():
    global input_str
    if 'file' in request.files:
        file = request.files['file']
        file_extension = os.path.splitext(file.filename)[1].lower()

        if file_extension == '.txt':
            input_str = file.read().decode('utf-8')  # Read text file content
        elif file_extension == '.pdf':
            input_str = extract_text_from_pdf(file)
        else:
            return jsonify({"error": "Unsupported file type"}), 400
    else:
        # This is plain text input, now using JSON to get inputText
        input_str = request.json.get('inputText')

    if input_str is None:
        return jsonify({"error": "No input text provided"}), 400
    print("input string: " + input_str)
    # Respond back to the frontend with a success message
    return jsonify({"message": "Text received successfully", "receivedText": input_str})

# helper function for reading from pdf
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

# API route to serve questions with URLs
@app.route('/api/get-questions', methods=['GET'])
def get_questions():
    if input_str is None:
        return jsonify({"error": "No input data available"}), 400
    questions = PurduePrepBackend(input_str)
    questions_with_urls = [{"question": q, "url": url} for q, url in questions]
    return jsonify({"questions": questions_with_urls})

if __name__ == '__main__':
    app.run(port=5328)