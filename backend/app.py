import os
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import io

from modules.form_module import process_form_data
from modules.voice_module import process_voice_data
from modules.cv_builder import generate_ats_cv

load_dotenv()

app = Flask(__name__)
CORS(app) # Allow frontend to communicate

@app.route('/api/generate/form', methods=['POST'])
def generate_from_form():
    try:
        data = request.json
        # 1. Process and enhance data using Groq & Web Scraping
        enhanced_data = process_form_data(data)
        
        # 2. Build ATS-friendly PDF
        pdf_buffer = generate_ats_cv(enhanced_data)
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"{enhanced_data.get('name', 'CV').replace(' ', '_')}_CV.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate/voice', methods=['POST'])
def generate_from_voice():
    try:
        data = request.json
        transcript = data.get('transcript', '')
        
        # 1. Extract structured data from voice transcript using Groq
        structured_data = process_voice_data(transcript)
        
        # 2. Build ATS-friendly PDF
        pdf_buffer = generate_ats_cv(structured_data)
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name="Voice_Generated_CV.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)