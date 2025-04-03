# Streamlit BERT Tokenizer UI Enhancement

import streamlit as st
from transformers import BertTokenizer
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="BERT Tokenizer Explorer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-title {
        color: #1E88E5;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        color: #424242;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        background-color: #f0f2f6;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E88E5 !important;
        color: white !important;
    }
    .token-table {
        margin-top: 20px;
    }
    .info-box {
        background-color: #e3f2fd;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown('<h1 class="main-title">BERT Tokenizer Explorer</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Understand how BERT breaks down text into tokens</p>', unsafe_allow_html=True)

# Load tokenizer
@st.cache_resource
def load_tokenizer():
    return BertTokenizer.from_pretrained('bert-large-uncased')

tokenizer = load_tokenizer()

# Example dataset
dataset = [
    {"id": 0, "text": "A puppy is to dog as kitten is to ___."},
    {"id": 1, "text": "What is the capital of France?"},
    {"id": 2, "text": "Who is the president of the United States?"},
    {"id": 3, "text": "What is the largest planet in our solar system?"},
    {"id": 4, "text": "What is the smallest country in the world?"},
]

# Sidebar information
with st.sidebar:
    st.title("About BERT Tokenizer")
    st.markdown("""
    <div class="info-box">
        <p>BERT (Bidirectional Encoder Representations from Transformers) uses WordPiece tokenization, which breaks words into subwords.</p>
        <p>Special tokens:</p>
        <ul>
            <li>[CLS] - Classification token (101)</li>
            <li>[SEP] - Separator token (102)</li>
            <li>[UNK] - Unknown token (100)</li>
            <li>[PAD] - Padding token (0)</li>
            <li>[MASK] - Mask token (103)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Try Your Own Text")
    custom_text = st.text_area("Enter custom text to tokenize:", height=100)
    if st.button("Tokenize Custom Text", type="primary"):
        if custom_text:
            st.markdown("### Custom Text Tokenization")
            tokens = tokenizer.encode(custom_text)
            token_words = [tokenizer.decode([token]) for token in tokens]
            
            # Create a dataframe for better display
            df = pd.DataFrame({
                "Token": token_words,
                "ID": tokens
            })
            
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Please enter some text to tokenize")

# Main content with tabs
tabs = st.tabs([f"Example {i+1}" for i in range(len(dataset))])

for i, tab in enumerate(tabs):
    with tab:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### Sample Text:")
            example_text = dataset[i]['text']
            st.info(example_text)
            
            # Form for tokenization
            with st.form(f"tokenize_form_{i}"):
                prompt = st.text_input(
                    "Edit text to tokenize:",
                    value=example_text,
                    key=f"prompt_{i}"
                )
                submit = st.form_submit_button("Tokenize", type="primary", use_container_width=True)
                
            if submit and prompt:
                tokens = tokenizer.encode(prompt)
                token_words = [tokenizer.decode([token]) for token in tokens]
                
                # Visualization of tokens
                st.markdown("### Tokenization Result:")
                
                # Create a dataframe for better display
                df = pd.DataFrame({
                    "Token": token_words,
                    "ID": tokens
                })
                
                # Apply background color to special tokens
                def highlight_special_tokens(row):
                    if row['ID'] in [101, 102, 100, 0, 103]:
                        return ['background-color: #ffeeaa'] * 2
                    return [''] * 2
                
                styled_df = df.style.apply(highlight_special_tokens, axis=1)
                st.dataframe(styled_df, use_container_width=True)
                
                # Show original text with token boundaries
                st.markdown("### Token Boundaries Visualization:")
                token_text = " ".join([f"[{word}]" for word in token_words])
                st.code(token_text)
        
        with col2:
            if i == 0:
                st.markdown("### About This Example")
                st.markdown("""
                This example shows how BERT tokenizes an analogy question.
                Notice how words like "puppy" remain intact, but rarer words might be split into subwords.
                """)
            elif i == 1:
                st.markdown("### About This Example")
                st.markdown("""
                A simple question about geography.
                Notice how proper nouns like "France" are tokenized.
                """)
            elif i == 2:
                st.markdown("### About This Example")
                st.markdown("""
                This example includes a longer proper noun ("United States").
                See how BERT handles multi-word entities.
                """)
            elif i == 3:
                st.markdown("### About This Example")
                st.markdown("""
                A question about our solar system.
                Observe how the tokenizer handles the possessive "our".
                """)
            elif i == 4:
                st.markdown("### About This Example")
                st.markdown("""
                This example includes a superlative ("smallest").
                Notice how BERT handles word morphology.
                """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Created with ❤️ using Streamlit and Hugging Face Transformers</p>
    </div>
    """,
    unsafe_allow_html=True
)
