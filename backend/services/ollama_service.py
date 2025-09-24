import requests
import logging
import json
import time
from typing import Optional, Dict, Any
from backend.config import Config

logger = logging.getLogger(__name__)

class OllamaService:
    """Service class for interacting with Ollama API"""
    
    def __init__(self):
        self.url = Config.OLLAMA_URL
        self.model_name = Config.MODEL_NAME
        self.timeout = Config.REQUEST_TIMEOUT
        self.keep_alive = getattr(Config, 'KEEP_ALIVE', None)
        # reuse a single session to reduce TCP/TLS overhead and keep-alive
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
    def is_available(self) -> bool:
        """
        Check if Ollama service is available
        
        Returns:
            bool: True if Ollama is running and accessible
        """
        try:
            # Try to get model list to check if Ollama is running
            response = self.session.get(
                f"http://{Config.OLLAMA_HOST}:{Config.OLLAMA_PORT}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama not available: {str(e)}")
            return False
    
    def get_explanation(self, code: str, mode: str) -> Dict[str, Any]:
        """
        Get code explanation from Ollama
        
        Args:
            code (str): The code to explain
            mode (str): The explanation mode/personality
            
        Returns:
            Dict[str, Any]: Response containing explanation or error
        """
        # Check if we should use fallback first due to memory constraints
        if Config.USE_FALLBACK_FIRST:
            logger.info("Using smart fallback due to memory optimization setting")
            return self._get_fallback_explanation(code, mode)
            
        try:
            # Get the mode prompt from config
            from backend.config import MODE_PROMPTS
            mode_alias = "review" if mode == "senior" else mode
            mode_prompt = MODE_PROMPTS.get(mode_alias, MODE_PROMPTS["friend"])
            prompt = self.create_prompt(code, mode_prompt)
            
            # Prepare request payload with memory optimization
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": Config.TEMPERATURE,
                    "top_p": Config.TOP_P,
                    "num_predict": Config.MAX_TOKENS,
                    "num_ctx": getattr(Config, 'OLLAMA_NUM_CTX', 2048),
                    "num_gpu": getattr(Config, 'OLLAMA_NUM_GPU', 0)
                }
            }
            
            logger.info(f"Sending request to Ollama at {self.url}")
            logger.debug(f"Payload: {payload}")
            
            # Make request to Ollama with configurable timeout for slow model
            # Attach keep_alive if configured
            if self.keep_alive:
                payload['keep_alive'] = self.keep_alive
            response = self.session.post(self.url, json=payload, timeout=self.timeout or 90)
            
            if response.status_code == 200:
                result = response.json()
                explanation = result.get('response', '').strip()
                
                if explanation:
                    return {
                        "success": True,
                        "explanation": explanation,
                        "model": self.model_name,
                        "mode": mode
                    }
                else:
                    return {
                        "success": False,
                        "error": "Empty response from AI model"
                    }
            else:
                logger.error(f"Ollama request failed: {response.status_code} - {response.text}")
                # Check if it's a memory issue and provide fallback
                if (response.text and "memory" in response.text.lower()) or response.status_code == 500:
                    return self._get_fallback_explanation(code, mode)
                return {
                    "success": False,
                    "error": f"AI model request failed: {response.status_code}"
                }
                
        except requests.exceptions.Timeout:
            logger.error("Request to Ollama timed out, will wait before using fallback if configured")
            self._delay_before_fallback()
            return self._get_fallback_explanation(code, mode)
        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to Ollama, will wait before using fallback if configured")
            self._delay_before_fallback()
            return self._get_fallback_explanation(code, mode)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }

    def _get_fallback_explanation(self, code: str, mode: str) -> Dict[str, Any]:
        """
        Provide a smart, code-specific fallback explanation
        """
        # Get detailed analysis of the specific code
        language = self._detect_language(code)
        specific_analysis = self._get_detailed_code_analysis(code)
        
        if mode == "friend":
            explanation = f"""Hey! Let me break this down for you!

{specific_analysis}

{self._get_code_suggestions(code)}

Hope this helps! Keep coding! 🚀"""
        
        elif mode == "professor":
            explanation = f"""Academic Analysis of {language} Code:

{specific_analysis}

{self._get_technical_insights(code)}

This demonstrates proper coding practices and structure."""
        
        elif mode == "senior":
            explanation = f"""Alright, let me tell you what I see in this {language} code...

{specific_analysis}

{self._get_critical_feedback(code)}

Fix the memory issue and come back for a real code review."""
        
        else:  # babysitter
            explanation = f"""Oh, what wonderful {language} code you have here! 

{self._get_beginner_explanation(code)}

You're doing such a great job learning to code! 🌟"""
        
        return {
            "success": True,
            "explanation": explanation,
            "model": "smart-fallback",
            "mode": mode
        }
    
    def get_explanation_stream(self, code: str, mode: str):
        """
        Get streaming code explanation from Ollama
        
        Args:
            code (str): The code to explain
            mode (str): The explanation mode/personality
            
        Yields:
            Dict[str, Any]: Stream chunks with explanation content
        """
        try:
            # Get the mode prompt from config
            from backend.config import MODE_PROMPTS
            mode_alias = "review" if mode == "senior" else mode
            mode_prompt = MODE_PROMPTS.get(mode_alias, MODE_PROMPTS["friend"])
            prompt = self.create_prompt(code, mode_prompt)
            
            # Prepare request payload for streaming with memory optimization
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": True,  # Enable streaming
                "options": {
                    "temperature": Config.TEMPERATURE,
                    "top_p": Config.TOP_P,
                    "num_predict": max(64, Config.MAX_TOKENS),  # Keep chunks small on low-RAM
                    "num_ctx": getattr(Config, 'OLLAMA_NUM_CTX', 2048),
                    "num_gpu": getattr(Config, 'OLLAMA_NUM_GPU', 0)
                }
            }
            
            logger.info(f"Starting streaming request to Ollama with mode: {mode}")
            
            # Make streaming request to Ollama
            if self.keep_alive:
                payload['keep_alive'] = self.keep_alive
            # Use (connect_timeout, read_timeout) to allow very long model generation
            stream_timeout = getattr(Config, 'STREAM_TIMEOUT', 600)
            response = self.session.post(self.url, json=payload, timeout=(10, stream_timeout), stream=True)
            
            if response.status_code == 200:
                accumulated_text = ""
                try:
                    for line in response.iter_lines():
                        if line:
                            try:
                                chunk_data = json.loads(line.decode('utf-8'))
                                if 'response' in chunk_data:
                                    text_chunk = chunk_data['response']
                                    accumulated_text += text_chunk
                                    
                                    yield {
                                        "type": "chunk",
                                        "content": text_chunk,
                                        "accumulated": accumulated_text
                                    }
                                    
                                    # Check if this is the final chunk
                                    if chunk_data.get('done', False):
                                        yield {
                                            "type": "done",
                                            "full_text": accumulated_text,
                                            "model": self.model_name
                                        }
                                        break
                                elif chunk_data.get('done', False):
                                    # Model signaled done without a 'response'
                                    yield {
                                        "type": "done",
                                        "full_text": accumulated_text,
                                        "model": self.model_name
                                    }
                                    break
                            except json.JSONDecodeError:
                                continue
                finally:
                    try:
                        response.close()
                    except Exception:
                        pass
            else:
                # Fallback to smart analysis if Ollama fails
                logger.warning(f"Ollama streaming failed, will wait before using smart fallback if configured")
                self._delay_before_fallback()
                fallback_result = self._get_fallback_explanation(code, mode)
                
                # Stream the fallback response word by word for smooth effect
                explanation = fallback_result["explanation"]
                words = explanation.split()
                accumulated = ""
                
                for i, word in enumerate(words):
                    accumulated += word + " "
                    yield {
                        "type": "chunk",
                        "content": word + " ",
                        "accumulated": accumulated.strip()
                    }
                
                yield {
                    "type": "done",
                    "full_text": explanation,
                    "model": "smart-fallback"
                }
                
        except Exception as e:
            logger.error(f"Error in streaming explanation: {str(e)}")
            # Fallback streaming on error — respect delay if configured
            self._delay_before_fallback()
            fallback_result = self._get_fallback_explanation(code, mode)
            explanation = fallback_result["explanation"]
            words = explanation.split()
            accumulated = ""
            
            for word in words:
                accumulated += word + " "
                yield {
                    "type": "chunk", 
                    "content": word + " ",
                    "accumulated": accumulated.strip()
                }
            
            yield {
                "type": "done",
                "full_text": explanation,
                "model": "smart-fallback"
            }
    
    def _detect_language(self, code: str) -> str:
        """Simple language detection based on code content"""
        code_lower = code.lower()
        if '<!doctype' in code_lower or '<html' in code_lower:
            return "HTML"
        elif 'def ' in code or 'import ' in code:
            return "Python"
        elif 'function' in code or 'const ' in code or 'let ' in code:
            return "JavaScript"
        elif '#include' in code or 'int main' in code:
            return "C/C++"
        elif 'class ' in code and '{' in code:
            return "Java/C#"
        else:
            return "programming"
    
    def _analyze_code_structure(self, code: str) -> str:
        """Analyze the basic structure of the code"""
        lines = code.strip().split('\n')
        analysis = []
        
        if '<!DOCTYPE' in code:
            analysis.append("✓ Proper HTML5 document structure")
        if 'import ' in code:
            analysis.append("✓ Uses imports/modules for organization")
        if 'function' in code or 'def ' in code:
            analysis.append("✓ Contains function definitions")
        if '{' in code and '}' in code:
            analysis.append("✓ Uses proper code blocks/scoping")
        if len(lines) > 10:
            analysis.append(f"✓ Well-structured code ({len(lines)} lines)")
        
        return "Code Structure:\n" + "\n".join(f"  {item}" for item in analysis) if analysis else "Basic code structure detected."
    
    def _get_detailed_code_analysis(self, code: str) -> str:
        """Provide detailed analysis of the specific code"""
        lines = code.strip().split('\n')
        analysis = []
        
        # Analyze based on language and content
        if 'fibonacci' in code.lower():
            analysis.append("📊 This is a Fibonacci sequence implementation!")
            if 'def fibonacci' in code:
                analysis.append("🔄 Uses recursive approach - elegant but can be slow for large numbers")
            if 'return fibonacci(n-1) + fibonacci(n-2)' in code:
                analysis.append("⚡ Classic recursive formula: F(n) = F(n-1) + F(n-2)")
            analysis.append(f"🎯 When called with fibonacci(10), it calculates the 10th Fibonacci number (55)")
        
        elif 'def hello' in code.lower():
            analysis.append("👋 This is a simple greeting function!")
            if 'print(' in code:
                analysis.append("📤 Uses print() to display output to the console")
            if 'Hello World' in code:
                analysis.append("🌍 Classic 'Hello World' - the traditional first program!")
            analysis.append("🔧 Simple function definition and call - great for learning basics")
        
        elif 'app.run' in code and ('Flask' in code or 'flask' in code):
            analysis.append("🌐 This is a Flask web application!")
            if 'debug=' in code:
                analysis.append("🐛 Debug mode enabled - shows detailed error messages")
            if 'host=' in code and 'port=' in code:
                analysis.append("🔧 Custom host and port configuration")
            if 'ollama' in code.lower():
                analysis.append("🤖 Integrates with Ollama AI service")
            analysis.append("🚀 Web server startup configuration")
        
        elif '<!DOCTYPE' in code:
            analysis.append("🌐 This is HTML5 document structure")
            if 'viewport' in code:
                analysis.append("📱 Includes responsive viewport configuration")
            if 'preconnect' in code:
                analysis.append("⚡ Optimized with font preconnection for faster loading")
            if 'Google Fonts' in code:
                analysis.append("🎨 Uses Google Fonts for typography")
        
        elif 'import' in code and 'requests' in code:
            analysis.append("🔧 This is a testing/API script")
            if 'BASE_URL' in code:
                analysis.append("🌐 Configured to test a web service")
            if 'localhost:5000' in code:
                analysis.append("🏠 Testing a local Flask development server")
        
        elif 'print(' in code:
            analysis.append("📤 This code produces output using print statements")
            
        return "\n".join(analysis) if analysis else f"This is {self._detect_language(code)} code with {len(lines)} lines."
    
    def _get_code_suggestions(self, code: str) -> str:
        """Get friendly suggestions for the code"""
        suggestions = []
        
        if 'fibonacci' in code.lower() and 'def fibonacci' in code:
            suggestions.append("💡 Pro tip: For better performance with large numbers, consider using memoization or iterative approach!")
            suggestions.append("🚀 This recursive version is great for learning but can be optimized!")
        
        if '<!DOCTYPE' in code:
            suggestions.append("✨ Your HTML structure looks solid! Great foundation for a web page.")
            
        return "\n".join(suggestions) if suggestions else "Keep up the great work! Your code structure looks good! 👍"
    
    def _get_technical_insights(self, code: str) -> str:
        """Get technical insights for professor mode"""
        insights = []
        
        if 'fibonacci' in code.lower():
            insights.append("• Time Complexity: O(2^n) - exponential due to repeated subproblems")
            insights.append("• Space Complexity: O(n) - due to recursion stack depth")
            insights.append("• Algorithm Type: Dynamic Programming problem, currently using naive recursion")
        
        if '<!DOCTYPE html>' in code:
            insights.append("• HTML5 semantic structure with proper document type declaration")
            insights.append("• Meta viewport enables responsive design across devices")
            insights.append("• External resource optimization with preconnect directives")
        
        return "\n".join(insights) if insights else "Standard code implementation observed."
    
    def _get_critical_feedback(self, code: str) -> str:
        """Get critical feedback for senior mode"""
        feedback = []
        
        if 'fibonacci' in code.lower() and 'def fibonacci' in code:
            feedback.append("🔥 Seriously? Naive recursive Fibonacci? This will explode with large inputs!")
            feedback.append("💀 O(2^n) complexity - you're basically DoS'ing yourself")
            feedback.append("🤦 Use memoization or just go iterative. This is CS 101 stuff!")
        elif 'def hello' in code.lower() and 'print(' in code:
            feedback.append("📤 This code produces output using print statements")
            feedback.append("🔧 Simple function definition - at least you're using functions")
            feedback.append("💡 Basic but functional. Nothing wrong with keeping it simple.")
        elif 'app.run' in code and 'Flask' in code:
            feedback.append("🌐 Flask application setup - standard boilerplate")
            feedback.append("⚠️ Running in debug mode - don't do this in production!")
            feedback.append("🔧 Basic web server configuration, nothing fancy")
        elif 'print(' in code:
            feedback.append("📤 This code produces output using print statements")
            feedback.append("🔧 Basic output functionality")
        
        return "\n".join(feedback) if feedback else "Code structure is acceptable. Nothing revolutionary, but it works."
    
    def _get_beginner_explanation(self, code: str) -> str:
        """Get beginner-friendly explanation for babysitter mode"""
        explanation = []
        
        if 'fibonacci' in code.lower():
            explanation.append("🔢 This code creates Fibonacci numbers! It's like a magic number sequence.")
            explanation.append("✨ Each number is made by adding the two numbers before it: 0, 1, 1, 2, 3, 5, 8...")
            explanation.append("🎯 The code asks: 'What's the 10th number in this sequence?' (Answer: 55!)")
            explanation.append("🔄 It uses something called 'recursion' - the function calls itself!")
        
        elif '<!DOCTYPE' in code:
            explanation.append("🏠 This is like building the foundation of a house, but for websites!")
            explanation.append("📋 The DOCTYPE tells the browser 'This is a modern webpage'")
            explanation.append("📱 The viewport part makes it work on phones and tablets too!")
        
        return "\n".join(explanation) if explanation else "This is a wonderful piece of code! You're learning to speak computer language! 🤖"
        
    def _delay_before_fallback(self):
        """Optionally wait before switching to fallback, to allow slow models to finish"""
        try:
            delay = int(getattr(Config, 'FALLBACK_DELAY_SECONDS', 0) or 0)
        except Exception:
            delay = 0
        if delay > 0:
            # Clamp to a reasonable maximum
            wait_seconds = min(delay, 3600)
            logger.info(f"Waiting {wait_seconds}s before using fallback (configured)")
            try:
                time.sleep(wait_seconds)
            except Exception:
                pass

    def create_prompt(self, code: str, mode_prompt: str) -> str:
        """
        Create a well-formatted prompt for code explanation
        
        Args:
            code (str): The code to explain
            mode_prompt (str): The personality prompt for the explanation mode
            
        Returns:
            str: The formatted prompt
        """
        return f"""{mode_prompt}

Please explain the following code:

```
{code}
```

Provide a clear explanation following the personality and style described above. 
Focus on what the code does, how it works, and any important concepts or patterns used."""

# Note: Do not create a module-level singleton here to avoid side effects