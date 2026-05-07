VOICE_QUESTIONS = [
    "What is your full name?",
    "What is your email address?",
    "What is your phone number?",
    "What is your GitHub profile?",
    "Which city do you live in?",
    "Which province are you in?",
    "What is your target job role?",
    "List your technical skills",
    "List your soft skills",
    "What is your education background?",
    "What certifications do you have?",
    "Describe your professional experience",
    "Describe your first project",
    "Describe your second project"
]

sessions = {}

def handle_voice_chat(data):

    user_id = data.get("user_id", "default")
    message = data.get("message", "")

    if user_id not in sessions:
        sessions[user_id] = {
            "step": 0,
            "answers": {}
        }

    session = sessions[user_id]
    step = session["step"]

    # store answer
    if step > 0:
        session["answers"][step - 1] = message

    # done
    if step >= len(VOICE_QUESTIONS):

        return {
            "done": True,
            "message": "All data collected. Generating CV...",
            "data": session["answers"]
        }

    # next question
    question = VOICE_QUESTIONS[step]
    session["step"] += 1

    return {
        "done": False,
        "message": question
    }