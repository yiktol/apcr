
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
    # Responsible AI
    {
        "id": 1,
        "question": "A healthcare company is deploying an AI system to assist radiologists in identifying potential anomalies in medical images. They want to ensure their AI implementation follows responsible AI principles. Which approach best addresses fairness considerations?",
        "options": {
            "A": "Optimize the model to maximize overall accuracy across all datasets regardless of demographic representation",
            "B": "Train the model exclusively on data from the most common patient demographic to ensure reliable performance for the majority of cases",
            "C": "Assess model performance across different demographic groups and balance training data to minimize performance disparities",
            "D": "Deploy the model as quickly as possible and iteratively address any fairness concerns reported by users after launch"
        },
        "correct_answer": "C",
        "explanation": {
            "A": "Simply maximizing overall accuracy can hide significant disparities in model performance across different demographic groups, which contradicts responsible AI principles of fairness.",
            "B": "Training exclusively on the most common demographic would create significant bias against underrepresented groups, violating fairness principles and potentially causing harm.",
            "C": "Correct! Responsible AI requires evaluating model performance across different demographic groups and ensuring balanced training data to minimize performance disparities. This approach directly addresses the fairness dimension of responsible AI.",
            "D": "Waiting for user reports after deployment could expose patients to harmful biases and represents a reactive rather than proactive approach to responsible AI implementation."
        },
        "category": "Responsible AI"
    },
    {
        "id": 2,
        "question": "A financial services company has developed a machine learning model to automate loan approval decisions. To implement responsible AI practices, what should they focus on to ensure transparency in their system?",
        "options": {
            "A": "Use complex ensemble models that maximize prediction accuracy without concern for interpretability",
            "B": "Implement Amazon SageMaker Model Cards to document model information such as intended use, performance metrics, and limitations",
            "C": "Keep model documentation confidential to prevent competitors from replicating their approach",
            "D": "Only explain decisions when explicitly required by regulation to maintain competitive advantage"
        },
        "correct_answer": "B",
        "explanation": {
            "A": "Using complex models that prioritize accuracy over interpretability contradicts the transparency principle of responsible AI, especially in regulated industries like financial services.",
            "B": "Correct! Amazon SageMaker Model Cards provide a structured way to document model information including intended use, training data characteristics, performance metrics, and limitations. This documentation is essential for transparency in AI systems.",
            "C": "Keeping documentation confidential contradicts transparency principles and may violate regulatory requirements in financial services where explainability is often mandated.",
            "D": "Only providing explanations when required by regulation represents a minimal compliance approach rather than embracing the transparency principle of responsible AI."
        },
        "category": "Responsible AI"
    },
    {
        "id": 3,
        "question": "A retail company is experiencing dataset bias in their recommendation system that tends to suggest higher-priced products to certain demographic groups. During the model building phase, what is the most appropriate approach to address this bias?",
        "options": {
            "A": "Exclude demographic information entirely from the model to prevent any possible bias",
            "B": "Perform bias analysis using Amazon SageMaker Clarify during exploratory data analysis and implement mitigation strategies",
            "C": "Accept that bias is inevitable in recommendation systems and focus on maximizing overall conversion rates",
            "D": "Create separate models for each demographic group to optimize recommendations independently"
        },
        "correct_answer": "B",
        "explanation": {
            "A": "Simply excluding demographic information doesn't address underlying bias in other correlated features and can make bias monitoring more difficult.",
            "B": "Correct! Using tools like Amazon SageMaker Clarify to identify bias during exploratory data analysis allows you to implement appropriate mitigation strategies early in the development process, addressing the root causes of bias.",
            "C": "Accepting bias as inevitable contradicts responsible AI principles and could lead to harmful outcomes, potentially violating fairness requirements.",
            "D": "Creating separate models for different demographic groups could amplify existing inequalities and reinforce discriminatory patterns, contrary to fairness objectives."
        },
        "category": "Responsible AI"
    },
    {
        "id": 4,
        "question": "A company has trained a machine learning model to generate creative content for marketing campaigns. To implement the controllability aspect of responsible AI, which approach should they prioritize?",
        "options": {
            "A": "Focus exclusively on maximizing the creativity metrics of the model's output without human oversight",
            "B": "Implement AWS CloudWatch to log model outputs, but allow the system to operate autonomously",
            "C": "Use black-box testing to evaluate system performance without examining internal decision processes",
            "D": "Implement Amazon Augmented AI (A2I) to provide human review and guidance for model outputs that don't meet confidence thresholds"
        },
        "correct_answer": "D",
        "explanation": {
            "A": "Focusing solely on creativity metrics without human oversight violates the controllability principle, which requires mechanisms to monitor and steer AI system behavior.",
            "B": "While logging outputs is helpful, it's a passive monitoring approach that doesn't provide active control over the system's behavior.",
            "C": "Black-box testing doesn't address controllability as it doesn't provide mechanisms to steer the AI system's behavior.",
            "D": "Correct! Amazon Augmented AI (A2I) enables human review of machine predictions, providing a mechanism to monitor and control AI system behavior when it operates with low confidence or produces potentially problematic outputs."
        },
        "category": "Responsible AI"
    },
    
    # Transparent and Explainable Models
    {
        "id": 5,
        "question": "A financial institution is developing a credit scoring model that must meet regulatory requirements for explainability. Which implementation would best address the need for model transparency while maintaining acceptable performance?",
        "options": {
            "A": "Deploy a deep neural network that achieves 98% accuracy but operates as a black box",
            "B": "Use a gradient boosting model with Amazon SageMaker Clarify to explain feature importance for individual predictions",
            "C": "Implement a complex ensemble model that combines five different algorithms to maximize performance",
            "D": "Use a proprietary algorithm that outperforms competitors but doesn't provide insight into decision factors"
        },
        "correct_answer": "B",
        "explanation": {
            "A": "Deep neural networks often lack transparency in their decision-making process, making them unsuitable for highly regulated use cases requiring explainability.",
            "B": "Correct! Gradient boosting models with explainability tools like Amazon SageMaker Clarify provide a good balance between performance and interpretability, enabling feature importance explanations that satisfy regulatory requirements.",
            "C": "Complex ensemble models typically sacrifice explainability for performance gains, making regulatory compliance difficult.",
            "D": "Proprietary black-box algorithms that don't provide insight into decision factors would fail to meet regulatory requirements for explainability in credit scoring."
        },
        "category": "Transparent and Explainable Models"
    },
    {
        "id": 6,
        "question": "A healthcare company is implementing a human-centered design approach for their AI system that provides treatment recommendations to clinicians. Which approach best embodies this principle?",
        "options": {
            "A": "Building the most accurate predictive model possible, focusing primarily on technical metrics like precision and recall",
            "B": "Building a diverse team of AI engineers, clinicians, ethicists, and patient advocates to collaboratively design the system",
            "C": "Designing the system to operate autonomously without requiring clinician input to save time",
            "D": "Prioritizing the latest AI techniques regardless of how easily they can be understood by the clinical staff"
        },
        "correct_answer": "B",
        "explanation": {
            "A": "While accuracy is important, human-centered design requires considering human factors beyond technical metrics.",
            "B": "Correct! Human-centered design requires building diverse, multidisciplinary teams that include domain experts (clinicians), ethicists, and end-user representatives (patient advocates) to ensure the system meets human needs and operates ethically.",
            "C": "Autonomous operation without clinician input contradicts human-centered design principles, which emphasize keeping humans in the loop, especially for critical healthcare decisions.",
            "D": "Prioritizing advanced techniques without considering interpretability for clinical staff contradicts human-centered design principles, which emphasize systems that complement human understanding."
        },
        "category": "Transparent and Explainable Models"
    },
    
    # Security for AI Systems
    {
        "id": 7,
        "question": "A company is concerned about prompt injection attacks against their generative AI application built using Amazon Bedrock. Which security approach would be most effective in mitigating this risk?",
        "options": {
            "A": "Rely on Amazon Macie to detect sensitive data patterns in the prompt inputs",
            "B": "Implement prompt filtering, sanitization, and validation before sending inputs to the model",
            "C": "Use AWS CloudTrail to log all prompts for future forensic analysis",
            "D": "Deploy the application in a dedicated VPC with no internet access"
        },
        "correct_answer": "B",
        "explanation": {
            "A": "Amazon Macie is designed to detect sensitive data in S3 buckets, not to prevent prompt injection attacks in real-time.",
            "B": "Correct! Prompt filtering, sanitization, and validation directly address prompt injection risks by preventing malicious inputs from reaching the model in the first place, following the security best practice of validating all inputs.",
            "C": "While logging is important for security, it's a detective control rather than a preventive one and doesn't actively mitigate prompt injection attacks.",
            "D": "Network isolation doesn't address prompt injection attacks, which occur at the application layer through legitimate communication channels."
        },
        "category": "Security for AI Systems"
    },
    {
        "id": 8,
        "question": "A company is storing sensitive customer data for training their machine learning models. Which combination of AWS services provides the most comprehensive protection for this data?",
        "options": {
            "A": "Amazon S3 with server-side encryption and Amazon Inspector for vulnerability scanning",
            "B": "AWS Key Management Service (KMS) for encryption key management and AWS CloudTrail for logging API calls",
            "C": "Amazon S3 with server-side encryption, AWS KMS for key management, Amazon Macie for sensitive data discovery, and AWS IAM for access control",
            "D": "Amazon EC2 with encrypted EBS volumes and security groups to restrict network access"
        },
        "correct_answer": "C",
        "explanation": {
            "A": "While S3 encryption is important, Amazon Inspector is focused on EC2 vulnerability assessment and doesn't help with data protection in S3.",
            "B": "KMS and CloudTrail are important components but lack data discovery and fine-grained access controls specific to the data.",
            "C": "Correct! This comprehensive approach combines encryption (S3 + KMS), sensitive data discovery (Macie), and access control (IAM) to protect data at rest, identify sensitive information, and enforce least privilege access.",
            "D": "EC2 with encrypted EBS is less suitable for large-scale data storage for ML than S3, and security groups only address network-level protection."
        },
        "category": "Security for AI Systems"
    },
    {
        "id": 9,
        "question": "A data science team is building an ML model using Amazon SageMaker that requires access to sensitive financial data stored in Amazon S3. Which approach provides the most secure access following the principle of least privilege?",
        "options": {
            "A": "Create a single IAM role for the entire data science team with permissions to access all S3 buckets",
            "B": "Use AWS SageMaker Role Manager to define custom roles with minimum necessary permissions for specific ML activities",
            "C": "Provide the team with administrative access to simplify development and improve productivity",
            "D": "Create shared IAM access keys that the team can use to access the required resources"
        },
        "correct_answer": "B",
        "explanation": {
            "A": "A single role for the entire team violates the principle of least privilege by providing broader access than necessary for individual tasks.",
            "B": "Correct! SageMaker Role Manager allows you to define minimum necessary permissions for specific ML activities, following the principle of least privilege by providing only the access needed for specific tasks.",
            "C": "Administrative access significantly violates the principle of least privilege and creates unnecessary security risks.",
            "D": "Shared access keys violate security best practices by making access tracking difficult and increasing the risk of credential exposure."
        },
        "category": "Security for AI Systems"
    },
    
    # Compliance Regulations for AI
    {
        "id": 10,
        "question": "A global company is deploying an AI system that processes customer data across multiple regions. They need to ensure compliance with different regulatory frameworks. Which approach best addresses this complexity?",
        "options": {
            "A": "Apply the least restrictive regulations to all operations to minimize overhead",
            "B": "Focus compliance efforts only on the region with the strictest regulations",
            "C": "Use AWS Artifact to access compliance reports and AWS Config to continuously monitor resource compliance across regions",
            "D": "Create separate, independently managed systems for each region with no centralized governance"
        },
        "correct_answer": "C",
        "explanation": {
            "A": "Applying only the least restrictive regulations would likely violate requirements in regions with stricter controls, creating legal risks.",
            "B": "Focusing only on the strictest region ignores region-specific requirements that may differ qualitatively, not just in strictness.",
            "C": "Correct! AWS Artifact provides access to compliance reports for different regulatory frameworks, while AWS Config enables continuous monitoring of resource configurations against compliance rules across regions, supporting comprehensive compliance management.",
            "D": "Completely independent systems without centralized governance would create inconsistencies and inefficiencies in compliance management."
        },
        "category": "Compliance Regulations for AI"
    },
    {
        "id": 11,
        "question": "A company wants to implement algorithm accountability for their AI system used in hiring decisions. Which approach would best satisfy regulatory requirements for transparency and fairness?",
        "options": {
            "A": "Keep the algorithm proprietary and confidential to protect the company's intellectual property",
            "B": "Document model information with Amazon SageMaker Model Cards and implement bias detection with SageMaker Clarify",
            "C": "Use the most sophisticated deep learning techniques available to maximize accuracy",
            "D": "Outsource the development and deployment to avoid direct accountability"
        },
        "correct_answer": "B",
        "explanation": {
            "A": "Keeping algorithms proprietary and confidential contradicts accountability principles and may violate regulatory requirements for hiring systems.",
            "B": "Correct! SageMaker Model Cards provide documentation of model information (intended use, performance, limitations), while SageMaker Clarify enables bias detection and explainability—both essential for algorithm accountability in sensitive domains like hiring.",
            "C": "Sophisticated techniques that prioritize accuracy over explainability may create 'black box' systems that fail accountability requirements.",
            "D": "Outsourcing development doesn't eliminate accountability obligations and may actually make compliance more difficult."
        },
        "category": "Compliance Regulations for AI"
    },
    {
        "id": 12,
        "question": "A financial services company is implementing a data governance strategy for their AI systems. Which approach best addresses both regulatory compliance and operational efficiency?",
        "options": {
            "A": "Store all data in a single repository to simplify access for AI practitioners",
            "B": "Implement minimum data governance controls to avoid hampering innovation speed",
            "C": "Implement data quality standards, data protection measures, and clear roles for data stewards using AWS services like AWS KMS, Amazon Macie, and AWS IAM",
            "D": "Focus exclusively on compliance documentation without modifying existing data workflows"
        },
        "correct_answer": "C",
        "explanation": {
            "A": "Storing all data in a single repository creates security risks and doesn't address data quality or protection requirements.",
            "B": "Minimal governance controls risk regulatory non-compliance and data quality issues that could affect AI model performance.",
            "C": "Correct! A comprehensive approach that includes data quality standards, protection measures (KMS, Macie), and clear governance roles addresses both compliance requirements and ensures data integrity for AI systems.",
            "D": "Documentation without workflow changes creates a 'paper compliance' situation that doesn't actually improve governance."
        },
        "category": "Compliance Regulations for AI"
    },
    
    # Governance for AI Systems
    {
        "id": 13,
        "question": "A company has deployed multiple machine learning models across different business units and needs to implement comprehensive monitoring. Which AWS service combination provides the most complete governance solution?",
        "options": {
            "A": "Amazon CloudWatch for basic metrics and Amazon Comprehend for model analysis",
            "B": "AWS Systems Manager for infrastructure management and AWS Lambda for custom monitoring scripts",
            "C": "Amazon SageMaker Model Dashboard for unified model monitoring, combined with SageMaker Model Monitor for drift detection and SageMaker Clarify for bias monitoring",
            "D": "Amazon QuickSight for visualization and Amazon SNS for alert notifications"
        },
        "correct_answer": "C",
        "explanation": {
            "A": "CloudWatch provides basic metrics but lacks ML-specific monitoring capabilities, and Comprehend is an NLP service, not a monitoring solution.",
            "B": "Systems Manager and Lambda could implement custom monitoring but lack built-in capabilities for ML-specific concerns like drift and bias.",
            "C": "Correct! This combination provides comprehensive ML governance with SageMaker Model Dashboard offering unified visibility into all models, Model Monitor detecting data and model quality drift, and Clarify monitoring for bias and feature attribution drift.",
            "D": "QuickSight and SNS are useful components but lack the ML-specific monitoring capabilities required for comprehensive governance."
        },
        "category": "Governance for AI Systems"
    },
    {
        "id": 14,
        "question": "An organization wants to ensure their foundation model deployment follows the AWS Generative AI Security Scoping Matrix guidelines. Their use case involves fine-tuning an Amazon Bedrock model on their sensitive customer data. Which scope should they consider and what security measures are most critical?",
        "options": {
            "A": "Scope 1 (Consumer App), focusing on network security and end-to-end encryption",
            "B": "Scope 4 (Fine-tuned Models), emphasizing data governance, privacy controls, and model access restrictions using AWS IAM",
            "C": "Scope 2 (Enterprise App), focusing primarily on application-level security measures",
            "D": "Scope 3 (Pre-trained Models), focusing on prompt injection prevention only"
        },
        "correct_answer": "B",
        "explanation": {
            "A": "Scope 1 applies to using public generative AI services, not fine-tuning models on sensitive data.",
            "B": "Correct! Scope 4 (Fine-tuned Models) is appropriate when customizing models with your own data. Given the sensitive nature of customer data, data governance, privacy controls, and access restrictions using IAM are indeed the most critical security concerns.",
            "C": "Scope 2 applies to using applications or SaaS with generative AI features, not fine-tuning your own models.",
            "D": "Scope 3 applies to building on versioned pre-trained models without customization, which doesn't match the described scenario."
        },
        "category": "Governance for AI Systems"
    },
    {
        "id": 15,
        "question": "A company is implementing ML governance for their Amazon SageMaker environment with multiple data scientists creating various models. They need to maintain comprehensive visibility of model activity. Which approach best satisfies this requirement?",
        "options": {
            "A": "Rely on manual documentation processes where each data scientist records their model information in a shared document",
            "B": "Configure CloudWatch to collect basic metrics from SageMaker endpoints",
            "C": "Implement a custom solution using SageMaker notebooks to track model development",
            "D": "Use Amazon SageMaker Model Dashboard for visibility into deployed models and endpoints, and configure AWS CloudTrail to log API calls with SageMaker"
        },
        "correct_answer": "D",
        "explanation": {
            "A": "Manual documentation is error-prone, inconsistent, and doesn't provide real-time visibility into model activity.",
            "B": "CloudWatch metrics provide operational monitoring but lack comprehensive governance capabilities for ML models.",
            "C": "Custom solutions in notebooks would require significant development effort and likely lack standardization across teams.",
            "D": "Correct! SageMaker Model Dashboard provides unified visibility into deployed models and endpoints, while CloudTrail logs API calls, creating a comprehensive audit trail of model-related activities for governance purposes."
        },
        "category": "Governance for AI Systems"
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
        num_questions = st.slider("Number of Questions", min_value=5, max_value=15, value=st.session_state.total_questions, step=1)
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
        st.markdown("<p style='text-align:center'>Domain 4 & 5: Responsible AI, Security, and Governance</p>", unsafe_allow_html=True)
    
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
