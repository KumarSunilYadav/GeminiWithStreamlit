import streamlit as st
import google.generativeai as genai
from datetime import datetime
import os
from utils.chat_utils import format_message, get_timestamp
from config import STREAMLIT_CONFIG

# Configure page
st.set_page_config(**STREAMLIT_CONFIG)

# Custom CSS for ChatGPT-like styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2e7d32;
        margin-bottom: 2rem;
        font-size: 2.5rem;
    }
    
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 5px 18px;
        margin: 1rem 0;
        margin-left: 20%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .bot-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 18px 5px;
        margin: 1rem 0;
        margin-right: 20%;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
    }
    
    .timestamp {
        font-size: 0.75rem;
        opacity: 0.8;
        margin-top: 0.5rem;
        text-align: right;
    }
    
    .chat-input {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 1rem;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    }
    
    .sidebar-header {
        color: #2e7d32;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 0.75rem 1rem;
    }
    
    .stButton > button {
        border-radius: 25px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        font-weight: bold;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

# Main app function
def main():
    initialize_session_state()
    
    # Header
    st.markdown("<h1 class='main-header'>🤖 Gemini Chat Assistant</h1>", unsafe_allow_html=True)
    
    # Sidebar
    setup_sidebar()
    
    # Main chat interface
    if not st.session_state.api_key:
        show_welcome_screen()
    else:
        chat_interface()

def setup_sidebar():
    with st.sidebar:
        st.markdown("<div class='sidebar-header'>⚙️ Configuration</div>", unsafe_allow_html=True)
        
        # API Key input
        api_key = st.text_input(
            "🔑 Gemini API Key:",
            type="password",
            value=st.session_state.api_key,
            help="Enter your Google Gemini API key"
        )
        
        if api_key:
            st.session_state.api_key = api_key
            genai.configure(api_key=api_key)
            st.success("✅ API Key configured!")
        
        st.markdown("---")
        
        # Chat controls
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("🔄 Refresh App", use_container_width=True):
            st.rerun()
        
        st.markdown("---")
        
        # Instructions
        st.markdown("""
        <div class='info-box'>
            <h4>🚀 How to get API Key:</h4>
            <ol>
                <li>Visit <a href='https://makersuite.google.com/app/apikey' target='_blank' style='color: white;'>Google AI Studio</a></li>
                <li>Create a new API key</li>
                <li>Copy and paste it above</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        # Stats
        if st.session_state.messages:
            st.markdown("---")
            st.markdown(f"💬 **Messages:** {len(st.session_state.messages)}")
            st.markdown(f"🤖 **Responses:** {len([m for m in st.session_state.messages if m['role'] == 'assistant'])}")

def show_welcome_screen():
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h2>Welcome to Gemini Chat! 🎉</h2>
        <p style='font-size: 1.2rem; color: #666;'>
            Please enter your Gemini API key in the sidebar to start chatting.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("🔑 Enter your API key in the sidebar to begin!")

def chat_interface():
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(format_message(
                    content=message["content"],
                    role="user",
                    timestamp=message["timestamp"]
                ), unsafe_allow_html=True)
            else:
                st.markdown(format_message(
                    content=message["content"],
                    role="assistant",
                    timestamp=message["timestamp"]
                ), unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "",
                placeholder="💭 Type your message here...",
                label_visibility="collapsed"
            )
        
        with col2:
            submit_button = st.form_submit_button("Send 🚀", use_container_width=True)
    
    # Process user input
    if submit_button and user_input.strip():
        handle_user_input(user_input.strip())

def handle_user_input(user_input):
    # Add user message
    timestamp = get_timestamp()
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": timestamp
    })
    
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Show loading
        with st.spinner("🤖 Gemini is thinking..."):
            # Generate response
            response = model.generate_content(user_input)
            
            # Add bot response
            bot_timestamp = get_timestamp()
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.text,
                "timestamp": bot_timestamp
            })
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.error("Please check your API key and internet connection.")
    
    # Rerun to update chat
    st.rerun()

# Footer
def show_footer():
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Built with ❤️ using <strong>Streamlit</strong> and <strong>Google Gemini API</strong></p>
        <p>🚀 Deployed on Streamlit Cloud</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    show_footer()