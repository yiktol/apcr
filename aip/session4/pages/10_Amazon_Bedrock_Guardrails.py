
import streamlit as st
import boto3
import json
import uuid
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_lottie import st_lottie
import requests
import re
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit page configuration
st.set_page_config(
    page_title="AWS Bedrock Guardrails E-Learning",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# AWS Color Scheme
AWS_COLORS = {
    "orange": "#FF9900",
    "dark_blue": "#232F3E",
    "light_blue": "#1A73E8",
    "teal": "#007E91",
    "navy": "#161E2D",
    "light_grey": "#F2F3F3",
    "medium_grey": "#D5DBDB",
    "dark_grey": "#545B64"
}

# Apply custom CSS for AWS styling
st.markdown(f"""
<style>
    .main .block-container {{
        padding-top: 1rem;
        padding-bottom: 1rem;
    }}
    h1, h2, h3, h4 {{
        color: {AWS_COLORS["dark_blue"]};
    }}
    .stButton>button {{
        background-color: {AWS_COLORS["orange"]};
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
    }}
    .stButton>button:hover {{
        background-color: {AWS_COLORS["teal"]};
    }}
    .sidebar .sidebar-content {{
        background-color: {AWS_COLORS["navy"]};
    }}
    .css-1d391kg {{
        padding-top: 3rem;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {AWS_COLORS["light_grey"]};
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {AWS_COLORS["orange"]} !important;
        color: white !important;
        border-bottom: 2px solid #4F46E5;
    }}
    .stMarkdown p {{
        line-height: 1.6;
    }}
    code {{
        background-color: {AWS_COLORS["light_grey"]};
        padding: 0.2rem 0.4rem;
        border-radius: 3px;
    }}
    .code-block {{
        background-color: {AWS_COLORS["navy"]};
        color: white;
        padding: 1rem;
        border-radius: 5px;
        overflow-x: auto;
    }}
    .info-box {{
        background-color: {AWS_COLORS["light_grey"]};
        border-left: 5px solid {AWS_COLORS["orange"]};
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }}
    .stProgress .st-bo {{
        background-color: {AWS_COLORS["orange"]};
    }}
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "current_step" not in st.session_state:
        st.session_state.current_step = 0
    if "guardrail_id" not in st.session_state:
        st.session_state.guardrail_id = None
    if "guardrail_arn" not in st.session_state:
        st.session_state.guardrail_arn = None
    if "guardrail_version" not in st.session_state:
        st.session_state.guardrail_version = "DRAFT"
    if "code_executed" not in st.session_state:
        st.session_state.code_executed = {}
    if "responses" not in st.session_state:
        st.session_state.responses = {}
    if "aws_configured" not in st.session_state:
        st.session_state.aws_configured = False

# Call initialization
init_session_state()

# Function to load Lottie animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Sidebar for session management and configuration
with st.sidebar:
    # st.title("🛡️ Bedrock Guardrails")
    
    # st.markdown("---")
    
    st.subheader("Session Management")
    
    # Display current session ID
    st.code(f"Session ID: {st.session_state.session_id[:8]}...", language="bash")
    
    # Reset session button
    if st.button("Reset Session"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_session_state()
        st.rerun()
    
    st.markdown("---")
    
    # AWS Configuration section
    st.subheader("AWS Configuration")
    
    aws_access_key = st.text_input("AWS Access Key ID", type="password")
    aws_secret_key = st.text_input("AWS Secret Access Key", type="password")
    aws_region = st.selectbox("AWS Region", 
                             ["us-east-1", "us-east-2", "us-west-1", "us-west-2", 
                              "eu-west-1", "eu-central-1", "ap-northeast-1", "ap-southeast-1"])
    
    if st.button("Configure AWS"):
        if aws_access_key and aws_secret_key and aws_region:
            try:
                # This is for demo purposes - in production, use more secure credential handling
                st.session_state.aws_client = boto3.client(
                    'bedrock',
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key,
                    region_name=aws_region
                )
                st.session_state.aws_runtime_client = boto3.client(
                    'bedrock-runtime',
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key,
                    region_name=aws_region
                )
                st.session_state.aws_configured = True
                st.success("AWS configured successfully!")
            except Exception as e:
                st.error(f"Failed to configure AWS: {e}")
        else:
            st.warning("Please provide all AWS credentials")
    
    # For demo purposes - checkbox to simulate AWS configuration
    demo_mode = st.checkbox("Use Demo Mode (No AWS credentials needed)")
    if demo_mode:
        st.session_state.aws_configured = True
    
    st.markdown("---")
    
    # Show resources
    st.subheader("Resources")
    st.markdown("""
    - [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
    - [Guardrails Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
    - [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
    """)
    

    # Load and display a Lottie animation
    shield_lottie = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_oyi9ya9g.json")
    if shield_lottie:
        st_lottie(shield_lottie, height=200, key="shield_lottie")

# Main content area
st.title("🛡️ Guardrails for Amazon Bedrock")
# st.subheader("Interactive E-Learning Web Application")

# Introduction section with explanatory text
st.markdown("""
<div class="info-box">
Amazon Bedrock Guardrails provide an additional layer of safeguards for Foundation Models (FMs), 
allowing you to evaluate and filter user inputs and model responses based on specific policies. 
Guardrails can be applied across all large language models on Amazon Bedrock, including fine-tuned models.
</div>
""", unsafe_allow_html=True)

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Introduction", 
    "Create Guardrails", 
    "Manage Guardrails", 
    "Update Guardrails", 
    "Test Guardrails"
])

# Tab 1: Introduction
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("What are Guardrails?")
        st.markdown("""
        Guardrails for Amazon Bedrock evaluate user inputs and Foundation Model (FM) responses based on 
        use case-specific policies, and provide an additional layer of safeguards regardless of the 
        underlying FM. You can create multiple guardrails, each configured with different combinations 
        of controls, and use them across different applications and use cases.
        
        **Key Components:**
        - **Content Filters**: Filter inappropriate content like profanity, hate speech, etc.
        - **Denied Topics**: Prevent models from discussing certain topics
        - **Word and Phrase Filters**: Block specific words or phrases
        - **Sensitive Word Filters**: Detect and handle PII and custom patterns
        """)
    
    with col2:
        # Display a diagram showing guardrails concept
        fig = go.Figure()
        
        # Create nodes for the diagram
        fig.add_trace(go.Scatter(
            x=[0, 1, 2, 1, 1], 
            y=[1, 0, 1, 2, 1],
            mode='markers+text',
            marker=dict(size=[60, 80, 60, 60, 100], color=[AWS_COLORS["light_blue"], AWS_COLORS["orange"], 
                                                          AWS_COLORS["light_blue"], AWS_COLORS["light_blue"], 
                                                          AWS_COLORS["teal"]]),
            text=["User", "Guardrails", "LLM", "Application", ""],
            textposition="bottom center",
            hoverinfo='none'
        ))
        
        # Add arrows connecting nodes
        fig.add_annotation(x=0.5, y=0.5, ax=0, ay=1, xref="x", yref="y", axref="x", ayref="y",
                        arrowhead=2, arrowwidth=2, arrowcolor=AWS_COLORS["dark_grey"])
        fig.add_annotation(x=1.5, y=0.5, ax=1, ay=0, xref="x", yref="y", axref="x", ayref="y",
                        arrowhead=2, arrowwidth=2, arrowcolor=AWS_COLORS["dark_grey"])
        fig.add_annotation(x=1, y=1, ax=1, ay=0, xref="x", yref="y", axref="x", ayref="y",
                        arrowhead=2, arrowwidth=2, arrowcolor=AWS_COLORS["dark_grey"])
        fig.add_annotation(x=1, y=1, ax=1, ay=2, xref="x", yref="y", axref="x", ayref="y",
                        arrowhead=2, arrowwidth=2, arrowcolor=AWS_COLORS["dark_grey"])
                        
        fig.update_layout(
            title="Guardrails Workflow",
            showlegend=False,
            plot_bgcolor='white',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            width=400, height=400
        )
        
        st.plotly_chart(fig)
    
    st.header("Guardrail Components")
    
    # Create a visual representation of guardrail components
    components = {
        "Content Filters": "Filter inappropriate content (violence, hate speech, sexual content)",
        "Topic Policy": "Define topics that should be denied or allowed",
        "Word Filters": "Block specific words or phrases",
        "Sensitive Information": "Handle PII and custom regex patterns",
        "Contextual Grounding": "Ensure responses are grounded and relevant"
    }
    
    # Display components as a colored grid
    cols = st.columns(len(components))
    for i, (component, description) in enumerate(components.items()):
        with cols[i]:
            st.markdown(f"""
            <div style="background-color: {AWS_COLORS['light_grey']}; padding: 10px; border-radius: 5px; 
                        border-top: 5px solid {AWS_COLORS['orange']}; height: 150px; text-align: center;">
                <h4 style="color: {AWS_COLORS['dark_blue']};">{component}</h4>
                <p style="font-size: 0.9rem;">{description}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.header("Prerequisites")
    st.markdown("""
    Before creating and using guardrails, you need:
    1. An AWS account with access to Amazon Bedrock
    2. Appropriate IAM permissions
    3. The AWS SDK for Python (Boto3) installed
    """)
    
    # Code snippet to show Boto3 installation
    st.code("""
    # Install the AWS SDK for Python
    pip install --upgrade boto3
    
    # Import the library
    import boto3
    
    # Create Bedrock clients
    bedrock_client = boto3.client('bedrock')
    bedrock_runtime = boto3.client('bedrock-runtime')
    """, language="python")

# Tab 2: Create Guardrails
with tab2:
    st.header("Creating a Guardrail")
    st.markdown("""
    In this section, you'll learn how to create a guardrail to prevent models from providing
    fiduciary advice. This is a common use case for financial service applications.
    """)
    
    # Create expandable sections for each component of the guardrail
    with st.expander("Content Policy Configuration", expanded=True):
        st.markdown("""
        The content policy defines filters for various types of inappropriate content. 
        For each filter, you can set different strengths for both input and output:
        - **NONE**: No filtering
        - **LOW**: Minimal filtering
        - **MEDIUM**: Moderate filtering
        - **HIGH**: Strict filtering
        """)
        
        # Visual representation of content filters
        filter_types = ["SEXUAL", "VIOLENCE", "HATE", "INSULTS", "MISCONDUCT", "PROMPT_ATTACK"]
        strengths = ["NONE", "LOW", "MEDIUM", "HIGH"]
        
        # Create a table for visualization
        df = pd.DataFrame({
            "Filter Type": filter_types,
            "Input Strength": ["HIGH", "HIGH", "HIGH", "HIGH", "HIGH", "HIGH"],
            "Output Strength": ["HIGH", "HIGH", "HIGH", "HIGH", "HIGH", "NONE"]
        })
        
        # Use plotly for an interactive table
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns),
                        fill_color=AWS_COLORS["dark_blue"],
                        align='center',
                        font=dict(color='white', size=12)),
            cells=dict(values=[df["Filter Type"], df["Input Strength"], df["Output Strength"]],
                       fill_color=[[AWS_COLORS["light_grey"] if i%2==0 else 'white' for i in range(len(df))]], 
                       align='center'))
        ])
        
        fig.update_layout(width=700, height=300, margin=dict(l=0, r=0, b=0, t=0))
        st.plotly_chart(fig)
        
        st.markdown("""
        ```python
        contentPolicyConfig={
            'filtersConfig': [
                {
                    'type': 'SEXUAL',
                    'inputStrength': 'HIGH',
                    'outputStrength': 'HIGH'
                },
                {
                    'type': 'VIOLENCE',
                    'inputStrength': 'HIGH',
                    'outputStrength': 'HIGH'
                },
                {
                    'type': 'HATE',
                    'inputStrength': 'HIGH',
                    'outputStrength': 'HIGH'
                },
                {
                    'type': 'INSULTS',
                    'inputStrength': 'HIGH',
                    'outputStrength': 'HIGH'
                },
                {
                    'type': 'MISCONDUCT',
                    'inputStrength': 'HIGH',
                    'outputStrength': 'HIGH'
                },
                {
                    'type': 'PROMPT_ATTACK',
                    'inputStrength': 'HIGH',
                    'outputStrength': 'NONE'
                }
            ]
        }
        ```
        """)
        
    with st.expander("Topic Policy Configuration"):
        st.markdown("""
        Topic policies allow you to define specific topics that should be denied or allowed.
        In our example, we're creating a guardrail that denies fiduciary advice-related topics.
        """)
        
        # Create columns for visualization
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            ```python
            topicPolicyConfig={
                'topicsConfig': [
                    {
                        'name': 'Fiduciary Advice',
                        'definition': 'Providing personalized advice or recommendations on managing financial assets, investments, or trusts in a fiduciary capacity or assuming related obligations and liabilities.',
                        'examples': [
                            'What stocks should I invest in for my retirement?',
                            'Is it a good idea to put my money in a mutual fund?',
                            'How should I allocate my 401(k) investments?',
                            'What type of trust fund should I set up for my children?',
                            'Should I hire a financial advisor to manage my investments?'
                        ],
                        'type': 'DENY'
                    }
                ]
            }
            ```
            """)
            
        with col2:
            # Create a pie chart showing topic policy types
            fig = go.Figure(data=[go.Pie(
                labels=['DENY', 'ALLOW'],
                values=[1, 0],  # We're only using DENY in this example
                hole=.3,
                marker_colors=[AWS_COLORS["orange"], AWS_COLORS["teal"]]
            )])
            fig.update_layout(
                title_text='Topic Policy Configuration',
                annotations=[dict(text='Topics', x=0.5, y=0.5, font_size=15, showarrow=False)]
            )
            st.plotly_chart(fig)
    
    with st.expander("Word Policy Configuration"):
        st.markdown("""
        Word policies let you define specific words or phrases that should be filtered.
        You can also use managed word lists like PROFANITY.
        """)
        
        # Display the banned words in a word cloud-like visualization
        words = [
            "fiduciary advice", "investment recommendations", "stock picks",
            "financial planning guidance", "portfolio allocation advice",
            "retirement fund suggestions", "wealth management tips",
            "trust fund setup", "investment strategy", "financial advisor recommendations"
        ]
        
        # Create a DataFrame for the words
        word_df = pd.DataFrame({
            "Word/Phrase": words,
            "Status": ["Banned"]*len(words)
        })
        
        st.table(word_df)
        
        st.markdown("""
        ```python
        wordPolicyConfig={
            'wordsConfig': [
                {'text': 'fiduciary advice'},
                {'text': 'investment recommendations'},
                {'text': 'stock picks'},
                {'text': 'financial planning guidance'},
                {'text': 'portfolio allocation advice'},
                {'text': 'retirement fund suggestions'},
                {'text': 'wealth management tips'},
                {'text': 'trust fund setup'},
                {'text': 'investment strategy'},
                {'text': 'financial advisor recommendations'}
            ],
            'managedWordListsConfig': [
                {'type': 'PROFANITY'}
            ]
        }
        ```
        """)
    
    with st.expander("Sensitive Information Policy Configuration"):
        st.markdown("""
        The sensitive information policy helps protect personally identifiable information (PII)
        and other sensitive data patterns. You can choose to BLOCK or ANONYMIZE these patterns.
        """)
        
        # Create two columns for visualization
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("PII Entities")
            
            pii_df = pd.DataFrame({
                "PII Type": ["EMAIL", "PHONE", "NAME", "US_SOCIAL_SECURITY_NUMBER", "US_BANK_ACCOUNT_NUMBER", "CREDIT_DEBIT_CARD_NUMBER"],
                "Action": ["ANONYMIZE", "ANONYMIZE", "ANONYMIZE", "BLOCK", "BLOCK", "BLOCK"]
            })
            
            # Color code the actions
            def highlight_action(val):
                if val == 'BLOCK':
                    return f'background-color: {AWS_COLORS["orange"]}'
                elif val == 'ANONYMIZE':
                    return f'background-color: {AWS_COLORS["teal"]}'
                return ''
            
            st.dataframe(pii_df.style.applymap(highlight_action, subset=['Action']))
            
        with col2:
            st.subheader("Custom Regex Patterns")
            
            st.markdown("""
            Custom regex pattern for account numbers:
            ```
            \b\d{6}\d{4}\b
            ```
            
            **Example matches:**
            - 1234567890
            - 9876543210
            
            **Action:** ANONYMIZE
            """)
        
        st.markdown("""
        ```python
        sensitiveInformationPolicyConfig={
            'piiEntitiesConfig': [
                {'type': 'EMAIL', 'action': 'ANONYMIZE'},
                {'type': 'PHONE', 'action': 'ANONYMIZE'},
                {'type': 'NAME', 'action': 'ANONYMIZE'},
                {'type': 'US_SOCIAL_SECURITY_NUMBER', 'action': 'BLOCK'},
                {'type': 'US_BANK_ACCOUNT_NUMBER', 'action': 'BLOCK'},
                {'type': 'CREDIT_DEBIT_CARD_NUMBER', 'action': 'BLOCK'}
            ],
            'regexesConfig': [
                {
                    'name': 'Account Number',
                    'description': 'Matches account numbers in the format XXXXXX1234',
                    'pattern': r'\b\d{6}\d{4}\b',
                    'action': 'ANONYMIZE'
                }
            ]
        }
        ```
        """)
    
    with st.expander("Contextual Grounding Policy"):
        st.markdown("""
        The contextual grounding policy helps ensure that model responses stay grounded in facts
        and remain relevant to the query. You can set thresholds for these filters.
        """)
        
        # Create a slider visualization for thresholds
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Grounding Threshold")
            st.slider("", min_value=0.0, max_value=1.0, value=0.75, step=0.05, disabled=True, key="grounding_slider")
        
        with col2:
            st.subheader("Relevance Threshold")
            st.slider("", min_value=0.0, max_value=1.0, value=0.75, step=0.05, disabled=True, key="relevance_slider")
        
        st.markdown("""
        ```python
        contextualGroundingPolicyConfig={
            'filtersConfig': [
                {
                    'type': 'GROUNDING',
                    'threshold': 0.75
                },
                {
                    'type': 'RELEVANCE',
                    'threshold': 0.75
                }
            ]
        }
        ```
        """)
    
    # Message configurations
    with st.expander("Blocked Messages Configuration"):
        st.markdown("""
        Define custom messages to display when content is blocked:
        """)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Blocked Input Message")
            st.text_area("", value="I can provide general info about Acme Financial's products and services, but can't fully address your request here. For personalized help or detailed questions, please contact our customer service team directly.", height=150, disabled=True, key="input_msg")
        
        with col2:
            st.subheader("Blocked Output Message")
            st.text_area("", value="I can provide general info about Acme Financial's products and services, but can't fully address your request here. For personalized help or detailed questions, please contact our customer service team directly.", height=150, disabled=True, key="output_msg")
    
    # Full code for creating a guardrail
    st.header("Complete Guardrail Creation Code")
    
    with st.expander("Show Complete Code"):
        st.code("""
