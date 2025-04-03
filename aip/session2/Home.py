# Streamlit AI Learning Hub - Single Page Landing Page

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
import numpy as np

# Page configuration
st.set_page_config(
    page_title="AI Learning Hub",
    page_icon="🧠",
    layout="wide",
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main styles */
    .main {
        background-color: #f8f9fa;
        color: #212529;
        padding: 0 !important;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 1200px;
    }
    
    /* Hero section */
    .hero-container {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        padding: 4rem 2rem;
        border-radius: 0px;
        margin-top: -1rem;
        margin-left: -4rem;
        margin-right: -4rem;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .hero-title {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }
    
    .hero-subtitle {
        font-size: 1.5rem !important;
        opacity: 0.9;
        margin-bottom: 2rem;
    }
    
    /* Card styles */
    .course-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    
    .course-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
    }
    
    .card-title {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #4338CA;
        margin-bottom: 0.75rem !important;
    }
    
    .card-text {
        font-size: 1rem;
        color: #4B5563;
        margin-bottom: 1rem;
    }
    
    .topic-tag {
        display: inline-block;
        background-color: #EEF2FF;
        color: #4338CA;
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-size: 0.875rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Section styles */
    .section-container {
        padding: 3rem 0;
        border-bottom: 1px solid #E5E7EB;
    }
    
    .section-title {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 2rem !important;
        text-align: center;
        color: #1F2937;
    }
    
    .section-subtitle {
        font-size: 1.7rem !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
        color: #4338CA;
    }
    
    /* For content boxes */
    .content-box {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
        height: 100%;
    }
    
    /* Icon style */
    .icon-display {
        font-size: 2rem;
        margin-bottom: 1rem;
        color: #4F46E5;
    }
    
    .highlight-box {
        background-color: #EEF2FF;
        border-left: 4px solid #4F46E5;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    /* CTA button */
    .cta-button {
        background-color: #4F46E5;
        color: white;
        font-weight: bold;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        display: inline-block;
        text-align: center;
        text-decoration: none;
        margin-top: 1rem;
        transition: background-color 0.3s;
    }
    
    .cta-button:hover {
        background-color: #4338CA;
    }
    
    /* Feature list */
    .feature-list {
        list-style-type: none;
        padding-left: 0.5rem;
    }
    
    .feature-list li {
        margin-bottom: 0.7rem;
        position: relative;
        padding-left: 1.5rem;
    }
    
    .feature-list li:before {
        content: "✓";
        color: #4F46E5;
        font-weight: bold;
        position: absolute;
        left: 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        margin-top: 2rem;
        background-color: #1F2937;
        color: white;
        margin-left: -4rem;
        margin-right: -4rem;
        margin-bottom: -3rem;
    }
    
    /* Progress meter */
    .progress-label {
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 0.25rem;
        color: #4B5563;
    }
    
    .progress-container {
        height: 8px;
        background-color: #E5E7EB;
        border-radius: 4px;
        margin-bottom: 1rem;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #818CF8 0%, #4F46E5 100%);
        border-radius: 4px;
    }
    
    /* Section separator */
    .section-separator {
        height: 4px;
        background: linear-gradient(90deg, #818CF8, #4F46E5);
        border-radius: 2px;
        margin: 3rem auto;
        width: 100px;
    }
    
    /* Tab styling */
    .stTabs {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        padding: 1rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 16px;
        border-radius: 4px 4px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #EEF2FF !important;
        color: #4338CA !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Function to create transformer diagram
def create_transformer_diagram():
    # Creating a simplified transformer architecture diagram with Plotly
    fig = go.Figure()
    
    # Define components
    components = [
        "Input Embedding", "Positional Encoding", 
        "Multi-Head Attention", "Add & Normalize", 
        "Feed Forward Network", "Add & Normalize", 
        "Output Embedding"
    ]
    
    y_positions = list(range(len(components), 0, -1))
    
    # Add components as rectangles
    for i, (comp, y) in enumerate(zip(components, y_positions)):
        color = "#6366F1" if "Attention" in comp else "#8B5CF6"
        
        fig.add_shape(
            type="rect",
            x0=0.2, y0=y-0.4, x1=0.8, y1=y+0.4,
            line=dict(color=color, width=2),
            fillcolor="rgba(99, 102, 241, 0.1)" if "Attention" in comp else "rgba(139, 92, 246, 0.1)",
        )
        
        fig.add_annotation(
            x=0.5, y=y,
            text=comp,
            showarrow=False,
            font=dict(color="#1F2937", size=12)
        )
        
        # Add arrows connecting components
        if i < len(components) - 1:
            fig.add_shape(
                type="line",
                x0=0.5, y0=y-0.5, x1=0.5, y1=y-0.9,
                line=dict(color="#4B5563", width=2, dash="dot"),
                layer="below"
            )
            fig.add_annotation(
                x=0.5, y=y-0.7,
                text="→",
                showarrow=False,
                font=dict(color="#4B5563", size=16)
            )
            
    # Set layout
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        width=350,
        height=500,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
    )
    
    return fig

# Function to create tokenization visualization
def create_tokenization_viz():
    sentence = "The transformer model has revolutionized natural language processing."
    tokens = ["The", "transform", "##er", "model", "has", "revolution", "##ized", "natural", "language", "processing", "."]
    
    colors = ["#818CF8", "#818CF8", "#C7D2FE", "#818CF8", "#818CF8", "#818CF8", 
              "#C7D2FE", "#818CF8", "#818CF8", "#818CF8", "#818CF8"]
    
    fig = go.Figure()
    
    y_base = 1
    x_start = 0
    text_width = 0.08
    
    # Add the original sentence
    fig.add_annotation(
        x=0.5, y=2,
        text=f"Original text: \"{sentence}\"",
        showarrow=False,
        font=dict(size=14, color="#1F2937"),
        xanchor="center"
    )
    
    # Add arrow pointing down
    fig.add_annotation(
        x=0.5, y=1.6,
        text="↓ Tokenization",
        showarrow=False,
        font=dict(size=14, color="#4338CA"),
        xanchor="center"
    )
    
    # Add tokens as colored rectangles
    for i, (token, color) in enumerate(zip(tokens, colors)):
        token_len = len(token) * text_width
        
        # Add rectangle for token
        fig.add_shape(
            type="rect",
            x0=x_start, y0=y_base-0.3, 
            x1=x_start + token_len, y1=y_base+0.3,
            line=dict(color="#4338CA", width=1),
            fillcolor=color,
        )
        
        # Add token text
        fig.add_annotation(
            x=x_start + token_len/2, y=y_base,
            text=token,
            showarrow=False,
            font=dict(size=12, color="#1F2937")
        )
        
        x_start += token_len + 0.02
    
    # Set layout
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        width=700,
        height=200,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0, x_start]),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0, 2.5])
    )
    
    return fig

