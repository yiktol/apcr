
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
            "question": "A small tech company is developing an AI chatbot to handle customer inquiries about their product line. They have access to a pre-trained large language model and are deciding on the best approach to customize it for their needs. The company has limited financial resources and wants to launch the chatbot within a month.\n\nWhich of the following approaches should they choose?",
            "options": [
                "Fine-tune the model on a dataset of past customer interactions to improve accuracy.",
                "Use prompt engineering to craft effective instructions for the model's responses.",
                "Combine fine-tuning and prompt engineering for optimal performance.",
                "Train a new model from scratch tailored specifically to their product line."
            ],
            "answer": 1,  # Index of correct option (zero-based)
            "explanation": "Prompt engineering is the most cost-effective and time-efficient approach for this scenario. It allows the company to quickly customize the model's behavior without the need for extensive computational resources or a large dataset. This method is ideal for companies with limited financial resources and tight timelines, as it can be implemented and iterated upon rapidly.",
            "incorrect_explanations": [
                "While fine-tuning can improve accuracy, it is more expensive and time-consuming than prompt engineering. It requires more computational resources, a substantial dataset, and typically takes longer to implement and test. Given the company's limited resources and one-month timeline, this approach is less suitable.",
                "",  # For correct answer
                "Combining fine-tuning and prompt engineering would offer comprehensive customization, but it's not the most cost-effective solution. The fine-tuning component would still introduce higher costs and longer development time, which doesn't align with the company's constraints.",
                "Training a new model from scratch would be the most expensive and time-consuming option. It requires significant expertise, computational resources, and a large amount of training data. This approach is far beyond the scope of what's needed and doesn't meet the company's resource and time constraints."
            ],
            "type": "single",
            "domain": "Foundation Model Customization",
            "difficulty": "Medium"
        },
        {
            "id": 2,
            "question": "A company is looking to build a Retrieval Augmented Generation (RAG) system. Select and order the correct steps from the following list that the company would need to take. Each step should be selected one time or not at all.",
            "options": [
                "Add examples of expected output to the prompt so the model generates desired results",
                "Retrieve relevant information by matching a user query with data in a vector database.",
                "Create external data and convert to numerical representations and store in vector database",
                "Create external data and embed the knowledge into the model through fine-tuning",
                "Augment the LLM prompt by adding the relevant retrieved data in context",
                "Augment the LLM prompt by asking the model to think step by step"
            ],
            "choices": [
                "Step 1",
                "Step 2",
                "Step 3"
            ],
            "answer": [2, 1, 4],  # Indices of the correct choices for each step
            "explanation": "The correct order for implementing a RAG system is: 1) Create external data and convert to numerical representations and store in vector database, 2) Retrieve relevant information by matching a user query with data in a vector database, and 3) Augment the LLM prompt by adding the relevant retrieved data in context.",
            "incorrect_explanations": [
                "This is describing few-shot prompting, not a step in RAG implementation.",
                "This is the second step in the RAG process, not the first or third.",
                "This is the first step in the RAG process, not the second or third.",
                "This describes fine-tuning, which is a different approach than RAG.",
                "This is the third step in the RAG process, not the first or second.",
                "This is describing Chain of Thought (CoT) prompting, not a step in RAG implementation."
            ],
            "type": "matching",
            "domain": "Retrieval Augmented Generation",
            "difficulty": "Hard"
        },
        {
            "id": 3,
            "question": "An insurance company is developing an AI-powered application to streamline their claims processing. The application needs to automatically break down and execute tasks, integrate with existing company APIs, and access company-specific insurance policy information. The company would also like the ability to choose the underlying Foundation Model.\n\nWhich combination of services would be most appropriate for this application?",
            "options": [
                "Amazon Q Developer",
                "Amazon Bedrock Knowledge Base",
                "Amazon Bedrock Agents",
                "PartyRock",
                "Amazon SageMaker JumpStart"
            ],
            "answer": [1, 2],  # Indices of correct options (zero-based, multiple correct)
            "explanation": "Amazon Bedrock Knowledge Base provides fully managed Retrieval Augmented Generation (RAG) capabilities, allowing the application to access and utilize company-specific insurance policy information effectively. Amazon Bedrock Agents offers natural language interaction, automatic task breakdown and execution, and integration with existing company APIs. It's ideal for orchestrating complex tasks in the claims processing workflow.",
            "incorrect_explanations": [
                "Amazon Q Developer is an AI-powered assistant for developers, but it's not designed for building customer-facing applications or processing insurance claims.",
                "Amazon Bedrock Knowledge Base provides fully managed Retrieval Augmented Generation (RAG) capabilities, allowing the application to access and utilize company-specific insurance policy information effectively.",
                "Amazon Bedrock Agents offers natural language interaction, automatic task breakdown and execution, and integration with existing company APIs. It's ideal for orchestrating complex tasks in the claims processing workflow.",
                "PartyRock is an experimental playground for generative AI applications, but it's not a production-ready service for building enterprise-grade insurance claim processing systems.",
                "Amazon SageMaker JumpStart provides pre-built machine learning models and algorithms, but it lacks the specific features needed for natural language processing, task orchestration, and knowledge retrieval required in this scenario."
            ],
            "type": "multi",
            "domain": "AWS Services for Generative AI",
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
                    index=None,
                    key=f"q{question['id']}_{i}"
                )
                if selection:
                    selected_choices.append(choices.index(selection))
                else:
                    selected_choices.append(None)
        
        if None not in selected_choices[:3]:  # We only need the first 3 selections
            st.session_state.answers[question['id']] = selected_choices[:3]
    
    elif question['type'] == 'multi':
        selected_options = []
        for i, option in enumerate(question['options']):
            if st.checkbox(option, key=f"q{question['id']}_{i}"):
                selected_options.append(i)
        
        if selected_options:
            st.session_state.answers[question['id']] = selected_options
    
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
        elif question['type'] == 'multi':
            is_correct = sorted(selected_answer) == sorted(question['answer'])
    
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
                option_text = question['options'][i]
                selected_text = question['choices'][selected] if selected is not None else "Not selected"
                correct_text = question['choices'][correct]
                
                if selected == correct:
                    st.markdown(f"""
                    <p>✅ {option_text}: {selected_text}</p>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <p>❌ {option_text}: {selected_text} (Correct: {correct_text})</p>
                    """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <p><strong>Explanation:</strong> {question['explanation']}</p>
            """, unsafe_allow_html=True)
        
        elif question['type'] == 'multi':
            selected_indices = st.session_state.answers.get(question['id'], [])
            correct_indices = question['answer']
            
            st.markdown("<p><strong>Your answers:</strong></p>", unsafe_allow_html=True)
            for i in selected_indices:
                if i in correct_indices:
                    st.markdown(f"✅ {question['options'][i]}", unsafe_allow_html=True)
                else:
                    st.markdown(f"❌ {question['options'][i]}", unsafe_allow_html=True)
            
            st.markdown("<p><strong>Correct answers:</strong></p>", unsafe_allow_html=True)
            for i in correct_indices:
                if i not in selected_indices:
                    st.markdown(f"• {question['options'][i]}", unsafe_allow_html=True)
            
            st.markdown(f"<p><strong>Explanation:</strong> {question['explanation']}</p>", unsafe_allow_html=True)
        
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
            elif question['type'] == 'multi':
                if sorted(selected_answer) == sorted(question['answer']):
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
