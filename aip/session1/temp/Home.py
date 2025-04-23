
import streamlit as st
import uuid
import random
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="AI Fundamentals Learning",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define AWS color scheme
AWS_COLORS = {
    "orange": "#FF9900",
    "dark_blue": "#232F3E",
    "light_blue": "#1A73E8",
    "dark_gray": "#4D4D4D",
    "light_gray": "#F2F2F2",
    "white": "#FFFFFF",
    "black": "#000000"
}

# Define custom CSS for styling
def apply_custom_css():
    st.markdown("""
    <style>
        /* Main background and text colors */
        .stApp {
            background-color: #FFFFFF;
            color: #232F3E;
        }
        
        /* Header styles */
        h1, h2, h3, h4, h5 {
            color: #232F3E;
        }
        
        /* Accent elements */
        .stButton button, .stSelectbox, .stSlider, .stNumberInput {
            border-color: #FF9900 !important;
        }
        
        /* Button hover */
        .stButton button:hover {
            background-color: #FF9900 !important;
            color: white !important;
        }
        
        /* Card-like containers */
        .info-card {
            background-color: #F2F2F2;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #FF9900;
        }
        
        /* Knowledge Check styling */
        .question-card {
            background-color: #F2F2F2;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #1A73E8;
        }
        
        /* Footer style */
        .footer {
            text-align: center;
            padding: 20px;
            color: #4D4D4D;
            font-size: 14px;
            border-top: 1px solid #F2F2F2;
            margin-top: 40px;
        }
        
        /* Image container */
        .img-container {
            text-align: center;
            margin: 20px 0;
        }
        
        /* Emoji headers */
        .emoji-header {
            font-size: 24px;
            margin-bottom: 20px;
            color: #232F3E;
        }
        
        /* Table styling */
        .styled-table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 0.9em;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        }
        .styled-table thead tr {
            background-color: #232F3E;
            color: white;
            text-align: left;
        }
        .styled-table th,
        .styled-table td {
            padding: 12px 15px;
        }
        .styled-table tbody tr {
            border-bottom: 1px solid #dddddd;
        }
        .styled-table tbody tr:nth-of-type(even) {
            background-color: #f3f3f3;
        }
        
        /* Code block styling */
        code {
            background-color: #F2F2F2;
            padding: 2px 6px;
            border-radius: 4px;
            color: #232F3E;
            font-family: monospace;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #FFFFFF;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #EAEDED;
            border-radius: 5px 5px 0 0;
            gap: 1px;
            padding: 10px 16px;
            color: #232F3E;
        }
        .stTabs [aria-selected="true"] {
            background-color: #FF9900 !important;
            color: #232F3E !important;
            font-weight: bold;
        }
        .stTabs [data-baseweb="tab-highlight"] {
            display: none;
            {                


    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def initialize_session():
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

# Function to reset session
def reset_session():
    st.session_state.user_id = str(uuid.uuid4())
    st.session_state.quiz_started = False
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = {}
    st.session_state.submitted = False
    st.rerun()

# Function to render section headers with emojis
def section_header(emoji, text):
    st.markdown(f"""<div class="emoji-header">{emoji} {text}</div>""", unsafe_allow_html=True)

# Knowledge check questions
def load_questions():
    questions = [
        {
            "id": 1,
            "question": "Which of the following best describes how machine learning differs from traditional programming?",
            "options": [
                "Machine learning algorithms learn from data, while traditional programming follows explicit instructions",
                "Traditional programming uses data, machine learning doesn't",
                "Machine learning is only used for image recognition",
                "Machine learning works only on cloud platforms, traditional programming works locally"
            ],
            "answer": 0,
            "type": "single"
        },
        {
            "id": 2,
            "question": "Which of the following are types of supervised learning? (Select all that apply)",
            "options": [
                "Classification",
                "Regression",
                "Clustering",
                "Association"
            ],
            "answer": [0, 1],
            "type": "multi"
        },
        {
            "id": 3,
            "question": "What is the primary learning method used in generative AI foundation models?",
            "options": [
                "Supervised Learning",
                "Unsupervised Learning",
                "Self-supervised Learning",
                "Reinforcement Learning"
            ],
            "answer": 2,
            "type": "single"
        },
        {
            "id": 4,
            "question": "Which AWS service is designed to extract text and data from documents?",
            "options": [
                "Amazon Rekognition",
                "Amazon Textract",
                "Amazon Comprehend",
                "Amazon Kendra"
            ],
            "answer": 1,
            "type": "single"
        },
        {
            "id": 5,
            "question": "Which of the following situations would be best suited for machine learning rather than traditional programming? (Select all that apply)",
            "options": [
                "When you cannot create explicit rules to make decisions",
                "When you need human-like expertise at large scale",
                "When you need to adapt and personalize based on individual data",
                "When calculations need to be perfectly precise every time"
            ],
            "answer": [0, 1, 2],
            "type": "multi"
        }
    ]
    return questions

# Function to render an info card
def info_card(title, content):
    st.markdown(f"""
    <div class="info-card">
        <h3>{title}</h3>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)

