from datetime import datetime
import re

def get_timestamp():
    """Get current timestamp in HH:MM:SS format"""
    return datetime.now().strftime("%H:%M:%S")

def format_message(content, role, timestamp):
    """Format message for display in chat interface"""
    if role == "user":
        return f"""
        <div class="user-message">
            <strong>👤 You:</strong><br>
            {content}
            <div class="timestamp">{timestamp}</div>
        </div>
        """
    else:
        return f"""
        <div class="bot-message">
            <strong>🤖 Gemini:</strong><br>
            {content}
            <div class="timestamp">{timestamp}</div>
        </div>
        """

def clean_text(text):
    """Clean and format text for better display"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    # Handle code blocks
    text = text.replace('```', '\n```\n')
    return text

def truncate_message(message, max_length=1000):
    """Truncate long messages"""
    if len(message) <= max_length:
        return message
    return message[:max_length] + "... [truncated]"

def validate_api_key(api_key):
    """Basic validation for API key format"""
    if not api_key:
        return False, "API key is required"
    
    if len(api_key) < 20:
        return False, "API key seems too short"
    
    return True, "Valid API key format"