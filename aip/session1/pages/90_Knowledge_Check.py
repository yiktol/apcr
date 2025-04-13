
import streamlit as st
import pandas as pd
import numpy as np
import random
from PIL import Image
import io
import base64
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(
    page_title="AWS AI Practitioner Knowledge Check",
    page_icon="🧠",
    layout="wide"
)

# AWS Color Scheme
AWS_COLORS = {
    "primary": "#232F3E",  # AWS Navy Blue
    "secondary": "#FF9900",  # AWS Orange
    "accent1": "#1A476F",  # Lighter Blue
    "accent2": "#D9381E",  # Red
    "background": "#F8F8F8",  # Light Gray Background
    "text": "#16191F",  # Dark Gray Text
    "success": "#008000",  # Green for correct answers
    "error": "#D9381E",  # Red for incorrect answers
}

# CSS styling
def local_css():
    st.markdown(f"""
    <style>
        .reportview-container .main .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}
        .stButton button {{
            background-color: {AWS_COLORS["secondary"]};
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            width: 100%;
        }}
        .stButton button:hover {{
            background-color: {AWS_COLORS["accent1"]};
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {AWS_COLORS["primary"]};
        }}
        .exam-header {{
            background-color: {AWS_COLORS["primary"]};
            color: white !important;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 2rem;
            text-align: center;
        }}
        .question-container {{
            background-color: white;
            padding: 1.5rem;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }}
        .explanation-container {{
            background-color: #f1f8ff;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid {AWS_COLORS["secondary"]};
            margin-top: 1rem;
        }}
        .correct {{
            background-color: rgba(0, 128, 0, 0.1);
            border-left: 4px solid green;
        }}
        .incorrect {{
            background-color: rgba(255, 0, 0, 0.1);
            border-left: 4px solid red;
        }}
        .navigation-buttons {{
            display: flex;
            gap: 1rem;
            margin-top: 2rem;
        }}
        .progress-container {{
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}
        .aws-logo {{
            display: flex;
            justify-content: center;
            margin-bottom: 1rem;
        }}
        .stProgress > div > div > div > div {{
            background-color: {AWS_COLORS["secondary"]};
        }}
        .chip {{
            background-color: {AWS_COLORS["secondary"]};
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 16px;
            display: inline-block;
            margin-right: 0.5rem;
            font-size: 0.85rem;
        }}
        .sidebar-header {{
            color: {AWS_COLORS["secondary"]};
            text-align: center;
            margin-bottom: 1rem;
        }}
        .summary-card {{
            background-color: white;
            border-radius: 5px;
            padding: 1.5rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }}
        .gauge-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }}
        .recommendation-card {{
            background-color: {AWS_COLORS["primary"]};
            color: white;
            border-radius: 5px;
            padding: 1.5rem;
            margin-top: 1rem;
        }}
    </style>
    """, unsafe_allow_html=True)

local_css()

#AWS Logo
@st.cache_data
def aws_logo():
    return "images/aws_logo.png"

# Initialize session state variables
def init_session_state():
    session_vars = {
        "current_question": 0,
        "answers": {},
        "submitted": False,
        "exam_completed": False,
        "score": 0,
        "total_questions": 0,
        "correct_answers": 0,
        "incorrect_answers": 0,
        "skipped_questions": 0,
        "question_times": {},
        "start_time": None,
        "end_time": None,
        "results_by_domain": {},
        "results_by_difficulty": {}
    }
    for var, value in session_vars.items():
        if var not in st.session_state:
            st.session_state[var] = value

