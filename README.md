# Code Whisper ✨
**AI-powered code explanation tool** with a beautiful, modern frontend and robust Flask backend. Code Whisper provides personality-based code explanations using CodeLLaMA via Ollama, featuring world-class animations and user experience.


## Prerequisites

1. **Python 3.8+**
2. **Ollama** installed and running
3. **CodeLLaMA model** pulled in Ollama

### Installing Ollama and CodeLLaMA

```bash
# Install Ollama (visit https://ollama.ai for platform-specific instructions)

# Start Ollama service
ollama serve

# Pull CodeLLaMA model
ollama pull codellama
```

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment** (optional)
   ```bash
   # Copy and modify .env file if needed
   cp .env .env.local
   ```

3. **Start the Application**
   ```bash
   python app.py
   ```

4. **Open in Browser**
   ```
   http://localhost:5000
   ```

5. **Test Everything**
   ```bash
   # Test backend API
   python test_backend.py
   
   # Test frontend (open in browser)
   http://localhost:5000/test_frontend.html
   ```

## API Endpoints

### POST `/explain`
Explain code using different personality modes.

**Request:**
```json
{
  "code": "def hello():\n    print('Hello, World!')",
  "mode": "friend"
}
```

**Response:**
```json
{
  "success": true,
  "mode": "friend",
  "explanation": "Hey! Let me break this down for you...",
  "code_length": 35
}
```

**Available Modes:**
- `friend`: Casual, encouraging explanations
- `professor`: Academic, detailed explanations  
- `senior`: Critical, blunt feedback
- `babysitter`: Beginner-friendly, simple explanations

### GET `/modes`
Get available explanation modes and descriptions.

### GET `/health`
Health check endpoint.

## Configuration

Environment variables can be set in `.env` file:

```env
# Flask Configuration
DEBUG=True
HOST=0.0.0.0
PORT=5000

# Ollama Configuration
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
MODEL_NAME=codellama

# AI Model Parameters
TEMPERATURE=0.7
TOP_P=0.9
MAX_TOKENS=1000
REQUEST_TIMEOUT=30

# Validation Limits
MAX_CODE_LENGTH=10000
```

## 📁 Project Structure

```
CODE WHISPER/
├── 🐍 Backend
│   ├── app.py                 # Main Flask application
│   ├── config.py             # Configuration management
│   ├── requirements.txt      # Python dependencies
│   ├── .env                  # Environment variables
│   ├── test_backend.py       # Comprehensive test suite
│   └── services/
│       ├── __init__.py
│       └── ollama_service.py # Ollama integration service
│
├── 🎨 Frontend
│   ├── index.html            # Main application interface
│   ├── styles.css            # Premium CSS with animations
│   ├── script.js             # Interactive JavaScript
│   └── test_frontend.html    # Frontend testing page
│
├── 🚀 Deployment
│   ├── start.py              # Startup script with health checks
│   ├── start.bat             # Windows batch starter
│   └── README.md             # This documentation
```


## Testing

Run the test suite to verify everything works:

```bash
python test_backend.py
```

The test suite checks:
- Health endpoint
- Modes endpoint  
- Explain endpoint with all modes
- Error handling scenarios
