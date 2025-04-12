
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
import seaborn as sns
from PIL import Image
import base64

# Set page configuration
st.set_page_config(
    page_title="AWS ML Engineer - Domain 2 Training",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'quiz_score' not in st.session_state:
    st.session_state['quiz_score'] = 0
if 'quiz_attempted' not in st.session_state:
    st.session_state['quiz_attempted'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'answers' not in st.session_state:
    st.session_state['answers'] = {}

# Custom CSS for styling with AWS Color Scheme
st.markdown("""
<style>
    /* AWS Color Scheme */
    :root {
        --aws-orange: #FF9900;
        --aws-blue: #232F3E;
        --aws-light-blue: #1E88E5;
        --aws-light-gray: #F8F9FA;
        --aws-dark-gray: #545B64;
    }
    
    .main-title {
        color: var(--aws-blue);
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
        border-bottom: 2px solid var(--aws-orange);
        padding-bottom: 10px;
    }
    
    .section-title {
        color: var(--aws-blue);
        font-size: 24px;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    
    .subsection-title {
        color: var(--aws-blue);
        font-size: 20px;
        font-weight: bold;
        margin-top: 15px;
    }
    
    .aws-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #E0E0E0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .orange-highlight {
        color: var(--aws-orange);
        font-weight: bold;
    }
    
    .important-note {
        background-color: #FFEFD5;
        border-left: 5px solid var(--aws-orange);
        padding: 10px 15px;
        margin: 15px 0;
        border-radius: 5px;
    }
    
    .code-box {
        background-color: var(--aws-light-gray);
        padding: 10px;
        border-radius: 5px;
        border-left: 3px solid var(--aws-orange);
        font-family: monospace;
        margin: 10px 0;
        overflow-x: auto;
    }
    
    .infobox {
        background-color: #E1F5FE;
        border-left: 5px solid var(--aws-light-blue);
        padding: 10px 15px;
        margin: 15px 0;
        border-radius: 5px;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: var(--aws-orange);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 24px;
        font-weight: bold;
    }
    
    .stButton>button:hover {
        background-color: #E68A00;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background-color: var(--aws-orange);
    }
    
    /* Custom expander styling */
    .streamlit-expanderHeader {
        background-color: var(--aws-light-gray);
        border-radius: 5px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        font-size: 1rem;
        border-radius: 5px 5px 0 0;
        background-color: #EEEEEE;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--aws-orange);
        color: white;
        font-weight: bold;
    }
    
    /* Highlight row styling */
    .highlight-row {
        background-color: #FFE4B5;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Functions for formatted content
def main_title(text):
    st.markdown(f'<div class="main-title">{text}</div>', unsafe_allow_html=True)

def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)

def subsection_title(text):
    st.markdown(f'<div class="subsection-title">{text}</div>', unsafe_allow_html=True)

def aws_card(content):
    st.markdown(f'<div class="aws-card">{content}</div>', unsafe_allow_html=True)

def important_note(text):
    st.markdown(f'<div class="important-note">{text}</div>', unsafe_allow_html=True)

def info_box(text):
    st.markdown(f'<div class="infobox">{text}</div>', unsafe_allow_html=True)

def reset_session():
    """Reset all session state variables"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state['quiz_score'] = 0
    st.session_state['quiz_attempted'] = False
    st.session_state['username'] = ""
    st.session_state['answers'] = {}
    st.rerun()

# Sidebar for session management
with st.sidebar:
    st.image("https://d1.awsstatic.com/training-and-certification/certification-badges/AWS-Certified-Machine-Learning-Specialty_badge.c17197d13b33ec8b9c62causagesh2bfca7df511cb2eb98c8becce5121d45ff.png", width=150)
    st.markdown("### AWS ML Engineer - Associate")
    st.markdown("#### Domain 2: ML Model Development")
    
    # Session management
    if st.session_state['username']:
        st.success(f"Welcome, {st.session_state['username']}!")
    else:
        username = st.text_input("Enter your name to begin:")
        if username:
            st.session_state['username'] = username
            st.rerun()
    
    st.markdown("---")
    
    # Reset session button
    if st.button("Reset Session 🔄"):
        reset_session()
    
    # Resources
    st.markdown("---")
    st.markdown("### Resources")
    st.markdown("""
    - [AWS ML Documentation](https://docs.aws.amazon.com/machine-learning)
    - [AWS SageMaker Developer Guide](https://docs.aws.amazon.com/sagemaker)
    - [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock)
    - [ML Engineer Certification](https://aws.amazon.com/certification/certified-machine-learning-specialty)
    """)

# Content rendering functions
def render_introduction():
    main_title("AWS Partner Certification Readiness: ML Engineer - Associate")
    st.markdown("## Session 2: Domain 2 - ML Model Development")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Welcome to Session 2 of the AWS Partner Certification Readiness program for ML Engineer - Associate certification.
        
        In this session, we will focus on Domain 2: ML Model Development, covering:
        
        - Task Statement 2.1: Choose a modeling approach
        - Task Statement 2.2: Train and refine models
        
        This interactive module will help you understand key concepts about machine learning models, development approaches,
        and refinement techniques on AWS.
        """)
        
        info_box("""
        <b>Learning Objectives:</b><br>
        • Understand the ML lifecycle and where model development fits<br>
        • Learn about different modeling approaches on AWS<br>
        • Understand hyperparameters and tuning techniques<br>
        • Explore model training and refinement techniques<br>
        • Learn about Amazon Bedrock and Foundation Models
        """)
    
    with col2:
        st.image("https://d1.awsstatic.com/re19/centauri2/Diagram_machine-learning-on-aws-services-2.0e6267be7d34ce5d6305be9a3debf1268a460947.png", caption="AWS ML Services")
    
    st.markdown("### Session Roadmap")
    
    roadmap_data = {
        'Sessions': ['Sessions 1 & 2', 'Sessions 3 & 4', 'Sessions 5 & 6', 'Sessions 7 & 8', 'Sessions 9 & 10'],
        'Focus': ['Domain 1: Data Preparation for ML', 'Domain 2: ML Model Development', 'Domain 2: ML Model Development',
                 'Domain 3: Deployment and Orchestration', 'Domain 4: Monitoring, Maintenance, and Security']
    }
    
    roadmap_df = pd.DataFrame(roadmap_data)
    
    # Apply custom styling to highlight the current session
    def highlight_current_row(row):
        styles = [''] * len(row)
        if row['Sessions'] == 'Sessions 3 & 4':
            styles = ['background-color: #FFE4B5; font-weight: bold'] * len(row)
        return styles
    
    # Display the roadmap with styled highlight
    st.dataframe(roadmap_df.style.apply(highlight_current_row, axis=1), use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("""
    ### Weekly Digital Training Curriculum
    
    Make sure you go through this week's training content:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### AWS Skill Builder Learning Plan Courses")
        st.markdown("""
        - AWS Glue Getting Started
        - Fundamentals of Machine Learning and Artificial Intelligence
        - Planning a Machine Learning Project
        - Introduction to Amazon SageMaker
        - Amazon Bedrock Getting Started
        """)
    
    with col2:
        st.markdown("#### Enhanced Exam Prep Plan (Optional)")
        st.markdown("""
        - Continue AWS Cloud Quest: Machine Learning
        - Complete – Domain 1 Courses
        """)

def render_ml_lifecycle():
    main_title("Machine Learning Lifecycle")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        The machine learning lifecycle consists of several key phases that guide the development and deployment of ML models.
        Understanding this lifecycle helps you approach ML projects systematically.
        """)
        
        # ML Lifecycle diagram
        lifecycle_fig, ax = plt.subplots(figsize=(10, 2))
        lifecycle_stages = ['Setup', 'Data Processing', 'Model Development', 'Deployment and Inference', 'Monitoring']
        ax.axis('off')
        for i, stage in enumerate(lifecycle_stages):
            if stage == 'Model Development':
                color = '#FF9900'  # AWS Orange for the current stage
                weight = 'bold'
            else:
                color = '#232F3E'  # AWS Blue
                weight = 'normal'
            ax.text(i/len(lifecycle_stages) + 0.1, 0.5, stage, ha='center', va='center', 
                   fontsize=12, color=color, fontweight=weight)
            if i < len(lifecycle_stages) - 1:
                ax.arrow(i/len(lifecycle_stages) + 0.2, 0.5, 0.15, 0, head_width=0.05, 
                        head_length=0.01, fc=color, ec=color)
        
        st.pyplot(lifecycle_fig)
    
    with col2:
        info_box("""<b>You are here: Model Development</b>
        
In this phase, you'll focus on:
- Training & Hyperparameter Tuning
- Built-in algorithms
- Automated model development
- Distributed training
        """)
    
    st.markdown("""
    In the **Model Development** phase, your data processing is complete, and your data is typically stored in S3.
    Now, you need to select the appropriate modeling approach and train your model.
    
    Key components of model development include:
    
    1. **Training and Hyperparameter tuning**
       - SageMaker training jobs
       - Built-in algorithms
       - Bring your own script or container
       - SageMaker Experiments and Debugger
       - Automatic Model Tuning
    
    2. **Automated and preconfigured model development**
       - Autopilot - Automated ML
       - SageMaker JumpStart
    
    3. **Distributed training and optimization**
       - Distributed Training frameworks
       - Training Compiler
    """)
    
    # AWS AI/ML Stack
    section_title("AWS AI/ML Stack")
    
    stack_data = {
        'Layer': ['AI Services', 'ML Services', 'ML Frameworks & Infrastructure'],
        'Description': [
            'Pre-trained AI services for ready-to-use intelligence',
            'Services to build, train, and deploy ML models (SageMaker)',
            'Support for deep learning frameworks, compute options'
        ],
        'Expertise Required': ['No ML expertise needed', 'Some ML knowledge', 'Deep ML expertise'],
        'Examples': [
            'Amazon Rekognition, Amazon Comprehend, Amazon Bedrock',
            'Amazon SageMaker, SageMaker JumpStart, SageMaker Autopilot',
            'TensorFlow, PyTorch, Apache MXNet on EC2/ECS'
        ]
    }
    
    stack_df = pd.DataFrame(stack_data)
    st.table(stack_df)

def render_modeling_approaches():
    main_title("Modeling Approaches")
    
    st.markdown("""
    When developing ML models on AWS, you have several approaches to choose from, depending on your requirements,
    expertise, and the complexity of your problem.
    """)
    
    # Create a comparison of model development methods
    st.image("https://miro.medium.com/max/1400/1*xmxe288KJ7WB5xiR_W6jcg.png", caption="Spectrum of AWS Machine Learning Options", use_container_width=True)
    
    subsection_title("SageMaker Model Development Methods")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Built-in Algorithms")
        st.markdown("""
        - Pre-implemented algorithms
        - No code required
        - Fast development
        - Scalable and optimized
        - Limited customization
        
        **Best for:** Standard problems with established algorithms
        """)
    
    with col2:
        st.markdown("### Bring Your Own Script")
        st.markdown("""
        - Use familiar ML frameworks
        - Customize training logic
        - SageMaker manages infrastructure
        - Supported frameworks:
          - TensorFlow, PyTorch
          - Scikit-learn, XGBoost
          - MXNet, HuggingFace
        
        **Best for:** Custom models using standard frameworks
        """)
    
    with col3:
        st.markdown("### Bring Your Own Container")
        st.markdown("""
        - Maximum flexibility
        - Full control over environment
        - Custom frameworks or packages
        - Build Docker containers
        - Integrate with SageMaker
        
        **Best for:** Highly specialized models or non-standard frameworks
        """)
    
    important_note("""
    <b>Note:</b> All these methods rely on containerization. The container includes the training code,
    dependencies, and runtime environment needed to train your model.
    """)
    
    # Supervised Learning Algorithms section
    section_title("Supervised Learning Algorithms")
    
    st.markdown("""
    Supervised learning algorithms learn from labeled training data to make predictions or classifications.
    SageMaker provides built-in implementations of many common supervised learning algorithms.
    """)
    
    # Create visualization of supervised learning algorithms
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create a simple tree representation
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Main node
    ax.text(5, 9, "Supervised Learning", ha='center', fontsize=16, bbox=dict(facecolor='#FF9900', alpha=0.5, boxstyle='round'))
    
    # First level nodes
    ax.text(2.5, 7, "Classification", ha='center', fontsize=14, bbox=dict(facecolor='#1E88E5', alpha=0.3, boxstyle='round'))
    ax.text(7.5, 7, "Regression", ha='center', fontsize=14, bbox=dict(facecolor='#1E88E5', alpha=0.3, boxstyle='round'))
    
    # Connect lines
    ax.plot([5, 2.5], [8.8, 7.3], 'k-')
    ax.plot([5, 7.5], [8.8, 7.3], 'k-')
    
    # Second level - Classification
    ax.text(1.5, 5, "Binary", ha='center', fontsize=12, bbox=dict(facecolor='lightgray', alpha=0.3, boxstyle='round'))
    ax.text(3.5, 5, "Multi-class", ha='center', fontsize=12, bbox=dict(facecolor='lightgray', alpha=0.3, boxstyle='round'))
    
    # Connect lines for classification
    ax.plot([2.5, 1.5], [6.8, 5.3], 'k-')
    ax.plot([2.5, 3.5], [6.8, 5.3], 'k-')
    
    # Algorithms - Binary
    ax.text(1.5, 3.5, "Linear Learner\nXGBoost\nSVM", ha='center', fontsize=10, bbox=dict(facecolor='white', boxstyle='round,pad=0.5', edgecolor='gray'))
    ax.plot([1.5, 1.5], [4.8, 3.8], 'k-')
    
    # Algorithms - Multi-class
    ax.text(3.5, 3.5, "XGBoost\nK-NN\nRandomForest", ha='center', fontsize=10, bbox=dict(facecolor='white', boxstyle='round,pad=0.5', edgecolor='gray'))
    ax.plot([3.5, 3.5], [4.8, 3.8], 'k-')
    
    # Algorithms - Regression
    ax.text(7.5, 5, "Linear Regression\nXGBoost\nRandomForest", ha='center', fontsize=10, bbox=dict(facecolor='white', boxstyle='round,pad=0.5', edgecolor='gray'))
    ax.plot([7.5, 7.5], [6.8, 5.3], 'k-')
    
    st.pyplot(fig)
    
    # Unsupervised learning
    section_title("Unsupervised Learning Algorithms")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        Unsupervised learning algorithms find patterns in unlabeled data. These algorithms are used for:
        
        - **Clustering**: Group similar items together (K-means)
        - **Dimensionality Reduction**: Simplify data while preserving information (PCA)
        - **Anomaly Detection**: Find unusual patterns (Random Cut Forest)
        - **Topic Modeling**: Discover abstract topics in documents (LDA, NTM)
        """)
        
    with col2:
        # Simple representation of unsupervised learning
        cluster_data = np.random.randn(100, 2) * 0.8
        cluster_centers = [(2, 2), (-2, 2), (0, -2)]
        for center_x, center_y in cluster_centers:
            new_points = np.random.randn(30, 2) * 0.3 + np.array([center_x, center_y])
            cluster_data = np.vstack([cluster_data, new_points])
        
        fig, ax = plt.subplots(figsize=(8, 6))
        scatter = ax.scatter(cluster_data[:, 0], cluster_data[:, 1], c=np.repeat(range(4), [100, 30, 30, 30]), 
                           cmap='viridis', alpha=0.6)
        ax.set_title("Unsupervised Learning: Clustering Example")
        ax.set_xlabel("Feature 1")
        ax.set_ylabel("Feature 2")
        ax.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig)
    
    info_box("""<b>Key SageMaker Built-in Algorithms:</b><br><br>
    
<b>For structured data:</b>
- XGBoost: For both classification and regression
- K-Nearest Neighbors (K-NN): Classification and regression
- Linear Learner: Linear and logistic regression

<b>For text data:</b>
- BlazingText: Word embeddings and text classification
- Neural Topic Model (NTM): Topic discovery
- LDA: Document topic discovery

<b>For images:</b>
- Image Classification: Multi-class classification
- Object Detection: Localize and classify objects
- Semantic Segmentation: Pixel-level classification
    """)
    
    # Special data types
    section_title("Algorithms for Specialized Data Types")
    
    st.markdown("""
    SageMaker offers specialized algorithms for specific data types:
    """)
    
    tab1, tab2, tab3 = st.tabs(["Text/Speech Data", "Image/Video Data", "Time Series Data"])
    
    with tab1:
        st.markdown("""
        ### Text and Speech Algorithms
        
        - **BlazingText**
          - Word2Vec embeddings
          - Text classification
          - Highly optimized implementation
          
        - **Object2Vec**
          - Multi-purpose embeddings
          - Customer-product, document-document relationships
          
        - **Sequence-to-Sequence**
          - Translation, summarization
          - Speech-to-text applications
          
        - **LDA and NTM**
          - Topic modeling
          - Document classification
          - Content recommendation
        """)
    
    with tab2:
        st.markdown("""
        ### Image and Video Algorithms
        
        - **Image Classification**
          - Multi-class/multi-label classification
          - Built on ResNet architecture
          
        - **Object Detection**
          - Locate and classify objects in images
          - Single Shot Detector (SSD)
          - Faster R-CNN implementations
          
        - **Semantic Segmentation**
          - Pixel-level classification
          - Scene understanding
          - Built on FCN, MobileNet architectures
        """)
    
    with tab3:
        st.markdown("""
        ### Time Series Algorithms
        
        - **DeepAR**
          - Time-series forecasting
          - Recurrent neural network (RNN) based
          - Supports multiple related time series
          
        - **Forecasting**
          - Automatic forecasting algorithm selection
          - Statistical and ML approaches
          - Auto-handles seasonality and missing values
        """)

def render_amazon_bedrock():
    main_title("Amazon Bedrock")
    
    st.markdown("""
    Amazon Bedrock is a fully managed service that offers a choice of high-performing foundation models (FMs) 
    from leading AI companies through a single API, along with a comprehensive set of capabilities to build 
    generative AI applications with security, privacy, and responsible AI.
    """)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        ### Key Features of Amazon Bedrock
        
        - **Choice of leading FMs through a single API**
          - Access multiple foundation models from companies like Anthropic, AI21, Cohere, and Amazon
          - Single API simplifies integration and experimentation
        
        - **Model customization**
          - Fine-tune models to better suit specific use cases
          - Optimize performance for your domain
        
        - **Retrieval Augmented Generation (RAG)**
          - Connect foundation models to your data sources
          - Generate more relevant, contextual, and accurate responses
        
        - **Agents that execute multistep tasks**
          - Create AI agents that can orchestrate complex workflows
          - Integrate with business systems and data sources
        
        - **Security, privacy, and safety**
          - Enterprise-grade security features
          - Private deployment options
          - Control model access and usage
        """)
    
    with col2:
        st.image("https://dmhnzl5mp9mj6.cloudfront.net/security_awsblog/images/BEDROCK-Architecture.png", caption="Amazon Bedrock Architecture")
        
        info_box("""<b>Foundation models (FMs)</b> are large AI models pre-trained on vast amounts of data that can be adapted to a wide range of tasks.
        
Unlike traditional ML models built for specific tasks, FMs provide a versatile foundation that can be customized for various applications.
        """)
    
    section_title("Customizing Foundation Models")
    
    # Create a visualization comparing foundation model customization methods
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Set up the axis
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Define the methods and their properties
    methods = [
        {"name": "Prompt Engineering", "x": 1.5, "y": 7, "complexity": "Low", "training": "No"},
        {"name": "Retrieval Augmented Generation (RAG)", "x": 3.5, "y": 7, "complexity": "Medium", "training": "No"},
        {"name": "Fine-tuning", "x": 6.5, "y": 7, "complexity": "High", "training": "Yes"},
        {"name": "Continued pretraining", "x": 9, "y": 7, "complexity": "Very High", "training": "Yes"}
    ]
    
    # Draw a horizontal line representing increasing complexity
    ax.plot([1, 9], [5, 5], 'k-', alpha=0.5)
    ax.text(5, 4.5, "Complexity, cost, time →", ha='center', fontsize=12)
    
    # Add methods to the visualization
    for method in methods:
        if method["training"] == "No":
            color = '#ADD8E6'  # Light blue for no training
            training_text = "No model training involved"
        else:
            color = '#FFA07A'  # Light salmon for training
            training_text = "Model training involved"
            
        # Draw method box
        ax.text(method["x"], method["y"], method["name"], ha='center', fontsize=12, 
                bbox=dict(facecolor=color, alpha=0.7, boxstyle='round,pad=0.5'))
        
        # Draw description below
        ax.text(method["x"], method["y"]-1, f"Complexity: {method['complexity']}\n{training_text}", 
                ha='center', fontsize=10)
        
        # Draw a vertical line to the horizontal complexity line
        ax.plot([method["x"], method["x"]], [method["y"]-1.5, 5], 'k--', alpha=0.3)
    
    st.pyplot(fig)
    
    st.markdown("""
    ### Common Approaches for Customizing Foundation Models
    
    1. **Prompt Engineering**
       - Crafting effective prompts to guide model outputs
       - No model training required
       - Quick and cost-effective, but limited customization
       
    2. **Retrieval Augmented Generation (RAG)**
       - Retrieving relevant knowledge to supplement model responses
       - Connects models to your data sources
       - Balances customization and complexity
       
    3. **Fine-tuning**
       - Adapting models for specific tasks using your data
       - Requires model training but with smaller datasets
       - Better performance on domain-specific tasks
       
    4. **Continued pretraining**
       - Further training the model on large amounts of domain data
       - Most complex and resource-intensive approach
       - Maximum customization for specialized domains
    """)
    
    section_title("Knowledge Bases for Amazon Bedrock")
    
    st.markdown("""
    Knowledge Bases for Amazon Bedrock enable you to implement Retrieval Augmented Generation (RAG) 
    by securely connecting foundation models to your data sources.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Key Benefits
        
        - **Securely connect FMs to your data sources**
          - Integrate with your enterprise data
          - Keep sensitive information private
        
        - **Fully managed RAG workflow**
          - Automatic ingestion of your data
          - Intelligent retrieval of relevant information
          - Seamless prompt augmentation
        
        - **Session context management**
          - Maintain conversation history
          - Support for multi-turn interactions
          
        - **Automatic citations**
          - Track source information
          - Improve result transparency
          - Validate information accuracy
        """)
    
    with col2:
        # Creating a simple RAG workflow diagram
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Create components
        components = [
            {"name": "User Query", "x": 1, "y": 8, "type": "input", "color": "#E1F5FE"},
            {"name": "Knowledge Base", "x": 5, "y": 6, "type": "db", "color": "#FFECB3"},
            {"name": "Augmented Prompt", "x": 5, "y": 8, "type": "process", "color": "#E8F5E9"},
            {"name": "Foundation Model", "x": 5, "y": 2, "type": "model", "color": "#FF9900", "models": [
                "Anthropic—Claude", "Meta—Llama", "Amazon Titan", "AI21 Labs—Jurassic"
            ]},
            {"name": "Response", "x": 9, "y": 8, "type": "output", "color": "#E8F5E9"}
        ]
        
        # Draw connections
        ax.arrow(2, 8, 2, 0, head_width=0.2, head_length=0.2, fc='black', ec='black', width=0.05)
        ax.arrow(5, 7, 0, -4, head_width=0.2, head_length=0.2, fc='black', ec='black', width=0.05)
        ax.arrow(6.5, 8, 1.5, 0, head_width=0.2, head_length=0.2, fc='black', ec='black', width=0.05)
        ax.arrow(5, 3, 0, 2, head_width=0.2, head_length=0.2, fc='black', ec='black', width=0.05)
        
        # Draw retrieval arrow
        ax.arrow(2, 7, 2, -0.5, head_width=0.2, head_length=0.2, fc='#FFA07A', ec='#FFA07A', width=0.05)
        ax.text(3, 6.5, "Semantic Search", fontsize=8, color="#D32F2F")
        
        # Draw components
        for c in components:
            if c["type"] == "model":
                # Draw foundation model box
                ax.add_patch(plt.Rectangle((c["x"]-3, c["y"]-1), 6, 2, fill=True, facecolor=c["color"], 
                                          edgecolor='gray', alpha=0.7, linewidth=2))
                ax.text(c["x"], c["y"], c["name"], ha='center', va='center', fontsize=12, fontweight='bold')
                
                # Draw model names
                y_offset = 0.5
                for model in c["models"]:
                    ax.text(c["x"], c["y"] - y_offset, model, ha='center', va='center', fontsize=8, fontstyle='italic')
                    y_offset += 0.3
            else:
                if c["type"] == "db":
                    # Database symbol (cylinder-like)
                    ax.add_patch(Rectangle((c["x"]-2, c["y"]-0.75), 4, 1.5, fill=True, facecolor=c["color"], 
                                               edgecolor='gray', alpha=0.7, linewidth=1))
                    ax.add_patch(Ellipse((c["x"], c["y"]+0.75), 4, 0.5, fill=True, facecolor=c["color"], 
                                             edgecolor='gray', alpha=0.7, linewidth=1))
                    ax.add_patch(Ellipse((c["x"], c["y"]-0.75), 4, 0.5, fill=True, facecolor=c["color"], 
                                             edgecolor='gray', alpha=0.7, linewidth=1))
                else:
                    # Regular boxes
                    ax.add_patch(plt.Rectangle((c["x"]-1, c["y"]-0.5), 2, 1, fill=True, facecolor=c["color"], 
                                               edgecolor='gray', alpha=0.7, linewidth=1))
                
                ax.text(c["x"], c["y"], c["name"], ha='center', va='center', fontsize=10)
        
        st.pyplot(fig)
        
        st.caption("RAG workflow in Amazon Bedrock Knowledge Bases")
    
    info_box("""<b>RAG in Action with Amazon Bedrock:</b><br><br>
    
1. <b>Data ingestion:</b> Your documents are chunked and converted to vector embeddings.<br>
2. <b>User query:</b> When a user asks a question, it's processed into a vector embedding.<br>
3. <b>Semantic search:</b> The system finds the most relevant document chunks.<br>
4. <b>Context enrichment:</b> The original query is augmented with retrieved information.<br>
5. <b>Foundation model processing:</b> The enriched prompt is sent to the foundation model.<br>
6. <b>Response:</b> The model generates an answer based on both its training and the supplied context.
    """)

def render_neural_networks():
    main_title("Neural Network Architecture")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        Neural networks are computational models inspired by the human brain. They consist of interconnected nodes (neurons) 
        organized in layers that process information and learn from data.
        
        ### Key Components of Neural Networks
        
        - **Input Layer**: Where data enters the network
        - **Hidden Layers**: Internal processing layers that transform data
        - **Output Layer**: Produces the final result/prediction
        - **Nodes/Neurons**: Processing units that apply activation functions
        - **Weights**: Connection strengths between nodes that are adjusted during learning
        - **Activation Functions**: Non-linear functions that determine node output (e.g., ReLU, Sigmoid, Tanh)
        """)
    
    with col2:
        # Create a neural network visualization
        fig, ax = plt.subplots(figsize=(8, 6))
        
        def draw_neural_network(ax, layer_sizes, layer_names=None):
            """Draw a neural network diagram"""
            if layer_names is None:
                layer_names = [f"Layer {i+1}" for i in range(len(layer_sizes))]
            
            # Vertical spacing
            v_spacing = 1
            h_spacing = 3
            
            # Compute positions
            layer_positions = []
            for i, size in enumerate(layer_sizes):
                layer_pos = []
                for j in range(size):
                    layer_pos.append((i*h_spacing, (size-1)/2 - j*v_spacing))
                layer_positions.append(layer_pos)
            
            # Draw nodes
            for i, layer in enumerate(layer_positions):
                for j, pos in enumerate(layer):
                    circle = plt.Circle(pos, 0.5, fill=True, facecolor='#FF9900' if i==0 else ('#232F3E' if i==len(layer_positions)-1 else '#1E88E5'), alpha=0.7)
                    ax.add_patch(circle)
                    
                # Add layer name
                if layer:
                    ax.text(i*h_spacing, -3, layer_names[i], ha='center')
            
            # Draw edges
            for i in range(len(layer_positions) - 1):
                for j, pos_a in enumerate(layer_positions[i]):
                    for k, pos_b in enumerate(layer_positions[i+1]):
                        ax.plot([pos_a[0], pos_b[0]], [pos_a[1], pos_b[1]], 'k-', alpha=0.3)
            
            # Set limits
            ax.set_aspect('equal')
            ax.set_xlim(-1, (len(layer_sizes) - 1) * h_spacing + 1)
            ax.set_ylim(-3.5, (max(layer_sizes) - 1) * v_spacing / 2 + 1)
            ax.axis('off')
        
        # Define network architecture
        layer_sizes = [4, 5, 5, 3]
        layer_names = ["Input Layer", "Hidden Layer 1", "Hidden Layer 2", "Output Layer"]
        
        draw_neural_network(ax, layer_sizes, layer_names)
        st.pyplot(fig)
    
    st.markdown("""
    ### How Neural Networks Work
    
    1. **Forward Propagation**
       - Input values are fed into the input layer
       - Each node receives inputs, applies weights, sums them, and applies an activation function
       - The output is passed to the next layer
       - This continues until the output layer produces predictions
    
    2. **Loss Calculation**
       - The model's predictions are compared to actual values
       - A loss function quantifies the error (e.g., MSE for regression, cross-entropy for classification)
    
    3. **Backpropagation**
       - The error is propagated backwards through the network
       - Gradients are calculated to determine how weights should be adjusted
       - The goal is to minimize the loss function
    
    4. **Weight Updates**
       - Weights are updated based on gradients and learning rate
       - The process repeats with new training examples
    """)
    
    important_note("""
    <b>Deep Learning</b> refers to neural networks with multiple hidden layers. These deep architectures can learn hierarchical features from data, with early layers learning simple features and deeper layers learning more complex, abstract features.
    """)
    
    section_title("Types of Neural Networks")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Feedforward Neural Networks")
        st.image("https://miro.medium.com/v2/resize:fit:1400/1*3fA77_mLNiJTSgZFhYnU0Q.png", caption="Feedforward NN")
        st.markdown("""
        - Information flows in one direction
        - Basic architecture for classification/regression
        - Fully connected layers
        - Good for tabular data
        """)
    
    with col2:
        st.markdown("### Convolutional Neural Networks (CNN)")
        st.image("https://miro.medium.com/v2/resize:fit:1400/1*vkQ0hXDaQv57sALXAJquxA.jpeg", caption="CNN")
        st.markdown("""
        - Specialized for grid-like data (images)
        - Uses convolutional filters to detect patterns
        - Pooling layers for downsampling
        - Extracts spatial features
        - Used in computer vision tasks
        """)
    
    with col3:
        st.markdown("### Recurrent Neural Networks (RNN)")
        st.image("https://miro.medium.com/v2/resize:fit:1400/1*6xj7xyBfK_IZ0re3XA0sTg.png", caption="RNN")
        st.markdown("""
        - Processes sequential data
        - Maintains memory of previous inputs
        - Feedback connections
        - LSTM and GRU variants address vanishing gradients
        - Used for time series, NLP
        """)

