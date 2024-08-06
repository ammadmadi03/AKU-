from flask import Flask, request, jsonify
import extract_data as ed
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and (file.filename.endswith('.pdf') or file.filename.endswith('.docx')):
        return jsonify(ed.parse_resume(file))

if __name__ == '__main__':
    app.run(debug=True)