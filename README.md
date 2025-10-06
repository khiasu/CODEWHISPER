## 📁 *Project Structure*


CODEWHISPER-main/
├── 📦 Core Application
│   ├── app.py                 # Main Flask application server
│   ├── requirements.txt       # Python dependencies with versions
│   └── .env                   # Environment configuration (optimized)
│
├── 💻 Backend Architecture
│   ├── backend/
│   │   ├── config.py         # Configuration management & mode prompts
│   │   └── services/
│   │       └── ollama_service.py # AI service layer with streaming
│   └── 🎨 Frontend Assets
│       ├── frontend/
│       │   ├── index.html        # Main HTML5 application
│       │   ├── script.js         # ES6+ JavaScript (701 lines)
│       │   └── styles.css        # Modern CSS3 with animations
│
├── 🚀 Automation Scripts
│   ├── setup.bat/sh          # Automated environment setup
│   ├── start_optimized.bat   # GPU-optimized startup
│   ├── optimize_gpu.bat      # GPU memory optimization
│   └── switch_model.bat/sh   # Model switching utility
│
├── 📊 Monitoring & Testing
│   ├── monitor.bat/sh        # System monitoring
│   ├── test_all.py           # Comprehensive test suite
│   └── comprehensive_test.bat # Full system testing
│
└── 📚 Documentation
    ├── README.md             # This comprehensive guide
    ├── SETUP_README.md       # Detailed setup instructions
    └── DEPLOYMENT_GUIDE.md   # Production deployment guide



## 🚀 *Quick Setup Guide*

### *Option 1: Automated Setup (Recommended)*
bash
# 1. Clone the repository
git clone https://github.com/khiasu/CODEWHISPER.git
cd CODEWHISPER

# 2. Run optimized setup (Windows)
.\start_optimized.bat

# 2. Run optimized setup (Linux/Mac)
./start_optimized.sh


### *Option 2: Manual Setup*
bash
# 1. Install Ollama
# Windows: Download from https://ollama.ai/download
# Linux/Mac:
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Start Ollama service
ollama serve

# 3. Pull the optimized model (in new terminal)
ollama pull qwen2.5-coder:7b

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Start CODEWHISPER
python app.py



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




*🚀 CODEWHISPER - Transforming Code into Knowledge*

Made with ❤ for developers who love clean code and great explanations!

*[⭐ Star this repo](https://github.com/khiasu/CODEWHISPER) | [🍴 Fork it](https://github.com/khiasu/CODEWHISPER/fork) | [📢 Share it](https://twitter.com/intent/tweet?text=Check%20out%20CODEWHISPER%20-%20AI-powered%20code%20explanation%20tool!&url=https://github.com/khiasu/CODEWHISPER)*

</div>
