import json
from dotenv import dotenv_values
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate


config = dotenv_values(".env")


GEMINI_API_KEY = config.get('GEMINI_API_KEY')
MODEL_NAME = config.get('MODEL_NAME')


app = Flask(__name__)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "baggage"],
        "expose_headers": ["Content-Range", "X-Content-Range"],
        "supports_credentials": True
    }
})

# Initialize LangChain Gemini model
llm = GoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)

# prompt with text that needs to be replaced
text_prompt = PromptTemplate(
    input_variables=["prompt", "text"],
    template="{prompt} to the following text: {text}. Please return only the final response and no additional context."
)

# single prompt
simple_prompt = PromptTemplate(
    input_variables=["prompt"],
    template="Generated new text based on prompt: Prompt: {prompt}. Please return only the final response and no additional context."
)

@app.route('/', methods=['POST'])
@cross_origin(supports_credentials=True)
def index():
    """
    Main endpoint that handles POST requests for text generation
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    prompt = data.get('prompt', '')
    text = data.get('data', '')
    
    if not prompt or not isinstance(prompt, str):
        return jsonify({"error": "Invalid or missing 'prompt' field"}), 400
    
    try:
        if text:
            final_prompt = text_prompt.format(prompt=prompt, text=text)
        else:
            final_prompt = simple_prompt.format(prompt=prompt)
        
        response = llm.invoke(final_prompt)
        
        return jsonify({"result": response}), 200
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/health/', methods=['GET'])
@cross_origin(supports_credentials=True)
def health_check():
    """
    Health check endpoint that returns a simple message
    """
    return jsonify({"response": "OK"}), 200

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8080)
