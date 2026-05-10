# VOICE_QUESTIONS = [
#     "What is your full name?",
#     "What is your email address?",
#     "What is your phone number?",
#     "What is your GitHub profile?",
#     "Which city do you live in?",
#     "Which province are you in?",
#     "What is your target job role?",
#     "List your technical skills",
#     "List your soft skills",
#     "What is your education background?",
#     "What certifications do you have?",
#     "Describe your professional experience",
#     "Describe your first project",
#     "Describe your second project"
# ]

# sessions = {}

# def handle_voice_chat(data):

#     user_id = data.get("user_id", "default")
#     message = data.get("message", "")

#     if user_id not in sessions:
#         sessions[user_id] = {
#             "step": 0,
#             "answers": {}
#         }

#     session = sessions[user_id]
#     step = session["step"]

#     # store answer
#     if step > 0:
#         session["answers"][step - 1] = message

#     # done
#     if step >= len(VOICE_QUESTIONS):

#         return {
#             "done": True,
#             "message": "All data collected. Generating CV...",
#             "data": session["answers"]
#         }

#     # next question
#     question = VOICE_QUESTIONS[step]
#     session["step"] += 1

#     return {
#         "done": False,
#         "message": question
#     }


import os
import json
from groq import Groq

def process_voice_data(transcript):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    prompt = f"""
    Extract IT CV information from the following user voice transcript.
    Structure it perfectly for an ATS-friendly CV.
    
    Transcript: "{transcript}"
    
    Return ONLY a valid JSON object with keys: "name", "links", "summary", "skills", "experience", "projects".
    Do not include markdown tags like ```json.
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        response_format={"type": "json_object"}
    )
    
    try:
        raw_content = response.choices[0].message.content
        clean_content = raw_content.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_content)
    except:
        # Fallback empty structure
        return {"name": "Voice User", "summary": transcript, "skills": "", "experience": "", "projects": ""}