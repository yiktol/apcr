# Interactive Transformer Architecture Demonstration with Streamlit


import streamlit as st
import numpy as np
import pandas as pd 
import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import matplotlib.pyplot as plt
import seaborn as sns
import time
from transformers import AutoTokenizer, AutoModelForCausalLM

# Set page configuration
st.set_page_config(
    page_title="Transformer Architecture Explained",
    page_icon="🤖",
    layout="wide"
)

# Title and introduction
st.title("🤖 Interactive Transformer Architecture Demonstration")
st.markdown("""
This application provides an interactive demonstration of how transformer models work.
Transformers are a type of neural network architecture that powers modern language models like GPT, BERT, and T5.
""")

# Sidebar navigation
st.sidebar.title("Navigation")
demo_option = st.sidebar.selectbox(
    "Choose a demonstration:",
    ["Introduction", "Sentence Completion", "Tokenization & Encoding", "Word Embeddings", 
     "Self-Attention Mechanism", "Encoder-Decoder Architecture", "Parallel Processing", 
     "Flexibility & Scalability"]
)

# Load a small pre-trained model
@st.cache_resource
def load_model_and_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
    model = AutoModelForCausalLM.from_pretrained("distilgpt2")
    return model, tokenizer

model, tokenizer = load_model_and_tokenizer()