# Function to visualize word vectors
def create_word_vector_viz():
    # Create some sample word vectors in 2D space
    np.random.seed(42)
    words = ["king", "queen", "man", "woman", "doctor", "nurse", "actor", "actress", 
             "programmer", "engineer", "teacher", "student"]
    
    # Create realistic-looking 2D word vectors with some semantic patterns
    vectors = [
        [2.1, 2.2],   # king
        [2.0, 1.3],   # queen
        [1.2, 2.1],   # man
        [1.1, 1.2],   # woman
        [0.2, 1.8],   # doctor
        [0.1, 0.9],   # nurse
        [-1.0, 1.7],  # actor
        [-1.1, 0.8],  # actress
        [-1.9, -0.9], # programmer
        [-1.7, -0.2], # engineer
        [-0.5, -1.5], # teacher
        [-0.3, -2.0]  # student
    ]
    
    # Define categories for coloring
    categories = ["royalty", "royalty", "gender", "gender", "medical", "medical", 
                 "entertainment", "entertainment", "technical", "technical", "education", "education"]
    
    # Create dataframe
    df = pd.DataFrame({
        "word": words,
        "x": [v[0] for v in vectors],
        "y": [v[1] for v in vectors],
        "category": categories
    })
    
    # Create scatter plot
    fig = px.scatter(df, x="x", y="y", color="category", text="word",
                    color_discrete_sequence=["#8B5CF6", "#EC4899", "#3B82F6", "#10B981", "#F59E0B", "#EF4444"])
    
    # Update traces to adjust text position
    fig.update_traces(textposition='top center', marker=dict(size=10))
    
    # Add vector arrows for some interesting relationships
    # King - Man + Woman = Queen
    fig.add_shape(type="line", x0=df.loc[df['word'] == 'king', 'x'].iloc[0], 
                 y0=df.loc[df['word'] == 'king', 'y'].iloc[0],
                 x1=df.loc[df['word'] == 'queen', 'x'].iloc[0], 
                 y1=df.loc[df['word'] == 'queen', 'y'].iloc[0],
                 line=dict(color="#EC4899", width=2, dash="dash"))
    
    fig.add_shape(type="line", x0=df.loc[df['word'] == 'man', 'x'].iloc[0], 
                 y0=df.loc[df['word'] == 'man', 'y'].iloc[0],
                 x1=df.loc[df['word'] == 'woman', 'x'].iloc[0], 
                 y1=df.loc[df['word'] == 'woman', 'y'].iloc[0],
                 line=dict(color="#3B82F6", width=2, dash="dash"))
    
    # Update layout
    fig.update_layout(
        title="Word Vectors in 2D Space",
        plot_bgcolor='rgba(0,0,0,0)',
        width=600,
        height=400,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )
    
    return fig

