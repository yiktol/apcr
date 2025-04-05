
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
        "question": "A company runs its website on Amazon EC2 instances behind an Application Load Balancer that is configured as the origin for an Amazon CloudFront distribution. The company wants to protect against cross-site scripting and SQL injection attacks. Which approach should a solutions architect recommend to meet these requirements?",
        "options": {
            "A": "Enable AWS Shield Advanced. List the CloudFront distribution as a protected resource.",
            "B": "Define an AWS Shield Advanced policy in AWS Firewall Manager to block cross-site scripting and SQL injection attacks.",
            "C": "Deploy AWS Firewall Manager on the EC2 instances. Create conditions and rules that block cross-site scripting and SQL injection attacks.",
            "D": "Set up AWS WAF on the CloudFront distribution. Use conditions and rules that block cross-site scripting and SQL injection attacks."
        },
        "correct_answer": "D",
        "explanation": {
            "A": "AWS Shield Advanced is primarily designed for DDoS protection, not for application-layer attacks like XSS and SQL injection. While it provides some application-layer protections, it's not as comprehensive or customizable as WAF for these specific threats.",
            "B": "AWS Shield Advanced doesn't directly provide rules for XSS and SQL injection protection. Firewall Manager is used for centrally configuring and managing firewalls across accounts and applications, not for creating specific application-layer rules.",
            "C": "AWS Firewall Manager is not deployed on EC2 instances; it's a service for managing firewalls across accounts and applications. For EC2 instances, you would typically use security groups or network ACLs for network-level protection, not application-layer protection.",
            "D": "Setting up AWS WAF on the CloudFront distribution is the most appropriate solution because AWS WAF is specifically designed to protect web applications from common web exploits like XSS and SQL injection. It can be easily integrated with CloudFront distributions, provides pre-configured rule sets for common attacks, and allows for custom rule creation to address specific security needs."
        },
        "category": "Security"
    },
    {
        "id": 2,
        "question": "A solutions architect is designing a VPC that requires access to a remote API server using IPv6. Resources within the VPC should not be accessed directly from the internet. How should this be achieved?",
        "options": {
            "A": "Use a NAT Gateway and deny public access using security groups.",
            "B": "Attach an egress-only internet gateway and update the routing tables.",
            "C": "Use a NAT Gateway and update the routing tables.",
            "D": "Attach an internet gateway and deny public access using security groups."
        },
        "correct_answer": "B",
        "explanation": {
            "A": "NAT Gateways are designed for IPv4 traffic, not IPv6. Security groups are stateful and don't provide the same level of control as an egress-only internet gateway for IPv6 traffic.",
            "B": "Attaching an egress-only internet gateway and updating the routing tables is the most appropriate solution because it's specifically designed for IPv6 traffic to allow outbound communication while preventing inbound access. It provides a way for IPv6-enabled instances in a VPC to access the internet without allowing internet-based IPv6 traffic to reach those instances.",
            "C": "NAT Gateways do not support IPv6 traffic. Even if it did work with IPv6, a NAT Gateway doesn't provide the same level of control over inbound traffic as an egress-only internet gateway.",
            "D": "An internet gateway allows both inbound and outbound traffic, which doesn't meet the requirement of preventing direct access to VPC resources. Relying solely on security groups for public access control is less secure than using an egress-only internet gateway for IPv6 traffic."
        },
        "category": "Networking"
    },
    {
        "id": 3,
        "question": "A company wants to build an immutable infrastructure for its software applications. The company wants to test the software applications before sending traffic to them. The company seeks an efficient solution that limits the effects of application bugs. Which combination of steps should a solutions architect recommend?",
        "options": {
            "A": "Use AWS CloudFormation to update the production infrastructure and roll back the stack if the update fails.",
            "B": "Apply Amazon Route 53 failover routing to test the staging environment and fail over to the production environment if the tests pass.",
            "C": "Apply Amazon Route 53 weighted routing to test the staging environment and gradually increase the traffic as the tests pass.",
            "D": "Use AWS CloudFormation with a parameter set to the staging value in a separate environment other than the production environment.",
            "E": "Use AWS CloudFormation to deploy the staging environment with a snapshot deletion policy and reuse the resources in the production environment if the tests pass."
        },
        "correct_answer": "C, D",
        "explanation": {
            "A": "It suggests making changes directly to the production environment, which goes against the principle of testing before sending traffic. Rolling back after a failure in production could lead to downtime or other issues.",
            "B": "Failover routing is designed for disaster recovery scenarios, not for gradual testing and traffic shifting. It doesn't provide the granular control needed for efficient testing and gradual rollout.",
            "C": "Weighted routing allows for gradual traffic shifting, which is ideal for testing new deployments. It enables a controlled approach to directing traffic to the new application version. Traffic can be incrementally increased as tests pass, limiting the impact of potential bugs.",
            "D": "It aligns with the principle of immutable infrastructure by using CloudFormation for deployment. Creating a separate staging environment allows for thorough testing without affecting production. Using parameters in CloudFormation templates enables easy management of different environments.",
            "E": "Reusing resources from staging in production goes against the principle of immutable infrastructure. It doesn't provide a clean separation between staging and production environments."
        },
        "category": "Deployment and Infrastructure"
    },
    {
        "id": 4,
        "question": "An application launched on Amazon EC2 instances needs to publish personally identifiable information (PII) about customers using Amazon Simple Notification Service (Amazon SNS). The application is launched in private subnets within an Amazon VPC. What is the MOST secure way to allow the application to access service endpoints in the same AWS Region?",
        "options": {
            "A": "Use an internet gateway.",
            "B": "Use a NAT gateway.",
            "C": "Use AWS PrivateLink.",
            "D": "Use a proxy instance."
        },
        "correct_answer": "C",
        "explanation": {
            "A": "It exposes the EC2 instances to the public internet, increasing security risks. For instances in private subnets, direct internet access via an internet gateway is not possible. It's not the most secure option for handling sensitive data like PII.",
            "B": "Traffic still goes through the public internet, increasing exposure of sensitive data. It doesn't provide the same level of isolation and security as PrivateLink. NAT gateways are primarily designed for allowing private instances to access the internet, not for accessing AWS services securely.",
            "C": "Using AWS PrivateLink provides private connectivity between VPCs and AWS services without exposing traffic to the public internet. It keeps all traffic within the AWS network, enhancing security for sensitive data like PII. It allows access to AWS services as if they were in your VPC, reducing the attack surface.",
            "D": "It introduces an additional point of failure and management overhead. The proxy instance itself could become a security risk if not properly maintained. It doesn't provide the same level of integration and security as PrivateLink."
        },
        "category": "Security"
    },
    {
        "id": 5,
        "question": "A company hosts a popular web application to learn more about various kinds of sports. The web application connects to an Amazon RDS for MySQL database running in a private VPC subnet. The web servers must be accessible only to customers on an SSL connection. The database server must be accessible only from the web servers. How should a solutions architect design a solution to meet the requirements without impacting running applications?",
        "options": {
            "A": "Create a network ACL on the web server's subnet, and allow HTTPS inbound and MySQL outbound. Place both database and web servers on the same subnet.",
            "B": "Open an HTTPS port on the security group for web servers and set the source to 0.0.0.0/0. Open the MySQL port on the database security group and attach it to the MySQL instance. Set the source to web server security group.",
            "C": "Create a network ACL on the web server's subnet; allow HTTPS inbound and specify the source as 0.0.0.0/0. Create a network ACL on a database subnet, allow MySQL port inbound for web servers, and deny all outbound traffic.",
            "D": "Open the MySQL port on the security group for web servers and set the source to 0.0.0.0/0. Open the HTTPS port on the database security group and attach it to the MySQL instance. Set the source to web server security group."
        },
        "correct_answer": "B",
        "explanation": {
            "A": "It uses network ACLs, which are stateless and less flexible than security groups. Placing web and database servers on the same subnet doesn't follow best practices for security isolation. It doesn't provide granular control over which web servers can access the database.",
            "B": "This solution uses security groups, which are stateful and provide more flexibility than network ACLs. It allows HTTPS access to web servers from anywhere (0.0.0.0/0), meeting the SSL requirement. It restricts database access to only the web servers by referencing the web server security group. It doesn't require changes to the existing network architecture, minimizing impact on running applications.",
            "C": "Using network ACLs alone doesn't provide the granularity needed for this scenario. Denying all outbound traffic on the database subnet would break functionality, as the database needs to send responses back to the web servers. It's more complex and harder to manage than using security groups.",
            "D": "It exposes the MySQL port of the web servers to the internet (0.0.0.0/0), which is a security risk. It opens HTTPS on the database security group, which is unnecessary as the database doesn't serve HTTPS traffic. It doesn't properly secure the web servers for HTTPS access."
        },
        "category": "Networking"
    },
    {
        "id": 6,
        "question": "A company expects the user base of its home shopping application to increase to 3 times the current level in 1 year. The company hosts the application in one AWS Region. The company uses an Amazon RDS for MySQL DB instance, an Application Load Balancer, and Amazon Elastic Container Service (Amazon ECS) to host the website, static content, and the microservices. A solutions architect must recommend design changes to support the expected growth and reduce operational overhead. Which design changes meet these requirements?",
        "options": {
            "A": "Move static files from Amazon ECS to Amazon S3.",
            "B": "Use an Amazon Route 53 geolocation routing policy.",
            "C": "Scale the RDS DB instance size based on AWS CloudTrail log monitoring.",
            "D": "Create a second RDS DB instance in another region. Split the load between the two DB instances.",
            "E": "Scale the RDS DB instance size based on RDS Performance Insights monitoring."
        },
        "correct_answer": ["A", "E"],
        "multi_select": True,
        "explanation": {
            "A": "Offloading static content to S3 reduces the load on ECS containers, allowing them to focus on dynamic content. S3 is highly scalable and can handle increased traffic without additional management. It reduces operational overhead as S3 is a fully managed service. S3 can be easily integrated with CloudFront for global content delivery, improving performance.",
            "B": "While this could improve performance for a global user base, it's not directly addressing the growth or operational overhead concerns. The question doesn't mention a global user base or performance issues related to user location.",
            "C": "CloudTrail is primarily for API activity logging, not for database performance monitoring. It doesn't provide the specific database performance insights needed for effective scaling.",
            "D": "It introduces unnecessary complexity for an application currently hosted in one region. Splitting load between two DB instances in different regions can lead to data consistency issues and increased latency. It doesn't align with the goal of reducing operational overhead.",
            "E": "RDS Performance Insights provides deep visibility into database performance. It helps in identifying when and how to scale the database to meet growing demands. It reduces operational overhead by providing clear, actionable insights. Proper scaling based on actual performance data ensures the database can handle increased load."
        },
        "category": "Database"
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