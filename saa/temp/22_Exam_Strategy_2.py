
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
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
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
        "question": "A company is experiencing problems with its message-processing application. During periods of high demand, the application becomes overloaded. The application is based on a monolithic design and is hosted in an on-premises data center. The company wants to move the application to the AWS Cloud and decouple the monolithic architecture. A solutions architect must design a solution that allows worker components of the application to access the messages and handle the peak volume. Which solution meets these requirements with the HIGHEST throughput?",
        "options": {
            "A": "Use a Network Load Balancer with target groups that are configured to perform the path-based routing to Amazon EC2 instances.",
            "B": "Use Amazon Simple Queue Service (Amazon SQS) FIFO queues in combination with Amazon EC2 instances that are scaled by an Auto Scaling group.",
            "C": "Use an Application Load Balancer with target groups that are configured to perform path-based routing to Amazon EC2 instances.",
            "D": "Use Amazon Simple Queue Service (Amazon SQS) standard queues in combination with Amazon EC2 instances that are scaled by an Auto Scaling group."
        },
        "correct_answer": "D",
        "explanation": {
            "A": "Incorrect. Network Load Balancers operate at the transport layer (Layer 4) and don't support path-based routing. Additionally, it doesn't address the decoupling of the monolithic architecture or provide a mechanism for handling message backlogs during peak periods.",
            "B": "Incorrect. While this solution is close to the correct answer, it's not the best for highest throughput. FIFO queues have a limit of 300 messages per second (or 3,000 with batching). FIFO queues guarantee exactly-once processing and strict ordering, which aren't necessary for this scenario and can limit throughput.",
            "C": "Incorrect. While ALBs support path-based routing, they don't provide a mechanism for message queueing. It doesn't effectively decouple the components of the monolithic application or provide a buffer for handling peak loads.",
            "D": "Correct! SQS standard queues offer nearly unlimited throughput, which is crucial for handling peak volumes. This solution effectively decouples the components of the monolithic application. Auto Scaling groups allow the system to automatically adjust the number of EC2 instances based on demand, providing a scalable, fault-tolerant, and highly available solution."
        },
        "category": "Messaging"
    },
    {
        "id": 2,
        "question": "A company is deploying a new application that will consist of an application layer and an online transaction processing (OLTP) relational database. The application must be available at all times. However, the application will have periods of inactivity. The company wants to pay the minimum for compute costs during these idle periods. Which solution meets these requirements MOST cost-effectively?",
        "options": {
            "A": "Run the application in containers with Amazon Elastic Container Service (ECS) on AWS Fargate. Use Amazon Aurora Serverless for the database.",
            "B": "Deploy the application and a MySQL database to Amazon EC2 instances by using AWS CloudFormation. Delete the stack at the beginning of the idle periods.",
            "C": "Deploy the application on Amazon EC2 instances in an Auto Scaling group behind an Application Load Balancer. Use Amazon RDS for MySQL for the database.",
            "D": "Run the application on Amazon EC2 instances by using a burstable instance type. Use Amazon Redshift for the database."
        },
        "correct_answer": "A",
        "explanation": {
            "A": "Correct! AWS Fargate allows you to run containers without managing servers, paying only for the compute resources used. ECS with Fargate can scale down to zero during idle periods, minimizing costs. Aurora Serverless automatically scales compute capacity based on application demand, including scaling to zero during idle periods. Both components maintain availability while minimizing costs during inactivity.",
            "B": "Incorrect. Deleting and recreating the stack doesn't meet the 'always available' requirement. It introduces operational overhead and potential for errors in managing the stack. There might be data loss risks associated with frequently deleting and recreating the database.",
            "C": "Incorrect. While this is a scalable solution, it's not the most cost-effective for periods of inactivity. EC2 instances in an Auto Scaling group typically have a minimum instance count, incurring costs even during idle periods. RDS for MySQL doesn't have the ability to scale to zero during idle periods.",
            "D": "Incorrect. While burstable instances can be cost-effective, they still incur costs during idle periods. Amazon Redshift is designed for data warehousing and analytics, not for OLTP workloads. Redshift doesn't have the ability to scale down to zero during idle periods."
        },
        "category": "Cost Optimization"
    },
    {
        "id": 3,
        "question": "A company is deploying a new database on a new Amazon EC2 instance. The workload of this database requires a single Amazon Elastic Block Store (Amazon EBS) volume that can support up to 20,000 IOPS. Which type of EBS volume meets this requirement?",
        "options": {
            "A": "Throughput Optimized HDD",
            "B": "General Purpose SSD",
            "C": "Provisioned IOPS SSD",
            "D": "Cold HDD"
        },
        "correct_answer": "C",
        "explanation": {
            "A": "Incorrect. Throughput Optimized HDD (st1) is designed for frequently accessed, throughput-intensive workloads. It can only provide up to 500 IOPS per volume, which is far below the required 20,000 IOPS. It's more suitable for big data, data warehouses, and log processing.",
            "B": "Incorrect. While General Purpose SSD can be suitable for many applications, it's not the best choice here. gp2 volumes can only provide up to 16,000 IOPS per volume. gp3 volumes can provide up to 16,000 IOPS, but require additional configuration. It may not provide the consistent performance needed for a high-IOPS database workload.",
            "C": "Correct! Provisioned IOPS SSD (io1/io2) is designed for I/O-intensive workloads, such as large databases, that require sustained IOPS performance. It allows you to provision a specific level of IOPS performance, up to 64,000 IOPS per volume. It provides the highest performance and lowest latency of any EBS volume type. It's ideal for applications that require consistent and predictable I/O performance.",
            "D": "Incorrect. Cold HDD (sc1) is designed for less frequently accessed workloads. It provides the lowest cost per GB of all EBS volume types but at the expense of performance. It can only deliver up to 250 IOPS per volume, far below the required 20,000 IOPS."
        },
        "category": "Storage"
    },
    {
        "id": 4,
        "question": "A company is developing a chat application that will be deployed on AWS. The application stores the messages by using a key-value data model. Groups of users typically read the messages multiple times. A solutions architect must select a database solution that will scale for a high rate of reads and will deliver messages with microsecond latency. Which database solution will meet these requirements?",
        "options": {
            "A": "Deploy Amazon Neptune with Amazon Elasticache for Memcached.",
            "B": "Deploy Amazon Aurora with Amazon ElastiCache for Memcached.",
            "C": "Deploy Amazon Aurora with Aurora Replicas to handle key pairs.",
            "D": "Deploy Amazon DynamoDB with DynamoDB Accelerator (DAX)."
        },
        "correct_answer": "D",
        "explanation": {
            "A": "Incorrect. Amazon Neptune is a graph database, which is not ideal for key-value data models. While ElastiCache can provide low latency, the combination with Neptune doesn't align with the key-value requirement.",
            "B": "Incorrect. Aurora is a relational database, which is not optimal for key-value data models. This combination might struggle to consistently deliver microsecond latency at scale.",
            "C": "Incorrect. Aurora is a relational database, not optimized for key-value data models. While Aurora Replicas can help with read scaling, they don't provide microsecond latency. This setup is more complex than necessary for the given requirements.",
            "D": "Correct! DynamoDB is a key-value and document database, perfectly matching the required data model. It provides single-digit millisecond performance at any scale. DAX is an in-memory cache for DynamoDB that reduces response times from milliseconds to microseconds. This combination can handle high read rates and frequent re-reading of data efficiently."
        },
        "category": "Database"
    },
    {
        "id": 5,
        "question": "A company asks a solutions architect to implement a pilot light disaster recovery (DR) strategy for an existing on-premises application. The application is self contained and does not need to access any databases. Which solution will implement a pilot light DR strategy?",
        "options": {
            "A": "Recreate the application hosting environment on AWS by using Amazon EC2 instances. Direct 10% of application traffic to the EC2 instances that are running in the AWS Cloud. When the on-premises application fails, direct 100% of application traffic to the EC2 instances that are running in the AWS Cloud.",
            "B": "Back up the on-premises application, configuration, and data to an Amazon S3 bucket. When the on-premises application fails, build a new hosting environment on AWS and restore the application from the information that is stored in the S3 bucket.",
            "C": "Recreate the application hosting environment on AWS by using Amazon EC2 instances and stop the EC2 instances. When the on-premises application fails, start the stopped EC2 instances and direct 100% of application traffic to the EC2 instances that are running in the AWS Cloud.",
            "D": "Back up the on-premises application, configuration, and data to an Amazon S3 bucket. When the on-premises application fails, rebuild the on-premises hosting environment and restore the application from the information that is stored in the S3 bucket."
        },
        "correct_answer": "C",
        "explanation": {
            "A": "Incorrect. This solution is not a pilot light strategy because it's actively serving traffic (10%) to the AWS environment. This approach is more aligned with an active-active or multi-site strategy.",
            "B": "Incorrect. This solution is not a pilot light strategy because it's more aligned with a backup and restore strategy. There's no pre-configured environment in AWS, leading to longer recovery times.",
            "C": "Correct! This solution aligns with the pilot light DR strategy because it maintains a minimal version of the environment always running in the cloud (the 'pilot light'). The core elements of the system are already configured and ready in AWS, but not actively serving traffic. It allows for quick recovery by simply starting the stopped EC2 instances when needed. It minimizes costs by keeping instances stopped when not in use.",
            "D": "Incorrect. This solution is not a pilot light strategy because it's a backup and restore strategy. It doesn't utilize AWS for disaster recovery, only for backup storage. Rebuilding the on-premises environment could lead to significant downtime."
        },
        "category": "Disaster Recovery"
    },
    {
        "id": 6,
        "question": "A company has an application that runs on a large general purpose Amazon EC2 instance type that is part of an EC2 Auto Scaling group. The company wants to reduce future costs associated with this application. After the company reviews metrics and logs in Amazon CloudWatch, the company notices that this application runs randomly a couple of times a day to retrieve and manage data. According to CloudWatch, the maximum runtime for each request is 10 minutes, the memory use is 4 GB, and the instances are always in the running state. Which solution will reduce costs the MOST?",
        "options": {
            "A": "Deploy the application on a large burstable EC2 instance",
            "B": "Refactor the application code to run as an AWS Lambda function",
            "C": "Containerize the application by using Amazon Elastic Kubernetes Service (EKS). Host the container on EC2 instances.",
            "D": "Use AWS Instance Scheduler to start and stop the instances based on the runtimes in the logs."
        },
        "correct_answer": "B",
        "explanation": {
            "A": "Incorrect. While burstable instances can be cost-effective for some workloads, this solution is not optimal because the instance would still be running and incurring costs even when the application is not in use. Given the infrequent usage, the cost savings from burst credits may not outweigh the costs of keeping the instance running continuously.",
            "B": "Correct! Lambda charges only for the compute time you consume, with no charge when your code is not running. Given the application's infrequent usage (a couple of times a day) and short runtime (max 10 minutes), Lambda would significantly reduce idle time costs. Lambda can easily handle the 4 GB memory requirement (up to 10 GB is supported). It eliminates the need for managing EC2 instances, reducing operational overhead.",
            "C": "Incorrect. This solution is not likely to reduce costs the most because it still requires running EC2 instances, which would incur costs even when the application is not in use. EKS adds additional complexity and potential costs for managing the Kubernetes cluster.",
            "D": "Incorrect. While this could reduce costs compared to running instances continuously, it's not likely to be the most cost-effective solution because there would still be some delay in starting and stopping instances, potentially leading to unnecessary runtime. The random nature of the application's usage might make scheduling less effective. It doesn't fully eliminate the costs associated with maintaining EC2 instances."
        },
        "category": "Cost Optimization"
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
    st.markdown("<div class='footer'>© 2025 AWS Certification Practice. Created for learning purposes.</div>", unsafe_allow_html=True)

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