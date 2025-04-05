import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Fundamentals of Generative AI",
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
    .icon-box {
        font-size: 24px;
        margin-right: 10px;
    }
    </style>
    
    <div class="gradient-header">
        <h1>Fundamentals of Generative AI</h1>
        <p>AWS Partner Certification Readiness: AI Practitioner - Session 2</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <h2>Welcome to Session 2!</h2>
        <p>In this session, we'll explore <span class="highlight">Domain 2: Fundamentals of Generative AI</span>. 
        You'll learn about foundation models, transformer architectures, and how these powerful technologies
        are reshaping the AI landscape. We'll also examine AWS services and infrastructure that enable
        you to build generative AI applications.</p>
        <p>By the end of this session, you'll understand the core concepts of generative AI, its capabilities 
        and limitations, and the AWS technologies that support it.</p>
        """, unsafe_allow_html=True)
    
    with col2:
        # Create a doughnut chart
        fig = go.Figure(go.Pie(
            labels=["Basic Concepts", "Capabilities & Limitations", "AWS Infrastructure"],
            values=[40, 30, 30],
            hole=.5,
            marker_colors=['#ff9900', '#232F3E', '#00A1C9']
        ))
        fig.update_layout(
            title="Session Topics",
            height=300,
            margin=dict(t=30, b=0, l=0, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Learning Outcomes Section
    st.markdown("<h2 style='text-align: center; margin-top: 20px;'>Learning Outcomes</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4 class="topic-header"><span class="icon-box">🧩</span>2.1: Basic Concepts of Generative AI</h4>
            <ul>
                <li>Foundation models and their components</li>
                <li>Transformer architecture and attention mechanisms</li>
                <li>Text-to-text and text-to-image models</li>
                <li>Tokenization, embeddings, and decoding processes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4 class="topic-header"><span class="icon-box">⚖️</span>2.2: Capabilities and Limitations</h4>
            <ul>
                <li>Inference parameters (temperature, top_p, top_k)</li>
                <li>Context and token limitations</li>
                <li>Addressing concerns: toxicity, hallucinations</li>
                <li>Intellectual property and ethical considerations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h4 class="topic-header"><span class="icon-box">🔧</span>2.3: AWS Infrastructure & Technologies</h4>
            <ul>
                <li>AWS Generative AI stack overview</li>
                <li>Amazon Bedrock and SageMaker</li>
                <li>Specialized hardware: AWS Trainium & Inferentia</li>
                <li>AWS AI services for building applications</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Foundation Models Visualization
    st.markdown("<h2 style='text-align: center; margin-top: 30px;'>Foundation Models</h2>", unsafe_allow_html=True)
    
    # Data for the visualization
    model_types = ["Text-to-Text", "Text-to-Image"]
    use_cases = [
        ["Summarization", "Q&A", "Content Creation", "Translation", "Code Generation"],
        ["Art Creation", "Product Visualization", "Design Prototyping", "Marketing Materials"]
    ]
    
    fig = go.Figure()
    
    for i, model_type in enumerate(model_types):
        for j, use_case in enumerate(use_cases[i]):
            fig.add_trace(go.Scatter(
                x=[i],
                y=[j],
                mode="markers+text",
                marker=dict(size=40, color=["#ff9900", "#00A1C9"][i]),
                text=use_case,
                name=f"{model_type}: {use_case}",
                textposition="middle center",
                hoverinfo="name"
            ))
    
    fig.update_layout(
        title="Foundation Model Types and Use Cases",
        xaxis=dict(
            tickmode="array",
            tickvals=[0, 1],
            ticktext=model_types,
            title=""
        ),
        yaxis=dict(
            showticklabels=False,
            title=""
        ),
        showlegend=False,
        height=400,
        width=800
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Transformer Architecture Section
    st.markdown("<h2 style='text-align: center; margin-top: 30px;'>Transformer Architecture</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4 class="topic-header">Key Benefits</h4>
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="background-color: #ff9900; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin-right: 15px; color: white; font-weight: bold;">1</div>
                <div><strong>Parallel Processing</strong> - Process entire sequences simultaneously</div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="background-color: #ff9900; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin-right: 15px; color: white; font-weight: bold;">2</div>
                <div><strong>Attention Mechanism</strong> - Focus on relevant parts of input</div>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="background-color: #ff9900; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin-right: 15px; color: white; font-weight: bold;">3</div>
                <div><strong>Flexibility & Scalability</strong> - Adapt to multiple modalities</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Simple animated transformer process visualization
        st.markdown("""
        <div class="card" style="padding: 0; overflow: hidden;">
            <div style="background-color: #f5f5f5; padding: 20px; text-align: center;">
                <div style="font-size: 18px; margin-bottom: 10px;">Transformer Process Flow</div>
                <div style="display: flex; justify-content: space-around; align-items: center; animation: pulse 2s infinite;">
                    <div style="background-color: #232f3e; color: white; padding: 10px; border-radius: 5px; width: 20%;">Input</div>
                    <div style="font-size: 24px;">→</div>
                    <div style="background-color: #ff9900; color: white; padding: 10px; border-radius: 5px; width: 20%;">Encode</div>
                    <div style="font-size: 24px;">→</div>
                    <div style="background-color: #00A1C9; color: white; padding: 10px; border-radius: 5px; width: 20%;">Attend</div>
                    <div style="font-size: 24px;">→</div>
                    <div style="background-color: #232f3e; color: white; padding: 10px; border-radius: 5px; width: 20%;">Output</div>
                </div>
            </div>
            <style>
            @keyframes pulse {
                0% { opacity: 0.7; }
                50% { opacity: 1; }
                100% { opacity: 0.7; }
            }
            </style>
        </div>
        """, unsafe_allow_html=True)
    
    # Model Inference Parameters
    st.markdown("<h2 style='text-align: center; margin-top: 30px;'>Model Inference Parameters</h2>", unsafe_allow_html=True)
    
    param_data = pd.DataFrame({
        'Parameter': ['Temperature', 'Top P', 'Top K', 'Response Length', 'Stop Sequences'],
        'Function': ['Controls randomness', 'Limits token probability pool', 'Limits number of tokens', 'Sets output length', 'Terminates generation'],
        'Default': ['Low (0-1)', 'High (0.9-1)', 'Varies by model', 'Model specific', 'None'],
        'Effect': ['Higher increases creativity', 'Lower increases focus', 'Lower increases focus', 'Longer may cost more', 'Custom control']
    })
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(param_data.columns),
            fill_color='#232f3e',
            align='center',
            font=dict(color='white', size=14)
        ),
        cells=dict(
            values=[param_data[k].tolist() for k in param_data.columns],
            fill_color=[['#f5f5f5', '#ffffff']*5],
            align='left'
        )
    )])
    
    fig.update_layout(
        height=300,
        margin=dict(l=5, r=5, b=10, t=10),
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # AWS Generative AI Stack
    st.markdown("<h2 style='text-align: center; margin-top: 30px;'>AWS Generative AI Stack</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4 class="topic-header">Applications</h4>
            <ul style="list-style-type: none; padding-left: 0;">
                <li>🤖 Amazon Q Business</li>
                <li>🛠️ Amazon Q Developer</li>
                <li>📊 Amazon Q in QuickSight</li>
                <li>📞 Amazon Q in Connect</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4 class="topic-header">Tools</h4>
            <ul style="list-style-type: none; padding-left: 0;">
                <li>🧩 Amazon Bedrock</li>
                <li>📋 SageMaker JumpStart</li>
                <li>🔒 Guardrails</li>
                <li>🎮 PartyRock</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h4 class="topic-header">Infrastructure</h4>
            <ul style="list-style-type: none; padding-left: 0;">
                <li>🖥️ EC2 Instances</li>
                <li>🔥 AWS Trainium</li>
                <li>⚡ AWS Inferentia</li>
                <li>🔄 SageMaker Training Jobs</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Model Customization Approaches
    st.markdown("<h2 style='text-align: center; margin-top: 30px;'>Model Customization Approaches</h2>", unsafe_allow_html=True)
    
    # Create data for customization approaches
    approaches = ["Prompt Engineering", "RAG", "Fine-tuning", "Continued Pretraining"]
    complexity = [1, 2, 3, 4]
    cost = [1, 2, 3, 4]
    time = [1, 2, 3, 4]
    
    fig = px.bar(
        x=approaches,
        y=[complexity, cost, time],
        labels={'value': 'Relative Scale', 'x': 'Approach', 'variable': 'Metric'},
        color_discrete_sequence=["#ff9900", "#232F3E", "#00A1C9"],
        barmode='group',
        title="Comparison of Model Customization Approaches"
    )
    
    fig.update_layout(
        legend_title_text='',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        height=400
    )
    
    # Update the names in the legend
    fig.data[0].name = 'Complexity'
    fig.data[1].name = 'Cost'
    fig.data[2].name = 'Time Required'
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Digital Training Curriculum
    st.markdown("""
    <div style="background-color: #f5f5f5; border-radius: 10px; padding: 20px; margin-top: 30px; text-align: center;">
        <h3>This Week's Digital Training Curriculum</h3>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap; margin-top: 20px;">
            <div style="background-color: white; border-radius: 8px; padding: 15px; margin: 10px; width: 180px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="color: #ff9900; font-size: 24px;">📝</div>
                <div style="font-weight: bold;">Essentials of Prompt Engineering</div>
            </div>
            <div style="background-color: white; border-radius: 8px; padding: 15px; margin: 10px; width: 180px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="color: #ff9900; font-size: 24px;">🔧</div>
                <div style="font-weight: bold;">Optimizing Foundation Models</div>
            </div>
            <div style="background-color: white; border-radius: 8px; padding: 15px; margin: 10px; width: 180px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="color: #ff9900; font-size: 24px;">🔒</div>
                <div style="font-weight: bold;">Security, Compliance, and Governance</div>
            </div>
            <div style="background-color: white; border-radius: 8px; padding: 15px; margin: 10px; width: 180px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="color: #ff9900; font-size: 24px;">👔</div>
                <div style="font-weight: bold;">Generative AI for Executives</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <p style="text-align: center; margin-top: 50px; font-size: 12px; color: #666;">
        © 2025, Amazon Web Services, Inc. or its affiliates. All rights reserved.
    </p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
