import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import yaml
import time
import base64
from datetime import datetime
import random

# Set page configuration
st.set_page_config(
    page_title="LLM Prompting Techniques",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #333;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f7ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
        margin-bottom: 1rem;
    }
    .warning-box {
        background-color: #fff8e1;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #FFC107;
        margin-bottom: 1rem;
    }
    .tip-box {
        background-color: #e8f5e9;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 1rem;
    }
    .completed {
        color: #4CAF50;
        font-weight: bold;
    }
    .pending {
        color: #FFC107;
        font-weight: bold;
    }
    .not-started {
        color: #9E9E9E;
    }
    .card {
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        height: 100%;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .blue-card {
        background-color: #e3f2fd;
    }
    .green-card {
        background-color: #e8f5e9;
    }
    .purple-card {
        background-color: #f3e5f5;
    }
    .quiz-form {
        background-color: #fafafa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .certificate {
        background-color: #fff;
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Course content stored as a dictionary
course_content = {
    "Introduction to Prompting": {
        "title": "Introduction to Prompting Techniques for LLMs",
        "description": """
        <div class="info-box">
        <p>Large Language Models (LLMs) like GPT-4, Claude, and LLaMA have revolutionized the way we interact with AI systems.
        The effectiveness of these models heavily depends on how we communicate our instructions to them through <b>prompting</b>.</p>
        
        <p>In this course, we'll explore the key differences between <b>zero-shot prompting</b> and <b>few-shot prompting</b>
        techniques, understanding how to leverage each method for optimal results.</p>
        </div>
        """,
        "learning_objectives": [
            "Understand the fundamental concepts of LLM prompting",
            "Distinguish between zero-shot and few-shot prompting techniques",
            "Learn when to apply each technique for optimal results",
            "Practice creating effective prompts for different scenarios"
        ],
        "estimated_time": "15 minutes",
        "image": "https://cdn-images-1.medium.com/max/1200/0*wbS8wGHVAGE0tzrU",
        "completion_points": 5
    },
    "Zero-Shot Prompting": {
        "title": "Zero-Shot Prompting: Capabilities and Limitations",
        "description": """
        <div class="info-box">
        <p>Zero-shot prompting refers to the technique where we ask an LLM to perform a task without providing any examples.
        The model relies solely on its pre-training to understand and execute the requested action.</p>
        
        <p>Modern LLMs have impressive zero-shot capabilities due to their extensive training on diverse text data,
        allowing them to understand and follow complex instructions with no additional context.</p>
        </div>
        """,
        "key_points": [
            "Definition: Asking an LLM to perform a task without examples",
            "Advantages: Quick to implement, requires minimal prompt engineering",
            "Limitations: May struggle with complex or highly specific tasks",
            "Best use cases: Common tasks, general knowledge questions, simple transformations"
        ],
        "code_example": """
# Example of Zero-Shot Prompting
prompt = \"\"\"
Classify the following text as expressing a positive, negative, or neutral sentiment:

'I absolutely loved the new restaurant downtown. The food was delicious and the service was excellent!'
\"\"\"

# Send to LLM API
response = llm.generate(prompt)
""",
        "image": "https://pbs.twimg.com/media/FvDuIUcaYAAWDoS?format=jpg",
        "completion_points": 10
    },
    "Few-Shot Prompting": {
        "title": "Few-Shot Prompting: Learning from Examples",
        "description": """
        <div class="info-box">
        <p>Few-shot prompting involves providing the LLM with a small number of examples that demonstrate the expected input-output pattern 
        before asking it to perform a similar task on a new input.</p>
        
        <p>This technique helps the model understand the specific pattern you want it to follow, 
        especially for tasks that might be ambiguous or require a particular format or reasoning style.</p>
        </div>
        """,
        "key_points": [
            "Definition: Providing examples of desired behavior before the actual task",
            "Advantages: Improves performance on complex, ambiguous, or specialized tasks",
            "Structure: Input-output pairs that demonstrate the pattern",
            "Best use cases: Format-specific outputs, classification with custom categories, reasoning tasks"
        ],
        "code_example": """
# Example of Few-Shot Prompting
prompt = \"\"\"
Classify the sentiment of the text as POSITIVE, NEGATIVE, or NEUTRAL:

Text: "The movie was absolutely fantastic!"
Sentiment: POSITIVE

Text: "The service was slow and the staff was rude."
Sentiment: NEGATIVE

Text: "The store opens at 9am and closes at 5pm."
Sentiment: NEUTRAL

Text: "I waited an hour for my food and when it arrived it was cold."
Sentiment: 
\"\"\"

# Send to LLM API
response = llm.generate(prompt)
""",
        "image": "https://miro.medium.com/max/1400/1*0inJfF8xp-VN69bqN1tEOw.png",
        "completion_points": 15
    },
    "Comparing Techniques": {
        "title": "Comparing Zero-Shot vs Few-Shot Approaches",
        "description": """
        <div class="info-box">
        <p>Understanding when to use zero-shot vs. few-shot prompting is crucial for effective LLM utilization.
        Each approach has specific strengths, weaknesses, and appropriate use cases.</p>
        </div>
        """,
        "comparison_table": [
            {"Feature": "Example requirements", "Zero-Shot": "None", "Few-Shot": "Several examples needed"},
            {"Feature": "Prompt length", "Zero-Shot": "Usually shorter", "Few-Shot": "Longer due to examples"},
            {"Feature": "Token usage", "Zero-Shot": "Lower consumption", "Few-Shot": "Higher consumption"},
            {"Feature": "Consistency", "Zero-Shot": "More variable", "Few-Shot": "More consistent"},
            {"Feature": "Custom formatting", "Zero-Shot": "Challenging", "Few-Shot": "Easier to enforce"},
            {"Feature": "Domain adaptation", "Zero-Shot": "Limited", "Few-Shot": "Better for specialized domains"}
        ],
        "scenario_analysis": [
            "Text classification: Few-shot often provides more consistent results",
            "General knowledge questions: Zero-shot usually sufficient",
            "Specialized jargon or domain: Few-shot demonstrates expected terminology",
            "Format-specific outputs (JSON, etc.): Few-shot helps enforce structure"
        ],
        "image": "https://blog.gopenai.com/content/images/size/w1600/2023/05/Few-Shot-Learning-2.png",
        "completion_points": 15
    },
    "Practical Applications": {
        "title": "Practical Applications and Best Practices",
        "description": """
        <div class="info-box">
        <p>Let's explore real-world applications of zero-shot and few-shot prompting,
        along with best practices for implementing these techniques effectively.</p>
        </div>
        """,
        "applications": [
            "Content generation with specific tones or styles",
            "Data extraction from unstructured text",
            "Code generation with specific patterns or frameworks",
            "Question answering systems",
            "Translation with specific terminology requirements",
            "Summarization with custom formats"
        ],
        "best_practices": [
            "Be explicit about the task and expectations",
            "For few-shot, use diverse but representative examples",
            "Include edge cases in your examples when relevant",
            "Test both approaches and compare results",
            "Consider token limits when designing prompts",
            "Iterate and refine based on model outputs"
        ],
        "challenges": [
            "Example selection bias in few-shot prompting",
            "Balancing prompt clarity vs. token efficiency",
            "Handling edge cases and exceptions",
            "Ensuring consistent performance across diverse inputs"
        ],
        "image": "https://cdn-images-1.medium.com/max/1200/1*j9TKEV3KRoVKQYVnwT3Srw.jpeg",
        "completion_points": 20
    }
}

# Quiz data
quiz_data = {
    "Introduction to Prompting": [
        {
            "question": "What does LLM stand for?",
            "options": ["Language Learning Model", "Large Language Model", "Linear Language Mechanism", "Linguistic Logical Module"],
            "correct_answer": "Large Language Model",
            "explanation": "LLM stands for Large Language Model, which refers to advanced AI models trained on vast amounts of text data to generate human-like text."
        },
        {
            "question": "What is the primary purpose of prompting in LLMs?",
            "options": [
                "To start the model's internal processors", 
                "To communicate instructions to the model", 
                "To debug model errors", 
                "To decrease model latency"
            ],
            "correct_answer": "To communicate instructions to the model",
            "explanation": "Prompting is how we communicate our intentions and instructions to LLMs, guiding them to produce the desired outputs."
        }
    ],
    "Zero-Shot Prompting": [
        {
            "question": "Which of the following best describes zero-shot prompting?",
            "options": [
                "Asking the model to perform a task without any examples", 
                "Training a model from scratch", 
                "Using exactly zero inputs for the model", 
                "Running the model with minimum parameters"
            ],
            "correct_answer": "Asking the model to perform a task without any examples",
            "explanation": "Zero-shot prompting refers to asking an LLM to perform a task without providing any examples of the task."
        },
        {
            "question": "For which of the following tasks would zero-shot prompting typically be MOST suitable?",
            "options": [
                "Generating text in a highly specific format", 
                "Answering a general knowledge question", 
                "Following a complex custom classification scheme", 
                "Mimicking a specific writing style"
            ],
            "correct_answer": "Answering a general knowledge question",
            "explanation": "Zero-shot prompting works well for tasks that align with the model's pre-training, such as answering general knowledge questions."
        },
        {
            "question": "What is a primary advantage of zero-shot prompting?",
            "options": [
                "It always produces the most accurate results", 
                "It requires minimal prompt engineering", 
                "It uses no computational resources", 
                "It works better for specialized tasks"
            ],
            "correct_answer": "It requires minimal prompt engineering",
            "explanation": "A key advantage of zero-shot prompting is its simplicity - it requires minimal prompt engineering compared to few-shot approaches."
        }
    ],
    "Few-Shot Prompting": [
        {
            "question": "In few-shot prompting, what are you providing to the model?",
            "options": [
                "Feedback after each response", 
                "Multiple training iterations", 
                "Examples that demonstrate the expected input-output pattern", 
                "Hardware acceleration parameters"
            ],
            "correct_answer": "Examples that demonstrate the expected input-output pattern",
            "explanation": "Few-shot prompting involves providing examples of input-output pairs to demonstrate the pattern you want the model to follow."
        },
        {
            "question": "Which statement about few-shot prompting is TRUE?",
            "options": [
                "It requires lower token consumption than zero-shot", 
                "It typically involves providing 100+ examples", 
                "It helps enforce specific output formats", 
                "It's only useful for simple tasks"
            ],
            "correct_answer": "It helps enforce specific output formats",
            "explanation": "Few-shot prompting is particularly effective at enforcing specific output formats by demonstrating the desired structure through examples."
        }
    ],
    "Comparing Techniques": [
        {
            "question": "Which prompting technique typically consumes more tokens?",
            "options": [
                "Zero-shot prompting", 
                "Few-shot prompting", 
                "Both use exactly the same number of tokens", 
                "It depends only on the model size"
            ],
            "correct_answer": "Few-shot prompting",
            "explanation": "Few-shot prompting typically consumes more tokens because it includes examples in the prompt, making the overall prompt longer."
        },
        {
            "question": "When would few-shot prompting be preferred over zero-shot prompting?",
            "options": [
                "When minimizing token usage is the top priority", 
                "For extremely simple questions", 
                "When immediate response is critical", 
                "When consistency and specific formatting are important"
            ],
            "correct_answer": "When consistency and specific formatting are important",
            "explanation": "Few-shot prompting is preferred when consistency and specific formatting are important, as examples help guide the model to produce outputs in the desired format."
        }
    ],
    "Practical Applications": [
        {
            "question": "What is a best practice when creating few-shot examples?",
            "options": [
                "Always use at least 10 examples", 
                "Use only the simplest possible examples", 
                "Include diverse but representative examples", 
                "Only include perfect cases, never edge cases"
            ],
            "correct_answer": "Include diverse but representative examples",
            "explanation": "When creating few-shot examples, it's best to include diverse but representative examples that cover the range of inputs the model might encounter."
        },
        {
            "question": "Which of the following applications would MOST benefit from few-shot prompting?",
            "options": [
                "Asking about the capital of France", 
                "Generating a summary in a specific format", 
                "Simple sentiment analysis (positive/negative)", 
                "Converting Celsius to Fahrenheit"
            ],
            "correct_answer": "Generating a summary in a specific format",
            "explanation": "Few-shot prompting is particularly beneficial for tasks requiring specific formats, like generating summaries with particular structures or sections."
        }
    ]
}

# Initialize session state variables
if "progress" not in st.session_state:
    st.session_state.progress = {}

if "quiz_results" not in st.session_state:
    st.session_state.quiz_results = {}

if "current_module" not in st.session_state:
    st.session_state.current_module = "Introduction to Prompting"

if "completed_modules" not in st.session_state:
    st.session_state.completed_modules = set()

if "points" not in st.session_state:
    st.session_state.points = 0

if "certificate_generated" not in st.session_state:
    st.session_state.certificate_generated = False

# Function to calculate progress percentage
def calculate_progress():
    total_modules = len(course_content)
    if total_modules == 0:
        return 0
    return int((len(st.session_state.completed_modules) / total_modules) * 100)

# Function to reset session state
def reset_session():
    st.session_state.progress = {}
    st.session_state.quiz_results = {}
    st.session_state.current_module = "Introduction to Prompting"
    st.session_state.completed_modules = set()
    st.session_state.points = 0
    st.session_state.certificate_generated = False
    st.rerun()

# Function to mark module as viewed
def mark_module_viewed(module_name):
    if module_name not in st.session_state.progress:
        st.session_state.progress[module_name] = "Viewed"

# Function to mark module as completed
def mark_module_completed(module_name):
    st.session_state.progress[module_name] = "Completed"
    st.session_state.completed_modules.add(module_name)
    if module_name in course_content:
        st.session_state.points += course_content[module_name]["completion_points"]

# Sidebar navigation
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>LLM Prompting Mastery</h1>", unsafe_allow_html=True)
    
    # Course progress
    progress_percentage = calculate_progress()
    st.progress(progress_percentage)
    st.markdown(f"<p style='text-align: center;'><b>{progress_percentage}%</b> completed</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Course Modules")
    
    # Module selection
    for module in course_content.keys():
        module_status = st.session_state.progress.get(module, "Not Started")
        
        if module_status == "Completed":
            status_html = f"<span class='completed'>✓ {module}</span>"
        elif module_status == "Viewed":
            status_html = f"<span class='pending'>➤ {module}</span>"
        else:
            status_html = f"<span class='not-started'>{module}</span>"
        
        if st.sidebar.button(status_html, key=f"btn_{module}", use_container_width=True):
            st.session_state.current_module = module
            mark_module_viewed(module)
            st.rerun()
    
    st.markdown("---")
    st.markdown(f"### Your Points: {st.session_state.points}")
    
    # Reset button
    if st.button("Reset Progress", use_container_width=True):
        reset_session()

# Main content area
current_module = st.session_state.current_module
module_data = course_content[current_module]

# Display module title
st.markdown(f"<h1 class='main-header'>{module_data['title']}</h1>", unsafe_allow_html=True)

# Display estimated time if available
if "estimated_time" in module_data:
    st.markdown(f"<p>⏱️ <b>Estimated time:</b> {module_data['estimated_time']}</p>", unsafe_allow_html=True)

# Display module image if available
if "image" in module_data:
    st.image(module_data["image"], use_column_width=True)

# Display module description
st.markdown(module_data["description"], unsafe_allow_html=True)

# Display learning objectives if available
if "learning_objectives" in module_data:
    with st.expander("Learning Objectives", expanded=True):
        for objective in module_data["learning_objectives"]:
            st.markdown(f"- {objective}")

# Display key points if available
if "key_points" in module_data:
    st.markdown("<h2 class='sub-header'>Key Points</h2>", unsafe_allow_html=True)
    for point in module_data["key_points"]:
        st.markdown(f"- {point}")

# Display code example if available
if "code_example" in module_data:
    st.markdown("<h2 class='sub-header'>Code Example</h2>", unsafe_allow_html=True)
    st.code(module_data["code_example"], language="python")

# Display comparison table if available
if "comparison_table" in module_data:
    st.markdown("<h2 class='sub-header'>Comparison: Zero-Shot vs Few-Shot</h2>", unsafe_allow_html=True)
    df = pd.DataFrame(module_data["comparison_table"])
    st.table(df)

# Display scenario analysis if available
if "scenario_analysis" in module_data:
    st.markdown("<h2 class='sub-header'>When to Use Each Approach</h2>", unsafe_allow_html=True)
    for scenario in module_data["scenario_analysis"]:
        st.markdown(f"- {scenario}")

# Display applications if available
if "applications" in module_data:
    st.markdown("<h2 class='sub-header'>Applications</h2>", unsafe_allow_html=True)
    for app in module_data["applications"]:
        st.markdown(f"- {app}")

# Display best practices if available
if "best_practices" in module_data:
    with st.expander("Best Practices", expanded=True):
        for practice in module_data["best_practices"]:
            st.markdown(f"- {practice}")

# Display challenges if available
if "challenges" in module_data:
    with st.expander("Common Challenges", expanded=True):
        for challenge in module_data["challenges"]:
            st.markdown(f"- {challenge}")

# Divider before quiz
st.markdown("---")

# Quiz section
if current_module in quiz_data:
    st.markdown("<h2 class='sub-header'>Module Quiz</h2>", unsafe_allow_html=True)
    
    quiz_key = f"quiz_{current_module}"
    quiz_questions = quiz_data[current_module]
    
    if quiz_key not in st.session_state:
        st.session_state[quiz_key] = {
            "current_question": 0,
            "correct_answers": 0,
            "total_questions": len(quiz_questions),
            "completed": False
        }
    
    quiz_state = st.session_state[quiz_key]
    
    if not quiz_state["completed"]:
        current_q_idx = quiz_state["current_question"]
        
        if current_q_idx < len(quiz_questions):
            question = quiz_questions[current_q_idx]
            
            with st.form(key=f"quiz_form_{current_module}_{current_q_idx}"):
                st.markdown(f"<div class='quiz-form'><p><b>Question {current_q_idx + 1}/{len(quiz_questions)}:</b> {question['question']}</p></div>", unsafe_allow_html=True)
                
                user_answer = st.radio("Select your answer:", question["options"], key=f"q_{current_module}_{current_q_idx}")
                
                submitted = st.form_submit_button("Submit Answer")
                
                if submitted:
                    if user_answer == question["correct_answer"]:
                        st.success("✅ Correct! " + question["explanation"])
                        quiz_state["correct_answers"] += 1
                    else:
                        st.error(f"❌ Incorrect. The correct answer is: {question['correct_answer']}")
                        st.info(question["explanation"])
                    
                    # Move to next question
                    quiz_state["current_question"] += 1
                    
                    # Check if quiz is complete
                    if quiz_state["current_question"] >= len(quiz_questions):
                        quiz_state["completed"] = True
                        score_percentage = (quiz_state["correct_answers"] / quiz_state["total_questions"]) * 100
                        
                        if score_percentage >= 70:
                            mark_module_completed(current_module)
                        
                    time.sleep(1)  # Give user time to see the result
                    st.rerun()
        
    if quiz_state["completed"]:
        score_percentage = (quiz_state["correct_answers"] / quiz_state["total_questions"]) * 100
        
        st.markdown(f"""
        <div class='info-box'>
            <h3>Quiz Results</h3>
            <p>You scored {quiz_state["correct_answers"]} out of {quiz_state["total_questions"]} ({score_percentage:.1f}%)</p>
        </div>
        """, unsafe_allow_html=True)
        
        if score_percentage >= 70:
            st.success("🎉 Congratulations! You've passed this module's quiz.")
            if st.button("Continue to Next Module", key=f"next_{current_module}"):
                # Find the index of the current module
                modules_list = list(course_content.keys())
                current_idx = modules_list.index(current_module)
                
                # If there's a next module, go to it
                if current_idx < len(modules_list) - 1:
                    st.session_state.current_module = modules_list[current_idx + 1]
                    mark_module_viewed(modules_list[current_idx + 1])
                    st.rerun()
        else:
            st.warning("You need to score at least 70% to complete this module. Feel free to review the content and try again.")
            if st.button("Retry Quiz", key=f"retry_{current_module}"):
                # Reset quiz state
                st.session_state[quiz_key] = {
                    "current_question": 0,
                    "correct_answers": 0,
                    "total_questions": len(quiz_questions),
                    "completed": False
                }
                st.rerun()

# Generate certificate if all modules completed
if len(st.session_state.completed_modules) == len(course_content) and not st.session_state.certificate_generated:
    st.markdown("---")
    st.markdown("<h2 class='sub-header'>🎉 Course Completed!</h2>", unsafe_allow_html=True)
    
    if st.button("Generate Certificate"):
        st.session_state.certificate_generated = True
        st.rerun()

if st.session_state.certificate_generated:
    current_date = datetime.now().strftime("%B %d, %Y")
    certificate_id = f"LLM-PROMPT-{random.randint(10000, 99999)}"
    
    st.markdown(f"""
    <div class="certificate">
        <h1 style="color:#1E88E5;">Certificate of Completion</h1>
        <h2>This is to certify that</h2>
        <h2 style="color:#333; font-size:1.8rem;">LLM Learner</h2>
        <p>has successfully completed the course</p>
        <h3 style="color:#4CAF50; font-size:1.5rem;">Zero-shot vs Few-shot Prompting Techniques</h3>
        <p>with a total score of {st.session_state.points} points</p>
        <p>Date: {current_date}</p>
        <p style="font-size:0.8rem; color:#666;">Certificate ID: {certificate_id}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("Start Over"):
        reset_session()

# Footer with features based on screen size
footer_cols = st.columns([1, 1, 1])

with footer_cols[0]:
    st.markdown("""
    <div class="card blue-card">
        <h3>📚 Resources</h3>
        <p>Explore additional learning materials on LLM prompting techniques.</p>
    </div>
    """, unsafe_allow_html=True)

with footer_cols[1]:
    st.markdown("""
    <div class="card green-card">
        <h3>💬 Community</h3>
        <p>Join our Discord community to discuss prompting strategies with peers.</p>
    </div>
    """, unsafe_allow_html=True)

with footer_cols[2]:
    st.markdown("""
    <div class="card purple-card">
        <h3>🔍 Advanced Course</h3>
        <p>Ready for more? Check out our advanced LLM fine-tuning course.</p>
    </div>
    """, unsafe_allow_html=True)
