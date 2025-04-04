
import streamlit as st
import json
import pandas as pd
import uuid
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="AWS Certification Practice",
    page_icon="☁️",
    layout="wide"
)

# Initialize session state variables
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'question_history' not in st.session_state:
    st.session_state.question_history = []
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "practice"  # Options: "practice", "review"

# AWS Exam questions data
questions = [
    {
        "id": 1,
        "question": "A company needs to maintain access logs for a minimum of 5 years due to regulatory requirements. The data is rarely accessed once stored, but must be accessible with one day's notice if it is needed. What is the MOST cost-effective data storage solution that meets these requirements?",
        "options": {
            "A": "Store the data in Amazon S3 Glacier Deep Archive storage and delete the objects after 5 years using a lifecycle rule.",
            "B": "Store the data in Amazon S3 Standard storage and transition to Amazon S3 Glacier after 30 days using a lifecycle rule.",
            "C": "Store the data in logs using Amazon CloudWatch Logs and set the retention period to 5 years.",
            "D": "Store the data in Amazon S3 Standard-Infrequent Access (S3 Standard-IA) storage and delete the objects after 5 years using a lifecycle rule."
        },
        "correct_answer": "A",
        "explanation": {
            "A": "Correct! Amazon S3 Glacier Deep Archive is indeed the most cost-effective storage class for long-term data archiving with very infrequent access needs. It's designed for data that might be accessed once or twice a year and can be retrieved within 12 hours for standard retrieval or 48 hours for bulk retrieval. This meets the requirement of access within one day's notice. S3 Glacier Deep Archive has the lowest storage cost among S3 storage classes, offers 11 9's of durability, and is ideal for regulatory archive requirements.",
            "B": "Incorrect. Transitioning is unnecessary because the data is rarely accessed once stored. Direct storage in Glacier Deep Archive is more cost-effective than using lifecycle policies to transition from other storage classes.",
            "C": "Incorrect. CloudWatch Logs are not designed for long-term data storage of this nature. While CloudWatch Logs can be used for storing and analyzing log data, it's primarily for operational and application logs, not for long-term regulatory compliance storage.",
            "D": "Incorrect. S3 Standard-Infrequent Access (S3 Standard-IA) is designed for data that is accessed less frequently but requires rapid access when needed. While it would work for this scenario, it's not the most cost-effective option for data that is rarely accessed. S3 Standard-IA has higher storage costs but lower retrieval costs compared to Glacier Deep Archive, and offers millisecond retrieval times, which is unnecessary for this use case."
        },
        "category": "Storage"
    },
    {
        "id": 2,
        "question": "A company uses Reserved Instances to run its data-processing workload. The nightly job typically takes 7 hours to run and must finish within a 10-hour time window. The company anticipates temporary increases in demand at the end of each month that will cause the job to run over the time limit with the capacity of the current resources. Once started, the processing job cannot be interrupted before completion. The company wants to implement a solution that would allow it to provide increased capacity as cost-effectively as possible. What should a solutions architect do to accomplish this?",
        "options": {
            "A": "Deploy On-Demand Instances during periods of high demand.",
            "B": "Create a second Amazon EC2 reservation for additional instances.",
            "C": "Deploy Spot Instances during periods of high demand.",
            "D": "Increase the instance size of the instances in the Amazon EC2 reservation to support the increased workload."
        },
        "correct_answer": "A",
        "explanation": {
            "A": "Correct! On-Demand Instances are the most suitable option for this scenario because: (1) They provide flexibility to scale up during periods of high demand. (2) They are billed per second, allowing for cost-effective use during short periods of increased capacity needs. (3) They can be started and stopped as needed without long-term commitments. (4) They guarantee the availability of the instance for the duration of the job, unlike Spot Instances.",
            "B": "Incorrect. Reserved Instances are not suitable for handling temporary increases in demand because they require a long-term commitment (1 or 3 years), are best for predictable, steady-state workloads, and don't provide the flexibility needed for temporary capacity increases.",
            "C": "Incorrect. Spot Instances are not appropriate for this scenario because they can be interrupted with only 2 minutes notice if AWS needs the capacity back. The job cannot be interrupted once started and must complete within a specific time window.",
            "D": "Incorrect. Increasing the size of Reserved Instances is not the best solution because it would result in unused capacity for most of the month, Reserved Instances are region-specific and instance type-specific, limiting flexibility, and vertical scaling may not always be the most cost-effective or efficient solution compared to horizontal scaling (adding more instances)."
        },
        "category": "Compute"
    },
    {
        "id": 3,
        "question": "A solutions architect wants to design a solution to save costs for Amazon EC2 instances that do not need to run during a 2-week company shutdown. The applications running on the EC2 instances store data in instance memory that must be present when the instances resume operation. Which approach should the solutions architect recommend to shut down and resume the EC2 instances?",
        "options": {
            "A": "Modify the application to store the data on instance store volumes. Reattach the volumes while restarting them.",
            "B": "Snapshot the EC2 instances before stopping them. Restore the snapshot after restarting the instances.",
            "C": "Run the applications on EC2 instances enabled for hibernation. Hibernate the instances before the 2-week company shutdown.",
            "D": "Note the Availability Zone for each EC2 instance before stopping it. Restart the instances in the same Availability Zones after the 2-week company shutdown."
        },
        "correct_answer": "C",
        "explanation": {
            "A": "Incorrect. Using instance store is not suitable because: (1) Instance store provides temporary block-level storage for EC2 instances. (2) Data in instance store is lost when the instance is stopped or terminated. (3) It doesn't preserve the contents of instance memory (RAM).",
            "B": "Incorrect. Creating an EBS snapshot is not the best solution because: (1) EBS snapshots capture the data on the EBS volume, not the contents of instance memory. (2) While useful for backup and disaster recovery, snapshots don't preserve the running state of the instance. (3) Restoring from a snapshot would require a full instance restart, not just resuming the previous state.",
            "C": "Correct! EC2 Hibernation is the most suitable option for this scenario because: (1) It saves the contents of instance memory (RAM) to the EBS root volume. (2) When instances are restarted, the memory contents are reloaded, preserving the application state. (3) It allows for quick resumption of operations after the shutdown period. (4) It saves costs by not running the instances during the shutdown while still preserving the necessary data.",
            "D": "Incorrect. Simply restarting the instances in the same Availability Zone would not preserve the instance memory contents because: (1) A standard restart clears the instance memory. (2) Applications would need to reload all data and restart processes. (3) It doesn't provide any cost savings during the shutdown period."
        },
        "category": "Compute"
    },
    {
        "id": 4,
        "question": "A company has a two-tier application architecture that runs in public and private subnets. Amazon EC2 instances running the web application are in the public subnet and an EC2 instance for the database runs on the private subnet. The web application instances and the database are running in a single Availability Zone (AZ). Which combination of steps should a solutions architect take to provide high availability for this architecture? (Select TWO.)",
        "options": {
            "A": "Create new public and private subnets in the same AZ.",
            "B": "Create an Amazon EC2 Auto Scaling group and Application Load Balancer spanning multiple AZs for the web application instances.",
            "C": "Add the existing web application instances to an Auto Scaling group behind an Application Load Balancer.",
            "D": "Create new public and private subnets in a new AZ. Create a database using an EC2 instance in the public subnet in the new AZ. Migrate the old database contents to the new database.",
            "E": "Create new public and private subnets in the same VPC, each in a new AZ. Create an Amazon RDS Multi-AZ DB instance in the private subnets. Migrate the old database contents to the new DB instance."
        },
        "correct_answer": ["B", "E"],
        "multi_select": True,
        "explanation": {
            "A": "Incorrect. Creating new subnets in the same AZ doesn't improve availability as it doesn't protect against AZ-level failures.",
            "B": "Correct! Creating an EC2 Auto Scaling group with an Application Load Balancer (ALB) across multiple AZs provides high availability for the web tier by automatically scaling EC2 instances based on demand, distributing traffic across multiple instances and AZs, and replacing unhealthy instances automatically.",
            "C": "Incorrect. While adding existing instances to an Auto Scaling group and ALB is a step in the right direction, it doesn't address the single AZ limitation.",
            "D": "Incorrect. Creating a database in a public subnet is not a security best practice. Databases should be kept in private subnets for better security.",
            "E": "Correct! Creating new subnets in different AZs and using Amazon RDS Multi-AZ provides high availability for the database tier by replicating data synchronously to a standby instance in a different AZ, enabling automatic failover in case of infrastructure failure, and allowing the database to span multiple AZs."
        },
        "category": "High Availability"
    },
    {
        "id": 5,
        "question": "A company has an on-premises application that exports log files about users of a website. These log files range from 20 GB to 30 GB in size. A solutions architect has created an Amazon S3 bucket to store these files. The files will be uploaded directly from the application. The network connection experiences intermittent failures, and the upload sometimes fails. A solutions architect must design a solution that resolves this problem. The solution must minimize operational overhead. Which solution will meet these requirements?",
        "options": {
            "A": "Copy the files to an Amazon EC2 instance in the closest AWS Region. Use S3 Lifecycle policies to copy the log files to Amazon S3.",
            "B": "Enable S3 Transfer Acceleration to handle the file exports.",
            "C": "Upload the files to two AWS Regions simultaneously. Enable two-way Cross-Region Replication between the Two Regions.",
            "D": "Use multipart upload to S3 to handle the file exports."
        },
        "correct_answer": "D",
        "explanation": {
            "A": "Incorrect. Using Amazon EC2 instances with S3 lifecycle policies is not suitable because it introduces unnecessary complexity and operational overhead, S3 lifecycle policies can't transfer files from EC2 block storage to S3, and it doesn't address the core issue of uploading large files over unreliable networks.",
            "B": "Incorrect. S3 Transfer Acceleration is not the best solution because it doesn't solve the 5 GB file size limitation for a single PUT operation, and while it can speed up transfers, it doesn't address the issue of interrupted uploads.",
            "C": "Incorrect. Configuring S3 replication to copy the files to multiple destination Regions is not appropriate because it doesn't solve the initial upload problem, each destination region would face the same upload issues, and it adds unnecessary complexity and cost.",
            "D": "Correct! S3 multipart upload is the most suitable option for this scenario because it allows uploading of large objects (up to 5 TB) in parts, provides the ability to pause and resume uploads (crucial for handling network failures), improves throughput by uploading parts in parallel, and doesn't require any additional services or infrastructure, minimizing operational overhead."
        },
        "category": "Storage"
    }
]

