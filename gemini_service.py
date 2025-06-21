import json
import logging
import os

from google import genai
from google.genai import types
from pydantic import BaseModel



client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "AIzaSyABge7vHFTpvZykbQd_EDvoT35-eSvZp2s"))


class CodeAnalysis(BaseModel):
    explanation: str
    optimization_suggestions: str
    security_notes: str
    performance_rating: int


def analyze_code_with_gemini(language: str, code: str, output: str = "", error: str = "") -> dict:
    """Analyze code execution results using Gemini AI"""
    try:
        prompt = f"""
        Analyze this {language} code execution:
        
        **Code:**
        ```{language}
        {code}
        ```
        
        **Output:**
        {output if output else "No output"}
        
        **Error:**
        {error if error else "No errors"}
        
        Please provide:
        1. Brief explanation of what the code does
        2. Optimization suggestions
        3. Security considerations
        4. Performance rating (1-10)
        
        Keep response concise and educational.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            'analysis': response.text or "Analysis unavailable",
            'status': 'success'
        }

    except Exception as e:
        logging.error(f"Gemini analysis error: {str(e)}")
        return {
            'analysis': f"AI analysis temporarily unavailable: {str(e)}",
            'status': 'error'
        }


def enhance_code_output(language: str, code: str, output: str) -> dict:
    """Enhance code output with AI insights"""
    try:
        prompt = f"""
        For this {language} code execution:
        
        Code: {code}
        Output: {output}
        
        Provide:
        1. Educational explanation of the output
        2. Next learning steps
        3. Related concepts to explore
        
        Be encouraging and educational.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            'enhancement': response.text or "Enhancement unavailable",
            'status': 'success'
        }

    except Exception as e:
        return {
            'enhancement': f"AI enhancement unavailable: {str(e)}",
            'status': 'error'
        }


def suggest_code_improvements(language: str, code: str) -> dict:
    """Suggest code improvements using Gemini"""
    try:
        prompt = f"""
        Review this {language} code and suggest improvements:
        
        ```{language}
        {code}
        ```
        
        Provide:
        1. Code quality assessment
        2. Best practice suggestions
        3. Alternative approaches
        4. Learning resources
        
        Focus on educational value.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            'suggestions': response.text or "Suggestions unavailable",
            'status': 'success'
        }

    except Exception as e:
        return {
            'suggestions': f"AI suggestions unavailable: {str(e)}",
            'status': 'error'
        }


def debug_code_with_gemini(language: str, code: str, error: str) -> dict:
    """Debug code errors using Gemini AI"""
    try:
        prompt = f"""
        Help debug this {language} code error:
        
        **Code:**
        ```{language}
        {code}
        ```
        
        **Error:**
        {error}
        
        Provide:
        1. Error explanation in simple terms
        2. Specific fix suggestions
        3. How to prevent similar errors
        4. Corrected code example if possible
        
        Be helpful and educational.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            'debug_help': response.text or "Debug help unavailable",
            'status': 'success'
        }

    except Exception as e:
        return {
            'debug_help': f"AI debug help unavailable: {str(e)}",
            'status': 'error'
        }