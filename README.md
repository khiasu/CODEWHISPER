# Code Whisper ✨

A **premium AI-powered code explanation tool** with a beautiful, modern frontend and robust Flask backend. Code Whisper provides personality-based code explanations using CodeLLaMA via Ollama, featuring world-class animations and user experience.

## 🎉 Features

### ✨ **Premium UI/UX**
- **🎨 Monochromatic Design**: Sophisticated color palette with perfect contrast
- **🌓 Dark/Light Theme Toggle**: Smooth transitions with theme persistence
- **⚡ Premium Animations**: Typing effects, button interactions, smooth transitions
- **📱 Fully Responsive**: Perfect experience on desktop, tablet, and mobile
- **🎯 Micro-interactions**: Hover effects, loading animations, state transitions

### 🤖 **AI-Powered Explanations**
- **🎭 Multiple Personalities**: Friend, Professor, Senior Dev, Babysitter modes
- **⚡ Smart Fallback System**: Intelligent responses even with memory constraints
- **🔄 Real-time Analysis**: Instant code explanations with typing effects
- **🧠 Language Detection**: Automatic detection of programming languages
- **📊 Code Structure Analysis**: Detailed insights into code patterns

### 🛠️ **Advanced Features**
- **📋 Copy to Clipboard**: One-click copying with visual feedback
- **🔊 Text-to-Speech**: Read explanations aloud with controls
- **🗑️ Clear Code Button**: Quick code clearing with animations
- **⌨️ Keyboard Shortcuts**: Ctrl+Enter to explain, Escape to stop speech
- **🎪 Loading States**: Beautiful loading animations and progress indicators

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

## Error Handling

The API provides comprehensive error handling:

- **400 Bad Request**: Invalid input (empty code, invalid mode, etc.)
- **503 Service Unavailable**: Ollama service not available
- **500 Internal Server Error**: Unexpected server errors

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

## Troubleshooting

### Common Issues

1. **"AI service is not available"**
   - Make sure Ollama is running: `ollama serve`
   - Verify CodeLLaMA is installed: `ollama list`

2. **"Could not connect to Ollama"**
   - Check if Ollama is running on the correct port (11434)
   - Verify firewall settings

3. **Slow responses**
   - CodeLLaMA model is large and may take time on first load
   - Consider adjusting `MAX_TOKENS` in configuration

### Development

For development, the backend runs in debug mode by default. You can modify the personality prompts in `config.py` to customize the explanation styles.

## Next Steps

This backend is ready for frontend integration. The next phase would be to:
1. Create the HTML/CSS/JS frontend
2. Implement the typing effect for AI responses
3. Add theme toggle and other UI features
4. Deploy the complete application

## License

This project is part of the Code Whisper application.
