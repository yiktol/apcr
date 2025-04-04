
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
        "question": "A company has many applications on Amazon EC2 instances running in Auto Scaling groups. Company policy requires that the data on the attached Amazon Elastic Block Store (Amazon EBS) volumes be retained. Which action will meet these requirements without impacting performance?",
        "options": {
            "A": "Enable termination protection on the Amazon EC2 instances.",
            "B": "Disable the DeleteOnTermination attribute for the Amazon EBS volumes",
            "C": "Use Amazon EC2 user data to set up a synchronization job for root volume data.",
            "D": "Change the Auto Scaling health check to point to a source on the root volume."
        },
        "correct_answer": "B",
        "explanation": {
            "A": "This solution is not appropriate because termination protection prevents instances from being manually terminated but doesn't prevent Auto Scaling from terminating instances. It could interfere with the normal operation of Auto Scaling groups, potentially impacting application availability and scalability.",
            "B": "Disabling the DeleteOnTermination attribute for EBS volumes is the most suitable solution because by default, EBS root volumes are set to be deleted when the EC2 instance is terminated. Disabling this attribute ensures that the EBS volume persists even after the instance is terminated by the Auto Scaling group. This approach doesn't impact the performance of the running instances and allows for easy data retention and recovery without interfering with Auto Scaling processes.",
            "C": "This solution is not optimal because it would likely impact performance by constantly synchronizing data. It adds complexity and potential points of failure to the system and doesn't directly address the requirement of retaining EBS volume data.",
            "D": "This solution doesn't address the data retention requirement because changing the health check doesn't affect what happens to the EBS volume when an instance is terminated. It could potentially interfere with proper Auto Scaling behavior if not implemented correctly."
        },
        "category": "EC2/EBS"
    },
    {
        "id": 2,
        "question": "A company plans to deploy a new application in the AWS Cloud. The application reads and writes information to a database. The company will deploy the application in two different AWS Regions, and each application will write to a database in its Region. The databases in the two Regions need to keep the data synchronized with minimal latency. The databases must be eventually consistent. In case of data conflict, queries should return the most recent write. Which solution will meet these requirements with the LEAST administrative work?",
        "options": {
            "A": "Use Amazon Athena with the data stored in Amazon S3 buckets in both regions. Use S3 Cross-Region Replication between the two S3 buckets.",
            "B": "Use AWS Database Migration Service (AWS DMS) change data capture (CDC) between an Amazon RDS for MySQL DB cluster in each region.",
            "C": "Use Amazon DynamoDB. Configure the table as a global table.",
            "D": "Use an Amazon RDS for PostgreSQL DB cluster with a cross-Region read replica."
        },
        "correct_answer": "C",
        "explanation": {
            "A": "This solution is not optimal because Athena is a query service for data in S3, not a database for frequent reads and writes. S3 Cross-Region Replication doesn't provide real-time synchronization or conflict resolution. It would require significant custom development to manage data consistency and conflicts.",
            "B": "While this could work, it's not the best solution because it requires more administrative work to set up and maintain DMS and RDS clusters. DMS is primarily designed for migration and ongoing replication, not for active-active multi-region setups. It would require additional effort to manage conflict resolution.",
            "C": "Using Amazon DynamoDB with global tables is the most suitable solution because DynamoDB global tables provide automatic multi-region replication with minimal latency. It offers eventual consistency by default, meeting the requirement. Global tables use a 'last writer wins' reconciliation between concurrent updates, satisfying the requirement for the most recent write in case of conflicts. It requires minimal administrative work as replication is managed automatically by AWS. It's a fully managed service, reducing operational overhead.",
            "D": "This solution doesn't fully meet the requirements because cross-region read replicas in RDS are read-only, not supporting writes in both regions. It doesn't provide a built-in mechanism for conflict resolution. It requires more administrative work compared to DynamoDB global tables."
        },
        "category": "Databases"
    },
    {
        "id": 3,
        "question": "An administrator wants to apply a resource-based policy to the S3 bucket named 'iam-policy-testbucket' to restrict access and to allow accounts to only write objects to the bucket. When the administrator tries to apply the following policy to the 'iam-policy-testbucket' bucket, the S3 bucket presents an error. {\n    \"Version\": \"2012-10-17\",\n    \"Id\": \"Policy1646946718956\",\n    \"Statement\": [\n        {\n            \"Sid\": \"Stmt1646946717210\",\n            \"Effect\": \"Allow\",\n            \"Action\": \"s3:PutObject\",\n            \"Resource\": \"arn:aws:s3:::iam-policy-testbucket/*\"\n        }\n    ]\n} How can the administrator correct the policy to resolve the error and successfully apply the policy?",
        "options": {
            "A": "Change the Action element from s3:PutObject to S3:*",
            "B": "Remove the Resource element because it is unnecessary for resource-based policies.",
            "C": "Change the Resource element to NotResource.",
            "D": "Add a Principal element to the policy to declare which accounts have access."
        },
        "correct_answer": "D",
        "explanation": {
            "A": "This solution is incorrect because changing to S3:* would grant all S3 actions, not just write access. It doesn't address the root cause of the error, which is the missing Principal. It would violate the requirement to only allow writing objects.",
            "B": "This solution is incorrect because the Resource element is necessary in S3 bucket policies to specify which resources the policy applies to. Removing it would make the policy too broad and potentially insecure. It doesn't address the root cause of the error (missing Principal).",
            "C": "This solution is incorrect because changing to NotResource would invert the resource specification, potentially granting access to unintended resources. It doesn't address the root cause of the error (missing Principal). It would complicate the policy unnecessarily.",
            "D": "Adding a Principal element to the policy is the correct solution because resource-based policies, like S3 bucket policies, require a Principal element to specify who is allowed or denied permission to access the resource. Without a Principal, the policy doesn't specify which AWS accounts, users, roles, or services are granted the permissions. The Principal element is crucial for defining the scope of access in resource-based policies."
        },
        "category": "Security & Identity"
    },
    {
        "id": 4,
        "question": "A media company is designing a new solution for graphic rendering. The application requires up to 400 GB of storage for temporary data that is discarded after the frames are rendered. The application requires approximately 40,000 random IOPS to perform the rendering. What is the MOST cost-effective storage option for this rendering application?",
        "options": {
            "A": "A storage optimized Amazon EC2 instance with instance store storage",
            "B": "A storage optimized Amazon EC2 instance with a Provisioned IOPS SSD (io1 or io2) Amazon Elastic Block Store (EBS) volume",
            "C": "A burstable Amazon EC2 instance with a Throughput Optimized HDD (st1) Amazon Elastic Block Store (EBS) volume",
            "D": "A burstable Amazon EC2 instance with Amazon S3 storage over a VPC endpoint"
        },
        "correct_answer": "A",
        "explanation": {
            "A": "A storage optimized EC2 instance with instance store storage is the most cost-effective solution because instance store provides high-performance, temporary block-level storage that's directly attached to the EC2 instance. It can deliver very high IOPS (often exceeding 40,000) at no additional cost beyond the EC2 instance price. The temporary nature of instance store aligns perfectly with the application's need for discardable data. Storage optimized instances (like i3 or i3en) are designed for workloads requiring high IOPS.",
            "B": "While this could meet the performance requirements, it's not the most cost-effective because Provisioned IOPS SSD volumes incur additional costs for both storage and IOPS. For temporary data, paying for persistent storage is unnecessary.",
            "C": "This solution is not suitable because Throughput Optimized HDD (st1) is designed for throughput-intensive workloads, not high IOPS. It cannot deliver the required 40,000 IOPS (maximum IOPS for st1 is much lower). Burstable instances may not provide consistent performance for this workload.",
            "D": "This solution is not appropriate because S3 is object storage, not block storage, and isn't suitable for the high IOPS requirements of this application. Accessing S3 over a VPC endpoint wouldn't provide the low-latency, high IOPS performance needed for rendering. Burstable instances may not provide consistent performance for this workload."
        },
        "category": "Storage"
    },
    {
        "id": 5,
        "question": "A company is creating a three-tier web application consisting of a web server, an application server, and a database server. The application will track GPS coordinates of packages as they are being delivered. The application will update the database every 0.5 seconds. The tracking will need to be read as fast as possible for users to check the status of their packages. Only a few packages might be tracked on some days, whereas millions of packages might be tracked on other days. Tracking will need to be searchable by tracking ID, customer ID, and order ID. Orders older than 1 month no longer need to be tracked. What should a solutions architect recommend to accomplish this with minimal total cost of ownership?",
        "options": {
            "A": "Use Amazon DynamoDB. Activate Auto Scaling for the DynamoDB table. Schedule an automatic deletion script for items older than 1 month.",
            "B": "Use Amazon DynamoDB with global secondary indexes. Activate Auto Scaling for the DynamoDB table and the global secondary indexes. Turn on TTL for the DynamoDB table.",
            "C": "Use an Amazon RDS On-Demand Instance with Provisioned IOPS. Configure Amazon CloudWatch alarms to send notifications when IOPS are exceeded. Increase and decrease IOPS as needed.",
            "D": "Use an Amazon RDS Reserved Instance with Provisioned IOPS. Configure Amazon CloudWatch alarms to send notifications when IOPS are exceeded. Increase and decrease IOPS as needed."
        },
        "correct_answer": "B",
        "explanation": {
            "A": "While close to the correct answer, this is not optimal because it doesn't mention Global Secondary Indexes, which are crucial for efficient querying by multiple attributes. Using a scheduled deletion script is less efficient and potentially more costly than using DynamoDB's built-in TTL feature.",
            "B": "This solution is the most suitable and cost-effective because DynamoDB is a fully managed NoSQL database that can handle high-frequency writes and reads with low latency. Auto Scaling allows the database to adjust capacity based on actual usage, optimizing costs during periods of low activity. Global Secondary Indexes (GSIs) enable efficient querying by multiple attributes (tracking ID, customer ID, and order ID). Time to Live (TTL) automatically removes old items, addressing the requirement to delete data older than 1 month without additional scripts or processes.",
            "C": "This solution is not ideal because RDS with Provisioned IOPS may not scale as efficiently for the varying workload described. Manually adjusting IOPS based on CloudWatch alarms is less efficient and potentially more costly than DynamoDB's automatic scaling. RDS may not provide the same level of performance for high-frequency updates and reads as DynamoDB.",
            "D": "This solution is not suitable because Reserved Instances are designed for steady-state workloads, not for the highly variable load described in the scenario. Like option C, manually adjusting IOPS is less efficient than automatic scaling. It doesn't address the requirement for efficient querying by multiple attributes or automatic data expiration."
        },
        "category": "Databases"
    },
    {
        "id": 6,
        "question": "A solutions architect is working on optimizing a legacy document management application running on multiple Microsoft Windows servers in an on-premises data center. The application accesses a large number of files on a network file share which is running out of space. The chief information officer wants to migrate the on-premises storage to AWS but still must be able to support the legacy application. What should the solutions architect do to meet these requirements?",
        "options": {
            "A": "Use an AWS Storage Gateway and the option of Amazon S3 File Gateway",
            "B": "Use Amazon Elastic File System (Amazon EFS)",
            "C": "Use AWS Storage Gateway and the option of volume gateway.",
            "D": "Use an Amazon Elastic Block Store (Amazon EBS) volume."
        },
        "correct_answer": "A",
        "explanation": {
            "A": "Using AWS Storage Gateway with the Amazon S3 File Gateway option is the most suitable solution because S3 File Gateway provides a seamless way to connect on-premises applications to Amazon S3 storage. It presents S3 objects as files through a Network File System (NFS) or Server Message Block (SMB) interface, which is compatible with Windows servers. It allows the legacy application to continue accessing files as if they were on a local network share. It provides virtually unlimited storage capacity through Amazon S3.",
            "B": "This solution is not suitable because Amazon EFS is designed for Linux-based workloads and doesn't natively support Windows file systems. The legacy application running on Windows servers would not be able to directly access an EFS file system.",
            "C": "While this is close to the correct answer, it's not the best solution because Volume Gateway is more suited for block storage use cases, not file-based access. It would require more complex configuration and management compared to File Gateway for this file-sharing scenario.",
            "D": "This solution is not appropriate because EBS volumes are designed to be attached to individual EC2 instances, not shared across multiple servers. It doesn't provide a native file-sharing mechanism for on-premises applications. It would require significant changes to the application architecture."
        },
        "category": "Hybrid Cloud & Storage"
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