# Function to create context visualization
def create_context_viz():
    # Example text
    text = "The model uses context to understand meaning."
    context_size = 5
    
    # Create dataframe for visualization
    words = text.split()
    df = pd.DataFrame({
        "word": words,
        "position": list(range(len(words)))
    })
    
    fig = go.Figure()
    
    # Target word position (we'll highlight "context")
    target_pos = 2
    
    # Add rectangles for each word
    for i, word in enumerate(words):
        # Determine color based on whether it's in context window
        if i == target_pos:
            color = "#4338CA"  # Target word color
            opacity = 0.9
            font_color = "white"
        elif abs(i - target_pos) <= context_size:
            color = "#818CF8"  # Context words color
            opacity = 0.5 + 0.3 * (1 - abs(i - target_pos) / context_size)
            font_color = "#1F2937"
        else:
            color = "#E5E7EB"  # Out of context words color
            opacity = 0.3
            font_color = "#6B7280"
        
        # Add rectangle for the word
        fig.add_shape(
            type="rect",
            x0=i - 0.4, y0=0.6, x1=i + 0.4, y1=1.4,
            line=dict(color=color, width=2),
            fillcolor=f"rgba({','.join(str(int(c)) for c in px.colors.hex_to_rgb(color))}, {opacity})"
        )
        
        # Add word text
        fig.add_annotation(
            x=i, y=1,
            text=word,
            showarrow=False,
            font=dict(color=font_color, size=14)
        )
    
    # Add context window annotation
    context_start = max(0, target_pos - context_size)
    context_end = min(len(words) - 1, target_pos + context_size)
    
    fig.add_shape(
        type="rect",
        x0=context_start - 0.5, y0=0.4, x1=context_end + 0.5, y1=1.6,
        line=dict(color="#4338CA", width=2, dash="dash"),
        fillcolor="rgba(0,0,0,0)"
    )
    
    fig.add_annotation(
        x=(context_start + context_end) / 2, y=0.3,
        text="Context Window",
        showarrow=False,
        font=dict(color="#4338CA", size=14)
    )
    
    # Set layout
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        width=700,
        height=200,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-1, len(words)]),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0, 2])
    )
    
    return fig

# Function to create masked language model visualization
def create_masked_lm_viz():
    # Example text with mask
    text = "The [MASK] model learns by predicting missing words."
    
    fig = go.Figure()
    
    # Add text as individual word boxes
    words = text.split()
    x_start = 0
    text_width = 0.15
    y_pos = 1
    
    for i, word in enumerate(words):
        # Special styling for [MASK] token
        if word == "[MASK]":
            rect_color = "#4338CA"
            text_color = "white"
            fill_opacity = 0.9
            border_width = 2
        else:
            rect_color = "#818CF8"
            text_color = "#1F2937"
            fill_opacity = 0.2
            border_width = 1
            
        word_len = len(word) * text_width
        
        # Add rectangle
        fig.add_shape(
            type="rect",
            x0=x_start, y0=y_pos-0.3, x1=x_start + word_len, y1=y_pos+0.3,
            line=dict(color=rect_color, width=border_width),
            fillcolor=f"rgba({','.join(str(int(c)) for c in px.colors.hex_to_rgb(rect_color))}, {fill_opacity})"
        )
        
        # Add word text
        fig.add_annotation(
            x=x_start + word_len/2, y=y_pos,
            text=word,
            showarrow=False,
            font=dict(color=text_color, size=14)
        )
        
        x_start += word_len + 0.05
        
    # Add predictions below the masked word
    mask_pos = 1  # Position of [MASK] in the sentence
    mask_x = (mask_pos * text_width * 5) + (mask_pos * 0.05) + (text_width * 2.5)
    
    predictions = [("transformer", 0.85), ("language", 0.08), ("neural", 0.05), ("masked", 0.02)]
    
    # Add arrow
    fig.add_shape(
        type="line",
        x0=mask_x, y0=y_pos - 0.4, x1=mask_x, y1=y_pos - 0.7,
        line=dict(color="#4338CA", width=2)
    )
    
    # Add predictions with probabilities
    for i, (pred, prob) in enumerate(predictions):
        y_pred = y_pos - 1.0 - (i * 0.5)
        
        # Add rectangle for prediction
        rect_width = len(pred) * text_width
        fig.add_shape(
            type="rect",
            x0=mask_x - rect_width/2, y0=y_pred-0.2, x1=mask_x + rect_width/2, y1=y_pred+0.2,
            line=dict(color="#4338CA" if i == 0 else "#818CF8", width=1),
            fillcolor=f"rgba({','.join(str(int(c)) for c in px.colors.hex_to_rgb('#4338CA'))}, {0.8 if i == 0 else 0.2})"
        )
        
        # Add text
        fig.add_annotation(
            x=mask_x, y=y_pred,
            text=f"{pred} ({prob:.0%})",
            showarrow=False,
            font=dict(color="white" if i == 0 else "#1F2937", size=12)
        )
    
    # Add BERT Prediction text
    fig.add_annotation(
        x=mask_x, y=y_pos - 0.85,
        text="Predictions:",
        showarrow=False,
        font=dict(color="#4338CA", size=14, weight="bold" )
    )
    
    # Set layout
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        width=700,
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-3, 2])
    )
    
    return fig

