
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

# Define AWS stock images URLs
aws_images = {
    "home": "https://d1.awsstatic.com/training-and-certification/certification-badges/AWS-Certified-Solutions-Architect-Associate_badge.3419559c682629072f1eb968d59dea0741772c0f.png",
    "sqs": "images/sqs.png",
    "sns": "images/sns1.png",
    "eventbridge": "images/eb.png",
    "lambda": "images/lambda.png",
    "api_gateway": "images/apigw.png",
    "containers": "images/container_on_aws.png",
    "ecs": "images/ecs.png",
    "eks": "images/eks.png",
    "fargate": "images/fargate.png",
    "secrets_manager": "images/secret_manager.png",
    "acm": "images/acm.png",
    "patch_manager": "images/patch_manager.tif",
    "iam_identity_center": "images/iam_identity_center.png",
    "security_catalog": "images/security_catalog.png",
    "directory_service": "images/directory_service.png",
    "ram": "images/ram.png",
    "cognito": "images/cognito.png",
    "analytics": "images/analytics-services.png",
    "ml": "images/ml_stack.jpg"
}

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

# Scenario-based quiz questions
quiz_data = {
    "sqs": [
        {
            "question": "A company has developed a multi-tier web application where the front-end sends requests to a backend processing service. During sales events, the application experiences high traffic that sometimes overwhelms the backend processing. The company wants to implement a solution that can handle traffic spikes without losing requests, while ensuring that all requests are processed exactly in the order they were received, with no duplicates. Which Amazon SQS configuration would best meet these requirements?",
            "options": [
                "Standard SQS queue with long polling",
                "Standard SQS queue with visibility timeout set to 12 hours",
                "FIFO SQS queue with content-based deduplication enabled",
                "FIFO SQS queue with message retention period set to maximum",
                "Standard SQS queue with dead-letter queue configured"
            ],
            "answer": "FIFO SQS queue with content-based deduplication enabled"
        },
        {
            "question": "A financial services application processes customer transactions through an SQS queue. Each transaction must be processed exactly once, and the processing time can vary from seconds to minutes. Occasionally, the processing service fails and needs to restart. What is the best approach to ensure no messages are lost while preventing duplicate processing?",
            "options": [
                "Set a visibility timeout that exceeds the maximum processing time and delete messages after successful processing",
                "Use a Standard queue with short polling to continuously check for new messages",
                "Process messages directly without using SQS to avoid visibility timeout issues",
                "Use multiple queues and route messages based on processing time estimates",
                "Set up automatic forwarding to a dead-letter queue after one failed processing attempt"
            ],
            "answer": "Set a visibility timeout that exceeds the maximum processing time and delete messages after successful processing"
        },
        {
            "question": "A media company has an application that uploads user-generated content for processing. They use Amazon SQS to decouple the upload from the processing components. Recently, users have complained about duplicate processing of some content. The development team has discovered that occasionally, a processing node crashes after retrieving a message but before completing the work. What combination of actions should they take to resolve this issue while ensuring all content is processed?",
            "options": [
                "Switch to a FIFO queue and enable content-based deduplication",
                "Implement idempotent processing logic and increase the visibility timeout based on processing time analysis",
                "Add more processing servers and reduce the message retention period",
                "Enable long polling and automatically forward unprocessed messages to a dead-letter queue",
                "Use message attributes to track processing status and implement custom deduplication logic"
            ],
            "answer": "Implement idempotent processing logic and increase the visibility timeout based on processing time analysis"
        },
        {
            "question": "An e-commerce company processes orders through a distributed system. They want to ensure that all order processing components can continue working independently even if one component fails temporarily. They also need to handle sudden spikes in order volume during flash sales. The solution should minimize the risk of data loss and be cost-effective. Which approach best meets these requirements?",
            "options": [
                "Use Amazon SNS to broadcast orders to multiple processing services simultaneously",
                "Implement a standard SQS queue with a large message retention period and auto-scaling based on queue depth",
                "Use Amazon MQ with persistent messaging and configure high availability across multiple AZs",
                "Implement a direct connection between services using Amazon API Gateway",
                "Use Amazon EventBridge with custom event buses for each processing component"
            ],
            "answer": "Implement a standard SQS queue with a large message retention period and auto-scaling based on queue depth"
        },
        {
            "question": "A company is building a data processing pipeline that requires messages to be processed in sequence for each customer, but processing can happen in parallel across different customers. The system must also handle occasional duplicate submissions from the front-end application without processing them twice. The average processing time is 30 seconds, but can sometimes take up to 2 minutes. Which combination of SQS features and configurations would be most effective?",
            "options": [
                "Standard queue with message groups defined by customer ID and server-side deduplication",
                "FIFO queue with message group IDs set to customer ID and content-based deduplication enabled",
                "Standard queue with message attributes for customer IDs and client-side deduplication logic",
                "Multiple standard queues, one per customer, with a router function to distribute messages",
                "FIFO queue with a single message group and custom visibility timeout extensions"
            ],
            "answer": "FIFO queue with message group IDs set to customer ID and content-based deduplication enabled"
        }
    ],
    "sns": [
        {
            "question": "A global retail company wants to implement a notification system that sends order updates to customers through their preferred communication channels (SMS, email, or mobile push notifications). The solution needs to support millions of customers and must be reliable, scalable, and cost-effective. Which approach using Amazon SNS would best meet these requirements?",
            "options": [
                "Create a single SNS topic with all customers as subscribers, using filter policies based on customer preferences",
                "Create multiple SNS topics, one for each communication channel, and subscribe customers based on preferences",
                "Create a separate SNS topic for each customer with subscriptions based on their preferred channels",
                "Use SNS with Amazon SQS queues as subscribers, then process and route messages based on customer preferences",
                "Use SNS FIFO topics to ensure ordered delivery of notifications to each customer"
            ],
            "answer": "Create multiple SNS topics, one for each communication channel, and subscribe customers based on preferences"
        },
        {
            "question": "A financial services application needs to notify various downstream systems when account transactions occur. Each transaction should be processed by multiple services including fraud detection, account balance updates, customer notification, and audit logging. Some services require immediate notification while others can process transactions in batches. What is the most efficient architecture using Amazon SNS?",
            "options": [
                "Create multiple SNS topics for different transaction types with all services subscribing to relevant topics",
                "Create a single SNS topic for all transactions with SQS queues as subscribers for services that need batch processing",
                "Use SNS message filtering with a single topic, allowing each service to receive only the transactions they need to process",
                "Implement direct service-to-service communication using API Gateway instead of SNS to ensure reliable delivery",
                "Use SNS FIFO topics with message deduplication to prevent duplicate transaction processing"
            ],
            "answer": "Create a single SNS topic for all transactions with SQS queues as subscribers for services that need batch processing"
        },
        {
            "question": "A healthcare company has developed a patient monitoring system that needs to notify medical staff when vital signs reach critical thresholds. Different types of alerts need to be sent to different teams based on severity and the type of medical issue. The system must be highly available, deliver notifications with minimal latency, and maintain patient privacy. Which SNS implementation would best meet these requirements?",
            "options": [
                "Use a single SNS topic with message attributes for alert details and implement client-side filtering",
                "Create separate SNS topics for each alert type and severity level with appropriate subscriptions",
                "Use SNS with message filtering and encryption, creating subscription filter policies based on alert attributes",
                "Implement direct Lambda invocations instead of SNS to ensure HIPAA compliance and privacy",
                "Use SNS FIFO topics to ensure critical alerts are processed in order of severity"
            ],
            "answer": "Use SNS with message filtering and encryption, creating subscription filter policies based on alert attributes"
        },
        {
            "question": "A manufacturing company uses IoT sensors to monitor equipment performance across multiple factories. They need to build a system that can receive sensor data and distribute it to various applications including real-time dashboards, maintenance scheduling systems, and long-term storage for analysis. The solution must be scalable to handle thousands of sensors and millions of messages per day. Which approach using Amazon SNS would be most effective?",
            "options": [
                "Create an SNS topic for each factory with Lambda functions as subscribers to process and route data",
                "Use a single SNS topic with Amazon Kinesis Data Firehose as a subscriber for all sensor data",
                "Implement a fanout pattern with one SNS topic publishing to multiple SQS queues and other AWS services",
                "Create separate SNS topics for each type of sensor with appropriate subscribers for each application",
                "Use IoT Core directly with rules that route messages to appropriate endpoints without SNS"
            ],
            "answer": "Implement a fanout pattern with one SNS topic publishing to multiple SQS queues and other AWS services"
        },
        {
            "question": "A global e-commerce platform wants to implement a notification system for order status updates. The system needs to handle messages in multiple languages, comply with international messaging regulations, and provide delivery status tracking. During peak shopping seasons, the platform experiences 100x normal traffic. Which combination of Amazon SNS features would best support these requirements?",
            "options": [
                "SNS message attributes for language preferences with direct SMS and email delivery",
                "SNS with Lambda subscribers that handle language translation and regulatory compliance before sending notifications",
                "SNS with SQS dead-letter queues for each subscription to handle failed deliveries and retries",
                "SNS with message filtering, delivery status tracking, and cross-region topics for global redundancy",
                "SNS FIFO topics with message deduplication to prevent duplicate order notifications"
            ],
            "answer": "SNS with message filtering, delivery status tracking, and cross-region topics for global redundancy"
        }
    ],
    "eventbridge": [
        {
            "question": "A company operates a microservices-based e-commerce platform with services running on a mix of EC2 instances, containers, and serverless functions. They want to implement an event-driven architecture where different services can react to events without tight coupling. Events include order placements, inventory changes, payment processing, and shipping updates. Which Amazon EventBridge configuration would provide the most scalable and maintainable solution?",
            "options": [
                "Create a single default event bus with detailed event patterns for each service",
                "Create custom event buses for each type of business event with appropriate rules and targets",
                "Use the default event bus with Lambda functions as targets that filter and route events",
                "Implement partner event buses for each microservice to isolate event processing",
                "Use a combination of EventBridge Pipes and the default event bus with content filtering"
            ],
            "answer": "Create custom event buses for each type of business event with appropriate rules and targets"
        },
        {
            "question": "A financial technology company needs to process stock market data events and route them to different applications based on stock symbols, price movements, and trading volumes. They need sub-second routing decisions while handling millions of events per minute during market hours. Some applications need specific events while others need aggregated data. Which EventBridge approach would be most efficient?",
            "options": [
                "Use EventBridge Scheduler to batch events and process them at regular intervals",
                "Create complex event patterns with multiple filtering criteria and rule priorities",
                "Use EventBridge Pipes to transform events before routing them to appropriate targets",
                "Implement custom event buses for different market sectors with content-based filtering rules",
                "Use Lambda functions to preprocess events before sending them to EventBridge"
            ],
            "answer": "Create complex event patterns with multiple filtering criteria and rule priorities"
        },
        {
            "question": "A multinational corporation has a complex AWS environment spanning multiple accounts and regions. They want to implement a centralized security monitoring system that collects and processes security-related events from all accounts, including CloudTrail API calls, GuardDuty findings, and Security Hub alerts. The system should allow different security teams to receive only the events relevant to their responsibilities. Which EventBridge architecture would best meet these requirements?",
            "options": [
                "Use the default event bus in each account with cross-account event forwarding to a security account",
                "Create custom event buses in a central security account and use resource-based policies to allow events from other accounts",
                "Configure EventBridge rules in each account to forward relevant events to SQS queues monitored by security teams",
                "Use AWS Organizations with EventBridge and organization-wide rules to route events to a central security account",
                "Implement EventBridge global endpoints to collect events across regions with content-based routing to appropriate teams"
            ],
            "answer": "Use AWS Organizations with EventBridge and organization-wide rules to route events to a central security account"
        },
        {
            "question": "A SaaS company wants to integrate with third-party services and allow customers to receive events from their platform. Some events contain sensitive customer data, and different customers should only receive their own events. The solution must be scalable to thousands of customers while minimizing management overhead. Which EventBridge approach would be most appropriate?",
            "options": [
                "Create a custom event bus for each customer with appropriate resource policies",
                "Use EventBridge Scheduler with customer-specific schedules for event delivery",
                "Implement the EventBridge schema registry with customer-specific schemas and validation",
                "Use EventBridge Pipes with customer-specific filtering and enrichment",
                "Create a single event bus with complex event patterns that filter events by customer ID"
            ],
            "answer": "Create a custom event bus for each customer with appropriate resource policies"
        },
        {
            "question": "A healthcare provider is building an application that needs to respond to various events in their patient management system. Some events require immediate action (like critical lab results), while others need to be processed according to specific schedules (like medication reminders). The solution must be HIPAA-compliant and provide reliable delivery with minimal management overhead. Which combination of EventBridge features would best satisfy these requirements?",
            "options": [
                "Use EventBridge Pipes for critical events and EventBridge Scheduler for time-based events",
                "Implement dead-letter queues for all event targets with automatic retries and encryption",
                "Use custom event buses with strict resource policies and content filtering for different event types",
                "Combine EventBridge with SQS queues as targets to buffer events and ensure processing",
                "Use event replay capabilities for failed events and archived events for compliance auditing"
            ],
            "answer": "Use EventBridge Pipes for critical events and EventBridge Scheduler for time-based events"
        }
    ],
    "lambda": [
        {
            "question": "A company processes image uploads for their e-commerce platform. Images must be resized to multiple dimensions, have watermarks applied, and be optimized for web delivery. Currently, EC2 instances handle this processing, but the workload is spiky, leading to either under-utilization or processing delays. The company wants a more cost-effective solution that scales automatically and processes images within seconds of upload. Which Lambda-based architecture would be most efficient?",
            "options": [
                "Create a single Lambda function triggered by S3 uploads that handles all image processing tasks sequentially",
                "Use Step Functions to orchestrate multiple Lambda functions, each handling a specific image processing task",
                "Implement a Lambda function that puts messages in an SQS queue, with worker Lambda functions processing different image operations in parallel",
                "Create separate Lambda functions for each image dimension, triggered directly by the S3 upload event",
                "Use a Lambda function to trigger an Amazon Rekognition job that handles all image processing requirements"
            ],
            "answer": "Use Step Functions to orchestrate multiple Lambda functions, each handling a specific image processing task"
        },
        {
            "question": "A financial services company needs to process transaction data in real-time. Each transaction requires validation against multiple databases, risk scoring, and notification to various downstream systems. The process must be highly available, scalable to handle thousands of transactions per second during peak times, and maintain transaction integrity. Some validation steps can take up to 10 seconds to complete. Which approach using Lambda would best meet these requirements?",
            "options": [
                "Create a single Lambda function with a 15-minute timeout that handles the entire transaction processing flow",
                "Use Amazon Kinesis Data Streams with Lambda consumers that process transactions in parallel with enhanced fan-out",
                "Implement an API Gateway with a Lambda integration and increase the API Gateway timeout to accommodate processing time",
                "Use SQS to queue transactions and trigger Lambda functions with appropriate concurrency settings and visibility timeouts",
                "Create a Step Functions workflow that coordinates multiple Lambda functions for different stages of transaction processing"
            ],
            "answer": "Create a Step Functions workflow that coordinates multiple Lambda functions for different stages of transaction processing"
        },
        {
            "question": "A global gaming company wants to implement a serverless leaderboard system that updates player rankings in real-time. The system needs to handle millions of score submissions per hour during peak times, calculate rankings across different dimensions (global, regional, friends), and make the results available with low latency. Storage requirements will grow over time as more players join. Which Lambda architecture would provide the best performance and cost-effectiveness?",
            "options": [
                "Use Lambda with DynamoDB Streams to process score updates and recalculate rankings whenever scores change",
                "Implement API Gateway with Lambda proxy integration that writes directly to DynamoDB with appropriate partition keys for different ranking dimensions",
                "Create a Lambda function that processes scores in batches from an SQS queue and updates aggregated rankings in ElastiCache for Redis",
                "Use Kinesis Data Analytics with Lambda to calculate rolling window rankings and store results in DynamoDB with DAX for caching",
                "Implement separate Lambda functions for score submission and scheduled aggregate ranking calculations using EventBridge rules"
            ],
            "answer": "Implement API Gateway with Lambda proxy integration that writes directly to DynamoDB with appropriate partition keys for different ranking dimensions"
        },
        {
            "question": "A healthcare provider needs to build a system that processes patient sensor data for anomaly detection. The data arrives continuously but has varying volume depending on the number of active sensors. Processing includes data validation, normalization, and running machine learning models that require significant memory. Results must be available within seconds for critical anomalies. Which Lambda configuration would best handle these requirements?",
            "options": [
                "Configure Lambda with maximum memory allocation (10GB) and use provisioned concurrency to handle peak loads",
                "Implement Lambda with container images to package the machine learning models and set appropriate memory allocation",
                "Use Lambda with SQS to buffer incoming data and process it with a consistent concurrency level",
                "Create a Lambda function that offloads intensive processing to Amazon SageMaker endpoints for the ML component",
                "Use Lambda with Kinesis Data Streams and configure enhanced fan-out with appropriate shard counts"
            ],
            "answer": "Configure Lambda with maximum memory allocation (10GB) and use provisioned concurrency to handle peak loads"
        },
        {
            "question": "A multinational retail company wants to implement a real-time inventory management system across thousands of stores. When inventory levels change, the system needs to update databases, check reorder thresholds, notify supply chain systems, and update customer-facing availability information. The solution must be resilient to partial failures and maintain data consistency. Which Lambda architecture would be most appropriate?",
            "options": [
                "Create a central Lambda function that processes all inventory changes and has retry logic for failed downstream updates",
                "Implement the Saga pattern using Step Functions and Lambda functions with compensation transactions for rollbacks",
                "Use SNS to publish inventory changes with Lambda subscribers for each downstream system and dead-letter queues for failed processing",
                "Create separate Lambda functions for each store with event sourcing to Amazon Kinesis Data Streams for processing",
                "Use Lambda with DynamoDB transactions and global tables for multi-region consistency"
            ],
            "answer": "Implement the Saga pattern using Step Functions and Lambda functions with compensation transactions for rollbacks"
        }
    ],
    "api_gateway": [
        {
            "question": "A global media company is building an API to deliver content to various client applications including web browsers, mobile apps, and smart TVs. The API needs to handle millions of requests per day with low latency, support different authentication mechanisms for different client types, and restrict access based on user subscription levels. Which Amazon API Gateway configuration would best meet these requirements?",
            "options": [
                "Create a single REST API with Lambda authorizers and caching enabled at the stage level",
                "Deploy multiple HTTP APIs, each optimized for specific client types with JWT authorizers",
                "Implement a REST API with custom domain names, edge-optimized endpoints, and resource policies",
                "Use a WebSocket API with Lambda integrations to push content updates to subscribed clients",
                "Create a REST API with API keys, usage plans, and throttling limits based on subscription levels"
            ],
            "answer": "Create a REST API with API keys, usage plans, and throttling limits based on subscription levels"
        },
        {
            "question": "A financial services company is exposing a set of microservices through API Gateway. The APIs handle sensitive financial data and must meet strict security and compliance requirements. They need to validate complex request payloads, implement detailed logging for audit purposes, and ensure encrypted communication. Which combination of API Gateway features would provide the most comprehensive security posture?",
            "options": [
                "Configure request/response data transformations, VPC endpoints, and AWS WAF integration",
                "Use Lambda authorizers, request validators, and CloudWatch Logs with Insights enabled",
                "Implement mutual TLS authentication, IAM authorization, and AWS X-Ray integration",
                "Use API Gateway resource policies, request throttling, and Shield Advanced protection",
                "Configure cognito user pools for authentication, stage variables for environment isolation, and API keys for client identification"
            ],
            "answer": "Implement mutual TLS authentication, IAM authorization, and AWS X-Ray integration"
        },
        {
            "question": "A retail company is migrating their monolithic application to a microservices architecture. They need to design an API layer that can route requests to different microservices based on the request path, handle service discovery, and manage different versions of each microservice concurrently. The solution should minimize client impact during service updates. Which API Gateway approach would be most effective?",
            "options": [
                "Use a single REST API with canary releases and stage variables to manage service versions",
                "Create separate API Gateway APIs for each microservice with custom domain names and base path mapping",
                "Implement an HTTP API with JWT authorizers and private integration with App Mesh",
                "Use a REST API with model validation, mapping templates, and Lambda proxy integration",
                "Create a WebSocket API with route selection expressions that map to different microservices"
            ],
            "answer": "Use a single REST API with canary releases and stage variables to manage service versions"
        },
        {
            "question": "A SaaS provider wants to offer their API to third-party developers. They need to monetize the API with different pricing tiers, track usage per customer, implement rate limiting based on subscription levels, and provide developers with API keys programmatically. Which API Gateway features and architecture would best support these requirements?",
            "options": [
                "Create an HTTP API with Lambda authorizers and integrate with a billing system via EventBridge",
                "Use API Gateway with AWS Marketplace integration and usage plans tied to API keys",
                "Implement a REST API with resource policies, request validators, and custom authorizers",
                "Create private APIs with VPC endpoints and use IAM roles for authentication and authorization",
                "Use a REST API with Amazon Cognito integration and attribute-based access control"
            ],
            "answer": "Use API Gateway with AWS Marketplace integration and usage plans tied to API keys"
        },
        {
            "question": "A healthcare company is building a telemedicine platform that needs to handle both REST API calls for patient data and real-time communication for video consultations. The platform must be HIPAA-compliant, maintain consistent low latency globally, and scale automatically during peak hours. Which combination of API Gateway types and features would best meet these requirements?",
            "options": [
                "Use separate REST and WebSocket APIs with Lambda integrations and client certificates",
                "Implement a single HTTP API with JWT authorization and private integrations to VPC services",
                "Create regional REST APIs with CloudFront distributions and field-level encryption",
                "Use WebSocket APIs for all communication with custom authorizers and connection management",
                "Implement REST APIs with Direct Connect private integrations and mutual TLS authentication"
            ],
            "answer": "Use separate REST and WebSocket APIs with Lambda integrations and client certificates"
        }
    ],
    "containers": [
        {
            "question": "A company is migrating a complex microservices application from their on-premises data center to AWS. The application consists of 20+ services with different resource requirements and scaling patterns. Some services are stateful, requiring persistent storage, while others are stateless web services. The operations team has experience with Docker but limited experience with Kubernetes. Which container orchestration approach on AWS would provide the best balance of control, operational simplicity, and cost-effectiveness?",
            "options": [
                "Use Amazon ECS with a mix of EC2 and Fargate launch types based on service requirements",
                "Deploy the entire application on Amazon EKS with managed node groups",
                "Run stateful services on ECS with EC2 launch type and stateless services on AWS Fargate",
                "Use Amazon ECS with Fargate for all services and Amazon EFS for persistent storage needs",
                "Deploy everything on self-managed EC2 instances with Docker and use Auto Scaling groups"
            ],
            "answer": "Use Amazon ECS with a mix of EC2 and Fargate launch types based on service requirements"
        },
        {
            "question": "A financial services company needs to containerize a high-performance trading application that requires GPU acceleration, ultra-low latency networking, and access to specialized hardware. The application must be highly available across multiple Availability Zones and the company has strict security and compliance requirements. Which container orchestration solution on AWS would best meet these specialized demands?",
            "options": [
                "Amazon ECS with Fargate and ENI trunking for enhanced networking",
                "Amazon ECS with EC2 launch type using P3 instances and cluster placement groups",
                "Amazon EKS with self-managed node groups using GPU-enabled instances and the Kubernetes Device Plugin",
                "AWS Batch with container support for GPU workloads and managed scaling",
                "Amazon Lightsail containers with persistent storage and load balancing"
            ],
            "answer": "Amazon EKS with self-managed node groups using GPU-enabled instances and the Kubernetes Device Plugin"
        },
        {
            "question": "A global retail company is building a containerized e-commerce platform that needs to handle variable traffic with significant spikes during sales events. They want to minimize operational overhead and optimize costs. The application includes web services, APIs, and background processing jobs with different resource requirements and scaling patterns. Which container deployment strategy would be most efficient?",
            "options": [
                "Run all containers on Amazon ECS with EC2 launch type using Spot Instances and Reserved Instances",
                "Use Amazon EKS for the entire application with Karpenter for dynamic node provisioning",
                "Implement Amazon ECS with Fargate for customer-facing services and ECS with EC2 for batch processing jobs",
                "Deploy services on AWS App Runner for simplicity and connect to containerized backends on Amazon ECS",
                "Use a multi-cluster approach with ECS Anywhere for edge locations and ECS on AWS for core services"
            ],
            "answer": "Implement Amazon ECS with Fargate for customer-facing services and ECS with EC2 for batch processing jobs"
        },
        {
            "question": "A healthcare company is containerizing their patient data processing applications. They need to ensure HIPAA compliance, data security, and maintain strict isolation between development, staging, and production environments. The company wants to leverage their existing investments in Kubernetes tooling and expertise. Which approach would provide the strongest security posture while meeting their operational requirements?",
            "options": [
                "Use Amazon ECS with separate clusters for each environment and Security Groups for isolation",
                "Deploy Amazon EKS with AWS PrivateLink and implement Kubernetes network policies",
                "Run containers on Amazon ECS with Fargate to eliminate shared infrastructure concerns",
                "Implement Amazon EKS with separate clusters per environment, private subnets, and AWS KMS encryption",
                "Use Amazon Lightsail containers with dedicated tenancy and VPC isolation"
            ],
            "answer": "Implement Amazon EKS with separate clusters per environment, private subnets, and AWS KMS encryption"
        },
        {
            "question": "A multinational corporation is implementing a hybrid container strategy where some workloads run in AWS and others remain in on-premises data centers. They need consistent management, security policies, and the ability to migrate workloads between environments as needed. The company has significant investments in both Docker and Kubernetes technologies. Which container approach would provide the most seamless hybrid experience?",
            "options": [
                "Use Amazon ECS in AWS and ECS Anywhere for on-premises workloads with a common control plane",
                "Implement Amazon EKS in AWS and self-managed Kubernetes on-premises with cluster federation",
                "Deploy Amazon EKS Anywhere on-premises and Amazon EKS in AWS with consistent tooling",
                "Run Amazon ECS on AWS and Kubernetes on-premises with custom integration scripts",
                "Use AWS Outposts with Amazon EKS for consistent container orchestration across environments"
            ],
            "answer": "Deploy Amazon EKS Anywhere on-premises and Amazon EKS in AWS with consistent tooling"
        }
    ],
    "aws_security": [
        {
            "question": "A financial services company needs to securely manage database credentials, API keys, and OAuth tokens used by their applications running on AWS. They need automatic rotation of credentials, fine-grained access control, centralized audit logging, and encryption. Different application teams should be able to manage their own secrets without accessing those of other teams. Which AWS service and configuration would best meet these requirements?",
            "options": [
                "Use AWS Systems Manager Parameter Store with KMS encryption and IAM policies per parameter path",
                "Implement AWS Secrets Manager with automatic rotation and resource-based policies",
                "Store encrypted credentials in DynamoDB with fine-grained access control and server-side encryption",
                "Use AWS Certificate Manager Private CA to issue and manage certificates for authentication",
                "Implement a custom solution using S3 with object encryption and bucket policies"
            ],
            "answer": "Implement AWS Secrets Manager with automatic rotation and resource-based policies"
        },
        {
            "question": "A multinational corporation is moving to AWS and needs to manage user access across hundreds of AWS accounts. They currently use Microsoft Active Directory on-premises for identity management and want to leverage their existing identity source while providing single sign-on to the AWS Management Console, CLI, and AWS applications. They need to enforce consistent access policies and enable attribute-based access control. Which approach would be most efficient?",
            "options": [
                "Configure cross-account IAM roles and establish trust relationships between all accounts",
                "Use AWS Organizations with Service Control Policies and direct federation to each account",
                "Implement AWS Directory Service and create trust relationships with on-premises Active Directory",
                "Use AWS IAM Identity Center (successor to AWS SSO) with Active Directory as the identity source",
                "Deploy Amazon Cognito user pools with SAML federation to Active Directory"
            ],
            "answer": "Use AWS IAM Identity Center (successor to AWS SSO) with Active Directory as the identity source"
        },
        {
            "question": "A healthcare provider needs to ensure that all EC2 instances across multiple AWS accounts are patched according to their security policy, which requires critical patches to be applied within 24 hours of release. They need centralized visibility into patch compliance status, automated remediation for non-compliant instances, and detailed reporting for auditing purposes. Which combination of AWS services would best meet these requirements?",
            "options": [
                "Use AWS Inspector to scan instances and AWS Lambda to apply patches when vulnerabilities are detected",
                "Implement AWS Systems Manager Patch Manager with patch baselines and maintenance windows across accounts",
                "Deploy AWS Config with custom rules that check patch status and auto-remediation through Lambda functions",
                "Use Amazon EC2 Auto Scaling with pre-patched AMIs and automatic instance refresh on new AMI versions",
                "Implement AWS Security Hub with custom security standards that check for patch compliance"
            ],
            "answer": "Implement AWS Systems Manager Patch Manager with patch baselines and maintenance windows across accounts"
        },
        {
            "question": "A company wants to securely share specific VPC subnets with their partner organizations while maintaining strict access controls. These partners need to deploy their own resources in the shared subnets but should be restricted from modifying the networking components or accessing resources in other subnets. The company needs a solution that minimizes administrative overhead as they onboard more partners. Which approach would be most effective?",
            "options": [
                "Create separate VPCs for each partner and establish VPC peering connections with appropriate route tables",
                "Use AWS PrivateLink to expose specific services to partners without sharing the underlying subnets",
                "Implement Transit Gateway with appropriate route tables and security groups for partner access",
                "Use AWS Resource Access Manager (RAM) to share specific subnets with partner AWS accounts",
                "Create IAM roles in the company's account that partners can assume with limited permissions"
            ],
            "answer": "Use AWS Resource Access Manager (RAM) to share specific subnets with partner AWS accounts"
        },
        {
            "question": "A SaaS application needs to implement authentication and authorization for millions of users across web and mobile platforms. Requirements include social identity provider integration, multi-factor authentication, customizable sign-up and sign-in experiences, and fine-grained access control based on user attributes. The solution must be scalable, secure, and require minimal development effort. Which AWS service would best meet these requirements?",
            "options": [
                "AWS IAM with web identity federation for social login providers",
                "Amazon Cognito user pools with identity pools for fine-grained access control",
                "AWS Directory Service with federation to social identity providers",
                "Amazon API Gateway with Lambda authorizers implementing custom authentication logic",
                "AWS IAM Identity Center with external identity provider connections"
            ],
            "answer": "Amazon Cognito user pools with identity pools for fine-grained access control"
        }
    ],
    "data_analytics": [
        {
            "question": "A company has millions of log files stored in Amazon S3 from their web applications. They need to analyze these logs to identify patterns in user behavior, troubleshoot errors, and generate reports. The data analysts prefer using SQL for queries and need an interactive query experience without setting up or managing infrastructure. The solution should be cost-effective for ad-hoc analysis of large datasets. Which AWS service would best meet these requirements?",
            "options": [
                "Amazon Redshift with Spectrum for querying data in S3",
                "Amazon RDS with cross-region read replicas for distributed querying",
                "Amazon Athena with data partitioning and compression optimizations",
                "Amazon EMR with Hive for SQL-like querying capabilities",
                "AWS Glue with SparkSQL for interactive queries"
            ],
            "answer": "Amazon Athena with data partitioning and compression optimizations"
        },
        {
            "question": "A financial services company needs to process and analyze real-time transaction data to detect fraud patterns. They receive thousands of transactions per second and need to apply complex algorithms within milliseconds to approve or flag transactions. The solution must be scalable, maintain low latency, and provide visualization capabilities for analysts. Which combination of AWS services would be most effective?",
            "options": [
                "Amazon Kinesis Data Streams with Lambda consumers and Amazon QuickSight for visualization",
                "Amazon SQS with EC2 workers and Elasticsearch for real-time analytics",
                "Amazon Kinesis Data Analytics for SQL processing with Amazon OpenSearch Service for analysis and visualization",
                "Amazon MSK (Managed Streaming for Kafka) with Amazon EMR for processing and Tableau integration",
                "AWS IoT Core with rules engine forwarding to DynamoDB and Amazon QuickSight"
            ],
            "answer": "Amazon Kinesis Data Analytics for SQL processing with Amazon OpenSearch Service for analysis and visualization"
        },
        {
            "question": "A healthcare research organization has petabytes of patient data and genomic information stored in various formats in Amazon S3. They need to build a data lake solution that enables researchers to catalog, transform, and analyze this data while maintaining strict access controls and data lineage tracking. Which combination of AWS services would provide the most comprehensive solution?",
            "options": [
                "Use AWS Glue for cataloging and ETL with Amazon Redshift for analysis and AWS KMS for encryption",
                "Implement Amazon EMR with Hadoop for processing and Hive Metastore for cataloging",
                "Deploy AWS Lake Formation with AWS Glue for ETL and Amazon Athena for querying with fine-grained access controls",
                "Use Amazon S3 with intelligent tiering, S3 Select for querying, and IAM policies for access control",
                "Implement Amazon RDS with read replicas and AWS Database Migration Service for data loading"
            ],
            "answer": "Deploy AWS Lake Formation with AWS Glue for ETL and Amazon Athena for querying with fine-grained access controls"
        },
        {
            "question": "A retail company wants to implement real-time analytics on customer shopping behavior from their website and mobile applications. They need to collect clickstream data, product views, cart additions, and purchase events for millions of users globally. The solution should enable both real-time dashboards for operations teams and batch processing for data scientists. Which architecture would be most efficient?",
            "options": [
                "Use CloudFront with Lambda@Edge to capture events and store in DynamoDB with DynamoDB Streams processing",
                "Implement Kinesis Data Streams for ingestion, Kinesis Data Firehose for delivery to S3, and Kinesis Data Analytics for real-time processing",
                "Use API Gateway with direct integrations to SQS for buffering and Lambda for processing into various databases",
                "Deploy Amazon MSK with Kafka Connect for data collection and multiple consumers for different processing needs",
                "Implement IoT Core for event ingestion with rules that route data to both real-time and batch processing pipelines"
            ],
            "answer": "Implement Kinesis Data Streams for ingestion, Kinesis Data Firehose for delivery to S3, and Kinesis Data Analytics for real-time processing"
        },
        {
            "question": "A manufacturing company has implemented IoT sensors throughout their factories to monitor equipment performance and environmental conditions. They need a comprehensive analytics solution that can process time-series data from thousands of sensors, detect anomalies in real-time, provide interactive visualizations for operations teams, and enable machine learning models to predict maintenance needs. Which combination of AWS services would best meet these requirements?",
            "options": [
                "Use AWS IoT Core for device connectivity, Amazon Timestream for time-series storage, and Amazon QuickSight for visualization",
                "Implement AWS IoT Greengrass for edge processing, AWS IoT Analytics for time-series analysis, and Amazon SageMaker for predictive maintenance",
                "Deploy Amazon Kinesis for data ingestion, Amazon OpenSearch Service for real-time analysis, and Amazon QuickSight with ML insights",
                "Use AWS IoT Core with rules routing to Amazon Managed Service for Prometheus and Amazon Managed Grafana for visualization",
                "Implement direct MQTT ingestion to Amazon MSK, processing with Amazon EMR, and custom dashboards with Amazon EC2"
            ],
            "answer": "Implement AWS IoT Greengrass for edge processing, AWS IoT Analytics for time-series analysis, and Amazon SageMaker for predictive maintenance"
        }
    ],
    "ml": [
        {
            "question": "A multinational e-commerce company wants to implement natural language processing to automatically categorize customer support emails into different priority levels and route them to the appropriate teams. The solution should handle multiple languages, be trainable on company-specific terminology, and integrate with their existing ticketing system. Which AWS machine learning service would be most appropriate?",
            "options": [
                "Use Amazon Comprehend custom classification with entity recognition for priority determination",
                "Implement Amazon Lex with custom intents for email classification and routing rules",
                "Use Amazon Translate for non-English emails followed by Amazon Rekognition to analyze any attachments",
                "Deploy a custom model on Amazon SageMaker with pre-processing using AWS Lambda",
                "Use Amazon Textract to extract text followed by Amazon Comprehend for sentiment analysis"
            ],
            "answer": "Use Amazon Comprehend custom classification with entity recognition for priority determination"
        },
        {
            "question": "A healthcare provider needs to extract patient information from scanned medical forms, including handwritten notes, to integrate with their electronic health record system. The solution must maintain high accuracy, handle various form layouts, and comply with HIPAA requirements. Which combination of AWS services would provide the most comprehensive solution?",
            "options": [
                "Use Amazon Rekognition for image analysis and Amazon Comprehend Medical for healthcare entity detection",
                "Implement Amazon Textract for form extraction with Amazon Comprehend Medical for healthcare entity recognition",
                "Deploy a custom OCR model on Amazon SageMaker with pre-trained medical terminology recognition",
                "Use Amazon Textract for document analysis and AWS Lambda with custom code for healthcare-specific processing",
                "Implement Amazon Transcribe Medical for converting voice notes to text and Amazon Comprehend for entity extraction"
            ],
            "answer": "Implement Amazon Textract for form extraction with Amazon Comprehend Medical for healthcare entity recognition"
        },
        {
            "question": "A global retail company wants to build a recommendation engine that suggests products to customers based on their browsing history, purchase patterns, and similar customer behaviors. The system needs to handle millions of products and customers, update recommendations in near-real-time as customer behavior changes, and integrate with their existing e-commerce platform. Which approach using AWS machine learning services would be most effective?",
            "options": [
                "Use Amazon Personalize with real-time event tracking and custom dataset groups",
                "Deploy a custom recommendation model on Amazon SageMaker with A/B testing using feature store",
                "Implement Amazon Kendra for product search enhanced with user behavior analysis",
                "Use Amazon Neptune with graph algorithms to identify product relationships and customer similarities",
                "Combine Amazon Elasticsearch with custom ML models deployed on Lambda functions"
            ],
            "answer": "Use Amazon Personalize with real-time event tracking and custom dataset groups"
        },
        {
            "question": "A financial services company wants to implement anomaly detection to identify potentially fraudulent transactions in real-time. They process millions of transactions daily across multiple payment channels and need to minimize false positives while catching sophisticated fraud patterns. The solution should adapt to evolving fraud techniques without requiring constant manual model updates. Which AWS machine learning approach would be most suitable?",
            "options": [
                "Use Amazon Fraud Detector with custom fraud insights and real-time APIs",
                "Implement Amazon SageMaker with Random Cut Forest algorithm and automatic model retraining",
                "Deploy Amazon Lookout for Metrics to detect anomalies in transaction data streams",
                "Use Amazon Comprehend to analyze transaction descriptions with Amazon QuickSight for visualization",
                "Implement a custom deep learning model on Amazon SageMaker with managed spot training"
            ],
            "answer": "Use Amazon Fraud Detector with custom fraud insights and real-time APIs"
        },
        {
            "question": "A manufacturing company wants to implement predictive maintenance for their factory equipment using sensor data collected from IoT devices. They need to predict potential failures before they occur, estimate remaining useful life of components, and optimize maintenance scheduling. The solution should work with minimal historical failure data and improve over time as more data is collected. Which machine learning approach on AWS would be most effective?",
            "options": [
                "Use Amazon Lookout for Equipment with customized models for different machine types",
                "Implement Amazon Monitron with AWS IoT Core for comprehensive equipment monitoring",
                "Deploy Amazon SageMaker with Forecast algorithms and feature engineering pipelines",
                "Use AWS IoT Analytics with built-in ML capabilities for time-series analysis",
                "Implement Amazon Kinesis Data Analytics with ML algorithms for real-time processing"
            ],
            "answer": "Use Amazon Lookout for Equipment with customized models for different machine types"
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

# Function for SQS page
def sqs_page():
    st.title("Amazon Simple Queue Service (SQS)")
    
    try:
        st.image(aws_images["sqs"], width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is Amazon SQS?")
    st.markdown("""
    Amazon Simple Queue Service (SQS) is a fully managed message queuing service that enables you to decouple and scale 
    microservices, distributed systems, and serverless applications. SQS eliminates the complexity and overhead 
    associated with managing and operating message-oriented middleware.
    """)
    
    # Create feature highlights with cards
    st.subheader("Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🚀 Unlimited Throughput</h4>
            <p>Supports virtually unlimited number of transactions per second with elastic capacity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔄 Message Delivery Guarantee</h4>
            <p>At-least-once message delivery with multiple copies stored for redundancy</p>
        </div>
        """, unsafe_allow_html=True)
        
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>⏱️ Message Retention</h4>
            <p>Configurable message retention period up to 14 days</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>📦 Batching Operations</h4>
            <p>Send and receive batching for greater throughput and cost efficiency</p>
        </div>
        """, unsafe_allow_html=True)
        
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔄 Dead-Letter Queues</h4>
            <p>Capture and isolate messages that fail processing for troubleshooting</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔒 Security</h4>
            <p>Encryption at rest and in transit with access control via IAM</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("SQS Queue Types")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h3>Standard Queues</h3>
            <h4>Features:</h4>
            <ul>
                <li>Unlimited throughput (nearly unlimited TPS)</li>
                <li>At-least-once delivery (may deliver duplicates)</li>
                <li>Best-effort ordering (messages may arrive out of order)</li>
            </ul>
            <h4>Best For:</h4>
            <ul>
                <li>Maximum throughput applications</li>
                <li>When message ordering is not critical</li>
                <li>When applications can handle duplicate messages</li>
            </ul>
            <h4>Use Cases:</h4>
            <ul>
                <li>Background jobs processing</li>
                <li>Decoupling microservices</li>
                <li>Work distribution among multiple workers</li>
                <li>Buffering requests during traffic spikes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h3>FIFO Queues</h3>
            <h4>Features:</h4>
            <ul>
                <li>First-In-First-Out delivery guarantee</li>
                <li>Exactly-once processing (no duplicates)</li>
                <li>Limited throughput (300 TPS by default, up to 3000 TPS with high throughput mode)</li>
                <li>Message group support for parallel processing</li>
            </ul>
            <h4>Best For:</h4>
            <ul>
                <li>Applications requiring strict ordering</li>
                <li>When duplicate processing can't be tolerated</li>
                <li>When transaction processing requires accuracy</li>
            </ul>
            <h4>Use Cases:</h4>
            <ul>
                <li>Financial transactions processing</li>
                <li>Order processing systems</li>
                <li>Sequential command execution</li>
                <li>Inventory updates</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("SQS Message Lifecycle")
    
    # Create a visual representation of message lifecycle
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <div style="display: inline-block; background-color: #f0f7fb; border-radius: 50%; width: 50px; height: 50px; line-height: 50px; margin: 10px;">1</div>
            <div style="display: inline-block; width: 40px; text-align: center;">→</div>
            <div style="display: inline-block; background-color: #f0f7fb; border-radius: 50%; width: 50px; height: 50px; line-height: 50px; margin: 10px;">2</div>
            <div style="display: inline-block; width: 40px; text-align: center;">→</div>
            <div style="display: inline-block; background-color: #f0f7fb; border-radius: 50%; width: 50px; height: 50px; line-height: 50px; margin: 10px;">3</div>
            <div style="display: inline-block; width: 40px; text-align: center;">→</div>
            <div style="display: inline-block; background-color: #f0f7fb; border-radius: 50%; width: 50px; height: 50px; line-height: 50px; margin: 10px;">4</div>
            <div style="display: inline-block; width: 40px; text-align: center;">→</div>
            <div style="display: inline-block; background-color: #f0f7fb; border-radius: 50%; width: 50px; height: 50px; line-height: 50px; margin: 10px;">5</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    1. **Send Message:** Producer sends a message to the queue
    2. **Storage:** SQS redundantly stores the message across multiple servers
    3. **Receive Message:** Consumer polls the queue and receives the message
    4. **Processing:** Consumer processes the message while it remains in the queue but is hidden (visibility timeout)
    5. **Deletion:** After successful processing, consumer explicitly deletes the message from the queue
    
    **If not deleted within the visibility timeout period:** Message becomes visible again for other consumers
    """)
    
    st.subheader("Visibility Timeout")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h4>🕒 Visibility Timeout Settings</h4>
            <ul>
                <li><strong>Default:</strong> 30 seconds</li>
                <li><strong>Range:</strong> 0 seconds to 12 hours</li>
                <li><strong>Purpose:</strong> Prevents other consumers from processing the message while it's being handled</li>
                <li><strong>Extension:</strong> Can be extended if processing takes longer than expected</li>
                <li><strong>Best Practice:</strong> Set to maximum expected processing time</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Create a simple chart to illustrate visibility timeout
        fig, ax = plt.subplots(figsize=(6, 3))
        
        # Define states and durations
        states = ['Available', 'In Flight (Processing)', 'Deleted or Back to Queue']
        durations = [10, 30, 15]
        colors = ['#1E88E5', '#FFC107', '#4CAF50']
        
        # Create horizontal bar chart
        y_pos = range(len(states))
        ax.barh(y_pos, durations, color=colors)
        
        # Add annotations
        ax.text(5, 0, 'Message in Queue')
        ax.text(15, 1, 'Visibility Timeout')
        ax.text(35, 2, 'Processing Complete')
        
        # Customize chart
        ax.set_yticks(y_pos)
        ax.set_yticklabels(states)
        ax.set_xlabel('Time (seconds)')
        ax.set_title('SQS Message Visibility Timeout')
        
        # Display the chart
        st.pyplot(fig)
    
    st.header("SQS Best Practices")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>💻 Performance Optimization</h4>
            <ul>
                <li>Use Long Polling to reduce empty responses</li>
                <li>Batch operations for higher throughput</li>
                <li>Right-size visibility timeout</li>
                <li>Implement request-response pattern with temporary queues</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>💰 Cost Optimization</h4>
            <ul>
                <li>Delete messages promptly after processing</li>
                <li>Structure data efficiently to minimize message size</li>
                <li>Monitor queue depth and scale consumers accordingly</li>
                <li>Use client-side buffering for optimal request rates</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🛡️ Reliability</h4>
            <ul>
                <li>Implement Dead-Letter Queues (DLQ)</li>
                <li>Apply idempotent processing logic</li>
                <li>Use separate queues for different processing priorities</li>
                <li>Implement retry policies with exponential backoff</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Technical diagram section
    st.header("Architectural Patterns")
    
    tab1, tab2, tab3 = st.tabs(["Queue per Worker", "Fanout Pattern", "Priority Queue"])
    
    with tab1:
        st.markdown("""
        ### Queue per Worker Pattern
        
        In this pattern, each worker has a dedicated queue, allowing for task distribution 
        based on worker capabilities or load balancing requirements.
        
        **Benefits:**
        - Worker-specific message routing
        - Isolation of processing failures
        - Different scaling policies per worker
        - Specialized throughput management
        
        **Implementation:**
        1. Create multiple SQS queues
        2. Route messages based on content, attributes, or load balancing algorithm
        3. Each worker consumes from its dedicated queue
        """)
        
        # Simple ASCII diagram
        st.code("""
        Producer → Router → Queue A → Worker A
                    ├→ Queue B → Worker B
                    └→ Queue C → Worker C
        """)
    
    with tab2:
        st.markdown("""
        ### Fanout Pattern
        
        SQS combined with SNS for distributing messages to multiple destinations.
        
        **Benefits:**
        - Single operation distributes message to multiple consumers
        - Each consumer processes messages independently
        - Decoupled processing paths
        - Combined reliability of both SNS and SQS
        
        **Implementation:**
        1. Create an SNS topic and multiple SQS queues
        2. Subscribe each queue to the SNS topic
        3. Publish messages to the SNS topic
        4. Each queue receives a copy of the message
        """)
        
        # Simple ASCII diagram
        st.code("""
                       ┌→ SQS Queue A → Consumer A
        Producer → SNS ├→ SQS Queue B → Consumer B
                       └→ SQS Queue C → Consumer C
        """)
    
    with tab3:
        st.markdown("""
        ### Priority Queue Pattern
        
        Using multiple queues with different polling frequencies to implement priority.
        
        **Benefits:**
        - Process high-priority messages first
        - No starving of low-priority messages
        - Different visibility timeouts per priority level
        - Separate monitoring and scaling for different priorities
        
        **Implementation:**
        1. Create queues for each priority level (high, medium, low)
        2. Route messages to appropriate queue based on priority
        3. Configure workers to poll high-priority queues more frequently
        """)
        
        # Simple ASCII diagram
        st.code("""
        Producer → High Priority Queue → ┐
              ├→ Medium Priority Queue → ├→ Workers (poll in priority order)
              └→ Low Priority Queue  → ┘
        """)

# Function for SNS page
def sns_page():
    st.title("Amazon Simple Notification Service (SNS)")
    
    try:
        st.image(aws_images["sns"], width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is Amazon SNS?")
    st.markdown("""
    Amazon Simple Notification Service (SNS) is a fully managed pub/sub messaging service for both application-to-application (A2A) 
    and application-to-person (A2P) communication. It enables you to decouple microservices, distributed systems, and serverless 
    applications by sending messages to multiple subscribers simultaneously.
    """)
    
    # Create feature highlights with cards
    st.subheader("Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>📢 Pub/Sub Messaging</h4>
            <p>Publish messages to topics with multiple subscribers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔌 Multi-Protocol Support</h4>
            <p>SMS, email, push notifications, HTTP endpoints, and AWS services</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🎯 Message Filtering</h4>
            <p>Filter messages at the subscriber level with attribute-based policies</p>
        </div>
        """, unsafe_allow_html=True)
        
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>📊 Message Archiving</h4>
            <p>Store messages in S3 for compliance and analytics</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔄 Message Durability</h4>
            <p>Redundant storage across multiple availability zones</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔒 Message Encryption</h4>
            <p>Server-side encryption for sensitive data</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("SNS Concepts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h3>📣 Topics and Subscriptions</h3>
            <h4>Topics:</h4>
            <ul>
                <li>Communication channels for sending messages</li>
                <li>Identified by Amazon Resource Name (ARN)</li>
                <li>Can have multiple subscribers</li>
                <li>Support two types:
                  <ul>
                    <li>Standard (high throughput, best-effort ordering)</li>
                    <li>FIFO (strict ordering, exactly-once delivery)</li>
                  </ul>
                </li>
            </ul>
            <h4>Subscriptions:</h4>
            <ul>
                <li>Endpoints that receive messages published to a topic</li>
                <li>Multiple subscription types:
                  <ul>
                    <li>Amazon SQS</li>
                    <li>AWS Lambda</li>
                    <li>HTTP/HTTPS</li>
                    <li>Email/Email-JSON</li>
                    <li>Mobile Push Notifications</li>
                    <li>SMS text messages</li>
                  </ul>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h3>🎯 Message Filtering</h3>
            <h4>Filter Policies:</h4>
            <ul>
                <li>JSON policies that specify which messages to deliver</li>
                <li>Based on message attributes</li>
                <li>Help reduce unwanted traffic and costs</li>
            </ul>
            <h4>Example Filter Policy:</h4>
            <pre style="background-color: #f8f8f8; padding: 10px; border-radius: 5px;">
<code>{
  "customer_interests": ["sports", "travel"],
  "price_usd": [{"numeric": [">=", 100]}]
}</code></pre>
            <h4>Benefits:</h4>
            <ul>
                <li>More efficient processing</li>
                <li>Reduced downstream costs</li>
                <li>Simplified application logic</li>
                <li>Decreased bandwidth usage</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("SNS Use Cases")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h3>💻 Application-to-Application (A2A)</h3>
            <h4>Fanout Pattern:</h4>
            <ul>
                <li>Publish a message once, deliver to multiple endpoints</li>
                <li>Parallel asynchronous processing</li>
                <li>Example: Order processing system sending notifications to inventory, shipping, and billing systems</li>
            </ul>
            <h4>Event-Driven Architecture:</h4>
            <ul>
                <li>React to events across distributed systems</li>
                <li>Trigger AWS Lambda functions based on events</li>
                <li>Enable microservices communication</li>
            </ul>
            <h4>Integration:</h4>
            <ul>
                <li>Connect with over 60 AWS services natively</li>
                <li>Capture events from multiple sources</li>
                <li>Distribute to various destinations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h3>👤 Application-to-Person (A2P)</h3>
            <h4>User Notifications:</h4>
            <ul>
                <li>Send notifications directly to users</li>
                <li>Support multiple delivery channels</li>
            </ul>
            <h4>Mobile Push:</h4>
            <ul>
                <li>Send notifications to mobile apps</li>
                <li>Support for Apple, Google, Amazon, Microsoft platforms</li>
                <li>Rich message content</li>
            </ul>
            <h4>SMS:</h4>
            <ul>
                <li>Text message delivery to over 200 countries</li>
                <li>Support for transactional and promotional messages</li>
                <li>Sender IDs and short codes in supported regions</li>
            </ul>
            <h4>Email:</h4>
            <ul>
                <li>Send formatted messages or JSON payloads</li>
                <li>Raw email delivery for customization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("SNS vs SQS Comparison")
    
    # Create comparison table with styling
    comparison_data = {
        "Feature": ["Model", "Message Delivery", "Use Case", "Message Persistence", "Delivery Attempt", "Consumers", "Common Pattern"],
        "Amazon SNS": [
            "Pub/Sub (push)",
            "Push to multiple subscribers",
            "Fanout to multiple endpoints",
            "Non-persistent unless using SQS subscription",
            "Up to 100,015 retries depending on protocol",
            "Multiple subscribers",
            "SNS + SQS: Fanout messages to multiple SQS queues for parallel processing"
        ],
        "Amazon SQS": [
            "Queue (poll)",
            "Pulled by a single consumer",
            "Decoupling and buffering",
            "Persistent (up to 14 days)",
            "Persists until deletion or expiration",
            "Single consumer (unless using FIFO with group IDs)",
            "-"
        ]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df.set_index("Feature"), use_container_width=True)
    
    # Technical diagram - Fanout pattern
    st.subheader("SNS-SQS Fanout Pattern")
    
    fanout_code = """
                             ┌→ SQS Queue → EC2 Instances (Email Service)
                             │
    Producer → SNS Topic ────┼→ SQS Queue → Lambda Function (Mobile Push)
                             │
                             └→ SQS Queue → ECS Containers (Data Processing)
    """
    
    st.code(fanout_code)
    
    st.markdown("""
    <div class="aws-info-card">
        <h4>Key Benefits of the Fanout Pattern</h4>
        <ul>
            <li><strong>Decoupling:</strong> Producers and consumers operate independently</li>
            <li><strong>Scalability:</strong> Add new subscribers without affecting publishers</li>
            <li><strong>Reliability:</strong> Combine SNS's delivery guarantees with SQS's message persistence</li>
            <li><strong>Load Leveling:</strong> SQS absorbs traffic spikes without overwhelming consumers</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("SNS Best Practices")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🛡️ Reliability</h4>
            <ul>
                <li>Implement DLQ for failed message deliveries</li>
                <li>Monitor delivery status logging</li>
                <li>Use message archiving for compliance and debugging</li>
                <li>Implement retry policies for critical messages</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔒 Security</h4>
            <ul>
                <li>Enable server-side encryption with KMS</li>
                <li>Use IAM policies and topic policies</li>
                <li>Consider VPC endpoints for internal communications</li>
                <li>Implement attribute-based access control</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>⚡ Performance</h4>
            <ul>
                <li>Use message filtering to reduce unnecessary delivery</li>
                <li>Implement message batching for higher throughput</li>
                <li>Consider FIFO topics when ordering is required</li>
                <li>Monitor performance metrics with CloudWatch</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Function for EventBridge page
def eventbridge_page():
    st.title("Amazon EventBridge")
    
    try:
        st.image(aws_images["eventbridge"], width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is Amazon EventBridge?")
    st.markdown("""
    Amazon EventBridge is a serverless event bus service that makes it easy to connect your applications with data from a variety 
    of sources. It delivers a stream of real-time data from event sources such as AWS services, SaaS applications, or your own 
    applications to targets like AWS Lambda functions, HTTP endpoints via API destinations, or other event buses.
    """)
    
    # Create feature highlights with cards
    st.subheader("Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔄 Serverless Event Routing</h4>
            <p>Route events at scale without managing infrastructure</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🎯 Advanced Filtering</h4>
            <p>Pattern matching and content-based filtering</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🛡️ Event Bus Isolation</h4>
            <p>Multiple event buses with resource-based policies</p>
        </div>
        """, unsafe_allow_html=True)
        
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>📊 Schema Registry</h4>
            <p>Discover, create and manage event schemas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔌 AWS Service Integration</h4>
            <p>Direct integration with over 200 AWS services</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔄 Archive and Replay</h4>
            <p>Store events and replay them for recovery</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("EventBridge Core Concepts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h3>🎯 Events and Event Buses</h3>
            <h4>Events:</h4>
            <ul>
                <li>JSON objects that represent state changes</li>
                <li>Contains metadata and detail fields</li>
            </ul>
            <h4>Example Event:</h4>
<pre style="background-color: #f8f8f8; padding: 10px; border-radius: 5px; font-size: 0.8em; overflow-x: auto;">
<code>{
  "version": "0",
  "id": "12345678-1234-1234-1234-123456789012",
  "detail-type": "EC2 Instance State Change",
  "source": "aws.ec2",
  "account": "123456789012",
  "time": "2023-11-29T13:45:00Z",
  "region": "us-east-1",
  "resources": ["arn:aws:ec2:us-east-1:123456789012:instance/i-0123456789abcdef"],
  "detail": {
    "instance-id": "i-0123456789abcdef",
    "state": "running"
  }
}</code>
</pre>
            <h4>Event Buses:</h4>
            <ul>
                <li>Routers that receive events and deliver to targets</li>
                <li>Types:
                  <ul>
                    <li>Default event bus (AWS services)</li>
                    <li>Custom event buses (your applications)</li>
                    <li>Partner event buses (third-party SaaS)</li>
                  </ul>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h3>📝 Rules and Targets</h3>
            <h4>Rules:</h4>
            <ul>
                <li>Event patterns that specify when to route events</li>
                <li>Match on event fields like source, detail-type, or detail</li>
                <li>Can also run on a schedule (like CloudWatch Events)</li>
            </ul>
            <h4>Example Pattern:</h4>
<pre style="background-color: #f8f8f8; padding: 10px; border-radius: 5px; font-size: 0.8em; overflow-x: auto;">
<code>{
"source": ["aws.ec2"],
"detail-type": ["EC2 Instance State Change"],
"detail": {
    "state": ["running", "stopped"]
    }
}</code>
</pre>
            <h4>Targets:</h4>
            <ul>
                <li>Services that receive matching events</li>
                <li>Up to 5 targets per rule</li>
                <li>Types include:
                  <ul>
                    <li>AWS Lambda functions</li>
                    <li>AWS Step Functions state machines</li>
                    <li>Amazon SQS queues</li>
                    <li>Amazon SNS topics</li>
                    <li>Amazon Kinesis streams</li>
                    <li>API destinations (HTTP endpoints)</li>
                    <li>Other event buses</li>
                  </ul>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("EventBridge Specialized Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h3>🔄 EventBridge Pipes</h3>
            <p>Point-to-point integration between sources and targets with built-in filtering, enrichment, and transformation.</p>
            <h4>Sources include:</h4>
            <ul>
                <li>DynamoDB streams</li>
                <li>Kinesis streams</li>
                <li>Amazon MQ</li>
                <li>Amazon MSK</li>
                <li>SQS queues</li>
            </ul>
            <h4>Benefits:</h4>
            <ul>
                <li>Simplified architecture</li>
                <li>Reduced custom code</li>
                <li>Enhanced error handling</li>
                <li>Support for synchronous target invocation</li>
            </ul>
            <img src="https://d1.awsstatic.com/product-marketing/EventBridge/Product-Page-Diagram_Amazon-EventBridge-Pipes.31ba8d7c7e8d0ee8c9ac1ed9a7ab2a8978492628.png" style="max-width: 100%; margin-top: 15px; border-radius: 5px;">
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h3>⏰ EventBridge Scheduler</h3>
            <p>Fully managed scheduler service that creates, runs, and manages scheduled tasks at scale.</p>
            <h4>Features:</h4>
            <ul>
                <li>Cron and rate expressions</li>
                <li>Timezone support</li>
                <li>Flexible retry policies</li>
                <li>Dead-letter queues for failed invocations</li>
                <li>Scales to millions of schedules</li>
            </ul>
            <h4>Use Cases:</h4>
            <ul>
                <li>Database maintenance</li>
                <li>Report generation</li>
                <li>Periodic data processing</li>
                <li>Automated resource management</li>
                <li>Scheduled notifications</li>
            </ul>
            <img src="https://d1.awsstatic.com/product-marketing/EventBridge/Product-Page-Diagram_Amazon-EventBridge-Scheduler.c50ddfcf0f0206a5c6825187611f3344c3eb4a82.png" style="max-width: 100%; margin-top: 15px; border-radius: 5px;">
        </div>
        """, unsafe_allow_html=True)
    
    st.header("EventBridge vs. SNS vs. SQS")
    
    # Create comparison table
    comparison_data = {
        "Feature": [
            "Primary Purpose", 
            "Delivery Model", 
            "Filtering", 
            "Integration", 
            "Event Replay",
            "Schema Registry",
            "Best For"
        ],
        "Amazon EventBridge": [
            "Event routing and integration",
            "Event-driven, rule-based routing",
            "Advanced pattern matching and transformation",
            "200+ AWS services, SaaS providers",
            "Archive and replay supported",
            "Built-in schema discovery and registry",
            "Complex event routing, SaaS integration"
        ],
        "Amazon SNS": [
            "Publishing to multiple subscribers",
            "Push-based pub/sub",
            "Subscription filter policies",
            "AWS services, HTTP/S, email, mobile, SMS",
            "No replay capability",
            "No schema registry",
            "Simple pub/sub messaging, notifications"
        ],
        "Amazon SQS": [
            "Message queuing and decoupling",
            "Pull-based queue",
            "No built-in filtering",
            "AWS services",
            "Messages persist until consumed",
            "No schema registry",
            "Workload decoupling, buffering"
        ]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df.set_index("Feature"), use_container_width=True)
    
    # Visual architecture patterns
    st.header("EventBridge Architecture Patterns")
    
    tab1, tab2, tab3 = st.tabs(["Event-Driven Microservices", "Multi-Account Architecture", "SaaS Integration"])
    
    with tab1:
        st.markdown("""
        ### Event-Driven Microservices
        
        Using EventBridge to decouple microservices for maximum flexibility and scalability.
        
        **Benefits:**
        - Services only communicate via events
        - No direct dependencies between services
        - Easier to scale, modify, and replace individual services
        - Asynchronous processing improves overall system resilience
        
        **Implementation:**
        1. Services publish domain events to EventBridge
        2. EventBridge routes events to interested services
        3. Each service processes events independently
        """)
        
        # ASCII diagram
        st.code("""
           ┌─────────────┐     ┌──────────────┐     ┌─────────────┐
           │ Order       │     │ EventBridge  │     │ Inventory   │
           │ Service     │────▶│ Default Bus  │────▶│ Service     │
           └─────────────┘     │              │     └─────────────┘
                               │              │
           ┌─────────────┐     │              │     ┌─────────────┐
           │ Payment     │◀───┐│              │┌───▶│ Shipping    │
           │ Service     │    ││              ││    │ Service     │
           └─────────────┘    │└──────────────┘│    └─────────────┘
                              │                │
                              └────────────────┘
        """)
    
    with tab2:
        st.markdown("""
        ### Multi-Account Event Architecture
        
        Using EventBridge to share events across multiple AWS accounts with appropriate permissions.
        
        **Benefits:**
        - Account isolation for security and billing
        - Central event management
        - Cross-account event sharing with fine-grained control
        - Organization-wide event flows
        
        **Implementation:**
        1. Create event buses in each account
        2. Configure resource policies to allow cross-account access
        3. Setup rules to route events between accounts
        """)
        
        # ASCII diagram
        st.code("""
           Account A (Production)          Account B (Monitoring)
           ┌────────────────────┐         ┌────────────────────┐
           │                    │         │                    │
           │  Production        │  Event  │  Monitoring        │
           │  Event Bus  ───────┼─────────┼──▶ Event Bus      │
           │                    │ Sharing │                    │
           └────────────────────┘         └─────────┬──────────┘
                                                    │
                                                    ▼
                                            ┌───────────────────┐
                                            │ CloudWatch Logs   │
                                            │ Security Analysis │
                                            │ Compliance Audits │
                                            └───────────────────┘
        """)
    
    with tab3:
        st.markdown("""
        ### SaaS Integration Pattern
        
        Using partner event buses to integrate with third-party SaaS providers securely.
        
        **Benefits:**
        - Native integration with SaaS applications
        - No webhook infrastructure to manage
        - Consistent event handling for all events
        - Secure authentication and authorization
        
        **Implementation:**
        1. Create partner event source in AWS console
        2. Share connection info with SaaS provider
        3. SaaS provider configures their system to send events
        4. Create rules to route partner events to targets
        """)
        
        # ASCII diagram
        st.code("""
           ┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
           │              │     │                  │     │              │
           │  SaaS        │────▶│  Partner         │────▶│  Lambda      │
           │  Provider    │     │  Event Bus       │     │  Functions   │
           │              │     │                  │     │              │
           └──────────────┘     └──────────────────┘     └──────────────┘
                                        │
                                        │
                                        ▼
                                ┌──────────────────┐
                                │                  │
                                │  SQS Queues      │
                                │  Step Functions  │
                                │  API Destinations│
                                └──────────────────┘
        """)
    
    st.header("EventBridge Best Practices")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🏛️ Design Considerations</h4>
            <ul>
                <li>Use multiple event buses to isolate domains</li>
                <li>Design for idempotent event processing</li>
                <li>Implement dead-letter queues for failed events</li>
                <li>Enable event archive for important events</li>
                <li>Use schema registry to maintain event consistency</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>⚡ Performance & Cost</h4>
            <ul>
                <li>Create specific event patterns to reduce processing</li>
                <li>Use content filtering before events reach targets</li>
                <li>Monitor usage metrics for optimization</li>
                <li>Use EventBridge Pipes for batch processing where appropriate</li>
                <li>Compress large event payloads</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔒 Security</h4>
            <ul>
                <li>Use resource-based policies to control access</li>
                <li>Encrypt sensitive event data with KMS</li>
                <li>Monitor API calls with CloudTrail</li>
                <li>Implement least privilege permissions</li>
                <li>Use VPC endpoints for private access</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Function for Lambda page
def lambda_page():
    st.title("AWS Lambda")
    
    try:
        st.image(aws_images["lambda"], width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is AWS Lambda?")
    st.markdown("""
    AWS Lambda is a serverless compute service that runs your code in response to events and automatically manages the underlying 
    compute resources. With Lambda, you can run code without provisioning or managing servers, paying only for the compute time 
    you consume.
    """)
    
    # Create feature highlights with cards
    st.subheader("Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🚀 Serverless Execution</h4>
            <p>Run code without provisioning servers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>⚖️ Automatic Scaling</h4>
            <p>Scales from a few requests to thousands per second</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>💰 Pay-Per-Use</h4>
            <p>Pay only for compute time consumed</p>
        </div>
        """, unsafe_allow_html=True)
        
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔌 Native Integration</h4>
            <p>Works with AWS services and third-party applications</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>💻 Multiple Runtimes</h4>
            <p>Support for Node.js, Python, Java, .NET, Go, Ruby, and more</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🛡️ Built-in Fault Tolerance</h4>
            <p>Automatic replication across Availability Zones</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Lambda Execution Models")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h3>🔄 Synchronous Invocation</h3>
            <p>Client waits for function to complete and return response.</p>
            <h4>Characteristics:</h4>
            <ul>
                <li>Wait for function to complete</li>
                <li>Returns response directly to caller</li>
                <li>Error handling by caller</li>
            </ul>
            <h4>Common Triggers:</h4>
            <ul>
                <li>API Gateway</li>
                <li>Application Load Balancer</li>
                <li>Amazon Cognito</li>
                <li>AWS SDK direct invocation</li>
                <li>CloudFront (Lambda@Edge)</li>
            </ul>
            <h4>Use Cases:</h4>
            <ul>
                <li>API backends</li>
                <li>User authentication</li>
                <li>Real-time processing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h3>📨 Asynchronous Invocation</h3>
            <p>Events queued for processing with no immediate response to initiator.</p>
            <h4>Characteristics:</h4>
            <ul>
                <li>Events queued for processing</li>
                <li>No immediate response</li>
                <li>Automatic retries (2 attempts)</li>
                <li>Dead-letter queue support</li>
            </ul>
            <h4>Common Triggers:</h4>
            <ul>
                <li>S3 bucket events</li>
                <li>SNS notifications</li>
                <li>EventBridge events</li>
                <li>CloudWatch Events</li>
                <li>CodeCommit triggers</li>
            </ul>
            <h4>Use Cases:</h4>
            <ul>
                <li>File processing</li>
                <li>Notifications handling</li>
                <li>Order processing</li>
                <li>Data processing pipelines</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="aws-card">
            <h3>🌊 Stream-Based Invocation</h3>
            <p>Lambda polls stream and invokes function with batch of records.</p>
            <h4>Characteristics:</h4>
            <ul>
                <li>Poll-based processing</li>
                <li>Batch record processing</li>
                <li>Lambda manages polling</li>
                <li>Checkpointing for failures</li>
            </ul>
            <h4>Common Triggers:</h4>
            <ul>
                <li>Kinesis Data Streams</li>
                <li>DynamoDB Streams</li>
                <li>SQS queues</li>
                <li>Amazon MSK</li>
            </ul>
            <h4>Use Cases:</h4>
            <ul>
                <li>Real-time analytics</li>
                <li>Log processing</li>
                <li>Click stream analysis</li>
                <li>IoT data processing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Create a visual representation of Lambda invocation
    st.subheader("Lambda Invocation Models Visualization")
    
    # Create simple chart
    invocation_types = ['Synchronous', 'Asynchronous', 'Stream-Based']
    processing_times = [1, 0.1, 0.5]  # Relative time units
    response_times = [1, 0, 0.5]  # Relative time units
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    x = range(len(invocation_types))
    width = 0.35
    
    rects1 = ax.bar([i - width/2 for i in x], processing_times, width, label='Processing Time')
    rects2 = ax.bar([i + width/2 for i in x], response_times, width, label='Response Time')
    
    ax.set_xticks(x)
    ax.set_xticklabels(invocation_types)
    ax.legend()
    
    ax.set_ylabel('Relative Time')
    ax.set_title('Lambda Invocation Models: Processing vs. Response Time')
    
    st.pyplot(fig)
    
    st.header("Lambda Configuration Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h3>💪 Memory and Performance</h3>
            <h4>Memory Allocation:</h4>
            <ul>
                <li>Range: 128MB to 10,240MB (10GB)</li>
                <li>CPU scales proportionally to memory</li>
                <li>More memory = more CPU = faster execution</li>
            </ul>
            <h4>Execution Time:</h4>
            <ul>
                <li>Maximum timeout: 15 minutes</li>
                <li>Default timeout: 3 seconds</li>
                <li>Best practice: Set timeout to expected duration</li>
            </ul>
            <h4>Concurrency:</h4>
            <ul>
                <li>Default: 1,000 concurrent executions per region</li>
                <li>Reserved concurrency: Guarantee function capacity</li>
                <li>Provisioned concurrency: Pre-warm execution environments</li>
            </ul>
            <div style="margin-top: 15px;">
                <img src="https://d2908q01vomqb2.cloudfront.net/1b6453892473a467d07372d45eb05abc2031647a/2020/12/10/1-83.png" style="max-width: 100%; border-radius: 5px;">
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h3>📦 Deployment and Packaging</h3>
            <h4>Deployment Options:</h4>
            <ul>
                <li>.zip file archive (up to 50 MB compressed)</li>
                <li>Container image (up to 10 GB)</li>
            </ul>
            <h4>Lambda Layers:</h4>
            <ul>
                <li>Shareable code components</li>
                <li>Separate dependencies from function code</li>
                <li>Promotes code reuse and smaller deployments</li>
            </ul>
            <h4>Versions and Aliases:</h4>
            <ul>
                <li>Versions: Immutable snapshots of your function</li>
                <li>Aliases: Pointers to specific versions</li>
                <li>Enable blue/green deployments and traffic shifting</li>
            </ul>
            <div style="margin-top: 15px;">
                <img src="https://docs.aws.amazon.com/lambda/latest/dg/images/versions-aliases.png" style="max-width: 100%; border-radius: 5px;">
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Lambda Integration Patterns")
    st.markdown("""
    <div class="aws-card">
        <h3>🔌 Common Architectures</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 20px;">
            <div>
                <h4>1. API Backend</h4>
                <pre style="background-color: #f8f8f8; padding: 10px; border-radius: 5px; font-size: 0.7em;">
API Gateway → Lambda → Database
                </pre>
                <p>Serverless REST or GraphQL APIs</p>
            </div>
            <div>
                <h4>2. Event Processing</h4>
                <pre style="background-color: #f8f8f8; padding: 10px; border-radius: 5px; font-size: 0.7em;">
Event Source → Lambda → Storage/Database
                </pre>
                <p>Process events from S3, DynamoDB, Kinesis</p>
            </div>
            <div>
                <h4>3. Fan-out Pattern</h4>
                <pre style="background-color: #f8f8f8; padding: 10px; border-radius: 5px; font-size: 0.7em;">
Event → SNS → Multiple Lambda functions
                </pre>
                <p>Parallel processing of events</p>
            </div>
            <div>
                <h4>4. Queue-based Processing</h4>
                <pre style="background-color: #f8f8f8; padding: 10px; border-radius: 5px; font-size: 0.7em;">
SQS → Lambda → Process batch of messages
                </pre>
                <p>Decoupled, scalable processing</p>
            </div>
            <div>
                <h4>5. Orchestration</h4>
                <pre style="background-color: #f8f8f8; padding: 10px; border-radius: 5px; font-size: 0.7em;">
Step Functions → Coordinate multiple Lambda functions
                </pre>
                <p>Complex workflows with state management</p>
            </div>
            <div>
                <h4>6. Real-time Processing</h4>
                <pre style="background-color: #f8f8f8; padding: 10px; border-radius: 5px; font-size: 0.7em;">
Kinesis → Lambda → Analyze/Transform data streams
                </pre>
                <p>Stream processing at scale</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Serverless web application architecture
    st.subheader("Serverless Web Application Architecture")
    
    st.markdown("""
    <div style="text-align: center; margin: 30px 0;">
        <img src="https://d1.awsstatic.com/architecture-diagrams/ArchitectureDiagrams/serverless_web_app_architecture_diagram.5434f715486a0bdd5786cd1c084cd96efa82438f.png" style="max-width: 90%; border-radius: 8px;">
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Lambda Best Practices")
    
    tab1, tab2, tab3 = st.tabs(["Performance", "Cost Optimization", "Monitoring"])
    
    with tab1:
        st.markdown("""
        ### Performance Optimization
        
        #### Optimize Cold Starts:
        - Use Provisioned Concurrency for latency-sensitive applications
        - Keep functions small and focused
        - Minimize dependencies
        - Consider container images for larger dependencies
        
        #### Memory Allocation:
        - Test with different memory settings
        - Often higher memory = better cost/performance
        - Use AWS Lambda Power Tuning tool to find optimal settings
        
        #### Execution Environment Reuse:
        - Initialize SDK clients outside handler
        - Cache static assets in /tmp (up to 512MB)
        - Reuse connections and expensive initializations
        
        ```python
        # Bad practice
        def lambda_handler(event, context):
            # Connection created for each invocation
            s3_client = boto3.client('s3')
            # Process event...
            return response
            
        # Good practice
        # Connection reused across invocations
        s3_client = boto3.client('s3')
        
        def lambda_handler(event, context):
            # Process event...
            return response
        ```
        """)
    
    with tab2:
        st.markdown("""
        ### Cost Optimization
        
        #### Right-size Memory:
        - Find optimal memory/performance balance
        - Use the Lambda pricing calculator to estimate costs
        - Consider the duration reduction from higher memory settings
        
        #### Optimize Function Duration:
        - Reduce unnecessary processing
        - Consider chunking large operations
        - Avoid recursive Lambda invocations
        
        #### Use Event Filtering:
        - Process only relevant events
        - Filter at the source when possible
        - Use SQS for batching when appropriate
        
        #### Cost Comparison Example:
        
        """)
        
        # Create cost comparison chart
        memory_options = [128, 256, 512, 1024, 2048]
        execution_time = [300, 160, 90, 50, 30]  # ms
        cost_per_million = [0.208, 0.208, 0.417, 0.834, 1.668]  # approximate
        
        # Convert to DataFrame
        cost_df = pd.DataFrame({
            'Memory (MB)': memory_options,
            'Execution Time (ms)': execution_time,
            'Cost per Million Invocations ($)': cost_per_million
        })
        
        st.table(cost_df)
        
        # Create bar chart
        c = alt.Chart(cost_df).mark_bar().encode(
            x='Memory (MB):O',
            y='Cost per Million Invocations ($):Q',
            color=alt.Color('Memory (MB):O', scale=alt.Scale(scheme='blues'))
        ).properties(
            title='Lambda Cost by Memory Configuration',
            width=400,
            height=300
        )
        
        st.altair_chart(c, use_container_width=True)
    
    with tab3:
        st.markdown("""
        ### Monitoring and Troubleshooting
        
        #### Implement Structured Logging:
        - Use JSON format for easier parsing
        - Include correlation IDs for tracing requests
        - Log appropriate context without sensitive data
        
        ```python
        import json
        import logging
        
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        
        def lambda_handler(event, context):
            request_id = context.aws_request_id
            
            logger.info(json.dumps({
                'request_id': request_id,
                'event_type': event.get('type'),
                'source': event.get('source'),
                'timestamp': event.get('time')
            }))
            
            # Process event...
            return response
        ```
        
        #### Configure CloudWatch Alarms:
        - Monitor errors, duration, concurrency
        - Set thresholds based on application requirements
        - Create dashboards for key metrics
        
        #### Enable X-Ray Tracing:
        - For distributed tracing and bottleneck identification
        - Trace requests across multiple services
        - Identify latency issues and errors
        
        #### Implement Custom Metrics:
        - Track business-specific metrics
        - Publish custom metrics to CloudWatch
        - Set up alerts on business metrics
        """)
        
        st.image("https://docs.aws.amazon.com/lambda/latest/dg/images/console-monitoring-functions-x-ray-tracing.png", caption="AWS X-Ray Tracing Example", width=700)

# Function for API Gateway page
def api_gateway_page():
    st.title("Amazon API Gateway")
    
    try:
        st.image(aws_images["api_gateway"], width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is Amazon API Gateway?")
    st.markdown("""
    Amazon API Gateway is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, 
    and secure APIs at any scale. API Gateway handles all the tasks involved in accepting and processing up to hundreds of 
    thousands of concurrent API calls, including traffic management, authorization and access control, monitoring, and API version management.
    """)
    
    # Create feature highlights with cards
    st.subheader("Key Features")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""<div class="aws-feature-card">
            <h4>🌐 RESTful & WebSocket APIs</h4>
            <p>Create REST APIs and real-time WebSocket APIs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""<div class="aws-feature-card">
            <h4>⚡ Performance Optimization</h4>
            <p>Caching and throttling capabilities</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""<div class="aws-feature-card">
            <h4>🔄 Request/Response Transformation</h4>
            <p>Transform data formats between clients and backends</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""<div class="aws-feature-card">
            <h4>🔐 Security Features</h4>
            <p>Authentication, authorization, and request validation</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("API Gateway Types")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h3>REST API</h3>
            <h4>Characteristics:</h4>
            <ul>
                <li>Traditional RESTful API design</li>
                <li>Full feature set</li>
                <li>Complex request/response transformations</li>
                <li>API keys and usage plans</li>
                <li>Request validation</li>
            </ul>
            <h4>Integration Types:</h4>
            <ul>
                <li>Lambda functions</li>
                <li>HTTP endpoints</li>
                <li>AWS services</li>
                <li>Mock integrations</li>
            </ul>
            <h4>Use Cases:</h4>
            <ul>
                <li>Complex APIs requiring full features</li>
                <li>Public-facing APIs with monetization</li>
                <li>APIs requiring detailed control</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h3>HTTP API</h3>
            <h4>Characteristics:</h4>
            <ul>
                <li>Simplified, low-latency RESTful API</li>
                <li>Up to 60% cost reduction vs. REST API</li>
                <li>Faster deployment and response times</li>
                <li>Limited feature set</li>
                <li>CORS support built-in</li>
            </ul>
            <h4>Integration Types:</h4>
            <ul>
                <li>Lambda functions</li>
                <li>HTTP endpoints</li>
                <li>Private integrations via ALB/NLB</li>
            </ul>
            <h4>Use Cases:</h4>
            <ul>
                <li>Serverless workloads</li>
                <li>Simple proxy APIs</li>
                <li>High-volume APIs prioritizing performance</li>
                <li>APIs with basic security requirements</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="aws-card">
            <h3>WebSocket API</h3>
            <h4>Characteristics:</h4>
            <ul>
                <li>Persistent two-way communication</li>
                <li>Maintains connection state</li>
                <li>Route messages based on content</li>
                <li>Full-duplex communication</li>
            </ul>
            <h4>Integration Types:</h4>
            <ul>
                <li>Lambda functions</li>
                <li>HTTP endpoints</li>
                <li>AWS services</li>
            </ul>
            <h4>Use Cases:</h4>
            <ul>
                <li>Real-time applications</li>
                <li>Chat applications</li>
                <li>Live dashboards</li>
                <li>Collaborative platforms</li>
                <li>Gaming applications</li>
                <li>Financial trading platforms</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature comparison
    st.subheader("API Gateway Types Comparison")
    
    comparison_data = {
        "Feature": [
            "Latency", 
            "Cost", 
            "Request Validation", 
            "API Keys/Usage Plans", 
            "Response Transformation",
            "WebSocket Support",
            "CORS Support",
            "OpenAPI Support",
            "Private Integrations"
        ],
        "REST API": [
            "Standard",
            "Higher",
            "Yes",
            "Yes",
            "Yes",
            "No",
            "Manual configuration",
            "OpenAPI 3.0",
            "Yes (VPC Link)"
        ],
        "HTTP API": [
            "Lower (~60% better)",
            "Lower (~70% cheaper)",
            "No",
            "No",
            "No",
            "No",
            "Built-in",
            "OpenAPI 3.0",
            "Yes (ALB/NLB)"
        ],
        "WebSocket API": [
            "Real-time",
            "Similar to REST API",
            "No",
            "No",
            "Yes",
            "Yes",
            "N/A",
            "No",
            "Yes (VPC Link)"
        ]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df.set_index("Feature"), use_container_width=True)
    
    st.header("API Gateway Integration Types")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h3>Lambda Integration</h3>
            <h4>Types of Integration:</h4>
            <ul>
                <li><strong>Lambda Proxy Integration:</strong>
                  <ul>
                    <li>Passes entire request to Lambda</li>
                    <li>Lambda returns the entire response</li>
                    <li>Simplest integration model</li>
                  </ul>
                </li>
                <li><strong>Lambda Custom Integration:</strong>
                  <ul>
                    <li>Define request/response mapping templates</li>
                    <li>Transform data between API Gateway and Lambda</li>
                    <li>More control over request/response</li>
                  </ul>
                </li>
            </ul>
            <h4>Best Practices:</h4>
            <ul>
                <li>Use proxy integration for simpler applications</li>
                <li>Custom integration for complex transformations</li>
                <li>Set appropriate timeouts</li>
                <li>Handle errors properly in Lambda code</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h3>HTTP Integration</h3>
            <h4>Types of Integration:</h4>
            <ul>
                <li><strong>HTTP Proxy Integration:</strong>
                  <ul>
                    <li>Passes request to HTTP endpoint</li>
                    <li>Returns endpoint response directly</li>
                    <li>Minimal configuration</li>
                  </ul>
                </li>
                <li><strong>HTTP Custom Integration:</strong>
                  <ul>
                    <li>Transform requests before sending to backend</li>
                    <li>Transform responses before returning to client</li>
                    <li>Apply content type conversions</li>
                  </ul>
                </li>
            </ul>
            <h4>Best Practices:</h4>
            <ul>
                <li>Use for integrating with existing HTTP APIs</li>
                <li>Set up appropriate timeouts</li>
                <li>Consider caching for frequently accessed resources</li>
                <li>Monitor backend health with CloudWatch</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # API Gateway Lambda Proxy Integration Diagram
    st.subheader("Lambda Proxy Integration Flow")
    
    st.markdown("""
    <div style="text-align: center; margin: 30px 0;">
        <img src="https://docs.aws.amazon.com/apigateway/latest/developerguide/images/api-gateway-simple-proxy.png" style="max-width: 80%; border-radius: 8px;">
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Security Features")
    
    # Create security options as expandable sections
    with st.expander("🔑 IAM Authorization"):
        st.markdown("""
        Uses AWS Signature Version 4 (SigV4) signing to authenticate and authorize API calls 
        based on the requesting user's IAM permissions.
        
        **When to use:**
        - For internal APIs consumed by other AWS services or resources
        - When you want to leverage existing IAM roles and permissions
        - For AWS service-to-service communication
        
        **Implementation:**
        ```json
        {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Action": "execute-api:Invoke",
              "Resource": "arn:aws:execute-api:region:account-id:api-id/stage/METHOD/resource"
            }
          ]
        }
        ```
        """)
    
    with st.expander("🧩 Lambda Authorizers"):
        st.markdown("""
        Custom authorization logic implemented in a Lambda function to control access to your API.
        
        **Types:**
        - **Token-based:** Validates tokens in headers (like JWT, OAuth)
        - **Request-based:** Uses multiple request parameters (headers, query string, context)
        
        **Benefits:**
        - Fully customizable authorization logic
        - Can integrate with existing auth systems
        - Supports complex authorization schemes
        - Results are cached for performance
        
        **Implementation Example (Node.js):**
        ```javascript
        exports.handler = function(event, context, callback) {
            // Get token from the Authorization header
            var token = event.authorizationToken;
            
            // Verify token and get user information
            // ...custom verification logic...
            
            // Return IAM policy document that allows/denies access
            callback(null, {
                principalId: 'user-id',
                policyDocument: {
                    Version: '2012-10-17',
                    Statement: [{
                        Action: 'execute-api:Invoke',
                        Effect: 'Allow',
                        Resource: event.methodArn
                    }]
                }
            });
        };
        ```
        """)
    
    with st.expander("👥 Cognito User Pools"):
        st.markdown("""
        Uses Amazon Cognito user pools to control who can access your API by requiring tokens from authenticated users.
        
        **Features:**
        - User management and authentication service
        - Handles registration, login, token validation
        - OAuth 2.0 and OpenID Connect support
        - Social identity provider integration (Google, Facebook, etc.)
        
        **Benefits:**
        - Managed user directory
        - Handles token issuance and validation
        - MFA support
        - Integration with identity providers
        
        **Implementation:**
        1. Create a Cognito User Pool
        2. Configure an app client
        3. Configure API Gateway to use the User Pool authorizer
        4. Client includes ID or access token in requests
        """)
    
    with st.expander("🔑 API Keys and Usage Plans"):
        st.markdown("""
        Control access to your APIs using API keys associated with usage plans that define throttling and quota limits.
        
        **Features:**
        - Track and limit usage by API key
        - Set throttling limits (requests per second)
        - Set quota limits (requests per day, week, month)
        - Monitor usage per customer
        
        **Best For:**
        - API monetization
        - Partner API access
        - Tiered API access (free tier, premium tier)
        - Usage tracking by client
        
        **Note:** API keys should not be used as a primary authentication method, 
        but rather for metering and throttling after authentication.
        """)
    
    with st.expander("📜 Resource Policies"):
        st.markdown("""
        JSON policy documents attached to your API that control which IP addresses, VPC endpoints, or AWS accounts can access your API.
        
        **Use Cases:**
        - Restrict API access to specific IP ranges
        - Allow access only from VPC endpoints
        - Allow access only from specific AWS accounts
        
        **Example Policy (IP restriction):**
        ```json
        {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Principal": "*",
              "Action": "execute-api:Invoke",
              "Resource": "execute-api:/*/*/*"
            },
            {
              "Effect": "Deny",
              "Principal": "*",
              "Action": "execute-api:Invoke",
              "Resource": "execute-api:/*/*/*",
              "Condition": {
                "NotIpAddress": {
                  "aws:SourceIp": [
                    "192.0.2.0/24",
                    "198.51.100.0/24"
                  ]
                }
              }
            }
          ]
        }
        ```
        """)
    
    with st.expander("🔒 Mutual TLS (mTLS)"):
        st.markdown("""
        Mutual TLS authentication requires clients to present X.509 certificates to verify their identity.
        
        **Features:**
        - Two-way TLS authentication
        - Server authenticates client, client authenticates server
        - Enhanced security for sensitive APIs
        
        **Use Cases:**
        - Financial services APIs
        - Healthcare applications
        - Enterprise-to-enterprise integration
        - IoT device authentication
        
        **Implementation:**
        1. Configure a custom domain name in API Gateway
        2. Upload a server certificate
        3. Configure mutual TLS by uploading trusted certificate authorities
        4. Clients must present valid certificates in requests
        """)
    
    st.header("Performance and Optimization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h3>⚡ Caching</h3>
            <ul>
                <li>Enable API caching to improve performance</li>
                <li>Cache TTL configurable (0-3600 seconds)</li>
                <li>Cache capacity between 0.5GB to 237GB</li>
                <li>Can flush cache as needed</li>
                <li>Cache encryption option available</li>
            </ul>
            <h4>Best Practices:</h4>
            <ul>
                <li>Enable caching for read-heavy APIs</li>
                <li>Set appropriate TTL based on data volatility</li>
                <li>Use cache invalidation for immediate updates</li>
                <li>Consider per-key caching for user-specific responses</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h3>🔄 Throttling</h3>
            <ul>
                <li>Account-level throttling (default: 10,000 RPS)</li>
                <li>Method-level throttling with usage plans</li>
                <li>Stage-level throttling for different environments</li>
                <li>Burst limits for handling traffic spikes</li>
            </ul>
            <h4>Deployment Options:</h4>
            <ul>
                <li><strong>Edge-optimized:</strong> Cached at CloudFront edge locations (default)</li>
                <li><strong>Regional:</strong> For clients in the same region</li>
                <li><strong>Private:</strong> Accessible only from your VPC using VPC endpoint</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Deployment stages diagram
    st.subheader("API Gateway Deployment Workflow")
    
    st.code("""
    Development Stage → Testing Stage → Production Stage
         │                   │                 │
         ▼                   ▼                 ▼
     Dev APIs             Test APIs         Prod APIs
    Rate: 100 RPS        Rate: 500 RPS     Rate: 1000 RPS
    Logging: Debug       Logging: Info      Logging: Error
    Cache: Disabled      Cache: 1.0 GB      Cache: 5.0 GB
    """)
    
    # Monitoring capabilities
    st.header("API Gateway Monitoring")
    
    st.markdown("""
    <div class="aws-card">
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
            <div>
                <h3>📊 CloudWatch Metrics</h3>
                <ul>
                    <li>4XX/5XX Error rates</li>
                    <li>Latency statistics</li>
                    <li>Cache hit/miss ratio</li>
                    <li>Integration latency</li>
                    <li>Count of requests</li>
                </ul>
            </div>
            <div>
                <h3>📜 Access Logging</h3>
                <ul>
                    <li>Customizable log formats</li>
                    <li>Request/response body logging</li>
                    <li>Request parameters</li>
                    <li>User context information</li>
                    <li>Integration with CloudWatch Logs</li>
                </ul>
            </div>
            <div>
                <h3>🔍 X-Ray Tracing</h3>
                <ul>
                    <li>End-to-end request tracing</li>
                    <li>Identify bottlenecks</li>
                    <li>Analyze latency distribution</li>
                    <li>Troubleshoot errors</li>
                    <li>Visualize service map</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Best practices summary
    st.header("API Gateway Best Practices")
    
    st.markdown("""
    <div class="aws-card">
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
            <div>
                <h4>🛡️ Security</h4>
                <ul>
                    <li>Use appropriate authorization for each API</li>
                    <li>Enable request validation</li>
                    <li>Implement throttling limits</li>
                    <li>Use SSL/TLS for all APIs</li>
                    <li>Consider AWS WAF for additional protection</li>
                </ul>
            </div>
            <div>
                <h4>🚀 Performance</h4>
                <ul>
                    <li>Enable caching for read-heavy endpoints</li>
                    <li>Use compressed payloads</li>
                    <li>Optimize Lambda integration timeouts</li>
                    <li>Choose appropriate deployment type</li>
                    <li>Implement pagination for large responses</li>
                </ul>
            </div>
            <div>
                <h4>📋 Operations</h4>
                <ul>
                    <li>Use stages for environment isolation</li>
                    <li>Implement canary deployments for testing</li>
                    <li>Configure detailed logging and monitoring</li>
                    <li>Use custom domain names</li>
                    <li>Implement CI/CD for API deployments</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Function for Containers page
def containers_page():
    st.title("Containers on AWS")
    
    try:
        st.image(aws_images["containers"], width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What are Containers?")
    st.markdown("""
    Containers are lightweight, portable, and standardized units that package application code, dependencies, and runtime 
    environments together. They provide consistent execution environments across different infrastructure, making applications 
    more portable and deployable.
    """)
    
    # Container benefits
    st.subheader("Key Benefits of Containers")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🚀 Consistency</h4>
            <p>Consistent environments from development to production</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>⚡ Efficiency</h4>
            <p>Lightweight and efficient resource utilization</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>⏱️ Speed</h4>
            <p>Faster startup times compared to virtual machines</p>
        </div>
        """, unsafe_allow_html=True)
        
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🛡️ Isolation</h4>
            <p>Strong isolation between applications</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>👩‍💻 Productivity</h4>
            <p>Improved developer productivity and deployment velocity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>📈 Scalability</h4>
            <p>Easy scaling and high availability</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Container vs VM diagram
    st.subheader("Containers vs. Virtual Machines")
    
    st.markdown("""
    <div style="display: flex; justify-content: center; margin: 30px 0;">
        <img src="images/containers_vs_vms.png" style="max-width: 80%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Container Orchestration")
    st.markdown("""
    Container orchestration automates the deployment, management, scaling, networking, and availability of container-based applications. 
    Orchestrators handle tasks such as:
    
    - Scheduling containers across a cluster of machines
    - Ensuring high availability and fault tolerance
    - Scaling containers based on demand
    - Service discovery and load balancing
    - Managing network connectivity between containers
    - Handling storage persistence
    - Rolling updates and rollbacks
    """)
    
    st.header("AWS Container Services")
    
    tab1, tab2, tab3 = st.tabs(["Amazon ECS", "Amazon EKS", "AWS Fargate"])
    
    with tab1:
        st.subheader("Amazon Elastic Container Service (ECS)")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            try:
                st.image(aws_images["ecs"], width=300)
            except:
                st.warning("ECS image could not be displayed")
        
        with col2:
            st.markdown("""
            **What is ECS?**
            
            Amazon Elastic Container Service (ECS) is a fully managed container orchestration service that helps you run, stop, 
            and manage containers on a cluster. ECS is AWS's own container orchestration platform integrated with the AWS ecosystem.
            """)
        
        st.markdown("""
        <div class="aws-card">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h4>Key Features</h4>
                    <ul>
                        <li>AWS-native container orchestration</li>
                        <li>Deep integration with AWS services (ALB, CloudWatch, IAM, etc.)</li>
                        <li>Task definitions for defining container applications</li>
                        <li>Service auto-scaling</li>
                        <li>Supports both EC2 and Fargate launch types</li>
                        <li>Built-in logging and monitoring</li>
                        <li>Simplified networking with VPC integration</li>
                    </ul>
                </div>
                <div>
                    <h4>Use Cases</h4>
                    <ul>
                        <li>Microservices architectures</li>
                        <li>Batch processing workloads</li>
                        <li>Web applications and APIs</li>
                        <li>Long-running services</li>
                        <li>Machine learning deployments</li>
                        <li>DevOps CI/CD pipelines</li>
                        <li>Scheduled tasks and cron jobs</li>
                    </ul>
                </div>
            </div>
            <h4>ECS Components</h4>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 15px;">
                <div style="background-color: #f0f7fb; padding: 10px; border-radius: 5px;">
                    <h5>Cluster</h5>
                    <p>Logical grouping of EC2 instances or Fargate capacity</p>
                </div>
                <div style="background-color: #f0f7fb; padding: 10px; border-radius: 5px;">
                    <h5>Task Definition</h5>
                    <p>Blueprint for your application (containers, resources, networking)</p>
                </div>
                <div style="background-color: #f0f7fb; padding: 10px; border-radius: 5px;">
                    <h5>Service</h5>
                    <p>Maintains and scales multiple copies of a task definition</p>
                </div>
                <div style="background-color: #f0f7fb; padding: 10px; border-radius: 5px;">
                    <h5>Task</h5>
                    <p>Instance of a task definition running on a cluster</p>
                </div>
                <div style="background-color: #f0f7fb; padding: 10px; border-radius: 5px;">
                    <h5>Container Instance</h5>
                    <p>EC2 instance running ECS container agent</p>
                </div>
                <div style="background-color: #f0f7fb; padding: 10px; border-radius: 5px;">
                    <h5>Launch Type</h5>
                    <p>EC2 (self-managed) or Fargate (serverless)</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Amazon Elastic Kubernetes Service (EKS)")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            try:
                st.image(aws_images["eks"], width=300)
            except:
                st.warning("EKS image could not be displayed")
        
        with col2:
            st.markdown("""
            **What is EKS?**
            
            Amazon Elastic Kubernetes Service (EKS) is a managed Kubernetes service that makes it easy to run Kubernetes 
            on AWS without needing to install, operate, and maintain your own Kubernetes control plane.
            """)
        
        st.markdown("""
        <div class="aws-card">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h4>Key Features</h4>
                    <ul>
                        <li>Fully managed Kubernetes control plane</li>
                        <li>Certified Kubernetes conformance</li>
                        <li>Integration with AWS services (IAM, VPC, etc.)</li>
                        <li>Support for both EC2 and Fargate compute</li>
                        <li>Managed node groups</li>
                        <li>Kubernetes add-on management</li>
                        <li>Multi-AZ high availability</li>
                    </ul>
                </div>
                <div>
                    <h4>Use Cases</h4>
                    <ul>
                        <li>Organizations with existing Kubernetes expertise</li>
                        <li>Multi-cloud container strategies</li>
                        <li>Complex container orchestration requirements</li>
                        <li>When Kubernetes-specific features are needed</li>
                        <li>Applications requiring open-source ecosystem tools</li>
                        <li>Large-scale microservices deployments</li>
                    </ul>
                </div>
            </div>
            <h4>EKS Components</h4>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 15px;">
                <div style="background-color: #f0f7fb; padding: 10px; border-radius: 5px;">
                    <h5>Control Plane</h5>
                    <p>Managed Kubernetes masters across multiple AZs</p>
                </div>
                <div style="background-color: #f0f7fb; padding: 10px; border-radius: 5px;">
                    <h5>Node Groups</h5>
                    <p>Collections of EC2 instances registered in a cluster</p>
                </div>
                <div style="background-color: #f0f7fb; padding: 10px; border-radius: 5px;">
                    <h5>Pod</h5>
                    <p>Group of containers with shared storage and network</p>
                </div>
                <div style="background-color: #f0f7fb; padding: 10px; border-radius: 5px;">
                    <h5>Deployment</h5>
                    <p>Manages a replicated application on your cluster</p>
                </div>
                <div style="background-color: #f0f7fb; padding: 10px; border-radius: 5px;">
                    <h5>Service</h5>
                    <p>Defines access policy for pods</p>
                </div>
                <div style="background-color: #f0f7fb; padding: 10px; border-radius: 5px;">
                    <h5>Namespace</h5>
                    <p>Virtual clusters for resource isolation</p>
                </div>
            </div>
            <h4>EKS Architecture</h4>
            <div style="text-align: center; margin-top: 20px;">
                <img src="https://d1.awsstatic.com/product-marketing/EKS/product-page-diagram_Amazon-EKS%402x.dab8ba69bad0c8b5598759d7ae3bc5b1c7bbf0a8.png" style="max-width: 90%; border-radius: 5px;">
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("AWS Fargate")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            try:
                st.image(aws_images["fargate"], width=300)
            except:
                st.warning("Fargate image could not be displayed")
        
        with col2:
            st.markdown("""
            **What is Fargate?**
            
            AWS Fargate is a serverless compute engine for containers that works with both Amazon ECS and Amazon EKS. 
            Fargate eliminates the need to provision and manage servers, allowing you to focus on application development.
            """)
        
        st.markdown("""
        <div class="aws-card">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h4>Key Features</h4>
                    <ul>
                        <li>Serverless compute for containers</li>
                        <li>Pay-per-task pricing model</li>
                        <li>No server management</li>
                        <li>Application-level isolation</li>
                        <li>Compatible with both ECS and EKS</li>
                        <li>Automatic scaling</li>
                        <li>Integrated with VPC networking</li>
                    </ul>
                </div>
                <div>
                    <h4>Use Cases</h4>
                    <ul>
                        <li>Unpredictable workloads</li>
                        <li>Development and test environments</li>
                        <li>Batch processing jobs</li>
                        <li>Microservices with variable load</li>
                        <li>Applications requiring high security isolation</li>
                        <li>Teams wanting to minimize operational overhead</li>
                        <li>Migrating from on-premises to cloud-native</li>
                    </ul>
                </div>
            </div>
            <h4>How Fargate Works</h4>
            <div style="display: flex; align-items: center; justify-content: center; margin-top: 20px;">
                <div style="background-color: #f0f7fb; padding: 20px; border-radius: 5px; text-align: center; max-width: 90%;">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div style="text-align: center; padding: 10px; width: 30%;">
                            <h5>1. Define</h5>
                            <p>Specify CPU, memory, networking, IAM policies</p>
                        </div>
                        <div style="font-size: 24px;">→</div>
                        <div style="text-align: center; padding: 10px; width: 30%;">
                            <h5>2. Deploy</h5>
                            <p>Launch containers with ECS or EKS</p>
                        </div>
                        <div style="font-size: 24px;">→</div>
                        <div style="text-align: center; padding: 10px; width: 30%;">
                            <h5>3. Scale</h5>
                            <p>Fargate automatically scales and manages infrastructure</p>
                        </div>
                    </div>
                </div>
            </div>
            <h4>Fargate Architecture with ECS</h4>
            <div style="text-align: center; margin-top: 20px;">
                <img src="https://d1.awsstatic.com/re19/FargateonEKS/Product-Page-Diagram_Fargate_How-it-Works.debb994482e31d2d4b58139e6cdd994ce4c23d70.png" style="max-width: 90%; border-radius: 5px;">
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Choosing the Right Container Service")
    
    # Create a decision matrix table
    selection_data = {
        "Consideration": [
            "Control Plane", 
            "Infrastructure Management", 
            "AWS Integration", 
            "Learning Curve",
            "Portability",
            "Cost Model",
            "Best For"
        ],
        "Amazon ECS": [
            "AWS-proprietary",
            "EC2 self-managed, or Fargate",
            "Deep, native integration",
            "Lower, AWS-specific",
            "AWS-specific",
            "No additional charge for ECS (pay for resources)",
            "AWS-focused organizations wanting simplicity"
        ],
        "Amazon EKS": [
            "Kubernetes",
            "EC2 self-managed, managed node groups, or Fargate",
            "Kubernetes-focused with AWS integrations",
            "Higher, Kubernetes knowledge required",
            "Highly portable (Kubernetes standard)",
            "$0.10 per hour per cluster ($73 per month)",
            "Organizations needing Kubernetes or multi-cloud compatibility"
        ],
        "AWS Fargate": [
            "N/A (Serverless)",
            "None (serverless)",
            "Works with both ECS and EKS",
            "Lowest, focus on containers only",
            "Depends on ECS or EKS usage",
            "Pay per vCPU and memory allocated to containers",
            "Teams wanting to focus on applications without managing infrastructure"
        ]
    }
    
    selection_df = pd.DataFrame(selection_data)
    st.dataframe(selection_df.set_index("Consideration"), use_container_width=True)
    
    # Decision flowchart for container service selection
    st.subheader("Container Service Selection Guide")
    
    st.markdown("""
    <div class="aws-card">
        <div style="padding: 15px;">
            <h4>Answer these questions to determine the best service for your needs:</h4>
            <div style="margin: 20px 0;">
                <p><strong>1. Do you want to manage infrastructure?</strong></p>
                <ul>
                    <li>No → Consider AWS Fargate</li>
                    <li>Yes → Continue to question 2</li>
                </ul>
            </div>
            <div style="margin: 20px 0;">
                <p><strong>2. Do you need Kubernetes-specific features or plan to use multiple clouds?</strong></p>
                <ul>
                    <li>Yes → Consider Amazon EKS</li>
                    <li>No → Continue to question 3</li>
                </ul>
            </div>
            <div style="margin: 20px 0;">
                <p><strong>3. Do you prefer deep AWS integration and simpler management?</strong></p>
                <ul>
                    <li>Yes → Consider Amazon ECS</li>
                    <li>No → Reconsider your requirements or evaluate EKS for advanced features</li>
                </ul>
            </div>
            <div style="margin: 20px 0;">
                <p><strong>4. Do you have mixed workloads with different infrastructure needs?</strong></p>
                <ul>
                    <li>Yes → Consider using a combination (e.g., ECS with both EC2 and Fargate)</li>
                    <li>No → Choose the single platform that best meets your primary workload needs</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Container Deployment Strategies")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Blue/Green Deployment", "Rolling Updates", "Canary Deployments", "A/B Testing"])
    
    with tab1:
        st.markdown("""
        ### Blue/Green Deployment
        
        Blue/Green deployment involves creating a completely new environment alongside the existing one, 
        then switching traffic all at once when the new version is ready.
        
        **Benefits:**
        - Zero downtime deployment
        - Easy and fast rollback (switch back to old environment)
        - Opportunity for full testing in production-like environment
        - No mixed versions running simultaneously
        
        **Implementation:**
        1. Create new "green" environment with updated application
        2. Test green environment thoroughly
        3. Switch traffic from blue to green environment
        4. Monitor for issues
        5. If problems occur, switch back to blue environment
        
        **AWS Services:**
        - ECS: Use service deployments with a new task definition
        - EKS: Use Kubernetes deployments with separate replica sets
        - Route 53 or ALB for traffic shifting
        """)
        
        # Blue/Green diagram
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <img src="https://d1.awsstatic.com/product-marketing/CodeDeploy/Products-Page-Diagram_AWS-CodeDeploy_Blue-Green-Deployments%402x.9a08890d8f6d5a4b679f74067e2be5b1c7b6a703.png" style="max-width: 80%; border-radius: 5px;">
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        ### Rolling Updates
        
        Rolling updates gradually replace instances of the old version with the new version, 
        allowing a controlled transition without downtime.
        
        **Benefits:**
        - No additional infrastructure needed
        - Gradual deployment reduces risk
        - Automatic rollout and scaling
        - Built into container orchestration platforms
        
        **Implementation:**
        1. Update a small batch of containers
        2. Wait for new containers to be healthy
        3. Route traffic to new containers
        4. Continue process until all containers are updated
        
        **AWS Services:**
        - ECS: Configure minimum healthy percent and maximum percent parameters
        - EKS: Use Kubernetes rolling update strategy for deployments
        """)
        
        # Rolling update diagram
        st.code("""
        Initial State:       [V1] [V1] [V1] [V1]
        
        Update Step 1:       [V1] [V1] [V2] [V1]
        
        Update Step 2:       [V1] [V2] [V2] [V1]
        
        Update Step 3:       [V2] [V2] [V2] [V1]
        
        Final State:         [V2] [V2] [V2] [V2]
        """)
    
    with tab3:
        st.markdown("""
        ### Canary Deployments
        
        Canary deployments route a small percentage of traffic to the new version while 
        maintaining most traffic on the stable version.
        
        **Benefits:**
        - Reduced risk by limiting exposure to the new version
        - Real user testing with limited blast radius
        - Ability to monitor and analyze new version's performance
        - Gradual traffic shifting based on confidence
        
        **Implementation:**
        1. Deploy new version alongside existing version
        2. Route small percentage (e.g., 5%) of traffic to new version
        3. Monitor performance, errors, and user feedback
        4. Gradually increase traffic to new version if successful
        5. Complete migration or rollback based on results
        
        **AWS Services:**
        - ECS: Use AWS App Mesh for advanced traffic routing
        - EKS: Use Kubernetes service mesh (Istio, Linkerd) or AWS App Mesh
        - ALB weighted target groups
        """)
        
        # Canary diagram
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <img src="https://d1.awsstatic.com/product-marketing/AppMesh/Product-Page-Diagram_AWS-App-Mesh_Canary-Deployment%402x.03c5a3d6d9c2ee7d842b44b6c8d3984a5745d852.png" style="max-width: 80%; border-radius: 5px;">
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("""
        ### A/B Testing
        
        A/B testing serves different versions to different users based on specific criteria, 
        allowing you to compare versions and make data-driven decisions.
        
        **Benefits:**
        - Test features with specific user segments
        - Collect data on user behavior and preferences
        - Make decisions based on metrics rather than opinions
        - Can target based on user attributes, geography, devices, etc.
        
        **Implementation:**
        1. Deploy both versions simultaneously
        2. Configure routing rules based on criteria (user ID, cookies, headers, etc.)
        3. Collect data on key metrics
        4. Analyze results and make decisions
        5. Roll out winning version to all users
        
        **AWS Services:**
        - ECS/EKS with AWS App Mesh
        - Lambda with API Gateway
        - CloudFront with Lambda@Edge for routing
        - Amazon CloudWatch for metric collection
        """)
        
        # A/B testing diagram
        st.code("""
                  ┌─────────────────┐
                  │                 │
                  │  Load Balancer  │
                  │                 │
                  └──────┬──────────┘
                         │
                 ┌───────┴───────┐
                 │               │
        ┌────────▼─────┐  ┌──────▼────────┐
        │              │  │               │
        │   Version A  │  │   Version B   │
        │    (90%)     │  │    (10%)      │
        │              │  │               │
        └──────────────┘  └───────────────┘
                 │               │
                 └───────┬───────┘
                         │
                  ┌──────▼──────┐
                  │             │
                  │  Analytics  │
                  │             │
                  └─────────────┘
        """)

# Function for Security Services page
def security_services_page():
    st.title("Additional AWS Security Services")
    
    st.header("AWS Security Services Overview")
    st.markdown("""
    AWS provides a comprehensive suite of security services to help you protect your data, accounts, and workloads in the cloud. 
    These services complement the core security features built into AWS services and provide additional layers of protection for 
    your applications and data.
    """)
    
    # Create a visual representation of security layers
    st.subheader("AWS Security Service Categories")
    
    st.markdown("""
    <div style="display: flex; justify-content: center; margin: 30px 0;">
        <div style="text-align: center;">
            <img src="Content_Review_5/images/security_catalog.png" style="max-width: 80%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create service groups
    service_groups = [
        {
            "name": "Secrets & Certificates Management",
            "services": [
                {
                    "name": "AWS Secrets Manager",
                    "image": "secrets_manager",
                    "description": "Helps you protect access to your applications, services, and IT resources without the upfront investment and ongoing maintenance costs of operating your own secrets management infrastructure.",
                    "features": [
                        "Secure storage of secrets (passwords, API keys, tokens)",
                        "Automatic secrets rotation",
                        "Fine-grained access control with IAM",
                        "Encryption at rest and in transit",
                        "Integration with AWS services",
                        "Centralized audit trail"
                    ],
                    "use_cases": [
                        "Database credential management",
                        "API key storage and rotation",
                        "OAuth token management",
                        "Storing TLS certificates",
                        "Application configuration secrets"
                    ]
                },
                {
                    "name": "AWS Certificate Manager (ACM)",
                    "image": "acm",
                    "description": "Handles the complexity of creating, storing, and renewing public and private SSL/TLS X.509 certificates and keys that protect your AWS websites and applications.",
                    "features": [
                        "Free public SSL/TLS certificates",
                        "Automated certificate renewal",
                        "Easy deployment to integrated services",
                        "Private certificate authority option",
                        "Managed certificate deployment",
                        "Centralized certificate management"
                    ],
                    "use_cases": [
                        "Securing websites with HTTPS",
                        "Protecting API endpoints",
                        "Securing internal applications",
                        "Implementing mutual TLS (mTLS)",
                        "Managing certificates for CloudFront distributions"
                    ]
                }
            ]
        },
        {
            "name": "Identity & Access Management",
            "services": [
                {
                    "name": "AWS IAM Identity Center",
                    "image": "iam_identity_center",
                    "description": "AWS IAM Identity Center (successor to AWS Single Sign-On) helps you securely create or connect your workforce identities and manage their access centrally across AWS accounts and applications.",
                    "features": [
                        "Single sign-on for AWS accounts and applications",
                        "Centralized permission management",
                        "Multiple identity source options",
                        "Integration with AWS Organizations",
                        "Attribute-based access control",
                        "User portal for application access"
                    ],
                    "use_cases": [
                        "Multi-account AWS access management",
                        "SaaS application access control",
                        "Workforce identity federation",
                        "Centralizing access management",
                        "Simplifying permission management"
                    ]
                },
                {
                    "name": "AWS Directory Service",
                    "image": "directory_service",
                    "description": "AWS Directory Service provides multiple ways to use Microsoft Active Directory (AD) with other AWS services. Directories store information about users, groups, and devices, and administrators use them to manage access to information and resources.",
                    "features": [
                        "Managed Microsoft Active Directory",
                        "Multiple directory types (Microsoft AD, Simple AD, AD Connector)",
                        "High availability and automatic failover",
                        "Seamless integration with AWS services",
                        "Domain join capabilities",
                        "Group policy support"
                    ],
                    "use_cases": [
                        "Windows workload management",
                        "Centralized user authentication",
                        "Extending on-premises AD to AWS",
                        "Providing directory services for AWS resources",
                        "Simplifying AWS resource access management"
                    ]
                },
                {
                    "name": "Amazon Cognito",
                    "image": "cognito",
                    "description": "Amazon Cognito provides authentication, authorization, and user management for web and mobile applications. It enables you to add user sign-up, sign-in, and access control to your applications easily and securely.",
                    "features": [
                        "User directories with sign-up and sign-in",
                        "Identity federation with social and enterprise IdPs",
                        "Multi-factor authentication",
                        "Access control for AWS resources",
                        "Secure storage of app data",
                        "Standards-based authentication (OAuth 2.0, OIDC, SAML)"
                    ],
                    "use_cases": [
                        "Mobile and web application authentication",
                        "Social identity federation",
                        "Secure AWS resource access from applications",
                        "Customer identity management",
                        "API authorization"
                    ]
                }
            ]
        },
        {
            "name": "Patch & Maintenance Management",
            "services": [
                {
                    "name": "AWS Systems Manager Patch Manager",
                    "image": "patch_manager",
                    "description": "AWS Systems Manager Patch Manager automates the process of patching managed instances with both security-related and other types of updates. You can use Patch Manager to apply patches for both operating systems and applications.",
                    "features": [
                        "Automated patch management",
                        "Support for Windows and Linux",
                        "Patch compliance reporting",
                        "Scheduled patching with maintenance windows",
                        "Customizable patch baselines",
                        "Centralized management across accounts"
                    ],
                    "use_cases": [
                        "Security patch deployment",
                        "OS and application updates",
                        "Compliance management",
                        "Vulnerability remediation",
                        "Centralized patch management"
                    ]
                }
            ]
        },
        {
            "name": "Resource Sharing",
            "services": [
                {
                    "name": "AWS Resource Access Manager (RAM)",
                    "image": "ram",
                    "description": "AWS Resource Access Manager (RAM) helps you securely share your resources across AWS accounts, within your organization or organizational units, and with IAM roles and users for supported resource types.",
                    "features": [
                        "Secure resource sharing across accounts",
                        "Fine-grained access controls",
                        "Centralized view of shared resources",
                        "Integration with AWS Organizations",
                        "No additional charge for the service"
                    ],
                    "use_cases": [
                        "Multi-account architectures",
                        "Shared services models",
                        "Central IT resource sharing",
                        "Sharing VPC subnets across accounts",
                        "Collaborative development environments"
                    ]
                }
            ]
        }
    ]
    
    # Display service groups
    for group in service_groups:
        st.header(group["name"])
        
        for service in group["services"]:
            with st.expander(f"📌 {service['name']}", expanded=False):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    try:
                        st.image(aws_images[service["image"]], width=300)
                    except:
                        st.warning(f"{service['name']} image could not be displayed")
                
                with col2:
                    st.markdown(f"""
                    ### {service['name']}
                    
                    {service['description']}
                    """)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div class="aws-feature-card">
                        <h4>Key Features</h4>
                        <ul> """ + "".join([f"<li>{feature}</li>" for feature in service["features"]]) + """
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="aws-feature-card">
                        <h4>Use Cases</h4>
                        <ul> """ + "".join([f"<li>{use_case}</li>" for use_case in service["use_cases"]]) + """
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.header("Security Service Selection Guide")
    
    st.markdown("""
    <div class="aws-card">
        <table style="width:100%; border-collapse: collapse;">
            <thead>
                <tr style="background-color: #232F3E; color: white;">
                    <th style="padding: 10px; text-align: left;">If You Need To...</th>
                    <th style="padding: 10px; text-align: left;">Consider Using...</th>
                </tr>
            </thead>
            <tbody>
                <tr style="background-color: #f8f8f8;">
                    <td style="padding: 10px;">Manage application secrets and credentials</td>
                    <td style="padding: 10px;"><strong>AWS Secrets Manager</strong></td>
                </tr>
                <tr>
                    <td style="padding: 10px;">Deploy and manage SSL/TLS certificates</td>
                    <td style="padding: 10px;"><strong>AWS Certificate Manager</strong></td>
                </tr>
                <tr style="background-color: #f8f8f8;">
                    <td style="padding: 10px;">Automate OS and application patching</td>
                    <td style="padding: 10px;"><strong>Systems Manager Patch Manager</strong></td>
                </tr>
                <tr>
                    <td style="padding: 10px;">Centralize access to multiple AWS accounts</td>
                    <td style="padding: 10px;"><strong>IAM Identity Center</strong></td>
                </tr>
                <tr style="background-color: #f8f8f8;">
                    <td style="padding: 10px;">Manage Microsoft Active Directory workloads</td>
                    <td style="padding: 10px;"><strong>AWS Directory Service</strong></td>
                </tr>
                <tr>
                    <td style="padding: 10px;">Share AWS resources across accounts</td>
                    <td style="padding: 10px;"><strong>AWS Resource Access Manager</strong></td>
                </tr>
                <tr style="background-color: #f8f8f8;">
                    <td style="padding: 10px;">Add user authentication to applications</td>
                    <td style="padding: 10px;"><strong>Amazon Cognito</strong></td>
                </tr>
                <tr>
                    <td style="padding: 10px;">Provide federated access to AWS resources</td>
                    <td style="padding: 10px;"><strong>AWS IAM with identity federation</strong></td>
                </tr>
                <tr style="background-color: #f8f8f8;">
                    <td style="padding: 10px;">Secure data with encryption</td>
                    <td style="padding: 10px;"><strong>AWS Key Management Service (KMS)</strong></td>
                </tr>
                <tr>
                    <td style="padding: 10px;">Protect web applications from attacks</td>
                    <td style="padding: 10px;"><strong>AWS WAF and Shield</strong></td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    # Architectural patterns section
    st.header("Security Architectural Patterns")
    
    tab1, tab2 = st.tabs(["Multi-Account Security", "Centralized Authentication"])
    
    with tab1:
        st.markdown("""
        ### Multi-Account Security Architecture
        
        A robust multi-account security strategy using AWS Organizations, IAM Identity Center, and RAM.
        
        **Key Components:**
        - AWS Organizations for account hierarchy
        - Service Control Policies for guardrails
        - IAM Identity Center for centralized access management
        - AWS RAM for secure resource sharing
        - Centralized logging and monitoring
        
        **Benefits:**
        - Separation of concerns
        - Defense in depth
        - Blast radius containment
        - Simplified compliance management
        - Centralized governance
        """)
        
        # Multi-account security diagram
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <img src="https://d1.awsstatic.com/AWS%20Prescriptive%20Guidance/Diagrams/multi-account-diagram-updated.300fb819d4a6d30e8c970c3af2c2e7b7a4134445.png" style="max-width: 80%; border-radius: 5px;">
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        ### Centralized Authentication Architecture
        
        Implementing centralized authentication for all AWS accounts and applications.
        
        **Key Components:**
        - IAM Identity Center as the central hub
        - Corporate directory integration (Active Directory)
        - Federated access to AWS accounts
        - Permission Sets for standard roles
        - Attribute-based access control
        
        **Benefits:**
        - Single sign-on experience
        - Consistent access policies
        - Reduced administrative burden
        - Improved security posture
        - Simplified user lifecycle management
        """)
        
        # Centralized authentication diagram
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <img src="https://d1.awsstatic.com/product-marketing/IAM/iam-identity-center-how-it-works.71dd14efd39003a48f841a4f82d8a17dce0a38bf.png" style="max-width: 80%; border-radius: 5px;">
        </div>
        """, unsafe_allow_html=True)

# Function for Data Analytics and ML page
def analytics_ml_page():
    st.title("Data Analytics & Machine Learning")
    
    # Analytics content
    st.header("AWS Data Analytics Services")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(aws_images["analytics"], width=300)
        except:
            st.warning("Analytics image could not be displayed")
    
    with col2:
        st.markdown("""
        AWS offers a comprehensive suite of data analytics services that help you analyze data of any volume, velocity, and variety. 
        These services enable you to build sophisticated data processing pipelines, perform interactive analysis, and derive insights 
        from your data at scale.
        
        **Key Data Analytics Categories:**
        - Data storage and management
        - Batch data processing
        - Real-time analytics
        - Data warehousing
        - Business intelligence
        - Search and log analytics
        """)
    
    st.subheader("Core AWS Analytics Services")
    
    # Create cards for the main analytics services
    analytics_services = [
        {
            "name": "Amazon Redshift",
            "icon": "🗄️",
            "description": "A fully managed, petabyte-scale data warehouse service for analyzing data using standard SQL.",
            "features": [
                "Columnar storage for analytical workloads",
                "Massively parallel processing (MPP) architecture",
                "SQL interface for querying",
                "Integration with data lakes via Redshift Spectrum",
                "Machine learning capabilities with Redshift ML"
            ],
            "use_cases": [
                "Enterprise data warehousing",
                "Business intelligence applications",
                "Analyzing large datasets with SQL",
                "Combining diverse datasets for analysis"
            ]
        },
        {
            "name": "Amazon Athena",
            "icon": "🔍",
            "description": "An interactive query service that makes it easy to analyze data in Amazon S3 using standard SQL.",
            "features": [
                "Serverless, no infrastructure to manage",
                "Pay-per-query pricing model",
                "Standard SQL support (based on Presto)",
                "Works directly with data in S3",
                "Support for various file formats (CSV, JSON, Parquet, ORC)"
            ],
            "use_cases": [
                "Ad-hoc data analysis",
                "Log and event data querying",
                "One-time data transformations",
                "Business reporting on S3 data"
            ]
        },
        {
            "name": "Amazon EMR",
            "icon": "🧮",
            "description": "A cloud big data platform for processing vast amounts of data using open-source tools.",
            "features": [
                "Managed Hadoop framework",
                "Support for multiple big data tools (Spark, Hive, HBase, etc.)",
                "Scalable compute resources",
                "Spot instance integration for cost savings",
                "Integration with AWS storage services"
            ],
            "use_cases": [
                "Big data processing",
                "Machine learning at scale",
                "Extract, transform, and load (ETL) operations",
                "Log analysis and genomics processing"
            ]
        },
        {
            "name": "Amazon OpenSearch Service",
            "icon": "🔎",
            "description": "A managed service for deploying, operating, and scaling OpenSearch clusters.",
            "features": [
                "Fully managed OpenSearch clusters",
                "Real-time analytics capabilities",
                "Full-text search engine",
                "Visualization with OpenSearch Dashboards",
                "Integration with popular log frameworks"
            ],
            "use_cases": [
                "Log and application monitoring",
                "Full-text search for applications",
                "Security information and event management",
                "Clickstream analytics"
            ]
        },
        {
            "name": "Amazon Kinesis",
            "icon": "📊",
            "description": "A platform for collecting, processing, and analyzing real-time streaming data.",
            "features": [
                "Real-time data streaming (Kinesis Data Streams)",
                "Load streaming data to destinations (Kinesis Data Firehose)",
                "Process streaming data with SQL or Apache Flink (Kinesis Data Analytics)",
                "Stream video for analysis and ML (Kinesis Video Streams)"
            ],
            "use_cases": [
                "Real-time analytics",
                "Log and event data collection",
                "IoT data processing",
                "Click-stream analysis"
            ]
        }
    ]
    
    # Display service cards in grid
    cols = st.columns(2)
    for i, service in enumerate(analytics_services):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="aws-card">
                <h3>{service['icon']} {service['name']}</h3>
                <p>{service['description']}</p>
                <h4>Key Features</h4>
                <ul>
            """ + "".join([f"<li>{feature}</li>" for feature in service["features"]]) + """
                </ul>
                <h4>Use Cases</h4>
                <ul>
            """ + "".join([f"<li>{use_case}</li>" for use_case in service["use_cases"]]) + """
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Machine Learning content
    st.header("AWS Machine Learning Services")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(aws_images["ml"], width=300)
        except:
            st.warning("ML image could not be displayed")
    
    with col2:
        st.markdown("""
        AWS offers a broad set of machine learning services and supporting infrastructure, putting machine learning in the hands of 
        every developer, data scientist, and researcher. From platforms for building custom models to pre-trained AI services for 
        ready-made intelligence, AWS provides options for all skill levels.
        
        **Levels of Machine Learning on AWS:**
        - AI services (pre-trained APIs)
        - ML services (managed platforms)
        - ML frameworks and infrastructure
        """)
    
    # Create a visual representation of ML service layers
    st.markdown("""
    <div style="display: flex; justify-content: center; margin: 30px 0;">
        <div style="text-align: center;">
            <img src="https://d1.awsstatic.com/re19/ML-layers-diagrams/ML-layers-v2.3c3612ecaebcefe3c307384444a80dd5e2e06e91.png" style="max-width: 80%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("AI Services (Pre-trained APIs)")
    
    # Create cards for the main ML services
    ai_services = [
        {
            "name": "Amazon Rekognition",
            "icon": "🖼️",
            "description": "Add image and video analysis to your applications with pre-trained computer vision capabilities.",
            "features": [
                "Object and scene detection",
                "Facial analysis and recognition",
                "Celebrity recognition",
                "Text detection in images",
                "Inappropriate content detection"
            ],
            "use_cases": [
                "Content moderation",
                "Facial verification",
                "Media asset management",
                "Public safety and security"
            ]
        },
        {
            "name": "Amazon Comprehend",
            "icon": "📝",
            "description": "Natural language processing service that finds relationships in text.",
            "features": [
                "Sentiment analysis",
                "Entity recognition",
                "Key phrase extraction",
                "Language detection",
                "Custom entity recognition"
            ],
            "use_cases": [
                "Customer feedback analysis",
                "Content classification",
                "Document processing",
                "Social media monitoring"
            ]
        },
        {
            "name": "Amazon Forecast",
            "icon": "📊",
            "description": "Time series forecasting service based on machine learning.",
            "features": [
                "Time series forecasting",
                "Built-in forecasting algorithms",
                "Automatic model selection",
                "What-if analysis",
                "Integration with business data"
            ],
            "use_cases": [
                "Demand planning",
                "Resource planning",
                "Financial planning",
                "Inventory management"
            ]
        },
        {
            "name": "Amazon Personalize",
            "icon": "👤",
            "description": "Real-time personalization and recommendation service.",
            "features": [
                "Real-time personalization",
                "Same technology as Amazon.com",
                "Similar items recommendations",
                "Personalized rankings",
                "Custom user segments"
            ],
            "use_cases": [
                "Product recommendations",
                "Content personalization",
                "Targeted marketing",
                "Personalized search results"
            ]
        }
    ]
    
    # Display service cards in grid
    cols = st.columns(2)
    for i, service in enumerate(ai_services):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="aws-card">
                <h3>{service['icon']} {service['name']}</h3>
                <p>{service['description']}</p>
                <h4>Key Features</h4>
                <ul>
            """ + "".join([f"<li>{feature}</li>" for feature in service["features"]]) + """
                </ul>
                <h4>Use Cases</h4>
                <ul>
            """ + "".join([f"<li>{use_case}</li>" for use_case in service["use_cases"]]) + """
                </ul>
            </div>
            """, unsafe_allow_html=True)

# Function for Knowledge Checks page
def knowledge_checks_page():
    st.title("Knowledge Checks")
    
    st.markdown("""
    <div class="aws-info-card">
        <h3>Test your knowledge of AWS services</h3>
        <p>Answer the scenario-based questions below to check your understanding. Your progress is tracked at the bottom of this page.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display quiz section tabs
    tab_names = [
        "SQS", "SNS", "EventBridge", "Lambda", 
        "API Gateway", "Containers", "Security", "Analytics & ML"
    ]
    
    tabs = st.tabs(tab_names)
    
    # SQS Quiz
    with tabs[0]:
        st.header("Amazon SQS Knowledge Check")
        for i, quiz in enumerate(quiz_data["sqs"]):
            handle_quiz("sqs", i, quiz)
    
    # SNS Quiz
    with tabs[1]:
        st.header("Amazon SNS Knowledge Check")
        for i, quiz in enumerate(quiz_data["sns"]):
            handle_quiz("sns", i, quiz)
    
    # EventBridge Quiz
    with tabs[2]:
        st.header("Amazon EventBridge Knowledge Check")
        for i, quiz in enumerate(quiz_data["eventbridge"]):
            handle_quiz("eventbridge", i, quiz)
    
    # Lambda Quiz
    with tabs[3]:
        st.header("AWS Lambda Knowledge Check")
        for i, quiz in enumerate(quiz_data["lambda"]):
            handle_quiz("lambda", i, quiz)
    
    # API Gateway Quiz
    with tabs[4]:
        st.header("Amazon API Gateway Knowledge Check")
        for i, quiz in enumerate(quiz_data["api_gateway"]):
            handle_quiz("api_gateway", i, quiz)
    
    # Containers Quiz
    with tabs[5]:
        st.header("Containers on AWS Knowledge Check")
        for i, quiz in enumerate(quiz_data["containers"]):
            handle_quiz("containers", i, quiz)
    
    # Security Quiz
    with tabs[6]:
        st.header("AWS Security Services Knowledge Check")
        for i, quiz in enumerate(quiz_data["aws_security"]):
            handle_quiz("aws_security", i, quiz)
    
    # Analytics & ML Quiz
    with tabs[7]:
        st.header("Data Analytics & Machine Learning Knowledge Check")
        
        st.subheader("Data Analytics")
        for i, quiz in enumerate(quiz_data["data_analytics"]):
            handle_quiz("data_analytics", i, quiz)
        
        st.subheader("Machine Learning")
        for i, quiz in enumerate(quiz_data["ml"]):
            handle_quiz("ml", i, quiz)
    
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
    st.title("AWS Solutions Architect - Associate")
    st.header("Content Review - Session 5")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(aws_images["home"], width=300)
        except:
            st.error("Unable to load image")
    
    with col2:
        st.markdown("""
        Welcome to the AWS Partner Certification Readiness program. This interactive guide will help you prepare 
        for the Solutions Architect - Associate certification. Navigate through the topics using the tabs above.
        
        Each section contains key concepts, important takeaways, and interactive quizzes to reinforce your learning.
        """)
    
    st.markdown("""
    <div class="aws-info-card">
        <h3>Topics covered in Week 5</h3>
        <p>
            • Decoupling and Messaging (SQS, SNS, EventBridge)<br>
            • AWS Lambda and Serverless Applications<br>
            • API Gateway<br>
            • Containers on AWS (ECS, EKS, Fargate)<br>
            • Additional AWS Security Services<br>
            • Data Analytics and Machine Learning
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display certification tips
    st.markdown("""
    <div class="aws-card">
        <h3>📝 Certification Preparation Tips</h3>
        <p>Practice hands-on with the services covered in this guide. The AWS Solutions Architect - Associate exam 
        focuses on practical knowledge of AWS services and how they can be used together to design resilient, 
        cost-effective solutions.</p>
        <ul>
            <li>Focus on understanding when to use each service</li>
            <li>Practice identifying the most cost-effective solution</li>
            <li>Learn about service integrations and limitations</li>
            <li>Review AWS Well-Architected Framework principles</li>
            <li>Take practice exams to familiarize yourself with the question format</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Services overview section
    st.header("Services Overview")
    
    # Create a grid of service cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔄 Decoupling & Messaging</h4>
            <ul>
                <li><strong>Amazon SQS:</strong> Managed message queuing for application decoupling</li>
                <li><strong>Amazon SNS:</strong> Pub/sub messaging for A2A and A2P communication</li>
                <li><strong>Amazon EventBridge:</strong> Serverless event bus for event-driven architectures</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="aws-feature-card">
            <h4>💻 Serverless Computing</h4>
            <ul>
                <li><strong>AWS Lambda:</strong> Run code without provisioning servers</li>
                <li><strong>Amazon API Gateway:</strong> Create, publish, and manage APIs at any scale</li>
                <li><strong>AWS Step Functions:</strong> Coordinate multiple AWS services into workflows</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🐳 Containers</h4>
            <ul>
                <li><strong>Amazon ECS:</strong> AWS-native container orchestration service</li>
                <li><strong>Amazon EKS:</strong> Managed Kubernetes service on AWS</li>
                <li><strong>AWS Fargate:</strong> Serverless compute engine for containers</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔐 Security & Analytics</h4>
            <ul>
                <li><strong>AWS Secrets Manager:</strong> Securely store and manage credentials</li>
                <li><strong>AWS IAM Identity Center:</strong> Centralized access management</li>
                <li><strong>Amazon Athena:</strong> Serverless interactive query service</li>
                <li><strong>Amazon SageMaker:</strong> Build, train, and deploy ML models</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Sidebar for navigation and session management
# st.sidebar.title("AWS Solutions Architect")
# st.sidebar.image("https://a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_1200x630.png", width=200)

# Session management section in sidebar
st.sidebar.subheader("⚙️ Session Management")

# Reset button for session data
if st.sidebar.button("🔄 Reset Progress", key="reset_button"):
    reset_session()

# Show session ID
st.sidebar.caption(f"Session ID: {st.session_state.session_id[:8]}...")

st.sidebar.divider()

# Main content tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "🏠 Home", 
    "🔄 SQS", 
    "📢 SNS", 
    "📅 EventBridge", 
    "λ Lambda", 
    "🌐 API Gateway", 
    "🐳 Containers",
    "🔐 Security",
    "📊 Analytics & ML",
    "🧪 Knowledge Checks"
])

with tab1:
    home_page()

with tab2:
    sqs_page()

with tab3:
    sns_page()

with tab4:
    eventbridge_page()

with tab5:
    lambda_page()

with tab6:
    api_gateway_page()

with tab7:
    containers_page()

with tab9:
    analytics_ml_page()
    
with tab8:
    security_services_page()

with tab10:
    knowledge_checks_page()

# Footer
st.markdown("""
<div class="footer">
    © 2025, Amazon Web Services, Inc. or its affiliates. All rights reserved.
</div>
""", unsafe_allow_html=True)
