
import streamlit as st
import random
from datetime import datetime
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="AWS AI Practitioner Quiz",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# AWS color scheme
AWS_ORANGE = "#FF9900"
AWS_BLUE = "#232F3E"
AWS_LIGHT_BLUE = "#1A73E8"
AWS_LIGHT_GRAY = "#F5F5F5"
AWS_GRAY = "#666666"
AWS_WHITE = "#FFFFFF"
AWS_GREEN = "#008000"
AWS_RED = "#D13212"

# Initialize session state variables
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'quiz_complete' not in st.session_state:
    st.session_state.quiz_complete = False
if 'questions_selected' not in st.session_state:
    st.session_state.questions_selected = False
if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = []
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 10
if 'time_started' not in st.session_state:
    st.session_state.time_started = datetime.now()
if 'auto_advance' not in st.session_state:
    st.session_state.auto_advance = True

# AWS AI Practitioner quiz questions database
all_questions = [
    # AWS AI Services
    {
        "id": 1,
        "question": "A company needs to automatically extract text, key-value pairs, and tables from scanned documents and forms. Which AWS service would be most appropriate?",
        "options": {
            "A": "Amazon Rekognition",
            "B": "Amazon Textract",
            "C": "Amazon Comprehend",
            "D": "Amazon Kendra"
        },
        "correct_answer": "B",
        "explanation": {
            "A": "Amazon Rekognition is used for image and video analysis, including object and scene detection, facial recognition, and content moderation. It doesn't specialize in document text extraction.",
            "B": "Correct! Amazon Textract is specifically designed to extract text, forms, and tables from scanned documents. It goes beyond simple OCR to understand the structure of documents and extract structured data.",
            "C": "Amazon Comprehend is a natural language processing (NLP) service used to extract insights and relationships from text, but it doesn't specialize in extracting structured data from scanned documents.",
            "D": "Amazon Kendra is an enterprise search service powered by machine learning, used for querying natural language questions across documents, not for extracting text from documents."
        },
        "category": "AWS AI Services"
    },
    {
        "id": 2,
        "question": "A retail company wants to provide personalized product recommendations to customers based on their browsing and purchase history. Which AWS AI service is best suited for this requirement?",
        "options": {
            "A": "Amazon Fraud Detector",
            "B": "Amazon Kendra",
            "C": "Amazon Personalize",
            "D": "Amazon Comprehend"
        },
        "correct_answer": "C",
        "explanation": {
            "A": "Amazon Fraud Detector is used for detecting online fraud, not for generating personalized recommendations.",
            "B": "Amazon Kendra is an enterprise search service, not a recommendation system.",
            "C": "Correct! Amazon Personalize is designed to create real-time, personalized user experiences and recommendations at scale, perfect for retail recommendation systems. It uses the same technology that powers Amazon.com's product recommendations.",
            "D": "Amazon Comprehend is a natural language processing service that extracts insights from text, but doesn't generate personalized recommendations."
        },
        "category": "AWS AI Services"
    },
    {
        "id": 3,
        "question": "A media company needs to automatically analyze and moderate user-generated image content to ensure it doesn't contain inappropriate material. Which AWS service would be best for this use case?",
        "options": {
            "A": "Amazon Rekognition",
            "B": "Amazon Textract",
            "C": "Amazon Comprehend",
            "D": "Amazon Kendra"
        },
        "correct_answer": "A",
        "explanation": {
            "A": "Correct! Amazon Rekognition provides content moderation capabilities that can detect inappropriate, unwanted, or offensive content in images and videos. It's ideal for moderating user-generated content.",
            "B": "Amazon Textract is used for extracting text and data from scanned documents, not for image content moderation.",
            "C": "Amazon Comprehend analyzes text for insights and relationships, not images.",
            "D": "Amazon Kendra is an enterprise search service, not designed for image content moderation."
        },
        "category": "AWS AI Services"
    },
    
    # Machine Learning Types
    {
        "id": 4,
        "question": "In which machine learning type does the model receive labeled training data and learns to predict the output based on this data?",
        "options": {
            "A": "Supervised Learning",
            "B": "Unsupervised Learning",
            "C": "Reinforcement Learning",
            "D": "Self-Supervised Learning"
        },
        "correct_answer": "A",
        "explanation": {
            "A": "Correct! In supervised learning, the model is trained on labeled data where the correct outputs are known. The algorithm learns by comparing its predicted output with the correct output, making it ideal for classification and regression tasks.",
            "B": "Unsupervised learning involves training models on data without labeled responses, typically to find patterns or groupings within the data.",
            "C": "Reinforcement learning involves training models to make sequences of decisions by rewarding desired behaviors and punishing undesired ones.",
            "D": "Self-supervised learning is where the model generates its own supervisory signal from the input data, often by masking parts of the input and trying to predict them."
        },
        "category": "Machine Learning Types"
    },
    {
        "id": 5,
        "question": "Which machine learning type is typically used to train foundation models for generative AI, where the model learns by predicting missing parts of the input data?",
        "options": {
            "A": "Supervised Learning",
            "B": "Unsupervised Learning",
            "C": "Reinforcement Learning",
            "D": "Self-Supervised Learning"
        },
        "correct_answer": "D",
        "explanation": {
            "A": "Supervised learning requires explicitly labeled data, which would be impractical for the massive datasets used to train foundation models.",
            "B": "While unsupervised learning doesn't require labels, it typically focuses on finding patterns or clusters in data rather than generating predictions based on context.",
            "C": "Reinforcement learning involves learning through interactions with an environment and reward signals, which is not how foundation models are primarily trained.",
            "D": "Correct! Self-supervised learning is used to train foundation models by creating pseudo-labels from the data itself. For example, by masking words in a sentence and training the model to predict the missing words based on context, the model learns rich representations of language."
        },
        "category": "Machine Learning Types"
    },
    {
        "id": 6,
        "question": "A data scientist is working on a project to group similar customer profiles without any predefined categories. Which type of machine learning approach is most suitable?",
        "options": {
            "A": "Supervised Learning",
            "B": "Unsupervised Learning",
            "C": "Reinforcement Learning",
            "D": "Transfer Learning"
        },
        "correct_answer": "B",
        "explanation": {
            "A": "Supervised learning requires labeled data with known outcomes, which isn't available in this scenario since there are no predefined categories.",
            "B": "Correct! Unsupervised learning is ideal for discovering patterns or groupings in data without labeled responses. Clustering algorithms like K-means would help group similar customer profiles.",
            "C": "Reinforcement learning is used for sequential decision-making problems, not for static grouping tasks.",
            "D": "Transfer learning involves applying knowledge from one task to another task, but doesn't specifically address the grouping requirement."
        },
        "category": "Machine Learning Types"
    },
    
    # Use Cases for AI/ML
    {
        "id": 7,
        "question": "A financial company needs to implement a system for detecting fraudulent transactions. Which approach would be most appropriate?",
        "options": {
            "A": "Generative AI using large language models",
            "B": "Traditional machine learning with explainable models",
            "C": "Self-supervised learning with unlabeled transaction data",
            "D": "Reinforcement learning that optimizes for fraud detection"
        },
        "correct_answer": "B",
        "explanation": {
            "A": "While generative AI could potentially help with fraud detection, it lacks the transparency and explainability required in financial services applications.",
            "B": "Correct! Traditional machine learning models are preferred for fraud detection because of their interpretability and transparency, which are crucial for regulatory compliance and explaining decisions in financial institutions.",
            "C": "Self-supervised learning typically doesn't provide the explainability needed for fraud detection in a regulated environment.",
            "D": "While reinforcement learning could be used for fraud detection, it's typically less interpretable than traditional ML models and might not satisfy regulatory requirements."
        },
        "category": "AI/ML Use Cases"
    },
    {
        "id": 8,
        "question": "A healthcare provider wants to use AI to assist with medical diagnoses from patient records and lab results. Which approach is most suitable given the need for accuracy and interpretability?",
        "options": {
            "A": "Generative AI with large language models",
            "B": "Unsupervised learning for patient clustering",
            "C": "Traditional machine learning on structured data",
            "D": "Reinforcement learning that maximizes positive outcomes"
        },
        "correct_answer": "C",
        "explanation": {
            "A": "While generative AI can process medical information, it lacks the transparency and deterministic behavior needed for critical healthcare diagnoses.",
            "B": "Clustering patients could provide insights but isn't directly applicable to making specific medical diagnoses.",
            "C": "Correct! Traditional machine learning on structured data (patient records, lab results, imaging data) provides reliable diagnoses with an auditable decision process, which is critical in healthcare applications where interpretability and accuracy are paramount.",
            "D": "Reinforcement learning is typically used for sequential decision-making problems rather than diagnostic classification from medical records."
        },
        "category": "AI/ML Use Cases"
    },
    
    # AI/ML Solution Architecture
    {
        "id": 9,
        "question": "A company wants to develop a machine learning pipeline on AWS to automate the process of training and deploying models. The pipeline should include data preprocessing, model training, and model deployment. Which AWS service would be most appropriate for orchestrating this ML pipeline?",
        "options": {
            "A": "Amazon Rekognition",
            "B": "Amazon Personalize",
            "C": "Amazon SageMaker",
            "D": "Amazon Bedrock"
        },
        "correct_answer": "C",
        "explanation": {
            "A": "Amazon Rekognition is specifically designed for image and video analysis, not for building and orchestrating ML pipelines.",
            "B": "Amazon Personalize is a service for building recommendation systems, not a general-purpose ML pipeline orchestration tool.",
            "C": "Correct! Amazon SageMaker provides a complete set of tools for building, training, and deploying ML models, including pipeline orchestration capabilities for automating the ML workflow from data preparation to deployment.",
            "D": "Amazon Bedrock is a service for accessing foundation models, not for building complete ML pipelines."
        },
        "category": "AI/ML Solution Architecture"
    },
    {
        "id": 10,
        "question": "A data science team needs to collect, clean, prepare, and analyze data before training their ML model. According to the ML development lifecycle, which phase should they focus on first?",
        "options": {
            "A": "Feature Engineering",
            "B": "Data Collection, Integration, and Preparation",
            "C": "Model Training and Parameter Tuning",
            "D": "Model Deployment"
        },
        "correct_answer": "B",
        "explanation": {
            "A": "Feature Engineering comes after data has been collected, integrated, and prepared.",
            "B": "Correct! The ML development lifecycle begins with the Data Collection, Integration, and Preparation phase after the business problem has been framed as an ML problem. This is fundamental to ensuring quality input data for the model.",
            "C": "Model Training and Parameter Tuning occurs after data has been collected, prepared, and analyzed, and features have been engineered.",
            "D": "Model Deployment is one of the final steps in the ML development lifecycle, after the model has been trained and evaluated."
        },
        "category": "AI/ML Solution Architecture"
    },
    {
        "id": 11,
        "question": "A company needs to deploy a trained machine learning model for real-time inference with consistent low latency. Which Amazon SageMaker deployment option is most appropriate?",
        "options": {
            "A": "SageMaker Batch Transform",
            "B": "SageMaker Real-Time Inference",
            "C": "SageMaker Serverless Inference",
            "D": "SageMaker Asynchronous Inference"
        },
        "correct_answer": "B",
        "explanation": {
            "A": "SageMaker Batch Transform is designed for offline inference on batches of data, not for real-time predictions.",
            "B": "Correct! SageMaker Real-Time Inference is designed for workloads with stable traffic patterns that require consistent low latency. It provides a persistent endpoint that processes requests synchronously.",
            "C": "SageMaker Serverless Inference is good for intermittent traffic but may have cold start latency which could impact consistent low-latency requirements.",
            "D": "SageMaker Asynchronous Inference is designed for large payload sizes or long processing times, not for low-latency real-time inference."
        },
        "category": "AI/ML Solution Architecture"
    },
    
    # ML vs Traditional Programming
    {
        "id": 12,
        "question": "When should a company choose machine learning over traditional programming?",
        "options": {
            "A": "When the problem requires simple rule-based decision making",
            "B": "When the business rules are well-defined and won't change over time",
            "C": "When the company needs to recognize speech or images",
            "D": "When the solution requires transparent and predictable behavior above all else"
        },
        "correct_answer": "C",
        "explanation": {
            "A": "Simple rule-based decision making is typically better handled by traditional programming approaches.",
            "B": "Well-defined, stable business rules are ideal scenarios for traditional programming.",
            "C": "Correct! Machine learning should be used when you can't easily code the rules, such as for recognizing speech or images where patterns are complex and difficult to express programmatically. ML excels at finding patterns in complex, high-dimensional data.",
            "D": "When transparent and predictable behavior is the top priority, traditional programming is often preferred over machine learning."
        },
        "category": "ML vs Traditional Programming"
    },
    {
        "id": 13,
        "question": "Which scenario is better suited for traditional programming rather than machine learning?",
        "options": {
            "A": "Predicting customer churn based on historical behavior patterns",
            "B": "Implementing a tax calculation system with fixed rules and rates",
            "C": "Detecting unusual patterns in network traffic",
            "D": "Personalizing content recommendations for website visitors"
        },
        "correct_answer": "B",
        "explanation": {
            "A": "Predicting customer churn involves finding patterns in complex historical data, which is well-suited for machine learning.",
            "B": "Correct! Tax calculations typically follow fixed, well-defined rules that can be explicitly coded. Traditional programming is more appropriate when the rules are clear and deterministic, as in this case.",
            "C": "Detecting unusual patterns (anomalies) in network traffic is a task well-suited for machine learning, as the patterns may be complex and evolving.",
            "D": "Content personalization based on user behavior is a classic use case for machine learning, as it involves finding patterns in user preferences and behaviors."
        },
        "category": "ML vs Traditional Programming"
    },
    {
        "id": 14,
        "question": "A company wants to identify which business scenarios are appropriate for traditional programming versus machine learning. Which of the following statements is accurate?",
        "options": {
            "A": "Machine learning should be used for all data-driven problems because it always produces better results than traditional programming",
            "B": "Traditional programming should be used when you need to adapt and personalize based on individual data",
            "C": "Machine learning should be used when you can't scale a solution with traditional programming",
            "D": "Traditional programming is always more cost-effective than machine learning"
        },
        "correct_answer": "C",
        "explanation": {
            "A": "Machine learning isn't always the right approach for every data-driven problem. Traditional programming might be more appropriate for problems with clear rules.",
            "B": "Adaptation and personalization based on individual data is actually a strength of machine learning, not traditional programming.",
            "C": "Correct! Machine learning should be used when you can't scale a solution with traditional programming, such as when you need human-like expertise for high-volume tasks like recommendations, spam detection, or fraud detection.",
            "D": "The cost-effectiveness depends on the specific problem. ML may require more upfront investment but can be more cost-effective for complex problems at scale."
        },
        "category": "ML vs Traditional Programming"
    }
]