# Main content
# ============ Hero Section ============
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">Fundamentals of Generative AI</h1>
    <p class="hero-subtitle">Learn the foundations and applications of modern language models</p>
    <p>Dive deep into transformer architecture, tokenization, embeddings, and practical applications</p>
</div>
""", unsafe_allow_html=True)

# ============ Introduction Section ============
st.markdown("<h2 class='section-title'>Welcome to Your Generative AI Journey</h2>", unsafe_allow_html=True)

st.markdown("""
This comprehensive course will guide you through the fascinating world of Generative AI, from the foundational concepts to practical applications. 
Our curriculum is designed to help you understand how modern language models work under the hood, giving you the knowledge to leverage 
these powerful technologies in your own projects.
""")

st.markdown("""
<div class="highlight-box">
<strong>What you'll gain:</strong> Deep understanding of transformer architecture, masked language models, tokenization, vector embeddings, 
and the practical skills to apply these technologies in real-world scenarios.
</div>
""", unsafe_allow_html=True)

# ============ Course Modules Section ============
st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)
# st.markdown("<h2 class='section-title'>🧩 Course Modules</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="course-card">
        <h3 class="card-title">🏗️ Transformer Architecture</h3>
        <p class="card-text">Understand the revolutionary architecture behind modern language models, from attention mechanisms to encoder-decoder designs.</p>
        <div>
            <span class="topic-tag">Self-Attention</span>
            <span class="topic-tag">Multi-Head Attention</span>
            <span class="topic-tag">Feed-Forward Networks</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="course-card">
        <h3 class="card-title">🧠 Word to Vector & Embeddings</h3>
        <p class="card-text">Discover how words are represented as vectors in high-dimensional space, and how these representations capture meaning.</p>
        <div>
            <span class="topic-tag">Word2Vec</span>
            <span class="topic-tag">GloVe</span>
            <span class="topic-tag">Semantic Space</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="course-card">
        <h3 class="card-title">🎭 Masked Language Models</h3>
        <p class="card-text">Learn about the training techniques that enable models to understand bidirectional context and predict masked tokens.</p>
        <div>
            <span class="topic-tag">BERT</span>
            <span class="topic-tag">RoBERTa</span>
            <span class="topic-tag">Masked Prediction</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="course-card">
        <h3 class="card-title">📜 Context in Language Models</h3>
        <p class="card-text">Explore how LLMs maintain and utilize context to generate coherent and contextually appropriate responses.</p>
        <div>
            <span class="topic-tag">Context Window</span>
            <span class="topic-tag">In-Context Learning</span>
            <span class="topic-tag">Context Length</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="course-card">
        <h3 class="card-title">🔤 Understanding Tokenization</h3>
        <p class="card-text">Explore how language models convert text into tokens, and how different tokenization strategies affect model performance.</p>
        <div>
            <span class="topic-tag">Subword Tokenization</span>
            <span class="topic-tag">BPE</span>
            <span class="topic-tag">WordPiece</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="course-card">
        <h3 class="card-title">🤖 Practical Applications of Generative AI</h3>
        <p class="card-text">Learn how to apply generative AI models to solve real-world problems, from content generation to creative assistance.</p>
        <div>
            <span class="topic-tag">Text Generation</span>
            <span class="topic-tag">RAG Systems</span>
            <span class="topic-tag">Fine-tuning</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============ Visual Explanations Section ============
st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)
st.markdown("<h2 class='section-title'>🎨 Interactive Visual Explanations</h2>", unsafe_allow_html=True)

st.markdown("""
Understanding complex AI concepts is easier with visual aids. Explore these interactive visualizations to grasp the core 
concepts behind modern language models.
""")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Transformer Architecture", 
    "Masked Language Models", 
    "Tokenization", 
    "Word Vectors", 
    "Context Window"
])

with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        transformer_fig = create_transformer_diagram()
        st.plotly_chart(transformer_fig, use_container_width=True)
    with col2:
        st.markdown("### Understanding Transformer Architecture")
        st.markdown("""
        The transformer architecture revolutionized NLP with its self-attention mechanism. Unlike traditional RNNs, 
        transformers process entire sequences in parallel, allowing for more efficient training and better long-range dependency modeling.

        **Key components:**
        
        - **Input Embedding**: Converts tokens to vectors
        - **Positional Encoding**: Adds position information
        - **Multi-Head Attention**: Allows focusing on different parts of the input
        - **Feed-Forward Networks**: Processes representations
        - **Layer Normalization**: Stabilizes training
        
        This architecture forms the foundation of models like BERT, GPT, and T5, enabling them to achieve state-of-the-art performance on language tasks.
        """)

with tab2:
    col1, col2 = st.columns([3, 2])
    with col1:
        masked_lm_fig = create_masked_lm_viz()
        st.plotly_chart(masked_lm_fig, use_container_width=True)
    with col2:
        st.markdown("### Masked Language Models")
        st.markdown("""
        Masked language modeling is a pre-training technique where random words in a text are replaced with a [MASK] token, 
        and the model must predict the original words.
        
        **Key aspects:**
        
        - Models learn bidirectional context
        - The ability to "fill in the blanks" builds strong language understanding
        - BERT and RoBERTa use this technique as their primary pre-training objective
        - Enables strong performance on a wide range of downstream tasks
        
        This approach differs from autoregressive models like GPT, which generate text sequentially from left to right.
        """)

with tab3:
    tokenization_fig = create_tokenization_viz()
    st.plotly_chart(tokenization_fig, use_container_width=True)
    
    st.markdown("### Tokenization Process")
    st.markdown("""
    Tokenization is the process of converting text into tokens that can be processed by a language model.
    It's the first step in the NLP pipeline and has significant impact on model performance.

    **Types of tokenizers:**
    
    - **Word-based**: Split by whitespace and punctuation
    - **Character-based**: Individual characters as tokens
    - **Subword-based**: Parts of words (like "transform" + "##er")
    
    Modern models typically use subword tokenization like BPE (Byte-Pair Encoding) or WordPiece to balance vocabulary size and handle unknown words better.
    """)

with tab4:
    col1, col2 = st.columns([2, 1])
    with col1:
        word_vector_fig = create_word_vector_viz()
        st.plotly_chart(word_vector_fig, use_container_width=True)
    with col2:
        st.markdown("### Word Vectors & Embeddings")
        st.markdown("""
        Word vectors represent words as dense vectors in a high-dimensional space where semantically similar words are closer together.
        
        **Key properties:**
        
        - Words with similar meanings cluster together
        - Vector arithmetic reveals relationships (e.g., king - man + woman ≈ queen)
        - Embeddings capture semantic and syntactic information
        - Pre-trained embeddings can be fine-tuned for specific tasks
        
        These vector representations form the foundation of how language models understand meaning and relationships between concepts.
        """)

with tab5:
    context_fig = create_context_viz()
    st.plotly_chart(context_fig, use_container_width=True)
    
    st.markdown("### Context in Large Language Models")
    st.markdown("""
    LLMs understand and generate text by considering the surrounding context. The context window determines
    how much text a model can "see" when making predictions or generating responses.

    **Important aspects:**
    
    - Larger context windows allow for more coherent long-form content
    - Attention mechanisms weigh the importance of different parts of the context
    - Recent innovations have extended context length from thousands to millions of tokens
    - Context enables models to maintain consistency across long conversations or documents
    
    Understanding how models process context is crucial for prompt engineering and getting the best results from generative AI systems.
    """)

# ============ Key Benefits Section ============
st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)
st.markdown("<h2 class='section-title'>🔑 What You'll Learn</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="content-box">
        <div class="icon-display">🧮</div>
        <h3>Model Architecture</h3>
        <p>Understand how transformer models work under the hood, from self-attention mechanisms to positional encodings.</p>
        <ul class="feature-list">
            <li>Self-attention mechanisms</li>
            <li>Encoder-decoder structures</li>
            <li>Multi-head attention</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-box">
        <div class="icon-display">🔬</div>
        <h3>Research Foundations</h3>
        <p>Learn about the key research breakthroughs that enabled the current generation of AI models.</p>
        <ul class="feature-list">
            <li>Attention is All You Need</li>
            <li>Transfer learning</li>
            <li>Scaling laws</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="content-box">
        <div class="icon-display">📊</div>
        <h3>Vector Representations</h3>
        <p>Master how language is converted into mathematical vectors that capture semantic meaning.</p>
        <ul class="feature-list">
            <li>Word embeddings</li>
            <li>Contextual embeddings</li>
            <li>Vector spaces</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-box">
        <div class="icon-display">🧩</div>
        <h3>Tokenization Strategies</h3>
        <p>Learn how models break text into tokens and why this process matters for performance.</p>
        <ul class="feature-list">
            <li>Byte-Pair Encoding</li>
            <li>WordPiece</li>
            <li>SentencePiece</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="content-box">
        <div class="icon-display">💼</div>
        <h3>Practical Applications</h3>
        <p>Build real applications that leverage generative AI capabilities.</p>
        <ul class="feature-list">
            <li>Text generation systems</li>
            <li>RAG implementations</li>
            <li>Content summarization</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-box">
        <div class="icon-display">📝</div>
        <h3>Prompt Engineering</h3>
        <p>Master the art of crafting effective prompts to get the best results from language models.</p>
        <ul class="feature-list">
            <li>Few-shot learning</li>
            <li>Chain-of-thought prompting</li>
            <li>System prompts</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ============ Why Learn Section ============
st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)
st.markdown("<h2 class='section-title'>💡 Why Learn Generative AI?</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="highlight-box">
    Generative AI is revolutionizing industries and creating new opportunities for innovation. Having a deep understanding of how these 
    technologies work will give you a competitive edge in this rapidly evolving field.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Career Opportunities")
    st.markdown("""
    - **AI Engineer**: Build and deploy language models
    - **Prompt Engineer**: Craft effective prompts for AI systems
    - **ML/NLP Specialist**: Develop specialized language models
    - **AI Application Developer**: Create products leveraging AI capabilities
    - **Research Scientist**: Advance the state of the art in AI
    - **AI Product Manager**: Define and lead AI product development
    """)

with col2:
    st.markdown("### Industry Applications")
    st.markdown("""
    - **Content Creation**: Automate writing tasks and generate creative content
    - **Customer Support**: Build intelligent chatbots and virtual assistants
    - **Healthcare**: Medical documentation and diagnostic support
    - **Finance**: Report generation and market analysis
    - **Education**: Personalized tutoring and content creation
    - **Legal**: Document analysis and contract review
    - **Software Development**: Code generation and documentation
    """)
    
    st.markdown("### Technology Trends")
    st.markdown("""
    - Multi-modal models connecting vision and language
    - Increasingly larger context windows
    - More efficient training and inference techniques
    - Specialized domain-specific models
    - Embedded AI for local applications
    """)

# ============ Call to Action Section ============
# st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)
# st.markdown("<h2 class='section-title'>🚀 Ready to Begin Your Journey?</h2>", unsafe_allow_html=True)

# col1, col2, col3 = st.columns([1, 2, 1])

# with col2:
#     st.markdown("""
#     <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%); border-radius: 12px;">
#         <h3>Start Learning Today</h3>
#         <p>Join our comprehensive Generative AI course and transform your understanding of how language models work.</p>
#         <button class="cta-button">Enroll Now</button>
#     </div>
#     """, unsafe_allow_html=True)

# ============ Footer Section ============
st.markdown("""
<div class="footer">
    <p>© 2023 AI Learning Hub • Privacy Policy • Terms of Service</p>
    <p style="font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem;">Mastering the foundations of AI, one concept at a time.</p>
</div>
""", unsafe_allow_html=True)
