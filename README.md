Project Structure

```
CODEWHISPER-main/
├── app.py                    # Main application file
├── requirements.txt          # Required Python packages
├── .env                      # Configuration settings
├── backend/
│   ├── config.py            # Application configuration
│   └── services/
│       └── ollama_service.py # AI service handling
├── frontend/
│   ├── index.html           # Main webpage
│   ├── script.js            # Application logic
│   └── styles.css           # Styling
├── setup.bat                # Setup script for Windows
├── setup.sh                 # Setup script for Linux/Mac
├── start_optimized.bat      # Startup for Windows
├── start_optimized.sh       # Startup for Linux/Mac
├── optimize_gpu.bat         # GPU optimization
├── switch_model.bat         # Model switching for Windows
├── switch_model.sh          # Model switching for Linux/Mac
├── monitor.bat              # Monitoring for Windows
├── monitor.sh               # Monitoring for Linux/Mac
├── test_all.py              # Test suite
└── comprehensive_test.bat   # Full tests
```

Getting Started

Automated Setup (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/khiasu/CODEWHISPER.git
   cd CODEWHISPER
   ```
2. Run the setup script:
   · Windows: .\start_optimized.bat
   · Linux/Mac: ./start_optimized.sh

Manual Setup

1. Install Ollama:
   · Windows: Download from https://ollama.ai/download
   · Linux/Mac: curl -fsSL https://ollama.ai/install.sh | sh
2. Start Ollama:
   ```bash
   ollama serve
   ```
3. Download the model (in a new terminal):
   ```bash
   ollama pull qwen2.5-coder:7b
   ```
4. Install Python packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the application:
   ```bash
   python app.py
   ```

Troubleshooting

· Ollama won't start: Try ollama serve and check with ollama list
· Model not found: Run ollama pull qwen2.5-coder:7b
· GPU issues: Check with nvidia-smi (if you have NVIDIA GPU)
· Port conflicts: Change the PORT value in the .env file

For performance issues:

· Monitor GPU memory: nvidia-smi
· Check system resources: Task Manager (Windows) or htop (Linux)
· Verify model is loaded: ollama list

Explanation Modes

The app offers four ways to explain code:

1. Friend Mode – Casual explanations with practical tips
2. Professor Mode – Structured, academic explanations
3. Babysitter Mode – Simple explanations for beginners
4. Review Mode – Critical review with improvement suggestions

---

Made for developers who want to understand code better.