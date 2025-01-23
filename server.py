import json
from dotenv import dotenv_values
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import OpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate


config = dotenv_values(".env")

# API Keys
GEMINI_API_KEY = config.get('GEMINI_API_KEY', '')
OPENAI_API_KEY = config.get('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = config.get('ANTHROPIC_API_KEY', '')

# Model names
GEMINI_MODEL = config.get('GEMINI_MODEL', 'gemini-1.5-flash')
OPENAI_MODEL = config.get('OPENAI_MODEL', 'gpt-3.5-turbo')
CLAUDE_MODEL = config.get('CLAUDE_MODEL', 'claude-2')

# Initialize models
models = {
    'gemini': GoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GEMINI_API_KEY,
        temperature=0.7
    ),
    'openai': OpenAI(
        model_name=OPENAI_MODEL,
        openai_api_key=OPENAI_API_KEY,
        temperature=0.7
    ),
    'claude': ChatAnthropic(
        model=CLAUDE_MODEL,
        anthropic_api_key=ANTHROPIC_API_KEY,
        temperature=0.7
    )
}

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


text_prompt = PromptTemplate(
    input_variables=["prompt", "text"],
    template="{prompt} to the following text: {text}. Please return only the final response and no additional context."
)

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
    model_name = data.get('model', 'gemini').lower()  # Default to Gemini
    
    if not prompt or not isinstance(prompt, str):
        return jsonify({"error": "Invalid or missing 'prompt' field"}), 400
    
    if model_name not in models:
        return jsonify({"error": f"Invalid model. Choose from: {', '.join(models.keys())}"}), 400
    
    try:
        if text:
            final_prompt = text_prompt.format(prompt=prompt, text=text)
        else:
            final_prompt = simple_prompt.format(prompt=prompt)
        
        llm = models[model_name]
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
