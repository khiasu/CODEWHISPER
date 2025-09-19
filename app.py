from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import logging
import os
from config import Config, MODE_PROMPTS
from services.ollama_service import ollama_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)  # Enable CORS for frontend integration

@app.route('/')
def index():
    """Serve the main frontend page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory('.', filename)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Code Whisper backend is running"})

@app.route('/explain', methods=['POST'])
def explain_code():
    """
    Main endpoint to explain code using different personality modes
    
    Expected JSON payload:
    {
        "code": "your code here",
        "mode": "friend|professor|senior|babysitter"
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        
        # Validate required fields
        if 'code' not in data or 'mode' not in data:
            return jsonify({"error": "Missing required fields: 'code' and 'mode'"}), 400
        
        code = data['code'].strip()
        mode = data['mode'].lower()
        
        # Validate inputs
        if not code:
            return jsonify({"error": "Code cannot be empty"}), 400
        
        if len(code) > Config.MAX_CODE_LENGTH:
            return jsonify({"error": f"Code too long. Maximum length: {Config.MAX_CODE_LENGTH} characters"}), 400
        
        if mode not in MODE_PROMPTS:
            return jsonify({
                "error": f"Invalid mode. Supported modes: {list(MODE_PROMPTS.keys())}"
            }), 400
        
        # Check if Ollama is available
        if not ollama_service.is_available():
            return jsonify({
                "error": "AI service is not available. Please make sure Ollama is running with CodeLLaMA model."
            }), 503
        
        # Send request to Ollama
        logger.info(f"Sending request to Ollama with mode: {mode}")
        result = ollama_service.get_explanation(code, mode)
        
        if not result.get("success", False):
            return jsonify({"error": result.get("error", "Failed to get explanation from AI model")}), 500
        
        # Return successful response
        return jsonify({
            "success": True,
            "mode": mode,
            "explanation": result.get("explanation"),
            "model": result.get("model", "unknown"),
            "code_length": len(code)
        })
        
    except Exception as e:
        logger.error(f"Error in explain_code: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/modes', methods=['GET'])
def get_available_modes():
    """Get list of available explanation modes"""
    return jsonify({
        "modes": list(MODE_PROMPTS.keys()),
        "descriptions": {
            "friend": "Casual, friendly explanations",
            "professor": "Academic, detailed explanations", 
            "senior": "Critical, blunt feedback",
            "babysitter": "Beginner-friendly, simple explanations"
        }
    })

if __name__ == '__main__':
    print("🚀 Starting Code Whisper Backend...")
    print("📡 Make sure Ollama is running with CodeLLaMA model")
    print(f"🔗 Backend will be available at http://{Config.HOST}:{Config.PORT}")
    
    # Check Ollama availability on startup
    if ollama_service.is_available():
        print("✅ Ollama service is available")
    else:
        print("⚠️  Warning: Ollama service is not available")
        print("   Make sure to run: ollama serve")
        print("   And pull the model: ollama pull codellama")
    
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
