from flask import Flask, request, jsonify
import pyp_extract_data as ped
import fitz_extract_data as fed
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.pdf'):
        # info = ped.parse_resume(file)
        info = fed.parse_resume(file)

        return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True)