# 🚀 CODEWHISPER - AI-Powered Code Explanation Tool

A premium AI-powered code explanation tool with a modern frontend and robust Flask backend. CODEWHISPER provides personality-based code explanations using local LLMs via Ollama, with smooth animations and a great user experience.

![CODEWHISPER Demo](https://img.shields.io/badge/Status-Production_Ready-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-2.3.3-lightgrey) ![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-orange)

## 🎉 Features

### ✨ *Premium UI/UX*
- *🎨 Modern Design*: Clean, professional interface with perfect typography
- *🌓 Dark/Light Theme Toggle*: Smooth transitions with theme persistence
- *⚡ Premium Animations*: Typing effects, button interactions, smooth transitions
- *📱 Fully Responsive*: Perfect experience on desktop, tablet, and mobile
- *🎯 Micro-interactions*: Hover effects, loading animations, state transitions

### 🤖 *AI-Powered Explanations*
- *🎭 Multiple Personalities*: Friend, Professor, Senior Dev, Babysitter modes
- *⚡ Smart Fallback System*: Intelligent responses even with memory constraints
- *🔄 Real-time Analysis*: Instant code explanations with typing effects
- *🧠 Language Detection*: Automatic detection of programming languages
- *📊 Code Structure Analysis*: Detailed insights into code patterns

### 🛠 *Advanced Features*
- *📋 Copy to Clipboard*: One-click copying with visual feedback
- *🔊 Text-to-Speech*: Read explanations aloud with controls
- *🗑 Clear Code Button*: Quick code clearing with animations
- *⌨ Keyboard Shortcuts*: Ctrl+Enter to explain, Escape to stop speech
- *🎪 Loading States*: Beautiful loading animations and progress indicators

## ⚡ Quick Setup (5 Minutes)

### *Option 1: Automated Setup (Recommended)*
bash
# Clone the repository
git clone <repository-url>
cd CODEWHISPER-main

# Run the automated setup script
./setup.bat    # Windows
./setup.sh     # Linux/Mac

# Start the application
./start.bat    # Windows
./start.sh     # Linux/Mac


### *Option 2: Manual Setup*
bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Start Ollama service
ollama serve &

# 3. Pull the optimized model
ollama pull qwen2.5-coder:7b

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Start CODEWHISPER
python app.py


### *Open in Browser*: http://localhost:5000

## 📋 Prerequisites

- *Python 3.8+* ✅
- *Ollama* (for AI model inference) ✅
- *RTX 4050 GPU* (6GB VRAM) - Recommended for optimal performance ✅
- *16GB RAM* - Minimum requirement ✅

### Optimized Model Configuration
bash
# Current configuration (14B model - may have VRAM issues on RTX 4050)
MODEL_NAME=qwen2.5-coder:14b

# Alternative models
ollama pull qwen2.5-coder:7b   # Recommended for RTX 4050 (6GB VRAM)
ollama pull qwen2.5-coder:3b   # Faster, less capable
ollama pull codellama:7b-code  # Alternative code specialist


## ⚠ *Important: RTX 4050 VRAM Limitations*

*Your RTX 4050 has 6GB VRAM, but the 14B model typically requires 8-12GB VRAM.*

### *What to Expect:*
- ✅ *14B Model*: Better code explanations, more detailed analysis
- ⚠ *Potential Issues*: May run slowly or fail due to VRAM limitations
- 🔄 *Automatic Fallback*: App will switch to 7B model if 14B fails
- 💡 *Recommendation*: Consider using 7B model for best performance

### *Quick Model Switcher:*
bash
# Switch to 7B model (recommended for your hardware)
./switch_model.bat    # Windows
./switch_model.sh     # Linux/Mac


## 🎯 Performance Optimization

Your setup is optimized for *Intel Core i5 13420H + RTX 4050 6GB VRAM + 16GB RAM*:

### *With 14B Model (Current Config):*
- *Response Time*: 4-8 seconds (slower due to VRAM constraints)
- *Memory Usage*: ~8-12GB VRAM (may exceed your 6GB limit)
- *Throughput*: 10-20 tokens/second
- *Code Quality*: Excellent, more detailed explanations

### *With 7B Model (Recommended):*
- *Response Time*: 2-4 seconds (optimal performance)
- *Memory Usage*: ~4.5GB VRAM (fits perfectly in RTX 4050)
- *Throughput*: 15-25 tokens/second
- *Code Quality*: Very good for all programming languages

### *GPU Optimization*
bash
# Set these environment variables before starting
export CUDA_VISIBLE_DEVICES=0
export OLLAMA_FLASH_ATTENTION=1
export OLLAMA_KV_CACHE_TYPE="q8_0"
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_GPU_LAYERS=35


## 🚀 Usage Guide

### *Basic Usage*
1. *Open*: http://localhost:5000
2. *Paste Code*: Enter your code in the text area
3. *Select Mode*:
   - friend: Casual, friendly explanations
   - professor: Academic, detailed explanations
   - babysitter: Beginner-friendly, simple explanations
   - review: Critical code review
4. *Get Explanation*: Click "Explain Code"

### *Advanced Features*
- *Streaming*: Real-time explanation streaming
- *Copy*: One-click code copying
- *Text-to-Speech*: Listen to explanations
- *Themes*: Dark/light mode toggle
- *Keyboard Shortcuts*: Ctrl+Enter to explain

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| / | GET | Main web interface |
| /explain | POST | Get code explanation |
| /explain-stream | POST | Stream code explanation |
| /modes | GET | Get available explanation modes |
| /config | GET | Get current configuration |
| /health | GET | Health check |

## 🔧 Configuration

The .env file contains optimized settings for your hardware:

env
MODEL_NAME=qwen2.5-coder:7b
OLLAMA_NUM_GPU=1
OLLAMA_NUM_CTX=4096
KEEP_ALIVE=10m
MAX_TOKENS=150
TEMPERATURE=0.7
TOP_P=0.9


## 📁 Project Structure


CODEWHISPER-main/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment configuration
├── setup.bat/sh          # Automated setup scripts
├── start.bat/sh          # Application startup scripts
├── SETUP_README.md       # Detailed setup guide
├── backend/
│   ├── config.py         # Backend configuration
│   └── services/
│       └── ollama_service.py
└── frontend/
    ├── index.html        # Main web interface
    ├── script.js         # Frontend JavaScript
    └── styles.css        # Styling


## 🔍 Troubleshooting

### Common Issues

*Ollama not starting:*
bash
ollama list
ollama serve


*Model not found:*
bash
ollama pull qwen2.5-coder:7b


*GPU issues:*
bash
nvidia-smi
nvcc --version


*Port conflicts:*
bash
# Change PORT in .env
PORT=5001


### Performance Issues
- Check GPU memory usage: nvidia-smi
- Monitor system resources: htop (Linux) or Task Manager (Windows)
- Verify model is loaded: ollama list

## 🎨 Explanation Modes

### *👥 Friend Mode*
Casual, friendly explanations in 5-8 bullet points with practical tips.

### *👨‍🏫 Professor Mode*
Academic, structured explanations with sections for Purpose, Flow, Key Concepts, Complexity, and Edge Cases.

### *👩‍🍼 Babysitter Mode*
Beginner-friendly explanations using simple words and tiny examples.

### *🔍 Review Mode*
Critical code review with Issues, Risks, and Refactor Suggestions.

## 🚀 Production Deployment

For production deployment:
1. Use a WSGI server like Gunicorn
2. Set up a reverse proxy (Nginx)
3. Configure proper logging
4. Set up monitoring and alerting

## 📈 Performance Benchmarks

| Hardware | Model | Response Time | Memory Usage | Status |
|----------|-------|---------------|--------------|---------|
| RTX 4050 6GB | qwen2.5-coder:14b | 4-8s | ~8-12GB VRAM | ⚠ May have issues |
| RTX 4050 6GB | qwen2.5-coder:7b | 2-4s | ~4.5GB VRAM | ✅ Recommended |
| RTX 4050 6GB | qwen2.5-coder:3b | 1-2s | ~2.5GB VRAM | ⚡ Fastest |
| CPU Only | qwen2.5-coder:3b | 5-8s | ~6GB RAM | 🔄 Fallback |

## 🔧 Configuration

The .env file contains optimized settings for your hardware:

env
MODEL_NAME=qwen2.5-coder:14b
OLLAMA_NUM_GPU=1
OLLAMA_NUM_CTX=4096
KEEP_ALIVE=10m
MAX_TOKENS=150
TEMPERATURE=0.7
TOP_P=0.9


### *Model Switching*
Use the model switcher scripts to change between models:
bash
./switch_model.bat    # Windows - Interactive menu
./switch_model.sh     # Linux/Mac - Interactive menu


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Check the troubleshooting section
- Review the setup logs
- Monitor GPU and system resources
- Test with different code samples

---

*Made with ❤ for developers who love clean code and great explanations!*
