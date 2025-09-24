import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for Code Whisper backend"""
    
    # Flask configuration
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Ollama configuration
    OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'localhost')
    OLLAMA_PORT = int(os.getenv('OLLAMA_PORT', 11434))
    OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"
    MODEL_NAME = os.getenv('MODEL_NAME', 'qwen2.5-coder:7b')
    KEEP_ALIVE = os.getenv('KEEP_ALIVE', '5m')  # keep model loaded between requests to avoid reloads
    
    # AI model parameters
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.7))
    TOP_P = float(os.getenv('TOP_P', 0.9))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 100))  # Reduced for memory efficiency
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 60))  # Non-stream requests timeout (seconds)
    STREAM_TIMEOUT = int(os.getenv('STREAM_TIMEOUT', 600))   # Stream read timeout (seconds)
    FALLBACK_DELAY_SECONDS = int(os.getenv('FALLBACK_DELAY_SECONDS', 0))  # Wait before using fallback
    
    # Prefer local model by default; fallback only on failure
    USE_FALLBACK_FIRST = os.getenv('USE_FALLBACK_FIRST', 'False').lower() == 'true'
    
    # Memory optimization settings
    OLLAMA_NUM_CTX = int(os.getenv('OLLAMA_NUM_CTX', 2048))  # Context window size
    OLLAMA_NUM_GPU = int(os.getenv('OLLAMA_NUM_GPU', 0))  # Use CPU by default
    
    # Validation limits
    MAX_CODE_LENGTH = int(os.getenv('MAX_CODE_LENGTH', 10000))  # 10KB limit
    MIN_CODE_LENGTH = int(os.getenv('MIN_CODE_LENGTH', 1))

# Mode prompts - separated for better maintainability
MODE_PROMPTS = {
    "friend": (
        "You are a supportive peer. Give a concise, positive explanation in 5-8 bullet points. "
        "Focus on what the code does and how, avoid heavy theory, end with one practical tip."
    ),
    "professor": (
        "You are a CS professor. Provide a structured explanation with sections: Purpose, Flow, Key Concepts, "
        "Complexity, Edge Cases. Be precise and technical; keep each section brief (2-3 lines)."
    ),
    "babysitter": (
        "You teach a beginner. Explain step-by-step using very simple words and tiny examples. "
        "Avoid jargon; define any necessary term in one short line."
    ),
    "review": (
        "You are a strict code reviewer. Output ONLY critical feedback and actionable improvements. "
        "No restating the code. Sections: Issues, Risks, Refactor Suggestions. Be direct and terse."
    ),
}