# Questions data
def create_questions():
    return [
        {
            "id": 1,
            "question": "A company wants to develop a machine learning model to analyze customer feedback on their products. They have a dataset of 10,000 customer reviews, with each review labeled as either \"positive\" or \"negative\". The company will train the machine learning model to predict whether new customer reviews are \"positive\" or \"negative\".\n\nWhich of the following machine learning types does this describe?",
            "options": [
                "Supervised Learning",
                "Unsupervised Learning",
                "Self-Supervised Learning",
                "Reinforcement Learning"
            ],
            "answer": 0,  # Index of correct option (zero-based)
            "explanation": "This is a supervised learning problem where you have to choose between two labels. The dataset provided is labelled positive and negative so this is a binary classification problem.",
            "incorrect_explanations": [
                "",  # For correct answer
                "This is not a clustering/grouping problem.",
                "Self-Supervised is when you hide part of the dataset and have the model try to predict the missing value.",
                "Reinforcement Learning is where you have an agent maximizing the reward."
            ],
            "type": "single",
            "domain": "Machine Learning Fundamentals",
            "difficulty": "Easy"
        },
        {
            "id": 2,
            "question": "An e-commerce company needs to integrate tailored recommendations to customers based on their browsing and purchase history. The company needs to quickly implement this solution but their team has limited machine learning expertise.\n\nWhich of the following solutions would meet the requirements in the most operationally efficient way?",
            "options": [
                "Set up an EC2 cluster and train the model on the cluster. Use Amazon S3 to store your training data and model artifacts, and deploy the model on an EC2 instance behind an Elastic Load Balancer.",
                "Add the data to Amazon Personalize and then access real time recommendations via the personalization API.",
                "Use Amazon SageMaker AI to create a machine learning pipeline that includes data preparation, model training, and model deployment steps.",
                "Use Amazon Bedrock to generate personalized recommendations that would be shown to customers on the website."
            ],
            "answer": 1,
            "explanation": "Amazon Personalize accelerates your digital transformation with ML, making it easier to integrate personalized recommendations into existing websites, applications, email marketing systems, and more. It allows you to quickly implement a customized personalization engine in days—not months—with no ML expertise required.",
            "incorrect_explanations": [
                "This would be a self managed system that would require undifferentiated heavy lifting as well as ML expertise.",
                "", # For correct answer
                "While SageMaker could work, it would require more effort than using Amazon Personalize and the company has limited ML expertise.",
                "Bedrock is for running Foundation Models. While it could generate personalized text, it cannot recommend products. It could be part of a larger system – for example, using another ML model to identify products to recommend and then sending the information to Amazon Bedrock to craft a personal recommendation."
            ],
            "type": "single",
            "domain": "AI Services",
            "difficulty": "Medium"
        },
        {
            "id": 3,
            "question": "A machine learning engineer wants to implement a machine learning pipeline on AWS to automate the process of training and deploying models. The pipeline should include data preprocessing, model training, and model deployment.\n\nWhich AWS service would the machine learning engineer use to orchestrate this machine learning pipeline?",
            "options": [
                "Amazon Rekognition",
                "Amazon Bedrock",
                "Amazon Q",
                "Amazon SageMaker AI"
            ],
            "answer": 3,
            "explanation": "Amazon SageMaker AI allows you to build, train, and deploy machine learning (ML) models for any use case with fully managed infrastructure, tools, and workflows.",
            "incorrect_explanations": [
                "Amazon Rekognition is used for image recognition and video analysis with machine learning.",
                "Amazon Bedrock allows you to build and scale generative AI applications with foundation models.",
                "Amazon Q is a generative AI-powered assistant for accelerating software development and leveraging companies' internal data.",
                "" # For correct answer
            ],
            "type": "single",
            "domain": "ML Development Lifecycle",
            "difficulty": "Medium"
        }
    ]

def create_gauge_chart(percentage, title):
    # Create a half-circle gauge chart
    fig, ax = plt.subplots(figsize=(6, 4), subplot_kw={'projection': 'polar'})
    
    # Customize the gauge
    theta = np.linspace(0, np.pi, 100)
    r = [1] * 100
    
    # Plot background (gray)
    ax.plot(theta, r, color='lightgray', linewidth=10, alpha=0.5)
    
    # Plot value (colored based on score)
    if percentage < 60:
        color = AWS_COLORS["error"]
    elif percentage < 80:
        color = AWS_COLORS["secondary"]
    else:
        color = AWS_COLORS["success"]
    
    value_theta = np.linspace(0, np.pi * (percentage/100), 100)
    value_r = [1] * len(value_theta)
    ax.plot(value_theta, value_r, color=color, linewidth=10)
    
    # Customize the chart
    ax.set_axis_off()
    
    # Add percentage text
    ax.text(np.pi/2, 0.5, f"{percentage}%", fontsize=24, ha='center', va='center')
    ax.text(np.pi/2, 0.2, title, fontsize=12, ha='center', va='center')
    
    plt.tight_layout()
    return fig

