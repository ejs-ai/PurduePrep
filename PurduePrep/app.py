from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import os
from PurduePrep.main import main

app = Flask(__name__)
CORS(app)  # allow Cross-Origin requests, required for communication between frontend and backend
input_str = None  # global variable for use in both API routes (input and output)

# API route for receiving input
@app.route('/api/receive-text', methods=['POST'])
def receive_text():
    global input_str
    global num_questions

    if 'file' in request.files:
        file = request.files['file']
        file_extension = os.path.splitext(file.filename)[1].lower()

        num_questions = int(request.form.get('numQuestions', 15))  # Default to 15 if not provided

        if file_extension == '.txt':
            input_str = file.read().decode('utf-8')  # Read text file content
        elif file_extension == '.pdf':
            input_str = extract_text_from_pdf(file)
            print("Successful text read from pdf file.")
        else:
            return jsonify({"error": "Unsupported file type"}), 400
    else:
        # This is plain text input, now using JSON to get inputText
        input_str = request.json.get('inputText')
        num_questions = int(request.json.get('numQuestions', 15))  # Default to 15 if not provided
    
    if input_str is None:
        return jsonify({"error": "No input text provided"}), 400
    # Respond back to the frontend with a success message
    return jsonify({
        "message": "Text received successfully", "receivedText": input_str,
        "numQuestions": num_questions
    })

# helper function for reading from pdf
def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text() or ''
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return None

# API route to serve questions with URLs
@app.route('/api/get-questions', methods=['GET'])
def get_questions():
    if input_str is None:
        return jsonify({"error": "No input data available"}), 400
    questions = main(input_str, num_questions)
    if questions is None:
        return jsonify({"error": "Processing failed, no questions generated"}), 500

    try:
        questions_with_urls = [{"question": q, "url": url} for q, url in questions]
    except TypeError:
        return jsonify({"error": "Unexpected response format from main function"}), 500

    return jsonify({"questions": questions_with_urls})

if __name__ == '__main__':
    app.run(port=5328)