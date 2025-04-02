
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
    "ebs": "https://d1.awsstatic.com/product-marketing/Elastic%20Block%20Store/Product-Page-Diagram_Amazon-Elastic-Block-Store.2dc2e41afdaab6e2d0a7506862522dce0d97b421.png",
    "ipv4": "https://d1.awsstatic.com/diagrams/VPC-IPv6_working_concept.62c842e76be2527954de7f3bef3789535d18d80c.png",
    "elb": "https://d1.awsstatic.com/product-marketing/Elastic%20Load%20Balancing/Product-Page-Diagram_Elastic-Load-Balancing_ALB-How-it-Works.b0d417e7c472e2a8c649c47d39da81ba8d5152cd.png",
    "cloudtrail": "https://d1.awsstatic.com/products/cloudtrail/product-page-diagram_AWS-CloudTrail_how-it-works.d2f36ddcc38509bf6e3307939327f8002507e7b8.png",
    "cloudwatch": "https://d1.awsstatic.com/Products/product-name/diagrams/product-page-diagram_CloudWatch_how-it-works.42544a3f7b72d4cc41cb0733908f416a04b31246.png",
    "cloudformation": "https://d1.awsstatic.com/Products/product-name/diagrams/product-page-diagram_CloudFormation.ad3a4c93b4fdd3366da3da0de87d7f056689c0a9.png",
    "athena": "https://d1.awsstatic.com/r2018/h/Products/product-page-diagram_Amazon-Athena%402x.918aaf505e47ec91cd24ed22d451c5cb60f2c2be.png",
    "opensearch": "https://d1.awsstatic.com/aws-icon-by-aws-service/opensearch-cube.a0e2d30db4047e3481b9c6e902c99c86c7341693.png",
    "emr": "https://d1.awsstatic.com/emr/B_Diagram_EMR_1_Platform-for-big-data.1e8d44af3767ad74db56e548a0ad9789dac13ed4.png",
    "glue": "https://d1.awsstatic.com/products/Glue/Product-Page-Diagram_AWS-Glue_How-it-Works.fed3c13226fa791f4d1254bd5eb7254a25caeb7e.png",
    "quicksight": "https://d1.awsstatic.com/Amazon%20QuickSight/product-page-diagram_Amazon-QuickSight_How-it-Works.a673c527feb6f2955a529177e22e9f5967548bc4.png"
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
        st.header("Content Review - Session 4")
        st.markdown("""
        Welcome to the AWS Partner Certification Readiness program. This interactive guide will help you prepare 
        for the Solutions Architect - Associate certification. Navigate through the topics using the sidebar menu.
        
        Each section contains key concepts, important takeaways, and interactive quizzes to reinforce your learning.
        
        **Topics covered in Week 4:**
        - AWS Elastic Block Store (EBS)
        - IPv4 vs. IPv6 Addressing
        - Elastic Load Balancer (ELB)
        - Management and Governance Services
        - AWS CloudFormation
        - AWS Analytics Services
        """)
    
    st.info("""
    **Certification Preparation Tip:** Practice hands-on with the services covered in this guide. 
    The AWS Solutions Architect - Associate exam focuses on practical knowledge of AWS services 
    and how they can be used together to design resilient, cost-effective solutions.
    """)

