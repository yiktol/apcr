from langchain_community.llms import Bedrock
from langchain_community.chat_models import BedrockChat
import streamlit as st
import boto3
import utils.helpers as helpers

# Page configuration
st.set_page_config(
    page_title="Few-shot vs. Zero-shot Prompting",
    page_icon=":rocket:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state variables if they don't exist
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.prompt_type = "Zero-shot"
    st.session_state.image = "images/zero_shot.png"
    
    # Example prompts
    st.session_state.prompt = """Tell me the sentiment of the following headline and categorize it as either positive, negative or neutral:\n
"New airline between Seattle and San Francisco offers a great opportunity for both passengers and investors.\""""
    
    st.session_state.height = 150

# AWS Bedrock client initialization
@st.cache_resource
def runtime_client(region='us-east-1'):
    bedrock_runtime = boto3.client(
        service_name='bedrock-runtime',
        region_name=region,
    )
    return bedrock_runtime

bedrock_runtime = runtime_client()

# Define prompts
prompt_options = {
    "Zero-shot": {
        "prompt": """Tell me the sentiment of the following headline and categorize it as either positive, negative or neutral:\n
"New airline between Seattle and San Francisco offers a great opportunity for both passengers and investors.\"""",
        "height": 150,
        "image": "images/zero_shot.png"
    },
    "Few-shot": {
        "prompt": """Tell me the sentiment of the following headline and categorize it as either positive, negative or neutral. Here are some examples: \
\n
Research firm fends off allegations of impropriety over new technology.\n
Answer: Negative \
\n
Offshore wind farms continue to thrive as vocal minority in opposition dwindles.\n
Answer: Positive \
\n
Manufacturing plant is the latest target in investigation by state officials.\n
Answer:""",
        "height": 350,
        "image": "images/few_shot.png"
    }
}

# Define helper functions
def reset_session():
    """Reset the session state to default values"""
    for key in st.session_state.keys():
        if key != "initialized":  # Keep the initialized flag
            del st.session_state[key]
    st.session_state.prompt = prompt_options["Zero-shot"]["prompt"]
    st.session_state.height = prompt_options["Zero-shot"]["height"]
    st.session_state.prompt_type = "Zero-shot"
    st.session_state.image = prompt_options["Zero-shot"]["image"]
    # st.rerun()

def update_prompt_type(prompt_type):
    """Update the prompt type and related fields"""
    st.session_state.prompt_type = prompt_type
    st.session_state.prompt = prompt_options[prompt_type]["prompt"]
    st.session_state.height = prompt_options[prompt_type]["height"]
    st.session_state.image = prompt_options[prompt_type]["image"]

def call_llm(prompt, model_id, provider):
    """Call the LLM based on provider type"""
    if provider == "Claude 3":
        params = helpers.getmodelparams(provider)
        params.update({'messages': [{"role": "user", "content": prompt}]})
        
        llm = BedrockChat(model_id=model_id, client=bedrock_runtime, model_kwargs=params)
        response = llm.invoke(prompt)
        
        return st.info(response.content)
    else:
        llm = Bedrock(model_id=model_id, client=bedrock_runtime, model_kwargs=helpers.getmodelparams(provider))
        response = llm.invoke(prompt)
        return st.info(response)

# Sidebar
with st.sidebar:
    st.title("Settings")
    
    # Reset session button
    st.button("Reset Session", on_click=reset_session, type="primary")
    
    # Model selection
    st.subheader("Model Configuration")
    provider = st.selectbox('Provider', helpers.list_providers, index=1)
    models = helpers.getmodelIds(provider)
    model_id = st.selectbox(
        'Model', models, index=models.index(helpers.getmodelId(provider)))
    
    # Prompt selection
    st.subheader("Prompt Type")
    prompt_tabs = st.tabs(list(prompt_options.keys()))
    
    for i, (prompt_type, tab) in enumerate(zip(prompt_options.keys(), prompt_tabs)):
        with tab:
            st.write(f"**{prompt_type} Prompting**")
            st.write(prompt_options[prompt_type]["prompt"][:100] + "...")
            st.button(f"Use {prompt_type} Prompt", key=f"btn_{prompt_type}", 
                     on_click=update_prompt_type, args=(prompt_type,))

# Main content
st.title("📝 Few-shot vs. Zero-shot Prompting")

st.markdown('''
### Understanding Different Prompting Strategies

**Zero-shot prompting** provides no examples and asks the model to perform a task directly.

**Few-shot prompting** (or in-context learning) provides examples of input-output pairs to help 
the model better understand what you're looking for, improving its performance on specific tasks.
''')

# Visual representation of current prompt type
st.subheader(f"Current Mode: {st.session_state.prompt_type} Prompting")
st.image(st.session_state.image, width=600)

# Input form
with st.form("prompt_form"):
    prompt_input = st.text_area(
        "Edit your prompt below:",
        value=st.session_state.prompt,
        height=st.session_state.height
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        submit_button = st.form_submit_button("Submit", type="primary", use_container_width=True)
    with col2:
        st.write("")

# Process the submission
if submit_button:
    with st.spinner("Processing your request..."):
        st.subheader("Response:")
        call_llm(prompt_input, model_id, provider)

# Information about the different approaches
with st.expander("Learn More About Prompting Techniques"):
    st.markdown("""
    ### Prompting Strategy Tips
    
    - **Zero-shot**: Best for straightforward tasks where the model already has sufficient knowledge
    - **Few-shot**: Useful for tasks requiring specific formatting or reasoning patterns
    
    Few-shot examples should be diverse and representative of the task to prevent bias.
    """)
