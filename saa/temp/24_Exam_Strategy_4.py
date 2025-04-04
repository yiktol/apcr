
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
        "question": "An application running in a private subnet accesses an Amazon DynamoDB table. The data cannot leave the AWS network to meet security requirements. How should this requirement be met?",
        "options": {
            "A": "Configure a Network ACL on DynamoDB to limit traffic to the private subnet.",
            "B": "Enable DynamoDB encryption at rest using an AWS Key Management Service (AWS KMS) key.",
            "C": "Add a NAT gateway and configure the route table on the private subnet.",
            "D": "Configure a VPC endpoint for DynamoDB and configure the endpoint policy."
        },
        "correct_answer": "D",
        "explanation": {
            "A": "Network ACLs are associated with subnets, not with AWS services like DynamoDB. DynamoDB is a managed service and doesn't support direct attachment of Network ACLs. It doesn't address the requirement of keeping traffic within the AWS network.",
            "B": "While encryption at rest is a good security practice, it doesn't address the specific requirement because it secures data stored in DynamoDB but doesn't affect how the data travels over the network. It doesn't prevent data from potentially leaving the AWS network during transit.",
            "C": "A NAT gateway is used for allowing private subnet resources to access the internet, not for keeping traffic within the AWS network. Using a NAT gateway would potentially route traffic over the public internet, violating the security requirement.",
            "D": "VPC endpoints allow you to privately connect your VPC to supported AWS services without requiring an internet gateway, NAT device, VPN connection, or AWS Direct Connect connection. The traffic between your VPC and DynamoDB stays within the Amazon network, never leaving the AWS infrastructure. It meets the security requirement of keeping data within the AWS network. Endpoint policies provide an additional layer of access control."
        },
        "category": "Security Knowledge Application"
    },
    {
        "id": 2,
        "question": "A company that processes satellite images has an application that runs on AWS. The company stores the images in an Amazon S3 bucket. For compliance reasons, the company must replicate all data once a month to an on-premises location. The average amount of data that the company needs to transfer is 60 TB. What is the MOST cost-effective way to transfer this data?",
        "options": {
            "A": "Export the data monthly from the existing S3 bucket to an AWS Snowball Edge Storage Optimized device. Ship the device to the on-premises location. Transfer the data. Return the device a week later.",
            "B": "Use S3 bucket replication to copy all objects to a new S3 bucket that uses S3 Standard-Infrequent Access (S3 Standard-IA) storage. Use an AWS Storage Gateway File Gateway to transfer the data from the new S3 bucket to the on-premises location. Delete the images from the new S3 bucket after the transfer of the data.",
            "C": "Use S3 bucket replication to copy all objects to a new S3 bucket that uses S3 Standard-Infrequent Access (S3 Standard-IA) storage. Use Amazon S3 to transfer the data from the new S3 bucket to the on-premises location. Delete the images from the new S3 bucket after the transfer of the data.",
            "D": "Create an Amazon CloudFront Distribution for the objects in the existing S3 bucket. Download the objects from CloudFront to the on-premises location every month."
        },
        "correct_answer": "A",
        "explanation": {
            "A": "Using AWS Snowball Edge is the most cost-effective solution for this scenario because it's designed for large-scale data transfers (up to 80 TB per device). It eliminates the need for high-bandwidth internet connections, which can be expensive for transferring 60 TB monthly. Data transfer with Snowball Edge incurs a fixed cost per job, which is generally more cost-effective for large transfers compared to network-based solutions. It provides a secure, physical transfer method, which can be beneficial for compliance reasons.",
            "B": "This solution is not the most cost-effective because it involves additional S3 storage costs for the replicated data. Transferring 60 TB monthly over the internet via Storage Gateway would require significant bandwidth and time. It may incur higher data transfer costs compared to Snowball Edge for this volume of data.",
            "C": "This solution is not optimal because it involves additional S3 storage costs for the replicated data. Transferring 60 TB monthly directly from S3 would incur significant data transfer costs. It may require substantial internet bandwidth, which could be expensive or impractical.",
            "D": "This is not the most cost-effective solution because CloudFront is designed for content delivery, not large-scale data transfer. Downloading 60 TB monthly through CloudFront would incur significant data transfer costs. It doesn't provide any specific advantages for this use case over direct S3 access."
        },
        "category": "Data Transfer"
    },
    {
        "id": 3,
        "question": "A company uses one AWS account to run production workloads. The company has a separate AWS account for its security engineering team. During periodic audits, the security engineering team needs to view specific account settings and resource configurations in the AWS account that runs production workloads. A solutions architect must provide the security engineering team with the required access permissions by designing a solution that follows prescribed AWS security best practices. Which solution will meet these requirements?",
        "options": {
            "A": "Create an IAM user for each security team member in the production account. Attach a permissions policy that provides the permissions required by the security engineering team to each user.",
            "B": "Create an IAM user for each member of the security engineering team in the production account. Attach a permissions policy that provides the permissions required by the security engineering team to a new IAM group. Assign security engineering members to the group.",
            "C": "Create an IAM role in the production account. Attach a permissions policy that provides the permissions required by the security engineering team. Add the security engineering team account to the trust policy.",
            "D": "Create a new IAM user in the production account. Assign administrative privileges to the user. Allow the security engineering team to use this account to log in to the systems that need to be accessed."
        },
        "correct_answer": "C",
        "explanation": {
            "A": "It creates multiple IAM users in the production account, increasing management overhead. It doesn't follow the best practice of centralized identity management. It makes it more difficult to manage and audit access permissions.",
            "B": "While this is better than option A due to the use of groups, it still creates multiple IAM users in the production account. It doesn't leverage cross-account access capabilities. It increases the complexity of identity management across accounts.",
            "C": "Creating an IAM role in the production account and using cross-account access follows the principle of least privilege by granting only necessary permissions. It leverages AWS Organizations and IAM roles for secure cross-account access. It doesn't require creating or managing individual IAM users in the production account. It allows for centralized management of permissions in the production account.",
            "D": "This is the least secure and least recommended option because it violates the principle of least privilege by granting administrative access. Sharing a single user account among multiple team members is a security anti-pattern. It doesn't provide any audit trail of individual actions. It grants much broader permissions than necessary for the audit requirements."
        },
        "category": "Security"
    },
    {
        "id": 4,
        "question": "A solutions architect needs to allow developers to have SSH connectivity to web servers. The requirements are as follows: · Limit access to users originating from the corporate network. · Web servers cannot have SSH access directly from the internet. · Web servers reside in a private subnet. Which combination of steps must the architect complete to meet these requirements?",
        "options": {
            "A": "Create a bastion host that authenticates users against the corporate directory.",
            "B": "Create a bastion host with security group rules that only allow traffic from the corporate network.",
            "C": "Attach an IAM role to the bastion host with relevant permissions.",
            "D": "Configure the web servers' security group to allow SSH traffic from a bastion host.",
            "E": "Deny all SSH traffic from the corporate network in the inbound network ACL."
        },
        "correct_answer": "B and D",
        "explanation": {
            "A": "While this could be a good practice, it's not necessary to meet the stated requirements. The question doesn't specify a need for integration with the corporate directory.",
            "B": "A bastion host provides a secure way to access private resources from an external network. By configuring security group rules to only allow traffic from the corporate network, it ensures that only authorized users can access the bastion host. It satisfies the requirement of limiting access to users originating from the corporate network.",
            "C": "This is not necessary to meet the specific requirements. IAM roles are typically used for granting permissions to AWS services, not for controlling SSH access.",
            "D": "It ensures that the web servers can only be accessed via SSH from the bastion host, not directly from the internet. It maintains the security of the web servers in the private subnet while still allowing authorized access. It complements the bastion host setup to create a secure SSH access path.",
            "E": "This would prevent the required access from the corporate network, contradicting the requirements."
        },
        "category": "Networking & Security"
    },
    {
        "id": 5,
        "question": "A reporting application runs on Amazon EC2 instances behind an Application Load Balancer. The instances run in an Amazon EC2 Auto Scaling group across multiple Availability Zones. For complex reports, the application can take up to 15 minutes to respond to a request. A solutions architect is concerned that users will receive HTTP 5xx errors if a report request is in process during a scale-in event. What should the solutions architect do to ensure that user requests will be completed before instances are terminated?",
        "options": {
            "A": "Enable sticky sessions (session affinity) for the target group of the instances.",
            "B": "Increase the instance size in the Application Load Balancer target group.",
            "C": "Increase the cooldown period for the Auto Scaling group to a greater amount of time than the time required for the longest running responses.",
            "D": "Increase the deregistration delay timeout for the target group of the instances to greater than 900 seconds."
        },
        "correct_answer": "D",
        "explanation": {
            "A": "Sticky sessions ensure that a client's requests are routed to the same instance, but don't prevent instance termination during scale-in events. It doesn't address the issue of in-flight requests being interrupted.",
            "B": "Increasing instance size doesn't prevent the interruption of in-flight requests during scale-in events. It might reduce the frequency of scale-in events but doesn't solve the core issue of request interruption.",
            "C": "The cooldown period affects the time between Auto Scaling activities, not the handling of in-flight requests. It doesn't directly prevent the termination of instances with active requests. It could lead to slower response to changing load conditions.",
            "D": "It allows in-flight requests to complete before the instance is deregistered from the load balancer. It ensures that no new requests are sent to the instance that is about to be terminated. It prevents interruption of long-running requests, avoiding HTTP 5xx errors. 900 seconds (15 minutes) matches the maximum time for complex reports, ensuring all requests can complete."
        },
        "category": "Auto Scaling"
    },
    {
        "id": 6,
        "question": "A company has decided to use AWS to achieve high availability. The company's architecture consists of an Application Load Balancer in front of an Auto Scaling group that consists of Amazon EC2 instances. The company uses Amazon CloudWatch metrics and alarms to monitor the architecture. A solutions architect notices that the company is not able to launch some instances. The solutions architect finds the following message: EC2 QUOTA EXCEEDED. How can the solutions architect ensure that the company is able to launch all the EC2 instances correctly?",
        "options": {
            "A": "Modify the Auto Scaling group to raise the maximum number of instances that the company can launch.",
            "B": "Use Service Quotas to request an increase to the number of EC2 instances that the company can launch.",
            "C": "Recreate the Auto Scaling group to ensure the Auto Scaling group is connected to the Application Load Balancer.",
            "D": "Modify the CloudWatch metric that the company monitors to launch the instances."
        },
        "correct_answer": "B",
        "explanation": {
            "A": "The Auto Scaling group's maximum size is different from the AWS account's EC2 instance quota. Increasing the Auto Scaling group's maximum size won't resolve the account-level quota issue. The error message specifically indicates an EC2 quota problem, not an Auto Scaling group configuration issue.",
            "B": "The 'EC2 QUOTA EXCEEDED' error indicates that the company has reached its account limit for the number of EC2 instances it can launch. AWS imposes default service quotas (formerly known as limits) on various resources, including EC2 instances, for each AWS account. Service Quotas provides a centralized way to view and manage your AWS service quotas. Requesting a quota increase is the proper way to address this specific error.",
            "C": "The error is related to EC2 instance quotas, not the Auto Scaling group's configuration or its connection to the ALB. Recreating the Auto Scaling group won't change the account's EC2 instance limits.",
            "D": "CloudWatch metrics are used for monitoring and triggering alarms, not for managing EC2 instance limits. Modifying a CloudWatch metric won't affect the account's ability to launch more EC2 instances. The error is related to AWS service quotas, not CloudWatch configurations."
        },
        "category": "Quotas & Limits"
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