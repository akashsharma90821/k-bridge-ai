import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "kbridge-secret-key"


def get_korean_translation(improved_message, tone, mode):
    text = improved_message.lower().strip()

    korean_map = {
        "hi!": {
            "casual": "안녕!",
            "polite": "안녕하세요!",
            "formal": "안녕하십니까?"
        },
        "hello.": {
            "casual": "안녕!",
            "polite": "안녕하세요!",
            "formal": "안녕하십니까?"
        },
        "hello, nice to speak with you.": {
            "casual": "안녕! 만나서 반가워.",
            "polite": "안녕하세요! 만나서 반가워요.",
            "formal": "안녕하십니까. 만나 뵙게 되어 반갑습니다."
        },
        "hey, what are you doing?": {
            "casual": "지금 뭐 해?",
            "polite": "지금 뭐 하고 있어요?",
            "formal": "지금 무엇을 하고 계신가요?"
        },
        "what are you doing right now?": {
            "casual": "지금 뭐 해?",
            "polite": "지금 뭐 하고 있어요?",
            "formal": "지금 무엇을 하고 계신가요?"
        },
        "may i ask what you are doing right now?": {
            "casual": "지금 뭐 해?",
            "polite": "지금 뭐 하고 있어요?",
            "formal": "지금 무엇을 하고 계신가요?"
        },
        "can you send me the file soon?": {
            "casual": "파일 곧 보내줄래?",
            "polite": "파일을 곧 보내주실 수 있나요?",
            "formal": "파일을 곧 보내주실 수 있으신가요?"
        },
        "could you please send me the file soon?": {
            "casual": "파일 곧 보내줄래?",
            "polite": "파일을 곧 보내주실 수 있나요?",
            "formal": "파일을 곧 보내주실 수 있으신가요?"
        },
        "could you please send me the file as soon as possible?": {
            "casual": "파일 빨리 보내줄래?",
            "polite": "파일을 가능한 빨리 보내주실 수 있나요?",
            "formal": "파일을 가능한 한 빨리 보내주실 수 있으신가요?"
        },
        "do you want to meet this week?": {
            "casual": "이번 주에 만날래?",
            "polite": "이번 주에 만날 수 있을까요?",
            "formal": "이번 주에 편하신 시간에 만날 수 있을까요?"
        },
        "would you like to meet sometime this week?": {
            "casual": "이번 주에 만날래?",
            "polite": "이번 주에 만날 수 있을까요?",
            "formal": "이번 주에 편하신 시간에 만날 수 있을까요?"
        },
        "would it be possible for us to meet sometime this week?": {
            "casual": "이번 주에 만날래?",
            "polite": "이번 주에 만날 수 있을까요?",
            "formal": "이번 주에 편하신 시간에 만날 수 있을까요?"
        },
        "would you be available to meet at a convenient time?": {
            "casual": "언제 만날래?",
            "polite": "편한 시간에 만날 수 있을까요?",
            "formal": "편하신 시간에 만날 수 있을지 알려주시면 감사하겠습니다."
        },
        "thank you.": {
            "casual": "고마워.",
            "polite": "감사합니다.",
            "formal": "감사드립니다."
        },
        "i am sorry.": {
            "casual": "미안해.",
            "polite": "죄송해요.",
            "formal": "죄송합니다."
        }
    }

    if text in korean_map:
        return korean_map[text].get(tone, korean_map[text]["polite"])

    if mode == "workplace":
        if tone == "formal":
            return "더 정중하고 격식 있는 직장용 한국어 표현입니다."
        return "더 자연스럽고 공손한 직장용 한국어 표현입니다."

    if mode == "friend":
        if tone == "casual":
            return "친구끼리 자연스럽게 쓸 수 있는 한국어 표현입니다."
        return "친구에게도 예의 있게 들리는 한국어 표현입니다."

    if tone == "casual":
        return "자연스럽고 편한 한국어 표현으로 바꿨어요."
    elif tone == "formal":
        return "더 정중하고 격식 있는 한국어 표현으로 바꿨어요."
    return "더 자연스럽고 공손한 한국어 표현으로 바꿨어요."


