import streamlit as st
import random
from PIL import Image
import base64
from streamlit_lottie import st_lottie
import requests
import json

# Set page configuration
st.set_page_config(
    page_title="AWS AI Practitioner Knowledge Check",
    page_icon="✅",
    layout="wide"
)

# AWS Color Scheme
aws_colors = {
    "orange": "#FF9900",
    "dark_blue": "#232F3E",
    "light_blue": "#1A73E8",
    "grey": "#EAEDED",
    "white": "#FFFFFF",
    "dark_grey": "#545B64",
    "squid_ink": "#232F3E"
}

# Function to load lottie animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load animations
lottie_ai = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_w51pcehl.json")
lottie_quiz = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_ksagpj2p.json")

# Custom CSS
def apply_custom_css():
    st.markdown("""
    <style>
    .main {
        background-color: #FFFFFF;
    }
    .stApp {
        # max-width: 1200px;
        margin: 0 auto;
    }
    .css-1d391kg {
        padding: 1rem 1rem 1rem;
    }
    h1, h2, h3 {
        color: #232F3E;
    }
    .domain-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 5px solid #FF9900;
        transition: transform 0.3s ease;
    }
    .domain-card:hover {
        transform: translateY(-5px);
    }
    .aws-button {
        background-color: #FF9900;
        color: white;
        padding: 12px 24px;
        border-radius: 4px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin: 10px 0;
        border: none;
        cursor: pointer;
    }
    .aws-button:hover {
        background-color: #EC7211;
    }
    .header-container {
        background-color: #232F3E;
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 30px;
    }
    .icon-text {
        display: flex;
        align-items: center;
        margin: 10px 0;
    }
    .icon-text img {
        margin-right: 10px;
    }
    .caption {
        color: #545B64;
        font-style: italic;
        font-size: 14px;
    }
    .footer {
        text-align: center;
        padding: 20px;
        color: #545B64;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

apply_custom_css()

# Header section
st.markdown("""
    <div class='header-container'>
        <h1>AWS AI Practitioner Certification</h1>
        <h2>Knowledge Check</h2>
        <p>Test your understanding of key concepts across all AWS AI Practitioner domains</p>
    </div>
""", unsafe_allow_html=True)

# Introduction section with animation
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## Assess Your AWS AI Knowledge")
    st.markdown("""
        Welcome to the Knowledge Check section of your AWS AI Practitioner Certification course. 
        This interactive assessment will help you gauge your understanding of the key concepts 
        and prepare you for the certification exam.
        
        Each domain covers essential topics that will be tested in the AWS AI Practitioner exam.
        Complete all knowledge checks to identify areas for further review.
    """)
    
    st.markdown("""
        <div class='icon-text'>
            <img src='https://img.icons8.com/color/24/000000/checked--v1.png'/>
            <span>Comprehensive coverage of all exam domains</span>
        </div>
        <div class='icon-text'>
            <img src='https://img.icons8.com/color/24/000000/checked--v1.png'/>
            <span>Interactive quizzes with detailed explanations</span>
        </div>
        <div class='icon-text'>
            <img src='https://img.icons8.com/color/24/000000/checked--v1.png'/>
            <span>Identify your strengths and areas for improvement</span>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st_lottie(lottie_ai, height=300, key="ai_animation")

# Domain sections
st.markdown("## Certification Domains")

# Domain 1
with st.container():
    st.markdown("""
        <div class='domain-card'>
            <h3>Domain 1: Fundamentals of AI and ML</h3>
            <p>Test your understanding of AI concepts, machine learning fundamentals, and the AWS ML stack.</p>
            <p class='caption'>Topics include: ML workflows, supervised vs. unsupervised learning, AWS ML services</p>
            <a href='https://t.yikyakyuk.com/apcr-aip-quiz/Quiz_1' class='aws-button'>Start Domain 1 Assessment →</a>
        </div>
    """, unsafe_allow_html=True)

# Domain 2
with st.container():
    st.markdown("""
        <div class='domain-card'>
            <h3>Domain 2: Fundamentals of Generative AI</h3>
            <p>Explore your knowledge of generative AI technologies including large language models, transformers, and diffusion models.</p>
            <p class='caption'>Topics include: LLMs, transformer architecture, Amazon Bedrock, image generation</p>
            <a href='https://t.yikyakyuk.com/apcr-aip-quiz/Quiz_2' class='aws-button'>Start Domain 2 Assessment →</a>
        </div>
    """, unsafe_allow_html=True)

# Domain 3
with st.container():
    st.markdown("""
        <div class='domain-card'>
            <h3>Domain 3: Applications of Foundation Models</h3>
            <p>Test your ability to identify appropriate foundation model applications and implementation strategies.</p>
            <p class='caption'>Topics include: Text applications, image generation, prompt engineering, fine-tuning</p>
            <a href='https://t.yikyakyuk.com/apcr-aip-quiz/Quiz_3' class='aws-button'>Start Domain 3 Assessment →</a>
        </div>
    """, unsafe_allow_html=True)

# Domains 4 & 5
with st.container():
    st.markdown("""
        <div class='domain-card'>
            <h3>Domain 4 & 5: Responsible AI, Security, and Governance</h3>
            <p>Evaluate your understanding of AI ethics, security considerations, and governance frameworks.</p>
            <p class='caption'>Topics include: Bias mitigation, transparency, data privacy, model security</p>
            <a href='https://t.yikyakyuk.com/apcr-aip-quiz/Quiz_4' class='aws-button'>Start Domains 4 & 5 Assessment →</a>
        </div>
    """, unsafe_allow_html=True)

# Study resources section
st.markdown("## Additional Resources")
st.markdown("""
    Enhance your knowledge with these recommended resources:
""")

resource_col1, resource_col2, resource_col3 = st.columns(3)

with resource_col1:
    st.markdown("""
        <div style="padding: 15px; border-radius: 5px; border: 1px solid #EAEDED;">
            <h4>AWS Documentation</h4>
            <p>Official AWS AI and ML service documentation</p>
            <a href="https://docs.aws.amazon.com/machine-learning/" target="_blank">Explore →</a>
        </div>
    """, unsafe_allow_html=True)

with resource_col2:
    st.markdown("""
        <div style="padding: 15px; border-radius: 5px; border: 1px solid #EAEDED;">
            <h4>AWS Training</h4>
            <p>Free digital training courses on AI and ML</p>
            <a href="https://aws.amazon.com/training/learn-about/machine-learning/" target="_blank">Learn →</a>
        </div>
    """, unsafe_allow_html=True)

with resource_col3:
    st.markdown("""
        <div style="padding: 15px; border-radius: 5px; border: 1px solid #EAEDED;">
            <h4>AWS Whitepapers</h4>
            <p>In-depth whitepapers on AI best practices</p>
            <a href="https://aws.amazon.com/whitepapers/" target="_blank">Read →</a>
        </div>
    """, unsafe_allow_html=True)

# FAQ section
with st.expander("Frequently Asked Questions"):
    st.markdown("""
        **How are the knowledge checks structured?**
        
        Each domain assessment contains a series of multiple-choice questions that mirror the format of the actual AWS certification exam. After completing each assessment, you'll receive detailed explanations for each question.
        
        **How should I use these knowledge checks?**
        
        Use these assessments to identify knowledge gaps before taking the certification exam. We recommend completing all domain assessments and reviewing any areas where you score below 80%.
        
        **Can I retake the assessments?**
        
        Yes, you can retake any assessment as many times as you need. The question pool will vary each time to ensure comprehensive coverage of the domain.
        
        **How do I prepare for areas where I'm struggling?**
        
        For each domain, we provide targeted resources including documentation links, tutorial videos, and practice exercises to help strengthen your understanding.
    """)

# Footer
st.markdown("""
    <div class='footer'>
        <p>© 2023 AWS AI Practitioner Certification Course</p>
        <p>All trademarks and service marks are the property of their respective owners.</p>
    </div>
""", unsafe_allow_html=True)
