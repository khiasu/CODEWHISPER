# Code Whisper: AI-Powered Code Explanation Tool

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.13+-blue.svg" alt="Python 3.13+">
  <img src="https://img.shields.io/badge/Flask-2.3.3-green.svg" alt="Flask 2.3.3">
  <img src="https://img.shields.io/badge/Qwen--2.5--Coder-14B-orange" alt="Qwen2.5-Coder 14B">
  <img src="https://img.shields.io/badge/license-MIT-brightgreen" alt="MIT License">
</div>

## 🌟 Table of Contents
- [🚀 Overview](#-overview)
- [✨ Features](#-features)
- [🛠️ System Requirements](#%EF%B8%8F-system-requirements)
- [🚀 Quick Start](#-quick-start)
- [🔧 Installation Guide](#-installation-guide)
- [⚙️ Configuration](#%EF%B8%8F-configuration)
- [🧠 AI Model Details](#-ai-model-details)
- [📚 API Documentation](#-api-documentation)
- [🧪 Testing](#-testing)
- [🚀 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

## 🚀 Overview

Code Whisper is an advanced AI-powered code explanation tool that helps developers understand complex codebases through interactive, personality-driven explanations. Built with Python, Flask, and powered by the `qwen2.5-coder:14b` model, it offers high-quality, context-aware code analysis with a beautiful, responsive interface.

## ✨ Features

### 🎨 Premium UI/UX
- **Modern, Clean Interface**: Intuitive design with a focus on readability
- **🌓 Dark/Light Theme**: Smooth transitions between themes with system preference detection
- **Responsive Design**: Perfectly adapts to desktop, tablet, and mobile devices
- **Micro-interactions**: Subtle animations and transitions for a polished feel
- **Keyboard Shortcuts**: Quick actions for power users

### 🤖 AI-Powered Explanations
- **Multiple AI Personalities**:
  - **👥 Friend Mode**: Casual, conversational explanations
  - **🎓 Professor Mode**: Detailed, academic-style breakdowns
  - **👨‍💻 Senior Dev Mode**: Professional, best-practices focused
  - **🧸 Babysitter Mode**: Extra patient, beginner-friendly explanations
- **Real-time Analysis**: Get explanations as you type
- **Code Structure Analysis**: Understand relationships between code components
- **Context-Aware**: Maintains conversation context for better explanations

### 🛠️ Advanced Features
- **📋 Copy to Clipboard**: One-click copying of explanations
- **🔊 Text-to-Speech**: Listen to explanations with adjustable settings
- **📁 Code History**: View and restore previous explanations
- **🔍 Syntax Highlighting**: For better code readability
- **📊 Performance Metrics**: Track response times and token usage

## 🛠️ System Requirements

### Minimum Requirements
- **CPU**: 4+ cores (Intel i5/Ryzen 5 or better)
- **RAM**: 16GB (32GB recommended)
- **GPU**: NVIDIA with CUDA support (RTX 3080 or better with 10GB+ VRAM)
- **Storage**: 20GB free space (for models and dependencies)
- **OS**: Windows 10/11, macOS 12+, or Linux (Ubuntu 20.04+)

### Software Dependencies
- **Python 3.13**
- **Ollama** (latest stable release)
- **Node.js 18+** (for frontend tooling)
- **Git** (for version control)
- **CUDA Toolkit 12.1+** (for GPU acceleration)

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/khiasu/CODEWHISPER.git
   cd CODEWHISPER
   ```

2. **Set up and activate Python virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Unix/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Ollama and download the model**
   ```bash
   # Start Ollama service (in a separate terminal)
   ollama serve
   
   # In another terminal, pull the model
   ollama pull qwen2.5-coder:14b
   ```

5. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   # Flask Configuration
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   
   # Ollama Configuration
   OLLAMA_BASE_URL=http://localhost:11434
   DEFAULT_MODEL=qwen2.5-coder:14b
   KEEP_ALIVE=5m
   
   # AI Parameters
   TEMPERATURE=0.7
   MAX_TOKENS=2048
   TOP_P=0.9
   
   # Performance Settings
   WORKERS=4
   TIMEOUT=120
   ```

6. **Start the application**
   ```bash
   flask run --host=0.0.0.0 --port=5000
   ```
   Open `http://localhost:5000` in your browser

## 🔧 Installation Guide

### Detailed Setup Instructions

#### 1. Python Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Upgrade pip and install wheel
python -m pip install --upgrade pip wheel
```

#### 2. Ollama Installation
```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows (PowerShell as Administrator)
winget install ollama.ollama

# macOS (using Homebrew)
brew install ollama
```

#### 3. Frontend Dependencies
```bash
# Install Node.js dependencies (if any)
npm install

# Build frontend assets (if using a build system)
npm run build
```

#### 4. Verify Installation
```bash
# Check Python version
python --version  # Should be 3.13.x

# Check Ollama
ollama --version
ollama list  # Should show qwen2.5-coder:14b

# Run tests
pytest tests/
```

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_APP` | `app.py` | Entry point for Flask application |
| `FLASK_ENV` | `development` | Environment (development/production) |
| `SECRET_KEY` | - | Secret key for session management |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `DEFAULT_MODEL` | `qwen2.5-coder:14b` | Default AI model to use |
| `TEMPERATURE` | `0.7` | Controls randomness (0-1) |
| `MAX_TOKENS` | `2048` | Maximum tokens per response |
| `TOP_P` | `0.9` | Nucleus sampling parameter |
| `KEEP_ALIVE` | `5m` | Keep model loaded in memory |
| `WORKERS` | `4` | Number of worker processes |
| `TIMEOUT` | `120` | Request timeout in seconds |

### Model Parameters

| Parameter | Recommended Value | Description |
|-----------|------------------|-------------|
| `temperature` | 0.7 | Controls randomness (0-1) |
| `top_p` | 0.9 | Nucleus sampling parameter |
| `top_k` | 40 | Limits token selection to top k |
| `repeat_penalty` | 1.1 | Penalizes repetition in responses |
| `num_ctx` | 4096 | Context window size |

## 🧠 AI Model Details

### qwen2.5-coder:14b Specifications

| Specification | Details |
|--------------|---------|
| **Model Name** | qwen2.5-coder:14b |
| **Parameters** | 14 billion |
| **Context Window** | 8,192 tokens |
| **Training Data** | Up to Q2 2024 |
| **Languages** | Python, JavaScript, Java, C++, and 20+ more |
| **Model Size** | ~8.5GB (quantized) |
| **VRAM Usage** | ~10-12GB (FP16) |
| **Inference Speed** | ~15-25 tokens/sec (RTX 3080) |

### Performance Optimization

1. **Quantization**: Use 4-bit or 8-bit quantization for lower VRAM usage
2. **Context Management**: Limit context size for faster responses
3. **Batch Processing**: Process multiple requests in parallel
4. **Caching**: Implement response caching for common queries

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api/v1
```

### Authentication
```http
GET /api/v1/auth/token
```

### Endpoints

#### 1. Explain Code
```http
POST /api/v1/explain
```

**Request Body:**
```json
{
  "code": "def hello():\n    print('Hello, World!')",
  "mode": "professor",
  "language": "python",
  "temperature": 0.7,
  "max_tokens": 1024
}
```

**Response:**
```json
{
  "success": true,
  "mode": "professor",
  "explanation": "Let me explain this Python function...",
  "tokens_used": 245,
  "processing_time": 1.23,
  "model": "qwen2.5-coder:14b",
  "language": "python"
}
```

#### 2. Get Available Modes
```http
GET /api/v1/modes
```

**Response:**
```json
{
  "modes": [
    {
      "id": "professor",
      "name": "Professor",
      "description": "Detailed, academic-style explanations",
      "icon": "🎓"
    },
    {
      "id": "friend",
      "name": "Friend",
      "description": "Casual, conversational explanations",
      "icon": "👥"
    }
  ]
}
```

#### 3. Health Check
```http
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "model": "qwen2.5-coder:14b",
  "uptime": "2h 15m 30s",
  "requests_processed": 42
}
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_backend.py -v

# Run with coverage report
coverage run -m pytest
coverage report
```

### Test Coverage
```bash
# Generate HTML coverage report
coverage html
# Open in browser
open htmlcov/index.html
```

### Linting
```bash
# Run flake8
flake8 .

# Auto-format code
black .

# Sort imports
isort .
```

## 🚀 Deployment

### Production Setup with Gunicorn and Nginx

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Create Gunicorn Config** (`gunicorn_config.py`):
   ```python
   workers = 4
   worker_class = 'gthread'
   threads = 2
   bind = '0.0.0.0:8000'
   timeout = 120
   keepalive = 5
   errorlog = '-'
   accesslog = '-'
   ```

3. **Systemd Service** (`/etc/systemd/system/codewhisper.service`):
   ```ini
   [Unit]
   Description=Code Whisper
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/code-whisper
   Environment="PATH=/path/to/venv/bin"
   ExecStart=/path/to/venv/bin/gunicorn -c gunicorn_config.py app:app
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

4. **Nginx Configuration** (`/etc/nginx/sites-available/codewhisper`):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
       
       location /static {
           alias /path/to/code-whisper/static;
       }
   }
   ```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Setup
```bash
# Install pre-commit hooks
pre-commit install

# Run pre-commit on all files
pre-commit run --all-files
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- The Ollama team for their amazing local LLM framework
- Qwen for the powerful code model
- The open-source community for their contributions
- All contributors who helped improve this project
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
=======
>>>>>>> 55549cc9e7230cf04d5d15895c9255bb26224068
