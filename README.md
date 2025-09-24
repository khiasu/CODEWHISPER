# Code Whisper

A premium AI-powered code explanation tool with a modern frontend and robust Flask backend. Code Whisper provides personality-based code explanations using local LLMs via Ollama, with smooth animations and a great user experience.

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

### Installing Ollama and AI Models

```bash
# Install Ollama (visit https://ollama.ai for platform-specific instructions)

# Start Ollama service
ollama serve

# Pull a smaller, faster model (recommended on low-RAM machines)
ollama pull qwen2.5-coder:3b

# Or use the larger 7B model if you have enough RAM/VRAM
ollama pull qwen2.5-coder:7b
```

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment** (optional)
   ```bash
   # Edit .env to tune performance
   # Example for faster responses on limited hardware:
   MODEL_NAME=qwen2.5-coder:3b
   MAX_TOKENS=128
   ```

3. **Start the Application**
   ```bash
   py -3.13 app.py
   # or simply: python app.py
   ```

4. **Open in Browser**
   ```
   http://localhost:5000
   ```

5. **Test Everything**
   ```bash
   # Test backend API
   py -3.13 tests\test_backend.py
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
MODEL_NAME=qwen2.5-coder:3b
KEEP_ALIVE=5m

# AI Model Parameters
TEMPERATURE=0.7
TOP_P=0.9
MAX_TOKENS=128

# Timeouts and fallback behavior
REQUEST_TIMEOUT=1200        # Non-stream requests timeout (seconds)
STREAM_TIMEOUT=1800         # Stream read timeout (seconds)
FALLBACK_DELAY_SECONDS=600  # Wait before switching to fallback (seconds)

# Validation Limits
MAX_CODE_LENGTH=10000
```

## 📁 Project Structure

```
CODE WHISPER/
├── app.py                     # Entry point (Flask), serves frontend from /frontend
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (gitignored)
├── backend/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   └── services/
│       ├── __init__.py
│       └── ollama_service.py  # Ollama integration service
│
├── frontend/
│   ├── index.html             # Main application interface
│   ├── styles.css             # Premium CSS with animations
│   └── script.js              # Interactive JavaScript
│
└── tests/
    └── test_backend.py        # Backend API tests
```

## Error Handling

The API provides comprehensive error handling:

- **400 Bad Request**: Invalid input (empty code, invalid mode, etc.)
- **503 Service Unavailable**: Ollama service not available
- **500 Internal Server Error**: Unexpected server errors

## Testing

Run the test suite to verify everything works:

```bash
py -3.13 test_backend.py
```

The test suite checks:
- Health endpoint
- Modes endpoint  
- Explain endpoint with all modes
- Error handling scenarios

## Troubleshooting

### Common Issues

1. "AI service is not available"
   - Make sure Ollama is running: `ollama serve`
   - Verify model is installed: `ollama list`

2. **"Could not connect to Ollama"**
   - Check if Ollama is running on the correct port (11434)
   - Verify firewall settings

3. **Slow responses**
   - CodeLLaMA model is large and may take time on first load
   - Consider adjusting `MAX_TOKENS` in configuration

### Development

For development, the backend runs in debug mode by default. You can modify the personality prompts in `backend/config.py` to customize the explanation styles.

## 🎯 Tech Fest Demo Features

This project showcases:
- **AI Integration**: Local LLM integration with Ollama
- **Modern Web Development**: Flask backend + Vanilla JS frontend
- **API Design**: RESTful endpoints with proper error handling
- **User Experience**: Multiple AI personalities for different explanation styles
- **Real-time Processing**: Streaming responses for better UX

## License

This project is part of the Code Whisper application.
