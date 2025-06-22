import os
import base64
from typing import Optional, Dict, Any
from anthropic import Anthropic
import streamlit as st


class ClaudeClient:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"
    
    def analyze_hardware(
        self,
        image_data: Optional[bytes] = None,
        image_format: Optional[str] = None,
        problem_description: str = "",
        system_prompt: str = ""
    ) -> str:
        try:
            messages = []
            
            user_content = []
            
            if problem_description:
                user_content.append({
                    "type": "text",
                    "text": f"Problem description: {problem_description}"
                })
            
            if image_data and image_format:
                base64_image = base64.b64encode(image_data).decode('utf-8')
                user_content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": f"image/{image_format}",
                        "data": base64_image
                    }
                })
            
            if not user_content:
                user_content.append({
                    "type": "text",
                    "text": "Please provide general hardware troubleshooting advice."
                })
            
            messages.append({
                "role": "user",
                "content": user_content
            })
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.3,
                system=system_prompt,
                messages=messages
            )
            
            return response.content[0].text
            
        except Exception as e:
            st.error(f"Error communicating with Claude API: {str(e)}")
            return "Sorry, I encountered an error while analyzing your hardware. Please try again."
    
    def validate_api_key(self) -> bool:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{
                    "role": "user",
                    "content": "Hello"
                }]
            )
            return True
        except Exception:
            return False