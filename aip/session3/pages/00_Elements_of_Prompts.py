import streamlit as st
import boto3
from langchain_community.llms import Bedrock
from langchain_community.chat_models import BedrockChat
import utils.helpers as helpers

# Page configuration with custom styling
st.set_page_config(
    page_title="AI Prompt Engineering",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom CSS for a modern look
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
    }
    .st-emotion-cache-16idsys p {
        font-size: 1.1rem;
    }
    .provider-selector {
        margin-bottom: 1rem;
    }
    .title-container {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize AWS clients
@st.cache_resource
def get_aws_clients(region='us-east-1'):
    bedrock_runtime = boto3.client(service_name='bedrock-runtime', region_name=region)
    bedrock_client = boto3.client(service_name='bedrock', region_name=region)
    return bedrock_runtime, bedrock_client

bedrock_runtime, bedrock_client = get_aws_clients()

# Model provider mapping
list_providers = ['Amazon', 'Anthropic', 'AI21', 'Claude 3', 'Cohere', 'Meta', 'Mistral']

# Session state management
def clear_session_state():
    for key in st.session_state.keys():
        del st.session_state[key]

# Model ID mapping function
def get_model_id(provider_name):
    model_mapping = {
        "Amazon": "amazon.titan-tg1-large",
        "Titan Image": "amazon.titan-image-generator-v1",
        "Anthropic": "anthropic.claude-v2:1",
        "Claude 3": "anthropic.claude-3-sonnet-20240229-v1:0",
        "AI21": "ai21.j2-ultra-v1",
        'Cohere': "cohere.command-text-v14",
        'Meta': "meta.llama2-70b-chat-v1",
        "Mistral": "mistral.mixtral-8x7b-instruct-v0:1",
        "Stability AI": "stability.stable-diffusion-xl-v1",
        "Anthropic Claude 3": "anthropic.claude-3-sonnet-20240229-v1:0"
    }
    return model_mapping.get(provider_name, model_mapping["Claude 3"])

# Get available models for a provider
@st.cache_data(ttl=3600)
def get_model_ids(provider_name):
    models = []
    available_models = bedrock_client.list_foundation_models()

    if provider_name == "Claude 3":
        for model in available_models['modelSummaries']:
            if 'claude-3' in model['modelId'].split('.')[1]:
                models.append(model['modelId'])
    else:
        for model in available_models['modelSummaries']:
            if provider_name in model['providerName']:
                models.append(model['modelId'])

    return models if models else [get_model_id(provider_name)]

# Sample prompt
default_prompt = """Write a summary of a service review using two sentences. 

Store: Online, Service: Shipping.

Review: Amazon Prime Student is a great option for students looking to save money. Not paying for shipping is the biggest save in my opinion. As a working mom of three who is also a student, it saves me tons of time with free 2-day shipping, and I get things I need quickly and sometimes as early as the next day, while enjoying all the free streaming services, and books that a regular prime membership has to offer for half the price. Amazon Prime Student is only available for college students, and it offers so many things to help make college life easier. This is why Amazon Prime is the no-brainer that I use to order my school supplies, my clothes, and even to watch movies in between classes. I think Amazon Prime Student is a great investment for all college students.

Summary: 
"""

# Sidebar components
with st.sidebar:
    st.title("⚙️ Configuration")
    
    with st.container(border=True):
        st.header("Model Selection")
        provider = st.selectbox('Select Provider', list_providers, key="provider_selector")
        
        models = get_model_ids(provider)
        default_model = get_model_id(provider)
        default_index = models.index(default_model) if default_model in models else 0
        
        model_id = st.selectbox('Select Model', models, index=default_index)
    
    st.button(label='Clear Session Data', on_click=clear_session_state, type="secondary")
    
    st.markdown("---")
    st.markdown("#### About")
    st.info("This app demonstrates prompt engineering techniques using various AI models from AWS Bedrock.")

# Call LLM functions
def call_llm(prompt):
    llm = Bedrock(
        model_id=model_id,
        client=bedrock_runtime,
        model_kwargs=helpers.getmodelparams(provider)
    )
    response = llm.invoke(prompt)
    return response

def call_llm_chat(prompt):
    params = helpers.getmodelparams(provider)
    params.update({'messages':[{"role": "user", "content": prompt}]})
    
    llm = BedrockChat(
        model_id=model_id, 
        client=bedrock_runtime, 
        model_kwargs=params
    )
    response = llm.invoke(prompt)
    return response.content

# Main content
st.title("🧠 AI Prompt Engineering Studio")

with st.container():
    col1, col2 = st.columns([0.6, 0.4])
    
    with col1:
        st.subheader("Elements of Effective Prompts")
        st.markdown("""
        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px;">
            For a summarization task, the prompt is a passage of text, and the model must respond with a shorter passage 
            that captures the main points of the input. Specification of the output in terms of length 
            (number of sentences or paragraphs) is helpful for this use case.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image("images/elements_of_prompts.png", use_container_width=True)

st.markdown("---")

# Prompt input area with tabs for different examples
tab1, tab2 = st.tabs(["📝 Prompt Editor", "📚 Examples"])

with tab1:
    with st.form("prompt_form"):
        text_prompt = st.text_area(
            "Enter your prompt:",
            value=default_prompt,
            height=250,
            help="Type or paste the prompt you want to submit to the model"
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            submitted = st.form_submit_button("Generate Response", type="primary", use_container_width=True)
        
        with col3:
            clear = st.form_submit_button("Clear", type="secondary", use_container_width=True)
            if clear:
                text_prompt = ""
    
    if submitted and text_prompt:
        with st.container(border=True):
            st.subheader("AI Response")
            with st.spinner("Generating response..."):
                try:
                    if provider == "Claude 3":
                        response = call_llm_chat(text_prompt)
                    else:
                        response = call_llm(text_prompt)
                    
                    st.success("Response generated successfully!")
                    st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50;">
                        {response}
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
                    st.exception(e)

with tab2:
    st.header("Example Prompts")
    
    example_tabs = st.tabs(["Summarization", "Classification", "Content Creation"])
    
    with example_tabs[0]:
        st.markdown("""
        ### Summarization Example
        
        ```
        Write a summary of a service review using two sentences. 
        
        Store: Online, Service: Shipping.
        
        Review: Amazon Prime Student is a great option for students looking to save money. Not paying for shipping is the biggest save in my opinion. As a working mom of three who is also a student, it saves me tons of time with free 2-day shipping, and I get things I need quickly and sometimes as early as the next day, while enjoying all the free streaming services, and books that a regular prime membership has to offer for half the price. Amazon Prime Student is only available for college students, and it offers so many things to help make college life easier. This is why Amazon Prime is the no-brainer that I use to order my school supplies, my clothes, and even to watch movies in between classes. I think Amazon Prime Student is a great investment for all college students.
        
        Summary:
        ```
        
        **Key elements:**
        - Clear task description
        - Output format specification (two sentences)
        - Relevant context and input data
        """)
        
        if st.button("Use this example", key="use_example_1"):
            st.session_state["text_prompt"] = default_prompt
            st.experimental_rerun()
            
    with example_tabs[1]:
        classification_example = """Classify the sentiment of this customer review as positive, neutral, or negative.

Review: "I ordered a laptop last week and it arrived two days earlier than expected. The packaging was secure and the laptop works perfectly. Very pleased with this purchase!"

Sentiment:"""
        
        st.markdown(f"""
        ### Classification Example
        
        ```
        {classification_example}
        ```
        
        **Key elements:**
        - Clear task definition (sentiment classification)
        - Limited set of response options
        - Well-formatted input
        """)
        
        if st.button("Use this example", key="use_example_2"):
            st.session_state["text_prompt"] = classification_example
            st.experimental_rerun()
            
    with example_tabs[2]:
        creation_example = """Create a product description for a new wireless noise-cancelling headphone named "SoundWave Pro" with the following features:
- 30-hour battery life
- Active noise cancellation
- Voice assistant compatibility
- Comfortable over-ear design
- Foldable for travel
- Water-resistant

The description should be approximately 100 words and target tech-savvy young professionals who travel frequently."""
        
        st.markdown(f"""
        ### Content Creation Example
        
        ```
        {creation_example}
        ```
        
        **Key elements:**
        - Detailed specifications
        - Target audience information
        - Length requirements
        - Purpose of the content
        """)
        
        if st.button("Use this example", key="use_example_3"):
            st.session_state["text_prompt"] = creation_example
            st.experimental_rerun()

# Footer
st.markdown("---")
st.caption("Built with Streamlit and AWS Bedrock")
