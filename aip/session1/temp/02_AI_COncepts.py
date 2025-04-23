import streamlit as st
import uuid
import time
import pandas as pd
from streamlit_lottie import st_lottie
import requests
import json
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import io
import base64
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="AI Concepts E-Learning",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# AWS Color Scheme
AWS_COLORS = {
    'orange': '#FF9900',
    'dark_blue': '#232F3E',
    'light_blue': '#1A73E8',
    'teal': '#007DBC',
    'light_grey': '#EAEDED',
    'dark_grey': '#545B64',
    'white': '#FFFFFF'
}

def load_lottie_url(url):
    """Load a Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def initialize_session_state():
    """Initialize session state variables"""
    if "user_id" not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    
    if "knowledge_check_started" not in st.session_state:
        st.session_state.knowledge_check_started = False
    
    if "knowledge_check_submitted" not in st.session_state:
        st.session_state.knowledge_check_submitted = False
    
    if "knowledge_check_score" not in st.session_state:
        st.session_state.knowledge_check_score = 0
    
    if "answers" not in st.session_state:
        st.session_state.answers = {
            "q1": None,
            "q2": [],
            "q3": None,
            "q4": None,
            "q5": []
        }

def reset_session():
    """Reset the session state"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    initialize_session_state()
    st.success("Session reset successfully!")

