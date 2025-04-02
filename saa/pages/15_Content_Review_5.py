
import streamlit as st
import base64
from PIL import Image
import requests
from io import BytesIO
import json
import random
import time

# Set page configuration
st.set_page_config(
    page_title="AWS Solutions Architect - Associate",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Function to load and cache images from URL
@st.cache_data
def load_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

# Define AWS stock images URLs
aws_images = {
    "home": "https://d1.awsstatic.com/training-and-certification/certification-badges/AWS-Certified-Solutions-Architect-Associate_badge.3419559c682629072f1eb968d59dea0741772c0f.png",
    "sqs": "https://d1.awsstatic.com/Products/product-name/diagrams/product-page-diagram_Amazon-SQS@2x.d79ebf1742ab78d2546045034c2deb402ddd31c4.png",
    "sns": "https://d1.awsstatic.com/product-marketing/SNS/product-page-diagram_Amazon-SNS_event-driven-SNS-compute%402x.07f1509816f60c8a98b1a7741e7fb5e0e7f970ea.png",
    "eventbridge": "https://d1.awsstatic.com/products/eventbridge/Product-Page-Diagram_Amazon-EventBridge%402x.24c0d8bd637766ba43d3364058d7a367919fc69e.png",
    "lambda": "https://d1.awsstatic.com/product-marketing/Lambda/Diagrams/product-page-diagram_Lambda-RealTimeFileProcessing.a59577de4b6471674a540b878b0b684e0249a18c.png",
    "api_gateway": "https://d1.awsstatic.com/serverless/New-API-GW-Diagram.c9fc9835d2a9aa00ef90d0dbb4df1e73fbb282e4.png",
    "containers": "https://d1.awsstatic.com/legal/AmazonElasticContainerServiceAgreement/Product-Page-Diagram_Amazon-ECS%402x.0d872eb6fb782ddc733a27d2ab5694e9b8ca095c.png",
    "ecs": "https://d1.awsstatic.com/product-marketing/ECS/ECS_Diagrams/ecs-fargate%402x.b8486599d2e50e5fcdc3326e42a4ba90e7c3f881.png",
    "eks": "https://d1.awsstatic.com/products/eks/Product-Page-Diagram_Amazon-EKS%402x.ccad94521511d0aa2a9c5cc7d147513ff8fb061e.png",
    "fargate": "https://d1.awsstatic.com/products/fargate/Product-Page-Diagram_Fargate.b7f73bbac9cc630a1c8c5a5668b282ab2a6b213a.png",
    "secrets_manager": "https://d1.awsstatic.com/diagrams/Secrets-Manager-HIW%402x.5d58b84637657bd3b720f265f5d1449f2ee56b31.png",
    "acm": "https://d1.awsstatic.com/products/ACM/product-page-diagram_certificate-manager_how-it-works%402x.457eaeac8fd3cf1b3db9c05904c937eb3b0dbc45.png",
    "patch_manager": "https://d1.awsstatic.com/products/systems-manager/Product-Page-Diagram_AWS-Systems-Manager_Patch-Manager_How-it-Works%402x.283c13eb185a92186361a9b21d8b46fa06ec77ab.png",
    "iam_identity_center": "https://d1.awsstatic.com/products/IAM/product-page-diagram-IAM-Identity-Center_How-it-Works.510a dec96b47cb6112661c0d2160ea6e2695b8ea.png",
    "directory_service": "https://d1.awsstatic.com/Products/product-name/diagrams/product-page-diagram_AWS-Directory-Service_how-it-works.11f6b76d3110b1c3a25422a0ea944ee1deed8b41.png",
    "ram": "https://d1.awsstatic.com/products/RAM/product-page-diagram-AWS-Resource-Access-Manager.1fcece1397fa7e53a5a5e59e9192dd4731473c55.png",
    "cognito": "https://d1.awsstatic.com/products/cognito/product-page-diagram-Amazon-Cognito-Authenticating-Users%402x.2f82c7afc4fd5e777d4426e7629909ef4b31dad9.png",
    "analytics": "https://d1.awsstatic.com/aws-monitoring-intelligentdiagnostics.3a18f07e68c4ea3786585ea712a279e929ca242c.png",
    "ml": "https://d1.awsstatic.com/AI-Brain-for-AI-ML%402x.9d5d606ffba0170c124d9cef9866d13934985299.png"
}

# Function to create nice card components
def create_card(title, content, key=None):
    with st.container():
        st.markdown(f"""
        <div style="
            padding: 20px;
            border-radius: 10px;
            background-color: #f5f5f5;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
            <h3>{title}</h3>
            <p>{content}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if key:
            st.button("Learn More", key=key)

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

# Function to display quiz
def display_quiz(topic):
    if topic in quiz_data and quiz_data[topic]:
        st.subheader("💡 Scenario-Based Knowledge Check")
        
        # Initialize session state for quiz results if not exists
        if f"{topic}_score" not in st.session_state:
            st.session_state[f"{topic}_score"] = 0
            st.session_state[f"{topic}_attempted"] = 0
            st.session_state[f"{topic}_answers"] = {}
        
        # Display each quiz question
        for i, quiz in enumerate(quiz_data[topic]):
            question = quiz["question"]
            options = quiz["options"]
            correct_answer = quiz["answer"]
            
            st.write(f"**Scenario {i+1}:** {question}")
            
            # Create a unique key for each radio button
            key = f"{topic}_quiz_{i}"
            answer_key = f"{topic}_answer_{i}"
            
            # Display radio buttons for quiz options
            selected_answer = st.radio(
                "Select your answer:",
                options,
                key=key,
                index=None
            )
            
            # Check button
            check_key = f"check_{topic}_{i}"
            
            if st.button("Check Answer", key=check_key):
                if selected_answer is None:
                    st.warning("Please select an answer first.")
                else:
                    st.session_state[f"{topic}_attempted"] += 1
                    if selected_answer == correct_answer:
                        st.success(f"✅ Correct! {correct_answer} is the right answer.")
                        if answer_key not in st.session_state[f"{topic}_answers"] or not st.session_state[f"{topic}_answers"][answer_key]:
                            st.session_state[f"{topic}_score"] += 1
                            st.session_state[f"{topic}_answers"][answer_key] = True
                    else:
                        st.error(f"❌ Incorrect. The correct answer is: {correct_answer}")
                        st.session_state[f"{topic}_answers"][answer_key] = False
            
            st.divider()
        
        # Display score if any questions have been attempted
        if st.session_state[f"{topic}_attempted"] > 0:
            st.info(f"Your score: {st.session_state[f'{topic}_score']} out of {st.session_state[f'{topic}_attempted']} questions attempted")

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
        st.header("Content Review - Session 5")
        st.markdown("""
        Welcome to the AWS Partner Certification Readiness program. This interactive guide will help you prepare 
        for the Solutions Architect - Associate certification. Navigate through the topics using the sidebar menu.
        
        Each section contains key concepts, important takeaways, and interactive quizzes to reinforce your learning.
        
        **Topics covered in Week 5:**
        - Decoupling and Messaging (SQS, SNS, EventBridge)
        - AWS Lambda and Serverless Applications
        - Containers on AWS (ECS, EKS, Fargate)
        - Additional AWS Security Services
        - Data Analytics and Machine Learning
        """)
    
    st.info("""
    **Certification Preparation Tip:** Practice hands-on with the services covered in this guide. 
    The AWS Solutions Architect - Associate exam focuses on practical knowledge of AWS services 
    and how they can be used together to design resilient, cost-effective solutions.
    """)

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
    
    **Key Features:**
    - Unlimited throughput and elastic capacity
    - At-least-once message delivery
    - Multiple message copies for redundancy
    - Message retention (configurable up to 14 days)
    - Send and receive batching for greater efficiency
    - Dead-letter queues for handling failed processing
    - Encryption at rest and in transit
    """)
    
    st.header("SQS Queue Types")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Standard Queues")
        st.markdown("""
        **Features:**
        - Unlimited throughput (nearly unlimited TPS)
        - At-least-once delivery (may deliver duplicates)
        - Best-effort ordering (messages may arrive out of order)
        
        **Best For:**
        - Maximum throughput applications
        - When message ordering is not critical
        - When applications can handle duplicate messages
        
        **Use Cases:**
        - Background jobs processing
        - Decoupling microservices
        - Work distribution among multiple workers
        - Buffering requests during traffic spikes
        """)
    
    with col2:
        st.subheader("FIFO Queues")
        st.markdown("""
        **Features:**
        - First-In-First-Out delivery guarantee
        - Exactly-once processing (no duplicates)
        - Limited throughput (300 TPS by default, up to 3000 TPS with high throughput mode)
        - Message group support for parallel processing
        
        **Best For:**
        - Applications requiring strict ordering
        - When duplicate processing can't be tolerated
        - When transaction processing requires accuracy
        
        **Use Cases:**
        - Financial transactions processing
        - Order processing systems
        - Sequential command execution
        - Inventory updates
        """)
    
    st.header("SQS Message Lifecycle")
    st.markdown("""
    1. **Send Message:** Producer sends a message to the queue
    2. **Storage:** SQS redundantly stores the message across multiple servers
    3. **Receive Message:** Consumer polls the queue and receives the message
    4. **Processing:** Consumer processes the message while it remains in the queue but is hidden (visibility timeout)
    5. **Deletion:** After successful processing, consumer explicitly deletes the message from the queue
    6. **Timeout Expiration:** If not deleted within the visibility timeout period, message becomes visible again for other consumers
    """)
    
    st.subheader("Visibility Timeout")
    st.markdown("""
    - Default: 30 seconds
    - Range: 0 seconds to 12 hours
    - Purpose: Prevents other consumers from processing the message while it's being handled
    - Extension: Can be extended if processing takes longer than expected
    - Best Practice: Set to maximum expected processing time
    """)
    
    st.header("SQS Best Practices")
    st.markdown("""
    **Performance Optimization:**
    
    1. **Use Long Polling:** Reduces empty responses when no messages are available and lowers costs
       - Set ReceiveMessageWaitTimeSeconds to a value between 1-20 seconds
    
    2. **Batch Operations:** Use SendMessageBatch and DeleteMessageBatch to reduce API calls
    
    3. **Right-size Visibility Timeout:** Set appropriate timeout based on processing time
    
    **Cost Optimization:**
    
    1. **Delete Messages Promptly:** After processing to avoid unnecessary storage
    
    2. **Use Message Attributes Efficiently:** Structure data to minimize message size
    
    3. **Implement Queue Depth Monitoring:** Scale consumers based on queue depth
    
    **Reliability:**
    
    1. **Implement Dead-Letter Queues (DLQ):** Capture messages that fail processing
    
    2. **Apply Idempotent Processing:** Handle potential duplicate messages
    
    3. **Use Separate Queues:** For different processing priorities or characteristics
    """)
    
    display_quiz("sqs")

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
    
    **Key Features:**
    - Publish/subscribe messaging pattern
    - Support for multiple protocols and delivery methods
    - Message filtering with subscription filter policies
    - Message archiving and analytics integration
    - Message durability with redundant storage
    - Message encryption for sensitive data
    - Cross-region delivery
    """)
    
    st.header("SNS Concepts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Topics and Subscriptions")
        st.markdown("""
        **Topics:**
        - Communication channels for sending messages
        - Identified by Amazon Resource Name (ARN)
        - Can have multiple subscribers
        - Support two types:
          - Standard (high throughput, best-effort ordering)
          - FIFO (strict ordering, exactly-once delivery)
        
        **Subscriptions:**
        - Endpoints that receive messages published to a topic
        - Multiple subscription types:
          - Amazon SQS
          - AWS Lambda
          - HTTP/HTTPS
          - Email/Email-JSON
          - Mobile Push Notifications
          - SMS text messages
        """)
    
    with col2:
        st.subheader("Message Filtering")
        st.markdown("""
        **Filter Policies:**
        - JSON policies that specify which messages to deliver
        - Based on message attributes
        - Help reduce unwanted traffic and costs
        
        **Example Filter Policy:**
        ```json
        {
          "customer_interests": ["sports", "travel"],
          "price_usd": [{"numeric": [">=", 100]}]
        }
        ```
        
        **Benefits:**
        - More efficient processing
        - Reduced downstream costs
        - Simplified application logic
        - Decreased bandwidth usage
        """)
    
    st.header("SNS Use Cases")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Application-to-Application (A2A)")
        st.markdown("""
        **Fanout Pattern:**
        - Publish a message once, deliver to multiple endpoints
        - Parallel asynchronous processing
        - Example: Order processing system sending notifications to inventory, shipping, and billing systems
        
        **Event-Driven Architecture:**
        - React to events across distributed systems
        - Trigger AWS Lambda functions based on events
        - Enable microservices communication
        
        **Integration:**
        - Connect with over 60 AWS services natively
        - Capture events from multiple sources
        - Distribute to various destinations
        """)
    
    with col2:
        st.subheader("Application-to-Person (A2P)")
        st.markdown("""
        **User Notifications:**
        - Send notifications directly to users
        - Support multiple delivery channels
        
        **Mobile Push:**
        - Send notifications to mobile apps
        - Support for Apple, Google, Amazon, Microsoft platforms
        - Rich message content
        
        **SMS:**
        - Text message delivery to over 200 countries
        - Support for transactional and promotional messages
        - Sender IDs and short codes in supported regions
        
        **Email:**
        - Send formatted messages or JSON payloads
        - Raw email delivery for customization
        """)
    
    st.header("SNS vs SQS Comparison")
    st.markdown("""
    | Feature | Amazon SNS | Amazon SQS |
    |---------|------------|------------|
    | **Model** | Pub/Sub (push) | Queue (poll) |
    | **Message Delivery** | Push to multiple subscribers | Pulled by a single consumer |
    | **Use Case** | Fanout to multiple endpoints | Decoupling and buffering |
    | **Message Persistence** | Non-persistent unless using SQS subscription | Persistent (up to 14 days) |
    | **Delivery Attempt** | Up to 100,015 retries depending on protocol | Persists until deletion or expiration |
    | **Consumers** | Multiple subscribers | Single consumer (unless using FIFO with group IDs) |
    | **Common Pattern** | SNS + SQS: Fanout messages to multiple SQS queues for parallel processing |
    """)
    
    st.header("SNS Best Practices")
    st.markdown("""
    **Reliability:**
    
    1. **Implement DLQ:** Configure dead-letter queues for failed message deliveries
    
    2. **Monitor Delivery Status:** Use delivery status logging for tracking
    
    3. **Use Message Archiving:** For compliance and debugging
    
    **Security:**
    
    1. **Encrypt Sensitive Data:** Enable server-side encryption with KMS
    
    2. **Implement Access Policies:** Use IAM policies and topic policies
    
    3. **Use Private Endpoints:** Consider VPC endpoints for internal communications
    
    **Performance:**
    
    1. **Use Message Filtering:** Reduce unnecessary message delivery
    
    2. **Implement Message Batching:** For higher throughput
    
    3. **Consider FIFO Topics:** When ordering and deduplication are required
    
    4. **Monitor Performance:** Set up CloudWatch alarms for delivery metrics
    """)
    
    display_quiz("sns")

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
    
    **Key Features:**
    - Serverless event routing at scale
    - Advanced event filtering and transformation
    - Multiple event buses with isolation
    - Schema registry and discovery
    - Direct integration with 200+ AWS services
    - Partner event sources from SaaS providers
    - Event archive and replay capabilities
    """)
    
    st.header("EventBridge Core Concepts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Events and Event Buses")
        st.markdown("""
        **Events:**
        - JSON objects that represent state changes
        - Contains metadata and detail fields
        - Example:
        ```json
        {
          "version": "0",
          "id": "12345678-1234-1234-1234-123456789012",
          "detail-type": "EC2 Instance State Change",
          "source": "aws.ec2",
          "account": "123456789012",
          "time": "2019-11-29T13:45:00Z",
          "region": "us-east-1",
          "resources": ["arn:aws:ec2:us-east-1:123456789012:instance/i-0123456789abcdef"],
          "detail": {
            "instance-id": "i-0123456789abcdef",
            "state": "running"
          }
        }
        ```
        
        **Event Buses:**
        - Routers that receive events and deliver to targets
        - Types:
          - Default event bus (AWS services)
          - Custom event buses (your applications)
          - Partner event buses (third-party SaaS)
        """)
    
    with col2:
        st.subheader("Rules and Targets")
        st.markdown("""
        **Rules:**
        - Event patterns that specify when to route events
        - Match on event fields like source, detail-type, or detail
        - Can also run on a schedule (like CloudWatch Events)
        - Example Pattern:
        ```json
        {
          "source": ["aws.ec2"],
          "detail-type": ["EC2 Instance State Change"],
          "detail": {
            "state": ["running", "stopped"]
          }
        }
        ```
        
        **Targets:**
        - Services that receive matching events
        - Up to 5 targets per rule
        - Types include:
          - AWS Lambda functions
          - AWS Step Functions state machines
          - Amazon SQS queues
          - Amazon SNS topics
          - Amazon Kinesis streams
          - API destinations (HTTP endpoints)
          - Other event buses
        """)
        

    st.header("EventBridge Specialized Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("EventBridge Pipes")
        st.markdown("""
        **Point-to-Point Integration:**
        - Direct connection between source and target
        - Built-in filtering, enrichment, and transformation
        - Support for synchronous target invocation
        
        **Sources include:**
        - DynamoDB streams
        - Kinesis streams
        - Amazon MQ
        - Amazon MSK
        - SQS queues
        
        **Benefits:**
        - Simplified architecture
        - Reduced custom code
        - Enhanced error handling
        """)
    
    with col2:
        st.subheader("EventBridge Scheduler")
        st.markdown("""
        **Fully Managed Scheduler:**
        - Create, run, and manage scheduled tasks
        - Supports one-time and recurring schedules
        - Scales to millions of schedules
        
        **Features:**
        - Cron and rate expressions
        - Timezone support
        - Flexible retry policies
        - Dead-letter queues for failed invocations
        
        **Use Cases:**
        - Database maintenance
        - Report generation
        - Periodic data processing
        - Automated resource management
        """)
    
    st.header("EventBridge vs. SNS vs. SQS")
    st.markdown("""
    | Feature | Amazon EventBridge | Amazon SNS | Amazon SQS |
    |---------|-------------------|------------|------------|
    | **Primary Purpose** | Event routing and integration | Publishing to multiple subscribers | Message queuing and decoupling |
    | **Delivery Model** | Event-driven, rule-based routing | Push-based pub/sub | Pull-based queue |
    | **Filtering** | Advanced pattern matching and transformation | Subscription filter policies | No built-in filtering |
    | **Integration** | 200+ AWS services, SaaS providers | AWS services, HTTP/S, email, mobile, SMS | AWS services |
    | **Event Replay** | Archive and replay supported | No replay capability | Messages persist until consumed |
    | **Schema Registry** | Built-in schema discovery and registry | No schema registry | No schema registry |
    | **Best For** | Complex event routing, SaaS integration | Simple pub/sub messaging, notifications | Workload decoupling, buffering |
    """)
    
    st.header("EventBridge Best Practices")
    st.markdown("""
    **Design Considerations:**
    
    1. **Use Multiple Event Buses:** Separate buses for different domains or environments
    
    2. **Design for Idempotency:** Handle potential duplicate events
    
    3. **Implement Dead-letter Queues:** For events that fail processing
    
    4. **Consider Event Archive:** Enable for important events to support replay
    
    **Performance and Cost Optimization:**
    
    1. **Create Specific Rules:** More specific patterns reduce unnecessary processing
    
    2. **Use Content Filtering:** Filter events before they reach targets
    
    3. **Monitor Usage Metrics:** Track invocation counts and failures
    
    4. **Consider Batching:** Use EventBridge Pipes for batch processing where appropriate
    
    **Security:**
    
    1. **Use Resource-Based Policies:** Control which principals can send events
    
    2. **Encrypt Sensitive Data:** Use KMS for event data encryption
    
    3. **Monitor API Calls:** Enable CloudTrail for EventBridge API activity
    
    4. **Implement Least Privilege:** Grant minimal permissions to event targets
    """)
    
    display_quiz("eventbridge")

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
    
    **Key Features:**
    - Serverless execution environment
    - Automatic scaling
    - Pay-per-use pricing model
    - Native integration with AWS services
    - Supports multiple programming languages
    - Built-in fault tolerance and availability
    - Stateless function execution
    """)
    
    st.header("Lambda Execution Models")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Synchronous Invocation")
        st.markdown("""
        **Characteristics:**
        - Wait for function to complete
        - Returns response directly to caller
        - Error handling by caller
        
        **Common Triggers:**
        - API Gateway
        - Application Load Balancer
        - Amazon Cognito
        - AWS SDK direct invocation
        - CloudFront (Lambda@Edge)
        
        **Use Cases:**
        - API backends
        - User authentication
        - Real-time processing
        """)
    
    with col2:
        st.subheader("Asynchronous Invocation")
        st.markdown("""
        **Characteristics:**
        - Events queued for processing
        - No immediate response
        - Automatic retries (2 attempts)
        - Dead-letter queue support
        
        **Common Triggers:**
        - S3 bucket events
        - SNS notifications
        - EventBridge events
        - CloudWatch Events
        - CodeCommit triggers
        
        **Use Cases:**
        - File processing
        - Notifications handling
        - Order processing
        - Data processing pipelines
        """)
    
    with col3:
        st.subheader("Stream-Based Invocation")
        st.markdown("""
        **Characteristics:**
        - Poll-based processing
        - Batch record processing
        - Lambda manages polling
        - Checkpointing for failures
        
        **Common Triggers:**
        - Kinesis Data Streams
        - DynamoDB Streams
        - SQS queues
        - Amazon MSK
        
        **Use Cases:**
        - Real-time analytics
        - Log processing
        - Click stream analysis
        - IoT data processing
        """)
    
    st.header("Lambda Configuration Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Memory and Performance")
        st.markdown("""
        **Memory Allocation:**
        - Range: 128MB to 10,240MB (10GB)
        - CPU scales proportionally to memory
        - More memory = more CPU = faster execution
        
        **Execution Time:**
        - Maximum timeout: 15 minutes
        - Default timeout: 3 seconds
        - Best practice: Set timeout to expected duration
        
        **Concurrency:**
        - Default: 1,000 concurrent executions per region
        - Reserved concurrency: Guarantee function capacity
        - Provisioned concurrency: Pre-warm execution environments
        """)
    
    with col2:
        st.subheader("Deployment and Packaging")
        st.markdown("""
        **Deployment Options:**
        - .zip file archive (up to 50 MB compressed)
        - Container image (up to 10 GB)
        
        **Lambda Layers:**
        - Shareable code components
        - Separate dependencies from function code
        - Promotes code reuse and smaller deployments
        
        **Versions and Aliases:**
        - Versions: Immutable snapshots of your function
        - Aliases: Pointers to specific versions
        - Enable blue/green deployments and traffic shifting
        """)
    
    st.header("Lambda Integration Patterns")
    st.markdown("""
    **Common Architectures:**
    
    1. **API Backend:**
       - API Gateway → Lambda → Database
       - Serverless REST or GraphQL APIs
    
    2. **Event Processing:**
       - Event Source → Lambda → Storage/Database
       - Process events from S3, DynamoDB, Kinesis, etc.
    
    3. **Fan-out Pattern:**
       - Event → SNS → Multiple Lambda functions
       - Parallel processing of events
    
    4. **Queue-based Processing:**
       - SQS → Lambda → Process batch of messages
       - Decoupled, scalable processing
    
    5. **Orchestration:**
       - Step Functions → Coordinate multiple Lambda functions
       - Complex workflows with state management
    
    6. **Real-time Processing:**
       - Kinesis → Lambda → Analyze/Transform data streams
       - Stream processing at scale
    """)
    
    st.header("Lambda Best Practices")
    st.markdown("""
    **Performance Optimization:**
    
    1. **Optimize Cold Starts:**
       - Use Provisioned Concurrency for latency-sensitive applications
       - Keep functions small and focused
       - Minimize dependencies
       - Consider container images for larger dependencies
    
    2. **Memory Allocation:**
       - Test with different memory settings
       - Often higher memory = better cost/performance
    
    3. **Execution Environment Reuse:**
       - Initialize SDK clients outside handler
       - Cache static assets in /tmp (up to 512MB)
       - Reuse connections and expensive initializations
    
    **Cost Optimization:**
    
    1. **Right-size Memory:** Find optimal memory/performance balance
    
    2. **Optimize Function Duration:**
       - Reduce unnecessary processing
       - Consider chunking large operations
    
    3. **Use Event Filtering:** Process only relevant events
    
    **Monitoring and Troubleshooting:**
    
    1. **Implement Structured Logging:** Use JSON format for easier parsing
    
    2. **Configure CloudWatch Alarms:** Monitor errors, duration, concurrency
    
    3. **Enable X-Ray Tracing:** For distributed tracing and bottleneck identification
    
    4. **Implement Custom Metrics:** Track business-specific metrics
    """)
    
    display_quiz("lambda")

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
    
    **Key Features:**
    - RESTful APIs and WebSocket APIs
    - Scalable and cost-effective
    - Performance optimization with caching
    - Request/response transformations
    - Monitoring and metrics
    - API Keys and usage plans
    - Integration with AWS and HTTP backends
    - Security features for authentication and authorization
    """)
    
    st.header("API Gateway Types")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("REST API")
        st.markdown("""
        **Characteristics:**
        - Traditional RESTful API design
        - Full feature set
        - Complex request/response transformations
        - API keys and usage plans
        - Request validation
        
        **Integration Types:**
        - Lambda functions
        - HTTP endpoints
        - AWS services
        - Mock integrations
        
        **Use Cases:**
        - Complex APIs requiring full features
        - Public-facing APIs with monetization
        - APIs requiring detailed control
        """)
    
    with col2:
        st.subheader("HTTP API")
        st.markdown("""
        **Characteristics:**
        - Simplified, low-latency RESTful API
        - Up to 60% cost reduction vs. REST API
        - Faster deployment and response times
        - Limited feature set
        - CORS support built-in
        
        **Integration Types:**
        - Lambda functions
        - HTTP endpoints
        - Private integrations via ALB/NLB
        
        **Use Cases:**
        - Serverless workloads
        - Simple proxy APIs
        - High-volume APIs prioritizing performance
        - APIs with basic security requirements
        """)
    
    with col3:
        st.subheader("WebSocket API")
        st.markdown("""
        **Characteristics:**
        - Persistent two-way communication
        - Maintains connection state
        - Route messages based on content
        - Full-duplex communication
        
        **Integration Types:**
        - Lambda functions
        - HTTP endpoints
        - AWS services
        
        **Use Cases:**
        - Real-time applications
        - Chat applications
        - Live dashboards
        - Collaborative platforms
        - Gaming applications
        - Financial trading platforms
        """)
    
    st.header("API Gateway Integration Types")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Lambda Integration")
        st.markdown("""
        **Types of Integration:**
        - **Lambda Proxy Integration:**
          - Passes entire request to Lambda
          - Lambda returns the entire response
          - Simplest integration model
          
        - **Lambda Custom Integration:**
          - Define request/response mapping templates
          - Transform data between API Gateway and Lambda
          - More control over request/response
        
        **Best Practices:**
        - Use proxy integration for simpler applications
        - Custom integration for complex transformations
        - Set appropriate timeouts
        - Handle errors properly in Lambda code
        """)
    
    with col2:
        st.subheader("HTTP Integration")
        st.markdown("""
        **Types of Integration:**
        - **HTTP Proxy Integration:**
          - Passes request to HTTP endpoint
          - Returns endpoint response directly
          - Minimal configuration
          
        - **HTTP Custom Integration:**
          - Transform requests before sending to backend
          - Transform responses before returning to client
          - Apply content type conversions
        
        **Best Practices:**
        - Use for integrating with existing HTTP APIs
        - Set up appropriate timeouts
        - Consider caching for frequently accessed resources
        - Monitor backend health with CloudWatch
        """)
    
    st.header("Security Features")
    st.markdown("""
    **Authentication and Authorization Options:**
    
    1. **IAM Authorization:**
       - Use AWS Signature Version 4 (SigV4) signing
       - Authenticate using IAM roles and policies
       - Best for internal or AWS service clients
    
    2. **Lambda Authorizers:**
       - Custom authorization logic in Lambda functions
       - Token-based or request parameter-based auth
       - Can implement any authorization scheme
       - Returns IAM policy document dynamically
    
    3. **Cognito User Pools:**
       - User management and authentication service
       - Handles registration, login, token validation
       - OAuth 2.0 and OpenID Connect support
       - Social identity provider integration
    
    4. **API Keys and Usage Plans:**
       - Control access based on API keys
       - Set throttling and quota limits
       - Monitor usage per client
       - Not recommended as primary authentication method
    
    5. **Resource Policies:**
       - Control access using JSON policies
       - Specify source IP addresses or VPC endpoints
       - Control which AWS accounts can access the API
    
    6. **Mutual TLS (mTLS):**
       - Client and server authenticate each other
       - Clients present certificates for authentication
       - For high-security applications
    """)
    
    st.header("Performance and Optimization")
    st.markdown("""
    **Caching:**
    - Enable API caching to improve performance
    - Cache TTL configurable (0-3600 seconds)
    - Cache capacity between 0.5GB to 237GB
    - Can flush cache as needed
    - Cache encryption option available
    
    **Throttling:**
    - Account-level throttling (default: 10,000 RPS)
    - Method-level throttling with usage plans
    - Stage-level throttling for different environments
    - Burst limits for handling traffic spikes
    
    **Deployment Options:**
    - **Edge-optimized:** Cached at CloudFront edge locations (default)
    - **Regional:** For clients in the same region
    - **Private:** Accessible only from your VPC using VPC endpoint
    
    **Monitoring:**
    - CloudWatch metrics for API calls, latency, errors
    - Access logs for detailed request information
    - X-Ray integration for distributed tracing
    - CloudWatch dashboard visualization
    """)
    
    display_quiz("api_gateway")

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
    
    **Key Benefits of Containers:**
    - Consistent environments from development to production
    - Lightweight and efficient resource utilization
    - Faster startup times compared to virtual machines
    - Isolation between applications
    - Improved developer productivity and deployment velocity
    - Scalability and high availability
    """)
    
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
            
            **Key Features:**
            - AWS-native container orchestration
            - Integration with AWS services (ALB, CloudWatch, IAM, etc.)
            - Task definitions for defining container applications
            - Service auto-scaling
            - Supports both EC2 and Fargate launch types
            - Built-in logging and monitoring
            - Simplified networking with VPC integration
            
            **Use Cases:**
            - Microservices architectures
            - Batch processing workloads
            - Web applications and APIs
            - Long-running services
            - Machine learning deployments
            """)
    
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
            
            **Key Features:**
            - Fully managed Kubernetes control plane
            - Certified Kubernetes conformance
            - Integration with AWS services (IAM, VPC, etc.)
            - Support for both EC2 and Fargate compute
            - Managed node groups
            - Kubernetes add-on management
            - Multi-AZ high availability
            
            **Use Cases:**
            - Organizations with existing Kubernetes expertise
            - Multi-cloud container strategies
            - Complex container orchestration requirements
            - When Kubernetes-specific features are needed
            - Applications requiring open-source ecosystem tools
            """)
    
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
            
            **Key Features:**
            - Serverless compute for containers
            - Pay-per-task pricing model
            - No server management
            - Application-level isolation
            - Compatible with both ECS and EKS
            - Automatic scaling
            - Integrated with VPC networking
            
            **Use Cases:**
            - Unpredictable workloads
            - Development and test environments
            - Batch processing jobs
            - Microservices with variable load
            - Applications requiring high security isolation
            - Teams wanting to minimize operational overhead
            """)
    
    st.header("Choosing the Right Container Service")
    st.markdown("""
    | Consideration | Amazon ECS | Amazon EKS | AWS Fargate |
    |--------------|------------|------------|-------------|
    | **Control Plane** | AWS-proprietary | Kubernetes | N/A (Serverless) |
    | **Infrastructure Management** | EC2 self-managed, or Fargate | EC2 self-managed, managed node groups, or Fargate | None (serverless) |
    | **AWS Integration** | Deep, native integration | Kubernetes-focused with AWS integrations | Works with both ECS and EKS |
    | **Learning Curve** | Lower, AWS-specific | Higher, Kubernetes knowledge required | Lowest, focus on containers only |
    | **Portability** | AWS-specific | Highly portable (Kubernetes standard) | Depends on ECS or EKS usage |
    | **Use When...** | You want AWS-native tooling and deep integration | You need Kubernetes features or multi-cloud compatibility | You want to focus on applications without managing infrastructure |
    """)
    
    st.header("Container Deployment Strategies")
    st.markdown("""
    **Common Deployment Patterns:**
    
    1. **Blue/Green Deployment:**
       - Create new environment alongside old one
       - Switch traffic all at once when ready
       - Easy rollback by switching back
       - ECS and EKS both support this pattern
    
    2. **Rolling Updates:**
       - Gradually replace containers with new version
       - Maintain availability during update
       - Built into both ECS and EKS
    
    3. **Canary Deployments:**
       - Route small percentage of traffic to new version
       - Monitor performance and errors
       - Gradually increase traffic to new version
       - Implement with AWS App Mesh or Kubernetes tools
    
    4. **A/B Testing:**
       - Deploy multiple versions simultaneously
       - Route traffic based on user characteristics
       - Measure performance and user behavior
       - Combine with application load balancer or service mesh
    """)
    
    display_quiz("containers")

