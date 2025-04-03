# Word2Vec Vectorizer App - Optimized UI

import streamlit as st
import gensim
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
import time

# Page configuration
def setup_page():
    st.set_page_config(
        page_title="Word2Vec Vectorizer",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
        /* Main header styling */
        h1 {
            color: #2D7FF9;
            text-align: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid #f0f0f5;
        }
        
        /* Sub-headers */
        h2, h3 {
            color: #2D7FF9;
            margin-top: 20px;
        }
        
        /* Card styling for containers */
        .stCard {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        /* Info box styling */
        .info-box {
            background-color: #f8f9fa;
            border-left: 4px solid #2D7FF9;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        
        /* Highlight for important elements */
        .highlight {
            background-color: #e6f2ff;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: 500;
        }
        
        /* Better button styles */
        .stButton > button {
            border-radius: 6px;
            font-weight: 500;
        }
        
        /* Footer styling */
        .footer {
            text-align: center;
            color: #71767a;
            font-size: 0.9rem;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #f0f0f5;
        }
        
        /* Improve form layout */
        div[data-baseweb="base-input"] {
            border-radius: 6px;
        }
        
        /* Matrix display styling */
        .matrix-container {
            overflow-x: auto;
            margin: 20px 0;
            border-radius: 8px;
            border: 1px solid #e6e6e6;
        }
        
        /* Slider styling */
        .stSlider {
            padding-top: 10px;
            padding-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

# Download required NLTK data
@st.cache_resource
def download_nltk_resources():
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
    except:
        pass

# Process text and create Word2Vec model
def process_text_to_vectors(text, vector_size):
    data = []
    
    # Tokenize sentences and words
    for sentence in sent_tokenize(text):
        tokens = [word.lower() for word in word_tokenize(sentence)]
        data.append(tokens)
    
    # Create Word2Vec model
    model = gensim.models.Word2Vec(
        data, 
        min_count=1,
        vector_size=vector_size,
        workers=4,
        seed=42
    )
    
    # Extract vectors and words
    vectors = model.wv.vectors
    words = list(model.wv.index_to_key)
    
    return vectors, words, model

# Create visualization of vectors
def visualize_vectors(vectors, words, dims=2):
    if len(vectors) < 2:
        return None
    
    # Reduce dimensions if needed
    if vectors.shape[1] > dims:
        pca = PCA(n_components=dims)
        reduced_vectors = pca.fit_transform(vectors)
    else:
        reduced_vectors = vectors
    
    # Create DataFrame for plotting
    df = pd.DataFrame(reduced_vectors, columns=[f'Dimension {i+1}' for i in range(dims)])
    df['Word'] = words
    
    # Create visualization based on dimensions
    if dims == 2:
        fig = px.scatter(
            df, x='Dimension 1', y='Dimension 2', 
            text='Word', hover_data=['Word'],
            title='2D Visualization of Word Vectors'
        )
        fig.update_traces(
            textposition='top center',
            marker=dict(size=10, opacity=0.8)
        )
        
    elif dims == 3:
        fig = px.scatter_3d(
            df, x='Dimension 1', y='Dimension 2', z='Dimension 3',
            text='Word', hover_data=['Word'],
            title='3D Visualization of Word Vectors'
        )
        fig.update_traces(
            marker=dict(size=5, opacity=0.8)
        )
    
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=0, b=0, t=40),
        template='plotly_white',
    )
    
    return fig

# Create heatmap for vector values
def create_vector_heatmap(vectors, words):
    fig = go.Figure(data=go.Heatmap(
        z=vectors,
        x=[f'Dim {i+1}' for i in range(vectors.shape[1])],
        y=words,
        colorscale='Viridis',
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='Word Vector Heatmap',
        height=max(300, 50 * len(words)),
        margin=dict(l=100, r=20, t=40, b=20),
        yaxis=dict(title='Words'),
        xaxis=dict(title='Vector Dimensions')
    )
    
    return fig

# Function to calculate word similarities
def get_word_similarities(model, target_word):
    try:
        similar_words = model.wv.most_similar(target_word, topn=10)
        return similar_words
    except KeyError:
        return None

# Example presets
example_presets = {
    "Simple Sentence": "The quick brown fox jumps over the lazy dog.",
    "Analogy Example": "A puppy is to dog as kitten is to cat.",
    "Semantic Relationships": "Paris is the capital of France. Berlin is the capital of Germany. Rome is the capital of Italy.",
    "Programming Context": "Python is a programming language. Java is also a programming language. Developers write code using programming languages.",
}

# Main function
def main():
    setup_page()
    download_nltk_resources()
    
    # App header
    st.title("📊 Word2Vec Vectorizer")
    st.markdown(
        """
        <div class='info-box'>
        Transform text into numerical vectors using Word2Vec, a neural network-based method for learning 
        word associations. This tool helps visualize how words can be represented as vectors in 
        a multi-dimensional space.
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Sidebar controls
    with st.sidebar:
        st.header("Configuration")
        
        vector_size = st.slider(
            "Vector Dimensions",
            min_value=2,
            max_value=100,
            value=20,
            step=1,
            help="Higher dimensions can capture more nuanced word relationships"
        )
        
        st.subheader("Visualization Options")
        viz_dimensions = st.radio(
            "Visualization Type",
            options=["2D", "3D", "Heatmap"],
            horizontal=True,
            help="How to visualize the resulting word vectors"
        )
        
        st.markdown("---")
        
        st.subheader("Example Presets")
        selected_preset = st.selectbox(
            "Choose a preset example",
            options=list(example_presets.keys()),
            help="Select a pre-defined example to try"
        )
        
        if st.button("Use Preset", key="preset_btn"):
            st.session_state.preset_text = example_presets[selected_preset]
        
        st.markdown("---")
        
        st.markdown(
            """
            <div class='info-box'>
            <h4>About Word2Vec</h4>
            <p>Word2Vec is an algorithm that transforms words into vectors of numbers to represent their meaning. Words with similar contexts will have vectors close to each other in the vector space.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<h3>Enter Text to Vectorize</h3>", unsafe_allow_html=True)
        
        # Initialize session state if needed
        if 'preset_text' not in st.session_state:
            st.session_state.preset_text = "A puppy is to dog as kitten is to cat."
            
        # Text input form
        with st.form("vectorize_form"):
            text_input = st.text_area(
                "Text Input",
                value=st.session_state.preset_text,
                height=150,
                help="Enter the text you want to convert to vectors"
            )
            
            submitted = st.form_submit_button("Vectorize", type="primary")
        
    with col2:
        st.markdown("<h3>Tips</h3>", unsafe_allow_html=True)
        st.markdown(
            """
            - Use text with multiple sentences for better results
            - Higher dimensions capture more nuanced meanings
            - Words need to appear in the text to be vectorized
            - Longer texts provide better word context
            """
        )
        
        st.markdown("<h3>Applications</h3>", unsafe_allow_html=True)
        st.markdown(
            """
            - Natural Language Processing
            - Semantic analysis
            - Document classification
            - Machine translation
            - Finding word analogies
            """
        )
    
    # Process submitted text
    vectors = None
    words = None
    model = None
    
    if submitted and text_input:
        with st.spinner('Generating word vectors...'):
            # Add slight delay for better visual feedback
            time.sleep(0.5)
            vectors, words, model = process_text_to_vectors(text_input, vector_size)
            
        # Show success message
        st.success(f"Successfully vectorized {len(words)} unique words into {vector_size}-dimensional vectors!")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["Visualization", "Vector Data", "Word Relationships"])
        
        with tab1:
            st.markdown("<h3>Vector Visualization</h3>", unsafe_allow_html=True)
            
            if len(words) < 2:
                st.warning("Need at least 2 unique words for visualization.")
            else:
                # Determine visualization type
                if viz_dimensions == "3D" and vector_size >= 3:
                    fig = visualize_vectors(vectors, words, dims=3)
                    st.plotly_chart(fig, use_container_width=True)
                    
                elif viz_dimensions == "Heatmap":
                    fig = create_vector_heatmap(vectors, words)
                    st.plotly_chart(fig, use_container_width=True)
                    
                else:  # Default to 2D
                    fig = visualize_vectors(vectors, words, dims=2)
                    st.plotly_chart(fig, use_container_width=True)
                    
                st.markdown(
                    """
                    <div class='info-box'>
                    Words that are used in similar contexts will appear closer together in the vector space.
                    The distance between words represents their semantic similarity.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        with tab2:
            st.markdown("<h3>Word Vector Data</h3>", unsafe_allow_html=True)
            
            # Create dataframe with word vectors
            vector_df = pd.DataFrame(
                vectors,
                index=words,
                columns=[f"Dim {i+1}" for i in range(vector_size)]
            )
            
            # Round to 4 decimal places for display
            vector_df = vector_df.round(4)
            
            # Display in an expandable section
            with st.expander("View full vector matrix", expanded=True):
                st.dataframe(vector_df, use_container_width=True)
            
            # Download option
            csv = vector_df.to_csv()
            st.download_button(
                label="Download Vector Data as CSV",
                data=csv,
                file_name='word_vectors.csv',
                mime='text/csv',
            )
        
        with tab3:
            st.markdown("<h3>Word Relationships & Similarities</h3>", unsafe_allow_html=True)
            
            if len(words) >= 2:
                # Word selection
                selected_word = st.selectbox(
                    "Select a word to find similarities:",
                    options=words,
                    index=0
                )
                
                # Find similar words
                similar_words = get_word_similarities(model, selected_word)
                
                if similar_words:
                    st.markdown(f"### Words most similar to '{selected_word}':")
                    
                    # Create similarity dataframe
                    similarity_df = pd.DataFrame(
                        similar_words,
                        columns=['Word', 'Similarity']
                    )
                    
                    # Create bar chart
                    fig = px.bar(
                        similarity_df,
                        x='Similarity', 
                        y='Word',
                        orientation='h',
                        labels={'Similarity': 'Cosine Similarity'},
                        title=f'Words Similar to "{selected_word}"',
                        color='Similarity',
                        color_continuous_scale='Viridis'
                    )
                    
                    fig.update_layout(
                        height=400,
                        yaxis={'categoryorder': 'total ascending'}
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(f"Not enough context to find words similar to '{selected_word}'.")
                
                # Try to analyze possible analogies
                if len(words) >= 4:
                    st.markdown("### Explore Word Analogies")
                    st.markdown("Word2Vec can identify analogical relationships (A is to B as C is to D)")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        word_a = st.selectbox("Word A:", options=words, key="word_a")
                    with col2:
                        word_b = st.selectbox("Word B:", options=words, key="word_b")
                    with col3:
                        word_c = st.selectbox("Word C:", options=words, key="word_c")
                    with col4:
                        st.markdown("### is to D:")
                    
                    if st.button("Find D (Analogy Completion)"):
                        try:
                            result = model.wv.most_similar(
                                positive=[word_b, word_c], 
                                negative=[word_a], 
                                topn=3
                            )
                            st.success(f"Best matches for {word_c} is to ___ as {word_a} is to {word_b}:")
                            for word, score in result:
                                st.markdown(f"- **{word}** (score: {score:.4f})")
                        except:
                            st.warning("Could not find a good analogy. Try different words or add more context in your text.")
            else:
                st.info("Need more unique words to analyze relationships.")
    
    # Footer
    st.markdown(
        """
        <div class='footer'>
            Word2Vec Vectorizer Tool | Created with Streamlit and Gensim
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
