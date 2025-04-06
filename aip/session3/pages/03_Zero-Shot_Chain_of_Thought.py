from langchain_community.llms import Bedrock
import streamlit as st
import boto3
import utils.helpers as helpers
import threading
import uuid

# Page configuration with custom styling
st.set_page_config(
    page_title="AI Prompt Engineering",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom CSS for modern look
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stTextArea textarea {
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    .header-text {
        font-size: 40px;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 20px;
    }
    .subheader-text {
        font-size: 20px;
        color: #555;
        margin-bottom: 30px;
    }
    .response-container {
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        background-color: #f1f8ff;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for first-time visitors
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    
    # Default prompts
    st.session_state.prompt1 = """Q: A juggler can juggle 16 balls. \
Half of the balls are golf balls, and half of the golf balls are blue. \
How many blue golf balls are there?\n 
A:
"""

    st.session_state.prompt2 = """Q: A juggler can juggle 16 balls. \
Half of the balls are golf balls, and half of the golf balls are blue. \
How many blue golf balls are there?
(Think Step-by-Step)\n
A:"""
    
    st.session_state.response1 = ""
    st.session_state.response2 = ""
    st.session_state.provider = "Anthropic"
    st.session_state.submitted = False

# Sidebar
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # Provider selection
    st.session_state.provider = st.selectbox(
        'Select Provider:',
        helpers.list_providers, 
        index=helpers.list_providers.index(st.session_state.provider)
    )
    
    # Model selection based on provider
    models = helpers.getmodelIds(st.session_state.provider)
    model_id = st.selectbox(
        'Select Model:', 
        models, 
        index=models.index(helpers.getmodelId(st.session_state.provider))
    )
    
    # Reset session button
    if st.button("Reset Session", type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # Information box
    with st.expander("About Chain-of-Thought Prompting"):
        st.info("""
        Chain-of-Thought (CoT) prompting is a technique that enhances reasoning in AI models by 
        encouraging them to generate step-by-step explanations before providing the final answer.
        This approach has been shown to significantly improve performance on complex reasoning tasks.
        """)

# Create Bedrock client
@st.cache_resource
def get_bedrock_client():
    return boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

bedrock_runtime = get_bedrock_client()

# Main function to call LLM
def call_llm(prompt, model_id):
    try:
        llm = Bedrock(
            model_id=model_id,
            client=bedrock_runtime,
            model_kwargs=helpers.getmodelparams(st.session_state.provider)
        )
        return llm.invoke(prompt)
    except Exception as e:
        return f"Error: {str(e)}"

# Main page content
st.markdown("<h1 class='header-text'>Chain-of-thought (CoT) Prompting</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader-text'>Explore how different prompting techniques affect AI reasoning capabilities</p>", unsafe_allow_html=True)

# Information cards
with st.container():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        ### Key Benefits of Chain-of-Thought:
        - ✅ Improves reasoning abilities in foundation models
        - ✅ Addresses multi-step problem-solving challenges
        - ✅ Generates intermediate reasoning steps, mimicking human thought
        - ✅ Enhances model performance compared to standard methods
        - ✅ Works particularly well with larger models (>100B parameters)
        """)
    
    with col2:
        st.image("images/zero-shot-cot.png", caption="CoT Illustration", use_container_width=True)

# Prompt input section
st.markdown("### 🔍 Compare Zero-Shot vs. Zero-Shot-CoT")

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Standard Zero-Shot")
        st.session_state.prompt1 = st.text_area(
            "Enter your zero-shot prompt:",
            value=st.session_state.prompt1,
            height=150,
            key="zero_shot_input"
        )
    
    with col2:
        st.markdown("#### Zero-Shot with Chain-of-Thought")
        st.session_state.prompt2 = st.text_area(
            "Enter your zero-shot-CoT prompt:",
            value=st.session_state.prompt2,
            height=150,
            key="zero_shot_cot_input"
        )

# Submit button
submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
with submit_col2:
    if st.button("📝 Generate Responses", type="primary"):
        st.session_state.submitted = True
        with st.spinner("Processing prompts..."):
            # Run both prompts concurrently
            st.session_state.response1 = call_llm(st.session_state.prompt1, model_id)
            st.session_state.response2 = call_llm(st.session_state.prompt2, model_id)

# Display responses
if st.session_state.submitted:
    st.markdown("### 🤖 Model Responses")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Zero-Shot Results")
        st.markdown(f"""<div class="response-container">
                    <pre>{st.session_state.response1}</pre>
                    </div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Zero-Shot-CoT Results")
        st.markdown(f"""<div class="response-container">
                    <pre>{st.session_state.response2}</pre>
                    </div>""", unsafe_allow_html=True)
    
    # Analysis section
    st.markdown("### 📊 Analysis")
    st.info("Compare the responses above to see how the Chain-of-Thought approach affects the model's reasoning process and final answer.")

# Footer
st.markdown("---")
st.markdown("*This tool demonstrates the impact of different prompting techniques on AI reasoning capabilities.*")