# Function for Security Services page
def security_services_page():
    st.title("Additional AWS Security Services")
    
    st.header("AWS Security Services Overview")
    st.markdown("""
    AWS provides a comprehensive suite of security services to help you protect your data, accounts, and workloads in the cloud. 
    These services complement the core security features built into AWS services and provide additional layers of protection for 
    your applications and data.
    """)
    
    # Secrets Manager
    st.subheader("AWS Secrets Manager")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(aws_images["secrets_manager"], width=300)
        except:
            st.warning("Secrets Manager image could not be displayed")
    
    with col2:
        st.markdown("""
        **What is AWS Secrets Manager?**
        
        AWS Secrets Manager is a service that helps you protect access to your applications, services, and IT resources without 
        the upfront investment and ongoing maintenance costs of operating your own secrets management infrastructure.
        
        **Key Features:**
        - Secure storage of secrets (passwords, API keys, tokens)
        - Automatic secrets rotation
        - Fine-grained access control with IAM
        - Encryption at rest and in transit
        - Integration with AWS services
        - Centralized audit trail
        
        **Use Cases:**
        - Database credential management
        - API key storage and rotation
        - OAuth token management
        - Storing TLS certificates
        - Application configuration secrets
        """)
    
    st.divider()
    
    # AWS Certificate Manager
    st.subheader("AWS Certificate Manager (ACM)")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(aws_images["acm"], width=300)
        except:
            st.warning("ACM image could not be displayed")
    
    with col2:
        st.markdown("""
        **What is AWS Certificate Manager?**
        
        AWS Certificate Manager (ACM) handles the complexity of creating, storing, and renewing public and private SSL/TLS X.509 
        certificates and keys that protect your AWS websites and applications.
        
        **Key Features:**
        - Free public SSL/TLS certificates
        - Automated certificate renewal
        - Easy deployment to integrated services
        - Private certificate authority option
        - Managed certificate deployment
        - Centralized certificate management
        
        **Use Cases:**
        - Securing websites with HTTPS
        - Protecting API endpoints
        - Securing internal applications
        - Implementing mutual TLS (mTLS)
        - Managing certificates for CloudFront distributions
        """)
    
    st.divider()
    
    # Systems Manager Patch Manager
    st.subheader("AWS Systems Manager Patch Manager")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(aws_images["patch_manager"], width=300)
        except:
            st.warning("Patch Manager image could not be displayed")
    
    with col2:
        st.markdown("""
        **What is AWS Systems Manager Patch Manager?**
        
        AWS Systems Manager Patch Manager automates the process of patching managed instances with both security-related and 
        other types of updates. You can use Patch Manager to apply patches for both operating systems and applications.
        
        **Key Features:**
        - Automated patch management
        - Support for Windows and Linux
        - Patch compliance reporting
        - Scheduled patching with maintenance windows
        - Customizable patch baselines
        - Centralized management across accounts
        
        **Use Cases:**
        - Security patch deployment
        - OS and application updates
        - Compliance management
        - Vulnerability remediation
        - Centralized patch management
        """)
    
    st.divider()
    
    # IAM Identity Center
    st.subheader("AWS IAM Identity Center")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(aws_images["iam_identity_center"], width=300)
        except:
            st.warning("IAM Identity Center image could not be displayed")
    
    with col2:
        st.markdown("""
        **What is AWS IAM Identity Center?**
        
        AWS IAM Identity Center (successor to AWS Single Sign-On) helps you securely create or connect your workforce identities 
        and manage their access centrally across AWS accounts and applications.
        
        **Key Features:**
        - Single sign-on for AWS accounts and applications
        - Centralized permission management
        - Multiple identity source options
        - Integration with AWS Organizations
        - Attribute-based access control
        - User portal for application access
        
        **Use Cases:**
        - Multi-account AWS access management
        - SaaS application access control
        - Workforce identity federation
        - Centralizing access management
        - Simplifying permission management
        """)
    
    st.divider()
    
    # AWS Directory Service
    st.subheader("AWS Directory Service")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(aws_images["directory_service"], width=300)
        except:
            st.warning("Directory Service image could not be displayed")
    
    with col2:
        st.markdown("""
        **What is AWS Directory Service?**
        
        AWS Directory Service provides multiple ways to use Microsoft Active Directory (AD) with other AWS services. Directories 
        store information about users, groups, and devices, and administrators use them to manage access to information and resources.
        
        **Key Features:**
        - Managed Microsoft Active Directory
        - Multiple directory types (Microsoft AD, Simple AD, AD Connector)
        - High availability and automatic failover
        - Seamless integration with AWS services
        - Domain join capabilities
        - Group policy support
        
        **Use Cases:**
        - Windows workload management
        - Centralized user authentication
        - Extending on-premises AD to AWS
        - Providing directory services for AWS resources
        - Simplifying AWS resource access management
        """)
    
    st.divider()
    
    # AWS Resource Access Manager
    st.subheader("AWS Resource Access Manager (RAM)")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(aws_images["ram"], width=300)
        except:
            st.warning("RAM image could not be displayed")
    
    with col2:
        st.markdown("""
        **What is AWS Resource Access Manager?**
        
        AWS Resource Access Manager (RAM) helps you securely share your resources across AWS accounts, within your organization or 
        organizational units, and with IAM roles and users for supported resource types.
        
        **Key Features:**
        - Secure resource sharing across accounts
        - Fine-grained access controls
        - Centralized view of shared resources
        - Integration with AWS Organizations
        - No additional charge for the service
        
        **Use Cases:**
        - Multi-account architectures
        - Shared services models
        - Central IT resource sharing
        - Sharing VPC subnets across accounts
        - Collaborative development environments
        """)
    
    st.divider()
    
    # Amazon Cognito
    st.subheader("Amazon Cognito")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(aws_images["cognito"], width=300)
        except:
            st.warning("Cognito image could not be displayed")
    
    with col2:
        st.markdown("""
        **What is Amazon Cognito?**
        
        Amazon Cognito provides authentication, authorization, and user management for web and mobile applications. It enables 
        you to add user sign-up, sign-in, and access control to your applications easily and securely.
        
        **Key Features:**
        - User directories with sign-up and sign-in
        - Identity federation with social and enterprise IdPs
        - Multi-factor authentication
        - Access control for AWS resources
        - Secure storage of app data
        - Standards-based authentication (OAuth 2.0, OIDC, SAML)
        
        **Use Cases:**
        - Mobile and web application authentication
        - Social identity federation
        - Secure AWS resource access from applications
        - Customer identity management
        - API authorization
        """)
    
    st.header("Security Service Selection Guide")
    st.markdown("""
    | If You Need To... | Consider Using... |
    |------------------|-------------------|
    | Manage application secrets and credentials | AWS Secrets Manager |
    | Deploy and manage SSL/TLS certificates | AWS Certificate Manager |
    | Automate OS and application patching | Systems Manager Patch Manager |
    | Centralize access to multiple AWS accounts | IAM Identity Center |
    | Manage Microsoft Active Directory workloads | AWS Directory Service |
    | Share AWS resources across accounts | AWS Resource Access Manager |
    | Add user authentication to applications | Amazon Cognito |
    | Provide federated access to AWS resources | AWS IAM with identity federation |
    | Secure data with encryption | AWS Key Management Service (KMS) |
    | Protect web applications from attacks | AWS WAF and Shield |
    """)
    
    display_quiz("aws_security")

