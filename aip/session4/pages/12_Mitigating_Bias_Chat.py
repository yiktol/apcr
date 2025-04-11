import streamlit as st
import boto3
from langchain_aws import ChatBedrock
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import (ChatPromptTemplate, 
                               SystemMessagePromptTemplate, 
                               HumanMessagePromptTemplate, 
                               MessagesPlaceholder)
from langchain_core.runnables import RunnablePassthrough
import utils.sdxl as sdxl
import nest_asyncio  # Added for nested event loops support
import threading

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Thread-safe session state access
thread_local = threading.local()

def safe_session_state_access(key, default=None):
    """Access session state safely from any thread"""
    try:
        if key in st.session_state:
            return st.session_state[key]
        return default
    except:
        # Return default when called from background thread
        return default

# Page configuration
st.set_page_config(
    page_title="AI Image Generator - Mitigating Bias",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session states - Make sure this runs first 
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        return_messages=True,
        human_prefix="Human",
        ai_prefix="Assistant",
        memory_key="history"
    )

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "Assistant", "content": "Hello! I can help you generate unbiased image prompts. What kind of image would you like to create?"}]

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = """You are a prompt generator, who generates prompts for text to image models based on a user question. You and the image AI are not biased and do not discriminate against certain groups of people. If you detect bias in the question, ask relevant questions based on gender, race and color before generating the prompt. If you don't know the answer to a question, truthfully say you don't know. If the image generation question includes human beings, ask all of the following questions with examples before generating the image prompt:

<questions>
- What is the gender of the subject in the picture? (e.g. male, female, transgender etc.)
- What is the color of the subject in the image? (e.g. white, black, or brown etc.)
- What is the race of the subject in the image? (e.g. African-american, latino, indian, korean,
  chineese, asian, etc.)
</questions>

When you are ready to generate the image prompt, return it in <imageprompt></imageprompt> XML tags.
"""

# Store system prompt in thread-safe variable
thread_local.system_prompt = st.session_state.system_prompt

# Setup AWS Bedrock client
@st.cache_resource
def get_bedrock_client():
    return boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

bedrock = get_bedrock_client()
model_id = "anthropic.claude-v2:1"
llm = ChatBedrock(model_id=model_id, client=bedrock)

# Create prompt template and conversation chain using LCEL
def update_conversation_chain():
    # Get system prompt safely for thread
    system_prompt = safe_session_state_access("system_prompt", 
        """You are a prompt generator for text to image models. If you detect bias in the question, ask relevant questions about gender, race and color. When ready to generate, use <imageprompt></imageprompt> XML tags.""")
    
    prompt_template = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(system_prompt),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )
    
    # Create a chain using the LCEL pipe syntax with thread-safe memory access
    def load_memory(_):
        try:
            if "memory" in st.session_state:
                return st.session_state.memory.load_memory_variables({})["history"]
            return []
        except:
            # Return empty when called from background thread
            return []
    
    chain = (
        {"input": RunnablePassthrough(), "history": load_memory}
        | prompt_template
        | llm
    )
    
    return chain

# Only create conversation chain after memory is initialized
conversation = update_conversation_chain()

# Function to generate image from prompt - Make thread-safe
def generate_image(prompt_data):
    # This function is called from main thread so spinner is safe
    with st.spinner("🎨 Generating Image..."):
        try:
            generated_image = sdxl.get_image_from_model(
                prompt=prompt_data, 
                negative_prompt="bias,discriminatory,poorly rendered,poor background details,poorly drawn feature,disfigured features",
                model="stability.stable-diffusion-xl-v1",
                height=512,
                width=512,
                cfg_scale=5, 
                seed=123456789,
                steps=20,
                style_preset="photographic"
            )
            return generated_image
        except Exception as e:
            st.error(f"Image generation error: {str(e)}")
            return None

# Sidebar with controls
with st.sidebar:
    st.title("⚙️ Options")
    
    st.subheader("Session Management")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [{"role": "Assistant", "content": "Hello! I can help you generate unbiased image prompts. What kind of image would you like to create?"}]
        # Make sure memory exists before clearing
        if "memory" in st.session_state:
            st.session_state.memory.clear()
        st.rerun()

    if st.button("🔄 Reset Session", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    with st.expander("ℹ️ About this app"):
        st.markdown("""
        This application generates unbiased image prompts using AI. It helps mitigate potential biases 
        by asking clarifying questions about race, gender, and other attributes when creating images of people.
        
        The app uses:
        - Claude AI for prompt generation
        - Stable Diffusion XL for image creation
        """)

# Main content area
st.title("🎨 AI Image Generator")
st.caption("Create unbiased images with AI assistance")

# System Prompt Expander
with st.expander("🔧 View/Edit System Prompt"):
    system_prompt_input = st.text_area("System Prompt", value=st.session_state.system_prompt, height=300)
    if st.button("Update System Prompt"):
        st.session_state.system_prompt = system_prompt_input
        # Update thread-local variable too
        thread_local.system_prompt = system_prompt_input
        # Make sure memory exists before clearing
        if "memory" in st.session_state:
            st.session_state.memory.clear()
        st.session_state.messages = [{"role": "Assistant", "content": "System prompt updated. How may I assist you?"}]
        conversation = update_conversation_chain()
        st.success("System prompt updated successfully!")

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if isinstance(message["content"], dict) and "text" in message["content"] and "image" in message["content"]:
                st.write(message["content"]["text"])
                st.image(message["content"]["image"])
            else:
                st.write(message["content"])

# User input
user_prompt = st.chat_input("Example: Create a photo of a doctor...")

if user_prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "Human", "content": user_prompt})
    
    # Display user message
    with st.chat_message("Human"):
        st.write(user_prompt)
    
    # Get and display assistant response
    with st.chat_message("Assistant"):
        with st.spinner("Thinking..."):
            # Verify memory exists before using the conversation
            if "memory" not in st.session_state:
                st.session_state.memory = ConversationBufferMemory(
                    return_messages=True,
                    human_prefix="Human",
                    ai_prefix="Assistant",
                    memory_key="history"
                )
                conversation = update_conversation_chain()
                
            try:
                # Use invoke with the chain
                response = conversation.invoke(user_prompt)
                response_text = response.content
                
                # After getting the response, update memory in the main thread
                st.session_state.memory.save_context({"input": user_prompt}, {"output": response_text})
                
                # Check if response contains image prompt
                if "<imageprompt>" in response_text:
                    ix_prompt_start = response_text.find("<imageprompt>") + len("<imageprompt>")
                    ix_prompt_end = response_text.find("</imageprompt>", ix_prompt_start)
                    img_prompt = response_text[ix_prompt_start:ix_prompt_end].strip()
                    
                    st.write(response_text)
                    image = generate_image(img_prompt)
                    
                    if image is not None:
                        st.image(image)
                        
                        # Store both text and image in messages
                        st.session_state.messages.append({
                            "role": "Assistant", 
                            "content": {"text": response_text, "image": image}
                        })
                    else:
                        st.error("Failed to generate image.")
                        st.session_state.messages.append({"role": "Assistant", "content": response_text})
                else:
                    st.write(response_text)
                    st.session_state.messages.append({"role": "Assistant", "content": response_text})
                    
            except Exception as e:
                error_msg = f"Error processing request: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "Assistant", "content": error_msg})
