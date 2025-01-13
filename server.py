# Standard library imports
import json
# Third-party imports
from dotenv import dotenv_values
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import google.generativeai as genai

# Local imports
config = dotenv_values(".env")

GEMINI_API_KEY = config.get('GEMINI_API_KEY')
MODEL_NAME = config.get('MODEL_NAME')


# Initialize Flask application
app = Flask(__name__)
cors = CORS(app, resources={
    r"/*": {  # Apply to all routes
        "origins": "*",  # Allow your frontend origin
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allow these HTTP methods
        "allow_headers": ["Content-Type", "Authorization", "baggage"],  # Explicitly allow the 'baggage' header
        "expose_headers": ["Content-Range", "X-Content-Range"],
        "supports_credentials": True  # Enable if you need to send cookies
    }
})

# Configure Gemini AI with API key
genai.configure(api_key=GEMINI_API_KEY)

# Create instance of the generative model
model = genai.GenerativeModel(MODEL_NAME)

@app.route('/', methods=['POST'])
@cross_origin(supports_credentials=True)
def index():
    """
    Main endpoint that handles POST requests for text generation
    Accepts JSON with 'prompt' and optional 'data' fields
    """
    # Parse incoming JSON data
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Extract prompt and text from the request
    prompt = data.get('prompt', '')
    text = data.get('data', '')
    
    # Validate prompt
    if not prompt or not isinstance(prompt, str):
        return jsonify({"error": "Invalid or missing 'prompt' field"}), 400
    
    # Construct the final prompt based on whether additional text is provided
    llm_response_formatting = "Please return only the final response and no additional context."
    if text:
        final_prompt = f"{prompt} to the following text: {text}. {llm_response_formatting}"
    else:
        final_prompt = f"Generated new text based on prompt: Prompt: {prompt}. {llm_response_formatting}"
    
    try:
        # Generate content using the Gemini model
        result = model.generate_content(final_prompt)
        # Clean up response by removing asterisks and handle empty results
        response = result.text.replace("*", "") if result and result.text else ""

        # Return successful response
        return jsonify({"result": response}), 200
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except genai.types.generation_types.BlockedPromptException:
        return jsonify({"error": "Content blocked by safety filters"}), 422
    except ConnectionError:
        return jsonify({"error": "Failed to connect to AI service"}), 503
    except ValueError as e:
        return jsonify({"error": f"Invalid value: {str(e)}"}), 400


@app.route('/health/', methods=['GET'])
@cross_origin(supports_credentials=True)
def health_check():
    """
    Health check endpoint that returns a simple message
    """
    return jsonify({"response": "OK"}), 200


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8080)  # Run on all network interfaces on port 8080
