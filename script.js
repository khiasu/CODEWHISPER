// Code Whisper Frontend JavaScript
class CodeWhisper {
    constructor() {
        this.apiUrl = 'http://localhost:5000';
        this.maxCodeLength = 10000;
        this.currentSpeech = null;
        this.currentTheme = 'light';
        
        this.initializeElements();
        this.initializeTheme();
        this.bindEvents();
        this.updateCharCount();
    }

    initializeElements() {
        // Form elements
        this.codeInput = document.getElementById('code-input');
        this.modeSelect = document.getElementById('mode-select');
        this.explainBtn = document.getElementById('explain-btn');
        this.charCount = document.getElementById('char-count');
        
        // Result elements
        this.resultsSection = document.getElementById('results-section');
        this.resultsMeta = document.getElementById('results-meta');
        this.emptyState = document.getElementById('empty-state');
        this.loadingState = document.getElementById('loading-state');
        this.explanationContent = document.getElementById('explanation-content');
        this.explanationText = document.getElementById('explanation-text');
        this.errorState = document.getElementById('error-state');
        this.errorMessage = document.getElementById('error-message');
        
        // Action buttons
        this.copyBtn = document.getElementById('copy-btn');
        this.speakBtn = document.getElementById('speak-btn');
        this.retryBtn = document.getElementById('retry-btn');
        this.clearBtn = document.getElementById('clear-btn');
        
        // Theme toggle
        this.themeToggle = document.getElementById('theme-toggle');
        this.themeIcon = this.themeToggle.querySelector('.theme-icon');
        this.themeText = this.themeToggle.querySelector('.theme-text');
    }

