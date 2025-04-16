import streamlit as st
import base64
from PIL import Image
import requests
from io import BytesIO
import json
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import uuid

# Define AWS color scheme
AWS_COLORS = {
    "primary": "#232F3E",     # AWS Navy
    "secondary": "#FF9900",   # AWS Orange
    "light": "#FFFFFF",       # White
    "dark_gray": "#545B64",   # Dark Gray
    "light_gray": "#D5DBDB",  # Light Gray
    "success": "#008296",     # Teal
    "warning": "#EC7211",     # Orange
    "error": "#D13212",       # Red
    "info": "#1E88E5",        # Blue
}

# Set page configuration
st.set_page_config(
    page_title="AWS Learning Platform",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply AWS color scheme with CSS
st.markdown(f"""
<style>
    /* Main colors */
    :root {{
        --primary: {AWS_COLORS["primary"]};
        --secondary: {AWS_COLORS["secondary"]};
        --light: {AWS_COLORS["light"]};
        --dark-gray: {AWS_COLORS["dark_gray"]};
        --light-gray: {AWS_COLORS["light_gray"]};
        --success: {AWS_COLORS["success"]};
        --warning: {AWS_COLORS["warning"]};
        --error: {AWS_COLORS["error"]};
        --info: {AWS_COLORS["info"]};
    }}
    
    /* General styling */
    .stApp {{
        background-color: var(--light);
    }}
    
    .main {{
        background-color: var(--light);
    }}
    
    h1, h2, h3, h4 {{
        color: var(--primary);
        font-family: 'Amazon Ember', 'Helvetica Neue', Arial, sans-serif;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: var(--light-gray);
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        height: 50px;
    }}
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
        background-color: var(--secondary);
        color: var(--light);
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: var(--light);
        padding: 1rem;
    }}
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
        color: var(--primary);
    }}
    
    /* Card styling */
    .aws-card {{
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }}
    
    .aws-info-card {{
        background-color: #f0f7fb;
        border-left: 5px solid var(--info);
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 15px;
    }}
    
    .aws-warning-card {{
        background-color: #fff8f0;
        border-left: 5px solid var(--warning);
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 15px;
    }}
    
    .aws-success-card {{
        background-color: #f0f9f8;
        border-left: 5px solid var(--success);
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 15px;
    }}
    
    .aws-feature-card {{
        background-color: white;
        padding: 15px;
        border-radius: 6px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        height: 100%;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    
    .aws-feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }}
    
    /* Button styling */
    .stButton>button {{
        background-color: var(--secondary);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: 600;
    }}
    
    .stButton>button:hover {{
        background-color: #e67e00;
    }}
    
    /* Table styling */
    .dataframe {{
        border-collapse: collapse;
        width: 100%;
        font-size: 14px;
    }}
    
    .dataframe th {{
        background-color: var(--primary);
        color: white;
        text-align: left;
        padding: 12px 8px;
    }}
    
    .dataframe td {{
        padding: 8px;
        border-bottom: 1px solid #ddd;
    }}
    
    .dataframe tr:nth-child(even) {{
        background-color: #f2f2f2;
    }}
    
    /* Progress indicators */
    .stProgress > div > div > div > div {{
        background-color: var(--secondary);
    }}
    
    /* Alert boxes */
    .alert-success {{
        background-color: #e6f4f1;
        color: var(--success);
        padding: 16px;
        border-radius: 4px;
        margin: 16px 0;
    }}
    
    .alert-warning {{
        background-color: #fdf2e9;
        color: var(--warning);
        padding: 16px;
        border-radius: 4px;
        margin: 16px 0;
    }}
    
    .alert-error {{
        background-color: #fdedec;
        color: var(--error);
        padding: 16px;
        border-radius: 4px;
        margin: 16px 0;
    }}
    
    .alert-info {{
        background-color: #e8f4f8;
        color: var(--info);
        padding: 16px;
        border-radius: 4px;
        margin: 16px 0;
    }}
    
    /* Topic icons */
    .topic-icon {{
        font-size: 24px;
        margin-right: 10px;
        vertical-align: middle;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        padding: 20px 0;
        font-size: 12px;
        color: var(--dark-gray);
        border-top: 1px solid var(--light-gray);
        margin-top: 40px;
    }}
    
    /* Sidebar buttons */
    .sidebar-button {{
        background-color: rgba(255, 255, 255, 0.1);
        border: none;
        color: white;
        padding: 10px 15px;
        text-align: left;
        width: 100%;
        margin: 5px 0;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
    }}
    
    .sidebar-button:hover {{
        background-color: rgba(255, 255, 255, 0.2);
    }}
    
    .sidebar-button.active {{
        background-color: var(--secondary);
    }}
    
    /* Knowledge Check Section */
    .quiz-section {{
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 8px;
        border: 1px solid var(--light-gray);
    }}
    
    .quiz-section h4 {{
        border-bottom: 1px solid var(--light-gray);
        padding-bottom: 10px;
    }}
    
    .quiz-header {{
        background-color: var(--secondary);
        color: white;
        padding: 10px 15px;
        border-radius: 5px 5px 0 0;
        margin-bottom: 0;
    }}
    
    .quiz-container {{
        border: 1px solid var(--secondary);
        border-radius: 5px;
        margin-bottom: 20px;
    }}
    
    .quiz-body {{
        padding: 15px;
    }}
</style>
""", unsafe_allow_html=True)

# Function to load and cache images from URL
@st.cache_data
def load_image_from_url(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        st.warning(f"Could not load image: {str(e)}")
        return None

# Initialize session state
def init_session_state():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    # Initialize tracking only for knowledge checks
    if "quiz_scores" not in st.session_state:
        st.session_state.quiz_scores = {}
    
    if "quiz_attempted" not in st.session_state:
        st.session_state.quiz_attempted = {}
    
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    
# Reset session state
def reset_session():
    for key in list(st.session_state.keys()):
        if key != "session_id":
            del st.session_state[key]
    init_session_state()
    st.success("✅ Session data has been reset successfully!")
    
# Initialize session state at app startup
init_session_state()

# Sample quiz data structure
quiz_data = {
    "topic1": [
        {
            "question": "This is a sample question for Topic 1?",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Option A"
        },
        {
            "question": "This is another sample question for Topic 1?",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Option C"
        }
    ],
    "topic2": [
        {
            "question": "This is a sample question for Topic 2?",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Option B"
        }
    ]
}

# Function to create a pretty chart for quiz results
def create_quiz_results_chart():
    if not st.session_state.quiz_attempted:
        return None
        
    # Prepare data for visualization
    topics = []
    scores = []
    attempted = []
    
    for topic, attempted_count in st.session_state.quiz_attempted.items():
        if attempted_count > 0:
            topics.append(topic.upper())
            scores.append(st.session_state.quiz_scores.get(topic, 0))
            attempted.append(attempted_count)
    
    if not topics:  # No quiz data yet
        return None
    
    # Create a DataFrame for the chart
    data = {
        'Topic': topics,
        'Correct': scores,
        'Attempted': attempted
    }
    df = pd.DataFrame(data)
    
    # Calculate percentage correct
    df['Percentage'] = (df['Correct'] / df['Attempted'] * 100).round(0).astype(int)
    
    # Create a bar chart with Altair
    source = pd.melt(df, id_vars=['Topic', 'Percentage'], value_vars=['Correct', 'Attempted'], 
                  var_name='Type', value_name='Questions')
    
    chart = alt.Chart(source).mark_bar().encode(
        x=alt.X('Topic:N', sort=None, title=None),
        y=alt.Y('Questions:Q', title='Questions'),
        color=alt.Color('Type:N', scale=alt.Scale(
            domain=['Correct', 'Attempted'],
            range=[AWS_COLORS["success"], AWS_COLORS["light_gray"]]
        )),
        tooltip=['Topic', 'Type', 'Questions', alt.Tooltip('Percentage:Q', title='Success Rate %')]
    ).properties(
        title='Quiz Results by Topic',
        height=350
    )
    
    text = alt.Chart(df).mark_text(
        align='center',
        baseline='bottom',
        dy=-5,
        color='black',
        fontSize=14
    ).encode(
        x='Topic:N',
        y=alt.Y('Attempted:Q'),
        text=alt.Text('Percentage:Q', format='.0f', title='Success Rate %'),
        tooltip=['Topic', 'Correct', 'Attempted', alt.Tooltip('Percentage:Q', title='Success Rate %')]
    )
    
    return (chart + text).interactive()

# Function to handle quiz in knowledge checks page
def handle_quiz(topic, index, quiz):
    question = quiz["question"]
    options = quiz["options"]
    correct_answer = quiz["answer"]
    
    # Create a unique key for each quiz component
    question_key = f"{topic}_{index}"
    radio_key = f"{topic}_radio_{index}"
    check_key = f"check_{topic}_{index}"
    
    # Create a container for this quiz question
    with st.container():
        st.markdown(f"""
        <div class="quiz-container">
            <div class="quiz-header">
                <h4>{topic.upper()} - Question {index+1}</h4>
            </div>
            <div class="quiz-body">
                <p>{question}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display radio buttons for options
        selected_answer = st.radio(
            "Select your answer:",
            options,
            key=radio_key,
            index=None
        )
        
        # Check button
        col1, col2 = st.columns([1, 4])
        with col1:
            check_clicked = st.button("Check Answer", key=check_key)
        
        # Result display
        with col2:
            if check_clicked:
                if selected_answer is None:
                    st.warning("Please select an answer first.")
                else:
                    # Initialize topic in session state if it doesn't exist
                    if topic not in st.session_state.quiz_attempted:
                        st.session_state.quiz_attempted[topic] = 0
                    if topic not in st.session_state.quiz_scores:
                        st.session_state.quiz_scores[topic] = 0
                    
                    # Check if this specific question has been answered correctly before
                    answer_key = f"{topic}_answer_{index}"
                    already_correct = st.session_state.quiz_answers.get(answer_key, False)
                    
                    # Update tracking
                    st.session_state.quiz_attempted[topic] += 1
                    
                    if selected_answer == correct_answer and not already_correct:
                        st.success(f"✅ Correct! {correct_answer} is the right answer.")
                        st.session_state.quiz_scores[topic] += 1
                        st.session_state.quiz_answers[answer_key] = True
                    elif selected_answer == correct_answer and already_correct:
                        st.success(f"✅ Correct! {correct_answer} is the right answer.")
                    else:
                        st.error(f"❌ Incorrect. The correct answer is: {correct_answer}")
                        st.session_state.quiz_answers[answer_key] = False
        
        st.divider()

# Function to display content for Topic 1
def topic1_page():
    st.title("Topic 1")
    
    st.header("Topic 1 Header")
    st.markdown("""
    This is a template for Topic 1 content. You can add text, images, and interactive elements here.
    """)
    
    # Create feature highlights with cards
    st.subheader("Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🚀 Feature 1</h4>
            <p>Description of Feature 1</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>⚡ Feature 2</h4>
            <p>Description of Feature 2</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔄 Feature 3</h4>
            <p>Description of Feature 3</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Create a card with key concepts
    st.header("Key Concepts")
    
    st.markdown("""
    <div class="aws-card">
        <h3>Concept Group 1</h3>
        <p>Description of concept group 1.</p>
        <ul>
            <li><strong>Point 1:</strong> Details about point 1</li>
            <li><strong>Point 2:</strong> Details about point 2</li>
            <li><strong>Point 3:</strong> Details about point 3</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Add an info card
    st.markdown("""
    <div class="aws-info-card">
        <h4>Important Note</h4>
        <p>This is an important note about Topic 1 that users should be aware of.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add tabs for subtopics
    subtab1, subtab2 = st.tabs(["Subtopic 1", "Subtopic 2"])
    
    with subtab1:
        st.markdown("Content for subtopic 1")
    
    with subtab2:
        st.markdown("Content for subtopic 2")

# Function to display content for Topic 2
def topic2_page():
    st.title("Topic 2")
    
    st.header("Topic 2 Header")
    st.markdown("""
    This is a template for Topic 2 content. You can add text, images, and interactive elements here.
    """)
    
    # Example of columns layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h3>Left Column</h3>
            <p>Content for left column.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h3>Right Column</h3>
            <p>Content for right column.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Example of a chart
    st.subheader("Example Chart")
    
    # Create a simple chart
    data = pd.DataFrame({
        'Category': ['A', 'B', 'C', 'D'],
        'Values': [10, 25, 15, 30]
    })
    
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Category', sort=None),
        y='Values',
        color=alt.Color('Category', scale=alt.Scale(scheme='blues'))
    ).properties(
        width=600,
        height=300
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    # Add a warning card
    st.markdown("""
    <div class="aws-warning-card">
        <h4>Warning</h4>
        <p>This is a warning message for Topic 2.</p>
    </div>
    """, unsafe_allow_html=True)

# Function for Knowledge Checks page
def knowledge_checks_page():
    st.title("Knowledge Checks")
    
    st.markdown("""
    <div class="aws-info-card">
        <h3>Test your knowledge</h3>
        <p>Answer the questions below to check your understanding. Your progress is tracked at the bottom of this page.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display quiz section tabs
    tab_names = ["Topic 1", "Topic 2"]
    
    tabs = st.tabs(tab_names)
    
    # Topic 1 Quiz
    with tabs[0]:
        st.header("Topic 1 Knowledge Check")
        for i, quiz in enumerate(quiz_data["topic1"]):
            handle_quiz("topic1", i, quiz)
    
    # Topic 2 Quiz
    with tabs[1]:
        st.header("Topic 2 Knowledge Check")
        for i, quiz in enumerate(quiz_data["topic2"]):
            handle_quiz("topic2", i, quiz)
    
    # Progress Summary
    st.header("Your Progress")
    
    # Display chart if there's data
    chart = create_quiz_results_chart()
    if chart:
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Complete some knowledge checks to see your progress!")
    
    # Calculate and display overall progress
    if st.session_state.quiz_attempted:
        total_attempted = sum(st.session_state.quiz_attempted.values())
        total_correct = sum(st.session_state.quiz_scores.values())
        
        if total_attempted > 0:
            percentage = int((total_correct / total_attempted) * 100)
            
            st.markdown(f"""
            <div class="aws-success-card">
                <h3>Overall Score: {total_correct}/{total_attempted} ({percentage}%)</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Progress bar
            st.progress(total_correct / total_attempted)

# Home page content
def home_page():
    st.title("AWS Learning Platform")
    st.header("Welcome to the Template")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Placeholder for an image
        st.image("https://d1.awsstatic.com/training-and-certification/certification-badges/AWS-Certified-Cloud-Practitioner_badge.634f8a21af2e0e956ed8905a72366146ba22b74c.png", width=300)
    
    with col2:
        st.markdown("""
        Welcome to the AWS Learning Platform template. This interactive guide will help you learn 
        AWS services and concepts. Navigate through the topics using the tabs above.
        
        Each section contains key concepts, important takeaways, and interactive quizzes to reinforce your learning.
        """)
    
    st.markdown("""
    <div class="aws-info-card">
        <h3>Topics covered</h3>
        <p>
            • Topic 1<br>
            • Topic 2<br>
            • Knowledge Checks
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display tips
    st.markdown("""
    <div class="aws-card">
        <h3>📝 Learning Tips</h3>
        <p>Here are some tips to help you get the most out of this learning platform.</p>
        <ul>
            <li>Tip 1</li>
            <li>Tip 2</li>
            <li>Tip 3</li>
            <li>Tip 4</li>
            <li>Tip 5</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Services overview section
    st.header("Overview")
    
    # Create a grid of service cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔄 Topic 1</h4>
            <ul>
                <li><strong>Subtopic 1:</strong> Description of subtopic 1</li>
                <li><strong>Subtopic 2:</strong> Description of subtopic 2</li>
                <li><strong>Subtopic 3:</strong> Description of subtopic 3</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>💻 Topic 2</h4>
            <ul>
                <li><strong>Subtopic 1:</strong> Description of subtopic 1</li>
                <li><strong>Subtopic 2:</strong> Description of subtopic 2</li>
                <li><strong>Subtopic 3:</strong> Description of subtopic 3</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Sidebar for session management
st.sidebar.subheader("⚙️ Session Management")

# Reset button for session data
if st.sidebar.button("🔄 Reset Progress", key="reset_button"):
    reset_session()

# Show session ID
st.sidebar.caption(f"Session ID: {st.session_state.session_id[:8]}...")

st.sidebar.divider()

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Home", 
    "📌 Topic 1", 
    "📌 Topic 2", 
    "🧪 Knowledge Checks"
])

with tab1:
    home_page()

with tab2:
    topic1_page()

with tab3:
    topic2_page()

with tab4:
    knowledge_checks_page()

# Footer
st.markdown("""
<div class="footer">
    © 2025, Amazon Web Services, Inc. or its affiliates. All rights reserved.
</div>
""", unsafe_allow_html=True)
