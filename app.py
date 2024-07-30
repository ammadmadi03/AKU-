from flask import Flask, request, jsonify
from md_pdf_json import parse_resume
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/upload": {"origins": "*"}})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'res_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['res_file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.pdf'):
        info = parse_resume(file)

        return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True)