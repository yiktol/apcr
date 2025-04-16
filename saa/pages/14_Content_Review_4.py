
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
    page_title="AWS Solutions Architect - Associate",
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
    
    /* Quiz Section */
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

# Initialize session state
def init_session_state():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    # Initialize topic scores
    topics = ["ebs", "ipv4", "elb", "management", "cloudformation", "analytics"]
    
    # Initialize tracking for quizzes
    if "quiz_scores" not in st.session_state:
        st.session_state.quiz_scores = {}
    
    if "quiz_attempted" not in st.session_state:
        st.session_state.quiz_attempted = {}
    
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    
    # Initialize for each topic
    for topic in topics:
        if topic not in st.session_state.quiz_scores:
            st.session_state.quiz_scores[topic] = 0
        if topic not in st.session_state.quiz_attempted:
            st.session_state.quiz_attempted[topic] = 0
        if topic not in st.session_state.quiz_answers:
            st.session_state.quiz_answers[topic] = {}

# Function to reset session state
def reset_session():
    topics = ["ebs", "ipv4", "elb", "management", "cloudformation", "analytics"]
    
    for topic in topics:
        st.session_state.quiz_scores[topic] = 0
        st.session_state.quiz_attempted[topic] = 0
        st.session_state.quiz_answers[topic] = {}
    
    st.success("✅ Quiz data has been reset successfully!")

# Initialize session state at app startup
init_session_state()

# Define AWS stock images URLs
aws_images = {
    "home": "https://d1.awsstatic.com/training-and-certification/certification-badges/AWS-Certified-Solutions-Architect-Associate_badge.3419559c682629072f1eb968d59dea0741772c0f.png",
    "ebs": "images/ebs.png",
    "ipv4": "images/dualstack.png",
    "elb": "images/elb.png",
    "cloudtrail": "images/cloudtrail.png",
    "cloudwatch": "images/cloudwatch.png",
    "cloudformation": "images/cloudformation.png",
    "athena": "images/athena.png",
    "opensearch": "images/opensearch.png",
    "emr": "images/emr.png",
    "glue": "images/glue.png",
    "quicksight": "images/quicksight.png"
}

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