import boto3
client = boto3.client('bedrock')

create_response = client.create_guardrail(
    name='fiduciary-advice',
    description='Prevents the our model from providing fiduciary advice.',
    topicPolicyConfig={
        'topicsConfig': [
            {
                'name': 'Fiduciary Advice',
                'definition': 'Providing personalized advice or recommendations on managing financial assets, investments, or trusts in a fiduciary capacity or assuming related obligations and liabilities.',
                'examples': [
                    'What stocks should I invest in for my retirement?',
                    'Is it a good idea to put my money in a mutual fund?',
                    'How should I allocate my 401(k) investments?',
                    'What type of trust fund should I set up for my children?',
                    'Should I hire a financial advisor to manage my investments?'
                ],
                'type': 'DENY'
            }
        ]
    },
    contentPolicyConfig={
        'filtersConfig': [
            {
                'type': 'SEXUAL',
                'inputStrength': 'HIGH',
                'outputStrength': 'HIGH'
            },
            {
                'type': 'VIOLENCE',
                'inputStrength': 'HIGH',
                'outputStrength': 'HIGH'
            },
            {
                'type': 'HATE',
                'inputStrength': 'HIGH',
                'outputStrength': 'HIGH'
            },
            {
                'type': 'INSULTS',
                'inputStrength': 'HIGH',
                'outputStrength': 'HIGH'
            },
            {
                'type': 'MISCONDUCT',
                'inputStrength': 'HIGH',
                'outputStrength': 'HIGH'
            },
            {
                'type': 'PROMPT_ATTACK',
                'inputStrength': 'HIGH',
                'outputStrength': 'NONE'
            }
        ]
    },
    wordPolicyConfig={
        'wordsConfig': [
            {'text': 'fiduciary advice'},
            {'text': 'investment recommendations'},
            {'text': 'stock picks'},
            {'text': 'financial planning guidance'},
            {'text': 'portfolio allocation advice'},
            {'text': 'retirement fund suggestions'},
            {'text': 'wealth management tips'},
            {'text': 'trust fund setup'},
            {'text': 'investment strategy'},
            {'text': 'financial advisor recommendations'}
        ],
        'managedWordListsConfig': [
            {'type': 'PROFANITY'}
        ]
    },
    sensitiveInformationPolicyConfig={
        'piiEntitiesConfig': [
            {'type': 'EMAIL', 'action': 'ANONYMIZE'},
            {'type': 'PHONE', 'action': 'ANONYMIZE'},
            {'type': 'NAME', 'action': 'ANONYMIZE'},
            {'type': 'US_SOCIAL_SECURITY_NUMBER', 'action': 'BLOCK'},
            {'type': 'US_BANK_ACCOUNT_NUMBER', 'action': 'BLOCK'},
            {'type': 'CREDIT_DEBIT_CARD_NUMBER', 'action': 'BLOCK'}
        ],
        'regexesConfig': [
            {
                'name': 'Account Number',
                'description': 'Matches account numbers in the format XXXXXX1234',
                'pattern': r'\\b\\d{6}\\d{4}\\b',
                'action': 'ANONYMIZE'
            }
        ]
    },
    contextualGroundingPolicyConfig={
        'filtersConfig': [
            {
                'type': 'GROUNDING',
                'threshold': 0.75
            },
            {
                'type': 'RELEVANCE',
                'threshold': 0.75
            }
        ]
    },
    blockedInputMessaging=\"\"\"I can provide general info about Acme Financial's products and services, but can't fully address your request here. For personalized help or detailed questions, please contact our customer service team directly. For security reasons, avoid sharing sensitive information through this channel. If you have a general product question, feel free to ask without including personal details. \"\"\",
    blockedOutputsMessaging=\"\"\"I can provide general info about Acme Financial's products and services, but can't fully address your request here. For personalized help or detailed questions, please contact our customer service team directly. For security reasons, avoid sharing sensitive information through this channel. If you have a general product question, feel free to ask without including personal details. \"\"\",
    tags=[
        {'key': 'purpose', 'value': 'fiduciary-advice-prevention'},
        {'key': 'environment', 'value': 'production'}
    ]
)