# Sidebar content
def sidebar_content():
    with st.sidebar:
        # st.markdown("<h3 class='sidebar-header'>Exam Navigator</h3>", unsafe_allow_html=True)
        
        # st.image(aws_logo(), width=200)
        # st.markdown("### AWS AI Practitioner")
        # st.markdown("#### Certification Exam Simulator")
        
        st.markdown("---")
        
        st.markdown("### Progress")
        progress = 0
        if st.session_state.total_questions > 0:
            progress = (st.session_state.current_question + 1) / st.session_state.total_questions
        st.progress(progress)
        
        st.markdown(f"Question {st.session_state.current_question + 1} of {st.session_state.total_questions}")
        
        st.markdown("---")
        
        if st.button("Reset Exam"):
            reset_exam()
            st.rerun()
            
        st.markdown("---")
        
        st.markdown("""
        ### Exam Tips
        - Read each question carefully
        - Review all options before selecting
        - Manage your time effectively
        - Mark challenging questions for review
        - Trust your knowledge
        """)

# Main exam interface
def render_question(question):
    st.markdown(f"<div class='question-container'><h3>Question {st.session_state.current_question + 1}</h3>", unsafe_allow_html=True)
    
    # Display domain and difficulty as chips
    st.markdown(f"""
    <div>
        <span class='chip'>{question['domain']}</span>
        <span class='chip'>{question['difficulty']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<p>{question['question']}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    option_letters = ["A", "B", "C", "D", "E", "F"]
    
    if question['type'] == 'single':
        answer = st.radio(
            "Select one answer:",
            options=question['options'],
            index=None,
            key=f"q{question['id']}"
        )
        
        if answer:
            selected_index = question['options'].index(answer)
            st.session_state.answers[question['id']] = selected_index
    
    elif question['type'] == 'matching':
        col1, col2 = st.columns(2)
        
        options = question['options']
        choices = question['choices']
        selected_choices = []
        
        for i, option in enumerate(options):
            with col1:
                st.markdown(f"**{option_letters[i]}. {option}**")
            
            with col2:
                selection = st.selectbox(
                    f"Select for option {option_letters[i]}:",
                    choices,
                    key=f"q{question['id']}_{i}"
                )
                selected_choices.append(choices.index(selection) if selection else None)
        
        if None not in selected_choices:
            st.session_state.answers[question['id']] = selected_choices
    
    # Display Submit button if answer is selected but not yet submitted
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Submit Answer", key=f"submit_{question['id']}"):
            st.session_state.submitted = True
    
    # Show explanation after submitting
    if st.session_state.submitted:
        display_explanation(question)
    
    # Navigation buttons
    st.markdown("<div class='navigation-buttons'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.current_question > 0:
            if st.button("Previous Question"):
                st.session_state.submitted = False
                st.session_state.current_question -= 1
                st.rerun()
    
    with col2:
        if st.session_state.current_question < st.session_state.total_questions - 1:
            if st.button("Next Question"):
                st.session_state.submitted = False
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("Finish Exam"):
                complete_exam()
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def display_explanation(question):
    is_correct = False
    
    if question['id'] in st.session_state.answers:
        selected_answer = st.session_state.answers[question['id']]
        
        if question['type'] == 'single':
            is_correct = selected_answer == question['answer']
        elif question['type'] == 'matching':
            is_correct = selected_answer == question['answer']
    
    if is_correct:
        st.markdown(f"""
        <div class='explanation-container correct'>
            <h4>✅ Correct!</h4>
            <p>{question['explanation']}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='explanation-container incorrect'>
            <h4>❌ Incorrect</h4>
        """, unsafe_allow_html=True)
        
        if question['type'] == 'single':
            selected_index = st.session_state.answers.get(question['id'], None)
            if selected_index is not None:
                st.markdown(f"""
                <p><strong>Your answer:</strong> {question['options'][selected_index]}</p>
                <p><strong>Explanation:</strong> {question['incorrect_explanations'][selected_index]}</p>
                <p><strong>Correct answer:</strong> {question['options'][question['answer']]}</p>
                <p><strong>Correct explanation:</strong> {question['explanation']}</p>
                """, unsafe_allow_html=True)
        
        elif question['type'] == 'matching':
            selected_choices = st.session_state.answers.get(question['id'], [])
            correct_choices = question['answer']
            
            st.markdown("<p><strong>Your answers:</strong></p>", unsafe_allow_html=True)
            for i, (selected, correct) in enumerate(zip(selected_choices, correct_choices)):
                choice_text = question['choices'][selected]
                correct_text = question['choices'][correct]
                
                if selected == correct:
                    st.markdown(f"""
                    <p>✅ {question['options'][i]}: {choice_text}</p>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <p>❌ {question['options'][i]}: {choice_text} (Correct: {correct_text})</p>
                    """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <p><strong>Explanation:</strong> {question['explanation']}</p>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def complete_exam():
    st.session_state.exam_completed = True
    
    # Calculate score
    correct = 0
    total = st.session_state.total_questions
    
    for question_id, selected_answer in st.session_state.answers.items():
        question = next((q for q in create_questions() if q['id'] == question_id), None)
        if question:
            if question['type'] == 'single':
                if selected_answer == question['answer']:
                    correct += 1
            elif question['type'] == 'matching':
                if selected_answer == question['answer']:
                    correct += 1
    
    st.session_state.score = round((correct / total) * 100) if total > 0 else 0
    st.session_state.correct_answers = correct
    st.session_state.incorrect_answers = total - correct

def reset_exam():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session_state()

def recommendation_based_on_score(score):
    if score >= 90:
        return "Excellent! You're well-prepared for the AWS AI Practitioner exam. Consider scheduling your certification exam soon."
    elif score >= 75:
        return "Good job! Review the topics where you made mistakes and take another practice exam before scheduling your certification."
    elif score >= 60:
        return "You're on the right track but need more practice. Focus on studying the domains where you struggled and take more practice exams."
    else:
        return "You need more preparation before taking the certification exam. Review the AWS AI Practitioner study materials, especially on the topics you missed, and practice with more mock exams."

def render_results():
    st.markdown("<h2 class='exam-header'>Results</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='summary-card'>", unsafe_allow_html=True)
        st.markdown("### Score Summary")
        st.markdown(f"**Total Questions**: {st.session_state.total_questions}")
        st.markdown(f"**Correct Answers**: {st.session_state.correct_answers}")
        st.markdown(f"**Incorrect Answers**: {st.session_state.incorrect_answers}")
        st.markdown(f"**Final Score**: {st.session_state.score}%")
        
        # Pass/Fail status (assuming 75% is passing score for AWS exams)
        if st.session_state.score >= 75:
            st.markdown("### Status: <span style='color:green;'>PASSED</span>", unsafe_allow_html=True)
        else:
            st.markdown("### Status: <span style='color:red;'>FAILED</span>", unsafe_allow_html=True)
            st.markdown("*Passing score is 75%*")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='gauge-container'>", unsafe_allow_html=True)
        gauge_chart = create_gauge_chart(st.session_state.score, "Overall Score")
        st.pyplot(gauge_chart)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Recommendation section
    st.markdown("<div class='recommendation-card'>", unsafe_allow_html=True)
    st.markdown("### Recommendation")
    st.markdown(recommendation_based_on_score(st.session_state.score))
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Review Questions"):
            st.session_state.exam_completed = False
            st.session_state.current_question = 0
            st.rerun()
    
    with col2:
        if st.button("Start New Exam"):
            reset_exam()
            st.rerun()

def main():
    init_session_state()
    
    # Load questions if not already loaded
    questions = create_questions()
    if st.session_state.total_questions == 0:
        st.session_state.total_questions = len(questions)
    
    # Set up sidebar
    sidebar_content()
    
    # Main content
    st.markdown("<h1 class='exam-header'>Knowledge Check</h1>", unsafe_allow_html=True)
    
    if st.session_state.exam_completed:
        render_results()
    else:
        current_question = questions[st.session_state.current_question]
        render_question(current_question)

if __name__ == "__main__":
    main()