# Function for Data Analytics and ML page
def analytics_ml_page():
    st.title("Data Analytics & Machine Learning")
    
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
    
    # Create tabs for different analytics services
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Amazon Redshift", "Amazon Athena", "Amazon EMR", "Amazon OpenSearch", "Amazon Kinesis"
    ])
    
    with tab1:
        st.markdown("""
        ## Amazon Redshift
        
        **What is Redshift?**
        
        Amazon Redshift is a fully managed, petabyte-scale data warehouse service that makes it simple and cost-effective to 
        analyze all your data using standard SQL and existing business intelligence (BI) tools.
        
        **Key Features:**
        - Columnar storage for analytical workloads
        - Massively parallel processing (MPP) architecture
        - SQL interface for querying
        - Integration with data lakes via Redshift Spectrum
        - Machine learning capabilities with Redshift ML
        - Automatic table optimization
        
        **Use Cases:**
        - Enterprise data warehousing
        - Business intelligence applications
        - Analyzing large datasets with SQL
        - Combining diverse datasets for analysis
        - Log analysis and reporting
        """)
    
    with tab2:
        st.markdown("""
        ## Amazon Athena
        
        **What is Athena?**
        
        Amazon Athena is an interactive query service that makes it easy to analyze data in Amazon S3 using standard SQL. 
        Athena is serverless, so there is no infrastructure to manage, and you pay only for the queries that you run.
        
        **Key Features:**
        - Serverless, no infrastructure to manage
        - Pay-per-query pricing model
        - Standard SQL support (based on Presto)
        - Works directly with data in S3
        - Support for various file formats (CSV, JSON, Parquet, ORC)
        - Integration with AWS Glue Data Catalog
        
        **Use Cases:**
        - Ad-hoc data analysis
        - Log and event data querying
        - One-time data transformations
        - Business reporting on S3 data
        - Cost-effective data analysis without ETL
        """)
    
    with tab3:
        st.markdown("""
        ## Amazon EMR
        
        **What is EMR?**
        
        Amazon EMR is a cloud big data platform for processing vast amounts of data using open-source tools such as Apache Spark, 
        Apache Hive, Apache HBase, Apache Flink, Apache Hudi, and Presto.
        
        **Key Features:**
        - Managed Hadoop framework
        - Support for multiple big data tools
        - Scalable compute resources
        - Spot instance integration for cost savings
        - Integration with S3, DynamoDB, and other AWS services
        - Various deployment options (clusters, serverless)
        
        **Use Cases:**
        - Big data processing
        - Machine learning at scale
        - Extract, transform, and load (ETL) operations
        - Log analysis
        - Genomics processing
        - Financial analysis
        """)
    
    with tab4:
        st.markdown("""
        ## Amazon OpenSearch Service
        
        **What is OpenSearch Service?**
        
        Amazon OpenSearch Service (successor to Amazon Elasticsearch Service) is a managed service that makes it easy to deploy, 
        operate, and scale OpenSearch clusters for log analytics, full-text search, and application monitoring.
        
        **Key Features:**
        - Fully managed OpenSearch clusters
        - Real-time analytics capabilities
        - Full-text search engine
        - Visualization with OpenSearch Dashboards
        - Integration with popular log frameworks
        - Fine-grained access control
        
        **Use Cases:**
        - Log and application monitoring
        - Full-text search for applications
        - Security information and event management (SIEM)
        - Clickstream analytics
        - Real-time application monitoring
        - Operational analytics
        """)
    
    with tab5:
        st.markdown("""
        ## Amazon Kinesis
        
        **What is Kinesis?**
        
        Amazon Kinesis makes it easy to collect, process, and analyze real-time, streaming data so you can get timely insights 
        and react quickly to new information. It offers key capabilities to cost-effectively process streaming data at any scale.
        
        **Key Components:**
        - **Kinesis Data Streams:** Real-time data streaming service
        - **Kinesis Data Firehose:** Load streaming data into destinations
        - **Kinesis Data Analytics:** Process streaming data with SQL or Apache Flink
        - **Kinesis Video Streams:** Stream video for analysis and ML
        
        **Use Cases:**
        - Real-time analytics
        - Log and event data collection
        - IoT data processing
        - Click-stream analysis
        - Application monitoring
        - Social media data monitoring
        """)
    
    st.subheader("Additional Analytics Services")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **AWS Glue:**
        - Fully managed ETL service
        - Data catalog and schema discovery
        - Serverless data preparation
        - Job scheduling and monitoring
        - Machine learning transforms
        
        **Amazon QuickSight:**
        - Cloud-native BI service
        - ML-powered insights
        - Interactive dashboards
        - Pay-per-session pricing
        - Embedding capabilities
        """)
    
    with col2:
        st.markdown("""
        **AWS Data Pipeline:**
        - Orchestration service for data movement
        - Managed workflow dependencies
        - Data transformation capabilities
        - Retry and failure handling
        - On-premises data source support
        
        **AWS Data Exchange:**
        - Data product marketplace
        - Subscription management
        - Automated delivery
        - Third-party data integration
        - Data licensing management
        """)
    
    with col3:
        st.markdown("""
        **AWS Lake Formation:**
        - Build, secure, and manage data lakes
        - Centralized permissions
        - Automated data ingestion
        - Data cataloging and discovery
        - Fine-grained access control
        
        **Amazon MSK:**
        - Managed Kafka service
        - Streaming data pipeline
        - Automatic scaling
        - High availability
        - Integration with AWS services
        """)
    
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
    
    st.subheader("AI Services (Pre-trained APIs)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Amazon Rekognition:**
        - Image and video analysis
        - Object and scene detection
        - Facial analysis and recognition
        - Celebrity recognition
        - Text detection in images
        
        **Amazon Textract:**
        - Document text extraction
        - Form data extraction
        - Table extraction
        - Handwriting recognition
        - Automatic document processing
        """)
    
    with col2:
        st.markdown("""
        **Amazon Comprehend:**
        - Natural language processing
        - Sentiment analysis
        - Entity recognition
        - Key phrase extraction
        - Language detection
        - Custom entity recognition
        
        **Amazon Transcribe:**
        - Speech-to-text conversion
        - Multiple language support
        - Custom vocabulary
        - Speaker identification
        - Real-time transcription
        """)
    
    with col3:
        st.markdown("""
        **Amazon Polly:**
        - Text-to-speech conversion
        - Lifelike voices
        - Multiple languages
        - SSML support
        - Neural text-to-speech
        
        **Amazon Translate:**
        - Machine translation
        - Real-time translation
        - Document translation
        - Custom terminology
        - Active custom translation
        """)
    
    st.subheader("Specialized AI Services")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Amazon Forecast:**
        - Time series forecasting
        - Built-in forecasting algorithms
        - Automatic model selection
        - What-if analysis
        - Integration with business data
        
        **Amazon Personalize:**
        - Real-time personalization
        - Recommendation engine
        - Similar items recommendations
        - Personalized rankings
        - Custom user segments
        """)
    
    with col2:
        st.markdown("""
        **Amazon Kendra:**
        - Enterprise search service
        - Natural language understanding
        - Document connector framework
        - Learning from user interactions
        - Custom synonym lists
        
        **Amazon Lex:**
        - Conversational interfaces
        - Chatbot building platform
        - Natural language understanding
        - Intent recognition
        - Integration with Lambda
        """)
    
    with col3:
        st.markdown("""
        **Amazon Fraud Detector:**
        - Fraud detection service
        - Custom fraud detection models
        - Real-time evaluation
        - Account takeover protection
        - Payment fraud detection
        
        **Amazon CodeGuru:**
        - Code reviews and analysis
        - Application performance insights
        - Security vulnerability detection
        - Code optimization suggestions
        - Resource utilization analysis
        """)
    
    st.subheader("ML Platform Services")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Amazon SageMaker:**
        - End-to-end ML platform
        - Managed notebook instances
        - Model training infrastructure
        - Model deployment and hosting
        - Built-in algorithms
        - Automated machine learning
        - Model monitoring
        
        **SageMaker Components:**
        - SageMaker Studio (IDE)
        - SageMaker Canvas (No-code ML)
        - SageMaker Data Wrangler (Data prep)
        - SageMaker Feature Store
        - SageMaker Model Registry
        - SageMaker Pipelines (CI/CD for ML)
        """)
    
    with col2:
        st.markdown("""
        **Supporting Services:**
        
        **Amazon Deep Learning AMIs:**
        - Pre-configured EC2 instances
        - Popular deep learning frameworks
        - GPU and CPU options
        - Auto-scaling support
        
        **Amazon Deep Learning Containers:**
        - Pre-built Docker images
        - Optimized ML environments
        - Framework-specific containers
        - Support for distributed training
        
        **AWS Neural Interface Computing:**
        - AWS Inferentia chips
        - AWS Trainium chips
        - High-performance ML inference
        - Cost-effective training and inference
        """)
    
    st.header("Data and ML Architecture Patterns")
    st.markdown("""
    **Common Architectures:**
    
    1. **Data Lake Architecture:**
       - S3 for storage
       - AWS Glue for cataloging and ETL
       - Athena and Redshift Spectrum for querying
       - SageMaker for ML model development
       - QuickSight for visualization
    
    2. **Real-time Analytics Pipeline:**
       - Kinesis Data Streams for ingestion
       - Kinesis Data Analytics for processing
       - Kinesis Data Firehose for delivery
       - S3 or Redshift for storage
       - Lambda for transformations
    
    3. **ML Operations Pipeline:**
       - SageMaker Pipelines for orchestration
       - SageMaker Feature Store for feature management
       - SageMaker Experiments for tracking
       - SageMaker Model Monitor for monitoring
       - AWS Step Functions for workflow management
    
    4. **Serverless Data Processing:**
       - S3 event triggers
       - Lambda for processing
       - Step Functions for orchestration
       - DynamoDB or Aurora Serverless for storage
       - API Gateway for exposing results
    """)
    
    display_quiz("data_analytics")
    display_quiz("ml")

