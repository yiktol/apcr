import os
import streamlit as st
import boto3
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
from langchain_aws import ChatBedrock

# Page configuration with custom styling
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stApp {
        # max-width: 120px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        display: flex;
    }
    .chat-message.user {
        background-color: #e3f2fd;
    }
    .chat-message.assistant {
        background-color: #f0f4c3;
    }
    .chat-header {
        background: linear-gradient(to right, #4776E6, #8E54E9);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    .sidebar .sidebar-content {
        background-color: #f0f4f8;
    }
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        font-weight: bold;
        background-color: #4CAF50;
        color: white;
    }
    /* Sidebar title styling */
    .sidebar-title {
        font-size: 1.5em;
        font-weight: bold;
        margin-bottom: 1.5rem;
        color: #333;
        text-align: center;
    }
    .memory-status {
        padding: 8px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        margin: 10px 0;
    }
    .memory-enabled {
        background-color: #c8e6c9;
        color: #2e7d32;
    }
    .memory-disabled {
        background-color: #ffcdd2;
        color: #c62828;
    }
</style>
""", unsafe_allow_html=True)

# Initialize AWS Bedrock client
@st.cache_resource
def init_bedrock_client():
    return boto3.client(
        service_name='bedrock-runtime',
        region_name='us-east-1',
    )

bedrock = init_bedrock_client()

# Get language model
@st.cache_resource
def get_llm(temperature=0.7):
    model_kwargs = {
        "maxTokenCount": 1024,
        "temperature": temperature,
        "topP": 0.8
    }
    
    llm = ChatBedrock(
        client=bedrock,
        model_id="amazon.titan-text-premier-v1:0",
        model_kwargs=model_kwargs
    )
    
    return llm

# Get memory for chat session
def get_memory():
    llm = get_llm()
    memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=1024)
    return memory

# Generate chat response
def get_chat_response(input_text, memory=None, use_memory=True):
    llm = get_llm(st.session_state.temperature)
    
    if use_memory and memory:
        conversation = ConversationChain(
            llm=llm,
            memory=memory,
            verbose=False
        )
        chat_response = conversation.predict(input=input_text)
    else:
        # Use a simple prompt without memory
        chat_response = llm.invoke(f"User: {input_text}\nAI: ")
        if hasattr(chat_response, 'content'):  # Handle different return types
            chat_response = chat_response.content
    
    return chat_response

# Sidebar configuration
with st.sidebar:
    st.markdown("<div class='sidebar-title'>Chat Controls</div>", unsafe_allow_html=True)
    
    st.markdown("### Memory Settings")
    
    # Memory toggle
    if 'memory_enabled' not in st.session_state:
        st.session_state.memory_enabled = True
        
    memory_enabled = st.toggle("Enable Conversation Memory", value=st.session_state.memory_enabled)
    st.session_state.memory_enabled = memory_enabled
    
    # Display memory status
    if memory_enabled:
        st.markdown("<div class='memory-status memory-enabled'>Memory: ENABLED</div>", unsafe_allow_html=True)
        st.markdown("Bot will remember your conversation and maintain context.")
    else:
        st.markdown("<div class='memory-status memory-disabled'>Memory: DISABLED</div>", unsafe_allow_html=True)
        st.markdown("Bot will respond to each message independently without context.")
    
    st.markdown("### Model Settings")
    if 'temperature' not in st.session_state:
        st.session_state.temperature = 0.7
    
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, 
                          value=st.session_state.temperature, step=0.1,
                          help="Higher values increase creativity, lower values make responses more deterministic")
    st.session_state.temperature = temperature
    
    st.markdown("### Chat Management")
    clear_chat_btn = st.button("🧹 Clear Chat History", key="clear_chat")
    reset_session_btn = st.button("🔄 Reset Session", key="reset_session")
    
    st.markdown("---")
    st.markdown("#### About")
    st.markdown("""
    This chatbot uses Amazon Bedrock's Titan model with LangChain.
    
    Toggle the conversation memory on/off to compare how the bot responds with and without context.
    """)

# Main content area
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    # Chat header
    memory_status = "with Memory" if st.session_state.memory_enabled else "without Memory"
    st.markdown(f"<div class='chat-header'><h1>AI Assistant ({memory_status})</h1><p>Ask me anything and I'll do my best to help!</p></div>", unsafe_allow_html=True)

    # Initialize session states
    if 'memory' not in st.session_state:
        st.session_state.memory = get_memory()

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "text": "Hello! How can I assist you today?"}]

    # Handle button clicks
    if clear_chat_btn:
        st.session_state.chat_history = [{"role": "assistant", "text": "Chat history cleared. How can I help you?"}]

    if reset_session_btn:
        st.session_state.memory = get_memory()
        st.session_state.chat_history = [{"role": "assistant", "text": "Session reset. How may I assist you?"}]
        st.session_state.memory_enabled = True

    # Display chat messages
    for i, message in enumerate(st.session_state.chat_history):
        message_role = "user" if message["role"] == "user" else "assistant"
        with st.chat_message(message["role"], avatar="👤" if message_role == "user" else "🤖"):
            st.markdown(message["text"])

    # Chat input
    input_text = st.chat_input("Type your message here...")

    # Process user input
    if input_text:
        # Add user message to chat
        with st.chat_message("user", avatar="👤"):
            st.markdown(input_text)
        
        st.session_state.chat_history.append({"role": "user", "text": input_text})
        
        # Get and display AI response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                chat_response = get_chat_response(
                    input_text=input_text, 
                    memory=st.session_state.memory,
                    use_memory=st.session_state.memory_enabled
                )
                st.markdown(chat_response)
        
        st.session_state.chat_history.append({"role": "assistant", "text": chat_response})
