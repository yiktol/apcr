from langchain_community.llms import Bedrock
import streamlit as st
import boto3
import utils.helpers as helpers
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
        background-color: #f9f9f9;
    }
    .stButton > button {
        width: 100%;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stTextArea textarea {
        border-radius: 6px;
        border: 1px solid #e0e0e0;
        font-family: 'Courier New', monospace;
    }
    .title-text {
        font-size: 38px;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 10px;
    }
    .subtitle-text {
        font-size: 18px;
        color: #4B5563;
    }
    .info-card {
        background-color: #EFF6FF;
        border-radius: 8px;
        padding: 15px;
        border-left: 4px solid #3B82F6;
    }
    .response-container {
        background-color: #F0F9FF;
        border-radius: 8px;
        padding: 15px;
        margin-top: 10px;
        border: 1px solid #BAE6FD;
    }
    .expander-content {
        padding: 15px;
    }
    .sidebar-header {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for first-time visitors
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    
    # Default prompts
    st.session_state.prompt1 = """Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. \
How many tennis balls does he have now?\n
A: The answer is 11.\n
Q: The cafeteria had 23 apples. If they used 20 to make lunch and bought 6 more, how many apples do they have?\n
A:
"""

    st.session_state.prompt2 = """Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. \
Each can has 3 tennis balls. How many tennis balls does he have now?\n
A: Roger started with 5 balls. 2 cans of 3 tennis balls each is 6 tennis balls. 5 + 6 = 11. The answer is 11.\n
Q: The cafeteria had 23 apples. If they used 20 to make lunch and bought 6 more, how many apples do they have?\n
A:"""
    
    st.session_state.response1 = ""
    st.session_state.response2 = ""
    st.session_state.provider = "Anthropic"
    st.session_state.submitted = False

# Create Bedrock client
@st.cache_resource
def get_bedrock_client():
    return boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

bedrock_runtime = get_bedrock_client()

# Sidebar
with st.sidebar:
    st.markdown("<div class='sidebar-header'>🛠️ Configuration</div>", unsafe_allow_html=True)
    
    # Provider selection
    st.session_state.provider = st.selectbox(
        'Select Provider:',
        helpers.list_providers,
        index=helpers.list_providers.index(st.session_state.provider) if st.session_state.provider in helpers.list_providers else 0
    )
    
    # Model selection based on provider
    models = helpers.getmodelIds(st.session_state.provider)
    model_id = st.selectbox(
        'Select Model:', 
        models, 
        index=models.index(helpers.getmodelId(st.session_state.provider)) if helpers.getmodelId(st.session_state.provider) in models else 0
    )
    
    # Session management
    st.markdown("---")
    st.markdown("### Session Management")
    
    if st.button('🔄 Reset Session', key='reset_session'):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # About section
    st.markdown("---")
    st.markdown("### About")
    st.info("This tool demonstrates the power of few-shot chain-of-thought prompting to improve model reasoning capabilities.")

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
st.markdown("<div class='title-text'>Few-Shot Chain-of-thought (CoT)</div>", unsafe_allow_html=True)

# Information section
with st.container():
    col1, col2 = st.columns([0.7, 0.3])
    
    with col1:
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.markdown("""
        ### Key Advantages:
        
        - ✅ **Works best with larger models**
        - ✅ **Especially effective with:**
            - Arithmetic problems
            - Common sense reasoning
            - Symbolic reasoning
        - ✅ **Provides examples of reasoning paths to guide model thinking**
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.image("images/few_shot_cot.png", caption="Few-Shot CoT Concept", use_container_width=True)

# Explanation
with st.expander("🔍 What is Few-Shot Chain-of-thought (CoT)?"):
    st.markdown("""
    Few-shot chain-of-thought (CoT) prompting is a technique where you provide the model with:
    
    1. A few example problems
    2. Step-by-step solutions to those problems
    3. A new problem to solve
    
    This approach teaches the model how to break down complex reasoning tasks by example, leading to better performance on 
    challenging problems that require multi-step reasoning. The model learns to mimic the reasoning pattern demonstrated in the examples.
    
    The key difference from standard few-shot prompting is that we show the **reasoning process** in addition to just the answers.
    """)
    st.image("images/few_shot_cot.png", use_container_width=True)

# Prompt input section
st.markdown("### 🧪 Compare Standard Few-Shot vs. Few-Shot CoT")

with st.container():
    tab1, tab2 = st.tabs(["📝 Prompts", "📊 Results"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Standard Few-Shot")
            st.session_state.prompt1 = st.text_area(
                "Example with just answers:",
                value=st.session_state.prompt1,
                height=250,
                key="few_shot_input"
            )
        
        with col2:
            st.markdown("#### Few-Shot with Chain-of-Thought")
            st.session_state.prompt2 = st.text_area(
                "Example with reasoning steps:",
                value=st.session_state.prompt2,
                height=250,
                key="few_shot_cot_input"
            )
        
        # Submit button in a centered column
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.button("🚀 Generate Responses", type="primary", use_container_width=True)
        
        if submit:
            st.session_state.submitted = True
            with st.spinner("Processing your prompts..."):
                st.session_state.response1 = call_llm(st.session_state.prompt1, model_id)
                st.session_state.response2 = call_llm(st.session_state.prompt2, model_id)
            
            # Auto-switch to results tab
            tab2.active = True
    
    with tab2:
        if st.session_state.get("submitted", False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Standard Few-Shot Response")
                st.markdown(f"""<div class="response-container">
                            {st.session_state.response1}
                            </div>""", unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### Few-Shot CoT Response")
                st.markdown(f"""<div class="response-container">
                            {st.session_state.response2}
                            </div>""", unsafe_allow_html=True)
            
            # Analysis
            st.markdown("### 💡 Observation")
            st.success("""
            Compare how the model approaches the problem in each case. With few-shot CoT, 
            the model is more likely to break down the problem into steps rather than jumping directly to the answer, 
            potentially leading to more accurate results on complex problems.
            """)
        else:
            st.info("Submit prompts to see results here")

# Footer
st.markdown("---")
st.caption("*Few-shot CoT prompting helps models learn to reason by example, especially effective for numerical and logical reasoning tasks.*")
