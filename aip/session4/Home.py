
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Responsible AI & Security",
        page_icon="🛡️",
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
    .badge {
        background-color: #ff9900;
        color: white;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 14px;
        margin-right: 8px;
    }
        ul {
        margin-left: 20px;
        margin-top: 10px;
    }
    li {
        margin-bottom: 5px;
    }
    </style>
    
    <div class="gradient-header">
        <h1>Responsible AI & Security Framework</h1>
        <p>AWS Partner Certification Readiness: AI Practitioner - Session 4</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction section with hero graphic
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <h2>Welcome to the Final Session!</h2>
        <p>In our culminating session, we'll explore <span class="highlight">Domains 4 & 5</span>, focusing on 
        guidelines for responsible AI and the crucial aspects of security, compliance, and governance 
        for AI solutions.</p>
        <p>As AI systems become increasingly integrated into critical applications, understanding how to 
        develop these systems responsibly and securely is essential for every AI practitioner.</p>
        """, unsafe_allow_html=True)
    
    with col2:
        # Create a circular gauge chart for session progress
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Program Progress", 'font': {'size': 24}},
            delta = {'reference': 75, 'increasing': {'color': "green"}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#ff9900"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#232f3e",
                'steps': [
                    {'range': [0, 25], 'color': '#e6f2ff'},
                    {'range': [25, 50], 'color': '#cce5ff'},
                    {'range': [50, 75], 'color': '#99ccff'},
                    {'range': [75, 100], 'color': '#80bfff'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 100
                }
            }
        ))
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    # Learning Outcomes Section
    st.markdown("<h2 style='text-align: center; margin-top: 20px;'>Learning Outcomes</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4 class="topic-header">Domain 4: Guidelines for Responsible AI</h4>
            
            <div style="margin-bottom: 15px;">
                <span class="badge">4.1</span> <strong>Explain Responsible AI Systems Development</strong>
                <ul>
                    <li>Dataset bias identification & mitigation</li>
                    <li>Model bias vs. variance tradeoffs</li>
                    <li>Human-in-the-loop with Amazon Augmented AI</li>
                    <li>SageMaker Clarify for bias detection</li>
                    <li>Model monitoring and governance</li>
                </ul>
            </div>
            
            <div>
                <span class="badge">4.2</span> <strong>Transparent & Explainable Models</strong>
                <ul>
                    <li>Transparency vs. explainability concepts</li>
                    <li>Model documentation with SageMaker Model Cards</li>
                    <li>Human-centered AI design practices</li>
                    <li>Balancing AI and human judgment</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4 class="topic-header">Domain 5: Security, Compliance & Governance</h4>
            
            <div style="margin-bottom: 15px;">
                <span class="badge">5.1</span> <strong>Securing AI Systems</strong>
                <ul>
                    <li>AWS identity and access management</li>
                    <li>Data encryption with AWS KMS</li>
                    <li>Network isolation with Amazon VPC</li>
                    <li>Privacy protection with Amazon Macie</li>
                    <li>Secure private connectivity with AWS PrivateLink</li>
                </ul>
            </div>
            
            <div>
                <span class="badge">5.2</span> <strong>Governance & Compliance Regulations</strong>
                <ul>
                    <li>AI standards compliance</li>
                    <li>Defense in depth security strategy</li>
                    <li>Data governance for AI workloads</li>
                    <li>AWS security monitoring services</li>
                    <li>Generative AI Security Scoping Matrix</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Responsible AI Framework Visualization
    st.markdown("<h2 style='text-align: center; margin-top: 30px;'>Responsible AI Framework</h2>", unsafe_allow_html=True)
    
    # Data for the radar chart
    categories = ['Fairness', 'Explainability', 'Controllability', 
                  'Privacy & Security', 'Governance', 'Transparency',
                  'Safety', 'Veracity & Robustness']
    
    fig = go.Figure()
    
    # Adding first trace (Current State)
    fig.add_trace(go.Scatterpolar(
        r=[4, 3, 5, 4, 3, 4, 5, 3],
        theta=categories,
        fill='toself',
        name='Current State',
        line_color='#ff9900'
    ))
    
    # Adding second trace (Target State)
    fig.add_trace(go.Scatterpolar(
        r=[5, 5, 5, 5, 5, 5, 5, 5],
        theta=categories,
        fill='toself',
        name='Target State',
        line_color='#232f3e'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=True,
        height=500,
        margin=dict(l=80, r=80, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # AWS Security Services for AI
    st.markdown("<h2 style='text-align: center; margin-top: 30px;'>AWS Security Services for AI Systems</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <div style="text-align: center; font-size: 36px; color: #ff9900; margin-bottom: 10px;">🔐</div>
            <h4 class="topic-header" style="text-align: center;">Identity & Access</h4>
            <ul>
                <li><strong>AWS IAM</strong> - Fine-grained access control</li>
                <li><strong>AWS KMS</strong> - Encryption key management</li>
                <li><strong>SageMaker Role Manager</strong> - ML-specific permissions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <div style="text-align: center; font-size: 36px; color: #ff9900; margin-bottom: 10px;">📊</div>
            <h4 class="topic-header" style="text-align: center;">Monitoring & Governance</h4>
            <ul>
                <li><strong>CloudWatch</strong> - Resource monitoring</li>
                <li><strong>CloudTrail</strong> - API activity tracking</li>
                <li><strong>AWS Config</strong> - Configuration management</li>
                <li><strong>SageMaker Model Dashboard</strong> - Model oversight</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <div style="text-align: center; font-size: 36px; color: #ff9900; margin-bottom: 10px;">🔍</div>
            <h4 class="topic-header" style="text-align: center;">Compliance & Audit</h4>
            <ul>
                <li><strong>Amazon Inspector</strong> - Vulnerability scanning</li>
                <li><strong>AWS Audit Manager</strong> - Controls assessment</li>
                <li><strong>AWS Artifact</strong> - Compliance reports</li>
                <li><strong>AWS Trusted Advisor</strong> - Best practice checks</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Defense in Depth Visualization
    st.markdown("<h2 style='text-align: center; margin-top: 30px;'>Defense in Depth for AI Systems</h2>", unsafe_allow_html=True)
    
    # Create stacked concentric circles visualization
    layers = ['User Access & Identity', 'Application Security', 'Data Security', 
              'Model Security', 'Network Security', 'Infrastructure Security', 'Physical Security']
    
    colors = px.colors.sequential.Oranges_r
    
    # Create data for the visualization
    layer_data = []
    for i, layer in enumerate(layers):
        layer_data.append(dict(
            values=[100],
            labels=[layer],
            domain=dict(x=[0, 1], y=[0, 1]),
            name=layer,
            hoverinfo='label',
            hole=(len(layers) - i) / len(layers),
            type='pie',
            textinfo='label',
            textposition='inside',
            textfont=dict(size=14, color='white'),
            marker=dict(colors=[colors[i]]),
            sort=False
        ))
    
    # Create the figure with all layers
    fig = go.Figure(data=layer_data)
    
    fig.update_layout(
        showlegend=False,
        height=500,
        annotations=[dict(text='AI Asset', x=0.5, y=0.5, font_size=20, showarrow=False)],
        margin=dict(t=0, b=0, l=20, r=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Best Practices & Resources
    st.markdown("<h2 style='text-align: center; margin-top: 30px;'>Best Practices & Key Takeaways</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4 class="topic-header">Responsible AI Best Practices</h4>
            <ol>
                <li><strong>Assess risk on a case-by-case basis</strong> - Different use cases have different risk profiles</li>
                <li><strong>Put your people first</strong> - Invest in education and awareness</li>
                <li><strong>Iterate across the AI lifecycle</strong> - Continuously improve and adapt</li>
                <li><strong>Test thoroughly and often</strong> - Rigorous testing for bias and accuracy</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4 class="topic-header">Final Digital Training Curriculum</h4>
            <p>Complete your journey with these final resources:</p>
            <ul>
                <li><strong>Amazon Bedrock Getting Started</strong></li>
                <li><strong>Exam Prep Standard Course: AWS Certified AI Practitioner</strong></li>
                <li><strong>CloudQuest: Generative AI</strong> (Enhanced Track)</li>
                <li><strong>Getting Started with Amazon Comprehend: Custom Classification</strong></li>
                <li><strong>Official Pretest</strong> (Enhanced Exam Prep Plan)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer with call to action
    st.markdown("""
    <div style="background-color: #f5f5f5; border-radius: 10px; padding: 20px; margin-top: 30px; text-align: center;">
        <h3 style="color: #232f3e;">Ready for Your AWS AI Practitioner Certification?</h3>
        <p>You've completed all sessions! Focus on reviewing key concepts and practicing with sample questions.</p>
        <p>Visit the <a href="https://aws.amazon.com/certification/certified-ai-practitioner/" target="_blank">AWS Certified AI Practitioner</a> page for more resources</p>
    </div>
    
    <p style="text-align: center; margin-top: 50px; font-size: 12px; color: #666;">
        © 2025, Amazon Web Services, Inc. or its affiliates. All rights reserved.
    </p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