# Sidebar menu
st.sidebar.title("AWS Solutions Architect")
st.sidebar.image("https://a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_1200x630.png", width=200)

menu = st.sidebar.radio(
    "Navigation",
    ["Home", 
     "Amazon SQS", 
     "Amazon SNS", 
     "Amazon EventBridge", 
     "AWS Lambda",
     "Amazon API Gateway", 
     "Containers on AWS",
     "AWS Security Services",
     "Data Analytics & Machine Learning"
    ]
)

# Display selected page
if menu == "Home":
    home_page()
elif menu == "Amazon SQS":
    sqs_page()
elif menu == "Amazon SNS":
    sns_page()
elif menu == "Amazon EventBridge":
    eventbridge_page()
elif menu == "AWS Lambda":
    lambda_page()
elif menu == "Amazon API Gateway":
    api_gateway_page()
elif menu == "Containers on AWS":
    containers_page()
elif menu == "AWS Security Services":
    security_services_page()
elif menu == "Data Analytics & Machine Learning":
    analytics_ml_page()

# Footer
st.sidebar.divider()

# Progress tracking
if "total_score" not in st.session_state:
    st.session_state["total_score"] = 0
    st.session_state["total_attempted"] = 0

topics = ["sqs", "sns", "eventbridge", "lambda", "api_gateway", "containers", "aws_security", "data_analytics", "ml"]
total_score = 0
total_attempted = 0

for topic in topics:
    if f"{topic}_score" in st.session_state:
        total_score += st.session_state[f"{topic}_score"]
        total_attempted += st.session_state[f"{topic}_attempted"]

if total_attempted > 0:
    st.sidebar.markdown(f"**Your overall progress:** {total_score}/{total_attempted} questions ({int(total_score/total_attempted*100)}%)")
    
    # Visual progress bar
    progress = total_score / (total_attempted if total_attempted > 0 else 1)
    st.sidebar.progress(progress)

st.sidebar.markdown("© 2025 AWS Partner Certification Readiness")
st.sidebar.info("This application is designed to help you prepare for the AWS Solutions Architect - Associate certification.")
