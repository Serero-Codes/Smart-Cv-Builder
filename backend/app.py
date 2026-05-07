from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from modules.form_module import generate_form_cv
from modules.voice_module import handle_voice_chat

app = Flask(__name__)
CORS(app)

# =========================
# FORM MODE
# =========================
@app.route("/generate-cv", methods=["POST"])
def generate_cv():

    data = request.get_json()

    file_path = generate_form_cv(data)

    return send_file(
        file_path,
        as_attachment=True,
        download_name="CareerPilot_CV.pdf"
    )


# =========================
# VOICE MODE
# =========================
@app.route("/voice-chat", methods=["POST"])
def voice_chat():

    data = request.get_json()

    response = handle_voice_chat(data)

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=5000)