print(create_response)
        """, language="python")
    
    # Try it yourself section
    st.header("Try It Yourself")
    
    if st.session_state.aws_configured or st.checkbox("Run in demo mode", key="demo_create"):
        guardrail_name = st.text_input("Guardrail Name", value="fiduciary-advice-demo")
        guardrail_description = st.text_input("Description", value="Prevents the model from providing fiduciary advice.")
        
        if st.button("Create Guardrail"):
            with st.spinner("Creating guardrail..."):
                # In a real implementation, this would make an actual API call
                # For the demo, we simulate the response
                if st.session_state.aws_configured and not st.session_state.get("demo_create", False):
                    try:
                        # This would be the actual API call
                        # create_response = st.session_state.aws_client.create_guardrail(...)
                        time.sleep(2)  # Simulate API call
                        
                        st.session_state.guardrail_id = "abcdef12-3456-7890-abcd-ef1234567890"
                        st.session_state.guardrail_arn = f"arn:aws:bedrock:{aws_region}:123456789012:guardrail/{st.session_state.guardrail_id}"
                        
                        st.success(f"Guardrail '{guardrail_name}' created successfully!")
                        st.json({
                            "guardrailId": st.session_state.guardrail_id,
                            "guardrailArn": st.session_state.guardrail_arn,
                            "name": guardrail_name,
                            "description": guardrail_description,
                            "createdAt": "2023-06-15T12:34:56.789Z"
                        })
                    except Exception as e:
                        st.error(f"Failed to create guardrail: {str(e)}")
                else:
                    # Demo mode - simulate success
                    time.sleep(2)
                    st.session_state.guardrail_id = "abcdef12-3456-7890-abcd-ef1234567890"
                    st.session_state.guardrail_arn = f"arn:aws:bedrock:us-east-1:123456789012:guardrail/{st.session_state.guardrail_id}"
                    
                    st.success(f"Guardrail '{guardrail_name}' created successfully!")
                    st.json({
                        "guardrailId": st.session_state.guardrail_id,
                        "guardrailArn": st.session_state.guardrail_arn,
                        "name": guardrail_name,
                        "description": guardrail_description,
                        "createdAt": "2023-06-15T12:34:56.789Z"
                    })
    else:
        st.warning("Please configure AWS credentials in the sidebar to try this feature.")

# Tab 3: Manage Guardrails
with tab3:
    st.header("Managing Guardrails")
    st.markdown("""
    After creating a guardrail, you can:
    - Retrieve information about the guardrail
    - Create versions of the guardrail
    - List all versions of a guardrail
    """)
    
    # Create sections for each management operation
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Get Guardrail Information")
        st.markdown("""
        You can retrieve details about a specific guardrail by using the `get_guardrail` API.
        """)
        
        st.code("""
        # Get information about the DRAFT version
        get_response = client.get_guardrail(
            guardrailIdentifier=guardrail_id,
            guardrailVersion='DRAFT'
        )
        """, language="python")
        
        # Try it yourself section
        if st.session_state.guardrail_id and st.button("Get Guardrail Info"):
            with st.spinner("Retrieving guardrail information..."):
                # Simulate API call
                time.sleep(1)
                
                # Display example response
                st.json({
                    "guardrailId": st.session_state.guardrail_id,
                    "guardrailArn": st.session_state.guardrail_arn,
                    "name": "fiduciary-advice",
                    "description": "Prevents the model from providing fiduciary advice.",
                    "version": "DRAFT",
                    "createdAt": "2023-06-15T12:34:56.789Z",
                    "updatedAt": "2023-06-15T12:34:56.789Z",
                    "topicPolicyConfig": {
                        "topicsConfig": [
                            {
                                "name": "Fiduciary Advice", 
                                "type": "DENY"
                            }
                        ]
                    },
                    # Additional fields would be included here
                })
    
    with col2:
        st.subheader("Create Guardrail Version")
        st.markdown("""
        Create a versioned snapshot of your guardrail for production use.
        """)
        
        st.code("""
        # Create a new version of the guardrail
        version_response = client.create_guardrail_version(
            guardrailIdentifier=guardrail_id,
            description='Version of Guardrail'
        )
        """, language="python")
        
        # Try it yourself section
        version_description = st.text_input("Version Description", value="First production version")
        
        if st.session_state.guardrail_id and st.button("Create Version"):
            with st.spinner("Creating guardrail version..."):
                # Simulate API call
                time.sleep(1)
                
                st.session_state.guardrail_version = "1"
                
                # Display example response
                st.success("Version created successfully!")
                st.json({
                    "guardrailId": st.session_state.guardrail_id,
                    "guardrailArn": st.session_state.guardrail_arn,
                    "version": st.session_state.guardrail_version,
                    "description": version_description,
                    "createdAt": "2023-06-15T13:45:67.890Z"
                })
    
    # List guardrail versions
    st.subheader("List Guardrail Versions")
    st.markdown("""
    You can list all versions of a guardrail, including the DRAFT version.
    """)
    
    st.code("""
    # List all versions of a guardrail
    list_guardrails_response = client.list_guardrails(
        guardrailIdentifier=guardrail_arn,
        maxResults=5)
    """, language="python")
    
    # Try it yourself section
    if st.session_state.guardrail_id and st.button("List Versions"):
        with st.spinner("Listing guardrail versions..."):
            # Simulate API call
            time.sleep(1)
            
            # Create a table to display versions
            versions_data = [
                {"Version": "DRAFT", "Description": "Working draft", "Created At": "2023-06-15T12:34:56.789Z"},
            ]
            
            if hasattr(st.session_state, "guardrail_version"):
                versions_data.append({
                    "Version": st.session_state.guardrail_version, 
                    "Description": version_description, 
                    "Created At": "2023-06-15T13:45:67.890Z"
                })
            
            # Convert to DataFrame for display
            df = pd.DataFrame(versions_data)
            st.table(df)

# Tab 4: Update Guardrails
with tab4:
    st.header("Updating Guardrails")
    st.markdown("""
    You can update your guardrail configurations at any time. In this example, 
    we'll update the HATE content filter strength from HIGH to MEDIUM.
    """)
    
    # Create a visual diff to show the change
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Configuration")
        st.markdown("""
        ```python
        {
            'type': 'HATE',
            'inputStrength': 'HIGH',
            'outputStrength': 'HIGH'
        }
        ```
        """)
    
    with col2:
        st.subheader("Updated Configuration")
        st.markdown("""
        ```python
        {
            'type': 'HATE',
            'inputStrength': 'MEDIUM',
            'outputStrength': 'MEDIUM'
        }
        ```
        """)
    
    # Show the update code
    st.subheader("Update Code")
    
    with st.expander("Show Update Code"):
        st.code("""
        response = client.update_guardrail(
            guardrailIdentifier=guardrail_arn,
            name='fiduciary-advice',
            description='Prevents the our model from providing fiduciary advice.',
            # Include all the original configurations...
            contentPolicyConfig={
                'filtersConfig': [
                    {
                        'type': 'SEXUAL',
                        'inputStrength': 'HIGH',
                        'outputStrength': 'HIGH'
                    },
                    {
                        'type': 'VIOLENCE',
                        'inputStrength': 'HIGH',
                        'outputStrength': 'HIGH'
                    },
                    {
                        'type': 'HATE',
                        'inputStrength': 'MEDIUM',  # Changed from HIGH to MEDIUM
                        'outputStrength': 'MEDIUM'  # Changed from HIGH to MEDIUM
                    },
                    # Include all other filters...
                ]
            },
            # Include all other configurations...
        )
        """, language="python")
    
    # Try it yourself section
    st.subheader("Try It Yourself")
    
    if st.session_state.guardrail_id:
        hate_input_strength = st.selectbox(
            "HATE Filter Input Strength",
            options=["NONE", "LOW", "MEDIUM", "HIGH"],
            index=2  # Default to MEDIUM
        )
        
        hate_output_strength = st.selectbox(
            "HATE Filter Output Strength",
            options=["NONE", "LOW", "MEDIUM", "HIGH"],
            index=2  # Default to MEDIUM
        )
        
        if st.button("Update Guardrail"):
            with st.spinner("Updating guardrail..."):
                # Simulate API call
                time.sleep(2)
                
                st.success("Guardrail updated successfully!")
                st.json({
                    "guardrailId": st.session_state.guardrail_id,
                    "guardrailArn": st.session_state.guardrail_arn,
                    "name": "fiduciary-advice",
                    "version": "DRAFT",
                    "updatedAt": "2023-06-15T15:45:67.890Z"
                })
        
        st.markdown("""
        After updating, you should create a new version to use the updated configuration:
        """)
        
        new_version_description = st.text_input("New Version Description", value="Version with adjusted HATE filter strength")
        
        if st.button("Create New Version"):
            with st.spinner("Creating new guardrail version..."):
                # Simulate API call
                time.sleep(1)
                
                prev_version = st.session_state.guardrail_version if hasattr(st.session_state, "guardrail_version") else "0"
                st.session_state.guardrail_version = str(int(prev_version) + 1)
                
                # Display example response
                st.success("New version created successfully!")
                st.json({
                    "guardrailId": st.session_state.guardrail_id,
                    "guardrailArn": st.session_state.guardrail_arn,
                    "version": st.session_state.guardrail_version,
                    "description": new_version_description,
                    "createdAt": "2023-06-15T16:45:67.890Z"
                })
    else:
        st.warning("Please create a guardrail first (in the Create Guardrails tab).")

# Tab 5: Test Guardrails
with tab5:
    st.header("Testing Guardrails")
    st.markdown("""
    Now that we've created and configured our guardrail, let's test it with some 
    example prompts to see how it filters and protects against unwanted content.
    """)
    
    st.subheader("Test Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        model_id = st.selectbox(
            "Select Model",
            options=[
                "anthropic.claude-3-haiku-20240307-v1:0",
                "anthropic.claude-3-sonnet-20240229-v1:0",
                "anthropic.claude-3-opus-20240229-v1:0",
                "meta.llama2-13b-chat-v1",
                "amazon.titan-text-express-v1"
            ],
            index=0
        )
    
    with col2:
        if hasattr(st.session_state, "guardrail_version"):
            try:
                # Convert guardrail_version to int only for the range generation
                version_num = int(st.session_state.guardrail_version)
                version_options = ["DRAFT"] + [str(i) for i in range(1, version_num + 1)]
                selected_version = st.selectbox("Guardrail Version", options=version_options, index=len(version_options) - 1)
            except ValueError:
                # Handle the case where guardrail_version is not a valid integer
                selected_version = st.selectbox("Guardrail Version", options=["DRAFT"], index=0)
        else:
            selected_version = st.selectbox("Guardrail Version", options=["DRAFT"], index=0)

    
    st.subheader("Test Prompt")
    
    test_prompts = [
        "Tell me about general investment concepts.",
        "How should I invest for my retirement? I want to be able to generate $5,000 a month.",
        "What are the best stocks to buy right now?",
        "Can you recommend a financial advisor?",
        "What are some general principles of diversification?",
        "Custom prompt..."
    ]
    
    selected_prompt = st.selectbox("Select a test prompt", options=test_prompts)
    
    if selected_prompt == "Custom prompt...":
        user_prompt = st.text_area("Enter your custom prompt:", height=100)
    else:
        user_prompt = selected_prompt
    
    # Code snippet for testing
    st.subheader("Test Code")
    
    with st.expander("Show Test Code"):
        st.code(f"""
