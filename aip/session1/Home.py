import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

def main():
    # Set page configuration
    st.set_page_config(
        page_title="AI Practitioner: Fundamentals of AI and ML",
        page_icon="🧠",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .gradient-header {
        background: linear-gradient(90deg, #232f3e, #ff9900);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    .card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        transition: transform 0.3s ease;
        height: 100%;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .topic-header {
        color: #232f3e;
        font-weight: bold;
        border-bottom: 2px solid #ff9900;
        padding-bottom: 5px;
        margin-bottom: 10px;
    }
    .highlight {
        color: #ff9900;
        font-weight: bold;
    }
    .btn-aws {
        background-color: #ff9900;
        color: white;
        padding: 10px 24px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-weight: bold;
        text-align: center;
        display: inline-block;
        margin: 10px 2px;
        transition: all 0.3s;
    }
    .btn-aws:hover {
        background-color: #ec7211;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
    
    <div class="gradient-header">
        <h1>AWS Partner Certification Readiness</h1>
        <h2>AI Practitioner - Session 1</h2>
        <p>Program Kickoff & Fundamentals of AI and ML</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction section with hero image
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <h2>Welcome to the AWS AI Practitioner Certification Program!</h2>
        <p>This accelerator program is designed to prepare you for the AWS Certified AI Practitioner exam. 
        In our first session, we'll cover <span class="highlight">program overview</span>, 
        <span class="highlight">AWS certification fundamentals</span>, and dive into the 
        <span class="highlight">basics of AI and ML</span>.</p>
        <p>Let's begin your journey toward becoming an AWS Certified AI Practitioner!</p>
        """, unsafe_allow_html=True)
    
    with col2:
        # Create a circular progress indicator
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 1,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Program Progress", 'font': {'size': 24}},
            gauge = {
                'axis': {'range': [None, 4], 'tickwidth': 1, 'tickcolor': "#232f3e", 'tickvals': [1, 2, 3, 4], 'ticktext': ["Session 1", "Session 2", "Session 3", "Session 4"]},
                'bar': {'color': "#ff9900"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#232f3e",
                'steps': [
                    {'range': [0, 1], 'color': '#ff9900'},
                    {'range': [1, 4], 'color': '#ededed'}
                ],
            }
        ))
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)
    
    # Learning outcomes section
    st.markdown("<h2 style='text-align: center; margin-top: 30px;'>Today's Learning Outcomes</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3 class="topic-header">Program Overview</h3>
            <ul>
                <li>Understanding the program structure</li>
                <li>Setting up AWS Partner Network account</li>
                <li>Accessing AWS Skill Builder resources</li>
                <li>Exam registration process</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3 class="topic-header">AI/ML Fundamentals</h3>
            <ul>
                <li>Differences between AI, ML, and Generative AI</li>
                <li>Traditional programming vs. machine learning</li>
                <li>Key AI/ML terminology and concepts</li>
                <li>Self-supervised learning for foundation models</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h3 class="topic-header">ML Use Cases & Lifecycle</h3>
            <ul>
                <li>Common use cases for AI/ML applications</li>
                <li>Understanding the ML development lifecycle</li>
                <li>AWS AI/ML service stack overview</li>
                <li>Amazon SageMaker and AI services</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Visualization of AI/ML concepts
    st.markdown("<h2 style='text-align: center; margin-top: 30px;'>AI & ML Concepts Relationship</h2>", unsafe_allow_html=True)
    
    # Data for Venn diagram-like visualization
    fig = go.Figure()

    # Circles data
    circles = [
        {"x": 0, "y": 0, "size": 1, "name": "Artificial Intelligence", "color": "rgba(35, 47, 62, 0.7)"},
        {"x": 0.5, "y": 0, "size": 0.7, "name": "Machine Learning", "color": "rgba(255, 153, 0, 0.7)"},
        {"x": 0.5, "y": -0.25, "size": 0.4, "name": "Deep Learning", "color": "rgba(0, 134, 211, 0.7)"},
        {"x": 0.5, "y": -0.25, "size": 0.2, "name": "Generative AI", "color": "rgba(220, 47, 2, 0.7)"}
    ]

    # Add each circle
    for circle in circles:
        fig.add_trace(go.Scatter(
            x=[circle["x"]], 
            y=[circle["y"]],
            mode="markers+text",
            marker=dict(
                size=circle["size"]*300, 
                color=circle["color"]
            ),
            text=circle["name"],
            textposition="middle center",
            name=circle["name"],
            hoverinfo="name"
        ))

    # Update layout
    fig.update_layout(
        showlegend=False,
        height=400,
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[-1, 1.5]
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[-0.7, 0.7]
        ),
        margin=dict(l=40, r=40, t=20, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)
    
    # Machine Learning Types
    st.markdown("<h2 style='text-align: center; margin-top: 30px;'>Machine Learning Types</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <div style="text-align: center; font-size: 36px; color: #ff9900;">🔍</div>
            <h3 class="topic-header" style="text-align: center;">Supervised Learning</h3>
            <p>Model trained on labeled data to make predictions or decisions.</p>
            <ul>
                <li><strong>Classification:</strong> Categorizing inputs</li>
                <li><strong>Regression:</strong> Predicting numeric values</li>
                <li><strong>Examples:</strong> Spam detection, price forecasting</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <div style="text-align: center; font-size: 36px; color: #ff9900;">🧩</div>
            <h3 class="topic-header" style="text-align: center;">Unsupervised Learning</h3>
            <p>Finding patterns in unlabeled data without guidance.</p>
            <ul>
                <li><strong>Clustering:</strong> Grouping similar data</li>
                <li><strong>Dimensionality Reduction:</strong> Simplifying data</li>
                <li><strong>Examples:</strong> Customer segmentation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <div style="text-align: center; font-size: 36px; color: #ff9900;">🎮</div>
            <h3 class="topic-header" style="text-align: center;">Reinforcement Learning</h3>
            <p>Learning optimal actions through trial and error.</p>
            <ul>
                <li><strong>Agent:</strong> Makes decisions</li>
                <li><strong>Environment:</strong> Provides feedback</li>
                <li><strong>Examples:</strong> Game AI, robotics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # AWS AI/ML Service Stack
    st.markdown("<h2 style='text-align: center; margin-top: 30px;'>AWS AI/ML Service Stack</h2>", unsafe_allow_html=True)
    
    # Create a stacked bar chart for AWS AI/ML services
    services = {
        'AI Services': ['Amazon Rekognition', 'Amazon Textract', 'Amazon Comprehend', 'Amazon Kendra', 'Amazon Personalize', 'Amazon Fraud Detector'],
        'ML Services': ['Amazon SageMaker Studio', 'SageMaker Notebooks', 'SageMaker Training', 'SageMaker Model Monitoring', 'SageMaker Pipelines'],
        'ML Frameworks & Infrastructure': ['TensorFlow', 'PyTorch', 'MXNet', 'AWS EC2', 'AWS Trainium', 'AWS Inferentia']
    }
    
    categories = list(services.keys())
    colors = ['#ff9900', '#232f3e', '#0073bb']
    
    fig = go.Figure()
    
    for i, category in enumerate(categories):
        fig.add_trace(go.Bar(
            y=[services[category]],
            x=[1],
            name=category,
            orientation='h',
            marker=dict(
                color=colors[i],
                line=dict(color='rgba(0,0,0,0)', width=0)
            ),
            text=[[service for service in services[category]]],
            textposition='inside',
            insidetextanchor='middle',
            width=0.8,
            offset=0
        ))
    
    fig.update_layout(
        barmode='stack',
        height=200,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Digital Training Curriculum
    st.markdown("<h2 style='text-align: center; margin-top: 30px;'>Week 1 Digital Training</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #f5f5f5; border-radius: 10px; padding: 20px; margin-top: 10px;">
        <h3 style="text-align: center;">Complete these courses this week:</h3>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap; margin-top: 20px;">
            <div style="background-color: white; border-radius: 8px; padding: 15px; margin: 10px; width: 200px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="color: #ff9900; font-size: 24px;">📚</div>
                <div style="font-weight: bold;">Fundamentals of Machine Learning and AI</div>
            </div>
            <div style="background-color: white; border-radius: 8px; padding: 15px; margin: 10px; width: 200px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="color: #ff9900; font-size: 24px;">🔍</div>
                <div style="font-weight: bold;">Exploring AI Use Cases and Applications</div>
            </div>
            <div style="background-color: white; border-radius: 8px; padding: 15px; margin: 10px; width: 200px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="color: #ff9900; font-size: 24px;">⚖️</div>
                <div style="font-weight: bold;">Responsible Artificial Practices</div>
            </div>
            <div style="background-color: white; border-radius: 8px; padding: 15px; margin: 10px; width: 200px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="color: #ff9900; font-size: 24px;">🛠️</div>
                <div style="font-weight: bold;">Developing Machine Learning Solutions</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("""
    <div style="text-align: center; margin-top: 40px;">
        <a href="https://aws.amazon.com/certification/certified-ai-practitioner/" target="_blank" class="btn-aws">
            Learn More About the AWS AI Practitioner Certification
        </a>
    </div>
    
    <p style="text-align: center; margin-top: 50px; font-size: 12px; color: #666;">
        © 2025, Amazon Web Services, Inc. or its affiliates. All rights reserved.
    </p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