def render_model_training():
    main_title("Model Training")
    
    st.markdown("""
    Model training is the process of teaching a machine learning model to make accurate predictions by showing it examples.
    The model learns patterns from the data and adjusts its internal parameters to minimize errors.
    """)
    
    section_title("Overview of Amazon SageMaker Training Jobs")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        Amazon SageMaker provides a fully managed environment for training machine learning models.
        When you create a training job, SageMaker:
        
        1. **Sets up the training environment**
           - Provisions the specified compute instances
           - Installs the necessary software and dependencies
        
        2. **Loads your data**
           - Fetches data from Amazon S3, EFS, or FSx
           - Makes it available to the training code
        
        3. **Executes your training code**
           - Runs your algorithm within a container
           - Handles distributed training if multiple instances are specified
        
        4. **Monitors the training process**
           - Collects logs and metrics
           - Tracks resource utilization
        
        5. **Stores the model artifacts**
           - Saves trained model to S3 when training completes
           - Makes it available for deployment
        """)
    
    with col2:
        st.image("https://d1.awsstatic.com/reInvent/reinvent-2022/sagemaker/SageMaker%20Training%20HIW%20Diagram.9c1e2f98a344d9e7a799cfe871dd68ee877e8ce1.png", caption="SageMaker Training Overview")
        
        info_box("""<b>SageMaker Training Features:</b><br><br>
        