# Content for AI concepts page
def ai_concepts():
    st.header("Basic AI Concepts and Terminologies")
    
    section_header("🧠", "What is AI, ML, and Generative AI?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Artificial Intelligence (AI)
        
        AI refers to computers that simulate human intelligence. It's the broadest category that encompasses all types of machine intelligence.
        
        **Key characteristics:**
        - Can perform tasks that typically require human intelligence
        - Includes reasoning, problem-solving, perception, and language understanding
        - Encompasses both rule-based systems and learning systems
        """)
    
    with col2:
        st.markdown("""
        ### Machine Learning (ML)
        
        Machine Learning is a subset of AI where computers automatically learn patterns from data to make predictions.
        
        **Key characteristics:**
        - Learns from data without explicit programming
        - Improves performance with more exposure to data
        - Makes predictions or decisions based on learned patterns
        """)
    
    st.markdown("""
    ### Deep Learning
    
    Deep Learning is a subset of Machine Learning that uses artificial neural networks with multiple layers.
    
    **Key characteristics:**
    - Excels with unstructured data (images, text, audio)
    - Uses neural networks inspired by the human brain
    - Capable of automatic feature extraction
    - Powers many modern AI applications
    """)
    
    st.markdown("""
    ### Generative AI
    
    Generative AI is a type of AI that can create new content (text, images, music, etc.) that didn't exist before.
    
    **Key characteristics:**
    - Creates novel content rather than just classifying or predicting
    - Often powered by large foundation models trained on vast datasets
    - Examples include text generation (GPT models), image creation (DALL-E, Stable Diffusion), and music composition
    """)
    
    st.markdown("""
    ### Foundation Models
    
    Foundation Models are large-scale, pre-trained AI models that serve as a base for fine-tuning on specific tasks.
    
    **Key characteristics:**
    - Pre-trained on internet-scale data
    - Can be adapted to multiple downstream tasks
    - Reduce the need for task-specific data collection and training
    - Examples include BERT, GPT, and T5 model families
    """)
    
    section_header("⚙️", "Traditional Programming vs. Machine Learning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Traditional Programming
        
        **Flow:** Input + Rules → Output
        
        In traditional programming, developers write explicit rules that the computer follows to process inputs and generate outputs. The rules must be completely defined by the programmer.
        
        **Example:** If a customer is over 30 years old AND has bought toys in the last 30 days, send them a toy promotion.
        
        **Limitations:**
        - Rules become complex and unmanageable as the problem grows
        - Difficult to account for all edge cases
        - Rules need manual updating as conditions change
        """)
    
    with col2:
        st.markdown("""
        ### Machine Learning
        
        **Flow:** Input + Output → Rules (Model)
        
        In machine learning, developers provide examples of inputs and corresponding outputs. The algorithm learns the underlying patterns and creates its own rules (model) to make predictions on new data.
        
        **Example:** Given customer data and their purchase history, the ML model learns patterns that predict which customers are likely to buy toys.
        
        **Advantages:**
        - Can handle complex relationships in data
        - Adapts as new data becomes available
        - Can discover patterns humans might miss
        """)
    
    section_header("🔍", "Machine Learning Types")
    
    st.markdown("""
    ## Types of Machine Learning
    
    Machine learning can be categorized into three main types based on how the algorithm learns:
    """)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Self-Supervised Learning"])
    
    with tab1:
        st.markdown("""
        ### Supervised Learning
        
        In supervised learning, the algorithm learns from labeled examples. It's given both the input data and the correct output (label).
        
        **How it works:**
        1. Algorithm is provided with labeled training data
        2. It learns the relationship between inputs and outputs
        3. Once trained, it can predict outputs for new inputs
        
        **Types of supervised learning:**
        - **Classification:** Predicts categorical labels (e.g., spam/not spam, cat/dog)
        - **Regression:** Predicts continuous values (e.g., house prices, temperature)
        
        **Real-world examples:**
        - Email spam detection
        - Credit scoring
        - Disease diagnosis
        - Price prediction
        """)
        
        st.image("https://miro.medium.com/v2/resize:fit:1400/1*JBSdDAjqwCUyNs2vXksL3Q.jpeg", caption="Supervised Learning Process", use_container_width=True)
    
    with tab2:
        st.markdown("""
        ### Unsupervised Learning
        
        In unsupervised learning, the algorithm learns from unlabeled data, finding patterns or structures without guidance.
        
        **How it works:**
        1. Algorithm is provided with unlabeled data
        2. It identifies patterns, similarities, or differences in the data
        3. It creates groupings or mappings based on discovered patterns
        
        **Types of unsupervised learning:**
        - **Clustering:** Groups similar data points together (e.g., customer segmentation)
        - **Dimensionality Reduction:** Reduces the number of variables while preserving information
        - **Association:** Identifies relationships between variables in large datasets
        
        **Real-world examples:**
        - Customer segmentation
        - Recommendation systems
        - Anomaly detection
        - Topic modeling
        """)
        
        st.image("https://miro.medium.com/v2/resize:fit:1400/1*0G-WZviswa8BgSf2QjPEMg.jpeg", caption="Unsupervised Learning Process", use_container_width=True)
    
    with tab3:
        st.markdown("""
        ### Reinforcement Learning
        
        In reinforcement learning, an agent learns to make decisions by taking actions in an environment to maximize rewards.
        
        **How it works:**
        1. Agent interacts with an environment
        2. Actions result in rewards or penalties
        3. Agent learns to maximize cumulative rewards over time
        
        **Key components:**
        - **Agent:** The decision-maker (the learning algorithm)
        - **Environment:** The world in which the agent operates
        - **Actions:** What the agent can do
        - **Rewards:** Feedback on how good an action was
        - **States:** Situations the agent finds itself in
        
        **Real-world examples:**
        - Game playing (AlphaGo, Chess)
        - Autonomous vehicles
        - Industrial robotics
        - Resource management
        """)
        
        st.image("https://miro.medium.com/v2/resize:fit:1400/1*HvoLc50Dpq1ESKuejhICHg.png", caption="Reinforcement Learning Process", use_container_width=True)
    
    with tab4:
        st.markdown("""
        ### Self-Supervised Learning
        
        Self-supervised learning is a type of learning where the system generates its own supervisory signals from the unlabeled data.
        
        **How it works:**
        1. Part of the input data is hidden or masked
        2. The model tries to predict the hidden part based on the visible part
        3. The hidden part serves as a pseudo-label for training
        
        **Distinctive features:**
        - Creates supervision from the data itself
        - Does not require human-annotated labels
        - Can leverage massive amounts of unlabeled data
        
        **Example:**
        In language models, words in sentences are masked, and the model learns to predict the masked words based on context.
        
        Original text: "The quick brown fox jumped over the lazy dog."
        Masked input: "The quick brown fox jumped over the [MASK] dog."
        Task: Predict that the masked word is "lazy"
        
        **Applications:**
        - Large language models like GPT, BERT
        - Image representation learning
        - Speech recognition pre-training
        """)
        
        st.image("https://miro.medium.com/v2/resize:fit:1400/1*8w1mT3EPJ4NJ-rFKYN_kUg.jpeg", caption="Self-Supervised Learning Process", use_container_width=True)
    
    section_header("📚", "AI Terminology")
    
    st.markdown("""
    ### Key Terminology in AI and ML
    
    Understanding these terms is essential for working with AI and ML systems:
    """)
    
    terminology_data = {
        "Term": ["Label/Target", "Feature", "Feature Engineering", "Feature Selection", "Model", "Training", "Inference", "Overfitting", "Underfitting", "Hyperparameters"],
        "Definition": [
            "What you are trying to predict (dependent variable)", 
            "Input data used to make predictions (independent variable)",
            "Process of creating new features from existing data to improve model performance",
            "Process of selecting the most relevant features for a model",
            "Mathematical representation learned from data that can make predictions",
            "Process of learning patterns from data",
            "Using a trained model to make predictions on new data",
            "When a model performs well on training data but poorly on new data",
            "When a model is too simple to capture the underlying pattern in the data",
            "Configuration settings that control how a model learns"
        ],
        "Example": [
            "Customer will purchase (yes/no), House price ($)",
            "Age, income, location, past purchase history",
            "Creating day-of-week from date, or converting temperature to categorical (hot/cold)",
            "Choosing only income and past purchases as predictors, discarding irrelevant features",
            "Random forest classifier, neural network, regression model",
            "Exposing a neural network to thousands of labeled images",
            "Using a trained spam filter to classify a new email",
            "A model that perfectly predicts training data but fails on new emails",
            "A linear model trying to fit complex non-linear data",
            "Learning rate, tree depth, number of hidden layers"
        ]
    }
    
    st.table(terminology_data)

