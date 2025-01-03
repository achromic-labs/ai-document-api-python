from flask import Flask
import google.generativeai as genai
from constants import GEMINI_API_KEY, MODEL_NAME


app = Flask(__name__)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)


@app.route('/')
def index():
    response = model.generate_content("How does RLHF work?")
    return response.text


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8080)
