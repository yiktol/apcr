
import streamlit as st
import pandas as pd
import random
from PIL import Image
import base64
import io

# Set page configuration
st.set_page_config(
    page_title="AWS ML Engineer Associate Exam Simulator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define AWS color scheme
aws_colors = {
    "primary": "#232F3E",    # AWS Navy
    "secondary": "#FF9900",  # AWS Orange
    "accent1": "#1A2B3C",    # Dark blue
    "accent2": "#00A1C9",    # Light blue
    "text": "#16191F",       # Dark text
    "success": "#1E8E3E",    # Green for success
    "warning": "#F9CB9C",    # Light orange for warnings
    "error": "#D13212"       # Red for errors/wrong answers
}

# Custom CSS
st.markdown(f"""
<style>
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {aws_colors["primary"]};
    }}
    .stButton button {{
        background-color: {aws_colors["secondary"]};
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: bold;
    }}
    .stButton button:hover {{
        background-color: {aws_colors["primary"]};
        color: {aws_colors["secondary"]};
    }}
    .correct-answer {{
        background-color: #E6F7E6;
        padding: 1rem;
        border-left: 5px solid {aws_colors["success"]};
        border-radius: 5px;
        margin: 1rem 0;
    }}
    .wrong-answer {{
        background-color: #FFEBEE;
        padding: 1rem;
        border-left: 5px solid {aws_colors["error"]};
        border-radius: 5px;
        margin: 1rem 0;
    }}
    .info-box {{
        background-color: #E3F2FD;
        padding: 1rem;
        border-left: 5px solid {aws_colors["accent2"]};
        border-radius: 5px;
        margin: 1rem 0;
    }}
    .aws-card {{
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }}
    .sidebar .sidebar-content {{
        background-color: {aws_colors["primary"]};
    }}
    .css-1d391kg {{
        background-color: {aws_colors["primary"]};
    }}
    footer {{
        visibility: hidden;
    }}
    .progress-container {{
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
        background-color: #f0f2f5;
    }}
    .stProgress > div > div > div > div {{
        background-color: {aws_colors["secondary"]};
    }}
    .mode-selector {{
        background-color: #f0f2f5;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 15px;
    }}
</style>
""", unsafe_allow_html=True)

# Function to generate AWS-style progress bar
def aws_progress_bar(percentage, text=""):
    st.markdown(f"""
    <div class="progress-container">
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <span>{text}</span>
            <span>{percentage}%</span>
        </div>
        <div style="height: 8px; width: 100%; background-color: #E6E6E6; border-radius: 4px;">
            <div style="height: 100%; width: {percentage}%; background-color: {aws_colors["secondary"]}; border-radius: 4px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Function to create an AWS-style card
def aws_card(content, key=None):
    st.markdown(f'<div class="aws-card">{content}</div>', unsafe_allow_html=True)

# Generate AWS-style header with logo
def aws_header():
    cols = st.columns([1, 5])
    
    # Create an AWS-style logo
    
    aws_logo = """
    <svg width="100" height="60" viewBox="0 0 100 60" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M29.5 30C29.5 32.5 27.5 39 23 39C18.5 39 16.5 33 16.5 30C16.5 27 18.5 21 23 21C27.5 21 29.5 27.5 29.5 30Z" fill="#FF9900"/>
        <path d="M55.5 30C55.5 32.5 53.5 39 49 39C44.5 39 42.5 33 42.5 30C42.5 27 44.5 21 49 21C53.5 21 55.5 27.5 55.5 30Z" fill="#FF9900"/>
        <path d="M80 25.5V35.5C80 37.7 78.2 39.5 76 39.5H69C66.8 39.5 65 37.7 65 35.5V25.5C65 23.3 66.8 21.5 69 21.5H76C78.2 21.5 80 23.3 80 25.5Z" fill="#FF9900"/>
    </svg>
    """
    
    with cols[0]:
        # st.markdown(aws_logo, unsafe_allow_html=True)
        st.image("https://d0.awsstatic.com/logos/powered-by-aws.png", width=200)
    
    with cols[1]:
        st.markdown("<h1 style='color: #232F3E; margin-bottom: 0;'>Machine Learning Engineer - Associate</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #FF9900; margin-top: 0;'>Certification Exam Simulator</h3>", unsafe_allow_html=True)

# Question data
questions = [
    {
        "question": "A company is developing a machine learning model using Amazon SageMaker to detect anomalies using the Random Cut Forest algorithm. The machine learning engineer needs to ensure that the data used to train the model is properly structured and stored in the appropriate location. Which of the following would be the most operationally efficient for storing the data so they can start training immediately?",
        "options": [
            "Tabular data in a CSV file in Amazon S3",
            "JSON documents in an Amazon DynamoDB table",
            "Transactional data in an Amazon RDS",
            "Structured data in an Amazon Redshift data warehouse"
        ],
        "correct": "Tabular data in a CSV file in Amazon S3",
        "explanations": {
            "Tabular data in a CSV file in Amazon S3": "Tabular data in a CSV file stored in Amazon S3 is the most suitable format because: Time series data for anomaly detection fits naturally into a tabular format with timestamps and metrics. SageMaker's built-in algorithms like Random Cut Forest expect CSV input format. S3 provides the necessary scalability for storing large volumes of metric data. CSV format allows easy representation of numerical features and timestamps. Efficient for batch processing and model training.",
            "JSON documents in an Amazon DynamoDB table": "While good for storing raw metrics data, JSON documents in DynamoDB are not optimal for ML training. It would require additional transformation steps to prepare for SageMaker. JSON format adds unnecessary complexity for time series data that is inherently tabular.",
            "Transactional data in an Amazon RDS": "Amazon RDS is better suited for operational database needs. It would require extraction and formatting for ML use. This adds unnecessary overhead when dealing with time series metrics.",
            "Structured data in an Amazon Redshift data warehouse": "While good for analyzing metrics data, Redshift is not optimal for direct ML consumption. It would still require export to S3 for SageMaker training. It's more complex and expensive than necessary for this specific use case. If using Redshift ML, it doesn't support RCF algorithm. Otherwise, they would need to extract the data to S3 first."
        },
        "type": "single"
    },
    {
        "question": "A team has developed a machine learning model to predict customer churn. The machine learning engineer needs to create a visual dashboard to help the business stakeholders understand the relationship between two variables that may influence churn. Which type of graph or chart would be the most appropriate to visualize this relationship in the customer churn prediction model?",
        "options": [
            "Pie chart",
            "Scatter plot",
            "Confusion matrix",
            "Line graph"
        ],
        "correct": "Scatter plot",
        "explanations": {
            "Pie chart": "A pie chart is used to show the composition of a whole, divided into parts. It is not suitable for showing the relationship between two continuous variables. Pie charts are better for displaying categorical data as percentages of a total, which is not what's required in this scenario.",
            "Scatter plot": "A scatter plot is the most appropriate type of graph to visualize the relationship between two continuous variables. In this case, the machine learning engineer needs to show the relationship between two continuous variables that may influence customer churn. Scatter plots are excellent for displaying how one variable changes with respect to another, allowing stakeholders to easily identify patterns, correlations, or clusters in the data.",
            "Confusion matrix": "A confusion matrix is typically used to evaluate the performance of a classification model by showing the counts of true positives, true negatives, false positives, and false negatives. While it can be useful in analyzing the results of a churn prediction model, it does not show the relationship between continuous variables that influence churn.",
            "Line graph": "While a line graph can show trends over time for continuous variables, it is not the best choice for showing the relationship between two variables that may influence churn. Line graphs are more suitable for displaying how a single variable changes over time or across categories, rather than showing the correlation between two variables."
        },
        "type": "single"
    },
    {
        "question": "A machine learning engineer is working with a large dataset containing categorical data that is updated weekly. They are using Amazon SageMaker Data Wrangler to preprocess their data and have defined a categorical encoding transform for a column containing nominal categories. New categories are frequently introduced into the column after the Data Wrangler job was created. The machine learning engineer wants to ensure that their job continues to run successfully even when encountering these new categories, while still properly encoding the known categories. Which of the following approaches would best meet these requirements?",
        "options": [
            "Use the one-hot encoding option and set the Invalid handling strategy to 'skip'",
            "Use the ordinal encoding option and set the Invalid handling strategy to 'skip'",
            "Use the one-hot encoding option and set the Invalid handling strategy to 'error'",
            "Use the ordinal encoding option and set the Invalid handling strategy to 'error'"
        ],
        "correct": "Use the one-hot encoding option and set the Invalid handling strategy to 'skip'",
        "explanations": {
            "Use the one-hot encoding option and set the Invalid handling strategy to 'skip'": "This approach uses one-hot encoding, which is appropriate for nominal categories. Setting the Invalid handling strategy to 'skip' allows the job to continue processing when it encounters new categories, meeting the requirement of ensuring the job runs successfully. Known categories will still be properly encoded.",
            "Use the ordinal encoding option and set the Invalid handling strategy to 'skip'": "While the 'skip' strategy allows the job to continue running when encountering new categories, ordinal encoding is not appropriate for nominal categories. Ordinal encoding assumes an order among categories, which may not exist in nominal data.",
            "Use the one-hot encoding option and set the Invalid handling strategy to 'error'": "Although one-hot encoding is appropriate for nominal categories, setting the Invalid handling strategy to 'error' would cause the job to fail when encountering new categories. This doesn't meet the requirement of ensuring the job continues to run successfully.",
            "Use the ordinal encoding option and set the Invalid handling strategy to 'error'": "This option is incorrect for two reasons: ordinal encoding is not suitable for nominal categories, and the 'error' strategy would cause the job to fail when encountering new categories, not meeting the requirement of continuous successful operation."
        },
        "type": "single"
    },
    {
        "question": "A machine learning engineer is building a machine learning pipeline using Amazon SageMaker and needs to create a feature store to manage and share features across different teams and accounts. The feature store should be able to handle both real-time and batch inference, as well as store historical data for model training and batch inference. Which of the following configurations would meet these requirements with the least management overhead?",
        "options": [
            "Create a feature group with an online store only.",
            "Create a feature group with an offline store only.",
            "Create a feature group with both online and offline stores.",
            "Create separate feature groups for online and offline stores."
        ],
        "correct": "Create a feature group with both online and offline stores.",
        "explanations": {
            "Create a feature group with an online store only.": "An online store only would not meet the requirement for storing historical data for model training and batch inference. Online stores are designed for real-time predictions with low latency reads and high throughput writes.",
            "Create a feature group with an offline store only.": "An offline store only would not meet the requirement for real-time inference. Offline stores are designed for storing large amounts of data for model training and batch inference.",
            "Create a feature group with both online and offline stores.": "Creating a feature group with both online and offline stores would meet the requirements for both real-time and batch inference, as well as storing historical data for model training and batch inference.",
            "Create separate feature groups for online and offline stores.": "Creating separate feature groups for online and offline stores would not allow for seamless integration between real-time and batch inference, and would require additional complexity in managing multiple feature groups."
        },
        "type": "single"
    },
    {
        "question": "A machine learning engineer at a financial institution is working on a binary classification problem to detect fraudulent transactions. The dataset is small and imbalanced, with only 5% of the transactions being fraudulent. The machine learning engineer wants to balance the dataset to create a better model. Which technique should they use to balance the dataset?",
        "options": [
            "Use Random Oversampling",
            "Use Random Undersampling",
            "Use Synthetic Minority Oversampling Technique (SMOTE)",
            "Use Cross Validation"
        ],
        "correct": "Use Synthetic Minority Oversampling Technique (SMOTE)",
        "explanations": {
            "Use Random Oversampling": "Random oversampling involves duplicating examples from the minority class, which can lead to overfitting and doesn't add new information to the dataset.",
            "Use Random Undersampling": "Random undersampling involves randomly removing examples from the majority class, which reduces the amount of training data and can discard valuable information.",
            "Use Synthetic Minority Oversampling Technique (SMOTE)": "Synthetic Minority Oversampling Technique (SMOTE) generates synthetic samples for the minority class by interpolating between existing minority class instances, helping the model generalize better without the risk of overfitting.",
            "Use Cross Validation": "Cross-validation is a technique for evaluating model performance, not for balancing the dataset. It does not address the issue of class imbalance directly."
        },
        "type": "single",
        "additional_info": """
        <div>
            <h4>When to use random oversampling vs SMOTE:</h4>
            <h5>Random Oversampling:</h5>
            <ul>
                <li>Use random oversampling when you have a relatively small imbalance in your dataset, and you want to simply duplicate the minority class samples to increase their representation.</li>
                <li>Random oversampling is a simpler and faster technique, but it can lead to overfitting as it creates duplicate samples without adding any new information.</li>
            </ul>
            <h5>SMOTE:</h5>
            <ul>
                <li>Use SMOTE when you have a more severe class imbalance, and you want to generate synthetic minority class samples to improve the model's performance.</li>
                <li>SMOTE creates new minority class samples by interpolating between existing minority class samples, which can help the model learn better decision boundaries without overfitting.</li>
                <li>SMOTE is more effective than random oversampling in improving model performance on imbalanced datasets, especially when the imbalance is significant.</li>
            </ul>
        </div>
        """
    }
]

# Helper functions
def initialize_session_state():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'exam_completed' not in st.session_state:
        st.session_state.exam_completed = False
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = len(questions)
    if 'mode' not in st.session_state:
        st.session_state.mode = "Practice Mode"
    # New score tracking approach
    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = {}

def reset_session():
    st.session_state.current_question = 0
    st.session_state.answers = {}
    st.session_state.submitted = False
    st.session_state.exam_completed = False
    # Reset the correct answers tracking
    st.session_state.correct_answers = {}
    # Keep the mode selection

def next_question():
    st.session_state.submitted = False
    st.session_state.current_question += 1
    if st.session_state.current_question >= st.session_state.total_questions:
        st.session_state.exam_completed = True
        calculate_results()

def prev_question():
    st.session_state.submitted = False
    st.session_state.current_question -= 1
    if st.session_state.current_question < 0:
        st.session_state.current_question = 0

def submit_answer():
    st.session_state.submitted = True
    
    # Check if answer is correct
    if st.session_state.current_question in st.session_state.answers:
        current_q = questions[st.session_state.current_question]
        selected_answer = st.session_state.answers[st.session_state.current_question]
        
        # For single-answer questions
        if current_q["type"] == "single":
            is_correct = selected_answer == current_q["correct"]
        # For multi-select questions
        else:
            is_correct = set(selected_answer) == set(current_q["correct"])
            
        # Store whether this question was answered correctly
        st.session_state.correct_answers[st.session_state.current_question] = is_correct

def calculate_results():
    # Count correct answers
    correct_count = sum(1 for is_correct in st.session_state.correct_answers.values() if is_correct)
    percentage = (correct_count / st.session_state.total_questions) * 100
    
    # Store results in session state
    st.session_state.correct_count = correct_count
    st.session_state.percentage = percentage

def go_to_results():
    st.session_state.exam_completed = True
    calculate_results()

def set_mode(mode):
    st.session_state.mode = mode
    # Reset the test when switching modes
    reset_session()

# Charts and visualizations
def create_pie_chart():
    # Calculate correct answers for visualization
    correct_count = sum(1 for is_correct in st.session_state.correct_answers.values() if is_correct)
    total = st.session_state.total_questions
    incorrect = total - correct_count
    
    # Generate a simple bar chart as a base64 string
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(6, 4))
    plt.bar(['Correct', 'Incorrect'], [correct_count, incorrect], color=[aws_colors["success"], aws_colors["error"]])
    plt.title('Exam Results')
    plt.ylabel('Number of Questions')
    plt.grid(axis='y', alpha=0.3)
    
    for i, v in enumerate([correct_count, incorrect]):
        plt.text(i, v + 0.1, str(v), ha='center')
    
    # Save the figure to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Return the base64 encoded image
    return base64.b64encode(buf.read()).decode()

def create_scatter_plot():
    # Create sample data for demonstration of scatter plot
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Sample data showing relationship between usage time and churn probability
    np.random.seed(42)
    usage_time = np.random.normal(50, 20, 100)
    churn_prob = 0.8 - 0.015 * usage_time + np.random.normal(0, 0.1, 100)
    churn_prob = np.clip(churn_prob, 0, 1)
    
    # Color points based on churn probability
    colors = ['#D13212' if p > 0.5 else '#1E8E3E' for p in churn_prob]
    
    plt.figure(figsize=(8, 6))
    plt.scatter(usage_time, churn_prob, c=colors, alpha=0.7)
    plt.title('Relationship Between Usage Time and Churn Probability')
    plt.xlabel('Weekly Usage Time (hours)')
    plt.ylabel('Churn Probability')
    plt.grid(True, alpha=0.3)
    
    # Add trend line
    z = np.polyfit(usage_time, churn_prob, 1)
    p = np.poly1d(z)
    plt.plot(usage_time, p(usage_time), "r--", color="#FF9900", linewidth=2)
    
    # Add annotations
    plt.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
    plt.text(80, 0.52, 'High Churn Risk', fontsize=10)
    plt.text(80, 0.48, 'Low Churn Risk', fontsize=10)
    
    # Save the figure to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Return the base64 encoded image
    return base64.b64encode(buf.read()).decode()

def create_smote_visualization():
    # Create a visualization explaining SMOTE
    from sklearn.datasets import make_blobs
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Generate imbalanced dataset
    X, y = make_blobs(n_samples=[100, 10], centers=[[0, 0], [2, 2]], random_state=42)
    
    # Create a figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Original imbalanced data
    ax1.scatter(X[y==0, 0], X[y==0, 1], label='Majority class', color='blue', alpha=0.7)
    ax1.scatter(X[y==1, 0], X[y==1, 1], label='Minority class', color='red', marker='x', s=100, alpha=0.7)
    ax1.set_title('Original Imbalanced Dataset')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # After SMOTE (simulated)
    ax2.scatter(X[y==0, 0], X[y==0, 1], label='Majority class', color='blue', alpha=0.7)
    ax2.scatter(X[y==1, 0], X[y==1, 1], label='Original minority', color='red', marker='x', s=100, alpha=0.7)
    
    # Generate synthetic samples (simplified simulation of SMOTE)
    from sklearn.neighbors import NearestNeighbors
    
    minority_samples = X[y==1]
    nn = NearestNeighbors(n_neighbors=3).fit(minority_samples)
    _, indices = nn.kneighbors(minority_samples)
    
    synthetic_samples = []
    for i in range(len(minority_samples)):
        for _ in range(4):  # Generate 4 synthetic samples for each minority sample
            nn_idx = random.choice(indices[i][1:])
            new_sample = minority_samples[i] + random.random() * (minority_samples[nn_idx] - minority_samples[i])
            synthetic_samples.append(new_sample)
    
    synthetic_samples = np.array(synthetic_samples)
    
    # Plot synthetic samples
    ax2.scatter(synthetic_samples[:, 0], synthetic_samples[:, 1], 
                label='Synthetic minority (SMOTE)', color='orange', alpha=0.7)
    ax2.set_title('After SMOTE: Balanced Dataset')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save the figure to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Return the base64 encoded image
    return base64.b64encode(buf.read()).decode()

# Main application
def main():
    initialize_session_state()
    
    # Initialize content area
    aws_header()
    
    # Sidebar with navigation and session management
    with st.sidebar:
        st.markdown(f"<h3 style='color: {aws_colors['secondary']}'>Exam Navigation</h3>", unsafe_allow_html=True)
        
        # Mode selection
        st.markdown("<div class='mode-selector'>", unsafe_allow_html=True)
        st.markdown("### Mode Selection")
        selected_mode = st.radio(
            "Choose exam mode:",
            ["Practice Mode", "Review Mode"],
            index=0 if st.session_state.mode == "Practice Mode" else 1,
            key="mode_selector"
        )
        
        # Apply mode change if needed
        if selected_mode != st.session_state.mode:
            set_mode(selected_mode)
        
        # Explain the difference between modes
        if selected_mode == "Practice Mode":
            st.markdown("In **Practice Mode**, you'll answer questions one by one and get immediate feedback.")
        else:
            st.markdown("In **Review Mode**, you can see all explanations for each question to study the material.")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Progress
        st.markdown("### Progress")
        progress_percentage = int((st.session_state.current_question + 1) / st.session_state.total_questions * 100) if not st.session_state.exam_completed else 100
        aws_progress_bar(progress_percentage, f"Question {st.session_state.current_question + 1} of {st.session_state.total_questions}")
        
        # Show current score in sidebar
        correct_count = sum(1 for is_correct in st.session_state.correct_answers.values() if is_correct)
        answered_count = len(st.session_state.answers)
        
        st.markdown(f"### Current Score")
        st.markdown(f"**Correct:** {correct_count}/{answered_count} answered questions")
        if answered_count > 0:
            score_percentage = int((correct_count / answered_count) * 100)
            aws_progress_bar(score_percentage, f"Score: {score_percentage}%")
        
        # Session management
        st.markdown("### Session Management")
        if st.button("Reset Progress"):
            reset_session()
            st.rerun()
            
        st.markdown("""---""")
        
        # Add information about the exam
        st.markdown("### About This Exam")
        st.markdown("""
        This simulator contains practice questions for the AWS Machine Learning Engineer Associate Certification.
        
        **Exam domains:**
        - Data Preparation for ML
        - ML Model Development
        - Deployment and Orchestration
        - Monitoring, Maintenance, and Security
        """)
        
        st.markdown("""---""")
        st.markdown("### Resources")
        st.markdown("[AWS Documentation](https://docs.aws.amazon.com/sagemaker/)")
        st.markdown("[AWS Certification](https://aws.amazon.com/certification/)")
    
    # Display exam completed page or question page
    if st.session_state.exam_completed:
        show_results_page()
    else:
        show_question_page()
        
def show_question_page():
    current_q = questions[st.session_state.current_question]
    
    with st.container():
        st.markdown(f"## Question {st.session_state.current_question + 1}")
        st.markdown(f"<div class='aws-card'>{current_q['question']}</div>", unsafe_allow_html=True)
        
        # Show appropriate question type input (radio for single, checkbox for multiple)
        if current_q["type"] == "single":
            # Get previously selected answer if it exists
            default_value = st.session_state.answers.get(st.session_state.current_question, None)
            
            selected_option = st.radio(
                "Select one answer:",
                current_q["options"],
                index=current_q["options"].index(default_value) if default_value in current_q["options"] else 0,
                key=f"q{st.session_state.current_question}",
                on_change=None
            )
            
            # Update answers when option is selected
            st.session_state.answers[st.session_state.current_question] = selected_option
            
        else:  # Multi-select question
            selected_options = st.multiselect(
                "Select all that apply:",
                current_q["options"],
                default=st.session_state.answers.get(st.session_state.current_question, []),
                key=f"q{st.session_state.current_question}"
            )
            
            # Update answers when options are selected
            st.session_state.answers[st.session_state.current_question] = selected_options
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.session_state.current_question > 0:
                if st.button("← Previous"):
                    prev_question()
                    st.rerun()
        
        with col2:
            # In Review Mode, always show the explanation
            # In Practice Mode, require submission
            if st.session_state.mode == "Practice Mode":
                if st.button("Submit Answer"):
                    submit_answer()
                    st.rerun()
            else:
                # In Review Mode, automatically show explanations
                st.session_state.submitted = True
        
        with col3:
            if st.session_state.current_question < st.session_state.total_questions - 1:
                if st.button("Next →"):
                    next_question()
                    st.rerun()
            else:
                if st.button("See Results"):
                    go_to_results()
                    st.rerun()
    
    # Display explanation after submission or always in Review Mode
    if st.session_state.submitted or st.session_state.mode == "Review Mode":
        selected_answer = st.session_state.answers.get(st.session_state.current_question, None)
        correct_answer = current_q["correct"]
        
        st.markdown("---")
        
        # For single-select questions
        if current_q["type"] == "single":
            if selected_answer == correct_answer and st.session_state.mode == "Practice Mode":
                st.markdown(f"""
                <div class="correct-answer">
                    <h3>✅ Correct!</h3>
                    <p><strong>You selected:</strong> {selected_answer}</p>
                    <p><strong>Explanation:</strong> {current_q["explanations"][selected_answer]}</p>
                </div>
                """, unsafe_allow_html=True)
            elif selected_answer and selected_answer != correct_answer and st.session_state.mode == "Practice Mode":
                st.markdown(f"""
                <div class="wrong-answer">
                    <h3>❌ Incorrect</h3>
                    <p><strong>You selected:</strong> {selected_answer}</p>
                    <p><strong>Explanation:</strong> {current_q["explanations"][selected_answer]}</p>
                </div>
                
                <div class="correct-answer">
                    <h3>The correct answer is: {correct_answer}</h3>
                    <p><strong>Explanation:</strong> {current_q["explanations"][correct_answer]}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Review Mode - show all explanations
                st.markdown(f"""
                <div class="correct-answer">
                    <h3>The correct answer is: {correct_answer}</h3>
                    <p><strong>Explanation:</strong> {current_q["explanations"][correct_answer]}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # If in review mode, show explanations for all options
                if st.session_state.mode == "Review Mode":
                    st.markdown("### All Answer Explanations:")
                    for option in current_q["options"]:
                        if option != correct_answer:
                            st.markdown(f"""
                            <div class="info-box">
                                <h4>{option}</h4>
                                <p>{current_q["explanations"][option]}</p>
                            </div>
                            """, unsafe_allow_html=True)
        
        # Additional info if available
        if "additional_info" in current_q:
            st.markdown(f"""
            <div class="info-box">
                <h3>Additional Information</h3>
                {current_q["additional_info"]}
            </div>
            """, unsafe_allow_html=True)
        
        # Display specific visualizations based on the question
        if st.session_state.current_question == 1:  # Scatter plot question
            st.markdown("### Example Scatter Plot Visualization")
            st.markdown("Below is an example of how a scatter plot can help visualize relationships between variables:")
            scatter_plot_img = create_scatter_plot()
            st.markdown(f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{scatter_plot_img}" style="max-width: 100%;">
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box">
                <p><strong>This scatter plot demonstrates:</strong></p>
                <ul>
                    <li>Negative correlation between usage time and churn probability</li>
                    <li>Clear visualization of relationship between variables</li>
                    <li>Easy identification of high-risk and low-risk customers</li>
                    <li>Trend line showing the overall pattern</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        elif st.session_state.current_question == 4:  # SMOTE question
            st.markdown("### Visualization of SMOTE Technique")
            smote_img = create_smote_visualization()
            st.markdown(f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{smote_img}" style="max-width: 100%;">
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box">
                <p><strong>How SMOTE works:</strong></p>
                <ol>
                    <li>For each minority class sample, identify its k nearest neighbors (from the same class)</li>
                    <li>Select one of these neighbors randomly</li>
                    <li>Create a synthetic point along the line between the original point and its neighbor</li>
                    <li>This creates synthetic examples that follow the distribution of the minority class</li>
                </ol>
                <p>This approach is more effective than simple oversampling because it creates new, synthetic points rather than just duplicating existing ones.</p>
            </div>
            """, unsafe_allow_html=True)

def show_results_page():
    st.markdown("## Exam Results")
    
    # Calculate final score
    correct_count = sum(1 for is_correct in st.session_state.correct_answers.values() if is_correct)
    percentage = (correct_count / st.session_state.total_questions) * 100
    
    # Different message based on score
    if percentage >= 80:
        result_message = "Congratulations! You're well prepared for the AWS ML Engineer Associate exam!"
        result_color = aws_colors["success"]
        result_icon = "🎉"
    elif percentage >= 60:
        result_message = "Good job! With some additional study, you'll be ready for the exam."
        result_color = aws_colors["secondary"]
        result_icon = "👍"
    else:
        result_message = "Keep studying! Review the areas where you had difficulty."
        result_color = aws_colors["error"]
        result_icon = "📚"
    
    # Display results card
    st.markdown(f"""
    <div class="aws-card" style="text-align: center;">
        <h1 style="font-size: 3rem;">{result_icon}</h1>
        <h2>Your Score: {correct_count}/{st.session_state.total_questions} ({percentage:.1f}%)</h2>
        <p style="color: {result_color}; font-weight: bold; font-size: 1.2rem;">{result_message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display results visualization
    col1, col2 = st.columns([2, 3])
    
    with col1:
        chart_img = create_pie_chart()
        st.markdown(f"""
        <div class="aws-card">
            <h3 style="text-align: center;">Performance Summary</h3>
            <div style="text-align: center;">
                <img src="data:image/png;base64,{chart_img}" style="max-width: 100%;">
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="aws-card">
            <h3>Recommended Next Steps</h3>
            <ol>
                <li>{"Review your incorrect answers and study those topics" if correct_count < st.session_state.total_questions else "You got everything correct! Great job!"}</li>
                <li>Complete the recommended AWS Skill Builder Training Path</li>
                <li>Try additional practice questions to reinforce your knowledge</li>
                <li>{"Schedule your certification exam when you're consistently scoring above 80%" if percentage < 80 else "You're ready to schedule your certification exam!"}</li>
            </ol>
            <h3>Key Resources</h3>
            <ul>
                <li><a href="https://aws.amazon.com/certification/certified-machine-learning-specialty/">AWS ML Engineer Certification Page</a></li>
                <li><a href="https://aws.amazon.com/sagemaker/">Amazon SageMaker Documentation</a></li>
                <li><a href="https://docs.aws.amazon.com/machine-learning">AWS Machine Learning Documentation</a></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Show which questions were answered correctly/incorrectly
    st.markdown("## Question Summary")
    
    summary_rows = []
    for i, q in enumerate(questions):
        is_correct = st.session_state.correct_answers.get(i, False)
        status = "✅ Correct" if is_correct else "❌ Incorrect"
        summary_rows.append([i+1, q['question'][:80] + "...", status])
    
    summary_df = pd.DataFrame(summary_rows, columns=["#", "Question", "Status"])
    
    # Style the dataframe
    def highlight_status(val):
        if val == "✅ Correct":
            return f"background-color: {aws_colors['success']}33; color: {aws_colors['success']}"
        elif val == "❌ Incorrect":
            return f"background-color: {aws_colors['error']}33; color: {aws_colors['error']}"
        return ""
    
    styled_summary = summary_df.style.applymap(highlight_status, subset=["Status"])
    st.dataframe(styled_summary, use_container_width=True)
    
    # Buttons for navigation
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Restart Exam"):
            reset_session()
            st.rerun()
    
    with col2:
        if st.button("Review Questions"):
            st.session_state.current_question = 0
            st.session_state.exam_completed = False
            st.session_state.mode = "Review Mode"
            st.rerun()

if __name__ == "__main__":
    main()
# ```

# ## What Changed in the Score Calculation

# Here's a step-by-step explanation of how I fixed the score calculation issues:

# 1. **Completely Rewrote the Score Tracking System**:
#    - Replaced the problematic score counting mechanism with a cleaner approach
#    - Created a dedicated dictionary `correct_answers` to track correct answers by question index

# 2. **Fixed the Score Calculation Logic**:
#    - Before: Was trying to use a single integer to track both score and correct count
#    - After: Using a dictionary to store a boolean value for each question index

# 3. **Improved the Submit Answer Function**:
#    - Now checks if the answer is correct for both single and multi-select questions
#    - Directly stores a boolean in the `correct_answers` dictionary for each question

# 4. **Added Current Score Display**:
#    - Added a current score display in the sidebar
#    - Shows correct answers out of attempted questions
#    - Added a progress bar showing current percentage score

# 5. **Enhanced Results Page**:
#    - Added a question summary table showing which questions were answered correctly/incorrectly
#    - Fixed the score calculation on the results page to use the correct count from the dictionary

# 6. **Fixed Visualization**:
#    - Updated the visualization functions to use the new score tracking method

# 7. **Improved Question Navigation**:
#    - Added default values for radio buttons and multi-select to preserve selections
#    - Ensured answers are properly stored and retrieved when navigating between questions

# 8. **Optimized Session State**:
#    - Simplified the session state variables for better clarity
#    - Removed redundant variables that were causing confusion

# 9. **Fixed the Mode Switching Logic**:
#    - Ensured proper state preservation when switching between modes
#    - Reset tracking for answers but preserve the mode selection

# These changes ensure that the score is calculated correctly throughout the exam, displayed consistently in the UI, and properly summarized on the results page.

# ## How to Run the Application

# 1. Make sure you have Python and the necessary libraries installed:
#    ```
#    pip install streamlit pandas matplotlib scikit-learn pillow
#    ```

# 2. Save the code to a file named `app.py`

# 3. Run the application:
#    ```
#    streamlit run app.py
#    ```

# The application now correctly calculates scores, tracks answered questions, and provides detailed feedback to the user throughout the exam experience.