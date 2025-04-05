import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Applications of Foundation Models",
        page_icon="🤖",
        layout="wide"
    )
    
    # Header with gradient
    st.markdown("""
        <style>
        .gradient-header {
            background: linear-gradient(90deg, #4b79a1, #283e51);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .topic-header {
            color: #4b79a1;
            font-weight: bold;
        }
        </style>
        <div class="gradient-header">
            <h1>Applications of Foundation Models</h1>
            <h3>AWS Partner Certification Readiness: AI Practitioner - Session 3</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Introduction
    st.markdown("### Welcome to Session 3 of the AWS AI Practitioner certification readiness program!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        In today's session, we'll explore Domain 3: Applications of Foundation Models. 
        This important domain covers how foundation models can be effectively applied 
        in real-world scenarios, including design considerations, prompt engineering 
        techniques, training methodologies, and performance evaluation.
        
        By the end of this session, you'll have a solid understanding of how to 
        leverage foundation models in practical applications and prepare for the 
        related exam questions.
        """)
    
    with col2:
        # Create a simple visualization
        fig = px.pie(
            values=[30, 25, 25, 20],
            names=['Prompt Engineering', 'Model Design', 'Fine-tuning', 'Evaluation'],
            title='Session Topics Distribution',
            color_discrete_sequence=px.colors.sequential.Blues_r,
            hole=0.4
        )
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
        st.plotly_chart(fig, use_container_width=True)
    
    # Learning Outcomes
    st.markdown("## 📚 Today's Learning Outcomes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4 class="topic-header">Task Statement 3.1</h4>
            <p>Describe design considerations for applications that use foundation models</p>
            <ul>
                <li>Retrieval Augmented Generation (RAG)</li>
                <li>Vector databases and semantic search</li>
                <li>Knowledge Bases for Amazon Bedrock</li>
                <li>Guardrails and safety considerations</li>
            </ul>
        </div>
        
        <div class="card">
            <h4 class="topic-header">Task Statement 3.2</h4>
            <p>Choose effective prompt engineering techniques</p>
            <ul>
                <li>Elements of a prompt</li>
                <li>Zero-shot, few-shot, and chain-of-thought prompting</li>
                <li>Prompt injection and leaking</li>
                <li>Prompt templating</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4 class="topic-header">Task Statement 3.3</h4>
            <p>Describe the training and fine-tuning process for foundation models</p>
            <ul>
                <li>Common approaches for customizing FMs</li>
                <li>Data preparation for fine-tuning</li>
                <li>Reinforcement Learning from Human Feedback (RLHF)</li>
            </ul>
        </div>
        
        <div class="card">
            <h4 class="topic-header">Task Statement 3.4</h4>
            <p>Describe methods to evaluate foundation model performance</p>
            <ul>
                <li>Foundation Model Evaluations with Amazon SageMaker Clarify</li>
                <li>Amazon Bedrock model evaluation</li>
                <li>Evaluation metrics: ROUGE, BLEU, BERTScore, F1 score</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Create a visualization of the model customization approaches
    st.markdown("## 📊 Foundation Model Customization Approaches")
    
    # Data for the chart
    approaches = ["Prompt Engineering", "RAG", "Fine-tuning", "Continued Pretraining"]
    complexity = [1, 2, 3, 4]
    cost = [1, 2, 3, 4]
    time = [1, 2, 3, 4]
    
    df = pd.DataFrame({
        "Approach": approaches,
        "Complexity": complexity,
        "Cost": cost,
        "Time Required": time
    })
    
    # Create a radar chart
    fig = px.line_polar(
        df, 
        r="Complexity", 
        theta="Approach", 
        line_close=True,
        color_discrete_sequence=["#4b79a1"]
    )
    fig.update_traces(fill='toself', opacity=0.6)
    
    fig.update_layout(
        title="Foundation Model Customization: Complexity by Approach",
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # AWS Services section
    st.markdown("## 🚀 Key AWS Services for Foundation Models")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card" style="height: 200px;">
            <h4 class="topic-header">Amazon Bedrock</h4>
            <p>Fully managed service for building and scaling generative AI applications with foundation models</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card" style="height: 200px;">
            <h4 class="topic-header">Amazon SageMaker Clarify</h4>
            <p>Tool for evaluating model performance and detecting bias in machine learning models</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card" style="height: 200px;">
            <h4 class="topic-header">Knowledge Bases for Amazon Bedrock</h4>
            <p>Securely connects foundation models to data sources for Retrieval Augmented Generation</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    ---
    ### 📝 Digital Training Curriculum
    
    Don't forget to complete this week's training content:
    - Amazon Bedrock Getting Started
    - Exam Prep Standard Course: AWS Certified AI Practitioner
    - CloudQuest: Generative AI (optional enhanced track)
    - Getting Started with Amazon Comprehend: Custom Classification lab
    """)

if __name__ == "__main__":
    main()