• Automatic model tuning<br>
• Distributed training<br>
• Spot instance support<br>
• Checkpointing<br>
• Training metrics<br>
• Debug and profile training jobs<br>
• Custom algorithms and containers
        """)
    
    section_title("Loading Training Data from Amazon S3")
    
    st.markdown("""
    Amazon SageMaker provides multiple options for loading training data into your training job.
    Choosing the right data loading mode can significantly impact training performance.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### File Mode")
        st.image("https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2019/12/30/SageMaker-FM.gif", width=300)
        st.markdown("""
        - Downloads entire dataset before training starts
        - Requires sufficient storage space
        - **Default setting**
        - Best for: Small datasets, simple workflows
        - All data must fit on training instance storage
        """)
    
    with col2:
        st.markdown("### Fast File Mode")
        st.image("https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2019/12/30/SageMaker-FFM.gif", width=300)
        st.markdown("""
        - Looks like normal files but streams in background
        - No waiting for downloads, reduced storage needs
        - Training starts immediately
        - Best for: Most modern workflows, random access patterns
        - Works well with large datasets
        """)
    
    with col3:
        st.markdown("### Pipe Mode")
        st.image("https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2019/12/30/SageMaker-PM.gif", width=300)
        st.markdown("""
        - Streaming mode that reads data sequentially
        - Direct streaming from S3 to training algorithm
        - Largely replaced by the newer Fast File mode
        - Best for: Algorithms that don't support Fast File mode
        - Higher throughput for sequential access
        """)
    
    important_note("""
    <b>Recommendation:</b> Fast File Mode is generally the best option for most modern workflows, as it combines the benefits of immediately starting training with the convenience of file system access.
    """)

