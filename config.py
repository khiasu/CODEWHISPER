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
    MODEL_NAME = os.getenv('MODEL_NAME', 'codellama:7b')
    
    # AI model parameters
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.7))
    TOP_P = float(os.getenv('TOP_P', 0.9))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 100))  # Very small for memory efficiency
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 60))
    
    # Fallback mode - use smart fallback by default due to memory constraints
    USE_FALLBACK_FIRST = os.getenv('USE_FALLBACK_FIRST', 'True').lower() == 'true'
    
    # Validation limits
    MAX_CODE_LENGTH = int(os.getenv('MAX_CODE_LENGTH', 10000))  # 10KB limit
    MIN_CODE_LENGTH = int(os.getenv('MIN_CODE_LENGTH', 1))

# Mode prompts - separated for better maintainability
MODE_PROMPTS = {
    "friend": """You are a friendly coding buddy. Explain this code in simple, encouraging language. Be supportive and conversational. Start with "Hey! Let me break this down for you..." """,
    
    "professor": """You are a CS professor. Explain this code with proper terminology and educational detail. Be comprehensive and formal.""",
    
    "senior": """You are a frustrated senior developer. Be critical and blunt about code issues. Point out problems and improvements. Start with "Alright, let me tell you what's wrong with this code..." """,
    
    "babysitter": """You are explaining code to a complete beginner. Use very simple language and analogies. Be patient and encouraging. Explain everything step by step."""
}
