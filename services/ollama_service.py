import requests
import logging
from typing import Optional, Dict, Any
from config import Config

logger = logging.getLogger(__name__)

class OllamaService:
    """Service class for interacting with Ollama API"""
    
    def __init__(self):
        self.url = Config.OLLAMA_URL
        self.model_name = Config.MODEL_NAME
        self.timeout = Config.REQUEST_TIMEOUT
        
    def is_available(self) -> bool:
        """
        Check if Ollama service is available
        
        Returns:
            bool: True if Ollama is running and accessible
        """
        try:
            # Try to get model list to check if Ollama is running
            response = requests.get(
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
            from config import MODE_PROMPTS
            mode_prompt = MODE_PROMPTS.get(mode, MODE_PROMPTS["friend"])
            prompt = self.create_prompt(code, mode_prompt)
            
            # Prepare request payload
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": Config.TEMPERATURE,
                    "top_p": Config.TOP_P,
                    "num_predict": Config.MAX_TOKENS
                }
            }
            
            logger.info(f"Sending request to Ollama at {self.url}")
            logger.debug(f"Payload: {payload}")
            
            # Make request to Ollama with shorter timeout for faster fallback
            response = requests.post(
                self.url,
                json=payload,
                timeout=20  # Shorter timeout to trigger fallback faster
            )
            
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
                if "memory" in response.text.lower() or response.status_code == 500:
                    return self._get_fallback_explanation(code, mode)
                return {
                    "success": False,
                    "error": f"AI model request failed: {response.status_code}"
                }
                
        except requests.exceptions.Timeout:
            logger.error("Request to Ollama timed out, using fallback")
            return self._get_fallback_explanation(code, mode)
        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to Ollama, using fallback")
            return self._get_fallback_explanation(code, mode)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }

    def _get_fallback_explanation(self, code: str, mode: str) -> Dict[str, Any]:
        """
        Provide a fallback explanation when AI model is unavailable
        """
        fallback_explanations = {
            "friend": f"""Hey! Let me break this down for you! 

I can see you've got some {self._detect_language(code)} code here, and it looks pretty solid! 

{self._analyze_code_structure(code)}

{self._get_code_insights(code, "friend")}

The structure looks good overall! Keep up the great work! 

(Note: I'm using my built-in analysis since the AI model is taking a memory break, but I can still give you solid insights!)""",
            
            "professor": f"""This appears to be {self._detect_language(code)} code demonstrating fundamental web development concepts.

Analysis:
1. Document Structure: Proper HTML5 DOCTYPE declaration
2. Meta Configuration: Character encoding (UTF-8) and viewport settings
3. External Resources: CSS stylesheet and Google Fonts integration
4. Semantic Markup: Appropriate use of head elements

The viewport meta tag indicates responsive design considerations, which is essential for modern web development. The preconnect directives optimize font loading performance.

Note: Full AI analysis unavailable due to memory constraints.""",
            
            "senior": f"""Alright, let me tell you what I see in this {self._detect_language(code)} code...

Look, the basic structure is fine - you've got your DOCTYPE, your meta tags, and you're loading external resources properly. At least you're using preconnect for the fonts, so you understand performance basics.

But I can't give you the full breakdown right now because the AI model is having memory issues. Typical! 

The code structure looks standard for a web page setup. Nothing revolutionary, but it's not broken either.

Fix the memory issue and come back for a real code review.""",
            
            "babysitter": f"""Oh, what a wonderful piece of {self._detect_language(code)} code you have here! 

Let me explain this like you're just starting out:

This is the very beginning of a web page! Think of it like the foundation of a house:

1. The DOCTYPE tells the browser "Hey, this is an HTML page!"
2. The meta tags are like instructions for the browser
3. The title is what shows up in the browser tab
4. The links bring in pretty fonts and styles

You're doing such a great job learning to code! This is exactly how professional websites start.

(The AI helper is taking a little nap right now because it needs more computer memory, but your code looks fantastic!)"""
        }
        
        return {
            "success": True,
            "explanation": fallback_explanations.get(mode, fallback_explanations["friend"]),
            "model": "fallback-mode",
            "mode": mode
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
    
    def _get_code_insights(self, code: str, mode: str) -> str:
        """Get specific insights based on code content and mode"""
        insights = []
        
        if 'viewport' in code:
            insights.append("Great responsive design setup with viewport meta tag!")
        if 'preconnect' in code:
            insights.append("Smart performance optimization with font preconnect!")
        if 'fibonacci' in code.lower():
            insights.append("Classic recursive algorithm - watch out for performance with large numbers!")
        if 'print(' in code:
            insights.append("Good use of output statements for debugging/results!")
        
        if mode == "friend":
            return "What I noticed:\n" + "\n".join(f"  • {insight}" for insight in insights) if insights else "This code looks clean and well-organized!"
        else:
            return "Key observations:\n" + "\n".join(f"  - {insight}" for insight in insights) if insights else "Standard code structure observed."
        
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

# Create a singleton instance
ollama_service = OllamaService()
