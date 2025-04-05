# Langchain Prompt Template Demonstrator

import streamlit as st
import uuid
import boto3
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import Bedrock
import pandas as pd
import time

# Page configuration with custom styling
st.set_page_config(
    page_title="LangChain Prompt Templates",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom CSS for modern UI
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f3f5;
        border-radius: 5px 5px 0px 0px;
        padding: 10px 16px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e7f5ff !important;
        color: #1971c2 !important;
        border-bottom: 2px solid #1971c2;
    }
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .sidebar-header {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
        color: #1971c2;
    }
    .stTextArea textarea {
        border-radius: 5px;
        border: 1px solid #dee2e6;
        font-family: 'Courier New', monospace;
    }
    .card-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .header-text {
        font-size: 24px;
        font-weight: bold;
        color: #333;
        border-left: 4px solid #1971c2;
        padding-left: 10px;
        margin-bottom: 15px;
    }
    .info-box {
        background-color: #e7f5ff;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 4px solid #339af0;
    }
    .code-box {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        margin-bottom: 15px;
        border: 1px solid #dee2e6;
        overflow-x: auto;
    }
    .output-container {
        background-color: #f1f8ff;
        border-radius: 5px;
        padding: 15px;
        border: 1px solid #d0ebff;
        margin-top: 15px;
    }
    .variable-pill {
        background-color: #e7f5ff;
        border-radius: 15px;
        padding: 2px 10px;
        margin-right: 5px;
        color: #1971c2;
        font-weight: 500;
        display: inline-block;
    }
    .template-preview {
        background-color: #f1f3f5;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #dee2e6;
        font-family: 'Courier New', monospace;
    }
    .prompt-builder {
        background-color: white;
        border-radius: 5px;
        padding: 15px;
        border: 1px solid #e9ecef;
        margin-bottom: 15px;
    }
    .example-container {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #e9ecef;
    }
    footer {
        font-size: 14px;
        color: #6c757d;
        text-align: center;
        margin-top: 30px;
        padding: 10px;
    }
    .generated-template {
        background-color: #fff9db;
        border-left: 4px solid #ffd43b;
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for new connections
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.provider = "Anthropic"
    st.session_state.temperature = 0.7
    st.session_state.max_tokens = 500
    st.session_state.top_p = 0.95
    st.session_state.current_tab = 0
    st.session_state.simple_template = "{product} features:\n{features}"
    st.session_state.output = None
    st.session_state.variables = {"product": "", "features": ""}
    st.session_state.formatted_prompt = ""
    
    # For few-shot templates
    st.session_state.few_shot_examples = [
        {"input": "Smartphone", "output": "- High resolution display\n- Long battery life\n- Fast processor\n- Multiple cameras"},
        {"input": "Laptop", "output": "- Lightweight design\n- Powerful graphics card\n- Large SSD storage\n- Backlit keyboard"}
    ]
    st.session_state.few_shot_prefix = "List product features in bullet points:\n\n"
    st.session_state.few_shot_suffix = "\nInput: {input}\nOutput:"
    st.session_state.few_shot_input_variable = ""
    st.session_state.fewshot_formatted_prompt = ""
    
    # For chain templates
    st.session_state.chain_result = ""
    st.session_state.chain_query = "What makes a good smartphone?"

# Initialize Bedrock client
@st.cache_resource
def get_bedrock_client():
    return boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

bedrock_runtime = get_bedrock_client()

# Provider and model mappings
def get_model_id(provider_name):
    model_mapping = {
        "Amazon": "amazon.titan-tg1-large",
        "Anthropic": "anthropic.claude-v2:1",
        "AI21": "ai21.j2-ultra-v1",
        "Cohere": "cohere.command-text-v14",
        "Meta": "meta.llama2-70b-chat-v1",
        "Mistral": "mistral.mixtral-8x7b-instruct-v0:1",
        "Anthropic Claude 3": "anthropic.claude-3-sonnet-20240229-v1:0"
    }
    return model_mapping.get(provider_name, "anthropic.claude-v2:1")

def get_model_ids(provider_name):
    models = []
    bedrock = boto3.client(service_name='bedrock', region_name='us-east-1')
    
    try:
        available_models = bedrock.list_foundation_models()
        for model in available_models['modelSummaries']:
            if provider_name in model['providerName']:
                models.append(model['modelId'])
    except Exception:
        # Fallback if API call fails
        if provider_name == "Anthropic":
            models = ["anthropic.claude-v2:1", "anthropic.claude-3-sonnet-20240229-v1:0"]
        elif provider_name == "Amazon":
            models = ["amazon.titan-tg1-large"]
        else:
            models = ["anthropic.claude-v2:1"]  # Default fallback
    
    return models if models else ["No models available"]

# Function to get model parameters based on provider
def get_model_params(provider_name):
    if provider_name == "Anthropic" or provider_name == "Anthropic Claude 3":
        return {
            "temperature": st.session_state.temperature,
            "max_tokens_to_sample": st.session_state.max_tokens,
            "top_p": st.session_state.top_p
        }
    elif provider_name == "Amazon":
        return {
            "temperature": st.session_state.temperature,
            "maxTokenCount": st.session_state.max_tokens,
            "topP": st.session_state.top_p
        }
    else:
        # Default parameters
        return {
            "temperature": st.session_state.temperature,
            "max_tokens": st.session_state.max_tokens,
            "top_p": st.session_state.top_p
        }

# Create LLM instance with Bedrock
def create_llm(model_id, provider_name):
    try:
        return Bedrock(
            model_id=model_id,
            client=bedrock_runtime,
            model_kwargs=get_model_params(provider_name)
        )
    except Exception as e:
        st.error(f"Error creating LLM instance: {str(e)}")
        return None

# Sidebar
with st.sidebar:
    st.markdown("<div class='sidebar-header'>🔗 LangChain Prompt Templates</div>", unsafe_allow_html=True)
    
    # Model configuration
    with st.container():
        st.markdown("### Model Configuration")
        
        provider_options = ['Anthropic', 'Amazon', 'AI21', 'Cohere', 'Meta', 'Mistral', 'Anthropic Claude 3']
        st.session_state.provider = st.selectbox(
            'Select Provider:',
            provider_options,
            index=provider_options.index(st.session_state.provider) if st.session_state.provider in provider_options else 0
        )
        
        models = get_model_ids(st.session_state.provider)
        default_model = get_model_id(st.session_state.provider)
        model_index = models.index(default_model) if default_model in models else 0
        
        model = st.selectbox(
            'Select Model:', 
            models,
            index=model_index
        )
    
    # Parameter tuning
    with st.expander("Model Parameters", expanded=False):
        st.session_state.temperature = st.slider(
            'Temperature', 
            min_value=0.0, 
            max_value=1.0, 
            value=st.session_state.temperature, 
            step=0.05,
            help="Higher values = more random, lower values = more deterministic"
        )
        
        st.session_state.top_p = st.slider(
            'Top P', 
            min_value=0.0, 
            max_value=1.0, 
            value=st.session_state.top_p, 
            step=0.05,
            help="Controls diversity of generated text"
        )
        
        st.session_state.max_tokens = st.number_input(
            'Max Tokens', 
            min_value=50, 
            max_value=4096, 
            value=st.session_state.max_tokens, 
            step=50,
            help="Maximum length of generated response"
        )
    
    # Session management
    st.markdown("---")
    st.markdown("### Session Management")
    
    if st.button('🔄 Reset Session', key='reset_session'):
        for key in list(st.session_state.keys()):
            if key != "session_id":  # Keep the same session ID but reset everything else
                del st.session_state[key]
        st.rerun()
    
    # Session info
    st.markdown(f"**Session ID:** {st.session_state.session_id[:8]}...")
    
    # Help section
    with st.expander("ℹ️ About Prompt Templates", expanded=False):
        st.markdown("""
        **LangChain Prompt Templates** provide a powerful system for:
        
        - Creating reusable prompt structures
        - Dynamically inserting variables into prompts
        - Building complex prompts from examples (few-shot learning)
        - Chaining prompts together for multi-step reasoning
        
        This tool helps you explore different template types and see how they work with LLMs.
        """)

# Main content area
st.markdown("<h1 style='text-align: center;'>LangChain Prompt Template Explorer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6c757d; margin-bottom: 30px;'>Master the art of creating effective prompts with LangChain</p>", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Simple Templates", 
    "Few-Shot Templates", 
    "Template Chains",
    "Template Best Practices"
])