def analyze_message(user_text, tone, mode):
    text = user_text.strip()
    lower_text = text.lower()

    improved_message = text
    korean_friendly = text
    cultural_note = ""

    if mode == "friend":
        context_note = "This is for a friendly conversation."
    elif mode == "workplace":
        context_note = "This is for a professional workplace setting."
    else:
        context_note = "This is for normal daily conversation."

    if lower_text in ["hi", "hii", "hello", "hey", "heyy"]:
        if tone == "casual":
            improved_message = "Hi!"
            korean_friendly = "Hi! How are you?"
            cultural_note = "This is a simple and friendly greeting for casual conversation."
        elif tone == "polite":
            improved_message = "Hello."
            korean_friendly = "Hello, how are you?"
            cultural_note = "This sounds polite and natural for everyday respectful conversation."
        else:
            improved_message = "Hello, nice to speak with you."
            korean_friendly = "Hello, it is nice to speak with you."
            cultural_note = "This sounds more formal and respectful, which is better in professional or unfamiliar situations."

    elif "thank" in lower_text:
        improved_message = "Thank you."
        korean_friendly = "Thank you for your help."
        cultural_note = "Expressions of gratitude are very important in Korean communication and help maintain warmth and respect."

    elif "sorry" in lower_text:
        improved_message = "I am sorry."
        korean_friendly = "I am sorry about that."
        cultural_note = "A clear and respectful apology sounds better in Korean communication than a casual short apology."

    elif "bro tu kya kar raha hai" in lower_text:
        if tone == "casual":
            improved_message = "Hey, what are you doing?"
            korean_friendly = "Hey, what are you up to right now?"
            cultural_note = "This keeps the message casual but removes slang that may sound too rough in Korean conversation."
        elif tone == "polite":
            improved_message = "What are you doing right now?"
            korean_friendly = "What are you doing at the moment?"
            cultural_note = "This sounds more natural and respectful. Korean conversations often avoid overly direct slang."
        else:
            improved_message = "May I ask what you are doing right now?"
            korean_friendly = "May I ask what you are currently doing?"
            cultural_note = "This sounds more respectful and suitable for formal or less familiar situations."

    elif "file" in lower_text and ("fast" in lower_text or "jaldi" in lower_text or "quick" in lower_text):
        if tone == "casual":
            improved_message = "Can you send me the file soon?"
            korean_friendly = "Can you send me the file when you get a chance?"
            cultural_note = "Even in casual Korean communication, softer requests usually sound better than direct commands."
        elif tone == "polite":
            improved_message = "Could you please send me the file soon?"
            korean_friendly = "Could you please send me the file when you have a moment?"
            cultural_note = "In Korean communication, polite requests sound better than direct commands. Softening the sentence makes it more respectful."
        else:
            improved_message = "Could you please send me the file as soon as possible?"
            korean_friendly = "Could you kindly send me the file at your earliest convenience?"
            cultural_note = "Formal Korean-style professional communication usually sounds respectful, calm, and less demanding."

    elif "meet" in lower_text or "mil" in lower_text:
        if tone == "casual":
            improved_message = "Do you want to meet this week?"
            korean_friendly = "Would you like to meet sometime this week?"
            cultural_note = "This sounds clearer and more natural than a vague invitation."
        elif tone == "polite":
            improved_message = "Would you like to meet sometime this week?"
            korean_friendly = "Would it be possible for us to meet sometime this week?"
            cultural_note = "In Korean culture, being slightly more specific and polite is usually better than vague wording."
        else:
            improved_message = "Would you be available to meet at a convenient time?"
            korean_friendly = "Please let me know a convenient time for us to meet."
            cultural_note = "In professional Korean settings, formal scheduling language sounds more appropriate than casual invitations."

    elif "what are you doing" in lower_text or "kya kar raha hai" in lower_text or "kar rha hai" in lower_text:
        if tone == "casual":
            improved_message = "What are you doing right now?"
            korean_friendly = "What are you doing right now?"
            cultural_note = "This version is simple and natural for daily conversation."
        elif tone == "polite":
            improved_message = "What are you doing right now?"
            korean_friendly = "What are you doing at the moment?"
            cultural_note = "This version sounds more natural and polite. Korean-style communication often avoids overly rough wording."
        else:
            improved_message = "May I ask what you are doing right now?"
            korean_friendly = "May I ask what you are currently working on?"
            cultural_note = "Formal Korean communication often uses respectful wording, especially in workplace or senior-junior situations."

    else:
        if mode == "workplace":
            if tone == "casual":
                improved_message = text
                korean_friendly = f"A smoother workplace version would be: {text}"
                cultural_note = "Workplace communication in Korea usually sounds clearer and softer than direct speech."
            elif tone == "polite":
                improved_message = f"Could you please say: {text}"
                korean_friendly = f"I wanted to say this politely in a workplace setting: {text}"
                cultural_note = "For Korean workplace communication, polite and indirect phrasing is often preferred."
            else:
                improved_message = f"I would like to express this more professionally: {text}"
                korean_friendly = f"A more formal workplace version would be: {text}"
                cultural_note = "Formal Korean-style workplace communication values respect, clarity, and professionalism."
        elif mode == "friend":
            if tone == "casual":
                improved_message = text
                korean_friendly = f"A natural friendly version would be: {text}"
                cultural_note = "Friendly Korean conversation still tends to sound softer than rough slang."
            elif tone == "polite":
                improved_message = f"Could you say this a bit more politely: {text}"
                korean_friendly = f"A polite but friendly version would be: {text}"
                cultural_note = "With friends, you can still sound warm and respectful without being too formal."
            else:
                improved_message = f"A respectful version would be: {text}"
                korean_friendly = f"A more formal but friendly version would be: {text}"
                cultural_note = "This keeps the sentence respectful while still fitting a friendly context."
        else:
            if tone == "casual":
                improved_message = text
                korean_friendly = f"A natural version would be: {text}"
                cultural_note = "This keeps the message simple for normal conversation."
            elif tone == "polite":
                improved_message = f"Could you please say: {text}"
                korean_friendly = f"I wanted to say this politely: {text}"
                cultural_note = "For Korean communication, polite and indirect phrasing is often preferred, especially with new people or coworkers."
            else:
                improved_message = f"I would like to express this more professionally: {text}"
                korean_friendly = f"A more formal Korean-friendly version would be: {text}"
                cultural_note = "Formal Korean-style communication values respect, clarity, and professionalism."

    korean_translation = get_korean_translation(improved_message, tone, mode)
    cultural_note = context_note + " " + cultural_note

    return {
        "user_message": text,
        "mode": mode,
        "tone": tone,
        "improved_message": improved_message,
        "korean_friendly": korean_friendly,
        "korean_translation": korean_translation,
        "cultural_note": cultural_note
    }


@app.route("/", methods=["GET", "POST"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        user_text = request.form.get("message", "").strip()
        tone = request.form.get("tone", "casual")
        mode = request.form.get("mode", "casual")

        if user_text:
            result = analyze_message(user_text, tone, mode)
            history = session["chat_history"]
            history.append(result)

            # keep only last 10 chats
            if len(history) > 10:
                history = history[-10:]

            session["chat_history"] = history
            session.modified = True

    return render_template("index.html", chat_history=session.get("chat_history", []))


@app.route("/clear", methods=["POST"])
def clear_chat():
    session["chat_history"] = []
    session.modified = True
    return render_template("index.html", chat_history=[])


if __name__ == "__main__":
    import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)   