# Define CSS for better styling with AWS color scheme
st.markdown(f"""
<style>
    .main-header {{
        font-size: 2.5rem;
        color: {AWS_ORANGE};
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }}
    .sub-header {{
        font-size: 1.5rem;
        color: {AWS_BLUE};
        margin-bottom: 1rem;
    }}
    .question-card {{
        background-color: {AWS_WHITE};
        padding: 25px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 5px solid {AWS_ORANGE};
    }}
    .option-button {{
        width: 100%;
        text-align: left;
        margin: 8px 0;
        padding: 12px 15px;
        border-radius: 5px;
        border: 1px solid #ddd;
        background-color: {AWS_WHITE};
        transition: all 0.3s ease;
    }}
    .option-button:hover {{
        background-color: #f5f5f5;
        border-color: {AWS_ORANGE};
    }}
    .selected-option {{
        background-color: #e6f7ff;
        border-color: {AWS_LIGHT_BLUE};
    }}
    .correct-option {{
        background-color: #d4edda;
        border-color: {AWS_GREEN};
    }}
    .incorrect-option {{
        background-color: #f8d7da;
        border-color: {AWS_RED};
    }}
    .category-tag {{
        background-color: {AWS_BLUE};
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 15px;
    }}
    .explanation-box {{
        padding: 18px;
        border-radius: 5px;
        background-color: #f0f8ff;
        margin-top: 20px;
        border-left: 4px solid {AWS_LIGHT_BLUE};
    }}
    .stats-box {{
        background-color: {AWS_LIGHT_GRAY};
        border-radius: 8px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    .aws-button {{
        background-color: {AWS_ORANGE};
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 18px;
        margin: 8px 5px;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    .aws-button:hover {{
        background-color: #ec7211;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }}
    .aws-secondary-button {{
        background-color: {AWS_BLUE};
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 18px;
        margin: 8px 5px;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    .aws-secondary-button:hover {{
        background-color: #1a2530;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }}
    .progress-container {{
        margin: 20px 0;
        padding: 15px;
        background-color: {AWS_WHITE};
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    .progress-label {{
        font-weight: 600;
        color: {AWS_BLUE};
        margin-bottom: 8px;
    }}
    .stProgress > div > div > div > div {{
        background-color: {AWS_ORANGE};
    }}
    .footer {{
        text-align: center;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #eee;
        color: {AWS_GRAY};
        font-size: 0.8rem;
    }}
    .sidebar .sidebar-content {{
        background-color: {AWS_LIGHT_GRAY};
    }}
    /* Responsive styling */
    @media (max-width: 768px) {{
        .main-header {{
            font-size: 2rem;
        }}
        .sub-header {{
            font-size: 1.2rem;
        }}
        .question-card {{
            padding: 15px;
        }}
        .option-button {{
            padding: 10px;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# Navigation and state management functions
def select_random_questions(num_questions=10):
    # Check if we need to select questions
    if not st.session_state.questions_selected:
        # Reset time when new questions are selected
        st.session_state.time_started = datetime.now()
        
        # Make a copy of all questions to avoid modifying the original
        available_questions = all_questions.copy()
        random.shuffle(available_questions)
        
        # Ensure we have at least one question from each category
        selected_questions = []
        categories = set(q["category"] for q in available_questions)
        
        for category in categories:
            category_questions = [q for q in available_questions if q["category"] == category]
            if category_questions:
                selected = random.choice(category_questions)
                selected_questions.append(selected)
                available_questions.remove(selected)
        
        # Fill the rest randomly
        remaining_needed = num_questions - len(selected_questions)
        if remaining_needed > 0:
            random.shuffle(available_questions)
            selected_questions.extend(available_questions[:remaining_needed])
        
        # Update IDs to be sequential
        for i, question in enumerate(selected_questions):
            question["id"] = i + 1
        
        # Update session state
        st.session_state.selected_questions = selected_questions
        st.session_state.questions_selected = True
        st.session_state.total_questions = len(selected_questions)
        st.session_state.score = 0  # Reset score when new questions are selected
        st.session_state.answers = {}  # Reset answers

def go_to_next_question():
    if st.session_state.current_question_index < len(st.session_state.selected_questions) - 1:
        st.session_state.current_question_index += 1
    else:
        st.session_state.quiz_complete = True

def go_to_previous_question():
    if st.session_state.current_question_index > 0:
        st.session_state.current_question_index -= 1

def reset_quiz():
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.answers = {}
    st.session_state.quiz_complete = False
    st.session_state.questions_selected = False
    st.session_state.selected_questions = []
    st.session_state.time_started = datetime.now()

def answer_selected(option_key, question_id):
    q_id = str(question_id)
    question = next((q for q in st.session_state.selected_questions if str(q["id"]) == q_id), None)
    
    # Check if this question has already been answered
    already_answered = q_id in st.session_state.answers
    
    # Record the answer
    st.session_state.answers[q_id] = option_key
    
    # Update score if correct and not already answered
    if not already_answered and option_key == question["correct_answer"]:
        st.session_state.score += 1
    
    # Auto-advance to next question if enabled
    if st.session_state.auto_advance:
        # Wait 1 second to show the answer before advancing
        # (We can't actually delay in Streamlit, but the rerun will create a small pause)
        if st.session_state.current_question_index < len(st.session_state.selected_questions) - 1:
            st.session_state.current_question_index += 1

# Calculate score based on answered questions
def calculate_score():
    correct_count = 0
    for q_id, user_answer in st.session_state.answers.items():
        question = next((q for q in st.session_state.selected_questions if str(q["id"]) == q_id), None)
        if question and user_answer == question["correct_answer"]:
            correct_count += 1
    return correct_count

# Select random questions if not already done
select_random_questions(st.session_state.total_questions)

# Main application
def main():
    # Sidebar
    with st.sidebar:
        st.image("images/AWS-Certified-AI-Practitioner_badge.png", width=100)
        st.markdown("## Session Management")
        
        # Quiz settings
        st.markdown("### Quiz Settings")
        # Number of questions selector
        num_questions = st.slider("Number of Questions", min_value=5, max_value=14, value=st.session_state.total_questions, step=1)
        if num_questions != st.session_state.total_questions:
            st.session_state.total_questions = num_questions
            st.session_state.questions_selected = False  # Force reselection of questions
            select_random_questions(num_questions)
            st.rerun()
        
        # Auto-advance toggle
        auto_advance = st.checkbox("Auto-advance to next question", value=st.session_state.auto_advance)
        if auto_advance != st.session_state.auto_advance:
            st.session_state.auto_advance = auto_advance
        
        # Quiz controls
        st.markdown("### Quiz Controls")
        if st.button("Reset Quiz", key="reset_quiz"):
            reset_quiz()
            select_random_questions(st.session_state.total_questions)
            st.rerun()
            
        if not st.session_state.quiz_complete and len(st.session_state.answers) > 0:
            if st.button("Skip to Results", key="skip_results"):
                st.session_state.quiz_complete = True
                st.rerun()
        
        # Navigation
        if not st.session_state.quiz_complete:
            st.markdown("### Navigation")
            question_nav = st.selectbox(
                "Jump to Question",
                [f"Question {i+1}" for i in range(len(st.session_state.selected_questions))],
                index=st.session_state.current_question_index
            )
            if st.button("Go", key="go_btn"):
                q_idx = int(question_nav.split()[1]) - 1
                st.session_state.current_question_index = q_idx
                st.rerun()
        
        # Quiz progress
        st.markdown("### Quiz Progress")
        total_questions = len(st.session_state.selected_questions)
        answered_questions = len(st.session_state.answers)
        progress_percentage = (answered_questions / total_questions) if total_questions > 0 else 0
        
        st.progress(progress_percentage)
        st.write(f"Completed: {answered_questions}/{total_questions} questions ({progress_percentage*100:.0f}%)")
        
        # Recalculate score from answers
        correct_answers = calculate_score()
        st.session_state.score = correct_answers  # Update the session state score
        
        # Score
        accuracy = (correct_answers / answered_questions) * 100 if answered_questions > 0 else 0
        st.write(f"Score: {correct_answers}/{answered_questions} correct ({accuracy:.1f}%)")
        
        # Time elapsed
        time_elapsed = datetime.now() - st.session_state.time_started
        minutes = time_elapsed.seconds // 60
        seconds = time_elapsed.seconds % 60
        st.write(f"Time: {minutes}m {seconds}s")
    
    # Header with AWS logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 class='main-header'>AWS AI Practitioner Quiz</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center'>Domain 1: Fundamentals of AI and ML</p>", unsafe_allow_html=True)
    
    # If quiz is complete, show results
    if st.session_state.quiz_complete:
        display_results()
    else:
        # Display current question
        display_question(st.session_state.current_question_index)
    
    # Footer
    st.markdown("<div class='footer'>© 2025 AWS AI Practitioner Quiz. Created for learning purposes.</div>", unsafe_allow_html=True)

# Display a question
def display_question(q_index):
    question = st.session_state.selected_questions[q_index]
    q_id = str(question["id"])
    
    st.markdown(f"<div class='question-card'>", unsafe_allow_html=True)
    
    # Display category tag
    category = question.get("category", "General")
    st.markdown(f"<span class='category-tag'>{category}</span>", unsafe_allow_html=True)
    
    # Display question
    st.markdown(f"<h2 class='sub-header'>Question {q_index + 1} of {len(st.session_state.selected_questions)}</h2>", unsafe_allow_html=True)
    st.write(question["question"])
    
    # Check if user has already answered
    user_answered = q_id in st.session_state.answers
    
    if not user_answered:
        for option_key, option_text in question["options"].items():
            # Use a consistent key without random numbers
            button_key = f"option_{q_id}_{option_key}"
            
            # Add a container for better button handling
            button_container = st.container()
            with button_container:
                if st.button(f"{option_key}: {option_text}", key=button_key):
                    # Call the answer_selected function
                    answer_selected(option_key, q_id)
                    # Force rerun to update the UI
                    st.rerun()

   
    else:
        user_answer = st.session_state.answers[q_id]
        for option_key, option_text in question["options"].items():
            is_correct = option_key == question["correct_answer"]
            user_selected = option_key == user_answer
            
            if user_selected and is_correct:
                st.success(f"{option_key}: {option_text} ✓")
            elif user_selected and not is_correct:
                st.error(f"{option_key}: {option_text} ✗")
            elif not user_selected and is_correct:
                st.warning(f"{option_key}: {option_text} (Correct Answer)")
            else:
                st.write(f"{option_key}: {option_text}")
        
        # Show explanation
        st.markdown("<div class='explanation-box'>", unsafe_allow_html=True)
        st.markdown("### Explanation")
        st.markdown(question["explanation"][user_answer])
        
        if user_answer != question["correct_answer"]:
            st.markdown("### Correct Answer")
            st.markdown(question["explanation"][question["correct_answer"]])
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.current_question_index > 0:
            if st.button("⬅️ Previous", key="prev_btn", help="Go to previous question"):
                go_to_previous_question()
                st.rerun()
    
    with col3:
        if st.session_state.current_question_index < len(st.session_state.selected_questions) - 1:
            next_text = "Next ➡️"
            if user_answered:
                if st.button(next_text, key="next_btn", help="Go to next question"):
                    go_to_next_question()
                    st.rerun()
            else:
                st.info("Please select an answer to continue")
        else:
            if user_answered:
                if st.button("Finish Quiz 🏁", key="finish_btn"):
                    st.session_state.quiz_complete = True
                    st.rerun()
            else:
                st.info("Please select an answer to complete the quiz")

# Display quiz results
def display_results():
    st.markdown("<div class='question-card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Quiz Results</h2>", unsafe_allow_html=True)
    
    # Calculate score directly from answers
    total_questions = len(st.session_state.selected_questions)
    answered_questions = len(st.session_state.answers)
    
    # Recalculate correct answers to ensure accuracy
    correct_answers = calculate_score()
    
    # Calculate percentage based on answered questions
    accuracy = (correct_answers / answered_questions) * 100 if answered_questions > 0 else 0
    
    # Calculate percentage based on total questions
    completion_percentage = (answered_questions / total_questions) * 100 if total_questions > 0 else 0
    
    # Time taken
    time_elapsed = datetime.now() - st.session_state.time_started
    minutes = time_elapsed.seconds // 60
    seconds = time_elapsed.seconds % 60
    
    # Display score
    st.markdown(f"<div class='stats-box'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### Your Score: {correct_answers}/{answered_questions}")
        st.markdown(f"### Accuracy: {accuracy:.1f}%")
    
    with col2:
        st.markdown(f"### Time Taken: {minutes}m {seconds}s")
        st.markdown(f"### Questions Answered: {answered_questions}/{total_questions} ({completion_percentage:.1f}%)")
    
    # Performance assessment
    if accuracy >= 80:
        st.success("Excellent! You have a strong understanding of AWS AI Practitioner concepts.")
    elif accuracy >= 60:
        st.info("Good job! You have a reasonable understanding, but some areas need improvement.")
    else:
        st.warning("You might need more study on AWS AI Practitioner concepts.")

        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Category breakdown
    st.markdown("### Performance by Category")
    
    # Group answers by category
    category_performance = {}
    for question in st.session_state.selected_questions:
        q_id = str(question["id"])
        category = question.get("category", "General")
        
        if category not in category_performance:
            category_performance[category] = {"correct": 0, "total": 0, "answered": 0}
        
        if q_id in st.session_state.answers:
            category_performance[category]["answered"] += 1
            if st.session_state.answers[q_id] == question["correct_answer"]:
                category_performance[category]["correct"] += 1
        
        category_performance[category]["total"] += 1
    
    # Create DataFrame for category performance
    if category_performance:
        data = []
        for category, stats in category_performance.items():
            accuracy = (stats["correct"] / stats["answered"]) * 100 if stats["answered"] > 0 else 0
            data.append({
                "Category": category,
                "Questions": stats["total"],
                "Answered": stats["answered"],
                "Correct": stats["correct"],
                "Accuracy": f"{accuracy:.1f}%"
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    
    # Question breakdown
    st.markdown("### Question Breakdown")
    
    for question in st.session_state.selected_questions:
        q_id = str(question["id"])
        user_answer = st.session_state.answers.get(q_id, "Not answered")
        is_correct = user_answer == question["correct_answer"] if q_id in st.session_state.answers else False
        
        with st.expander(f"Question {question['id']}: {question['question'][:100]}..."):
            st.write(question["question"])
            st.write(f"**Your answer:** Option {user_answer}")
            st.write(f"**Correct answer:** Option {question['correct_answer']}")
            st.write(f"**Result:** {'✓ Correct' if is_correct else '✗ Incorrect' if user_answer != 'Not answered' else '⚠️ Not Answered'}")
            
            # Show explanation
            st.markdown("### Explanation")
            if q_id in st.session_state.answers:
                st.markdown(question["explanation"][user_answer])
                
                if user_answer != question["correct_answer"]:
                    st.markdown("### Correct Answer")
                    st.markdown(question["explanation"][question["correct_answer"]])
            else:
                st.markdown(question["explanation"][question["correct_answer"]])
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Review Questions", key="review_btn", help="Review your answers"):
            st.session_state.quiz_complete = False
            st.session_state.current_question_index = 0
            st.rerun()
    
    with col2:
        if st.button("New Quiz", key="new_quiz_btn", help="Start a new quiz with different questions"):
            reset_quiz()
            select_random_questions(st.session_state.total_questions)
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