def render_hyperparameters():
    main_title("Hyperparameters")
    
    st.markdown("""
    Hyperparameters are external configuration variables that control the behavior of a machine learning algorithm.
    Unlike model parameters (weights and biases) that are learned during training, hyperparameters are set before
    training begins and influence how the model learns.
    """)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        ### Common Hyperparameters
        
        - **Learning rate**: Controls step size during optimization
        - **Number of epochs**: How many times the training dataset is processed
        - **Batch size**: Number of samples processed before model update
        - **Network architecture**: Number of layers, nodes per layer
        - **Regularization parameters**: L1/L2 coefficients to prevent overfitting
        - **Tree depth**: Maximum depth for tree-based algorithms
        - **Number of estimators**: Trees in ensemble methods like Random Forest
        """)
    
    with col2:
        info_box("""<b>Why Hyperparameters Matter:</b><br><br>
        
• Directly impact model performance<br>
• Affect training speed and convergence<br>
• Influence model complexity and overfitting<br>
• Can make the difference between a successful and failed model
        """)
    
    section_title("Learning Rate")
    
    st.markdown("""
    The learning rate is one of the most important hyperparameters. It controls how much the model parameters
    are adjusted during training in response to the estimated error.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Function to create learning rate visualization
        def plot_learning_rate_effect(alpha):
            # Simple function with local minimum
            x = np.linspace(-5, 5, 100)
            y = x**2 + 2*np.sin(x)
            
            # Starting point
            x0 = 4
            y0 = x0**2 + 2*np.sin(x0)
            
            # Gradient at x0
            grad = 2*x0 + 2*np.cos(x0)
            
            # Update
            x1 = x0 - alpha * grad
            y1 = x1**2 + 2*np.sin(x1)
            
            # Create figure
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # Plot function
            ax.plot(x, y, 'b-', linewidth=2)
            
            # Plot current point
            ax.scatter(x0, y0, color='red', s=100, zorder=3)
            
            # Plot update
            ax.scatter(x1, y1, color='green', s=100, zorder=3)
            
            # Plot update vector
            ax.arrow(x0, y0, x1-x0, y1-y0, head_width=0.2, head_length=0.2, fc='black', ec='black', linewidth=2)
            
            # Annotate points
            ax.annotate("Starting point", (x0, y0), xytext=(x0+0.5, y0+2), arrowprops=dict(facecolor='black', shrink=0.05))
            ax.annotate("Updated position", (x1, y1), xytext=(x1-0.5, y1+2), arrowprops=dict(facecolor='black', shrink=0.05))
            
            # Title and labels
            ax.set_title(f"Effect of Learning Rate = {alpha}")
            ax.set_xlabel("Parameter Value")
            ax.set_ylabel("Loss")
            ax.grid(True, linestyle='--', alpha=0.7)
            
            return fig
        
        # Plot with small learning rate
        fig = plot_learning_rate_effect(0.1)
        st.pyplot(fig)
        st.markdown("**Small Learning Rate**: Slow convergence but stable")
    
    with col2:
        # Plot with large learning rate
        fig = plot_learning_rate_effect(0.5)
        st.pyplot(fig)
        st.markdown("**Large Learning Rate**: Fast updates but may overshoot minimum")
    
    st.markdown("""
    ### Impact of Learning Rate
    
    - **Too small**: Training will be slow and may get stuck in local minima
    - **Too large**: Training may diverge or oscillate around the minimum
    - **Just right**: Training converges efficiently to a good solution
    
    Modern approaches often use learning rate schedules that adjust the learning rate during training, 
    typically starting with a larger rate and decreasing it over time.
    """)
    
    section_title("Other Key Hyperparameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Network Architecture Hyperparameters
        
        - **Number of hidden layers**: Controls model depth
          - More layers can capture more complex patterns
          - Too many can lead to vanishing gradients and overfitting
        
        - **Nodes per layer**: Controls model width
          - More nodes increase capacity to learn
          - Increases computational requirements
        
        - **Activation functions**: Type of non-linearity
          - ReLU, Sigmoid, Tanh, etc.
          - Affects training dynamics and representational capacity
        
        - **Batch normalization**: Whether to normalize layer inputs
          - Improves training stability
          - Reduces sensitivity to initialization
        """)
    
    with col2:
        st.markdown("""
        ### Training Hyperparameters
        
        - **Batch size**: Samples per gradient update
          - Larger batches: more stable but require more memory
          - Smaller batches: noisier updates but better generalization
        
        - **Number of epochs**: Complete passes through the dataset
          - Too few: underfitting
          - Too many: potential overfitting
        
        - **Optimizer**: Algorithm for weight updates
          - SGD, Adam, RMSProp, etc.
          - Each has its own hyperparameters (momentum, beta)
        
        - **Dropout rate**: Fraction of nodes to deactivate
          - Higher rates increase regularization
          - Too high can prevent learning
        """)

def render_hyperparameter_tuning():
    main_title("Hyperparameter Tuning")
    
    st.markdown("""
    Hyperparameter tuning is the process of finding the optimal hyperparameter values for a machine learning model.
    Since hyperparameters cannot be learned directly from the training data, we need special techniques to find the best configuration.
    """)
    
    section_title("Automatic Model Tuning in Amazon SageMaker")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        Amazon SageMaker provides automatic model tuning (also known as hyperparameter tuning) to find the best version of a model by running many training jobs on your dataset using different hyperparameter combinations.
        
        ### Key Components for Setting Up a Tuning Job
        
        1. **Objective metrics**
           - The metric to optimize (maximize or minimize)
           - Example: accuracy, AUC, F1-score, MSE
        
        2. **Hyperparameter ranges**
           - The search space for each hyperparameter
           - Types: continuous, integer, categorical
        
        3. **Maximum number of jobs**
           - Total number of training jobs to run
        
        4. **Maximum parallel jobs**
           - Number of concurrent training jobs
        """)
    
    with col2:
        # Create diagram for hyperparameter tuning
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Create boxes and arrows for the workflow
        components = [
            {"name": "Define hyperparameter ranges\nand objective metric", "y": 5},
            {"name": "Create tuning job", "y": 4},
            {"name": "Run multiple training jobs\nwith different configurations", "y": 3},
            {"name": "Evaluate model performance", "y": 2},
            {"name": "Select best hyperparameters", "y": 1}
        ]
        
        for i, comp in enumerate(components):
            # Draw box
            ax.add_patch(plt.Rectangle((1, comp["y"]-0.4), 6, 0.8, fill=True, facecolor='#E1F5FE', alpha=0.7, edgecolor='#1E88E5'))
            ax.text(4, comp["y"], comp["name"], ha='center', va='center', fontsize=10)
            
            # Draw arrow
            if i < len(components) - 1:
                ax.arrow(4, comp["y"]-0.4, 0, -0.2, head_width=0.2, head_length=0.1, fc='black', ec='black')
        
        # Add AWS icon
        ax.text(7.5, 3, "Amazon\nSageMaker", ha='center', va='center', fontsize=12, 
               bbox=dict(facecolor='#FF9900', alpha=0.7, boxstyle='round,pad=0.5'))
        
        # Connect to tuning
        ax.arrow(7, 3, -0.5, 0, head_width=0.2, head_length=0.2, fc='black', ec='black')
        
        ax.set_xlim(0, 8)
        ax.set_ylim(0, 6)
        ax.axis('off')
        
        st.pyplot(fig)
        
        info_box("""<b>Benefits of SageMaker Automatic Model Tuning:</b><br><br>
        
• Automates the trial-and-error process<br>
• Uses advanced Bayesian optimization<br>
• Scales to thousands of hyperparameter combinations<br>
• Supports early stopping to save on compute costs<br>
• Tracks all experiments automatically
        """)
    
    section_title("Hyperparameter Tuning Techniques")
    
    st.markdown("""
    There are several approaches to search through the hyperparameter space effectively:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Grid Search")
        st.image("https://www.sciencedirect.com/science/article/pii/S0169743922000314/gr1_lrg", width=250)
        st.markdown("""
        - Systematically searches all combinations
        - Divides each hyperparameter range into equally spaced values
        - Exhaustive but inefficient for high-dimensional spaces
        - Computationally expensive
        - Works well for small search spaces
        """)
    
    with col2:
        st.markdown("### Random Search")
        st.image("https://www.sciencedirect.com/science/article/pii/S0169743922000314/gr2_lrg", width=250)
        st.markdown("""
        - Randomly samples points from hyperparameter space
        - More efficient than grid search
        - Better coverage with same compute budget
        - Can be more effective at finding optimal values
        - Works well for spaces with few important parameters
        """)
    
    with col3:
        st.markdown("### Bayesian Optimization")
        st.image("https://www.sciencedirect.com/science/article/pii/S0169743922000314/gr3_lrg", width=250)
        st.markdown("""
        - Uses results of previous evaluations
        - Builds probabilistic model of the objective
        - Intelligently selects next points to evaluate
        - More efficient for expensive function evaluations
        - **Default strategy in SageMaker**
        """)
    
    important_note("""
    <b>Advanced technique:</b> Amazon SageMaker also supports Hyperband, which dynamically allocates resources to promising configurations and stops underperforming ones early, making it particularly efficient for training deep learning models.
    """)
    
    section_title("Implementing Hyperparameter Tuning in SageMaker")
    
    st.markdown("""
    Here's how to set up hyperparameter tuning in Amazon SageMaker using the Python SDK:
    """)
    
    st.code("""
    # Setup the hyperparameter ranges
    hyperparameter_ranges = {
        'eta': ContinuousParameter(0, 1),
        'min_child_weight': ContinuousParameter(1, 10),
        'alpha': ContinuousParameter(0, 2),
        'max_depth': IntegerParameter(1, 10),
        'num_round': IntegerParameter(100, 1000)
    }
    
    # Define the target metric and the objective type (max/min)
    objective_metric_name = 'validation:auc'
    objective_type='Maximize'
    
    # Define the HyperparameterTuner
    tuner = HyperparameterTuner(
        estimator = xgb,
        objective_metric_name = objective_metric_name,
        hyperparameter_ranges = hyperparameter_ranges,
        objective_type = objective_type,
        max_jobs=9,
        max_parallel_jobs=3,
        early_stopping_type='Auto'
    )
    
    # Start the tuning job
    tuner.fit({'training': inputs})
    """, language="python")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### Hyperparameter Ranges
        
        - **ContinuousParameter**: Float values within a range
          - Example: learning rate, regularization strength
        
        - **IntegerParameter**: Integer values within a range
          - Example: max_depth, num_round
        
        - **CategoricalParameter**: Values from a discrete set
          - Example: activation function, optimizer
        """)
    
    with col2:
        st.markdown("""
        ### Scaling Types
        
        For numeric hyperparameters, you can specify a scaling type:
        
        - **Linear**: Uniform sampling across range
          - Good for narrow ranges (within one order of magnitude)
        
        - **Logarithmic**: Values sampled on log scale
          - Good for wide ranges (multiple orders of magnitude)
          - Example: learning rate from 0.0001 to 0.1
        
        - **Auto**: SageMaker chooses the appropriate scale
        """)
    
    section_title("Warm Start Tuning")
    
    st.markdown("""
    Amazon SageMaker also supports **Warm Start Tuning**, which lets you start a new hyperparameter tuning job using one or more previous tuning jobs as a starting point.
    """)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        ### Benefits of Warm Start
        
        - **Transfer learning for hyperparameters**
          - Use knowledge from previous tuning jobs
          - Focus on promising regions of the hyperparameter space
        
        - **Time and cost efficiency**
          - Reduces the number of jobs needed to find optimal configuration
          - Particularly valuable for expensive models
        
        - **Iterative refinement**
          - Gradually narrow down search space
          - Fine-tune hyperparameters in stages
        """)
    
    with col2:
        # Create a visualization of warm start benefit
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Create a contour plot representing hyperparameter space
        x = np.linspace(0, 10, 100)
        y = np.linspace(0, 10, 100)
        X, Y = np.meshgrid(x, y)
        Z = 3*(1-X)**2 * np.exp(-X**2 - (Y+1)**2) - 10*(X/5 - X**3 - Y**5) * np.exp(-X**2 - Y**2) - 1/3 * np.exp(-(X+1)**2 - Y**2)
        
        # Plot contour
        contour = ax.contourf(X, Y, Z, 15, cmap='viridis', alpha=0.7)
        
        # Add points for cold start (spread across space)
        cold_x = np.random.uniform(0, 10, 20)
        cold_y = np.random.uniform(0, 10, 20)
        ax.scatter(cold_x, cold_y, color='red', marker='x', label='Cold Start Evaluations')
        
        # Add points for warm start (concentrated in promising area)
        warm_x = np.random.normal(7, 1, 20)
        warm_y = np.random.normal(3, 1, 20)
        ax.scatter(warm_x, warm_y, color='white', marker='o', label='Warm Start Evaluations')
        
        # Circle the optimal region
        optimal = plt.Circle((7, 3), 1.5, fill=False, color='yellow', linewidth=2, linestyle='--', label='Optimal Region')
        ax.add_patch(optimal)
        
        ax.set_xlabel('Hyperparameter 1')
        ax.set_ylabel('Hyperparameter 2')
        ax.set_title('Warm Start vs Cold Start Hyperparameter Tuning')
        ax.legend()
        
        st.pyplot(fig)

def render_distributed_training():
    main_title("Distributed Training and Early Stopping")
    
    st.markdown("""
    When dealing with large models or datasets, distributed training can significantly reduce training time.
    Additionally, techniques like early stopping can help optimize the training process and prevent overfitting.
    """)
    
    section_title("Early Stopping")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        **Early stopping** is a technique that stops training when the model's performance on a validation set stops improving.
        This helps prevent overfitting and saves compute resources.
        
        ### How Early Stopping Works
        
        1. Monitor a validation metric during training
        2. Stop training when the metric stops improving for a specified number of iterations
        3. Use the best model from the training process
        
        ### Benefits of Early Stopping
        
        - **Prevents overfitting**: Stops before model starts memorizing training data
        - **Reduces training time**: Avoids unnecessary additional epochs
        - **Automatic optimal epoch selection**: No need to manually determine the ideal number of epochs
        - **Resource efficiency**: Saves compute resources by not running unnecessary iterations
        """)
    
    with col2:
        # Create visualization for early stopping
        epochs = np.arange(1, 101)
        train_loss = 1 / (1 + 0.1*epochs) + 0.1*np.random.randn(100)
        val_loss = 1 / (1 + 0.1*epochs) + 0.2/(1 + 0.04*epochs) + 0.1*np.random.randn(100)
        
        # Make validation loss start increasing after epoch 50
        val_loss[50:] = val_loss[50:] + 0.005 * (epochs[50:] - 50)
        
        best_epoch = np.argmin(val_loss)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(epochs, train_loss, 'b-', label='Training Loss')
        ax.plot(epochs, val_loss, 'r-', label='Validation Loss')
        ax.axvline(x=best_epoch, color='g', linestyle='--', label=f'Early Stopping (Epoch {best_epoch})')
        
        # Highlight overfitting region
        ax.fill_between(epochs[best_epoch:], val_loss[best_epoch:], train_loss[best_epoch:], 
                       alpha=0.3, color='orange', label='Overfitting Region')
        
        ax.set_xlabel('Epochs')
        ax.set_ylabel('Loss')
        ax.set_title('Early Stopping to Prevent Overfitting')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        
        st.pyplot(fig)
        
        info_box("""<b>SageMaker Early Stopping:</b><br><br>
        
SageMaker automatically implements early stopping for hyperparameter tuning jobs, saving time and resources by terminating poorly performing training jobs early.
        """)
    
    section_title("Distributed Training")
    
    st.markdown("""
    **Distributed training** allows machine learning training to be split across multiple machines or GPUs,
    enabling faster training of large models and datasets.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### Data Parallelism
        
        - **How it works**:
          - Splitting the dataset across multiple nodes
          - Each node has a copy of the complete model
          - Nodes process different data batches in parallel
          - Gradients are synchronized to update the model
        
        - **Best for**:
          - Large datasets
          - Models that fit in single device memory
          - Batch size that can be divided across devices
        """)
    
    with col2:
        st.markdown("""
        ### Model Parallelism
        
        - **How it works**:
          - Splitting the model across multiple nodes
          - Different parts of the model run on different devices
          - Activations are passed between devices during forward pass
          - Gradients passed between devices during backward pass
        
        - **Best for**:
          - Large models that don't fit in single device memory
          - Models with components that can be efficiently partitioned
          - Giant neural networks with billions of parameters
        """)