# Function to create nice card components
def create_card(title, content, key=None):
    with st.container():
        st.markdown(f"""
        <div class="aws-card">
            <h3>{title}</h3>
            <p>{content}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if key:
            st.button("Learn More", key=key)

# Scenario-based quiz questions
quiz_data = {
    "ebs": [
        {
            "question": "A financial services company is migrating an application that processes sensitive transaction data to AWS. The application runs on EC2 instances and requires block storage with consistent low-latency performance for a high number of small random I/O operations. Data encryption and regular snapshots are also required for compliance. Which EBS volume type would best meet these requirements?",
            "options": [
                "General Purpose SSD (gp2)",
                "Provisioned IOPS SSD (io1)",
                "Throughput Optimized HDD (st1)",
                "Cold HDD (sc1)",
                "Magnetic (standard)"
            ],
            "answer": "Provisioned IOPS SSD (io1)"
        },
        {
            "question": "A media company stores large video files that are processed initially and then accessed infrequently afterward. They need a cost-effective storage solution for these files but still require the ability to access them quickly when needed. The files average 100GB each. Which EBS volume type should they choose?",
            "options": [
                "Provisioned IOPS SSD (io1)",
                "General Purpose SSD (gp2)",
                "Throughput Optimized HDD (st1)",
                "Cold HDD (sc1)",
                "Magnetic (standard)"
            ],
            "answer": "Throughput Optimized HDD (st1)"
        },
        {
            "question": "A startup is building a new application on AWS and needs to store application logs. The logs will be written continuously throughout the day but will only be analyzed once per week. Cost optimization is a priority. Which EBS volume type is most appropriate for this use case?",
            "options": [
                "General Purpose SSD (gp2)",
                "Provisioned IOPS SSD (io1)",
                "Throughput Optimized HDD (st1)",
                "Cold HDD (sc1)",
                "Magnetic (standard)"
            ],
            "answer": "Cold HDD (sc1)"
        },
        {
            "question": "A company is planning to migrate a database that supports their e-commerce website to AWS. The database requires storage that can handle a moderate amount of transactional workload with occasional spikes in activity during sales events. They need a cost-effective solution that provides good performance for this varying workload. Which EBS volume type should they choose?",
            "options": [
                "General Purpose SSD (gp2)",
                "Provisioned IOPS SSD (io1)",
                "Throughput Optimized HDD (st1)",
                "Cold HDD (sc1)",
                "Magnetic (standard)"
            ],
            "answer": "General Purpose SSD (gp2)"
        },
        {
            "question": "A data science team needs to run complex machine learning workloads on EC2 instances. Their process involves loading large datasets sequentially, processing them, and then storing the results. The priority is high throughput for these sequential read and write operations rather than low latency for random access. Which EBS volume type would be most appropriate for this workload?",
            "options": [
                "General Purpose SSD (gp2)",
                "Provisioned IOPS SSD (io1)",
                "Throughput Optimized HDD (st1)",
                "Cold HDD (sc1)",
                "Magnetic (standard)"
            ],
            "answer": "Throughput Optimized HDD (st1)"
        }
    ],
    "ipv4": [
        {
            "question": "A company is planning their VPC architecture for a new application deployment. They anticipate needing to host approximately 500 EC2 instances across multiple subnets, with room for growth. They also plan to connect to their on-premises data center via AWS Direct Connect in the future. Which IPv4 CIDR block would be most appropriate for their VPC?",
            "options": [
                "10.0.0.0/24 (provides 256 IP addresses)",
                "10.0.0.0/20 (provides 4,096 IP addresses)",
                "10.0.0.0/16 (provides 65,536 IP addresses)",
                "10.0.0.0/8 (provides 16,777,216 IP addresses)",
                "172.16.0.0/28 (provides 16 IP addresses)"
            ],
            "answer": "10.0.0.0/16 (provides 65,536 IP addresses)"
        },
        {
            "question": "A company is designing a new VPC to host a multi-tier application. They need to create subnets in two Availability Zones for high availability. Each tier (web, application, and database) requires its own subnet in each AZ. The company expects to host up to 30 EC2 instances per subnet initially, with potential growth to 100 instances per subnet. Which subnet CIDR blocks would be most appropriate?",
            "options": [
                "Use /28 subnets providing 16 IP addresses each",
                "Use /24 subnets providing 256 IP addresses each",
                "Use /20 subnets providing 4,096 IP addresses each",
                "Use /16 subnets providing 65,536 IP addresses each",
                "Use /26 subnets providing 64 IP addresses each"
            ],
            "answer": "Use /24 subnets providing 256 IP addresses each"
        },
        {
            "question": "A global company is setting up AWS infrastructure in multiple regions. Their on-premises network uses the CIDR block 10.0.0.0/8. They plan to implement VPC peering and AWS Transit Gateway to connect VPCs across regions. Which IP addressing strategy should they implement to avoid IP address conflicts?",
            "options": [
                "Use the same CIDR block (10.0.0.0/8) for all VPCs to maintain consistency",
                "Use 10.0.0.0/16 for all VPCs since it's a subset of their on-premises network",
                "Use non-overlapping CIDR blocks from the 172.16.0.0/12 private address space for their AWS VPCs",
                "Use public IP ranges for all VPCs to avoid any potential conflicts",
                "Use the 169.254.0.0/16 link-local address space for all VPCs"
            ],
            "answer": "Use non-overlapping CIDR blocks from the 172.16.0.0/12 private address space for their AWS VPCs"
        },
        {
            "question": "A company is planning to deploy a new application that will be accessible over IPv6. They want to ensure their VPC and subnets are properly configured for IPv6 traffic. Which statement accurately describes IPv6 configuration in Amazon VPC?",
            "options": [
                "IPv6 is enabled by default on all new VPCs, replacing IPv4 addressing",
                "IPv6 addressing can be enabled on a VPC, and the IPv6 CIDR block is chosen by the customer",
                "IPv6 addressing can be enabled on a VPC, and the IPv6 CIDR block is automatically assigned from Amazon's pool of IPv6 addresses",
                "IPv6 can only be enabled when creating a new VPC and cannot be added to existing VPCs",
                "IPv6 can only be used with Internet-facing resources and cannot be used for internal-only resources"
            ],
            "answer": "IPv6 addressing can be enabled on a VPC, and the IPv6 CIDR block is automatically assigned from Amazon's pool of IPv6 addresses"
        },
        {
            "question": "A solutions architect is designing a VPC with several subnets. When creating the subnets, what IP addresses in each subnet CIDR block are reserved by AWS and unavailable for use?",
            "options": [
                "Only the first IP address is reserved for the network address",
                "The first IP address (network address) and the last IP address (broadcast address) are reserved",
                "The first four IP addresses and the last IP address in each subnet CIDR block are reserved by AWS",
                "Only the last IP address is reserved for VPC routing",
                "No IP addresses are reserved, all addresses in a subnet CIDR block can be assigned to instances"
            ],
            "answer": "The first four IP addresses and the last IP address in each subnet CIDR block are reserved by AWS"
        }
    ],
    "elb": [
        {
            "question": "A company runs a microservices-based web application on Amazon EC2 instances. They need to implement a load balancer to distribute traffic efficiently. The application uses HTTP/2 and WebSockets for real-time updates, and they need to route traffic to different services based on URL paths. Which AWS load balancer should they use?",
            "options": [
                "Classic Load Balancer with sticky sessions enabled",
                "Network Load Balancer with cross-zone load balancing",
                "Application Load Balancer with path-based routing",
                "Gateway Load Balancer with health checks",
                "A combination of Classic Load Balancer and Network Load Balancer in a layered architecture"
            ],
            "answer": "Application Load Balancer with path-based routing"
        },
        {
            "question": "A financial services company runs a trading platform that requires ultra-low latency and handles millions of requests per second. They need to ensure that SSL/TLS connections are terminated at the load balancer level and that the platform can scale to handle unpredictable traffic patterns. Which load balancer best meets these requirements?",
            "options": [
                "Application Load Balancer with multiple target groups",
                "Classic Load Balancer with cross-zone load balancing enabled",
                "Network Load Balancer with TLS listeners",
                "Gateway Load Balancer with AWS WAF integration",
                "Application Load Balancer with WebSocket support"
            ],
            "answer": "Network Load Balancer with TLS listeners"
        },
        {
            "question": "A security team wants to implement a third-party firewall solution for traffic inspection before it reaches their application servers in AWS. They need a solution that allows transparent network packet inspection at layers 3 and 4, with the ability to scale the inspection appliances based on traffic volume. Which AWS load balancing solution should they implement?",
            "options": [
                "Application Load Balancer with AWS WAF",
                "Network Load Balancer with SSL termination",
                "Classic Load Balancer with sticky sessions",
                "Gateway Load Balancer with third-party security appliances",
                "Internal Application Load Balancer with security group rules"
            ],
            "answer": "Gateway Load Balancer with third-party security appliances"
        },
        {
            "question": "A company is migrating a complex application to AWS that consists of multiple components. The application requires routing based on the content of the request, such as HTTP headers, methods, and query parameters. They also need to redirect HTTP traffic to HTTPS and perform health checks on the target instances. Which load balancer should they use?",
            "options": [
                "Network Load Balancer with protocol detection",
                "Application Load Balancer with advanced request routing",
                "Gateway Load Balancer with traffic mirroring",
                "Classic Load Balancer with HTTP health checks",
                "Internal Load Balancer with SSL offloading"
            ],
            "answer": "Application Load Balancer with advanced request routing"
        },
        {
            "question": "A company runs containerized applications using Amazon ECS. They need to implement a load balancing solution that can direct traffic to dynamically changing container ports while maintaining IP address-based routing for certain client applications that require consistent IP addresses for security rules. Which combination of AWS services provides the best solution?",
            "options": [
                "Application Load Balancer for container port mapping and static IP addresses through Elastic IPs",
                "Network Load Balancer with static IP addresses and Application Load Balancer as a target for container port mapping",
                "Classic Load Balancer with cross-zone load balancing and port forwarding",
                "Gateway Load Balancer for IP address preservation and Application Load Balancer for container port mapping",
                "Two separate Application Load Balancers with different target groups for different client applications"
            ],
            "answer": "Network Load Balancer with static IP addresses and Application Load Balancer as a target for container port mapping"
        }
    ],
    "management": [
        {
            "question": "A company needs to comply with an industry regulation that requires them to track and audit all user actions taken on specific AWS resources. They need to know which user made the changes, what changes were made, and when they occurred. This data must be stored securely for compliance audits. Which AWS service should they implement?",
            "options": [
                "Amazon CloudWatch with detailed monitoring enabled",
                "AWS CloudTrail with log file validation enabled",
                "AWS Config with compliance rules",
                "Amazon EventBridge with custom event patterns",
                "VPC Flow Logs with traffic monitoring"
            ],
            "answer": "AWS CloudTrail with log file validation enabled"
        },
        {
            "question": "A DevOps team needs to monitor the performance of their applications running on EC2 instances. They want to create custom dashboards, set up automated alerts when CPU utilization exceeds 80% for more than 5 minutes, and collect application-specific metrics from their code. Which AWS service should they use?",
            "options": [
                "AWS CloudTrail with CloudWatch integration",
                "Amazon CloudWatch with custom metrics",
                "AWS Config with resource monitoring",
                "Amazon Inspector with assessment templates",
                "AWS Systems Manager with Run Command"
            ],
            "answer": "Amazon CloudWatch with custom metrics"
        },
        {
            "question": "A financial services company needs to ensure that all their AWS resources comply with specific configuration standards. They need to automatically detect and remediate non-compliant resources, such as unencrypted S3 buckets or security groups with overly permissive rules. Which AWS service should they implement?",
            "options": [
                "Amazon Inspector with assessment rules",
                "AWS CloudTrail with event selectors",
                "Amazon CloudWatch with alerting",
                "AWS Config with conformance packs and remediation actions",
                "AWS Security Hub with security standards"
            ],
            "answer": "AWS Config with conformance packs and remediation actions"
        },
        {
            "question": "A company's security team wants to receive notifications when unauthorized API calls occur in their AWS account, particularly for security-related services. They need to identify potential security breaches quickly. Which combination of AWS services and features should they implement?",
            "options": [
                "AWS Config with config rules and Amazon SNS notifications",
                "Amazon Inspector with assessment reports and EventBridge",
                "VPC Flow Logs with CloudWatch Logs Insights queries",
                "AWS CloudTrail with CloudWatch alarms and SNS notifications",
                "AWS Security Hub with compliance standards and EventBridge rules"
            ],
            "answer": "AWS CloudTrail with CloudWatch alarms and SNS notifications"
        },
        {
            "question": "A DevOps team needs to monitor a large number of microservices running on EC2 instances. They want to collect detailed performance data, identify performance bottlenecks, and set up anomaly detection to automatically identify unusual behavior patterns. Which service or feature should they implement?",
            "options": [
                "AWS X-Ray with trace analysis",
                "Amazon CloudWatch with Container Insights",
                "AWS CloudTrail with API monitoring",
                "AWS Config with configuration history",
                "Amazon CloudWatch with anomaly detection and detailed monitoring"
            ],
            "answer": "Amazon CloudWatch with anomaly detection and detailed monitoring"
        }
    ],
    "cloudformation": [
        {
            "question": "A company wants to implement infrastructure as code practices for their AWS deployments. They need to create identical environments for development, testing, and production with consistent configurations. These environments include complex networking setups, EC2 instances, and RDS databases. Which approach using CloudFormation would be most efficient?",
            "options": [
                "Create a single large template that includes all resources for all environments",
                "Use separate templates for each environment with duplicated resource definitions",
                "Create reusable templates with parameters and use nested stacks for common components",
                "Deploy all environments in a single CloudFormation stack with conditions",
                "Use AWS Elastic Beanstalk instead of CloudFormation for this use case"
            ],
            "answer": "Create reusable templates with parameters and use nested stacks for common components"
        },
        {
            "question": "A DevOps team is using CloudFormation to manage their infrastructure. They need to update a production stack that includes a critical database and want to ensure that they understand the potential impact of the changes before applying them. Which CloudFormation feature should they use?",
            "options": [
                "Stack policies to prevent resource updates",
                "Drift detection to identify manual changes",
                "Change sets to preview changes before execution",
                "Template validation to check for errors",
                "Resource import to add existing resources"
            ],
            "answer": "Change sets to preview changes before execution"
        },
        {
            "question": "A company is using CloudFormation to manage their infrastructure. They have a stack with multiple resources including EC2 instances, an RDS database, and an Elastic Load Balancer. During a stack update, the database update fails due to insufficient storage. What is the default behavior of CloudFormation in this scenario?",
            "options": [
                "The stack update continues and skips the failed resource",
                "The stack update fails but leaves the partially updated resources in place",
                "The stack update fails and automatically rolls back all changes to the previous stable state",
                "The stack update pauses and waits for manual intervention",
                "The stack update fails but only rolls back the failed resource"
            ],
            "answer": "The stack update fails and automatically rolls back all changes to the previous stable state"
        },
        {
            "question": "A solutions architect needs to create a CloudFormation template that includes a Lambda function, but the function code needs to be updated frequently without changing the rest of the infrastructure. What is the most efficient way to structure this in CloudFormation?",
            "options": [
                "Include the Lambda function code directly in the CloudFormation template",
                "Store the Lambda function code in an S3 bucket and reference it in the CloudFormation template",
                "Use AWS SAM instead of plain CloudFormation for Lambda resources",
                "Create a separate template for the Lambda function and link them using cross-stack references",
                "Use CloudFormation custom resources to manage the Lambda function code"
            ],
            "answer": "Store the Lambda function code in an S3 bucket and reference it in the CloudFormation template"
        },
        {
            "question": "A company is expanding their infrastructure and wants to ensure that all teams follow consistent standards when creating AWS resources. They already use CloudFormation for deployments. Which approach would help them standardize resource configurations across multiple teams and projects?",
            "options": [
                "Implement AWS Config rules to enforce standards after deployment",
                "Create and publish CloudFormation templates in the AWS Service Catalog",
                "Use CloudFormation StackSets to deploy consistent resources",
                "Implement AWS Organizations SCPs to restrict resource creation",
                "Use CloudFormation imports to manage existing resources"
            ],
            "answer": "Create and publish CloudFormation templates in the AWS Service Catalog"
        }
    ],
    "analytics": [
        {
            "question": "A data analytics team needs to analyze a large dataset stored in Amazon S3 in CSV format. They want to perform ad-hoc SQL queries without setting up any infrastructure or loading the data into a database. The solution should be cost-effective and require minimal setup. Which AWS service should they use?",
            "options": [
                "Amazon Redshift with Spectrum",
                "Amazon RDS with read replicas",
                "Amazon Athena with S3 integration",
                "Amazon EMR with Hadoop cluster",
                "AWS Glue with ETL jobs"
            ],
            "answer": "Amazon Athena with S3 integration"
        },
        {
            "question": "A company needs to analyze log data from their applications to identify operational issues and security threats. They require full-text search capabilities, visualization dashboards, and the ability to set up alerts based on specific patterns in the logs. Which AWS service is most suitable for this requirement?",
            "options": [
                "Amazon Athena with Athena Workgroups",
                "Amazon QuickSight with Q",
                "Amazon OpenSearch Service with Dashboards",
                "Amazon EMR with Spark SQL",
                "Amazon Redshift with AQUA"
            ],
            "answer": "Amazon OpenSearch Service with Dashboards"
        },
        {
            "question": "A healthcare company needs to process large datasets containing patient information for research purposes. The data processing involves complex transformations using Apache Spark. They need a managed service that makes it easy to run these big data frameworks without managing the underlying infrastructure. Which AWS service should they use?",
            "options": [
                "AWS Batch with compute environments",
                "Amazon EC2 with Auto Scaling groups",
                "Amazon EMR with Spark clusters",
                "AWS Lambda with S3 triggers",
                "Amazon Athena with federated queries"
            ],
            "answer": "Amazon EMR with Spark clusters"
        },
        {
            "question": "A retail company has data stored in multiple sources including S3, RDS, and DynamoDB. They want to create a central catalog of this data, transform it for analytics, and load it into a data lake for business intelligence applications. They need a service that can automatically discover schema and data types. Which AWS service should they use?",
            "options": [
                "Amazon Kinesis Data Analytics",
                "Amazon QuickSight with direct query",
                "AWS Glue with Data Catalog and ETL jobs",
                "Amazon Athena with federated queries",
                "AWS Data Pipeline with transformation activities"
            ],
            "answer": "AWS Glue with Data Catalog and ETL jobs"
        },
        {
            "question": "A financial services company wants to create interactive dashboards for their business users to visualize and explore their data. The solution needs to connect to multiple data sources, support scheduled data refreshes, and allow users to create their own visualizations without technical expertise. Which AWS service is most appropriate?",
            "options": [
                "Amazon CloudWatch Dashboards",
                "Amazon Managed Grafana",
                "Amazon QuickSight with self-service analytics",
                "AWS Amplify with charting libraries",
                "Amazon OpenSearch Dashboards"
            ],
            "answer": "Amazon QuickSight with self-service analytics"
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
                <h4>{topic.upper()} - Scenario {index+1}</h4>
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
                    already_correct = st.session_state.quiz_answers.get(topic, {}).get(answer_key, False)
                    
                    # Update tracking
                    st.session_state.quiz_attempted[topic] += 1
                    
                    if selected_answer == correct_answer and not already_correct:
                        st.success(f"✅ Correct! {correct_answer} is the right answer.")
                        st.session_state.quiz_scores[topic] += 1
                        if topic not in st.session_state.quiz_answers:
                            st.session_state.quiz_answers[topic] = {}
                        st.session_state.quiz_answers[topic][answer_key] = True
                    elif selected_answer == correct_answer and already_correct:
                        st.success(f"✅ Correct! {correct_answer} is the right answer.")
                    else:
                        st.error(f"❌ Incorrect. The correct answer is: {correct_answer}")
                        if topic not in st.session_state.quiz_answers:
                            st.session_state.quiz_answers[topic] = {}
                        st.session_state.quiz_answers[topic][answer_key] = False
        
        st.divider()

# Function for home page
def home_page():
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(aws_images["home"], width=300)
        except:
            st.error("Unable to load image")
    
    with col2:
        st.title("AWS Solutions Architect - Associate")
        st.header("Content Review - Session 4")
        st.markdown("""
        Welcome to the AWS Partner Certification Readiness program. This interactive guide will help you prepare 
        for the Solutions Architect - Associate certification. Navigate through the topics using the tabs above.
        
        Each section contains key concepts and important takeaways. Test your knowledge with the Knowledge Checks tab.
        """)
    
    st.markdown("""
    <div class="aws-info-card">
        <h3>Topics covered in Week 4:</h3>
        <ul>
            <li>AWS Elastic Block Store (EBS)</li>
            <li>IPv4 vs. IPv6 Addressing</li>
            <li>Elastic Load Balancer (ELB)</li>
            <li>Management and Governance Services</li>
            <li>AWS CloudFormation</li>
            <li>AWS Analytics Services</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="aws-success-card">
        <h3>Certification Preparation Tip</h3>
        <p>Practice hands-on with the services covered in this guide. 
        The AWS Solutions Architect - Associate exam focuses on practical knowledge of AWS services 
        and how they can be used together to design resilient, cost-effective solutions.</p>
    </div>
    """, unsafe_allow_html=True)

# Function for EBS page
def ebs_page():
    st.title("AWS Elastic Block Store (EBS)")
    
    try:
        st.image(aws_images["ebs"], width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is Amazon EBS?")
    st.markdown("""
    <div class="aws-card">
        <p>Amazon Elastic Block Store (EBS) provides persistent block-level storage volumes for use with Amazon EC2 instances. 
        EBS volumes are network-attached storage that persists independently from the life of an EC2 instance.</p>
        <h4>Key Features:</h4>
        <ul>
            <li>Persistent storage that survives instance termination</li>
            <li>Point-in-time snapshots stored in S3</li>
            <li>Encryption using AWS KMS</li>
            <li>Easily resizable without service disruption</li>
            <li>Attach to and detach from EC2 instances as needed</li>
            <li>Multiple volume types optimized for different workloads</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("EBS Volume Types")
    
    # Create columns for different EBS types
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h3>SSD-Backed Volumes</h3>
            <h4>General Purpose SSD (gp2/gp3)</h4>
            <ul>
                <li>Balance of price and performance</li>
                <li>3 IOPS/GB (up to 16,000 IOPS for gp2)</li>
                <li>gp3: Baseline 3,000 IOPS and 125 MiB/s</li>
                <li><strong>Use cases</strong>: Boot volumes, dev/test environments, low-latency interactive applications</li>
            </ul>
            <h4>Provisioned IOPS SSD (io1/io2)</h4>
            <ul>
                <li>Highest performance SSD volume</li>
                <li>Up to 64,000 IOPS per volume (io1), 256,000 IOPS (io2)</li>
                <li><strong>Use cases</strong>: I/O-intensive workloads, large databases, latency-sensitive applications</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h3>HDD-Backed Volumes</h3>
            <h4>Throughput Optimized HDD (st1)</h4>
            <ul>
                <li>Low-cost HDD designed for frequently accessed, throughput-intensive workloads</li>
                <li>Max throughput of 500 MiB/s per volume</li>
                <li><strong>Use cases</strong>: Big data, data warehouses, log processing</li>
            </ul>
            <h4>Cold HDD (sc1)</h4>
            <ul>
                <li>Lowest cost HDD for less frequently accessed workloads</li>
                <li>Max throughput of 250 MiB/s per volume</li>
                <li><strong>Use cases</strong>: Infrequently accessed data, archive storage</li>
            </ul>
            <h4>Magnetic (standard) - Previous Generation</h4>
            <ul>
                <li>Previous generation HDD</li>
                <li><strong>Use cases</strong>: Workloads where data is infrequently accessed</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Key Considerations")
    st.markdown("""
    <div class="aws-info-card">
        <h4>When choosing an EBS volume type, consider:</h4>
        <ol>
            <li><strong>Performance Requirements</strong>: IOPS vs. Throughput</li>
            <li><strong>Access Patterns</strong>: Random vs. Sequential access</li>
            <li><strong>Workload Characteristics</strong>: Read-heavy vs. Write-heavy</li>
            <li><strong>Data Criticality</strong>: Durability and availability needs</li>
            <li><strong>Cost Optimization</strong>: Balance performance and cost</li>
        </ol>
        <p>Remember that EBS volumes are AZ-specific - they can only be attached to EC2 instances in the same Availability Zone.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("EBS Snapshots")
    st.markdown("""
    <div class="aws-card">
        <h4>EBS Snapshots provide a way to back up and restore your EBS volumes:</h4>
        <ul>
            <li><strong>Incremental</strong>: Only the blocks that have changed since the last snapshot are saved</li>
            <li><strong>S3 Storage</strong>: Snapshots are stored in Amazon S3 (not visible in your S3 buckets)</li>
            <li><strong>Region-specific</strong>: Snapshots are region-specific but can be copied across regions</li>
            <li><strong>Sharing</strong>: Snapshots can be shared with other AWS accounts or made public</li>
            <li><strong>Automation</strong>: AWS Backup can be used to manage and automate snapshots</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Function for IPv4 vs. IPv6 page
def ip_addressing_page():
    st.title("IPv4 vs. IPv6 Addressing")
    
    try:
        st.image(aws_images["ipv4"], width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("IP Addressing in AWS")
    st.markdown("""
    <div class="aws-card">
        <p>AWS supports both IPv4 and IPv6 addressing protocols. Understanding IP addressing is crucial for designing 
        VPC networks, managing connectivity, and ensuring proper routing.</p>
        <h4>Key Points:</h4>
        <ul>
            <li>By default, all AWS VPCs use IPv4 addressing</li>
            <li>IPv6 support can be added optionally to VPCs and subnets</li>
            <li>IPv4 and IPv6 can be used simultaneously in a VPC (dual-stack)</li>
            <li>Proper IP addressing planning is critical for future growth and connectivity</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Create columns for IPv4 and IPv6
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h3>IPv4 Addressing</h3>
            <h4>IPv4 in AWS:</h4>
            <ul>
                <li>Required for all VPCs</li>
                <li>CIDR block range: /16 (65,536 IPs) to /28 (16 IPs)</li>
                <li>Uses RFC 1918 private IP ranges:
                    <ul>
                        <li>10.0.0.0/8</li>
                        <li>172.16.0.0/12</li>
                        <li>192.168.0.0/16</li>
                    </ul>
                </li>
            </ul>
            <h4>Subnet Reserves:</h4>
            <ul>
                <li>First 4 IPs and last IP in each subnet are reserved</li>
                <li>Example for 10.0.1.0/24:
                    <ul>
                        <li>10.0.1.0: Network address</li>
                        <li>10.0.1.1: VPC router</li>
                        <li>10.0.1.2: DNS resolver</li>
                        <li>10.0.1.3: Reserved for future use</li>
                        <li>10.0.1.255: Broadcast address</li>
                    </ul>
                </li>
            </ul>
            <h4>Public IPv4:</h4>
            <ul>
                <li>Assigned via Elastic IP or auto-assigned public IP</li>
                <li>Mapped to private IP through NAT</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h3>IPv6 Addressing</h3>
            <h4>IPv6 in AWS:</h4>
            <ul>
                <li>Optional addition to VPCs</li>
                <li>AWS assigns a /56 CIDR block to the VPC</li>
                <li>Subnets receive a /64 CIDR block</li>
                <li>All IPv6 addresses in AWS are publicly routable</li>
            </ul>
            <h4>IPv6 Features:</h4>
            <ul>
                <li>No need for NAT - direct routing to internet</li>
                <li>Globally unique addresses</li>
                <li>Simpler address management</li>
                <li>Future-proof as IPv4 addresses become scarce</li>
            </ul>
            <h4>IPv6-only Subnets:</h4>
            <ul>
                <li>EC2 instances can be launched with IPv6-only configuration</li>
                <li>Requires specific instance types and AMIs</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("IP Addressing Best Practices")
    st.markdown("""
    <div class="aws-info-card">
        <h4>VPC Design Considerations:</h4>
        <ol>
            <li><strong>Plan your CIDR blocks carefully</strong> - consider future growth and potential connections to other networks</li>
            <li><strong>Avoid overlapping IP ranges</strong> with:
                <ul>
                    <li>On-premises networks you might connect to</li>
                    <li>Partner networks you might connect to</li>
                    <li>Other VPCs you might peer with</li>
                </ul>
            </li>
            <li><strong>Subnet sizing</strong> - create appropriately sized subnets based on expected workload</li>
            <li><strong>Consider IPv6</strong> for new deployments to avoid IPv4 address constraints</li>
            <li><strong>Reserve IP space</strong> for different environments (dev, test, prod) and different applications</li>
            <li><strong>Document your IP addressing scheme</strong> to avoid confusion and conflicts</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("VPC IP Addressing Limitations")
    st.markdown("""
    <div class="aws-warning-card">
        <h4>Important Limitations to Remember:</h4>
        <ul>
            <li>Cannot change the primary IPv4 CIDR block after creating a VPC</li>
            <li>Can add secondary CIDR blocks to expand a VPC</li>
            <li>Maximum of 5 CIDR blocks per VPC (primary + 4 secondary)</li>
            <li>Maximum of 200 subnets per VPC</li>
            <li>Subnet size cannot be changed after creation</li>
            <li>Each EC2 instance receives a primary private IPv4 address from the subnet range</li>
            <li>IPv6 addresses are assigned from Amazon's pool (cannot bring your own)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Function for ELB page
def elb_page():
    st.title("Elastic Load Balancing (ELB)")
    
    try:
        st.image(aws_images["elb"], width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is Elastic Load Balancing?")
    st.markdown("""
    <div class="aws-card">
        <p>Elastic Load Balancing automatically distributes incoming application traffic across multiple targets, 
        such as EC2 instances, containers, and IP addresses. It can handle the varying load of your application 
        traffic in a single Availability Zone or across multiple Availability Zones.</p>
        <h4>Key Benefits:</h4>
        <ul>
            <li>High availability and fault tolerance</li>
            <li>Elastic scaling based on traffic</li>
            <li>Security features with integrated certificate management</li>
            <li>Health checking and monitoring</li>
            <li>Integration with AWS services like Auto Scaling</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("ELB Types")
    
    # Create tabs for different ELB types
    tab1, tab2, tab3, tab4 = st.tabs(["Application Load Balancer", "Network Load Balancer", "Gateway Load Balancer", "Classic Load Balancer"])
    
    with tab1:
        st.subheader("Application Load Balancer (ALB)")
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Layer 7 (Application Layer) Load Balancer</h4>
            <h5>Key Features:</h5>
            <ul>
                <li>Content-based routing (path, host, HTTP headers, query parameters)</li>
                <li>Support for HTTP/HTTPS/gRPC protocols</li>
                <li>WebSockets and HTTP/2 support</li>
                <li>Request tracing and access logs</li>
                <li>Integration with AWS WAF and AWS Cognito</li>
            </ul>
            <h5>Best For:</h5>
            <ul>
                <li>Microservices and container-based applications</li>
                <li>Applications requiring advanced routing</li>
                <li>Applications with HTTP/HTTPS traffic</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.image("https://d1.awsstatic.com/Digital%20Marketing/House/Hero/products/EC2/ALB-diagram.09d8e791b316c68d3ff0c3bfb7fbfb4c24e6d56a.png", width=600)
    
    with tab2:
        st.subheader("Network Load Balancer (NLB)")
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Layer 4 (Transport Layer) Load Balancer</h4>
            <h5>Key Features:</h5>
            <ul>
                <li>Ultra-high performance and low latency</li>
                <li>Handles millions of requests per second</li>
                <li>Static IP addresses per AZ</li>
                <li>Preserve source IP address</li>
                <li>Support for TCP, UDP, and TLS protocols</li>
            </ul>
            <h5>Best For:</h5>
            <ul>
                <li>Extreme performance requirements</li>
                <li>Static IP requirements</li>
                <li>Applications using protocols beyond HTTP/HTTPS</li>
                <li>Use with PrivateLink for exposing services</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.image("https://d1.awsstatic.com/products/load-balancing/Network-Load-Balancer.5200501ae919b50163c201133c2374ec52bbd2a3.png", width=600)
    
    with tab3:
        st.subheader("Gateway Load Balancer (GLB)")
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Layer 3/4 (Network Layer) Gateway and Load Balancer</h4>
            <h5>Key Features:</h5>
            <ul>
                <li>Deploy, scale, and manage virtual appliances</li>
                <li>Transparent network gateway</li>
                <li>Load balancing for security appliances</li>
                <li>Uses GENEVE protocol (port 6081)</li>
                <li>Preserves original network packets</li>
            </ul>
            <h5>Best For:</h5>
            <ul>
                <li>Security appliances (firewalls, IDS/IPS)</li>
                <li>Network traffic inspection</li>
                <li>Third-party virtual appliances</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.image("https://d1.awsstatic.com/products/gateway-load-balancer/Product-Page-Diagram_Gateway-Load-Balancer%402x.4c5a2078bc33ba239c8d12183e0cce6322c83d36.png", width=600)
    
    with tab4:
        st.subheader("Classic Load Balancer (CLB)")
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Legacy Load Balancer for EC2-Classic Network</h4>
            <h5>Key Features:</h5>
            <ul>
                <li>Layer 4 and basic Layer 7 features</li>
                <li>Support for TCP/SSL/HTTP/HTTPS</li>
                <li>Sticky sessions using cookies</li>
                <li>Only health check is TCP or HTTP/HTTPS</li>
            </ul>
            <h5>Best For:</h5>
            <ul>
                <li>Legacy applications built on the EC2-Classic network</li>
                <li>Simple load balancing with minimal features</li>
                <li>Applications that require TCP passthrough with Layer 7 features</li>
            </ul>
            <div class="aws-warning-card">
                <p><strong>Note:</strong> AWS recommends using newer load balancer types for all new applications</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("ELB Common Features")
    st.markdown("""
    <div class="aws-card">
        <h4>Features Available Across ELB Types:</h4>
        <ol>
            <li><strong>Health Checks</strong>: Monitor the health of registered targets and route traffic only to healthy targets</li>
            <li><strong>Security Groups</strong>: Control inbound and outbound traffic (except GWLB)</li>
            <li><strong>SSL/TLS Termination</strong>: Offload encryption/decryption to the load balancer (ALB, NLB, CLB)</li>
            <li><strong>CloudWatch Integration</strong>: Monitor load balancer performance with metrics</li>
            <li><strong>Access Logs</strong>: Capture detailed information about requests (ALB, CLB)</li>
            <li><strong>Cross-Zone Load Balancing</strong>: Distribute traffic evenly across all targets regardless of AZ</li>
            <li><strong>Connection Draining/Deregistration Delay</strong>: Complete in-flight requests during target deregistration</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Load Balancing Best Practices")
    st.markdown("""
    <div class="aws-success-card">
        <h4>Architectural Recommendations:</h4>
        <ol>
            <li><strong>Multi-AZ Deployment</strong>: Deploy targets in multiple AZs for high availability</li>
            <li><strong>Right-Sizing</strong>: Ensure sufficient targets to handle peak load plus margin</li>
            <li><strong>Pre-Warming</strong>: Contact AWS for expected traffic spikes beyond normal patterns</li>
            <li><strong>Security</strong>: Apply security groups to control traffic to/from load balancers</li>
            <li><strong>Monitoring</strong>: Set up CloudWatch alarms for key metrics</li>
            <li><strong>Health Checks</strong>: Configure appropriate health checks that verify application health</li>
            <li><strong>Choose the Right Type</strong>: Select the appropriate load balancer type based on application requirements</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Function for Management and Governance page
def management_page():
    st.title("Management and Governance")
    
    st.header("AWS Management and Monitoring Services")
    st.markdown("""
    <div class="aws-card">
        <p>AWS provides a comprehensive set of tools for managing, monitoring, and governing your AWS resources. 
        These services help you maintain operational excellence, ensure compliance, and optimize your infrastructure.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # CloudTrail section
    st.subheader("AWS CloudTrail")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(aws_images["cloudtrail"], width=300)
        except:
            st.warning("CloudTrail image could not be displayed")
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>What is CloudTrail?</h4>
            <p>AWS CloudTrail is a service that provides event history of your AWS account activity, including actions 
            taken through the AWS Management Console, AWS SDKs, command line tools, and other AWS services.</p>
            <h5>Key Features:</h5>
            <ul>
                <li>Records API calls across AWS services</li>
                <li>Maintains event history for 90 days</li>
                <li>Delivers log files to S3 for long-term storage</li>
                <li>Validates log file integrity</li>
                <li>Integrates with CloudWatch Logs for monitoring</li>
            </ul>
            <h5>Use Cases:</h5>
            <ul>
                <li>Security analysis and compliance auditing</li>
                <li>Resource change tracking</li>
                <li>Troubleshooting operational issues</li>
                <li>Identifying unauthorized access</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # CloudWatch section
    st.subheader("Amazon CloudWatch")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(aws_images["cloudwatch"], width=300)
        except:
            st.warning("CloudWatch image could not be displayed")
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>What is CloudWatch?</h4>
            <p>Amazon CloudWatch is a monitoring and observability service that provides data and actionable 
            insights for AWS, hybrid, and on-premises applications and infrastructure resources.</p>
            <h5>Key Features:</h5>
            <ul>
                <li>Collects and tracks metrics</li>
                <li>Collects and monitors log files</li>
                <li>Sets alarms and creates triggers to automate actions</li>
                <li>Custom dashboards for visualization</li>
                <li>Anomaly detection using machine learning</li>
            </ul>
            <h5>Use Cases:</h5>
            <ul>
                <li>Application performance monitoring</li>
                <li>Resource utilization tracking</li>
                <li>Operational health insights</li>
                <li>Setting up automated actions based on defined thresholds</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # AWS Config section
    st.subheader("AWS Config")
    st.markdown("""
    <div class="aws-feature-card">
        <h4>What is AWS Config?</h4>
        <p>AWS Config is a service that enables you to assess, audit, and evaluate the configurations of your 
        AWS resources. It continuously monitors and records AWS resource configurations and allows 
        automated evaluation of recorded configurations against desired configurations.</p>
        <h5>Key Features:</h5>
        <ul>
            <li>Resource inventory and configuration history</li>
            <li>Configuration change notifications</li>
            <li>Relationship mapping between resources</li>
            <li>Compliance auditing against rules and policies</li>
            <li>Automated remediation actions</li>
        </ul>
        <h5>Use Cases:</h5>
        <ul>
            <li>Compliance auditing</li>
            <li>Security analysis</li>
            <li>Resource change tracking</li>
            <li>Troubleshooting</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("Comparing Management Services")
    
    comparison_data = {
        "Service": ["CloudTrail", "CloudWatch", "Config"],
        "Primary Function": ["Records API activity", "Monitors resources and applications", "Records resource configurations"],
        "Focus Area": ["Who did what, when", "Performance and operations", "What changed and when"],
        "Use When You Need": ["Audit trail of actions taken in your AWS account", "Metrics, logs, and automated responses to changes", "Track resource configuration changes over time"]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df.set_index("Service"), use_container_width=True)
    
    st.header("Integration Between Services")
    st.markdown("""
    <div class="aws-info-card">
        <h4>These services work together to provide comprehensive management capabilities:</h4>
        <ol>
            <li><strong>CloudTrail + CloudWatch</strong>: Send CloudTrail events to CloudWatch Logs for monitoring and alarming</li>
            <li><strong>CloudWatch + Auto Scaling</strong>: Use CloudWatch metrics to trigger Auto Scaling actions</li>
            <li><strong>CloudTrail + Config</strong>: Use CloudTrail to detect who made configuration changes tracked by Config</li>
            <li><strong>Config + Lambda</strong>: Use Lambda functions to automatically remediate non-compliant resources</li>
            <li><strong>CloudWatch + SNS</strong>: Send notifications when CloudWatch alarms are triggered</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Function for CloudFormation page
def cloudformation_page():
    st.title("AWS CloudFormation")
    
    try:
        st.image(aws_images["cloudformation"], width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is AWS CloudFormation?")
    st.markdown("""
    <div class="aws-card">
        <p>AWS CloudFormation is an infrastructure as code (IaC) service that allows you to model, provision, and 
        manage AWS and third-party resources by treating infrastructure as code.</p>
        <h4>Key Benefits:</h4>
        <ul>
            <li>Define infrastructure in template files (JSON or YAML)</li>
            <li>Automate and simplify resource provisioning and updates</li>
            <li>Version control your infrastructure alongside application code</li>
            <li>Reproducible environments across regions and accounts</li>
            <li>Free to use (pay only for resources created)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Core Concepts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h3>Templates</h3>
            <h4>CloudFormation Templates:</h4>
            <ul>
                <li>JSON or YAML formatted text files</li>
                <li>Describe the AWS resources to build</li>
                <li>Can include parameters for customization</li>
                <li>Key sections:
                    <ul>
                        <li>Resources (required)</li>
                        <li>Parameters (optional)</li>
                        <li>Mappings (optional)</li>
                        <li>Conditions (optional)</li>
                        <li>Outputs (optional)</li>
                    </ul>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.code("""
        AWSTemplateFormatVersion: '2010-09-09'
        Description: 'Simple EC2 instance'
        
        Resources:
          MyEC2Instance:
            Type: AWS::EC2::Instance
            Properties:
              InstanceType: t2.micro
              ImageId: ami-0abcdef1234567890
              SecurityGroups:
                - !Ref InstanceSecurityGroup
                
          InstanceSecurityGroup:
            Type: AWS::EC2::SecurityGroup
            Properties:
              GroupDescription: Enable SSH access
              SecurityGroupIngress:
              - IpProtocol: tcp
                FromPort: 22
                ToPort: 22
                CidrIp: 0.0.0.0/0
        """, language="yaml")
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h3>Stacks</h3>
            <h4>CloudFormation Stacks:</h4>
            <ul>
                <li>Collection of AWS resources managed as a single unit</li>
                <li>Created, updated, and deleted together</li>
                <li>Resources in a stack are defined by the template</li>
                <li>Stack operations:
                    <ul>
                        <li>Create-stack</li>
                        <li>Update-stack</li>
                        <li>Delete-stack</li>
                    </ul>
                </li>
            </ul>
            <h4>Stack Features:</h4>
            <ul>
                <li>Automatic rollbacks on errors</li>
                <li>Drift detection</li>
                <li>Stack policies to protect resources</li>
                <li>Change sets to preview updates</li>
                <li>Nested stacks for reusable components</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.image("https://docs.aws.amazon.com/images/AWSCloudFormation/latest/UserGuide/images/update-stack-changesets-diagram.png", width=400)
    
    st.header("CloudFormation vs. Elastic Beanstalk")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h3>AWS CloudFormation</h3>
            <ul>
                <li>General-purpose infrastructure as code</li>
                <li>Provides complete control over all resource types</li>
                <li>Requires defining all resources and their relationships</li>
                <li>Supports many AWS resources and third-party extensions</li>
            </ul>
            <p><strong>When to use:</strong> When you need fine-grained control over all infrastructure resources</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h3>AWS Elastic Beanstalk</h3>
            <ul>
                <li>Platform as a Service (PaaS) focused on applications</li>
                <li>Simplifies deployment of applications</li>
                <li>Handles infrastructure details automatically</li>
                <li>Limited to specific application types and patterns</li>
                <li>Uses CloudFormation behind the scenes</li>
            </ul>
            <p><strong>When to use:</strong> When you want to focus on your application code rather than infrastructure</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Change Sets and Updates")
    st.markdown("""
    <div class="aws-info-card">
        <h4>Stack Updates:</h4>
        <p>When updating a CloudFormation stack, you can:</p>
        <ol>
            <li><strong>Direct Update:</strong> Submit changed template or parameter values
                <ul>
                    <li>CloudFormation updates only the changed resources</li>
                    <li>Automatic rollback if update fails</li>
                </ul>
            </li>
            <li><strong>Change Sets:</strong> Preview changes before execution
                <ul>
                    <li>Create multiple change sets to explore options</li>
                    <li>Review potential impacts before implementing changes</li>
                    <li>Execute the chosen change set when ready</li>
                </ul>
            </li>
        </ol>
        <h4>Update Behaviors:</h4>
        <p>Resources are updated in different ways depending on the property changes:</p>
        <ul>
            <li><strong>No Interruption:</strong> Updates without disrupting the resource or changing physical ID</li>
            <li><strong>Some Interruption:</strong> Updates with possible disruption but preserves physical ID</li>
            <li><strong>Replacement:</strong> Creates a new resource with a new physical ID</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Nested Stacks")
    st.markdown("""
    <div class="aws-card">
        <h4>What are Nested Stacks?</h4>
        <p>Nested stacks are stacks created as part of other stacks. They allow you to decompose complex templates into smaller, reusable components.</p>
        <h4>Benefits:</h4>
        <ul>
            <li><strong>Modularity:</strong> Break down complex architectures into manageable pieces</li>
            <li><strong>Reusability:</strong> Create common patterns once and reuse them</li>
            <li><strong>Maintenance:</strong> Update components independently</li>
        </ul>
        <h4>Implementation:</h4>
        <ul>
            <li>Use the <code>AWS::CloudFormation::Stack</code> resource type</li>
            <li>Specify the template URL (must be stored in S3)</li>
            <li>Pass parameters from parent stack to nested stack</li>
        </ul>
        <h4>Considerations:</h4>
        <ul>
            <li>Nested stacks are created, updated, and deleted with the parent stack</li>
            <li>Maximum nesting depth of 10 levels</li>
            <li>Changes to nested stacks affect the parent stack</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Function for Analytics Services page
def analytics_page():
    st.title("AWS Analytics Services")
    
    st.header("Overview of AWS Analytics Services")
    st.markdown("""
    <div class="aws-card">
        <p>AWS offers a comprehensive suite of analytics services to help you collect, process, analyze, 
        and visualize data at any scale. These services enable you to build sophisticated data analytics 
        and machine learning solutions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Amazon Athena
    st.subheader("Amazon Athena")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(aws_images["athena"], width=300)
        except:
            st.warning("Athena image could not be displayed")
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>What is Amazon Athena?</h4>
            <p>An interactive query service that makes it easy to analyze data in Amazon S3 using standard SQL. 
            Athena is serverless, so there is no infrastructure to manage.</p>
            <h5>Key Features:</h5>
            <ul>
                <li>Serverless query service - no clusters to manage</li>
                <li>Pay per query - only for data scanned</li>
                <li>Built on Presto and supports ANSI SQL</li>
                <li>Works with data in S3 in various formats (CSV, JSON, ORC, Parquet, Avro)</li>
                <li>Integrates with AWS Glue Data Catalog</li>
            </ul>
            <h5>Use Cases:</h5>
            <ul>
                <li>Ad-hoc data exploration</li>
                <li>Log analysis</li>
                <li>Business intelligence reporting</li>
                <li>SQL-based queries on S3 data</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Amazon OpenSearch Service
    st.subheader("Amazon OpenSearch Service")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(aws_images["opensearch"], width=300)
        except:
            st.warning("OpenSearch image could not be displayed")
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>What is Amazon OpenSearch Service?</h4>
            <p>A managed service that makes it easy to deploy, operate, and scale OpenSearch clusters in the AWS Cloud. 
            OpenSearch is a fork of Elasticsearch.</p>
            <h5>Key Features:</h5>
            <ul>
                <li>Fully managed search and analytics engine</li>
                <li>Visualization capabilities with OpenSearch Dashboards</li>
                <li>Scales with your data volume</li>
                <li>Integrated security and access controls</li>
                <li>Automated snapshots for backup</li>
            </ul>
            <h5>Use Cases:</h5>
            <ul>
                <li>Log and infrastructure monitoring</li>
                <li>Security information and event management (SIEM)</li>
                <li>Full-text search capabilities</li>
                <li>Real-time application monitoring</li>
                <li>Clickstream analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Amazon EMR
    st.subheader("Amazon EMR")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(aws_images["emr"], width=300)
        except:
            st.warning("EMR image could not be displayed")
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>What is Amazon EMR?</h4>
            <p>A managed cluster platform that simplifies running big data frameworks like Apache Hadoop, Apache Spark, 
            and Presto on AWS to process and analyze vast amounts of data.</p>
            <h5>Key Features:</h5>
            <ul>
                <li>Managed cluster environment for big data processing</li>
                <li>Support for multiple frameworks (Hadoop, Spark, Hive, Presto, etc.)</li>
                <li>Flexible deployment options (on EC2, on EKS, or serverless)</li>
                <li>Automatic scaling based on workload</li>
                <li>Integration with AWS services like S3, DynamoDB, and Kinesis</li>
            </ul>
            <h5>Use Cases:</h5>
            <ul>
                <li>Big data processing</li>
                <li>Machine learning</li>
                <li>Interactive SQL queries</li>
                <li>Data transformations</li>
                <li>Scientific simulations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # AWS Glue
    st.subheader("AWS Glue")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(aws_images["glue"], width=300)
        except:
            st.warning("Glue image could not be displayed")
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>What is AWS Glue?</h4>
            <p>A serverless data integration service that makes it easy to discover, prepare, and combine data 
            for analytics, machine learning, and application development.</p>
            <h5>Key Features:</h5>
            <ul>
                <li>Serverless ETL (Extract, Transform, Load) service</li>
                <li>Automated schema discovery and data cataloging</li>
                <li>Visual ETL job development</li>
                <li>Job scheduling and monitoring</li>
                <li>Built-in transforms for data cleaning and enrichment</li>
            </ul>
            <h5>Use Cases:</h5>
            <ul>
                <li>Data preparation for analytics</li>
                <li>Building data lakes</li>
                <li>Creating ETL pipelines</li>
                <li>Cataloging data from multiple sources</li>
                <li>Streaming ETL for real-time data</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Amazon QuickSight
    st.subheader("Amazon QuickSight")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(aws_images["quicksight"], width=300)
        except:
            st.warning("QuickSight image could not be displayed")
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>What is Amazon QuickSight?</h4>
            <p>A cloud-native business intelligence service that makes it easy to create and publish interactive 
            dashboards and data visualizations.</p>
            <h5>Key Features:</h5>
            <ul>
                <li>Machine learning-powered insights</li>
                <li>Serverless architecture that scales automatically</li>
                <li>Pay-per-session pricing model</li>
                <li>Embedded analytics capabilities</li>
                <li>Integration with various data sources</li>
            </ul>
            <h5>Use Cases:</h5>
            <ul>
                <li>Business intelligence dashboards</li>
                <li>Ad hoc data analysis</li>
                <li>Embedded analytics in applications</li>
                <li>Automated business insights</li>
                <li>Interactive data reporting</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Choosing the Right Analytics Service")
    st.markdown("""
    <div class="aws-info-card">
        <h4>Decision Factors:</h4>
        <ol>
            <li><strong>Data Volume and Velocity:</strong>
                <ul>
                    <li>For massive datasets or streaming data → EMR or Kinesis</li>
                    <li>For moderate data with SQL needs → Athena</li>
                    <li>For real-time analytics → OpenSearch or Kinesis</li>
                </ul>
            </li>
            <li><strong>Query Types:</strong>
                <ul>
                    <li>For ad-hoc SQL queries → Athena</li>
                    <li>For full-text search and log analysis → OpenSearch</li>
                    <li>For complex big data processing → EMR</li>
                </ul>
            </li>
            <li><strong>Integration Requirements:</strong>
                <ul>
                    <li>For data catalog and ETL → AWS Glue</li>
                    <li>For visualization needs → QuickSight</li>
                    <li>For building a data lake → Combination of S3, Glue, and Athena</li>
                </ul>
            </li>
            <li><strong>Operational Complexity:</strong>
                <ul>
                    <li>For minimal management → Serverless options like Athena and Glue</li>
                    <li>For control over the environment → EMR</li>
                    <li>For managed search service → OpenSearch Service</li>
                </ul>
            </li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Common Analytics Architectures")
    st.markdown("""
    <div class="aws-card">
        <h4>Data Lake Architecture:</h4>
        <ol>
            <li>Ingest data to S3 (raw zone)</li>
            <li>Catalog metadata with AWS Glue</li>
            <li>Transform data with Glue ETL</li>
            <li>Store processed data in S3 (processed zone)</li>
            <li>Query with Athena or EMR</li>
            <li>Visualize with QuickSight</li>
        </ol>
        <h4>Log Analytics Architecture:</h4>
        <ol>
            <li>Collect logs with CloudWatch Logs or Kinesis</li>
            <li>Store logs in S3</li>
            <li>Index logs in OpenSearch Service</li>
            <li>Analyze with OpenSearch Dashboards</li>
            <li>Set up alerts for anomalies</li>
        </ol>
        <h4>Batch Processing Architecture:</h4>
        <ol>
            <li>Store raw data in S3</li>
            <li>Process with EMR using Spark or Hadoop</li>
            <li>Load results to data warehouse or S3</li>
            <li>Query with Athena or Redshift</li>
            <li>Create reports with QuickSight</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Function for Knowledge Checks page
def knowledge_checks_page():
    st.title("Knowledge Checks")
    
    st.markdown("""
    <div class="aws-info-card">
        <h3>Test your knowledge</h3>
        <p>Answer the scenario-based questions below to check your understanding. Your progress is tracked automatically.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for each topic's quizzes
    tabs = st.tabs([
        "EBS", 
        "IPv4 Addressing", 
        "Load Balancers", 
        "Management", 
        "CloudFormation", 
        "Analytics"
    ])
    
    topic_keys = ["ebs", "ipv4", "elb", "management", "cloudformation", "analytics"]
    
    # Loop through tabs and display corresponding quizzes
    for i, tab in enumerate(tabs):
        with tab:
            topic = topic_keys[i]
            st.header(f"{topic.upper()} Knowledge Check")
            
            if topic in quiz_data:
                for j, quiz in enumerate(quiz_data[topic]):
                    handle_quiz(topic, j, quiz)
    
    # Progress Summary
    st.header("Your Progress")
    
    # Display chart if there's data
    chart = create_quiz_results_chart()
    if chart:
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Complete some knowledge checks to see your progress!")
    
    # Calculate and display overall progress
    total_attempted = sum(st.session_state.quiz_attempted.values()) if st.session_state.quiz_attempted else 0
    total_correct = sum(st.session_state.quiz_scores.values()) if st.session_state.quiz_scores else 0
    
    if total_attempted > 0:
        percentage = int((total_correct / total_attempted) * 100)
        
        st.markdown(f"""
        <div class="aws-success-card">
            <h3>Overall Score: {total_correct}/{total_attempted} ({percentage}%)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar
        st.progress(total_correct / total_attempted)

# Session management in sidebar
st.sidebar.subheader("⚙️ Session Management")

# Reset button
if st.sidebar.button("🔄 Reset Quiz Data", key="reset_button"):
    reset_session()

# Show session ID
st.sidebar.caption(f"Session ID: {st.session_state.session_id[:8]}...")

# Main tabs navigation with emojis
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🏠 Home",
    "💽 EBS",
    "🔢 IP Addressing",
    "⚖️ Load Balancing",
    "🛠️ Management",
    "📐 CloudFormation",
    "📊 Analytics",
    "📝 Knowledge Checks"
])

# Content for each tab
with tab1:
    home_page()

with tab2:
    ebs_page()

with tab3:
    ip_addressing_page()

with tab4:
    elb_page()

with tab5:
    management_page()

with tab6:
    cloudformation_page()

with tab7:
    analytics_page()

with tab8:
    knowledge_checks_page()

# Footer
st.markdown("""
<div class="footer">
    © 2025 AWS Partner Certification Readiness. This application is designed to help you prepare for the AWS Solutions Architect - Associate certification.
</div>
""", unsafe_allow_html=True)