def apply_aws_style():
    """Apply AWS styling to the app"""
    st.markdown(
        f"""
        <style>
        .main {{
            background-color: {AWS_COLORS['white']};
            color: {AWS_COLORS['dark_grey']};
        }}
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 4px 4px 0px 0px;
            padding: 10px 20px;
            background-color: {AWS_COLORS['light_grey']};
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {AWS_COLORS['orange']};
            color: {AWS_COLORS['white']};
        }}
        .stButton>button {{
            background-color: {AWS_COLORS['orange']};
            color: {AWS_COLORS['white']};
            border: none;
        }}
        .stButton>button:hover {{
            background-color: {AWS_COLORS['teal']};
            color: {AWS_COLORS['white']};
        }}
        footer {{
            text-align: center;
            padding: 20px;
            font-size: 14px;
            color: {AWS_COLORS['dark_grey']};
        }}
        .title {{
            color: {AWS_COLORS['dark_blue']};
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
        }}
        .subtitle {{
            color: {AWS_COLORS['dark_blue']};
            font-size: 24px;
            margin-top: 30px;
            margin-bottom: 10px;
        }}
        .card {{
            background-color: {AWS_COLORS['light_grey']};
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def render_topic_ai_ml_genai():
    """Render content for AI, ML, and Generative AI differences"""
    st.markdown("<h2 class='subtitle'>Difference between AI, ML, and Generative AI</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Artificial Intelligence (AI)
        AI refers to computer systems designed to perform tasks that typically require human intelligence. It's the broadest term that encompasses all technologies that enable machines to mimic human capabilities.
        
        **Key characteristics:**
        - Aims to simulate human intelligence and behavior
        - Encompasses all machine intelligence technologies
        - Can include rule-based systems that don't necessarily learn
        
        ### Machine Learning (ML)
        ML is a subset of AI that focuses on developing algorithms that allow computers to learn from and make predictions or decisions based on data.
        
        **Key characteristics:**
        - Learns patterns from data without explicit programming
        - Improves performance with more data and experience
        - Focuses on making predictions based on known features
        
        ### Generative AI
        Generative AI is a subset of ML focused on creating new content (text, images, audio, etc.) that resembles human-created content.
        
        **Key characteristics:**
        - Creates new, original content
        - Can understand context and nuance
        - Uses large language models or diffusion models
        - Examples include ChatGPT, DALL-E, and Midjourney
        """)
    
    with col2:
        # Hierarchy diagram
        fig = go.Figure()
        
        # Create a hierarchical structure
        fig.add_trace(go.Scatter(
            x=[0, 1, 2, 1], 
            y=[3, 2, 3, 1], 
            mode='markers+text',
            marker=dict(size=30, color=[AWS_COLORS['dark_blue'], AWS_COLORS['teal'], AWS_COLORS['dark_blue'], AWS_COLORS['orange']]),
            text=["AI", "ML", "Other AI<br>Technologies", "Generative<br>AI"],
            textposition="bottom center",
            hoverinfo="text",
            name=""
        ))
        
        # Add lines connecting the nodes
        fig.add_trace(go.Scatter(
            x=[0, 1, 1, 2], 
            y=[3, 2, 2, 3], 
            mode='lines',
            line=dict(color=AWS_COLORS['dark_grey'], width=2),
            hoverinfo="skip",
            name=""
        ))
        
        fig.add_trace(go.Scatter(
            x=[1, 1], 
            y=[2, 1], 
            mode='lines',
            line=dict(color=AWS_COLORS['dark_grey'], width=2),
            hoverinfo="skip",
            name=""
        ))
        
        fig.update_layout(
            title="AI Hierarchy",
            xaxis_title="",
            yaxis_title="",
            showlegend=False,
            xaxis=dict(showticklabels=False, showgrid=False),
            yaxis=dict(showticklabels=False, showgrid=False),
            plot_bgcolor='rgba(0,0,0,0)',
            width=400,
            height=400
        )
        
        st.plotly_chart(fig)
    
    # Interactive example
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🧪 Interactive Example")
    
    example_option = st.selectbox(
        "Select a technology to see a real-world example:",
        ["Artificial Intelligence (AI)", "Machine Learning (ML)", "Generative AI"]
    )
    
    if example_option == "Artificial Intelligence (AI)":
        st.markdown("""
        **Example: Expert System for Medical Diagnosis**
        
        An AI system that uses predefined rules to diagnose medical conditions:
        ```python
        def diagnose_flu(symptoms):
            if "fever" in symptoms and ("cough" in symptoms or "sore throat" in symptoms):
                if "body ache" in symptoms:
                    return "High probability of flu"
                else:
                    return "Moderate probability of flu"
            else:
                return "Low probability of flu"
                
        patient_symptoms = ["fever", "cough", "body ache"]
        diagnosis = diagnose_flu(patient_symptoms)
        print(diagnosis)  # Output: "High probability of flu"
        ```
        
        This is AI because it mimics a doctor's decision-making process, but it's rule-based and doesn't learn from data.
        """)
        
    elif example_option == "Machine Learning (ML)":
        st.markdown("""
        **Example: Email Spam Classification**
        
        A machine learning model trained to classify emails as spam or not:
        ```python
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.naive_bayes import MultinomialNB
        
        # Training data
        emails = ["Get rich quick", "Buy now discount", "Meeting tomorrow", "Project update"]
        labels = ["spam", "spam", "not spam", "not spam"]
        
        # Create features from text
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(emails)
        
        # Train model
        classifier = MultinomialNB()
        classifier.fit(X, labels)
        
        # Predict for new email
        new_email = ["Huge discount available"]
        X_new = vectorizer.transform(new_email)
        prediction = classifier.predict(X_new)
        print(prediction)  # Output: ["spam"]
        ```
        
        This is ML because the system learns patterns from data rather than following explicit rules.
        """)
        
    else:
        st.markdown("""
        **Example: Text Generation with GPT**
        
        A generative AI model creating new content based on a prompt:
        ```python
        import openai

        # Set up OpenAI API (key would be required)
        openai.api_key = "your-api-key"
        
        # Generate text
        prompt = "Write a short poem about artificial intelligence"
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=150
        )
        
        print(response.choices[0].text)
        # Output might be something like:
        # In silicon minds, a spark ignites,
        # Learning, growing through endless bytes,
        # Not human, yet thinking in its way,
        # Artificial brilliance on display.
        ```
        
        This is Generative AI because it creates new, original content that wasn't explicitly programmed.
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_topic_traditional_vs_ml():
    """Render content for Traditional Programming vs ML"""
    st.markdown("<h2 class='subtitle'>Traditional Programming vs Machine Learning</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Traditional Programming
        In traditional programming, developers write explicit rules and instructions for the computer to follow.
        
        **Key characteristics:**
        - Developers code explicit rules
        - Rules are deterministic
        - Program logic is human-defined
        - Changes require manual updates to code
        
        **Process flow:**
        1. Analysis of problem
        2. Design algorithm
        3. Write code with explicit rules
        4. Test and debug
        5. Deploy solution
        """)
    
    with col2:
        st.markdown("""
        ### Machine Learning
        In machine learning, developers create models that learn patterns from data to make predictions or decisions.
        
        **Key characteristics:**
        - Algorithms learn from data
        - Patterns can be probabilistic
        - Program logic is data-driven
        - Improves with more data without code changes
        
        **Process flow:**
        1. Data collection and preparation
        2. Feature engineering
        3. Model selection and training
        4. Model evaluation and tuning
        5. Deploy model for inference
        """)
    
    # Comparative diagram
    st.markdown("""
    ### Visual Comparison
    """)
    
    fig = go.Figure()
    
    # Traditional programming flow
    fig.add_trace(go.Scatter(
        x=[1, 2, 3, 4],
        y=[2, 2, 2, 2],
        mode='markers+lines+text',
        name='Traditional Programming',
        line=dict(color=AWS_COLORS['dark_blue'], width=2),
        marker=dict(size=15, color=AWS_COLORS['dark_blue']),
        text=['Data', 'Rules<br>(Code)', '', 'Output'],
        textposition='top center'
    ))
    
    # Add arrow in traditional flow
    fig.add_annotation(
        x=3.5, 
        y=2,
        text='',
        showarrow=True,
        axref='x', ayref='y',
        ax=3, ay=2,
        arrowhead=3,
        arrowcolor=AWS_COLORS['dark_blue'],
        arrowsize=1.5
    )
    
    # Machine Learning flow
    fig.add_trace(go.Scatter(
        x=[1, 2, 3, 4],
        y=[1, 1, 1, 1],
        mode='markers+lines+text',
        name='Machine Learning',
        line=dict(color=AWS_COLORS['orange'], width=2),
        marker=dict(size=15, color=AWS_COLORS['orange']),
        text=['Data', 'Output', '', 'Rules<br>(Model)'],
        textposition='bottom center'
    ))
    
    # Add arrow in ML flow
    fig.add_annotation(
        x=3.5, 
        y=1,
        text='',
        showarrow=True,
        axref='x', ayref='y',
        ax=3, ay=1,
        arrowhead=3,
        arrowcolor=AWS_COLORS['orange'],
        arrowsize=1.5
    )
    
    fig.update_layout(
        title='Traditional Programming vs Machine Learning Approach',
        xaxis=dict(showticklabels=False, showgrid=False, range=[0.5, 4.5]),
        yaxis=dict(showticklabels=False, showgrid=False, range=[0.5, 2.5]),
        plot_bgcolor='rgba(0,0,0,0)',
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Interactive example
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🧪 Interactive Example: Email Classification")
    
    tab1, tab2 = st.tabs(["Traditional Programming", "Machine Learning"])
    
    with tab1:
        st.markdown("""
        #### Traditional Programming Approach
        ```python
        def classify_email(email_text):
            # Predefined rules for classification
            spam_keywords = ['discount', 'offer', 'buy now', 'free', 'cash', 'winner']
            
            # Convert text to lowercase for case-insensitive matching
            email_lower = email_text.lower()
            
            # Check for spam keywords
            spam_score = 0
            for keyword in spam_keywords:
                if keyword in email_lower:
                    spam_score += 1
            
            # Classify based on score threshold
            if spam_score >= 2:
                return "Spam"
            else:
                return "Not Spam"
        
        # Test the function
        email = "Congratulations! You are our lucky winner. Claim your free cash prize now!"
        result = classify_email(email)
        print(f"Classification result: {result}")  # Output: Classification result: Spam
        ```
        
        **Limitations:**
        - Rules are manually defined and might miss new spam patterns
        - Requires updating rules as spam tactics evolve
        - Cannot adapt to personalized preferences automatically
        """)
    
    with tab2:
        st.markdown("""
        #### Machine Learning Approach
        ```python
        import pandas as pd
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.model_selection import train_test_split
        
        # Sample data (in a real scenario, you'd have thousands of examples)
        data = {
            'email_text': [
                "Congratulations! You won $1,000,000",
                "Limited time offer: 90% discount",
                "Meeting scheduled for tomorrow at 10 AM",
                "Project report attached for review",
                "Claim your free prize now",
                "Updates on the quarterly budget"
            ],
            'label': ['spam', 'spam', 'not_spam', 'not_spam', 'spam', 'not_spam']
        }
        
        df = pd.DataFrame(data)
        
        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            df['email_text'], df['label'], test_size=0.2, random_state=42
        )
        
        # Create features from text data
        vectorizer = CountVectorizer()
        X_train_features = vectorizer.fit_transform(X_train)
        X_test_features = vectorizer.transform(X_test)
        
        # Train the model
        classifier = MultinomialNB()
        classifier.fit(X_train_features, y_train)
        
        # Make predictions
        new_email = ["Important team update and project timeline"]
        new_email_features = vectorizer.transform(new_email)
        prediction = classifier.predict(new_email_features)
        print(f"Classification: {prediction[0]}")  # Output: Classification: not_spam
        
        # Model evaluation
        accuracy = classifier.score(X_test_features, y_test)
        print(f"Model accuracy: {accuracy}")
        ```
        
        **Advantages:**
        - Learns patterns from data rather than relying on predefined rules
        - Can discover non-obvious relationships in the data
        - Improves with more training data
        - Can adapt to changing patterns over time with retraining
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_topic_when_to_use_ml():
    """Render content for When to Use Machine Learning"""
    st.markdown("<h2 class='subtitle'>When to Use Machine Learning</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    Machine learning is powerful but not always the right solution. Here's guidance on when to use ML and when other approaches might be more appropriate.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Use Machine Learning When:
        
        ✅ **The problem involves complex patterns**
        - Pattern recognition in images, audio, or text
        - User behavior prediction
        - Anomaly detection in data
        
        ✅ **Rules are difficult to define explicitly**
        - Spam detection that evolves over time
        - Natural language understanding
        - Content recommendations
        
        ✅ **You have sufficient quality data**
        - Large labeled datasets available
        - Ongoing data collection possible
        - Data represents the problem well
        
        ✅ **The problem has clear inputs and outputs**
        - Well-defined features (inputs)
        - Clear objectives to optimize for
        - Measurable outcomes
        
        ✅ **The environment is changing**
        - Problems where patterns evolve over time
        - Systems that need to adapt to new conditions
        """)
    
    with col2:
        st.markdown("""
        ### Consider Alternatives When:
        
        ❌ **The problem is simple and rule-based**
        - Basic calculations or transformations
        - Deterministic workflows
        - Problems with clear logical rules
        
        ❌ **Interpretability is critical**
        - Medical diagnosis requiring explanation
        - Financial decisions needing justification
        - Legal or compliance requirements
        
        ❌ **Data is limited or poor quality**
        - Small datasets
        - Highly imbalanced data
        - Noisy or inconsistent data
        
        ❌ **Resources are constrained**
        - Limited computing power
        - Real-time requirements with low latency
        - Deployment on edge devices
        
        ❌ **Absolute precision is required**
        - Critical safety systems
        - Financial calculations
        - Scenarios where errors are unacceptable
        """)
    
    # Decision flow chart
    st.markdown("### Decision Flowchart: Should You Use Machine Learning?")
    
    # Use Plotly to create a simple flowchart
    fig = go.Figure()
    
    # Nodes
    nodes = [
        {"id": 0, "label": "Start", "x": 0, "y": 5},
        {"id": 1, "label": "Complex\nPatterns?", "x": 2, "y": 5},
        {"id": 2, "label": "Sufficient\nData?", "x": 4, "y": 5},
        {"id": 3, "label": "Rules Hard\nto Define?", "x": 6, "y": 5},
        {"id": 4, "label": "Use ML", "x": 8, "y": 5},
        {"id": 5, "label": "Use\nTraditional\nProgramming", "x": 4, "y": 3},
    ]
    
    # Add nodes
    for node in nodes:
        color = AWS_COLORS['orange'] if node["label"] in ["Use ML", "Start"] else AWS_COLORS['dark_blue'] if node["label"] == "Use\nTraditional\nProgramming" else AWS_COLORS['teal']
        
        fig.add_trace(go.Scatter(
            x=[node["x"]], 
            y=[node["y"]],
            mode='markers+text',
            marker=dict(size=30, color=color),
            text=[node["label"]],
            textposition="middle center",
            name=node["label"],
            hoverinfo="text"
        ))
    
    # Add edges/connections
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4),  # Main path
        (1, 5, "No"), (2, 5, "No"), (3, 5, "No"),  # No paths
        (1, 2, "Yes"), (2, 3, "Yes"), (3, 4, "Yes")  # Yes paths
    ]
    
    for edge in edges:
        if len(edge) == 2:
            src, tgt = edge
            text = ""
        else:
            src, tgt, text = edge
        
        src_node = nodes[src]
        tgt_node = nodes[tgt]
        
        # For vertical connections (to "Use Traditional Programming")
        if tgt == 5:
            fig.add_trace(go.Scatter(
                x=[nodes[src]["x"], nodes[src]["x"], tgt_node["x"]],
                y=[nodes[src]["y"], (nodes[src]["y"] + tgt_node["y"])/2, tgt_node["y"]],
                mode='lines',
                line=dict(color=AWS_COLORS['dark_grey'], width=2),
                hoverinfo="none",
                showlegend=False
            ))
            
            # Add text for "No" labels
            fig.add_annotation(
                x=nodes[src]["x"],
                y=(nodes[src]["y"] + tgt_node["y"])/2 + 0.3,
                text=text,
                showarrow=False,
                font=dict(color=AWS_COLORS['dark_grey'])
            )
        else:
            # For horizontal connections
            fig.add_trace(go.Scatter(
                x=[src_node["x"], tgt_node["x"]],
                y=[src_node["y"], tgt_node["y"]],
                mode='lines',
                line=dict(color=AWS_COLORS['dark_grey'], width=2),
                hoverinfo="none",
                showlegend=False
            ))
            
            # Add text for "Yes" labels if this is a yes path
            if text:
                fig.add_annotation(
                    x=(src_node["x"] + tgt_node["x"])/2,
                    y=src_node["y"] + 0.3,
                    text=text,
                    showarrow=False,
                    font=dict(color=AWS_COLORS['dark_grey'])
                )
    
    fig.update_layout(
        showlegend=False,
        xaxis=dict(showticklabels=False, showgrid=False, range=[-1, 9]),
        yaxis=dict(showticklabels=False, showgrid=False, range=[2, 6]),
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Interactive example
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🧪 Interactive Example: Scenario Analysis")
    
    scenario = st.selectbox(
        "Select a scenario to analyze if machine learning is appropriate:",
        [
            "Customer churn prediction for a subscription service",
            "Calculating monthly interest on a loan",
            "Real-time fraud detection for credit card transactions",
            "Converting temperatures from Celsius to Fahrenheit",
            "Image recognition for automatic tagging of photos"
        ]
    )
    
    if scenario == "Customer churn prediction for a subscription service":
        st.markdown("""
        #### Analysis: Customer Churn Prediction
        
        **Machine Learning is highly appropriate ✅**
        
        **Why ML works well:**
        - **Complex patterns:** Customer behavior involves many variables and subtle patterns
        - **Data availability:** Subscription services typically have extensive customer data
        - **Evolving patterns:** Customer behavior and churn reasons change over time
        - **Clear objective:** Predicting which customers are likely to cancel
        
        **Suggested approach:**
        ```python
        import pandas as pd
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, precision_score, recall_score
        
        # Load customer data
        data = pd.read_csv('customer_data.csv')
        
        # Features: usage statistics, customer age, payment history, etc.
        X = data.drop('churned', axis=1)
        # Target: whether the customer churned (1) or not (0)
        y = data['churned']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        # Train model
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        
        # Predict and evaluate
        y_pred = model.predict(X_test)
        
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
        print(f"Precision: {precision_score(y_test, y_pred):.2f}")
        print(f"Recall: {recall_score(y_test, y_pred):.2f}")
        
        # Extract feature importance for insights
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("Top churn predictors:")
        print(feature_importance.head())
        ```
        """)
    
    elif scenario == "Calculating monthly interest on a loan":
        st.markdown("""
        #### Analysis: Calculating Loan Interest
        
        **Traditional programming is more appropriate ❌**
        
        **Why traditional works better:**
        - **Simple formula:** Interest calculation follows a well-defined mathematical formula
        - **Deterministic process:** Same inputs always produce the same output
        - **Perfect accuracy required:** Financial calculations need to be precise
        - **No pattern recognition needed:** No complex relationships to discover
        
        **Suggested approach:**
        ```python
        def calculate_monthly_interest(principal, annual_rate, days_in_month, days_in_year=365):
            """
            Calculate monthly interest on a loan
            
            Args:
                principal: The loan amount
                annual_rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
                days_in_month: Number of days in the month
                days_in_year: Number of days in the year (365 or 366 for leap year)
                
            Returns:
                Monthly interest amount
            """
            monthly_interest = principal * annual_rate * (days_in_month / days_in_year)
            return round(monthly_interest, 2)
        
        # Example usage
        loan_amount = 10000
        annual_interest_rate = 0.045  # 4.5%
        
        # Calculate for February in a leap year
        february_interest = calculate_monthly_interest(loan_amount, annual_interest_rate, 29, 366)
        print(f"February interest: ${february_interest}")
        
        # Calculate for March in a regular year
        march_interest = calculate_monthly_interest(loan_amount, annual_interest_rate, 31, 365)
        print(f"March interest: ${march_interest}")
        ```
        """)
    
    elif scenario == "Real-time fraud detection for credit card transactions":
        st.markdown("""
        #### Analysis: Credit Card Fraud Detection
        
        **Machine Learning is highly appropriate ✅**
        
        **Why ML works well:**
        - **Complex patterns:** Fraud patterns are sophisticated and constantly evolving
        - **Abundant data:** Large volumes of transaction data available
        - **Hard-to-define rules:** Fraudulent behavior varies and is difficult to capture in static rules
        - **Pattern detection:** ML can identify subtle anomalies humans might miss
        - **Adaptability:** Can be retrained to detect new fraud patterns
        
        **Suggested approach:**
        ```python
        import pandas as pd
        from sklearn.ensemble import IsolationForest
        from sklearn.preprocessing import StandardScaler
        import numpy as np
        
        # Load transaction data
        transactions = pd.read_csv('credit_card_transactions.csv')
        
        # Feature engineering
        # Add time-based features like hour of day, day of week
        transactions['hour'] = pd.to_datetime(transactions['timestamp']).dt.hour
        transactions['day_of_week'] = pd.to_datetime(transactions['timestamp']).dt.dayofweek
        
        # Calculate statistical features
        # Group by customer to get recent behavior patterns
        customer_stats = transactions.groupby('customer_id').agg({
            'amount': ['mean', 'std', 'max'],
            'transaction_id': 'count'
        }).reset_index()
        
        # Normalize features
        features = ['amount', 'hour', 'day_of_week']  # Plus more features in real scenario
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(transactions[features])
        
        # Train anomaly detection model
        model = IsolationForest(contamination=0.01)  # Expected 1% fraud rate
        model.fit(scaled_features)
        
        # Function for real-time prediction
        def check_transaction(transaction_data):
            # Preprocess transaction
            processed_data = scaler.transform([transaction_data])
            
            # Get anomaly score (-1 for anomaly, 1 for normal)
            score = model.predict(processed_data)[0]
            
            # Get anomaly probability
            anomaly_score = model.score_samples(processed_data)[0]
            fraud_probability = 1 - (anomaly_score - model.offset_) / 0.5
            
            return {
                'is_fraudulent': score == -1,
                'fraud_probability': fraud_probability,
                'should_block': fraud_probability > 0.8
            }
        
        # Example usage
        new_transaction = [250.00, 3, 6]  # $250 at 3 AM on Sunday
        result = check_transaction(new_transaction)
        print(f"Fraud check result: {result}")
        ```
        """)
    
    elif scenario == "Converting temperatures from Celsius to Fahrenheit":
        st.markdown("""
        #### Analysis: Temperature Conversion
        
        **Traditional programming is more appropriate ❌**
        
        **Why traditional works better:**
        - **Fixed formula:** Temperature conversion uses a simple mathematical formula
        - **No learning required:** The relationship is perfectly known (F = C * 9/5 + 32)
        - **Perfect accuracy needed:** Conversions should be exact
        - **Minimal data advantage:** More data doesn't improve a mathematical conversion
        - **Explainability:** Simple formula is fully transparent
        
        **Suggested approach:**
        ```python
        def celsius_to_fahrenheit(celsius):
            """
            Convert Celsius temperature to Fahrenheit
            
            Args:
                celsius: Temperature in Celsius
                
            Returns:
                Temperature in Fahrenheit
            """
            return (celsius * 9/5) + 32
        
        # Example usage
        temperatures_c = [0, 20, 37, 100]
        
        for temp_c in temperatures_c:
            temp_f = celsius_to_fahrenheit(temp_c)
            print(f"{temp_c}°C = {temp_f}°F")
        
        # Output:
        # 0°C = 32.0°F
        # 20°C = 68.0°F
        # 37°C = 98.6°F
        # 100°C = 212.0°F
        ```
        
        **Why using ML would be inappropriate:**
        ```python
        # Using ML for something that doesn't need it
        import numpy as np
        from sklearn.linear_model import LinearRegression
        
        # Training data
        celsius = np.array([-40, 0, 37, 100]).reshape(-1, 1)
        fahrenheit = np.array([-40, 32, 98.6, 212])
        
        # Train a model
        model = LinearRegression()
        model.fit(celsius, fahrenheit)
        
        # Predict
        celsius_test = np.array([[20]])
        fahrenheit_pred = model.predict(celsius_test)[0]
        
        print(f"20°C = {fahrenheit_pred}°F")  # Approximately 68°F but with potential error
        
        # This approach:
        # - Adds unnecessary complexity
        # - Could introduce errors/approximations
        # - Uses resources inefficiently
        # - Might break outside the training range
        ```
        """)
    
    else:  # Image recognition
        st.markdown("""
        #### Analysis: Image Recognition for Photo Tagging
        
        **Machine Learning is essential ✅**
        
        **Why ML is necessary:**
        - **Complex visual patterns:** Images contain intricate patterns human vision recognizes but are difficult to program explicitly
        - **Huge feature space:** Each pixel represents a feature, creating thousands of dimensions
        - **Impossible to define rules:** No feasible way to write explicit rules for recognizing objects
        - **Transfer learning benefits:** Can leverage pre-trained models
        - **Constantly improving:** Performance improves with more diverse training data
        
        **Suggested approach:**
        ```python
        import tensorflow as tf
        from tensorflow.keras.applications import MobileNetV2
        from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
        from tensorflow.keras.preprocessing import image
        import numpy as np
        
        # Load pre-trained model
        model = MobileNetV2(weights='imagenet')
        
        def tag_image(image_path):
            # Load and preprocess image
            img = image.load_img(image_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            
            # Predict image content
            predictions = model.predict(img_array)
            decoded_predictions = decode_predictions(predictions, top=5)[0]
            
            # Format results
            tags = []
            for _, label, confidence in decoded_predictions:
                if confidence > 0.1:  # Only include tags with >10% confidence
                    tags.append({
                        'tag': label.replace('_', ' ').title(),
                        'confidence': float(confidence)
                    })
            
            return tags
        
        # Example usage
        image_tags = tag_image('vacation_beach.jpg')
        print("Detected tags:")
        for tag in image_tags:
            print(f"- {tag['tag']}: {tag['confidence']*100:.1f}%")
        
        # Example output:
        # Detected tags:
        # - Sandy Beach: 89.5%
        # - Seashore: 76.2%
        # - Umbrella: 45.3%
        # - Palm Tree: 23.8%
        # - Sunglasses: 14.2%
        ```
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_topic_ml_vs_genai():
    """Render content for Machine Learning vs Generative AI"""
    st.markdown("<h2 class='subtitle'>Machine Learning vs Generative AI: Making the Right Choice</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    While Generative AI is a subset of Machine Learning, they're used for different purposes and have distinct strengths and applications.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Traditional Machine Learning
        
        **Strengths:**
        - **Highly accurate predictions** for well-defined problems
        - **Efficient with structured data**
        - **Less compute-intensive** than generative models
        - **Easier to interpret** (especially models like decision trees)
        - **Better for critical decisions** where explanation is needed
        
        **Best for:**
        - Classification tasks (spam vs. not spam)
        - Regression problems (predicting house prices)
        - Anomaly detection (fraud identification)
        - Recommendation systems based on similarity
        - Time series forecasting
        """)
    
    with col2:
        st.markdown("""
        ### Generative AI
        
        **Strengths:**
        - **Creates new content** like text, images, code
        - **Understands context and nuance** in human language
        - **Versatile across domains** with minimal tuning
        - **Handles unstructured data** well
        - **Solves open-ended problems** without specific structure
        
        **Best for:**
        - Content creation and creative tasks
        - Natural language understanding and generation
        - Converting between formats (text to image)
        - Summarization and information extraction
        - Assistance and augmentation of human work
        """)
    
    # Comparison table
    st.markdown("### Detailed Comparison")
    
    comparison_data = {
        'Aspect': [
            'Primary Purpose', 
            'Data Requirements',
            'Training Approach',
            'Model Size',
            'Interpretability',
            'Output Format',
            'Example Tasks',
            'Computing Resources',
            'Human Involvement'
        ],
        'Traditional ML': [
            'Make predictions on specific tasks', 
            'Can work with smaller, task-specific datasets',
            'Typically trained from scratch for each task',
            'Relatively small (MBs to few GBs)',
            'Ranges from transparent to black box',
            'Labels, categories, numerical values',
            'Classification, regression, clustering',
            'Moderate (can run on standard hardware)',
            'Requires feature engineering and model selection'
        ],
        'Generative AI': [
            'Create new content similar to training data', 
            'Requires massive datasets (billions of examples)',
            'Pre-trained on general data, fine-tuned for specifics',
            'Very large (tens to hundreds of GBs)',
            'Usually black box with limited explanation',
            'Natural language, images, audio, etc.',
            'Text generation, image creation, translation',
            'High (often requires multiple GPUs)',
            'Prompt engineering rather than feature engineering'
        ]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.table(comparison_df)
    
    # Interactive example
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🧪 Interactive Example: Solving the Same Problem with ML vs. Generative AI")
    
    problem_type = st.selectbox(
        "Select a problem to see how ML and Generative AI would approach it:",
        [
            "Customer Service Automation",
            "Image Processing",
            "Product Recommendation"
        ]
    )
    
    if problem_type == "Customer Service Automation":
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Traditional ML Approach")
            st.markdown("""
            **Implementation: Intent Classification System**
            
            ```python
            import pandas as pd
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.pipeline import Pipeline
            
            # Load training data (customer queries and their intents)
            data = {
                'query': [
                    "How do I reset my password?",
                    "I forgot my password",
                    "Can't login to my account",
                    "When will my order arrive?",
                    "Order delivery status",
                    "Tracking my recent purchase",
                    "I want to return this product",
                    "How do I get a refund?",
                    "Product is damaged"
                ],
                'intent': [
                    'password_reset', 'password_reset', 'password_reset',
                    'order_tracking', 'order_tracking', 'order_tracking',
                    'return_refund', 'return_refund', 'return_refund'
                ]
            }
            
            df = pd.DataFrame(data)
            
            # Create ML pipeline
            intent_classifier = Pipeline([
                ('vectorizer', TfidfVectorizer()),
                ('classifier', RandomForestClassifier())
            ])
            
            # Train model
            intent_classifier.fit(df['query'], df['intent'])
            
            # Function to route customer queries
            def handle_customer_query(query):
                intent = intent_classifier.predict([query])[0]
                
                responses = {
                    'password_reset': "To reset your password, please visit the login page and click 'Forgot Password'.",
                    'order_tracking': "You can find your order status by logging into your account and visiting 'Order History'.",
                    'return_refund': "Our return policy allows returns within 30 days. Please visit the Returns page for instructions."
                }
                
                return responses.get(intent, "I'm not sure how to help with that. Please contact our support team.")
            
            # Example usage
            query = "I need to change my password"
            response = handle_customer_query(query)
            print(response)
            ```
            
            **Characteristics:**
            - Classifies queries into pre-defined intents
            - Returns canned responses based on intent
            - Handles only expected scenarios
            - Limited to training examples
            - Needs retraining to handle new intents
            """)
        
        with col2:
            st.markdown("#### Generative AI Approach")
            st.markdown("""
            **Implementation: LLM-based Assistant**
            
            ```python
            import openai
            
            # Configure API
            openai.api_key = "your-api-key"
            
            # Company information for context
            company_context = """
            Our company is TechGadgets Inc. We sell electronics online.
            Return policy: 30-day returns with receipt.
            Shipping: 2-day standard, overnight premium option.
            Password reset: Self-service on website or call support.
            """
            
            # Function to handle customer queries
            def handle_customer_query(query):
                prompt = f"""
                '''You are a customer service representative for TechGadgets Inc.
                
                Company information:
                {company_context}
                
                Please respond to the customer query below in a helpful,
                concise, and professional manner. If you don't know the
                answer, ask for more information or offer to connect 
                them with a human agent.
                
                Customer query: {query}'''
                """
                
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    max_tokens=150,
                    temperature=0.7
                )
                
                return response.choices[0].text.strip()
            
            # Example usage
            query = "I need to change my password but also have a question about my recent order"
            response = handle_customer_query(query)
            print(response)
            ```
            
            **Characteristics:**
            - Generates custom responses for each query
            - Can handle multiple intents in one query
            - Adapts to unexpected questions
            - Can ask clarifying questions when needed
            - Can be updated with new information without retraining
            """)
    
    elif problem_type == "Image Processing":
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Traditional ML Approach")
            st.markdown("""
            **Implementation: Image Classification and Object Detection**
            
            ```python
            import tensorflow as tf
            from tensorflow.keras.applications import ResNet50
            from tensorflow.keras.preprocessing import image
            from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
            import numpy as np
            
            # Load pre-trained model
            model = ResNet50(weights='imagenet')
            
            def process_image(image_path):
                # Load and preprocess image
                img = image.load_img(image_path, target_size=(224, 224))
                img_array = image.img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)
                img_array = preprocess_input(img_array)
                
                # Predict image content
                predictions = model.predict(img_array)
                results = decode_predictions(predictions, top=5)[0]
                
                # Format results
                objects_found = []
                for _, object_name, confidence in results:
                    objects_found.append({
                        'object': object_name.replace('_', ' ').title(),
                        'confidence': float(confidence)
                    })
                
                return {
                    'objects_detected': objects_found,
                    'primary_object': objects_found[0]['object'],
                    'image_type': 'outdoor' if any(o['object'] in ['Tree', 'Mountain', 'Sky'] for o in objects_found) else 'indoor'
                }
            
            # Example usage
            result = process_image('vacation_photo.jpg')
            print(f"Main subject: {result['primary_object']}")
            print(f"Scene type: {result['image_type']}")
            print("All objects detected:")
            for obj in result['objects_detected']:
                print(f"- {obj['object']}: {obj['confidence']*100:.1f}%")
            ```
            
            **Characteristics:**
            - Identifies objects in the image
            - Provides confidence scores for each object
            - Limited to classification and detection
            - Cannot modify or generate new images
            - Works with a fixed set of object categories
            """)
        
        with col2:
            st.markdown("#### Generative AI Approach")
            st.markdown("""
            **Implementation: Image Understanding and Generation**
            
            ```python
            import openai
            from PIL import Image
            import requests
            from io import BytesIO
            
            # Configure API
            openai.api_key = "your-api-key"
            
            def process_image(image_path):
                # Load image
                image = Image.open(image_path)
                
                # Analyze image content
                analysis_response = openai.ChatCompletion.create(
                    model="gpt-4-vision-preview",
                    messages=[
                        {
                            "role": "user", 
                            "content": [
                                {"type": "text", "text": "Describe this image in detail."},
                                {"type": "image_url", "image_url": {"url": f"file://{image_path}"}}
                            ]
                        }
                    ],
                    max_tokens=300
                )
                
                image_description = analysis_response.choices[0].message.content
                
                # Generate variations or modifications (using DALL-E)
                prompt = f"Based on this description: {image_description}, create a similar image but at sunset."
                
                variation_response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size="512x512"
                )
                
                # Get the URL of the generated image
                generated_image_url = variation_response["data"][0]["url"]
                
                # Download generated image
                response = requests.get(generated_image_url)
                generated_image = Image.open(BytesIO(response.content))
                generated_image.save("sunset_variation.jpg")
                
                return {
                    "original_description": image_description,
                    "generated_variation": "sunset_variation.jpg"
                }
            
            # Example usage
            result = process_image('vacation_photo.jpg')
            print("Original image description:")
            print(result["original_description"])
            print(f"Generated variation saved to: {result['generated_variation']}")
            ```
            
            **Characteristics:**
            - Provides detailed description of image content
            - Can interpret context and subtle details
            - Creates new variations of the image
            - Can modify specific aspects while maintaining others
            - Understands and can manipulate higher-level concepts
            """)
    
    else:  # Product Recommendation
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Traditional ML Approach")
            st.markdown("""
            **Implementation: Collaborative Filtering Recommendation System**
            
            ```python
            import pandas as pd
            import numpy as np
            from sklearn.metrics.pairwise import cosine_similarity
            
            # Sample user-item interaction data (user_id, product_id, rating)
            data = {
                'user_id': [1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5],
                'product_id': [101, 102, 103, 101, 104, 101, 102, 105, 107, 103, 104, 106, 102, 103, 105],
                'rating': [5, 4, 3, 4, 5, 5, 3, 4, 5, 3, 5, 4, 4, 3, 5]
            }
            
            interactions = pd.DataFrame(data)
            
            # Create user-item matrix
            user_item_matrix = interactions.pivot(
                index='user_id', 
                columns='product_id', 
                values='rating'
            ).fillna(0)
            
            # Calculate cosine similarity between users
            user_similarity = cosine_similarity(user_item_matrix)
            user_similarity_df = pd.DataFrame(
                user_similarity, 
                index=user_item_matrix.index, 
                columns=user_item_matrix.index
            )
            
            def recommend_products(user_id, top_n=3):
                if user_id not in user_item_matrix.index:
                    return "User not found in database"
                
                # Get products the user hasn't rated
                user_products = user_item_matrix.loc[user_id]
                unrated_products = user_products[user_products == 0].index
                
                # Find similar users
                similar_users = user_similarity_df[user_id].sort_values(ascending=False)[1:]
                
                # Calculate predicted ratings
                recommendations = {}
                for product in unrated_products:
                    product_ratings = []
                    product_similarity_scores = []
                    
                    for similar_user, similarity in similar_users.items():
                        # Get rating for this product from similar user
                        rating = user_item_matrix.loc[similar_user, product]
                        
                        if rating > 0:
                            product_ratings.append(rating)
                            product_similarity_scores.append(similarity)
                    
                    # Calculate weighted average
                    if product_ratings:
                        recommendations[product] = np.average(
                            product_ratings, 
                            weights=product_similarity_scores
                        )
                
                # Return top N recommendations
                top_recommendations = sorted(
                    recommendations.items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:top_n]
                
                return [
                    {"product_id": product_id, "predicted_rating": rating}
                    for product_id, rating in top_recommendations
                ]
            
            # Example usage
            user_id = 5
            recommendations = recommend_products(user_id)
            print(f"Top recommendations for user {user_id}:")
            for rec in recommendations:
                print(f"- Product {rec['product_id']}: Predicted rating {rec['predicted_rating']:.2f}")
            ```
            
            **Characteristics:**
            - Based on user behavior patterns
            - Recommends products similar users enjoyed
            - Provides numerical rating predictions
            - Requires sufficient user interaction data
            - Limited to existing products in catalog
            """)
        
        with col2:
            st.markdown("#### Generative AI Approach")
            st.markdown("""
            **Implementation: LLM-based Personalized Recommendation**
            
            ```python
            import openai
            import json
            
            # Configure API
            openai.api_key = "your-api-key"
            
            # User profile and purchase history
            user_profile = {
                "user_id": 5,
                "preferences": {
                    "favorite_categories": ["Electronics", "Books", "Outdoor Gear"],
                    "price_sensitivity": "medium",
                    "style_preferences": "modern, minimalist"
                },
                "purchase_history": [
                    {"product_id": 102, "name": "Wireless Headphones", "category": "Electronics"},
                    {"product_id": 103, "name": "Science Fiction Novel", "category": "Books"},
                    {"product_id": 105, "name": "Hiking Backpack", "category": "Outdoor Gear"}
                ],
                "browsing_history": [
                    "Smart Home Devices", "Fitness Trackers", "Travel Guides"
                ]
            }
            
            # Product catalog (simplified)
            product_catalog = [
                {"product_id": 101, "name": "Smartphone", "category": "Electronics", "price": 699, "description": "Latest model with advanced camera"},
                {"product_id": 104, "name": "Coffee Maker", "category": "Kitchen Appliances", "price": 89, "description": "Programmable with timer"},
                {"product_id": 106, "name": "Fitness Tracker", "category": "Electronics", "price": 129, "description": "Waterproof with heart rate monitoring"},
                {"product_id": 107, "name": "Travel Guide: Europe", "category": "Books", "price": 24, "description": "Complete guide with maps and tips"},
                {"product_id": 108, "name": "Smart Speaker", "category": "Electronics", "price": 79, "description": "Voice controlled with premium sound"},
                {"product_id": 109, "name": "Camping Tent", "category": "Outdoor Gear", "price": 199, "description": "Lightweight and weather resistant"}
            ]
            
            def generate_recommendations(user_profile, product_catalog, top_n=3):
                # Format user profile for LLM context
                user_history = ", ".join([p["name"] for p in user_profile["purchase_history"]])
                user_browsing = ", ".join(user_profile["browsing_history"])
                
                # Create product catalog for LLM context
                catalog_text = ""
                for product in product_catalog:
                    catalog_text += f"Product ID: {product['product_id']}, Name: {product['name']}, Category: {product['category']}, Price: ${product['price']}, Description: {product['description']}\\n"
                
                prompt = f"""
                You are a personalized recommendation engine. Based on the user profile and product catalog below,
                recommend {top_n} products that would most interest this user. Consider their purchase history,
                browsing history, and preferences. Do not recommend products they've already purchased.
                
                USER PROFILE:
                - Favorite categories: {', '.join(user_profile['preferences']['favorite_categories'])}
                - Price sensitivity: {user_profile['preferences']['price_sensitivity']}
                - Style preferences: {user_profile['preferences']['style_preferences']}
                - Previous purchases: {user_history}
                - Recently browsed: {user_browsing}
                
                PRODUCT CATALOG:
                {catalog_text}
                
                Provide your recommendations as a JSON array with product_id, name, and a personalized reason
                for each recommendation.
                """
                
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                
                # Extract JSON from response
                content = response.choices[0].message.content
                try:
                    # Find JSON part in the response
                    start = content.find('[')
                    end = content.rfind(']') + 1
                    if start >= 0 and end > start:
                        json_str = content[start:end]
                        recommendations = json.loads(json_str)
                    else:
                        recommendations = []
                except json.JSONDecodeError:
                    recommendations = []
                    
                return recommendations
            
            # Example usage
            recommendations = generate_recommendations(user_profile, product_catalog)
            print("Personalized product recommendations:")
            for rec in recommendations:
                print(f"- {rec['name']} (ID: {rec['product_id']})")
                print(f"  Reason: {rec['reason']}")
                print()
            ```
            
            **Characteristics:**
            - Considers multiple user data points (purchases, browsing, preferences)
            - Provides personalized explanations for recommendations
            - Can recommend based on subtle patterns and connections
            - Takes into account catalog descriptions and context
            - Can handle cold start cases better with less user data
            """)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_knowledge_check():
    """Render knowledge check section with questions and tracking"""
    st.markdown("<h2 class='subtitle'>Knowledge Check</h2>", unsafe_allow_html=True)
    
    if not st.session_state.knowledge_check_started:
        st.warning("Ready to test your knowledge? This quiz will help you assess your understanding of AI concepts.")
        if st.button("Start Knowledge Check"):
            st.session_state.knowledge_check_started = True
            st.experimental_rerun()
    
    elif not st.session_state.knowledge_check_submitted:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # Question 1 (single answer)
        st.markdown("#### Q1: What is the primary difference between traditional programming and machine learning?")
        q1_options = [
            "Traditional programming is faster, while machine learning is more accurate",
            "In traditional programming, explicit rules are coded, while in machine learning patterns are learned from data",
            "Machine learning is only used for image recognition, while traditional programming is used for everything else",
            "Traditional programming requires more data than machine learning"
        ]
        st.session_state.answers["q1"] = st.radio(
            "Select one answer:",
            q1_options,
            key="q1",
            index=None
        )
        
        # Question 2 (multiple answers)
        st.markdown("#### Q2: Which of the following are characteristics of Generative AI? (Select all that apply)")
        q2_options = [
            "Can create new content like text or images",
            "Typically requires less computing power than traditional ML",
            "Examples include DALL-E and ChatGPT",
            "Only works with structured data"
        ]
        st.session_state.answers["q2"] = []
        q2_col1, q2_col2 = st.columns(2)
        with q2_col1:
            if st.checkbox("Can create new content like text or images", key="q2_1"):
                st.session_state.answers["q2"].append("Can create new content like text or images")
            if st.checkbox("Typically requires less computing power than traditional ML", key="q2_2"):
                st.session_state.answers["q2"].append("Typically requires less computing power than traditional ML")
        with q2_col2:
            if st.checkbox("Examples include DALL-E and ChatGPT", key="q2_3"):
                st.session_state.answers["q2"].append("Examples include DALL-E and ChatGPT")
            if st.checkbox("Only works with structured data", key="q2_4"):
                st.session_state.answers["q2"].append("Only works with structured data")
        
        # Question 3 (single answer)
        st.markdown("#### Q3: When is traditional programming more appropriate than machine learning?")
        q3_options = [
            "When dealing with natural language processing",
            "When solving complex pattern recognition problems",
            "When the problem has well-defined rules and formulas",
            "When working with very large datasets"
        ]
        st.session_state.answers["q3"] = st.radio(
            "Select one answer:",
            q3_options,
            key="q3",
            index=None
        )
        
        # Question 4 (single answer)
        st.markdown("#### Q4: Which relationship correctly describes the hierarchy of these technologies?")
        q4_options = [
            "Machine Learning is a subset of Generative AI, which is a subset of Artificial Intelligence",
            "Artificial Intelligence is a subset of Machine Learning, which is a subset of Generative AI",
            "Generative AI is a subset of Machine Learning, which is a subset of Artificial Intelligence",
            "All three are separate technologies with no hierarchical relationship"
        ]
        st.session_state.answers["q4"] = st.radio(
            "Select one answer:",
            q4_options,
            key="q4",
            index=None
        )
        
        # Question 5 (multiple answers)
        st.markdown("#### Q5: Which of the following are appropriate use cases for machine learning? (Select all that apply)")
        q5_options = [
            "Converting temperatures from Celsius to Fahrenheit",
            "Predicting customer churn based on past behavior",
            "Detecting fraudulent credit card transactions",
            "Calculating the monthly interest on a loan"
        ]
        st.session_state.answers["q5"] = []
        q5_col1, q5_col2 = st.columns(2)
        with q5_col1:
            if st.checkbox("Converting temperatures from Celsius to Fahrenheit", key="q5_1"):
                st.session_state.answers["q5"].append("Converting temperatures from Celsius to Fahrenheit")
            if st.checkbox("Predicting customer churn based on past behavior", key="q5_2"):
                st.session_state.answers["q5"].append("Predicting customer churn based on past behavior")
        with q5_col2:
            if st.checkbox("Detecting fraudulent credit card transactions", key="q5_3"):
                st.session_state.answers["q5"].append("Detecting fraudulent credit card transactions")
            if st.checkbox("Calculating the monthly interest on a loan", key="q5_4"):
                st.session_state.answers["q5"].append("Calculating the monthly interest on a loan")
        
        # Submit button
        if st.button("Submit Answers"):
            # Calculate score
            score = 0
            
            # Check Q1
            if st.session_state.answers["q1"] == "In traditional programming, explicit rules are coded, while in machine learning patterns are learned from data":
                score += 1
            
            # Check Q2
            correct_q2 = ["Can create new content like text or images", "Examples include DALL-E and ChatGPT"]
            if set(st.session_state.answers["q2"]) == set(correct_q2):
                score += 1
            
            # Check Q3
            if st.session_state.answers["q3"] == "When the problem has well-defined rules and formulas":
                score += 1
            
            # Check Q4
            if st.session_state.answers["q4"] == "Generative AI is a subset of Machine Learning, which is a subset of Artificial Intelligence":
                score += 1
            
            # Check Q5
            correct_q5 = ["Predicting customer churn based on past behavior", "Detecting fraudulent credit card transactions"]
            if set(st.session_state.answers["q5"]) == set(correct_q5):
                score += 1
            
            # Update session state
            st.session_state.knowledge_check_score = score
            st.session_state.knowledge_check_submitted = True
            st.experimental_rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    else:  # Show results
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # Display score
        score = st.session_state.knowledge_check_score
        total = 5
        percentage = (score / total) * 100
        
        if percentage >= 80:
            st.success(f"🎉 Congratulations! Your score: {score}/{total} ({percentage:.0f}%)")
        elif percentage >= 60:
            st.warning(f"👍 Good effort! Your score: {score}/{total} ({percentage:.0f}%)")
        else:
            st.error(f"📚 Keep learning! Your score: {score}/{total} ({percentage:.0f}%)")
        
        # Show answers and explanations
        st.markdown("### Review Answers")
        
        # Q1
        st.markdown("**Q1: What is the primary difference between traditional programming and machine learning?**")
        st.markdown(f"Your answer: {st.session_state.answers['q1'] if st.session_state.answers['q1'] else 'No answer'}")
        st.markdown("Correct answer: In traditional programming, explicit rules are coded, while in machine learning patterns are learned from data")
        st.markdown("_Explanation: Traditional programming requires developers to write explicit rules for every situation, while machine learning algorithms discover patterns from data without being explicitly programmed._")
        
        # Q2
        st.markdown("**Q2: Which of the following are characteristics of Generative AI? (Select all that apply)**")
        st.markdown(f"Your answer: {', '.join(st.session_state.answers['q2']) if st.session_state.answers['q2'] else 'No answer'}")
        st.markdown("Correct answers: Can create new content like text or images, Examples include DALL-E and ChatGPT")
        st.markdown("_Explanation: Generative AI creates new content and includes models like DALL-E and ChatGPT. It typically requires more (not less) computing power than traditional ML, and it works well with unstructured data._")
        
        # Q3
        st.markdown("**Q3: When is traditional programming more appropriate than machine learning?**")
        st.markdown(f"Your answer: {st.session_state.answers['q3'] if st.session_state.answers['q3'] else 'No answer'}")
        st.markdown("Correct answer: When the problem has well-defined rules and formulas")
        st.markdown("_Explanation: Traditional programming is best for problems with clear rules and deterministic outcomes, like mathematical calculations. ML is better for complex patterns, large datasets, and problems where rules are difficult to define._")
        
        # Q4
        st.markdown("**Q4: Which relationship correctly describes the hierarchy of these technologies?**")
        st.markdown(f"Your answer: {st.session_state.answers['q4'] if st.session_state.answers['q4'] else 'No answer'}")
        st.markdown("Correct answer: Generative AI is a subset of Machine Learning, which is a subset of Artificial Intelligence")
        st.markdown("_Explanation: AI is the broadest category encompassing all intelligent systems. ML is a subset of AI that learns from data. Generative AI is a specific type of ML focused on creating new content._")
        
        # Q5
        st.markdown("**Q5: Which of the following are appropriate use cases for machine learning? (Select all that apply)**")
        st.markdown(f"Your answer: {', '.join(st.session_state.answers['q5']) if st.session_state.answers['q5'] else 'No answer'}")
        st.markdown("Correct answers: Predicting customer churn based on past behavior, Detecting fraudulent credit card transactions")
        st.markdown("_Explanation: ML is ideal for predicting customer behavior and detecting fraud as these involve complex patterns. Temperature conversion and loan interest calculations follow simple mathematical formulas, making traditional programming more appropriate._")
        
        if st.button("Retake Quiz"):
            # Reset quiz state but keep session
            st.session_state.knowledge_check_started = False
            st.session_state.knowledge_check_submitted = False
            st.session_state.knowledge_check_score = 0
            st.session_state.answers = {
                "q1": None,
                "q2": [],
                "q3": None,
                "q4": None,
                "q5": []
            }
            st.experimental_rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

def render_footer():
    """Render footer with copyright information"""
    st.markdown("""
    <div style='text-align: center; padding: 20px; color: #545B64; font-size: 14px;'>
    © 2025, Amazon Web Services, Inc. or its affiliates. All rights reserved.
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main function to run the app"""
    # Initialize session state
    initialize_session_state()
    
    # Apply AWS styling
    apply_aws_style()
    
    # Sidebar content
    with st.sidebar:
        st.markdown("## AI Concepts E-Learning")
        st.markdown("### Session Management")
        st.markdown(f"**User ID:** {st.session_state.user_id}")
        
        if st.button("Reset Session"):
            reset_session()
        
        # About this app - collapsible
        with st.expander("About this App", expanded=False):
            st.write("An interactive e-learning platform to explore core AI concepts and differences between AI technologies.")
    
    # Main content
    st.markdown("<h1 class='title'>AI Concepts E-Learning</h1>", unsafe_allow_html=True)
    
    # Create tabs with emojis
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🧠 AI, ML & Generative AI",
        "🔄 Traditional vs ML",
        "⚖️ When to Use ML",
        "🤖 ML vs Generative AI",
        "📝 Knowledge Check"
    ])
    
    with tab1:
        render_topic_ai_ml_genai()
    
    with tab2:
        render_topic_traditional_vs_ml()
    
    with tab3:
        render_topic_when_to_use_ml()
    
    with tab4:
        render_topic_ml_vs_genai()
    
    with tab5:
        render_knowledge_check()
    
    # Footer
    render_footer()

if __name__ == "__main__":
    main()
# ```

# ## Requirements.txt
# ```
# streamlit==1.26.0
# pandas==2.0.3
# numpy==1.24.3
# matplotlib==3.7.2
# plotly==5.15.0
# scikit-learn==1.3.0
# pillow==9.5.0
# requests==2.31.0
# streamlit-lottie==0.0.5
# ```

# This implementation creates a responsive, well-structured e-learning application for AI concepts with:

# 1. AWS-themed styling and modern UI/UX
# 2. Tab-based navigation with emojis
# 3. Session management in the sidebar
# 4. Detailed explanations of:
#    - Differences between AI, ML, and Generative AI
#    - Traditional programming vs. machine learning
#    - When to use machine learning
#    - Machine Learning vs. Generative AI
# 5. Interactive examples for each concept
# 6. A knowledge check section with 5 questions (3 single-answer, 2 multi-answer)
# 7. Progress tracking for the knowledge check
# 8. AWS footer and collapsible "About" section

# The code is modular, follows Python best practices, and is optimized for web presentation via Streamlit.