def render_ensemble_learning():
    main_title("Ensemble Learning")
    
    st.markdown("""
    Ensemble learning combines multiple machine learning models to produce a more powerful model that has better predictive performance than any individual model in the ensemble.
    """)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        ### Key Benefits of Ensemble Methods
        
        - **Improved accuracy**: Combined models often outperform individual models
        - **Reduced overfitting**: Ensembles tend to generalize better to new data
        - **Increased stability**: Less variance in predictions across different datasets
        - **Better handling of complex problems**: Capture different aspects of the data
        
        ### When to Use Ensembles
        
        - When you need the highest possible accuracy
        - When you have computational resources for multiple models
        - When individual models have complementary strengths
        - When you want to reduce the risk of selecting a poor model
        """)
    
    with col2:
        info_box("""<b>Types of Ensemble Methods:</b><br><br>
        
• <b>Stacking</b>: Trains a meta-model on the predictions of base models<br>
• <b>Bagging</b>: Trains models on random subsets of the data (e.g., Random Forest)<br>
• <b>Boosting</b>: Builds models sequentially, each correcting the errors of previous models (e.g., XGBoost)<br>
• <b>Voting</b>: Combines predictions through majority vote (classification) or averaging (regression)
        """)
    
    section_title("Ensemble Learning Techniques")
    
    tab1, tab2, tab3 = st.tabs(["Stacking", "Bagging", "Boosting"])
    
    with tab1:
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.markdown("""
            ### Stacking (Stacked Generalization)
            
            - **How it works**:
              - Train multiple base models on the training data
              - Use predictions from these models as inputs to a meta-model
              - Meta-model learns to combine base predictions optimally
            
            - **Strengths**:
              - Can combine very different types of models
              - Often achieves higher accuracy than any single model
              - Leverages strengths of different algorithms
            
            - **Implementation**:
              - Base layer: diverse models (e.g., random forest, SVM, neural network)
              - Meta-model: simple model to combine predictions (e.g., logistic regression)
            """)
        
        with col2:
            # Stacking visualization
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # Dataset
            ax.add_patch(plt.Rectangle((1, 9), 8, 1, fill=True, facecolor='#E8F5E9', 
                                      edgecolor='#388E3C', alpha=0.7))
            ax.text(5, 9.5, "Training Data", ha='center', va='center', fontsize=12)
            
            # Base models
            base_models = [
                {"name": "Random Forest", "x": 2, "y": 7, "color": "#E1F5FE"},
                {"name": "Neural Network", "x": 5, "y": 7, "color": "#FFECB3"},
                {"name": "SVM", "x": 8, "y": 7, "color": "#F3E5F5"}
            ]
            
            for model in base_models:
                ax.add_patch(plt.Rectangle((model["x"]-1, model["y"]-0.5), 2, 1, fill=True, 
                                          facecolor=model["color"], edgecolor='gray', alpha=0.7))
                ax.text(model["x"], model["y"], model["name"], ha='center', va='center', fontsize=10)
                
                # Connect to dataset
                ax.arrow(model["x"], 9, 0, -1.5, head_width=0.2, head_length=0.2, 
                        fc='black', ec='black', width=0.05, alpha=0.7)
            
            # Predictions
            for i, model in enumerate(base_models):
                ax.add_patch(plt.Rectangle((model["x"]-0.75, model["y"]-2.5), 1.5, 1, fill=True, 
                                          facecolor=model["color"], edgecolor='gray', alpha=0.7))
                ax.text(model["x"], model["y"]-2, f"Predictions {i+1}", 
                       ha='center', va='center', fontsize=8)
                
                # Connect to model
                ax.arrow(model["x"], model["y"]-0.5, 0, -0.5, head_width=0.2, head_length=0.2, 
                        fc='black', ec='black', width=0.05, alpha=0.7)
            
            # Meta model
            ax.add_patch(plt.Rectangle((3, 3), 4, 1, fill=True, facecolor='#FF9900', 
                                      edgecolor='#E65100', alpha=0.7))
            ax.text(5, 3.5, "Meta Model (Logistic Regression)", 
                   ha='center', va='center', fontsize=10)
            
            # Connect predictions to meta model
            for model in base_models:
                ax.arrow(model["x"], model["y"]-1.5, 5-model["x"], 4.5-model["y"], head_width=0.2, head_length=0.2, 
                        fc='black', ec='black', width=0.05, alpha=0.7)
            
            # Final prediction
            ax.add_patch(plt.Rectangle((4, 1), 2, 1, fill=True, facecolor='#DCEDC8', 
                                      edgecolor='#689F38', alpha=0.7))
            ax.text(5, 1.5, "Final Prediction", ha='center', va='center', fontsize=10)
            
            # Connect meta model to final prediction
            ax.arrow(5, 3, 0, -0.5, head_width=0.2, head_length=0.2, 
                    fc='black', ec='black', width=0.05, alpha=0.7)
            
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            ax.set_title("Stacking Ensemble Method")
            
            st.pyplot(fig)
    
    with tab2:
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.markdown("""
            ### Bagging (Bootstrap Aggregating)
            
            - **How it works**:
              - Create multiple training sets by sampling with replacement
              - Train the same algorithm on each sample
              - Combine predictions (majority vote or average)
            
            - **Strengths**:
              - Reduces variance and helps avoid overfitting
              - Improves stability and accuracy
              - Works well with high-variance models (e.g., decision trees)
            
            - **Examples**:
              - Random Forest (bagging with decision trees)
              - Bagged SVM
              - Extra Trees (extremely randomized trees)
            """)
        
        with col2:
            # Bagging visualization
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # Original dataset
            ax.add_patch(plt.Rectangle((4, 9), 2, 1, fill=True, facecolor='#E8F5E9', 
                                     edgecolor='#388E3C', alpha=0.7))
            ax.text(5, 9.5, "Original Dataset", ha='center', va='center', fontsize=12)
            
            # Bootstrap samples
            bootstrap_samples = [
                {"x": 2, "y": 7, "samples": [1, 2, 2, 4, 5]},
                {"x": 5, "y": 7, "samples": [1, 3, 3, 4, 6]},
                {"x": 8, "y": 7, "samples": [2, 2, 3, 5, 6]}
            ]
            
            for i, sample in enumerate(bootstrap_samples):
                ax.add_patch(plt.Rectangle((sample["x"]-1, sample["y"]-0.5), 2, 1, fill=True, 
                                         facecolor='#E1F5FE', edgecolor='#1E88E5', alpha=0.7))
                ax.text(sample["x"], sample["y"], f"Bootstrap Sample {i+1}", 
                       ha='center', va='center', fontsize=10)
                
                # Show some sample numbers
                ax.text(sample["x"], sample["y"]-0.3, f"Samples: {sample['samples']}", 
                       ha='center', va='center', fontsize=7)
                
                # Connect to original dataset
                ax.arrow(5, 9, sample["x"]-5, -1.5, head_width=0.2, head_length=0.2, 
                       fc='black', ec='black', width=0.05, alpha=0.7)
            
            # Models
            models = [
                {"x": 2, "y": 5, "name": "Model 1"},
                {"x": 5, "y": 5, "name": "Model 2"},
                {"x": 8, "y": 5, "name": "Model 3"}
            ]
            
            for i, model in enumerate(models):
                ax.add_patch(plt.Rectangle((model["x"]-1, model["y"]-0.5), 2, 1, fill=True, 
                                         facecolor='#FFECB3', edgecolor='#FFA000', alpha=0.7))
                ax.text(model["x"], model["y"], model["name"], ha='center', va='center', fontsize=10)
                
                # Connect to bootstrap sample
                sample = bootstrap_samples[i]
                ax.arrow(sample["x"], sample["y"]-0.5, 0, -1, head_width=0.2, head_length=0.2, 
                       fc='black', ec='black', width=0.05, alpha=0.7)
            
            # Predictions
            predictions = [
                {"x": 2, "y": 3, "pred": "Class A"},
                {"x": 5, "y": 3, "pred": "Class B"},
                {"x": 8, "y": 3, "pred": "Class A"}
            ]
            
            for i, pred in enumerate(predictions):
                ax.add_patch(plt.Rectangle((pred["x"]-0.75, pred["y"]-0.5), 1.5, 1, fill=True, 
                                          facecolor='#F3E5F5', edgecolor='#9C27B0', alpha=0.7))
                ax.text(pred["x"], pred["y"], pred["pred"], ha='center', va='center', fontsize=8)
                
                # Connect to model
                model = models[i]
                ax.arrow(model["x"], model["y"]-0.5, 0, -1, head_width=0.2, head_length=0.2, 
                        fc='black', ec='black', width=0.05, alpha=0.7)
            
            # Aggregation
            ax.add_patch(plt.Rectangle((3.5, 1), 3, 1, fill=True, facecolor='#FF9900', 
                                      edgecolor='#E65100', alpha=0.7))
            ax.text(5, 1.5, "Majority Vote: Class A", ha='center', va='center', fontsize=10)
            
            # Connect predictions to aggregation
            for pred in predictions:
                ax.arrow(pred["x"], pred["y"]-0.5, 5-pred["x"], 1.5-pred["y"]+0.5, head_width=0.2, head_length=0.2, 
                        fc='black', ec='black', width=0.05, alpha=0.7)
            
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            ax.set_title("Bagging Ensemble Method")
            
            st.pyplot(fig)
    
    with tab3:
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.markdown("""
            ### Boosting
            
            - **How it works**:
              - Train models sequentially
              - Each model focuses on examples previous models got wrong
              - Weighted combination of all models
            
            - **Strengths**:
              - Often achieves best performance of ensemble methods
              - Makes weak learners stronger
              - Can capture complex patterns
            
            - **Examples**:
              - AdaBoost
              - Gradient Boosting Machines (GBM)
              - XGBoost
              - LightGBM
              - CatBoost
            """)
        
        with col2:
            # Boosting visualization
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # Dataset
            ax.add_patch(plt.Rectangle((1, 8.5), 8, 1, fill=True, facecolor='#E8F5E9', 
                                      edgecolor='#388E3C', alpha=0.7))
            ax.text(5, 9, "Training Data (with weights)", ha='center', va='center', fontsize=12)
            
            # Models in sequence
            models = [
                {"x": 2, "y": 6.5, "name": "Model 1", "error_focus": "Initial uniform weights"},
                {"x": 5, "y": 6.5, "name": "Model 2", "error_focus": "Focus on errors from Model 1"},
                {"x": 8, "y": 6.5, "name": "Model 3", "error_focus": "Focus on errors from Model 2"}
            ]
            
            for i, model in enumerate(models):
                # Model box
                ax.add_patch(plt.Rectangle((model["x"]-1.5, model["y"]-0.5), 3, 1, fill=True, 
                                         facecolor='#FFECB3', edgecolor='#FFA000', alpha=0.7))
                ax.text(model["x"], model["y"], model["name"], ha='center', va='center', fontsize=10)
                
                # Error focus
                ax.text(model["x"], model["y"]-0.3, model["error_focus"], 
                       ha='center', va='center', fontsize=7, fontstyle='italic')
                
                # Data to model connection
                ax.arrow(5, 8.5, model["x"]-5, -1.5, head_width=0.2, head_length=0.2, 
                       fc='black', ec='black', width=0.05, alpha=0.7)
            
            # Sequential flow between models
            for i in range(len(models)-1):
                ax.arrow(models[i]["x"]+1.5, models[i]["y"], 1.5, 0, head_width=0.2, head_length=0.2, 
                       fc='black', ec='black', width=0.05, alpha=0.7)
                ax.text(models[i]["x"]+2.25, models[i]["y"]+0.3, "Update weights", 
                       ha='center', va='center', fontsize=7, fontstyle='italic')
            
            # Predictions
            for model in models:
                y_pos = model["y"] - 2
                ax.add_patch(plt.Rectangle((model["x"]-0.75, y_pos-0.5), 1.5, 1, fill=True, 
                                          facecolor='#F3E5F5', edgecolor='#9C27B0', alpha=0.7))
                ax.text(model["x"], y_pos, f"Weak Prediction", 
                       ha='center', va='center', fontsize=8)
                
                # Connect model to prediction
                ax.arrow(model["x"], model["y"]-0.5, 0, -1.5, head_width=0.2, head_length=0.2, 
                        fc='black', ec='black', width=0.05, alpha=0.7)
            
            # Final weighted prediction
            ax.add_patch(plt.Rectangle((3.5, 2), 3, 1, fill=True, facecolor='#FF9900', 
                                      edgecolor='#E65100', alpha=0.7))
            ax.text(5, 2.5, "Weighted Combination", ha='center', va='center', fontsize=10)
            
            # Connect predictions to weighted combination
            weights = [0.2, 0.3, 0.5]
            for i, model in enumerate(models):
                y_pos = model["y"] - 2
                ax.arrow(model["x"], y_pos-0.5, 5-model["x"], 2.5-y_pos+0.5, head_width=0.2, head_length=0.2, 
                        fc='black', ec='black', width=0.05, alpha=0.7)
                
                # Weight label
                mid_x = (model["x"] + 5) / 2
                mid_y = (y_pos - 0.5 + 2.5 + 0.5) / 2
                ax.text(mid_x, mid_y, f"w={weights[i]}", ha='center', va='center', 
                       fontsize=8, bbox=dict(facecolor='white', alpha=0.7))
            
            # Final prediction
            ax.add_patch(plt.Rectangle((4, 0.5), 2, 1, fill=True, facecolor='#DCEDC8', 
                                      edgecolor='#689F38', alpha=0.7))
            ax.text(5, 1, "Strong Prediction", ha='center', va='center', fontsize=10)
            
            # Connect weighted combination to final prediction
            ax.arrow(5, 2, 0, -0.5, head_width=0.2, head_length=0.2, 
                    fc='black', ec='black', width=0.05, alpha=0.7)
            
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            ax.set_title("Boosting Ensemble Method")
            
            st.pyplot(fig)

def render_quiz():
    main_title("Knowledge Check")
    
    st.markdown("""
    Test your understanding of Domain 2: ML Model Development concepts with this quiz.
    Select the best answer for each question.
    """)
    
    # Define quiz questions
    questions = [
        {
            "question": "Which Amazon SageMaker model development method requires the least amount of code?",
            "options": ["Using built-in algorithms", "Bring your own script", "Bring your own container", "SageMaker Processing"],
            "correct": "Using built-in algorithms"
        },
        {
            "question": "What is the primary benefit of using SageMaker automatic model tuning?",
            "options": ["It automatically selects the best algorithm for your data", "It finds optimal hyperparameter values by running multiple training jobs", "It reduces the cost of model training", "It automatically deploys the model to production"],
            "correct": "It finds optimal hyperparameter values by running multiple training jobs"
        },
        {
            "question": "Which feature of Amazon Bedrock allows foundation models to incorporate information from your data sources?",
            "options": ["Foundation model fine-tuning", "Continued pretraining", "Retrieval Augmented Generation (RAG)", "Model distillation"],
            "correct": "Retrieval Augmented Generation (RAG)"
        },
        {
            "question": "Which hyperparameter tuning strategy builds a probabilistic model of the objective function based on previous evaluations?",
            "options": ["Grid search", "Random search", "Bayesian optimization", "Evolutionary algorithms"],
            "correct": "Bayesian optimization"
        },
        {
            "question": "In distributed training, what is the main difference between data parallelism and model parallelism?",
            "options": ["Data parallelism splits the dataset across devices while model parallelism splits the model", "Data parallelism is for regression while model parallelism is for classification", "Data parallelism uses CPUs while model parallelism uses GPUs", "Data parallelism is synchronous while model parallelism is asynchronous"],
            "correct": "Data parallelism splits the dataset across devices while model parallelism splits the model"
        }
    ]
    
    # Quiz logic
    if not st.session_state['quiz_attempted']:
        # Form to collect answers
        with st.form("quiz_form"):
            user_answers = {}
            
            for i, q in enumerate(questions):
                st.markdown(f"**Question {i+1}**: {q['question']}")
                user_answers[i] = st.radio(
                    f"Select your answer for question {i+1}:",
                    q['options'],
                    key=f"q{i}"
                )
                st.markdown("---")
            
            submitted = st.form_submit_button("Submit Quiz")
            
            if submitted:
                score = 0
                for i, q in enumerate(questions):
                    if user_answers[i] == q['correct']:
                        score += 1
                
                st.session_state['quiz_score'] = score
                st.session_state['quiz_attempted'] = True
                st.session_state['answers'] = user_answers
                st.rerun()
    else:
        # Show results
        score = st.session_state['quiz_score']
        user_answers = st.session_state['answers']
        
        st.markdown(f"### Your Score: {score}/{len(questions)}")
        
        if score == len(questions):
            st.success("🎉 Perfect score! You've mastered Domain 2 concepts!")
        elif score >= len(questions) * 0.8:
            st.success("👍 Great job! You have a strong understanding of the material.")
        elif score >= len(questions) * 0.6:
            st.warning("🔍 Good effort! Review the concepts you missed to strengthen your understanding.")
        else:
            st.error("📚 You might want to revisit the material to reinforce your understanding.")
        
        # Show detailed results
        st.markdown("### Question Review")
        
        for i, q in enumerate(questions):
            is_correct = user_answers[i] == q['correct']
            result_container = st.container()
            
            with result_container:
                st.markdown(f"**Question {i+1}**: {q['question']}")
                st.markdown(f"Your answer: **{user_answers[i]}**")
                
                if is_correct:
                    st.markdown("**✅ Correct!**")
                else:
                    st.markdown(f"**❌ Incorrect. The correct answer is: {q['correct']}**")
                
                st.markdown("---")
        
        if st.button("Try Again"):
            st.session_state['quiz_attempted'] = False
            st.rerun()

# Main app layout
main_title("AWS Partner Certification Readiness: ML Engineer - Associate")
st.markdown("### Domain 2 - ML Model Development")

# Create tabs with emojis for navigation
tabs = st.tabs([
    "🏠 Introduction", 
    "🔄 ML Lifecycle", 
    "🧠 Modeling Approaches", 
    "🤖 Amazon Bedrock", 
    "🔬 Neural Networks", 
    "🚂 Model Training", 
    "⚙️ Hyperparameters", 
    "🎯 Hyperparameter Tuning", 
    "⚡ Distributed Training", 
    "🌟 Ensemble Learning", 
    "❓ Knowledge Check"
])

# Render content based on tab selection
with tabs[0]:
    render_introduction()
with tabs[1]:
    render_ml_lifecycle()
with tabs[2]:
    render_modeling_approaches()
with tabs[3]:
    render_amazon_bedrock()
with tabs[4]:
    render_neural_networks()
with tabs[5]:
    render_model_training()
with tabs[6]:
    render_hyperparameters()
with tabs[7]:
    render_hyperparameter_tuning()
with tabs[8]:
    render_distributed_training()
with tabs[9]:
    render_ensemble_learning()
with tabs[10]:
    render_quiz()

# Footer
st.markdown("---")
st.markdown("© 2023 AWS Partner Certification Readiness | ML Engineer - Associate | Domain 2: ML Model Development")