# Introduction page
if demo_option == "Introduction":
    st.header("The Transformer Architecture")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        The transformer architecture was introduced in the 2017 paper "Attention Is All You Need" and has revolutionized NLP and many other fields.
        
        Key components of the transformer:
        
        1. **Tokenization & Encoding**: Convert text to numerical tokens
        2. **Embeddings**: Transform tokens into vector representations
        3. **Self-Attention**: Allow the model to focus on relevant parts of the input
        4. **Feed-Forward Networks**: Process the contextualized representations
        5. **Encoder-Decoder Structure**: Process input and generate output
        
        Use the sidebar to explore different aspects of the transformer architecture.
        """)
    
    with col2:
        st.image("https://miro.medium.com/max/1400/1*BHzGVskWGS_3jEcYYi6miQ.png", 
                 caption="The Transformer Architecture from 'Attention Is All You Need'")

# Sentence Completion Demo
elif demo_option == "Sentence Completion":
    st.header("Sentence Completion Demonstration")
    
    st.markdown("""
    See how a transformer model completes sentences in real-time. Type a prompt and 
    watch as the model generates a continuation.
    """)
    
    prompt = st.text_area("Enter a prompt:", "A puppy is to dog as kitten is to")
    
    max_length = st.slider("Maximum output length:", min_value=10, max_value=200, value=50)
    temperature = st.slider("Temperature (higher = more creative):", min_value=0.1, max_value=1.5, value=0.7, step=0.1)
    
    if st.button("Generate Completion"):
        with st.spinner("Generating..."):
            # Tokenize the input
            inputs = tokenizer(prompt, return_tensors="pt")
            
            # Record start time
            start_time = time.time()
            
            # Generate output
            outputs = model.generate(
                inputs["input_ids"],
                max_length=max_length,
                temperature=temperature,
                do_sample=True,
                top_p=0.92,
                pad_token_id=tokenizer.eos_token_id
            )
            
            # Measure elapsed time
            elapsed_time = time.time() - start_time
            
            # Decode the output
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Display the result
            st.subheader("Generated Output:")
            st.write(generated_text)
            
            # Show timing info
            st.info(f"Generation completed in {elapsed_time:.2f} seconds")
            
            # Highlight the original prompt vs. the generated part
            prompt_length = len(prompt)
            st.markdown("### Original vs. Generated")
            st.markdown(f"**Original Prompt (user input):** {prompt}")
            st.markdown(f"**Generated Continuation (model output):** {generated_text[prompt_length:]}")

# Tokenization & Encoding Demo
elif demo_option == "Tokenization & Encoding":
    st.header("Tokenization & Encoding Process")
    
    st.markdown("""
    Tokenization is the first step in processing text with a transformer. It breaks down
    text into smaller units (tokens) and converts them to numerical IDs that the model can work with.
    """)
    
    demo_text = st.text_input("Enter text to tokenize:", "Transformers are powerful neural networks.")
    
    if demo_text:
        # Show tokenization process
        tokens = tokenizer.tokenize(demo_text)
        token_ids = tokenizer.encode(demo_text)
        
        # Display results in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Tokens (Subwords)")
            st.write(tokens)
            st.markdown(f"**Number of tokens:** {len(tokens)}")
            
            # Show special tokens
            st.markdown("### Special tokens")
            st.markdown("- **[CLS]** - Classification token (beginning of sequence)")
            st.markdown("- **[SEP]** - Separator token (end of sequence)")
            st.markdown("- **[PAD]** - Padding token")
            st.markdown("- **[UNK]** - Unknown token (for words not in vocabulary)")
        
        with col2:
            st.subheader("Token IDs")
            st.write(token_ids)
            
            # Visualize token IDs as a simple bar chart
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.bar(range(len(token_ids)), token_ids, color='skyblue')
            ax.set_xlabel('Position in Sequence')
            ax.set_ylabel('Token ID')
            ax.set_title('Token IDs Representation')
            st.pyplot(fig)
        
        # Show token to ID mapping
        st.subheader("Token to ID Mapping")
        token_id_map = pd.DataFrame({
            'Token': tokens,
            'ID': token_ids[1:len(tokens)+1] if len(token_ids) > len(tokens) else token_ids[:len(tokens)]
        })
        st.table(token_id_map)
        
        st.markdown("""
        ### Why Tokenization Matters
        
        1. **Vocabulary Size Management**: Reduces the vocabulary to a manageable size
        2. **Out-of-Vocabulary Handling**: Can represent unseen words through subword units
        3. **Efficiency**: Enables efficient processing of text data
        """)

# Word Embeddings Demo
elif demo_option == "Word Embeddings":
    st.header("Word Embeddings Visualization")
    
    st.markdown("""
    After tokenization, each token is converted into a vector representation called an embedding.
    These embeddings capture semantic meaning in a high-dimensional space.
    """)
    
    # Demo text for embedding visualization
    demo_words = ["king", "queen", "man", "woman", "doctor", "nurse", "programmer"]
    selected_words = st.multiselect(
        "Select words to visualize embeddings:",
        options=demo_words,
        default=["king", "queen", "man", "woman"]
    )
    
    if selected_words:
        # Get embeddings from the model
        with st.spinner("Calculating embeddings..."):
            # Plot a mock embedding visualization
            st.subheader("2D Projection of Word Embeddings")
            
            # Create a mock visualization of word embeddings in 2D space
            # In a real implementation, you would use t-SNE or PCA to reduce dimensions
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Mock coordinates for visualization
            np.random.seed(42)
            coords = {
                "king": [1.2, 0.5],
                "queen": [1.0, -0.5],
                "man": [0.5, 0.6],
                "woman": [0.3, -0.6],
                "doctor": [-0.8, 0.3],
                "nurse": [-1.0, -0.3],
                "programmer": [-0.5, 0.8]
            }
            
            x_coords = [coords[word][0] for word in selected_words]
            y_coords = [coords[word][1] for word in selected_words]
            
            ax.scatter(x_coords, y_coords, color='blue', s=100)
            
            # Add labels to the points
            for word, x, y in zip(selected_words, x_coords, y_coords):
                ax.annotate(word, (x, y), fontsize=12, 
                            xytext=(5, 5), textcoords='offset points')
            
            ax.set_xlabel("Dimension 1")
            ax.set_ylabel("Dimension 2")
            ax.set_title("2D Projection of Word Embeddings")
            ax.grid(True)
            ax.set_axisbelow(True)
            
            # Remove axes ticks as they don't have meaningful values in this visualization
            ax.set_xticks([])
            ax.set_yticks([])
            
            st.pyplot(fig)
            
            st.markdown("""
            ### Properties of Word Embeddings
            
            1. **Semantic Relationships**: Words with similar meanings have similar embeddings
            2. **Analogical Relationships**: Embeddings can capture relationships like "king - man + woman = queen"
            3. **Dimensionality**: Typically 256-1024 dimensions (compressed to 2D for visualization)
            
            The transformer uses these embeddings as the foundation for its processing, adding
            position information to retain the order of tokens in the sequence.
            """)
            
            # Show embedding dimensions
            st.info(f"In this model, each token is represented by a {model.config.n_embd}-dimensional vector")

# Self-Attention Mechanism Demo
elif demo_option == "Self-Attention Mechanism":
    st.header("Self-Attention Mechanism")
    
    st.markdown("""
    The self-attention mechanism is the core innovation of transformers. It allows the model 
    to weigh the importance of different words in relation to each other.
    """)
    
    # Input for attention visualization
    attention_demo_text = st.text_input(
        "Enter a sentence to visualize attention:",
        "The cat sat on the mat because it was comfortable."
    )
    
    if attention_demo_text:
        # Tokenize the text
        tokens = tokenizer.tokenize(attention_demo_text)
        
        # Create a mock attention matrix for visualization
        n_tokens = len(tokens)
        
        # Generate a mock attention pattern
        # In a real implementation, you would extract actual attention weights from the model
        np.random.seed(42)
        
        # Create synthetic attention patterns
        # For "it", create higher attention to "cat" 
        attention_matrix = np.random.rand(n_tokens, n_tokens) * 0.1
        
        # Find "it" and "cat" positions
        it_pos = None
        cat_pos = None
        for i, token in enumerate(tokens):
            if token == 'it':
                it_pos = i
            elif token == 'cat':
                cat_pos = i
        
        # Create meaningful attention patterns
        if it_pos is not None and cat_pos is not None:
            attention_matrix[it_pos, cat_pos] = 0.8  # "it" attends strongly to "cat"
        
        # Visualize the attention matrix
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(attention_matrix, 
                    xticklabels=tokens, 
                    yticklabels=tokens, 
                    cmap="YlOrRd", 
                    annot=False, 
                    cbar_kws={'label': 'Attention Weight'})
        plt.title("Self-Attention Visualization")
        plt.xlabel("Keys/Values (tokens being attended to)")
        plt.ylabel("Queries (tokens attending)")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)
        
        st.markdown("""
        ### How Self-Attention Works
        
        1. **Queries, Keys, and Values**: Each token generates these three vectors
        2. **Attention Scores**: Computed as dot products between queries and keys
        3. **Softmax**: Convert scores to probabilities
        4. **Weighted Sum**: Combine value vectors according to attention probabilities
        
        The heatmap above shows which words are paying attention to which other words. Brighter colors indicate stronger attention.
        """)
        
        # Multi-head attention explanation
        st.subheader("Multi-Head Attention")
        st.markdown("""
        Transformers use multiple "attention heads" in parallel, each focusing on different 
        aspects of relationships between words:
        
        - One head might focus on syntactic relationships
        - Another might focus on semantic relationships
        - Others might capture different linguistic patterns
        
        This allows the model to capture rich, complex relationships between words in the input.
        """)
        
        # Show number of attention heads in the model
        st.info(f"This model uses {model.config.n_head} attention heads")

# Encoder-Decoder Demo
elif demo_option == "Encoder-Decoder Architecture":
    st.header("Encoder-Decoder Architecture")
    
    st.markdown("""
    Transformers often use an encoder-decoder architecture, especially for tasks like translation or summarization.
    
    - **Encoder**: Processes the input and builds representations
    - **Decoder**: Generates the output based on encoder representations and previous outputs
    """)
    
    # Visual representation of encoder-decoder
    encoder_decoder_img = """
    digraph G {
        rankdir=LR;
        
        subgraph cluster_0 {
            color=lightblue;
            style=filled;
            node [style=filled,color=white];
            edge [color=black];
            
            E1 [label="Encoder\nLayer 1"];
            E2 [label="Encoder\nLayer 2"];
            E3 [label="Encoder\nLayer 3"];
            
            E1 -> E2;
            E2 -> E3;
            
            label = "Encoder";
        }
        
        subgraph cluster_1 {
            color=lightgreen;
            style=filled;
            node [style=filled,color=white];
            edge [color=black];
            
            D1 [label="Decoder\nLayer 1"];
            D2 [label="Decoder\nLayer 2"];
            D3 [label="Decoder\nLayer 3"];
            
            D1 -> D2;
            D2 -> D3;
            
            label = "Decoder";
        }
        
        Input [shape=box];
        Output [shape=box];
        
        Input -> E1;
        E3 -> D1 [label="Encoder\nOutputs"];
        D3 -> Output;
    }
    """
    
    # Encode for URL
    import base64
    graphbytes = encoder_decoder_img.encode("utf8")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    
    st.markdown(f"![Encoder-Decoder Architecture](https://quickchart.io/graphviz?graph={base64_string})")
    
    # Example task
    st.subheader("Example: Translation Task")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**English Input (Encoder)**")
        st.write("The cat sat on the mat.")
        
        st.markdown("**Process:**")
        st.markdown("""
        1. Input is tokenized
        2. Tokens are embedded
        3. Self-attention is applied
        4. Representations are passed to decoder
        """)
    
    with col2:
        st.markdown("**French Output (Decoder)**")
        st.write("Le chat s'est assis sur le tapis.")
        
        st.markdown("**Process:**")
        st.markdown("""
        1. Output is generated token-by-token
        2. Each step attends to encoder outputs
        3. Each step also attends to previously generated tokens
        4. Probabilities determine the next token
        """)
    
    # Explain model variants
    st.subheader("Transformer Model Variants")
    
    model_variants = {
        "Encoder-only": ["BERT", "RoBERTa", "DistilBERT"],
        "Decoder-only": ["GPT", "GPT-2", "GPT-3", "GPT-4", "LLaMA"],
        "Encoder-Decoder": ["T5", "BART", "mT5"]
    }
    
    for variant, examples in model_variants.items():
        st.markdown(f"**{variant} Models:** {', '.join(examples)}")
        
    st.markdown("""
    - **Encoder-only**: Good for understanding tasks (classification, NER)
    - **Decoder-only**: Good for generation tasks (text completion, creative writing)
    - **Encoder-Decoder**: Good for transformation tasks (translation, summarization)
    """)

# Parallel Processing Demo
elif demo_option == "Parallel Processing":
    st.header("Parallel Processing Advantage")
    
    st.markdown("""
    Unlike RNNs and LSTMs, transformers process all tokens in parallel during training.
    This parallelization enables much faster training on modern hardware.
    """)
    
    # Compare RNN vs Transformer processing
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sequential RNN Processing")
        
        # Create an animation-like display for RNN
        rnn_text = "Transformers are better than RNNs."
        rnn_tokens = rnn_text.split()
        
        processing_time_per_token = 0.5  # seconds
        
        total_rnn_time = len(rnn_tokens) * processing_time_per_token
        
        st.markdown(f"**Input text:** {rnn_text}")
        st.markdown(f"**Tokens:** {len(rnn_tokens)}")
        
        # Simulate RNN processing token by token
        if st.button("Simulate RNN Processing"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Process tokens one by one
            for i, token in enumerate(rnn_tokens):
                # Update progress bar
                progress = (i + 1) / len(rnn_tokens)
                progress_bar.progress(progress)
                
                # Update status text
                status_text.markdown(f"Processing token: **{token}**")
                
                # Wait to simulate processing time
                time.sleep(processing_time_per_token)
            
            status_text.markdown("✅ Processing complete!")
            st.markdown(f"**Total time:** {total_rnn_time} seconds")
    
    with col2:
        st.subheader("Parallel Transformer Processing")
        
        # Create an animation-like display for Transformer
        transformer_text = "Transformers are better than RNNs."
        transformer_tokens = transformer_text.split()
        
        # Transformer processes all tokens at once, so it's much faster
        total_transformer_time = processing_time_per_token  # Just one step for all tokens
        
        st.markdown(f"**Input text:** {transformer_text}")
        st.markdown(f"**Tokens:** {len(transformer_tokens)}")
        
        # Simulate Transformer processing all tokens at once
        if st.button("Simulate Transformer Processing"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Process all tokens at once
            status_text.markdown(f"Processing all tokens in parallel: **{' '.join(transformer_tokens)}**")
            
            # Simulate single processing step
            time.sleep(total_transformer_time)
            progress_bar.progress(1.0)
            
            status_text.markdown("✅ Processing complete!")
            st.markdown(f"**Total time:** {total_transformer_time} seconds")
    
    # Compare computational complexity
    st.subheader("Computational Complexity Comparison")
    
    complexity_data = {
        "Model Type": ["RNN/LSTM", "Transformer"],
        "Sequential Operations": ["O(sequence length)", "O(1)"],
        "Total Computation": ["O(d × sequence length)", "O(d × sequence length²)"]
    }
    
    import pandas as pd
    complexity_df = pd.DataFrame(complexity_data)
    st.table(complexity_df)
    
    st.markdown("""
    While transformers use more total computation due to the attention mechanism (quadratic complexity),
    they require far fewer sequential operations. This makes them much faster on modern parallel hardware like GPUs.
    """)
    
    # Hardware acceleration
    st.subheader("Hardware Acceleration")
    st.markdown("""
    The parallel nature of transformers allows them to fully utilize:
    
    - **GPUs**: Graphics Processing Units with thousands of cores
    - **TPUs**: Tensor Processing Units optimized for matrix operations
    - **Distributed Training**: Training across multiple accelerators
    
    This has enabled the scaling of transformers to hundreds of billions of parameters.
    """)

# Flexibility & Scalability Demo
elif demo_option == "Flexibility & Scalability":
    st.header("Flexibility & Scalability")
    
    st.markdown("""
    Transformers have proven to be remarkably flexible and scalable, enabling advances in many fields.
    """)
    
    # Show scaling of transformers over time
    st.subheader("Growth in Model Size")
    
    model_sizes = {
        "BERT (2018)": 340,
        "GPT-2 (2019)": 1500,
        "T5 (2020)": 11000,
        "GPT-3 (2020)": 175000,
        "PaLM (2022)": 540000,
        "GPT-4 (2023)": 1000000  # Estimated
    }
    
    # Create bar chart of model sizes
    fig, ax = plt.subplots(figsize=(10, 6))
    models = list(model_sizes.keys())
    sizes = [model_sizes[m] for m in models]
    
    # Log scale for better visualization
    ax.bar(models, sizes, color='skyblue')
    ax.set_yscale('log')
    ax.set_ylabel('Model Size (Millions of Parameters)')
    ax.set_title('Transformer Model Scaling Over Time')
    plt.xticks(rotation=45)
    
    for i, v in enumerate(sizes):
        ax.text(i, v * 1.1, f"{v:,}", ha='center', fontsize=9)
    
    st.pyplot(fig)
    
    # Application domains
    st.subheader("Transformer Applications")
    
    applications = {
        "Natural Language Processing": [
            "Text Generation", "Translation", "Summarization", "Question Answering"
        ],
        "Computer Vision": [
            "Image Classification", "Object Detection", "Image Generation"
        ],
        "Audio Processing": [
            "Speech Recognition", "Text-to-Speech", "Music Generation"
        ],
        "Multimodal": [
            "Text-to-Image Generation", "Visual Question Answering", "Video Captioning"
        ],
        "Scientific Applications": [
            "Protein Structure Prediction", "Drug Discovery", "Code Generation"
        ]
    }
    
    for domain, apps in applications.items():
        with st.expander(domain):
            for app in apps:
                st.markdown(f"- {app}")
    
    # Scaling laws
    st.subheader("Transformer Scaling Laws")
    st.markdown("""
    Research has shown that transformer performance scales predictably with:
    
    1. **More parameters**: Larger models have greater capacity
    2. **More data**: More training data improves performance
    3. **More compute**: More training computation yields better results
    
    This predictable scaling has enabled researchers to plan and execute training
    of increasingly powerful models.
    """)
    
    # Few-shot learning capability
    st.subheader("Emergent Abilities with Scale")
    st.markdown("""
    As transformers scale up, they develop new capabilities that weren't explicitly trained for:
    
    - **Few-shot learning**: Learning from just a few examples
    - **Zero-shot learning**: Performing tasks without specific examples
    - **Instruction following**: Following natural language instructions
    - **Chain-of-thought reasoning**: Solving problems step by step
    
    These emergent abilities have made large language models increasingly useful for a wide
    range of applications.
    """)

# Add a footer with references
st.markdown("---")
st.markdown("""
**References:**
- Vaswani, A., et al. (2017). "Attention Is All You Need"
- Devlin, J., et al. (2019). "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"
- Brown, T., et al. (2020). "Language Models are Few-Shot Learners"
""")

 # Needed for some dataframes in the app