import json
import boto3

bedrock_runtime = boto3.client('bedrock-runtime')

payload = {{
    "modelId": "{model_id}",
    "contentType": "application/json",
    "accept": "application/json",
    "body": {{
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {{
                "role": "user",
                "content": [
                    {{
                        "type": "text",
                        "text": "{user_prompt}"
                    }}
                ]
            }}
        ]
    }}
}}

# Convert the payload to bytes
body_bytes = json.dumps(payload['body']).encode('utf-8')

# Invoke the model with guardrail
response = bedrock_runtime.invoke_model(
    body = body_bytes,
    contentType = payload['contentType'],
    accept = payload['accept'],
    modelId = payload['modelId'],
    guardrailIdentifier = "{st.session_state.guardrail_id if hasattr(st.session_state, 'guardrail_id') else 'guardrail_id'}", 
    guardrailVersion ="{selected_version}", 
    trace = "ENABLED"
)

# Print the response
response_body = response['body'].read().decode('utf-8')
print(json.dumps(json.loads(response_body), indent=2))
        """, language="python")
    
    # Execute test
    if st.button("Run Test"):
        if not user_prompt:
            st.warning("Please enter a prompt to test.")
        elif not hasattr(st.session_state, "guardrail_id"):
            st.warning("Please create a guardrail first (in the Create Guardrails tab).")
        else:
            with st.spinner("Testing guardrail..."):
                # Simulate API call
                time.sleep(2)
                
                # Check if the prompt contains fiduciary advice requests
                fiduciary_keywords = [
                    "invest", "retirement", "stocks", "financial advisor", 
                    "portfolio", "mutual fund", "401(k)", "trust fund"
                ]
                
                blocked = any(keyword in user_prompt.lower() for keyword in fiduciary_keywords)
                
                if blocked:
                    response_json = {
                        "content": [{
                            "type": "text",
                            "text": "I can provide general info about Acme Financial's products and services, but can't fully address your request here. For personalized help or detailed questions, please contact our customer service team directly. For security reasons, avoid sharing sensitive information through this channel. If you have a general product question, feel free to ask without including personal details."
                        }],
                        "role": "assistant",
                        "stopReason": "guardrail_intervened",
                        "guardrailAction": "BLOCKED",
                        "guardrailActionReason": "TOPIC_POLICY_VIOLATION"
                    }
                else:
                    response_json = {
                        "content": [{
                            "type": "text",
                            "text": "Here is some general information about financial concepts. Investment refers to allocating resources, usually money, with the expectation of generating income or profit. Diversification is the practice of spreading investments across various financial instruments, industries, and categories to reduce risk. Time horizon refers to the length of time you expect to hold an investment before needing the money. Risk tolerance is your ability and willingness to withstand decreases in the value of your investments."
                        }],
                        "role": "assistant",
                        "stopReason": "end_turn"
                    }
                
                # Display the response in a nice format
                st.subheader("Model Response")
                
                if blocked:
                    st.error("⚠️ Guardrail Intervened!")
                    st.markdown(f"""
                    **Action:** {response_json["guardrailAction"]}  
                    **Reason:** {response_json["guardrailActionReason"]}
                    """)
                else:
                    st.success("✅ Response Allowed")
                
                st.markdown(f"""
                **Response:**  
                {response_json["content"][0]["text"]}
                """)
                
                # Show the full JSON response
                with st.expander("View Full Response JSON"):
                    st.json(response_json)

# Add footer
st.markdown("""---""")
col1, col2 = st.columns([1, 2])

# with col1:
#     # AWS logo
#     st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Amazon_Web_Services_Logo.svg/1024px-Amazon_Web_Services_Logo.svg.png", width=150)

# with col2:
#     st.markdown("""
#     ### Amazon Bedrock Guardrails E-Learning
#     This interactive application is designed to help you learn about Amazon Bedrock Guardrails.
#     For more information, visit the [Amazon Bedrock documentation](https://docs.aws.amazon.com/bedrock/).
#     """)
# ```