# Define CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF9900;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #232F3E;
        margin-bottom: 1rem;
    }
    .question-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .option-button {
        width: 100%;
        text-align: left;
        margin: 5px;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    .option-button:hover {
        background-color: #f5f5f5;
    }
    .selected-option {
        background-color: #e6f7ff;
        border-color: #1890ff;
    }
    .correct-option {
        background-color: #d4edda;
        border-color: #28a745;
    }
    .incorrect-option {
        background-color: #f8d7da;
        border-color: #dc3545;
    }
    .footer {
        text-align: center;
        margin-top: 20px;
        color: #666;
    }
    .progress-container {
        margin: 20px 0;
    }
    .explanation-box {
        padding: 15px;
        border-radius: 5px;
        background-color: #f0f8ff;
        margin-top: 15px;
    }
    .category-tag {
        background-color: #232F3E;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        margin-right: 5px;
        display: inline-block;
    }
    .metrics-card {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
        border-left: 4px solid #FF9900;
    }
    .tab-container {
        margin-bottom: 20px;
    }
    .button-primary {
        background-color: #FF9900;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        margin: 5px;
    }
    .button-secondary {
        background-color: #232F3E;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Navigation functions
def go_to_next_question():
    if st.session_state.current_question_index < len(questions) - 1:
        st.session_state.current_question_index += 1

def go_to_previous_question():
    if st.session_state.current_question_index > 0:
        st.session_state.current_question_index -= 1

def go_to_question(index):
    if 0 <= index < len(questions):
        st.session_state.current_question_index = index

# Main application
def main():
    # Header
    st.markdown("<h1 class='main-header'>AWS Certification Exam Practice</h1>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://d1.awsstatic.com/training-and-certification/certification-badges/AWS-Certified-Solutions-Architect-Associate_badge.3419559c682629072f1eb968d59dea0741772c0f.png", width=200)
        st.markdown("### Your Progress")
        
        # Calculate progress
        progress = (len(st.session_state.answers) / len(questions)) * 100
        st.progress(progress / 100)
        st.write(f"Completed: {int(progress)}%")
        
        # Display score
        correct_count = sum(1 for q_id, answer in st.session_state.answers.items() 
                          if (isinstance(questions[int(q_id)-1]["correct_answer"], list) and 
                              set(answer) == set(questions[int(q_id)-1]["correct_answer"])) or 
                          (not isinstance(questions[int(q_id)-1]["correct_answer"], list) and 
                           answer == questions[int(q_id)-1]["correct_answer"]))
        
        if len(st.session_state.answers) > 0:
            accuracy = (correct_count / len(st.session_state.answers)) * 100
            st.write(f"Current Score: {correct_count}/{len(st.session_state.answers)} ({int(accuracy)}%)")
        
        # Filter by category
        st.markdown("### Filter Questions")
        categories = sorted(list(set([q.get("category", "Uncategorized") for q in questions])))
        selected_category = st.selectbox("Select a category", ["All"] + categories)
        
        # View mode selection
        st.markdown("### Study Mode")
        view_mode_options = {
            "practice": "Practice Mode",
            "review": "Review Answers"
        }
        selected_mode = st.radio("Select mode", list(view_mode_options.keys()), format_func=lambda x: view_mode_options[x])
        
        if st.session_state.view_mode != selected_mode:
            st.session_state.view_mode = selected_mode
        
        # Navigation
        st.markdown("### Actions")
        if st.button("Reset Progress", key="reset"):
            reset_session()
        
        # Question selector
        filtered_questions = questions
        if selected_category != "All":
            filtered_questions = [q for q in questions if q.get("category", "Uncategorized") == selected_category]
        
        question_options = [f"Question {q['id']}" for q in filtered_questions]
        if question_options:
            selected_question = st.selectbox(
                "Jump to question:",
                question_options,
                index=min(st.session_state.current_question_index, len(question_options)-1)
            )
            if selected_question:
                q_num = int(selected_question.split()[1])
                # Find the index of the question in the full questions list
                q_index = next((i for i, q in enumerate(questions) if q["id"] == q_num), 0)
                if st.button("Go to Selected Question"):
                    go_to_question(q_index)
        else:
            st.write("No questions in this category.")
    
    # Main content
    # Tabs
    tab1, tab2 = st.tabs(["Practice Questions", "Your Stats"])
    
    with tab1:
        display_question(st.session_state.current_question_index)

        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.session_state.current_question_index > 0:
                if st.button("⬅️ Previous", key="prev_btn"):
                    go_to_previous_question()
                    st.rerun()
                    
        with col3:
            if st.session_state.current_question_index < len(questions) - 1:
                if st.button("Next ➡️", key="next_btn"):
                    go_to_next_question()
                    st.rerun()
    
    with tab2:
        display_stats()
    
    # Footer
    st.markdown("<div class='footer'>© 2023 AWS Certification Practice. Created for learning purposes.</div>", unsafe_allow_html=True)

# Display a question
def display_question(q_index):
    question = questions[q_index]
    q_id = str(question["id"])
    multi_select = question.get("multi_select", False)
    
    st.markdown(f"<div class='question-card'>", unsafe_allow_html=True)
    
    # Display category tag if available
    category = question.get("category", "Uncategorized")
    st.markdown(f"<span class='category-tag'>{category}</span>", unsafe_allow_html=True)
    
    st.markdown(f"<h2 class='sub-header'>Question {question['id']}</h2>", unsafe_allow_html=True)
    st.write(question["question"])
    
    user_answered = q_id in st.session_state.answers
    
    if multi_select:
        # For multi-select questions
        options = []
        for option_key, option_text in question["options"].items():
            if user_answered or st.session_state.view_mode == "review":
                is_correct = option_key in question["correct_answer"]
                user_selected = q_id in st.session_state.answers and option_key in st.session_state.answers[q_id]
                
                if user_selected and is_correct:
                    st.success(f"{option_key}: {option_text}")
                elif user_selected and not is_correct:
                    st.error(f"{option_key}: {option_text}")
                elif not user_selected and is_correct:
                    st.warning(f"{option_key}: {option_text}")
                else:
                    st.write(f"{option_key}: {option_text}")
            else:
                options.append(option_key)
        
        if not user_answered and st.session_state.view_mode == "practice":
            selected_options = st.multiselect(
                "Select all that apply:",
                options,
                format_func=lambda x: f"{x}: {question['options'][x]}"
            )
            if st.button("Submit", key=f"submit_{q_id}"):
                st.session_state.answers[q_id] = selected_options
                record_answer(q_id, selected_options)
                st.rerun()
    else:
        # For single-select questions
        for option_key, option_text in question["options"].items():
            if user_answered or st.session_state.view_mode == "review":
                is_correct = option_key == question["correct_answer"]
                user_selected = q_id in st.session_state.answers and option_key == st.session_state.answers[q_id]
                
                if user_selected and is_correct:
                    st.success(f"{option_key}: {option_text}")
                elif user_selected and not is_correct:
                    st.error(f"{option_key}: {option_text}")
                elif not user_selected and is_correct and st.session_state.view_mode == "review":
                    st.warning(f"{option_key}: {option_text}")
                else:
                    st.write(f"{option_key}: {option_text}")
            elif st.session_state.view_mode == "practice":
                if st.button(f"{option_key}: {option_text}", key=f"option_{q_id}_{option_key}"):
                    st.session_state.answers[q_id] = option_key
                    record_answer(q_id, option_key)
                    st.rerun()
    
    # Display explanation if the user has answered or in review mode
    if user_answered or st.session_state.view_mode == "review":
        st.markdown("<div class='explanation-box'>", unsafe_allow_html=True)
        st.markdown("### Explanation")
        
        if q_id in st.session_state.answers:
            user_answer = st.session_state.answers[q_id]
            
            if multi_select:
                for option in user_answer:
                    st.markdown(f"**Option {option}**: {question['explanation'][option]}")
                
                # Show explanations for correct answers that weren't selected
                for correct_option in question["correct_answer"]:
                    if correct_option not in user_answer:
                        st.markdown(f"**Option {correct_option}** (Missed): {question['explanation'][correct_option]}")
            else:
                st.markdown(f"**Your answer** (Option {user_answer}): {question['explanation'][user_answer]}")
                
                # If incorrect, show the correct answer explanation
                if user_answer != question["correct_answer"]:
                    correct = question["correct_answer"]
                    st.markdown(f"**Correct answer** (Option {correct}): {question['explanation'][correct]}")
        else:
            # Just show all explanations in review mode
            for option_key, explanation in question["explanation"].items():
                is_correct = (isinstance(question["correct_answer"], list) and option_key in question["correct_answer"]) or option_key == question["correct_answer"]
                st.markdown(f"**Option {option_key}** {'✓' if is_correct else '✗'}: {explanation}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Question counter
    st.write(f"Question {st.session_state.current_question_index + 1} of {len(questions)}")

# Display statistics
def display_stats():
    st.markdown("<h2 class='sub-header'>Your Performance</h2>", unsafe_allow_html=True)
    
    if not st.session_state.question_history:
        st.info("You haven't answered any questions yet. Start practicing to see your stats!")
        return
    
    # Overall statistics
    total_answered = len(set(item["question_id"] for item in st.session_state.question_history))
    total_correct = sum(1 for item in st.session_state.question_history if item["correct"])
    
    if total_answered > 0:
        accuracy = (total_correct / total_answered) * 100
    else:
        accuracy = 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Questions Answered", total_answered)
    with col2:
        st.metric("Correct Answers", total_correct)
    with col3:
        st.metric("Accuracy", f"{accuracy:.1f}%")
    
    # Category performance
    st.markdown("### Performance by Category")
    
    # Group answers by category
    category_performance = {}
    for item in st.session_state.question_history:
        q_id = int(item["question_id"]) - 1
        category = questions[q_id].get("category", "Uncategorized")
        
        if category not in category_performance:
            category_performance[category] = {"correct": 0, "total": 0}
        
        category_performance[category]["total"] += 1
        if item["correct"]:
            category_performance[category]["correct"] += 1
    
    # Create and display a DataFrame for category performance
    if category_performance:
        data = []
        for category, stats in category_performance.items():
            accuracy = (stats["correct"] / stats["total"]) * 100 if stats["total"] > 0 else 0
            data.append({
                "Category": category,
                "Questions Answered": stats["total"],
                "Correct": stats["correct"],
                "Accuracy": f"{accuracy:.1f}%"
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    
    # Recently answered questions
    st.markdown("### Recently Answered Questions")
    recent_answers = st.session_state.question_history[-5:][::-1]  # Last 5 answers in reverse order
    
    for item in recent_answers:
        q_id = int(item["question_id"]) - 1
        question_index = next((i for i, q in enumerate(questions) if str(q["id"]) == item["question_id"]), 0)
        question = questions[question_index]
        
        with st.expander(f"Q{item['question_id']}: {question['question'][:100]}..."):
            st.write(f"**Your answer:** {item['answer']}")
            st.write(f"**Correct:** {'✓' if item['correct'] else '✗'}")
            st.write(f"**Time:** {item['timestamp']}")
            
            if st.button("Review Question", key=f"review_{item['question_id']}"):
                go_to_question(question_index)
                st.rerun()

# Record answer in history
def record_answer(question_id, answer):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    question_index = next((i for i, q in enumerate(questions) if str(q["id"]) == question_id), 0)
    question = questions[question_index]
    
    if isinstance(question["correct_answer"], list):
        is_correct = set(answer) == set(question["correct_answer"])
    else:
        is_correct = answer == question["correct_answer"]
    
    record = {
        "question_id": question_id,
        "answer": answer,
        "correct": is_correct,
        "timestamp": timestamp
    }
    
    st.session_state.question_history.append(record)

# Reset session
def reset_session():
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.answers = {}
    st.session_state.question_history = []

if __name__ == "__main__":
    main()