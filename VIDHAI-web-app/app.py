from flask import Flask, request, jsonify
from flask_cors import CORS
import openai, os, io, base64, re
from dotenv import load_dotenv
from gtts import gTTS

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

def detect_language(text):
    return "ml" if any('\u0D00' <= ch <= '\u0D7F' for ch in text) else "en"

@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        lang = detect_language(user_message)  # Detect Malayalam or English
        
         # === Detect greeting request ===
        if user_message == "__greeting__":
            greeting_text = "👋 ഹലോ! ഞാൻ നിങ്ങളുടെ AI സഹായിയാണ്. ഇന്ന് നിങ്ങളെ എങ്ങനെ സഹായിക്കാം?"
            # Create greeting audio
            tts = gTTS(text=greeting_text, lang="ml")
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            audio_base64 = base64.b64encode(mp3_fp.read()).decode("utf-8")
            return jsonify({"response": greeting_text, "audio": audio_base64})



        # 🧠 Ask OpenAI for a reply
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Vithai, an AI companion for Kerala farmers. "
                        "Answer clearly in the user's language (Malayalam or English) "
                        "about crops, irrigation, fertilizer, pests, diseases, and government schemes."
                    )
                },
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response.choices[0].message.content

        # 🧹 Clean text for audio (remove Markdown)
        clean_text = re.sub(r"[*#]", "", bot_reply)
        clean_text = re.sub(r"\[.*?\]\(.*?\)", "", clean_text)
        clean_text = re.sub(r"\s{2,}", " ", clean_text).strip()

        # 🔊 Convert reply to speech in the same language
        lang = "ml" if any('\u0D00' <= ch <= '\u0D7F' for ch in bot_reply) else "en"
        tts = gTTS(text=clean_text, lang=lang)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio_base64 = base64.b64encode(mp3_fp.read()).decode("utf-8")

        return jsonify({"response": bot_reply, "audio": audio_base64})
    except Exception as e:
        return jsonify({"response": f"⚠️ Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