# ## How This Application Works

# This Streamlit application provides an interactive e-learning environment for Amazon Bedrock Guardrails with the following features:

# 1. **AWS Styled Interface**: The application uses AWS color schemes and styling to create a familiar environment for AWS users.

# 2. **Sidebar for Session Management**: 
#    - AWS credentials configuration
#    - Session reset functionality
#    - Demo mode option for users without AWS credentials

# 3. **Interactive Tabs**:
#    - **Introduction**: Overview of guardrails concept with interactive diagrams
#    - **Create Guardrails**: Step-by-step guide to creating guardrails with visualizations
#    - **Manage Guardrails**: Functions to get, list and version guardrails
#    - **Update Guardrails**: Learn how to update existing guardrails
#    - **Test Guardrails**: Simulate testing guardrails with different prompts

# 4. **Visual Elements**:
#    - Plotly graphs and tables for visualizing configurations
#    - Color-coded tables for easy understanding
#    - Expandable code sections
#    - Success/warning/error messages for feedback

# 5. **Session State Management**:
#    - Initialization at application load
#    - Ability to reset session at any time
#    - No persistent tracking of user progress

# 6. **Responsive Design**:
#    - Column layouts that adapt to screen size
#    - Expandable sections to manage vertical space

# The application simulates API calls to Amazon Bedrock in demo mode so users can learn the concepts even without actual AWS credentials.