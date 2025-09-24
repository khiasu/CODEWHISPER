from flask import Flask, request, jsonify, render_template, send_from_directory, Response, stream_template
from flask_cors import CORS
import logging
import json
import time
from backend.config import Config, MODE_PROMPTS
from backend.services.ollama_service import OllamaService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='frontend', template_folder='frontend')
CORS(app)  # Enable CORS for frontend integration

# Initialize Ollama service once per process
ollama_service = OllamaService()

@app.route('/')
def index():
    """Serve the main frontend page"""
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory('frontend', filename)

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
        
        allowed_modes = set(MODE_PROMPTS.keys()) | {"senior"}
        if mode not in allowed_modes:
            return jsonify({
                "error": f"Invalid mode. Supported modes: {sorted(list(allowed_modes))}"
            }), 400
        
        # Check if Ollama is available
        if not ollama_service.is_available():
            return jsonify({
                "error": "AI service is not available. Please make sure Ollama is running with the configured model."
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


@app.route('/explain-stream', methods=['POST'])
def explain_code_stream():
    """
    Stream code explanation in real-time using Server-Sent Events
    """
    # Validate request BEFORE creating the generator to avoid context loss
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json(silent=True) or {}

    if 'code' not in data or 'mode' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    code = (data.get('code') or '').strip()
    mode = str(data.get('mode') or '').lower()

    if not code:
        return jsonify({"error": "Code cannot be empty"}), 400

    if len(code) > Config.MAX_CODE_LENGTH:
        return jsonify({"error": f"Code too long. Maximum length: {Config.MAX_CODE_LENGTH} characters"}), 400

    allowed_modes = set(MODE_PROMPTS.keys()) | {"senior"}
    if mode not in allowed_modes:
        return jsonify({"error": f"Invalid mode. Supported modes: {sorted(list(allowed_modes))}"}), 400

    def generate_stream(validated_code: str, validated_mode: str):
        try:
            # Send start event
            yield f"data: {json.dumps({'type': 'start', 'mode': validated_mode, 'model': Config.MODEL_NAME})}\n\n"

            # Get streaming explanation
            for chunk in ollama_service.get_explanation_stream(validated_code, validated_mode):
                yield f"data: {json.dumps(chunk)}\n\n"
                # no artificial delay; stream as fast as available

            # Send completion event
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"

        except Exception as e:
            logger.error(f"Error in explain_code_stream: {str(e)}")
            yield f"data: {json.dumps({'type': 'error', 'message': 'Internal server error'})}\n\n"

    return Response(
        generate_stream(code, mode),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Cache-Control'
        }
    )


@app.route('/modes', methods=['GET'])
def get_available_modes():
    """Get list of available explanation modes"""
    modes = sorted(list(set(MODE_PROMPTS.keys()) | {"senior"}))
    return jsonify({
        "modes": modes,
        "descriptions": {
            "friend": "Casual, friendly explanations",
            "professor": "Academic, detailed explanations", 
            "senior": "Critical, blunt feedback (alias of 'review')",
            "babysitter": "Beginner-friendly, simple explanations",
            "review": "Strict code review with actionable improvements"
        }
    })

@app.route('/config', methods=['GET'])
def get_config():
    """Expose current backend configuration (safe subset)"""
    return jsonify({
        "model": Config.MODEL_NAME,
        "ollama_host": Config.OLLAMA_HOST,
        "ollama_port": Config.OLLAMA_PORT,
        "keep_alive": getattr(Config, 'KEEP_ALIVE', None),
        "use_fallback_first": Config.USE_FALLBACK_FIRST,
        "max_tokens": Config.MAX_TOKENS,
        "temperature": Config.TEMPERATURE,
        "top_p": Config.TOP_P
    })

if __name__ == '__main__':
    print("🚀 Starting Code Whisper Backend...")
    print(f"📡 Using model: {Config.MODEL_NAME}")
    print(f"🔗 Backend will be available at http://{Config.HOST}:{Config.PORT}")
    
    # Check Ollama availability on startup
    if ollama_service.is_available():
        print("✅ Ollama service is available")
    else:
        print("⚠️  Warning: Ollama service is not available")
        print("   Make sure to run: ollama serve")
        print(f"   And pull the model: ollama pull {Config.MODEL_NAME}")
    
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)