# Simple Templates Tab
with tab1:
    st.markdown("<div class='header-text'>Simple Prompt Templates</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("""
    **Simple prompt templates** allow you to create reusable prompt structures with variable placeholders.
    These templates make it easy to:
    - Insert dynamic content into standardized prompts
    - Maintain consistent prompt structure across multiple requests
    - Quickly iterate on prompt designs
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Template builder
    st.markdown("### 🛠️ Template Builder")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.session_state.simple_template = st.text_area(
            "Create your prompt template (use {variable_name} for placeholders):",
            value=st.session_state.simple_template,
            height=150,
            help="Example: 'Summarize this {text} in {language}'"
        )
        
        # Extract variables from template
        import re
        variables = re.findall(r'{(\w+)}', st.session_state.simple_template)
        
        if variables:
            st.markdown("### 📝 Fill in your variables")
            
            # Create input fields for each variable
            cols = st.columns(min(3, len(variables)))
            for i, var in enumerate(variables):
                with cols[i % min(3, len(variables))]:
                    if var not in st.session_state.variables:
                        st.session_state.variables[var] = ""
                    st.session_state.variables[var] = st.text_area(
                        f"{var}:",
                        value=st.session_state.variables.get(var, ""),
                        height=100
                    )
            
            # Format the template with variables
            try:
                st.session_state.formatted_prompt = st.session_state.simple_template.format(**{k: v for k, v in st.session_state.variables.items() if k in variables})
            except KeyError as e:
                st.warning(f"Missing variable: {e}")
                st.session_state.formatted_prompt = "Error: Missing variables"
            
            # Display formatted template
            st.markdown("### 🔍 Preview")
            st.markdown("<div class='generated-template'>", unsafe_allow_html=True)
            st.text(st.session_state.formatted_prompt)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Generate response
            if st.button("🚀 Generate Response", key="simple_generate"):
                with st.spinner("Generating response..."):
                    try:
                        llm = create_llm(model, st.session_state.provider)
                        if llm:
                            st.session_state.output = llm.invoke(st.session_state.formatted_prompt)
                            
                            st.markdown("### 💬 Model Response")
                            st.markdown("<div class='output-container'>", unsafe_allow_html=True)
                            st.write(st.session_state.output)
                            st.markdown("</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")
    
    with col2:
        st.markdown("### 💡 Code Example")
        st.markdown("<div class='code-box'>", unsafe_allow_html=True)
        st.code("""
from langchain.prompts import PromptTemplate

# Define the template
template = "{product} features:\\n{features}"

# Create a PromptTemplate
prompt = PromptTemplate(
    input_variables=["product", "features"],
    template=template,
)

# Format the prompt
formatted = prompt.format(
    product="Smartphone",
    features="Please list 5 key features"
)

# Send to LLM
response = llm.invoke(formatted)
        """, language="python")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("### 🧩 Variable Placeholders")
        for var in variables:
            st.markdown(f"<span class='variable-pill'>{{{var}}}</span>", unsafe_allow_html=True)
        
        st.markdown("### 📋 Tips")
        st.info("• Keep templates reusable by using descriptive variable names\n• Use clear formatting to help the model understand structure\n• Consider adding system instructions at the beginning")

# Few-Shot Templates Tab
with tab2:
    st.markdown("<div class='header-text'>Few-Shot Prompt Templates</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("""
    **Few-shot templates** provide examples to the model before asking it to perform a task.
    This approach can significantly improve performance by:
    - Demonstrating the expected format and style
    - Showing reasoning patterns for complex tasks
    - Reducing ambiguity in the instructions
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Few-shot template builder
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📚 Example Builder")
        
        # Display existing examples
        for i, example in enumerate(st.session_state.few_shot_examples):
            with st.expander(f"Example {i+1}: {example['input']}", expanded=False):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.session_state.few_shot_examples[i]['input'] = st.text_area(
                        "Input:",
                        value=example['input'],
                        key=f"input_{i}",
                        height=100
                    )
                with col_b:
                    st.session_state.few_shot_examples[i]['output'] = st.text_area(
                        "Output:",
                        value=example['output'],
                        key=f"output_{i}",
                        height=100
                    )
                
                if st.button("Delete Example", key=f"del_{i}"):
                    st.session_state.few_shot_examples.pop(i)
                    st.rerun()
        
        # Add new example
        with st.expander("➕ Add New Example", expanded=False):
            col_a, col_b = st.columns(2)
            with col_a:
                new_input = st.text_area("Input:", key="new_input", height=100)
            with col_b:
                new_output = st.text_area("Output:", key="new_output", height=100)
            
            if st.button("Add Example", key="add_example"):
                if new_input and new_output:
                    st.session_state.few_shot_examples.append({
                        "input": new_input,
                        "output": new_output
                    })
                    st.rerun()
                else:
                    st.warning("Both input and output must be provided")
        
        # Template configuration
        st.markdown("### 🔧 Template Configuration")
        
        st.session_state.few_shot_prefix = st.text_area(
            "Prefix (instructions before examples):",
            value=st.session_state.few_shot_prefix,
            height=100
        )
        
        st.session_state.few_shot_suffix = st.text_area(
            "Suffix (format after examples, with {input} placeholder):",
            value=st.session_state.few_shot_suffix,
            height=100
        )
        
        st.session_state.few_shot_input_variable = st.text_input(
            "Your query for the model:",
            value=st.session_state.few_shot_input_variable
        )
        
        # Generate the few-shot template preview
        if st.session_state.few_shot_examples:
            try:
                # Create example template
                example_template = "Input: {input}\nOutput: {output}"
                example_prompt = PromptTemplate(
                    input_variables=["input", "output"],
                    template=example_template
                )
                
                # Create few-shot template
                few_shot_prompt = FewShotPromptTemplate(
                    examples=st.session_state.few_shot_examples,
                    example_prompt=example_prompt,
                    prefix=st.session_state.few_shot_prefix,
                    suffix=st.session_state.few_shot_suffix,
                    input_variables=["input"],
                    example_separator="\n\n"
                )
                
                # Format the prompt
                if st.session_state.few_shot_input_variable:
                    st.session_state.fewshot_formatted_prompt = few_shot_prompt.format(
                        input=st.session_state.few_shot_input_variable
                    )
                    
                    st.markdown("### 🔍 Preview")
                    st.markdown("<div class='generated-template'>", unsafe_allow_html=True)
                    st.text(st.session_state.fewshot_formatted_prompt)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    if st.button("🚀 Generate Response", key="fewshot_generate"):
                        with st.spinner("Processing with few-shot template..."):
                            try:
                                llm = create_llm(model, st.session_state.provider)
                                if llm:
                                    st.session_state.output = llm.invoke(st.session_state.fewshot_formatted_prompt)
                                    
                                    st.markdown("### 💬 Model Response")
                                    st.markdown("<div class='output-container'>", unsafe_allow_html=True)
                                    st.write(st.session_state.output)
                                    st.markdown("</div>", unsafe_allow_html=True)
                            except Exception as e:
                                st.error(f"Error generating response: {str(e)}")
                
            except Exception as e:
                st.error(f"Error creating few-shot template: {str(e)}")
                
    with col2:
        st.markdown("### 💡 Code Example")
        st.markdown("<div class='code-box'>", unsafe_allow_html=True)
        st.code("""
from langchain.prompts import FewShotPromptTemplate
from langchain.prompts import PromptTemplate

# Define example template
example_template = "Input: {input}\\nOutput: {output}"
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template=example_template
)

# Define examples
examples = [
    {"input": "Smartphone", 
     "output": "- High res display\\n- Long battery life"},
    {"input": "Laptop", 
     "output": "- Lightweight design\\n- Powerful GPU"}
]

# Create few-shot template
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="List features in bullet points:\\n\\n",
    suffix="\\nInput: {input}\\nOutput:",
    input_variables=["input"],
    example_separator="\\n\\n"
)

# Format prompt with user query
formatted = few_shot_prompt.format(input="Tablet")

# Get response from LLM
response = llm.invoke(formatted)
        """, language="python")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("### 📋 Tips for Few-Shot Learning")
        st.info("""
        • Use 3-5 diverse but consistent examples
        • Make sure examples follow the same pattern
        • Order examples from simple to complex
        • Include examples that cover edge cases
        • Keep the format consistent between examples
        """)
        
        st.markdown("### 🧩 Structure")
        st.markdown("""
        A few-shot template consists of:
        1. **Prefix**: Instructions and context
        2. **Examples**: Input/output pairs
        3. **Suffix**: Final prompt with placeholder
        """)

# Template Chains Tab
with tab3:
    st.markdown("<div class='header-text'>Template Chains</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("""
    **Template chains** combine prompt templates with LLMs to create powerful workflows.
    With LangChain's LLMChain, you can:
    - Connect templates directly to models
    - Process inputs through multiple templates
    - Build complex reasoning systems
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### ⛓️ Create a Chain")
        
        # Template for the chain
        chain_template = st.text_area(
            "Define your prompt template:",
            value="You are a product advisor specialized in technology.\n\nUser query: {query}\n\nProvide a helpful response with specific product recommendations:",
            height=150
        )
        
        # Query to process
        st.session_state.chain_query = st.text_area(
            "Your query:",
            value=st.session_state.chain_query,
            height=100
        )
        
        # Create and run the chain
        if st.button("🔄 Run Chain", key="run_chain"):
            with st.spinner("Processing chain..."):
                try:
                    # Create prompt template
                    prompt_template = PromptTemplate.from_template(chain_template)
                    
                    # Create LLM instance
                    llm = create_llm(model, st.session_state.provider)
                    
                    if llm:
                        # Create chain
                        chain = LLMChain(
                            llm=llm,
                            prompt=prompt_template,
                            verbose=True
                        )
                        
                        # Run chain
                        st.session_state.chain_result = chain.run(query=st.session_state.chain_query)
                        
                        # Display trace steps animation
                        st.markdown("### 🔄 Chain Execution Steps")
                        with st.status("Chain Process", expanded=True) as status:
                            st.write("1️⃣ Initializing chain...")
                            time.sleep(0.5)
                            st.write("2️⃣ Formatting prompt template...")
                            
                            formatted_prompt = prompt_template.format(query=st.session_state.chain_query)
                            st.code(formatted_prompt, language="text")
                            
                            time.sleep(0.5)
                            st.write("3️⃣ Sending to LLM...")
                            time.sleep(0.5)
                            st.write("4️⃣ Processing response...")
                            time.sleep(0.5)
                            status.update(label="Completed!", state="complete")
                        
                        # Show result
                        st.markdown("### 🎯 Chain Result")
                        st.markdown("<div class='output-container'>", unsafe_allow_html=True)
                        st.write(st.session_state.chain_result)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Error running chain: {str(e)}")
    
    with col2:
        st.markdown("### 💡 Code Example")
        st.markdown("<div class='code-box'>", unsafe_allow_html=True)
        st.code("""
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import Bedrock

# Create prompt template
prompt = PromptTemplate(
    input_variables=["query"],
    template="You are a product advisor.\\n\\n"
             "User query: {query}\\n\\n"
             "Provide recommendations:",
)

# Initialize LLM
llm = Bedrock(
    model_id="anthropic.claude-v2:1",
    client=bedrock_client
)

# Create the chain
chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True
)

# Run the chain
result = chain.run(query="What smartphone should I buy?")
        """, language="python")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("### 🧩 Advanced Chain Types")
        st.info("""
        Beyond simple LLMChains, LangChain offers:
        
        • **Sequential Chains**: Run multiple chains in sequence
        • **Router Chains**: Direct input to different chains based on content
        • **Memory Chains**: Keep track of conversation history
        • **ReAct Chains**: Combine reasoning and actions
        """)
        
        st.markdown("### 📊 Chain Applications")
        apps_data = pd.DataFrame({
            "Application": ["Document QA", "Chatbots", "Summarization", "Data Analysis"],
            "Chain Type": ["RetrievalQA", "ConversationChain", "MapReduceChain", "SQLDatabaseChain"]
        })
        st.table(apps_data)

# Best Practices Tab
with tab4:
    st.markdown("<div class='header-text'>Template Best Practices</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🎯 Effective Structure")
        st.markdown("""
        #### Clear Role Definition
        ```
        You are a {role} specialized in {domain}.
        ```
        
        #### Specific Instructions
        ```
        Your task is to {action} with these requirements:
        - {requirement_1}
        - {requirement_2}
        ```
        
        #### Output Formatting
        ```
        Format your response as:
        {format_description}
        ```
        """)
        
        st.markdown("### 🔄 Template Variables")
        variables_data = pd.DataFrame({
            "Variable Type": ["Content", "Instructions", "Format", "Context", "Examples"],
            "Purpose": [
                "Dynamic content to analyze or transform",
                "Specific actions or operations to perform",
                "Output structure and presentation",
                "Background information for the task",
                "Demonstrations of expected behavior"
            ]
        })
        st.table(variables_data)
    
    with col2:
        st.markdown("### 🚫 Common Mistakes")
        
        with st.expander("❌ Ambiguous Instructions"):
            st.markdown("""
            **Poor Template:**
            ```
            Please analyze {text}.
            ```
            
            **Improved Template:**
            ```
            Analyze {text} by:
            1. Identifying the main theme
            2. Listing key arguments
            3. Evaluating supporting evidence
            ```
            """)
        
        with st.expander("❌ Inconsistent Formatting"):
            st.markdown("""
            **Poor Template:**
            ```
            Example 1: input={input1}, output={output1}
            For input={input2} the output is {output2}
            ```
            
            **Improved Template:**
            ```
            Example 1:
            Input: {input1}
            Output: {output1}
            
            Example 2:
            Input: {input2}
            Output: {output2}
            ```
            """)
        
        with st.expander("❌ Information Overload"):
            st.markdown("""
            **Poor Template:**
            ```
            {20_paragraphs_of_context}
            Now answer: {question}
            ```
            
            **Improved Template:**
            ```
            Context: {concise_relevant_context}
            
            Using ONLY the information above, answer:
            Question: {question}
            ```
            """)
        
        st.markdown("### 🌟 Template Evaluation")
        st.info("""
        Test your templates with this checklist:
        
        1. **Clarity**: Are instructions specific and unambiguous?
        2. **Completeness**: Does the template include all necessary information?
        3. **Consistency**: Are examples and formatting consistent?
        4. **Effectiveness**: Does the template produce desired outputs?
        5. **Efficiency**: Is the template concise and focused?
        """)

# Footer
st.markdown("""
<footer>
    <p>LangChain Prompt Template Explorer - Learn to craft effective prompts for any LLM application</p>
</footer>
""", unsafe_allow_html=True)
