from flask import Flask
import google.generativeai as genai
from constants import GEMINI_API_KEY, MODEL_NAME  # Import API key and model name from constants
from flask import request, jsonify

# Initialize Flask application
app = Flask(__name__)

# Configure Gemini AI with API key
genai.configure(api_key=GEMINI_API_KEY)

# Create instance of the generative model
model = genai.GenerativeModel(MODEL_NAME)

@app.route('/', methods=['POST'])
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

    try:
        # Construct the final prompt based on whether additional text is provided
        llm_response_formatting = "Please return only the final response and no additional context."
        if text:
            final_prompt = f"{prompt} to the following text: {text}. {llm_response_formatting}"
        else:
            final_prompt = f"Generated new text based on prompt: Prompt: {prompt}. {llm_response_formatting}"

        # Generate content using the Gemini model
        result = model.generate_content(final_prompt)
        # Clean up response by removing asterisks and handle empty results
        response = result.text.replace("*", "") if result and result.text else ""

        # Return successful response
        return jsonify({
            "result": response
        }), 200
    except Exception as e:
        # Return error response if something goes wrong
        return jsonify({
            "error": str(e)
        }), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8080)  # Run on all network interfaces on port 8080
