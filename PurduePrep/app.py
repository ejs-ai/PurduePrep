from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow Cross-Origin requests, required for communication between frontend and backend

@app.route('/api/receive-text', methods=['POST'])
def receive_text():
    data = request.json  # Get the JSON data from the request body
    input_text = data.get('inputText')  # Access the input text sent from the frontend
    
    # Save the input to a file so it can be read by main.py
    with open('input_text.txt', 'w') as fp:
        fp.write(input_text)

    # Respond back to the frontend with a success message or processed data
    return jsonify({"message": "Text received successfully", "receivedText": input_text})


if __name__ == '__main__':
    app.run(port=5328)