# Content for practical use cases page
def practical_use_cases():
    st.header("Practical Use Cases for AI")
    
    st.markdown("""
    AI technologies are transforming industries across the world. Here we explore real-world applications where AI and ML are making significant impacts.
    """)
    
    section_header("💲", "Financial Services")
    
    col1, col2 = st.columns(2)
    
    with col1:
        info_card("Fraud Detection", """
        AI systems analyze transaction patterns to identify potential fraud in real-time. Traditional ML models like Random Forests and Gradient Boosting are preferred for their transparency and interpretability, which are crucial for regulatory compliance.
        <br><br>
                  <strong>Why Traditional ML:</strong> 
        <ul>
            <li>Clear decision rules that can be audited</li>
            <li>High accuracy with controlled false positives</li>
            <li>Regulatory requirements for explainability</li>
        </ul>
        """)
    
    with col2:
        info_card("Credit Risk Assessment", """
        ML models evaluate loan applicants by analyzing their financial history and predicting the likelihood of default. Models like logistic regression are widely used due to their interpretability.
        <br><br>
                  <strong>Why Traditional ML:</strong>
        <ul>
            <li>Transparent decision-making process</li>
            <li>Consistent evaluation criteria</li>
            <li>Ability to provide reasons for credit decisions</li>
        </ul>
        """)
    
    section_header("🏥", "Healthcare")
    
    col1, col2 = st.columns(2)
    
    with col1:
        info_card("Medical Diagnostics", """
        AI assists in analyzing medical images and patient data to detect diseases like cancer at early stages. Computer vision models can identify patterns in X-rays, MRIs, and CT scans that might be missed by human eyes.
        <br><br>
                  <strong>Key applications:</strong>
        <ul>
            <li>Radiology image analysis</li>
            <li>Pathology slide examination</li>
            <li>Early disease detection</li>
            <li>Treatment recommendation</li>
        </ul>
        """)
    
    with col2:
        info_card("Patient Monitoring", """
        ML models analyze real-time patient data to predict deterioration before critical symptoms appear. Time-series analysis and anomaly detection algorithms monitor vital signs and alert healthcare providers to potential issues.
        <br><br>
                  <strong>Benefits:</strong>
        <ul>
            <li>Early intervention opportunities</li>
            <li>Reduced ICU admissions</li>
            <li>Optimized resource allocation</li>
            <li>Improved patient outcomes</li>
        </ul>
        """)
    
    section_header("🏭", "Manufacturing and Industry")
    
    col1, col2 = st.columns(2)
    
    with col1:
        info_card("Predictive Maintenance", """
        ML models predict equipment failures before they occur by analyzing sensor data, maintenance records, and operational patterns. This reduces downtime and maintenance costs while extending equipment lifespan.
        <br><br>
        <strong>Implementation:</strong>
        <ul>
            <li>Sensor data collection from machinery</li>
            <li>Time-series analysis of operational patterns</li>
            <li>Anomaly detection for unusual behavior</li>
            <li>Scheduled maintenance before failure</li>
        </ul>
        """)
    
    with col2:
        info_card("Quality Control", """
        Computer vision systems inspect products on assembly lines to detect defects with greater accuracy and speed than human inspectors. These systems can work 24/7 without fatigue or inconsistency.
        <br><br>
        <strong>Advantages:</strong>
        <ul>
            <li>Consistent quality standards</li>
            <li>Detection of subtle defects</li>
            <li>Real-time feedback to manufacturing processes</li>
            <li>Reduction in waste and rework</li>
        </ul>
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:   
        section_header("🚗", "Automotive and Transportation")
        
        info_card("Autonomous Vehicles","""
        Self-driving cars represent one of the most complex AI applications, combining multiple ML techniques:
        <br><br>
        <ul>
            <li><strong>Computer Vision</strong>: Recognizes road signs, pedestrians, and other vehicles</li>
            <li><strong>Sensor Fusion</strong>: Integrates data from cameras, LIDAR, radar, and ultrasonic sensors</li>
            <li><strong>Reinforcement Learning</strong>: Improves driving decisions through experience</li>
            <li><strong>Path Planning</strong> Determines optimal routes considering traffic and obstacles</li>
        </ul>
        <br>
        The automotive industry prioritizes traditional ML approaches due to the safety-critical nature of driving, where decisions must be deterministic and explainable.
        """)
    
        section_header("🛡️", "Cybersecurity")
        
        info_card("Threat Detection and Response","""
        AI systems continuously monitor network traffic and system behavior to identify potential security threats:
        <br><br>
        <ul>
            <li><strong>Anomaly Detection</strong>: Identifies unusual patterns that may indicate breaches</li>
            <li><strong>User Behavior Analysis</strong>: Creates baselines of normal user activity to spot suspicious actions</li>
            <li><strong>Automated Response</strong>: Contains threats by isolating affected systems or blocking malicious traffic</li>
        </ul>
        <br>
        Traditional ML models excel in this domain due to:
                  <br>
        <p>1. Need for explainable security alerts</p>
        <p>2. Requirement for high precision (low false positives)</p>
        <p>3. Ability to adapt to new threat patterns</p>
        """)
    
    section_header("🛍️", "Retail and E-commerce")
    
    col1, col2 = st.columns(2)
    
    with col1:
        info_card("Personalized Recommendations", """
        AI analyzes browsing history, purchase patterns, and demographic information to recommend products customers are likely to purchase. This increases sales and improves customer experience.
        <br><br>
                  <strong>AWS Solution:</strong> Amazon Personalize provides recommendation capabilities similar to those used by Amazon.com.
        """)
    
    with col2:
        info_card("Inventory Management", """
        ML models predict product demand based on historical data, seasonal trends, and external factors like weather or events. This helps retailers optimize inventory levels and reduce costs.
        <br><br>
                  <strong>Benefits:</strong>
        <ul>
            <li>Reduced stockouts and overstocking</li>
            <li>Improved cash flow</li>
            <li>Enhanced customer satisfaction</li>
            <li>Optimized supply chain operations</li>
        </ul>
        """)
    
    st.markdown("""
    ## Choosing Between Traditional ML and Generative AI
    
    When deciding which approach to use for a specific use case, consider these factors:
    """)
    
    comparison_data = {
        "Factor": ["Interpretability", "Data Requirements", "Task Specificity", "Regulatory Compliance", "Consistency"],
        "Traditional ML": [
            "High - decisions can be traced and explained", 
            "Can work with smaller, structured datasets",
            "Optimized for specific tasks with clear objectives",
            "Easier to validate and document decision processes",
            "Produces consistent outputs for the same inputs"
        ],
        "Generative AI": [
            "Lower - complex models can be 'black boxes'",
            "Typically requires massive datasets",
            "Versatile across multiple tasks but may lack specialization",
            "More challenging to validate decision-making process",
            "May produce varying outputs for the same prompt"
        ],
        "Best For": [
            "Financial services, healthcare, legal applications",
            "Specialized business problems with limited data",
            "Problems requiring high precision in specific domains",
            "Highly regulated industries",
            "Mission-critical applications requiring predictability"
        ]
    }
    
    st.table(comparison_data)

# Content for ML development lifecycle page
def ml_development_lifecycle():
    st.header("Machine Learning Development Lifecycle")
    
    st.markdown("""
    The ML development lifecycle is an iterative process that transforms a business problem into a deployed ML solution. Understanding this lifecycle is essential for successfully implementing ML projects.
    """)
    
    section_header("🔄", "Overview of the ML Process")
    
    st.image("https://miro.medium.com/v2/resize:fit:1400/1*KzmIUYPmxgEHhXX7S1HCRA.png", caption="Machine Learning Development Lifecycle", use_container_width=True)
    
    st.markdown("""
    ## The 9 Phases of ML Development
    
    Machine learning development can be broken down into these key phases:
    """)
    
    phases = [
        {
            "name": "Business Problem Framing", 
            "description": "Identify the business challenge and determine if ML is an appropriate solution. Define clear objectives and success metrics.",
            "key_activities": ["Stakeholder interviews", "Problem definition", "Success criteria establishment", "Feasibility assessment"],
            "outputs": ["Project charter", "Success metrics", "ML problem statement"]
        },
        {
            "name": "Data Collection and Integration", 
            "description": "Gather relevant data from various sources and consolidate it for analysis. Ensure data quality and relevance.",
            "key_activities": ["Source identification", "Data extraction", "Integration of disparate sources", "Initial quality assessment"],
            "outputs": ["Raw dataset", "Data catalog", "Source mapping documentation"]
        },
        {
            "name": "Data Preparation", 
            "description": "Clean, normalize, and transform data to make it suitable for modeling. Handle missing values, outliers, and inconsistencies.",
            "key_activities": ["Data cleaning", "Missing value imputation", "Outlier detection", "Format standardization"],
            "outputs": ["Cleaned dataset", "Data quality report", "Transformation documentation"]
        },
        {
            "name": "Data Visualization and Analysis", 
            "description": "Explore and analyze data to understand patterns, relationships, and potential features. Generate insights to inform model design.",
            "key_activities": ["Exploratory data analysis", "Statistical analysis", "Correlation studies", "Distribution visualization"],
            "outputs": ["EDA report", "Statistical summaries", "Visual insights", "Initial feature ideas"]
        },
        {
            "name": "Feature Engineering", 
            "description": "Create new features or transform existing ones to improve model performance. Select the most relevant features for modeling.",
            "key_activities": ["Feature creation", "Feature transformation", "Feature selection", "Dimension reduction"],
            "outputs": ["Feature set", "Feature importance analysis", "Engineering documentation"]
        },
        {
            "name": "Model Training and Parameter Tuning", 
            "description": "Select appropriate algorithms, train models on the prepared data, and optimize parameters to improve performance.",
            "key_activities": ["Algorithm selection", "Training dataset preparation", "Model training", "Hyperparameter tuning"],
            "outputs": ["Trained models", "Training metrics", "Parameter configurations"]
        },
        {
            "name": "Model Evaluation", 
            "description": "Assess model performance against business objectives using appropriate metrics and validation techniques.",
            "key_activities": ["Validation strategy implementation", "Metric calculation", "Cross-validation", "Business impact assessment"],
            "outputs": ["Performance metrics", "Validation report", "Business value assessment"]
        },
        {
            "name": "Model Deployment", 
            "description": "Implement the validated model in a production environment where it can generate real business value.",
            "key_activities": ["Deployment strategy selection", "Integration with existing systems", "Scaling considerations", "Monitoring setup"],
            "outputs": ["Deployed model", "API documentation", "Deployment architecture"]
        },
        {
            "name": "Monitoring and Debugging", 
            "description": "Continuously track model performance, detect issues, and maintain effectiveness over time. Update as needed.",
            "key_activities": ["Performance monitoring", "Drift detection", "Error analysis", "Model updating"],
            "outputs": ["Monitoring dashboard", "Alert systems", "Maintenance schedule", "Performance reports"]
        }
    ]
    
    # Use tabs to display phases
    tabs = st.tabs([phase["name"] for phase in phases])
    
    for i, tab in enumerate(tabs):
        with tab:
            st.subheader(phases[i]["name"])
            st.markdown(phases[i]["description"])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Key Activities")
                for activity in phases[i]["key_activities"]:
                    st.markdown(f"• {activity}")
            
            with col2:
                st.markdown("#### Outputs")
                for output in phases[i]["outputs"]:
                    st.markdown(f"• {output}")
    
    section_header("🧩", "AWS AI/ML Services Stack")
    
    st.markdown("""
    AWS offers a comprehensive stack of AI and ML services that can support different stages of the ML development lifecycle:
    """)
    
    st.image("https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2023/03/30/ML-2230-1.jpg", caption="AWS AI/ML Services Stack", use_container_width=True)
    
    st.markdown("""
    ### Three Layers of AWS AI/ML Stack:
    
    1. **AI Services (Top Layer)**
       - Pre-trained AI services requiring no ML expertise
       - Examples: Amazon Rekognition, Amazon Textract, Amazon Comprehend
       - Use case: Quick implementation of specific AI capabilities through APIs
    
    2. **ML Services (Middle Layer)**
       - Amazon SageMaker and related tools for building custom ML models
       - Examples: SageMaker Studio, Canvas, JumpStart, Ground Truth
       - Use case: Building custom ML models with reduced overhead
    
    3. **ML Frameworks and Infrastructure (Bottom Layer)**
       - Flexible infrastructure for advanced ML workloads
       - Examples: Deep Learning AMIs, EC2 instances with GPUs
       - Use case: Highly specialized ML workloads requiring complete control
    """)
    
    section_header("🔧", "Key AWS AI Services")
    
    services = [
        {
            "name": "Amazon Rekognition",
            "description": "Automates image and video analysis with machine learning",
            "use_cases": ["Media analysis", "Identity verification", "Content moderation"],
            "key_features": ["Object detection", "Facial analysis", "Text detection", "Celebrity recognition"]
        },
        {
            "name": "Amazon Textract",
            "description": "Extracts text and data from scanned documents",
            "use_cases": ["Smart search indexes", "Automated document processing", "Compliance management"],
            "key_features": ["OCR", "Form extraction", "Table extraction", "Natural language processing"]
        },
        {
            "name": "Amazon Comprehend",
            "description": "Discovers insights and relationships in text using NLP",
            "use_cases": ["Call center analytics", "Product review analysis", "Content personalization"],
            "key_features": ["Entity recognition", "Sentiment analysis", "Topic modeling", "Language detection"]
        },
        {
            "name": "Amazon Kendra",
            "description": "Enterprise search service powered by machine learning",
            "use_cases": ["Internal knowledge base search", "Customer support enhancement", "Research assistance"],
            "key_features": ["Natural language questions", "Data connector integration", "Relevance tuning", "Incremental learning"]
        },
        {
            "name": "Amazon Personalize",
            "description": "Creates real-time personalized recommendations",
            "use_cases": ["Product recommendations", "Content personalization", "Personalized marketing"],
            "key_features": ["Real-time recommendations", "Easy implementation", "Contextual personalization"]
        },
        {
            "name": "Amazon Fraud Detector",
            "description": "Detects online fraud using machine learning",
            "use_cases": ["Account fraud", "Payment fraud", "Loyalty program abuse"],
            "key_features": ["Customized fraud detection", "No ML expertise required", "Pay-per-use pricing"]
        }
    ]
    
    # Use tabs for services
    service_tabs = st.tabs([service["name"] for service in services])
    
    for i, tab in enumerate(service_tabs):
        with tab:
            st.subheader(services[i]["name"])
            st.markdown(services[i]["description"])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Use Cases")
                for use_case in services[i]["use_cases"]:
                    st.markdown(f"• {use_case}")
            
            with col2:
                st.markdown("#### Key Features")
                for feature in services[i]["key_features"]:
                    st.markdown(f"• {feature}")
    
    section_header("📈", "Amazon SageMaker")
    
    st.markdown("""
    Amazon SageMaker is AWS's flagship ML service that provides tools for every step of the ML development lifecycle:
    """)
    
    st.image("https://d1.awsstatic.com/r2018/h/99product-page-diagram_Amazon-SageMaker-0101.ff313db5b5eb6b9c9805add129acc4fe55154ffe.png", caption="Amazon SageMaker End-to-End ML Platform", use_container_width=True)
    
    st.markdown("""
    ### SageMaker Components by ML Phase:
    
    #### Prepare
    - **Ground Truth**: Create high-quality labeled datasets
    - **Data Wrangler**: Aggregate and prepare data for ML
    - **Feature Store**: Store, catalog, and reuse features
    - **Clarify**: Detect bias and explain model predictions
    
    #### Build
    - **Studio/Notebooks**: Fully managed Jupyter notebooks
    - **Canvas**: No-code ML for business users
    - **JumpStart**: Pre-built models and solutions
    - **Autopilot**: Automated ML model creation
    
    #### Train & Tune
    - **Training**: Fully managed model training with various hardware options
    - **Distributed Training**: Scale training across multiple instances
    - **Hyperparameter Tuning**: Automatic optimization of model parameters
    - **Debugger**: Debug and profile training jobs
    
    #### Deploy & Manage
    - **Endpoints**: Deploy models for real-time inference
    - **Batch Transform**: Process large batches of data
    - **Model Monitor**: Track model quality and drift
    - **Pipeline**: Automate ML workflows
    """)

# Function for knowledge check
def knowledge_check():
    st.header("Knowledge Check")
    
    questions = load_questions()
    
    if not st.session_state.quiz_started:
        st.markdown("""
        Test your understanding of AI and ML fundamentals with this quick quiz. It consists of 5 questions covering key concepts we've discussed.
        
        Click "Start Quiz" when you're ready to begin.
        """)
        
        if st.button("Start Quiz"):
            st.session_state.quiz_started = True
            st.rerun()
    else:
        if not st.session_state.submitted:
            question = questions[st.session_state.current_question]
            
            st.markdown(f"""
            <div class="question-card">
                <h3>Question {question['id']} of {len(questions)}</h3>
                <p>{question['question']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if question['type'] == 'single':
                answer = st.radio("Select one answer:", question['options'], key=f"q{question['id']}")
                selected_index = question['options'].index(answer)
                st.session_state.answers[question['id']] = selected_index
            else:  # multi
                selected_options = []
                for i, option in enumerate(question['options']):
                    if st.checkbox(option, key=f"q{question['id']}_{i}"):
                        selected_options.append(i)
                st.session_state.answers[question['id']] = selected_options
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.session_state.current_question > 0:
                    if st.button("Previous"):
                        st.session_state.current_question -= 1
                        st.rerun()
            
            with col2:
                if st.session_state.current_question < len(questions) - 1:
                    if st.button("Next"):
                        st.session_state.current_question += 1
                        st.rerun()
                else:
                    if st.button("Submit Quiz"):
                        # Calculate score
                        for q_id, selected_answer in st.session_state.answers.items():
                            question_index = q_id - 1
                            correct_answer = questions[question_index]['answer']
                            
                            if questions[question_index]['type'] == 'single':
                                if selected_answer == correct_answer:
                                    st.session_state.score += 1
                            else:  # multi
                                if set(selected_answer) == set(correct_answer):
                                    st.session_state.score += 1
                        
                        st.session_state.submitted = True
                        st.rerun()
        else:
            # Show results
            score_percentage = (st.session_state.score / len(questions)) * 100
            
            st.markdown(f"""
            <div class="info-card">
                <h3>Quiz Results</h3>
                <p>You scored {st.session_state.score} out of {len(questions)} ({score_percentage:.1f}%).</p>
            </div>
            """, unsafe_allow_html=True)
            
            for q_id, selected_answer in st.session_state.answers.items():
                question_index = q_id - 1
                question = questions[question_index]
                correct_answer = question['answer']
                
                is_correct = False
                if question['type'] == 'single':
                    is_correct = selected_answer == correct_answer
                else:  # multi
                    is_correct = set(selected_answer) == set(correct_answer)
                
                result_color = "#4CAF50" if is_correct else "#F44336"
                
                st.markdown(f"""
                <div style="margin-bottom: 20px; padding: 15px; border-left: 5px solid {result_color}; background-color: #F2F2F2;">
                    <h4>Question {q_id}: {question['question']}</h4>
                """, unsafe_allow_html=True)
                
                if question['type'] == 'single':
                    for i, option in enumerate(question['options']):
                        prefix = "✓ " if i == correct_answer else ""
                        selected = i == selected_answer
                        style = "font-weight: bold;" if selected else ""
                        correct_style = "color: #4CAF50;" if i == correct_answer else ""
                        incorrect_style = "color: #F44336;" if selected and i != correct_answer else ""
                        st.markdown(f"<p style='{style} {correct_style} {incorrect_style}'>{prefix}{option}</p>", unsafe_allow_html=True)
                else:  # multi
                    for i, option in enumerate(question['options']):
                        prefix = "✓ " if i in correct_answer else ""
                        selected = i in selected_answer
                        style = "font-weight: bold;" if selected else ""
                        correct_style = "color: #4CAF50;" if i in correct_answer else ""
                        incorrect_style = "color: #F44336;" if selected and i not in correct_answer else ""
                        st.markdown(f"<p style='{style} {correct_style} {incorrect_style}'>{prefix}{option}</p>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            if st.button("Retake Quiz"):
                st.session_state.quiz_started = False
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.answers = {}
                st.session_state.submitted = False
                st.rerun()

# Main application
def main():
    # Apply custom CSS
    apply_custom_css()
    
    # Initialize session state
    initialize_session()
    
    # Sidebar
    st.sidebar.markdown("### Session Management")
    st.sidebar.info(f"**Session ID:** {st.session_state.user_id[:8]}...")
    
    if st.sidebar.button("🔄 Reset Session"):
        reset_session()
    
    with st.sidebar.expander("About this App", expanded=False):
        st.write("An interactive learning platform for understanding the fundamentals of AI and ML concepts, use cases, and development lifecycle.")
    
    # Main content
    st.title("🤖 AI Fundamentals")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📚 AI Concepts", 
        "🔍 Use Cases", 
        "🔄 ML Lifecycle", 
        "❓ Knowledge Check"
    ])
    
    with tab1:
        ai_concepts()
    
    with tab2:
        practical_use_cases()
    
    with tab3:
        ml_development_lifecycle()
    
    with tab4:
        knowledge_check()
    
    # Footer
    st.markdown("""
    <div class="footer">
        © 2025, Amazon Web Services, Inc. or its affiliates. All rights reserved.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
# ```

# ## Requirements.txt

# ```
# streamlit==1.31.1
# pandas==2.2.0
# numpy==1.26.3
# Pillow==10.2.0
# plotly==5.18.0
# matplotlib==3.8.2
# uuid==1.30
# ```

# ## Application Features

# 1. **Tab-Based Navigation**:
#    - AI Concepts
#    - Practical Use Cases
#    - ML Development Lifecycle
#    - Knowledge Check

# 2. **Interactive Elements**:
#    - Knowledge check with single and multiple-choice questions
#    - Expandable sections
#    - Visual elements (tables, cards)

# 3. **AWS Styling**:
#    - AWS color scheme (Orange, Dark Blue, etc.)
#    - Clean, modern interface
#    - Responsive layout

# 4. **Session Management**:
#    - Unique user ID
#    - Session reset functionality
#    - Score tracking for knowledge check

# 5. **Content Organization**:
#    - Clearly structured topics
#    - Visual aids (images, tables)
#    - Information cards

# This application provides an engaging, interactive learning experience for understanding AI and ML fundamentals, following AWS's styling guidelines and best practices for Streamlit application development.