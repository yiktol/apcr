import streamlit as st
import uuid
import json
import boto3
from typing import List, Dict, Any

# Page configuration
st.set_page_config(
    page_title="Retail Assistant",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
def init_session_state():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "text": "Hi, I'm a Customer Retail Assistant. How may I assist you today?"}]
    if "agent_id" not in st.session_state:
        st.session_state.agent_id = 'W789VIBDQ3'
    if "agent_alias_id" not in st.session_state:
        st.session_state.agent_alias_id = 'TSTALIASID'
    if "enable_trace" not in st.session_state:
        st.session_state.enable_trace = False

init_session_state()

# Initialize AWS Bedrock client
@st.cache_resource
def get_bedrock_client():
    return boto3.client("bedrock-agent-runtime", region_name='us-east-1')

client = get_bedrock_client()

# Sidebar UI
with st.sidebar:
    st.markdown("## 🛠️ Agent Configuration")
    
    st.session_state.agent_id = st.text_input("Agent ID", value=st.session_state.agent_id)
    st.session_state.agent_alias_id = st.text_input("Agent Alias ID", value=st.session_state.agent_alias_id)
    st.session_state.enable_trace = st.checkbox("Enable Trace", value=st.session_state.enable_trace)
    
    st.divider()
    
    st.markdown("### 🧩 Session Controls")
    
    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.chat_history = [{"role": "assistant", "text": "Hi, I'm a Customer Retail Assistant. How may I assist you today?"}]
        st.rerun()
    
    if st.button("🔄 Reset Session", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_session_state()
        st.rerun()
    
    st.divider()
    
    with st.expander("ℹ️ About this app"):
        st.markdown("""
        This application uses AWS Bedrock Agents to power a retail assistant 
        specializing in footwear recommendations.
        
        The assistant can help you find the right shoes based on your 
        preferences and needs.
        """)
    
    # Display current session information
    st.markdown("### 📊 Session Info")
    st.markdown(f"**Session ID:** `{st.session_state.session_id[:8]}...`")
    st.markdown(f"**Messages:** {len(st.session_state.chat_history)}")

# Main UI
st.title("👟 Retail Assistant - Shoe Department")
st.markdown("""
<div style='display: flex; align-items: center; margin-bottom: 20px;'>
    <div style='font-size: 48px; margin-right: 15px;'>🏃‍♀️👞👢👠👟</div>
    <div>
        <p>Ask me about running shoes, hiking boots, or any footwear!</p>
        <p><em>I'm here to help you find the perfect fit.</em></p>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat container with custom styling
chat_container = st.container()
with chat_container:
    # Display chat messages from history
    for message in st.session_state.chat_history:
        icon = "🛍️" if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=icon if message["role"] == "assistant" else None):
            st.markdown(message["text"])

# Function to get response from Bedrock agent
def get_chat_response(input_text: str) -> str:
    response = client.invoke_agent(
        inputText=input_text,
        agentId=st.session_state.agent_id,
        agentAliasId=st.session_state.agent_alias_id,
        sessionId=st.session_state.session_id,
        enableTrace=st.session_state.enable_trace
    )
    
    event_stream = response['completion']
    full_response = ""
    
    try:
        for event in event_stream:
            if 'chunk' in event:
                chunk = event['chunk']['bytes'].decode('utf-8')
                full_response += chunk
            elif 'trace' in event and st.session_state.enable_trace:
                st.sidebar.json(event['trace'])
    except Exception as e:
        st.error(f"Error processing response: {str(e)}")
    
    return full_response

# Chat input and processing
user_input = st.chat_input("Ask about shoes...", key="user_input")

if user_input:
    # Add user message to chat
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    
    # Generate and display assistant response
    with st.chat_message("assistant", avatar="🛍️"):
        with st.spinner("Finding the perfect shoes for you..."):
            response = get_chat_response(user_input)
            st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.chat_history.append({"role": "assistant", "text": response})

# Add some CSS for better styling
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .stChatMessage[data-testid="stChatMessage"] {
        background-color: #f0f2f6;
    }
    .stChatMessage[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] {
        background-color: white;
        border-radius: 0.5rem;
        padding: 0.75rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    .stSidebar {
        background-color: #f8f9fa;
    }
    h1 {
        margin-bottom: 0.5rem;
    }
    .main .block-container {
        padding-top: 2rem;
    }
    /* Styling for emoji row */
    .shoe-emoji-banner {
        font-size: 24px;
        margin: 10px 0;
        text-align: center;
    }
    /* Button styling */
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
    }
</style>

<div class="shoe-emoji-banner">👟 👞 👠 👢 👡 🥾 🥿 👟</div>
""", unsafe_allow_html=True)