# Function for EBS page
def ebs_page():
    st.title("AWS Elastic Block Store (EBS)")
    
    try:
        st.image(aws_images["ebs"], width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is Amazon EBS?")
    st.markdown("""
    Amazon Elastic Block Store (EBS) provides persistent block-level storage volumes for use with Amazon EC2 instances. 
    EBS volumes are network-attached storage that persists independently from the life of an EC2 instance.
    
    **Key Features:**
    - Persistent storage that survives instance termination
    - Point-in-time snapshots stored in S3
    - Encryption using AWS KMS
    - Easily resizable without service disruption
    - Attach to and detach from EC2 instances as needed
    - Multiple volume types optimized for different workloads
    """)
    
    st.header("EBS Volume Types")
    
    # Create columns for different EBS types
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("SSD-Backed Volumes")
        
        st.markdown("""
        **General Purpose SSD (gp2/gp3)**
        - Balance of price and performance
        - 3 IOPS/GB (up to 16,000 IOPS for gp2)
        - gp3: Baseline 3,000 IOPS and 125 MiB/s
        - **Use cases**: Boot volumes, dev/test environments, low-latency interactive applications
        
        **Provisioned IOPS SSD (io1/io2)**
        - Highest performance SSD volume
        - Up to 64,000 IOPS per volume (io1), 256,000 IOPS (io2)
        - **Use cases**: I/O-intensive workloads, large databases, latency-sensitive applications
        """)
    
    with col2:
        st.subheader("HDD-Backed Volumes")
        
        st.markdown("""
        **Throughput Optimized HDD (st1)**
        - Low-cost HDD designed for frequently accessed, throughput-intensive workloads
        - Max throughput of 500 MiB/s per volume
        - **Use cases**: Big data, data warehouses, log processing
        
        **Cold HDD (sc1)**
        - Lowest cost HDD for less frequently accessed workloads
        - Max throughput of 250 MiB/s per volume
        - **Use cases**: Infrequently accessed data, archive storage
        
        **Magnetic (standard) - Previous Generation**
        - Previous generation HDD
        - **Use cases**: Workloads where data is infrequently accessed
        """)
    
    st.header("Key Considerations")
    st.markdown("""
    When choosing an EBS volume type, consider:
    
    1. **Performance Requirements**: IOPS vs. Throughput
    2. **Access Patterns**: Random vs. Sequential access
    3. **Workload Characteristics**: Read-heavy vs. Write-heavy
    4. **Data Criticality**: Durability and availability needs
    5. **Cost Optimization**: Balance performance and cost
    
    Remember that EBS volumes are AZ-specific - they can only be attached to EC2 instances in the same Availability Zone.
    """)
    
    st.header("EBS Snapshots")
    st.markdown("""
    EBS Snapshots provide a way to back up and restore your EBS volumes:
    
    - **Incremental**: Only the blocks that have changed since the last snapshot are saved
    - **S3 Storage**: Snapshots are stored in Amazon S3 (not visible in your S3 buckets)
    - **Region-specific**: Snapshots are region-specific but can be copied across regions
    - **Sharing**: Snapshots can be shared with other AWS accounts or made public
    - **Automation**: AWS Backup can be used to manage and automate snapshots
    """)
    
    display_quiz("ebs")

# Function for IPv4 vs. IPv6 page
def ip_addressing_page():
    st.title("IPv4 vs. IPv6 Addressing")
    
    try:
        st.image(aws_images["ipv4"], width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("IP Addressing in AWS")
    st.markdown("""
    AWS supports both IPv4 and IPv6 addressing protocols. Understanding IP addressing is crucial for designing 
    VPC networks, managing connectivity, and ensuring proper routing.
    
    **Key Points:**
    - By default, all AWS VPCs use IPv4 addressing
    - IPv6 support can be added optionally to VPCs and subnets
    - IPv4 and IPv6 can be used simultaneously in a VPC (dual-stack)
    - Proper IP addressing planning is critical for future growth and connectivity
    """)
    
    # Create columns for IPv4 and IPv6
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("IPv4 Addressing")
        st.markdown("""
        **IPv4 in AWS:**
        - Required for all VPCs
        - CIDR block range: /16 (65,536 IPs) to /28 (16 IPs)
        - Uses RFC 1918 private IP ranges:
          - 10.0.0.0/8
          - 172.16.0.0/12
          - 192.168.0.0/16
        
        **Subnet Reserves:**
        - First 4 IPs and last IP in each subnet are reserved
        - Example for 10.0.1.0/24:
          - 10.0.1.0: Network address
          - 10.0.1.1: VPC router
          - 10.0.1.2: DNS resolver
          - 10.0.1.3: Reserved for future use
          - 10.0.1.255: Broadcast address
        
        **Public IPv4:**
        - Assigned via Elastic IP or auto-assigned public IP
        - Mapped to private IP through NAT
        """)
    
    with col2:
        st.subheader("IPv6 Addressing")
        st.markdown("""
        **IPv6 in AWS:**
        - Optional addition to VPCs
        - AWS assigns a /56 CIDR block to the VPC
        - Subnets receive a /64 CIDR block
        - All IPv6 addresses in AWS are publicly routable
        
        **IPv6 Features:**
        - No need for NAT - direct routing to internet
        - Globally unique addresses
        - Simpler address management
        - Future-proof as IPv4 addresses become scarce
        
        **IPv6-only Subnets:**
        - EC2 instances can be launched with IPv6-only configuration
        - Requires specific instance types and AMIs
        """)
    
    st.header("IP Addressing Best Practices")
    st.markdown("""
    **VPC Design Considerations:**
    
    1. **Plan your CIDR blocks carefully** - consider future growth and potential connections to other networks
    
    2. **Avoid overlapping IP ranges** with:
       - On-premises networks you might connect to
       - Partner networks you might connect to
       - Other VPCs you might peer with
    
    3. **Subnet sizing** - create appropriately sized subnets based on expected workload
    
    4. **Consider IPv6** for new deployments to avoid IPv4 address constraints
    
    5. **Reserve IP space** for different environments (dev, test, prod) and different applications
    
    6. **Document your IP addressing scheme** to avoid confusion and conflicts
    """)
    
    st.header("VPC IP Addressing Limitations")
    st.markdown("""
    **Important Limitations to Remember:**
    
    - Cannot change the primary IPv4 CIDR block after creating a VPC
    - Can add secondary CIDR blocks to expand a VPC
    - Maximum of 5 CIDR blocks per VPC (primary + 4 secondary)
    - Maximum of 200 subnets per VPC
    - Subnet size cannot be changed after creation
    - Each EC2 instance receives a primary private IPv4 address from the subnet range
    - IPv6 addresses are assigned from Amazon's pool (cannot bring your own)
    """)
    
    display_quiz("ipv4")

# Function for ELB page
def elb_page():
    st.title("Elastic Load Balancing (ELB)")
    
    try:
        st.image(aws_images["elb"], width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is Elastic Load Balancing?")
    st.markdown("""
    Elastic Load Balancing automatically distributes incoming application traffic across multiple targets, 
    such as EC2 instances, containers, and IP addresses. It can handle the varying load of your application 
    traffic in a single Availability Zone or across multiple Availability Zones.
    
    **Key Benefits:**
    - High availability and fault tolerance
    - Elastic scaling based on traffic
    - Security features with integrated certificate management
    - Health checking and monitoring
    - Integration with AWS services like Auto Scaling
    """)
    
    st.header("ELB Types")
    
    # Create tabs for different ELB types
    tab1, tab2, tab3, tab4 = st.tabs(["Application Load Balancer", "Network Load Balancer", "Gateway Load Balancer", "Classic Load Balancer"])
    
    with tab1:
        st.subheader("Application Load Balancer (ALB)")
        st.markdown("""
        **Layer 7 (Application Layer) Load Balancer**
        
        **Key Features:**
        - Content-based routing (path, host, HTTP headers, query parameters)
        - Support for HTTP/HTTPS/gRPC protocols
        - WebSockets and HTTP/2 support
        - Request tracing and access logs
        - Integration with AWS WAF and AWS Cognito
        
        **Best For:**
        - Microservices and container-based applications
        - Applications requiring advanced routing
        - Applications with HTTP/HTTPS traffic
        """)
        
        st.image("https://d1.awsstatic.com/Digital%20Marketing/House/Hero/products/EC2/ALB-diagram.09d8e791b316c68d3ff0c3bfb7fbfb4c24e6d56a.png", width=600)
    
    with tab2:
        st.subheader("Network Load Balancer (NLB)")
        st.markdown("""
        **Layer 4 (Transport Layer) Load Balancer**
        
        **Key Features:**
        - Ultra-high performance and low latency
        - Handles millions of requests per second
        - Static IP addresses per AZ
        - Preserve source IP address
        - Support for TCP, UDP, and TLS protocols
        
        **Best For:**
        - Extreme performance requirements
        - Static IP requirements
        - Applications using protocols beyond HTTP/HTTPS
        - Use with PrivateLink for exposing services
        """)
        
        st.image("https://d1.awsstatic.com/products/load-balancing/Network-Load-Balancer.5200501ae919b50163c201133c2374ec52bbd2a3.png", width=600)
    
    with tab3:
        st.subheader("Gateway Load Balancer (GLB)")
        st.markdown("""
        **Layer 3/4 (Network Layer) Gateway and Load Balancer**
        
        **Key Features:**
        - Deploy, scale, and manage virtual appliances
        - Transparent network gateway
        - Load balancing for security appliances
        - Uses GENEVE protocol (port 6081)
        - Preserves original network packets
        
        **Best For:**
        - Security appliances (firewalls, IDS/IPS)
        - Network traffic inspection
        - Third-party virtual appliances
        """)
        
        st.image("https://d1.awsstatic.com/products/gateway-load-balancer/Product-Page-Diagram_Gateway-Load-Balancer%402x.4c5a2078bc33ba239c8d12183e0cce6322c83d36.png", width=600)
    
    with tab4:
        st.subheader("Classic Load Balancer (CLB)")
        st.markdown("""
        **Legacy Load Balancer for EC2-Classic Network**
        
        **Key Features:**
        - Layer 4 and basic Layer 7 features
        - Support for TCP/SSL/HTTP/HTTPS
        - Sticky sessions using cookies
        - Only health check is TCP or HTTP/HTTPS
        
        **Best For:**
        - Legacy applications built on the EC2-Classic network
        - Simple load balancing with minimal features
        - Applications that require TCP passthrough with Layer 7 features
        
        **Note:** AWS recommends using newer load balancer types for all new applications
        """)
    
    st.header("ELB Common Features")
    st.markdown("""
    **Features Available Across ELB Types:**
    
    1. **Health Checks**: Monitor the health of registered targets and route traffic only to healthy targets
    
    2. **Security Groups**: Control inbound and outbound traffic (except GWLB)
    
    3. **SSL/TLS Termination**: Offload encryption/decryption to the load balancer (ALB, NLB, CLB)
    
    4. **CloudWatch Integration**: Monitor load balancer performance with metrics
    
    5. **Access Logs**: Capture detailed information about requests (ALB, CLB)
    
    6. **Cross-Zone Load Balancing**: Distribute traffic evenly across all targets regardless of AZ
    
    7. **Connection Draining/Deregistration Delay**: Complete in-flight requests during target deregistration
    """)
    
    st.header("Load Balancing Best Practices")
    st.markdown("""
    **Architectural Recommendations:**
    
    1. **Multi-AZ Deployment**: Deploy targets in multiple AZs for high availability
    
    2. **Right-Sizing**: Ensure sufficient targets to handle peak load plus margin
    
    3. **Pre-Warming**: Contact AWS for expected traffic spikes beyond normal patterns
    
    4. **Security**: Apply security groups to control traffic to/from load balancers
    
    5. **Monitoring**: Set up CloudWatch alarms for key metrics
    
    6. **Health Checks**: Configure appropriate health checks that verify application health
    
    7. **Choose the Right Type**: Select the appropriate load balancer type based on application requirements
    """)
    
    display_quiz("elb")

# Function for Management and Governance page
def management_page():
    st.title("Management and Governance")
    
    st.header("AWS Management and Monitoring Services")
    st.markdown("""
    AWS provides a comprehensive set of tools for managing, monitoring, and governing your AWS resources. 
    These services help you maintain operational excellence, ensure compliance, and optimize your infrastructure.
    """)
    
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
        **What is CloudTrail?**  
        AWS CloudTrail is a service that provides event history of your AWS account activity, including actions 
        taken through the AWS Management Console, AWS SDKs, command line tools, and other AWS services.
        
        **Key Features:**
        - Records API calls across AWS services
        - Maintains event history for 90 days
        - Delivers log files to S3 for long-term storage
        - Validates log file integrity
        - Integrates with CloudWatch Logs for monitoring
        
        **Use Cases:**
        - Security analysis and compliance auditing
        - Resource change tracking
        - Troubleshooting operational issues
        - Identifying unauthorized access
        """)
    
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
        **What is CloudWatch?**  
        Amazon CloudWatch is a monitoring and observability service that provides data and actionable 
        insights for AWS, hybrid, and on-premises applications and infrastructure resources.
        
        **Key Features:**
        - Collects and tracks metrics
        - Collects and monitors log files
        - Sets alarms and creates triggers to automate actions
        - Custom dashboards for visualization
        - Anomaly detection using machine learning
        
        **Use Cases:**
        - Application performance monitoring
        - Resource utilization tracking
        - Operational health insights
        - Setting up automated actions based on defined thresholds
        """)
    
    st.divider()
    
    # AWS Config section
    st.subheader("AWS Config")
    st.markdown("""
    **What is AWS Config?**  
    AWS Config is a service that enables you to assess, audit, and evaluate the configurations of your 
    AWS resources. It continuously monitors and records AWS resource configurations and allows 
    automated evaluation of recorded configurations against desired configurations.
    
    **Key Features:**
    - Resource inventory and configuration history
    - Configuration change notifications
    - Relationship mapping between resources
    - Compliance auditing against rules and policies
    - Automated remediation actions
    
    **Use Cases:**
    - Compliance auditing
    - Security analysis
    - Resource change tracking
    - Troubleshooting
    """)
    
    st.divider()
    
    st.header("Comparing Management Services")
    st.markdown("""
    | Service | Primary Function | Focus Area | Use When You Need |
    |---------|-----------------|------------|-------------------|
    | **CloudTrail** | Records API activity | Who did what, when | Audit trail of actions taken in your AWS account |
    | **CloudWatch** | Monitors resources and applications | Performance and operations | Metrics, logs, and automated responses to changes |
    | **Config** | Records resource configurations | What changed and when | Track resource configuration changes over time |
    """)
    
    st.header("Integration Between Services")
    st.markdown("""
    These services work together to provide comprehensive management capabilities:
    
    1. **CloudTrail + CloudWatch**: Send CloudTrail events to CloudWatch Logs for monitoring and alarming
    
    2. **CloudWatch + Auto Scaling**: Use CloudWatch metrics to trigger Auto Scaling actions
    
    3. **CloudTrail + Config**: Use CloudTrail to detect who made configuration changes tracked by Config
    
    4. **Config + Lambda**: Use Lambda functions to automatically remediate non-compliant resources
    
    5. **CloudWatch + SNS**: Send notifications when CloudWatch alarms are triggered
    """)
    
    display_quiz("management")

# Function for CloudFormation page
def cloudformation_page():
    st.title("AWS CloudFormation")
    
    try:
        st.image(aws_images["cloudformation"], width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is AWS CloudFormation?")
    st.markdown("""
    AWS CloudFormation is an infrastructure as code (IaC) service that allows you to model, provision, and 
    manage AWS and third-party resources by treating infrastructure as code.
    
    **Key Benefits:**
    - Define infrastructure in template files (JSON or YAML)
    - Automate and simplify resource provisioning and updates
    - Version control your infrastructure alongside application code
    - Reproducible environments across regions and accounts
    - Free to use (pay only for resources created)
    """)
    
    st.header("Core Concepts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Templates")
        st.markdown("""
        **CloudFormation Templates:**
        - JSON or YAML formatted text files
        - Describe the AWS resources to build
        - Can include parameters for customization
        - Key sections:
          - Resources (required)
          - Parameters (optional)
          - Mappings (optional)
          - Conditions (optional)
          - Outputs (optional)
        """)
        
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
        st.subheader("Stacks")
        st.markdown("""
        **CloudFormation Stacks:**
        - Collection of AWS resources managed as a single unit
        - Created, updated, and deleted together
        - Resources in a stack are defined by the template
        - Stack operations:
          - Create-stack
          - Update-stack
          - Delete-stack
        
        **Stack Features:**
        - Automatic rollbacks on errors
        - Drift detection
        - Stack policies to protect resources
        - Change sets to preview updates
        - Nested stacks for reusable components
        """)
        
        st.image("https://docs.aws.amazon.com/images/AWSCloudFormation/latest/UserGuide/images/update-stack-changesets-diagram.png", width=400)
    
    st.header("CloudFormation vs. Elastic Beanstalk")
    st.markdown("""
    **AWS CloudFormation:**
    - General-purpose infrastructure as code
    - Provides complete control over all resource types
    - Requires defining all resources and their relationships
    - Supports many AWS resources and third-party extensions
    
    **AWS Elastic Beanstalk:**
    - Platform as a Service (PaaS) focused on applications
    - Simplifies deployment of applications
    - Handles infrastructure details automatically
    - Limited to specific application types and patterns
    - Uses CloudFormation behind the scenes
    
    **When to use CloudFormation:** When you need fine-grained control over all infrastructure resources
    
    **When to use Elastic Beanstalk:** When you want to focus on your application code rather than infrastructure
    """)
    
    st.header("Change Sets and Updates")
    st.markdown("""
    **Stack Updates:**
    
    When updating a CloudFormation stack, you can:
    
    1. **Direct Update:** Submit changed template or parameter values
       - CloudFormation updates only the changed resources
       - Automatic rollback if update fails
    
    2. **Change Sets:** Preview changes before execution
       - Create multiple change sets to explore options
       - Review potential impacts before implementing changes
       - Execute the chosen change set when ready
    
    **Update Behaviors:**
    
    Resources are updated in different ways depending on the property changes:
    
    - **No Interruption:** Updates without disrupting the resource or changing physical ID
    - **Some Interruption:** Updates with possible disruption but preserves physical ID
    - **Replacement:** Creates a new resource with a new physical ID
    """)
    
    st.header("Nested Stacks")
    st.markdown("""
    **What are Nested Stacks?**
    
    Nested stacks are stacks created as part of other stacks. They allow you to decompose complex templates into smaller, reusable components.
    
    **Benefits:**
    
    - **Modularity:** Break down complex architectures into manageable pieces
    - **Reusability:** Create common patterns once and reuse them
    - **Maintenance:** Update components independently
    
    **Implementation:**
    
    - Use the `AWS::CloudFormation::Stack` resource type
    - Specify the template URL (must be stored in S3)
    - Pass parameters from parent stack to nested stack
    
    **Considerations:**
    
    - Nested stacks are created, updated, and deleted with the parent stack
    - Maximum nesting depth of 10 levels
    - Changes to nested stacks affect the parent stack
    """)
    
    display_quiz("cloudformation")

# Function for Analytics Services page
def analytics_page():
    st.title("AWS Analytics Services")
    
    st.header("Overview of AWS Analytics Services")
    st.markdown("""
    AWS offers a comprehensive suite of analytics services to help you collect, process, analyze, 
    and visualize data at any scale. These services enable you to build sophisticated data analytics 
    and machine learning solutions.
    """)
    
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
        **What is Amazon Athena?**  
        An interactive query service that makes it easy to analyze data in Amazon S3 using standard SQL. 
        Athena is serverless, so there is no infrastructure to manage.
        
        **Key Features:**
        - Serverless query service - no clusters to manage
        - Pay per query - only for data scanned
        - Built on Presto and supports ANSI SQL
        - Works with data in S3 in various formats (CSV, JSON, ORC, Parquet, Avro)
        - Integrates with AWS Glue Data Catalog
        
        **Use Cases:**
        - Ad-hoc data exploration
        - Log analysis
        - Business intelligence reporting
        - SQL-based queries on S3 data
        """)
    
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
        **What is Amazon OpenSearch Service?**  
        A managed service that makes it easy to deploy, operate, and scale OpenSearch clusters in the AWS Cloud. 
        OpenSearch is a fork of Elasticsearch.
        
        **Key Features:**
        - Fully managed search and analytics engine
        - Visualization capabilities with OpenSearch Dashboards
        - Scales with your data volume
        - Integrated security and access controls
        - Automated snapshots for backup
        
        **Use Cases:**
        - Log and infrastructure monitoring
        - Security information and event management (SIEM)
        - Full-text search capabilities
        - Real-time application monitoring
        - Clickstream analytics
        """)
    
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
        **What is Amazon EMR?**  
        A managed cluster platform that simplifies running big data frameworks like Apache Hadoop, Apache Spark, 
        and Presto on AWS to process and analyze vast amounts of data.
        
        **Key Features:**
        - Managed cluster environment for big data processing
        - Support for multiple frameworks (Hadoop, Spark, Hive, Presto, etc.)
        - Flexible deployment options (on EC2, on EKS, or serverless)
        - Automatic scaling based on workload
        - Integration with AWS services like S3, DynamoDB, and Kinesis
        
        **Use Cases:**
        - Big data processing
        - Machine learning
        - Interactive SQL queries
        - Data transformations
        - Scientific simulations
        """)
    
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
        **What is AWS Glue?**  
        A serverless data integration service that makes it easy to discover, prepare, and combine data 
        for analytics, machine learning, and application development.
        
        **Key Features:**
        - Serverless ETL (Extract, Transform, Load) service
        - Automated schema discovery and data cataloging
        - Visual ETL job development
        - Job scheduling and monitoring
        - Built-in transforms for data cleaning and enrichment
        
        **Use Cases:**
        - Data preparation for analytics
        - Building data lakes
        - Creating ETL pipelines
        - Cataloging data from multiple sources
        - Streaming ETL for real-time data
        """)
    
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
        **What is Amazon QuickSight?**  
        A cloud-native business intelligence service that makes it easy to create and publish interactive 
        dashboards and data visualizations.
        
        **Key Features:**
        - Machine learning-powered insights
        - Serverless architecture that scales automatically
        - Pay-per-session pricing model
        - Embedded analytics capabilities
        - Integration with various data sources
        
        **Use Cases:**
        - Business intelligence dashboards
        - Ad hoc data analysis
        - Embedded analytics in applications
        - Automated business insights
        - Interactive data reporting
        """)
    
    st.header("Choosing the Right Analytics Service")
    st.markdown("""
    **Decision Factors:**
    
    1. **Data Volume and Velocity:**
       - For massive datasets or streaming data → EMR or Kinesis
       - For moderate data with SQL needs → Athena
       - For real-time analytics → OpenSearch or Kinesis
    
    2. **Query Types:**
       - For ad-hoc SQL queries → Athena
       - For full-text search and log analysis → OpenSearch
       - For complex big data processing → EMR
    
    3. **Integration Requirements:**
       - For data catalog and ETL → AWS Glue
       - For visualization needs → QuickSight
       - For building a data lake → Combination of S3, Glue, and Athena
    
    4. **Operational Complexity:**
       - For minimal management → Serverless options like Athena and Glue
       - For control over the environment → EMR
       - For managed search service → OpenSearch Service
    """)
    
    st.header("Common Analytics Architectures")
    st.markdown("""
    **Data Lake Architecture:**
    1. Ingest data to S3 (raw zone)
    2. Catalog metadata with AWS Glue
    3. Transform data with Glue ETL
    4. Store processed data in S3 (processed zone)
    5. Query with Athena or EMR
    6. Visualize with QuickSight
    
    **Log Analytics Architecture:**
    1. Collect logs with CloudWatch Logs or Kinesis
    2. Store logs in S3
    3. Index logs in OpenSearch Service
    4. Analyze with OpenSearch Dashboards
    5. Set up alerts for anomalies
    
    **Batch Processing Architecture:**
    1. Store raw data in S3
    2. Process with EMR using Spark or Hadoop
    3. Load results to data warehouse or S3
    4. Query with Athena or Redshift
    5. Create reports with QuickSight
    """)
    
    display_quiz("analytics")

# Sidebar menu
st.sidebar.title("AWS Solutions Architect")
st.sidebar.image("https://a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_1200x630.png", width=200)

menu = st.sidebar.radio(
    "Navigation",
    ["Home", 
     "AWS Elastic Block Store (EBS)", 
     "IPv4 vs. IPv6 Addressing", 
     "Elastic Load Balancer (ELB)", 
     "Management and Governance",
     "AWS CloudFormation", 
     "AWS Analytics Services"]
)

# Display selected page
if menu == "Home":
    home_page()
elif menu == "AWS Elastic Block Store (EBS)":
    ebs_page()
elif menu == "IPv4 vs. IPv6 Addressing":
    ip_addressing_page()
elif menu == "Elastic Load Balancer (ELB)":
    elb_page()
elif menu == "Management and Governance":
    management_page()
elif menu == "AWS CloudFormation":
    cloudformation_page()
elif menu == "AWS Analytics Services":
    analytics_page()

# Footer
st.sidebar.divider()

# Progress tracking
if "total_score" not in st.session_state:
    st.session_state["total_score"] = 0
    st.session_state["total_attempted"] = 0

topics = ["ebs", "ipv4", "elb", "management", "cloudformation", "analytics"]
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