    initializeTheme() {
        // Check for saved theme preference or default to light mode
        const savedTheme = localStorage.getItem('codewhisper-theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        this.currentTheme = savedTheme || (prefersDark ? 'dark' : 'light');
        this.applyTheme(this.currentTheme);
        
        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('codewhisper-theme')) {
                this.currentTheme = e.matches ? 'dark' : 'light';
                this.applyTheme(this.currentTheme);
            }
        });
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        this.currentTheme = theme;
        
        // Update theme toggle button
        if (theme === 'dark') {
            this.themeIcon.textContent = '☀️';
            this.themeText.textContent = 'Light';
        } else {
            this.themeIcon.textContent = '🌙';
            this.themeText.textContent = 'Dark';
        }
        
        // Save preference
        localStorage.setItem('codewhisper-theme', theme);
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        
        // Create smooth transition overlay
        this.createThemeTransition(() => {
            this.applyTheme(newTheme);
        });
    }

    createThemeTransition(callback) {
        // Create overlay element
        const overlay = document.createElement('div');
        overlay.className = 'theme-transition-overlay';
        document.body.appendChild(overlay);
        
        // Trigger transition
        setTimeout(() => {
            overlay.classList.add('active');
        }, 10);
        
        // Apply theme change at peak of transition
        setTimeout(() => {
            callback();
        }, 150);
        
        // Remove overlay
        setTimeout(() => {
            overlay.classList.remove('active');
            setTimeout(() => {
                if (overlay.parentNode) {
                    overlay.parentNode.removeChild(overlay);
                }
            }, 150);
        }, 300);
        
        // Add bounce effect to theme toggle button
        this.themeToggle.style.transform = 'scale(0.9)';
        setTimeout(() => {
            this.themeToggle.style.transform = '';
        }, 150);
    }

    bindEvents() {
        // Form events
        this.codeInput.addEventListener('input', () => this.updateCharCount());
        this.codeInput.addEventListener('paste', () => {
            // Update char count after paste
            setTimeout(() => this.updateCharCount(), 10);
        });
        
        this.explainBtn.addEventListener('click', () => this.explainCode());
        this.codeInput.addEventListener('keydown', (e) => {
            // Ctrl+Enter to explain
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                this.explainCode();
            }
        });
        
        // Action button events
        this.copyBtn.addEventListener('click', () => this.copyExplanation());
        this.speakBtn.addEventListener('click', () => this.toggleSpeech());
        this.retryBtn.addEventListener('click', () => this.explainCode());
        this.clearBtn.addEventListener('click', () => this.clearCode());
        
        // Theme toggle event
        this.themeToggle.addEventListener('click', () => this.toggleTheme());
        
        // Check backend health on load
        this.checkBackendHealth();
    }

    updateCharCount() {
        const length = this.codeInput.value.length;
        this.charCount.textContent = `${length.toLocaleString()} / ${this.maxCodeLength.toLocaleString()} characters`;
        
        // Update color based on length
        if (length > this.maxCodeLength * 0.9) {
            this.charCount.style.color = 'var(--error-color)';
        } else if (length > this.maxCodeLength * 0.7) {
            this.charCount.style.color = 'var(--warning-color)';
        } else {
            this.charCount.style.color = 'var(--text-tertiary)';
        }
        
        // Disable button if too long or empty
        const isDisabled = length > this.maxCodeLength || length === 0;
        this.explainBtn.disabled = isDisabled;
        
        // Enable/disable clear button
        this.clearBtn.disabled = length === 0;
        
        // Add ready state animation when button is enabled and has content
        if (!isDisabled && length > 10) {
            this.explainBtn.classList.add('ready');
        } else {
            this.explainBtn.classList.remove('ready');
        }
    }

    async checkBackendHealth() {
        try {
            const response = await fetch(`${this.apiUrl}/health`);
            if (!response.ok) {
                throw new Error('Backend not responding');
            }
            console.log('✅ Backend is healthy');
        } catch (error) {
            console.warn('⚠️ Backend health check failed:', error);
            this.showNotification('Backend connection issue. Make sure the Flask server is running.', 'warning');
        }
    }

    async explainCode() {
        const code = this.codeInput.value.trim();
        const mode = this.modeSelect.value;

        // Validation
        if (!code) {
            this.showNotification('Please enter some code to explain.', 'error');
            return;
        }

        if (code.length > this.maxCodeLength) {
            this.showNotification(`Code is too long. Maximum ${this.maxCodeLength} characters allowed.`, 'error');
            return;
        }

        // Show loading state
        this.showLoadingState();
        this.explainBtn.disabled = true;

        try {
            const startTime = Date.now();
            
            const response = await fetch(`${this.apiUrl}/explain`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    code: code,
                    mode: mode
                })
            });

            const data = await response.json();
            const duration = Date.now() - startTime;

            if (!response.ok) {
                throw new Error(data.error || `HTTP ${response.status}`);
            }

            // Show success result
            this.showExplanation(data, duration);
            this.showNotification('Code explained successfully!', 'success');

        } catch (error) {
            console.error('Error explaining code:', error);
            this.showErrorState(error.message);
            this.showNotification(`Failed to explain code: ${error.message}`, 'error');
        } finally {
            this.explainBtn.disabled = false;
        }
    }

    showLoadingState() {
        this.hideAllStates();
        this.loadingState.style.display = 'block';
        
        // Add staggered animation to loading elements
        const loadingElements = this.loadingState.querySelectorAll('h3, p, .loading-spinner');
        loadingElements.forEach((el, index) => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            setTimeout(() => {
                el.style.transition = 'all 0.4s ease-out';
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }, index * 100);
        });
        
        // Smooth scroll to results
        this.resultsSection.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }

    showExplanation(data, duration) {
        this.hideAllStates();
        
        // Update meta information
        const modeNames = {
            'friend': '🤝 Friend',
            'professor': '🎓 Professor', 
            'senior': '😤 Senior Dev',
            'babysitter': '🍼 Babysitter'
        };
        
        this.resultsMeta.innerHTML = `
            <div>Mode: ${modeNames[data.mode] || data.mode}</div>
            <div>Response time: ${(duration / 1000).toFixed(1)}s</div>
        `;
        
        // Show explanation content with entrance animation
        this.explanationContent.style.display = 'block';
        this.explanationContent.style.opacity = '0';
        this.explanationContent.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            this.explanationContent.style.transition = 'all 0.5s cubic-bezier(0.16, 1, 0.3, 1)';
            this.explanationContent.style.opacity = '1';
            this.explanationContent.style.transform = 'translateY(0)';
        }, 100);
        
        // Start typing effect after entrance animation
        setTimeout(() => {
            this.startTypingEffect(data.explanation);
        }, 300);
        
        // Update speak button state
        this.updateSpeakButton();
    }

    startTypingEffect(text) {
        // Clear any existing content
        this.explanationText.innerHTML = '';
        
        // Split text into lines for better typing effect
        const lines = text.split('\n');
        let currentLineIndex = 0;
        
        const typeNextLine = () => {
            if (currentLineIndex >= lines.length) {
                // Typing complete
                this.explanationText.classList.add('typing-complete');
                return;
            }
            
            const line = lines[currentLineIndex];
            const lineElement = document.createElement('div');
            lineElement.className = 'typing-line';
            
            // Add line to container
            this.explanationText.appendChild(lineElement);
            
            // Animate line appearance
            setTimeout(() => {
                lineElement.style.animationDelay = '0ms';
            }, 50);
            
            // Type characters in this line
            let charIndex = 0;
            const typeChar = () => {
                if (charIndex < line.length) {
                    lineElement.textContent += line[charIndex];
                    charIndex++;
                    setTimeout(typeChar, 20 + Math.random() * 30); // Variable speed for natural feel
                } else {
                    // Line complete, move to next
                    currentLineIndex++;
                    setTimeout(typeNextLine, 200);
                }
            };
            
            // Start typing this line after a brief delay
            setTimeout(typeChar, 100);
        };
        
        // Start the typing effect
        typeNextLine();
    }

    showErrorState(message) {
        this.hideAllStates();
        this.errorMessage.textContent = message;
        this.errorState.style.display = 'block';
    }

    hideAllStates() {
        this.emptyState.style.display = 'none';
        this.loadingState.style.display = 'none';
        this.explanationContent.style.display = 'none';
        this.errorState.style.display = 'none';
    }

    clearCode() {
        // Clear the textarea with animation
        this.codeInput.style.transition = 'opacity 0.2s ease-out';
        this.codeInput.style.opacity = '0.5';
        
        setTimeout(() => {
            this.codeInput.value = '';
            this.updateCharCount();
            this.codeInput.style.opacity = '1';
            this.codeInput.focus();
            
            // Clear any existing results
            this.hideAllStates();
            this.emptyState.style.display = 'block';
            
            // Show notification
            this.showNotification('Code cleared! Ready for new input.', 'info');
        }, 100);
    }

    async copyExplanation() {
        try {
            const text = this.explanationText.textContent;
            await navigator.clipboard.writeText(text);
            
            // Visual feedback
            const originalText = this.copyBtn.textContent;
            this.copyBtn.textContent = '✅ Copied!';
            this.copyBtn.style.backgroundColor = 'var(--success-color)';
            this.copyBtn.style.color = 'var(--text-inverse)';
            
            setTimeout(() => {
                this.copyBtn.textContent = originalText;
                this.copyBtn.style.backgroundColor = '';
                this.copyBtn.style.color = '';
            }, 2000);
            
            this.showNotification('Explanation copied to clipboard!', 'success');
        } catch (error) {
            console.error('Failed to copy:', error);
            this.showNotification('Failed to copy to clipboard.', 'error');
        }
    }

    toggleSpeech() {
        if (this.currentSpeech && !this.currentSpeech.paused) {
            // Stop current speech
            this.currentSpeech.cancel();
            this.currentSpeech = null;
            this.updateSpeakButton();
        } else {
            // Start speech
            this.speakExplanation();
        }
    }

    speakExplanation() {
        if (!('speechSynthesis' in window)) {
            this.showNotification('Text-to-speech is not supported in your browser.', 'error');
            return;
        }

        const text = this.explanationText.textContent;
        if (!text) return;

        // Cancel any existing speech
        speechSynthesis.cancel();

        // Create new speech
        this.currentSpeech = new SpeechSynthesisUtterance(text);
        this.currentSpeech.rate = 0.9;
        this.currentSpeech.pitch = 1;
        this.currentSpeech.volume = 1;

        // Event handlers
        this.currentSpeech.onstart = () => {
            this.updateSpeakButton(true);
        };

        this.currentSpeech.onend = () => {
            this.currentSpeech = null;
            this.updateSpeakButton(false);
        };

        this.currentSpeech.onerror = (event) => {
            console.error('Speech error:', event);
            this.currentSpeech = null;
            this.updateSpeakButton(false);
            this.showNotification('Failed to read text aloud.', 'error');
        };

        // Start speaking
        speechSynthesis.speak(this.currentSpeech);
    }

    updateSpeakButton(speaking = null) {
        const isSpeaking = speaking !== null ? speaking : (this.currentSpeech && !this.currentSpeech.paused);
        
        if (isSpeaking) {
            this.speakBtn.textContent = '⏹️ Stop';
            this.speakBtn.style.backgroundColor = 'var(--error-color)';
            this.speakBtn.style.color = 'var(--text-inverse)';
        } else {
            this.speakBtn.textContent = '🔊 Read Aloud';
            this.speakBtn.style.backgroundColor = '';
            this.speakBtn.style.color = '';
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '12px 20px',
            borderRadius: '8px',
            color: 'white',
            fontWeight: '500',
            zIndex: '1000',
            maxWidth: '400px',
            boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease-in-out'
        });
        
        // Set background color based on type
        const colors = {
            success: 'var(--success-color)',
            error: 'var(--error-color)',
            warning: 'var(--warning-color)',
            info: 'var(--accent-color)'
        };
        notification.style.backgroundColor = colors[type] || colors.info;
        
        // Add to DOM
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 10);
        
        // Remove after delay
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 4000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.codeWhisper = new CodeWhisper();
    
    // Add some helpful keyboard shortcuts info
    console.log('🎯 Code Whisper Keyboard Shortcuts:');
    console.log('   Ctrl+Enter: Explain code');
    console.log('   Escape: Stop speech (if speaking)');
    console.log('   Theme toggle: Click the theme button');
    
    // Add escape key handler for stopping speech
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && window.codeWhisper?.currentSpeech) {
            window.codeWhisper.toggleSpeech();
        }
    });
    
    console.log('🚀 Code Whisper loaded successfully!');
});
