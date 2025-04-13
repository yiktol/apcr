
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
            "question": "A machine learning engineer is tasked with generating text using a Large Language Model (LLM) hosted in Amazon Bedrock. They need to decide between using the temperature and top_p parameters to control the output.\n\nWhich of the following statements is true about the temperature and top_p parameters used for text generation?",
            "options": [
                "The temperature parameter controls the creativity of the output, while top_p limits the next word choice to the most likely options.",
                "The temperature parameter limits the next word choice to the most likely options, while top_p controls the creativity of the output.",
                "Both temperature and top_p parameters control the creativity of the output.",
                "Both temperature and top_p parameters limit the next word choice to the most likely options."
            ],
            "answer": 0,  # Index of correct option (zero-based)
            "explanation": "The temperature parameter adjusts the randomness of the output by scaling the logits before applying the softmax function. Lower temperatures result in less random output, while higher temperatures result in more random output. The top_p parameter, on the other hand, controls the number of tokens considered for each word by selecting the top p tokens with the highest probability.",
            "incorrect_explanations": [
                "",  # For correct answer
                "The roles of temperature and top_p are reversed in this option.",
                "Only temperature controls the randomness of the output, while top_p controls the number of tokens considered.",
                "Only top_p controls the number of tokens considered, while temperature controls the randomness of the output."
            ],
            "type": "single",
            "domain": "Generative AI Fundamentals",
            "difficulty": "Medium"
        },
        {
            "id": 2,
            "question": "A data scientist is working for a large retail company that wants to leverage the power of existing large language models (LLMs) for various natural language processing tasks, such as product description generation, customer support chatbots, and sentiment analysis. They have decided to use Amazon SageMaker for training and deploying these models.\n\nWhich of the following would be the most appropriate approach for working with LLMs on Amazon SageMaker?",
            "options": [
                "Use SageMaker's built-in algorithms for natural language processing tasks, such as the BlazingText algorithm for text classification or the Sequence-to-Sequence algorithm for text generation.",
                "Train your own custom language model from scratch using SageMaker's Deep Learning Containers and the TensorFlow or PyTorch frameworks.",
                "Use SageMaker JumpStart to quickly get started with pre-trained foundation models like BERT or T5 without the need for extensive training.",
                "Provision a high-performance EC2 instance with GPU support, install the necessary deep learning frameworks and libraries, and train your language model outside of SageMaker."
            ],
            "answer": 2,
            "explanation": "SageMaker JumpStart provides a convenient way to get started with pre-trained foundation models like GPT-3, BERT, and T5. It offers pre-trained model checkpoints, pre-built Docker containers, and example notebooks, allowing you to quickly fine-tune and deploy these models for various natural language processing tasks without the need for extensive training from scratch.",
            "incorrect_explanations": [
                "While SageMaker's built-in algorithms are useful for specific natural language processing tasks, they are not suitable for working with large foundation models like GPT-3 or BERT. These models require specialized infrastructure and pre-trained checkpoints.",
                "Training a large language model from scratch is an extremely resource-intensive and time-consuming process, requiring massive amounts of data and computational power. For most practical use cases, it is more efficient to leverage pre-trained models and fine-tune them for specific tasks.",
                "", # For correct answer
                "While you can certainly train language models outside of SageMaker by provisioning EC2 instances and installing the necessary frameworks and libraries, this approach is more complex and requires manual setup and management. SageMaker provides a managed service with built-in support for distributed training, automatic model tuning, and easy deployment, making it a more convenient and scalable choice for working with large language models."
            ],
            "type": "single",
            "domain": "AWS Infrastructure for Generative AI",
            "difficulty": "Medium"
        },
        {
            "id": 3,
            "question": "A company is developing a generative AI chatbot for its users. The chatbot must be available at all times. To manage costs, the system should be efficient during idle times. Additionally, the company wants the ability to select the underlying Foundation Model (FM) for the chatbot.\n\nWhich service meets these requirements MOST cost-effectively?",
            "options": [
                "Amazon Q",
                "Amazon SageMaker",
                "Amazon Elastic Compute Cloud",
                "Amazon Bedrock"
            ],
            "answer": 3,
            "explanation": "Bedrock checks all the boxes – its pricing is token based so if there are no invocations, there are no costs. Bedrock also allows you to choose the Foundation Model.",
            "incorrect_explanations": [
                "Amazon Q does not allow you to select the underlying Foundation Model.",
                "While SageMaker could work, it would not be the most cost effective solution during times of inactivity since you are paying for provisioned compute to provide inferencing.",
                "EC2 would not be the most efficient choice because you would need to run and manage instances during the idle times.",
                "" # For correct answer
            ],
            "type": "single",
            "domain": "AWS Services for Generative AI",
            "difficulty": "Easy"
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
