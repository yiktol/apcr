
import streamlit as st
import base64
from PIL import Image
import os
import json
import random
from io import BytesIO
import requests
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
    topics = ["caching", "database", "ec2", "placement_groups", "amis_metadata", "kms", "security"]
    
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
    topics = ["caching", "database", "ec2", "placement_groups", "amis_metadata", "kms", "security"]
    
    for topic in topics:
        st.session_state.quiz_scores[topic] = 0
        st.session_state.quiz_attempted[topic] = 0
        st.session_state.quiz_answers[topic] = {}
    
    st.success("✅ Quiz data has been reset successfully!")

# Initialize session state at app startup
init_session_state()

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
    "caching": "https://d1.awsstatic.com/product-marketing/ElastiCache/ElastiCache_Redis.4a0a3395fceaaf7c1768319949c6a98fa96e1ddf.png",
    "database": "https://d1.awsstatic.com/webteam/product-pages/Product-Page_Standard-Icons_Database_60_Dark.8e764fec1e8a618d657bd571128d8d39b768a48c.png",
    "ec2": "https://d1.awsstatic.com/re19/FX-Diagram_EC2-Amazon-EC2.164a9cce04c473bca3fce528e10b60a406104a4a.png",
    "security": "https://d1.awsstatic.com/security-center/SecurityCenter-header@2x.3b48f05c0bbaf7f91ce5d1a7a319161cc875d308.png",
    "kms": "https://d1.awsstatic.com/products/KMS/product-page-diagram_AWS-KMS_how-it-works.7a711974a037ea8a9edc53aa3c5b541a84261048.png",
}

# Quiz questions data - with scenario-based questions
quiz_data = {
    "caching": [
        {
            "question": "Your e-commerce application is experiencing high database load during flash sales. The application uses a relational database and most operations are read-heavy. The development team needs a caching solution that supports multi-threading to distribute workloads efficiently across CPU cores. Which caching solution should you recommend?",
            "options": [
                "Amazon ElastiCache for Redis with cluster mode enabled",
                "Amazon ElastiCache for Memcached with multi-threaded processing",
                "Amazon DynamoDB Accelerator (DAX) with multi-threaded client",
                "Amazon RDS Read Replicas with connection pooling",
                "Amazon ElastiCache for Redis with single-threaded processing and sharding"
            ],
            "answer": "Amazon ElastiCache for Memcached with multi-threaded processing"
        },
        {
            "question": "A financial services company needs to migrate their Windows-based file share environment to AWS. They require SMB protocol support, Windows-native permissions, and integration with their existing Active Directory. The solution must also support Microsoft SQL Server databases that require high-performance file storage. Which AWS service best meets these requirements?",
            "options": [
                "Amazon EFS with Windows compatibility layer",
                "Amazon S3 with AWS Storage Gateway",
                "Amazon FSx for Windows File Server",
                "Amazon FSx for Lustre with Windows Integration",
                "Amazon EBS volumes shared across multiple EC2 instances"
            ],
            "answer": "Amazon FSx for Windows File Server"
        },
        {
            "question": "A media company processes large video files and needs a shared file system accessible from multiple Linux-based EC2 instances simultaneously. The workflow involves both initial processing and long-term archival, with some files accessed frequently and others rarely accessed after the initial processing. Cost optimization is a priority. Which storage configuration would you recommend?",
            "options": [
                "Amazon EFS Standard with lifecycle management to EFS Infrequent Access",
                "Amazon S3 with S3 File Gateway mounted on each EC2 instance",
                "Amazon FSx for Lustre with data repository integration to S3",
                "Amazon EBS Multi-Attach volumes with a custom replication solution",
                "Instance store volumes with a distributed file system like HDFS"
            ],
            "answer": "Amazon EFS Standard with lifecycle management to EFS Infrequent Access"
        },
        {
            "question": "Your gaming company has deployed a global online multiplayer game with leaderboards. Players around the world need low-latency access to constantly updating leaderboard data. The development team needs advanced data structures like sorted sets and replication capabilities. Which AWS service combination would provide the optimal solution?",
            "options": [
                "DynamoDB with Global Tables and DAX in each region",
                "ElastiCache for Redis with Global Datastore enabled",
                "ElastiCache for Memcached with a custom replication solution",
                "RDS for MySQL with Multi-AZ and read replicas in each region",
                "Neptune cluster with cross-region replication"
            ],
            "answer": "ElastiCache for Redis with Global Datastore enabled"
        },
        {
            "question": "A healthcare application needs to store patient records and allow secure access from multiple applications. The data requires 11 9's of durability, automatic scaling, and must be accessible from both AWS Lambda functions and containerized applications running on ECS. Which storage solution would you recommend?",
            "options": [
                "Amazon S3 with VPC Endpoints and server-side encryption",
                "Amazon EFS with encryption at rest and transit",
                "Amazon FSx for Windows with encryption enabled",
                "Amazon EBS volumes with Multi-Attach enabled",
                "Instance store volumes with RAID configuration"
            ],
            "answer": "Amazon EFS with encryption at rest and transit"
        }
    ],
    "database": [
        {
            "question": "A manufacturing company is collecting sensor data from thousands of IoT devices in their factories. The data is time-stamped and needs to be stored for analysis of machine performance over time. Engineers need to query patterns over specific time ranges and run analysis on how measurements change over time. Which AWS database service would be most appropriate for this use case?",
            "options": [
                "Amazon DynamoDB with Time-To-Live attributes",
                "Amazon RDS for PostgreSQL with TimescaleDB extension",
                "Amazon Timestream with memory store and magnetic store tiers",
                "Amazon DocumentDB with time-series collections",
                "Amazon Neptune with time-based graph relationships"
            ],
            "answer": "Amazon Timestream with memory store and magnetic store tiers"
        },
        {
            "question": "A financial company is migrating their MySQL database to AWS. The application handles over 500,000 transactions per minute during peak hours. They need high availability, automated backups, and the ability to scale read operations across multiple regions. The database is currently 2TB in size. Which AWS database solution offers the best performance while minimizing the operational overhead?",
            "options": [
                "Amazon RDS for MySQL with Multi-AZ and cross-region read replicas",
                "Amazon DynamoDB with Global Tables and DAX",
                "Amazon Aurora MySQL with Global Database",
                "Self-managed MySQL on EC2 with Application Load Balancer",
                "Amazon DocumentDB cluster with sharding"
            ],
            "answer": "Amazon Aurora MySQL with Global Database"
        },
        {
            "question": "An e-commerce platform experiences performance issues during flash sales when product catalog queries spike to millions per second. The application currently uses RDS MySQL, and the development team doesn't want to completely refactor the application. They need a solution that can handle the massive query throughput for product information while maintaining sub-millisecond latency. Which approach would provide the best improvement?",
            "options": [
                "Add more RDS read replicas and implement client-side connection pooling",
                "Implement Amazon ElastiCache for Redis as a cache layer with proper TTL settings",
                "Migrate to DynamoDB with DAX for in-memory acceleration",
                "Scale up the RDS instance to a larger DB instance class with higher IOPS",
                "Implement an Application Load Balancer with sticky sessions"
            ],
            "answer": "Implement Amazon ElastiCache for Redis as a cache layer with proper TTL settings"
        },
        {
            "question": "A startup is building a social media platform where users can create posts, follow other users, and interact with content through likes and comments. They need a database solution that can efficiently store and query these complex relationships. What is the most suitable AWS database service for this requirement?",
            "options": [
                "Amazon DynamoDB with single-table design",
                "Amazon RDS for PostgreSQL with JSON functions",
                "Amazon Neptune with graph data model",
                "Amazon DocumentDB with nested documents",
                "Amazon Keyspaces with wide-column storage"
            ],
            "answer": "Amazon Neptune with graph data model"
        },
        {
            "question": "A gaming company needs to implement a high-performance leaderboard system that can handle millions of concurrent players. The system needs to update scores in real-time and provide millisecond latency for leaderboard queries. Users should be able to view global rankings and rankings filtered by region. Which database architecture would provide the best performance?",
            "options": [
                "Amazon DynamoDB with Global Secondary Indexes for region filtering",
                "Amazon Aurora with read replicas in each region",
                "Amazon ElastiCache for Redis using sorted sets with DAX as an additional cache layer",
                "Amazon ElastiCache for Redis using sorted sets with Global Datastore",
                "Amazon Timestream with time-based partitioning by region"
            ],
            "answer": "Amazon ElastiCache for Redis using sorted sets with Global Datastore"
        }
    ],
    "ec2": [
        {
            "question": "A data processing company runs batch workloads that are time-flexible and can be interrupted. The jobs process scientific data and require high CPU performance, but have checkpointing capabilities to resume if interrupted. The company wants to minimize costs while ensuring the jobs complete within 24 hours. Which EC2 purchasing option would be most cost-effective?",
            "options": [
                "On-Demand Instances with Capacity Reservations",
                "Reserved Instances with a one-year commitment",
                "Spot Instances with a max price set at 40% of On-Demand pricing",
                "Dedicated Hosts with partial upfront payment",
                "EC2 Fleet with a mix of On-Demand and Reserved Instances"
            ],
            "answer": "Spot Instances with a max price set at 40% of On-Demand pricing"
        },
        {
            "question": "A healthcare analytics application processes large datasets of patient information. The application is memory-intensive during data analysis phases and requires high RAM-to-vCPU ratios. The datasets are processed in memory and require fast access to temporary storage. Which EC2 instance family would best meet these requirements?",
            "options": [
                "C5 instances with EBS optimization enabled",
                "M5 instances with large EBS volumes",
                "R5 instances with instance store volumes",
                "I3 instances with NVMe SSD storage",
                "T3 instances with burstable performance"
            ],
            "answer": "R5 instances with instance store volumes"
        },
        {
            "question": "A financial trading platform requires ultra-low latency networking between instances that perform real-time market analysis. The application consists of 8 instances that need to communicate with each other at high speed within the same Availability Zone. Which EC2 deployment strategy would provide the lowest network latency?",
            "options": [
                "Deploy instances in a spread placement group across multiple AZs",
                "Deploy instances in a cluster placement group within a single AZ",
                "Deploy instances in a partition placement group with 8 partitions",
                "Deploy instances with enhanced networking in different subnets",
                "Deploy instances with Elastic Network Adapters in multiple AZs"
            ],
            "answer": "Deploy instances in a cluster placement group within a single AZ"
        },
        {
            "question": "A video streaming service needs to transcode videos into multiple formats. The workload is variable, with peaks during content upload events. The application should scale automatically based on the queue depth of videos waiting to be processed. What is the most efficient architecture for this scenario?",
            "options": [
                "Fixed fleet of GPU-optimized EC2 instances with reserved capacity",
                "Auto Scaling group of EC2 instances with scheduled scaling actions",
                "Auto Scaling group triggered by SQS queue depth using CloudWatch metrics",
                "Fargate containers scheduled based on time of day predictions",
                "Lambda functions with X-Ray tracing for performance monitoring"
            ],
            "answer": "Auto Scaling group triggered by SQS queue depth using CloudWatch metrics"
        },
        {
            "question": "A web application runs on EC2 instances behind an Application Load Balancer. During routine patching, you need to ensure zero downtime while replacing instances. The application maintains session state in memory. Which combination of features would you implement to ensure smooth instance replacement?",
            "options": [
                "Multi-AZ deployment with Cross-Zone Load Balancing",
                "Auto Scaling group with a target tracking scaling policy",
                "Auto Scaling group with instance protection and ElastiCache for session storage",
                "Spot Fleet with instance weighting and Sticky Sessions on the ALB",
                "EC2 Auto Scaling group with lifecycle hooks and a warm-up period"
            ],
            "answer": "Auto Scaling group with instance protection and ElastiCache for session storage"
        }
    ],
    "placement_groups": [
        {
            "question": "A genomics research institute needs to run a distributed HPC workload that requires high-bandwidth, low-latency networking between compute nodes. The application processes large datasets and requires frequent node-to-node communication. The solution must minimize network latency between instances. Which placement strategy would be most effective?",
            "options": [
                "Spread placement group across multiple Availability Zones",
                "Partition placement group with one partition per computation task",
                "Cluster placement group with C5n instances that support enhanced networking",
                "Instances deployed in different subnets with VPC endpoints",
                "Multi-AZ deployment with Application Load Balancer distribution"
            ],
            "answer": "Cluster placement group with C5n instances that support enhanced networking"
        },
        {
            "question": "A financial services company runs critical transaction processing systems that cannot tolerate correlated failures. They need to deploy 7 EC2 instances for their core banking application, and each instance must run on completely separate hardware to maximize resilience. Which deployment strategy ensures maximum fault isolation?",
            "options": [
                "Deploy instances in a single AZ with a cluster placement group",
                "Deploy instances across multiple AZs without placement groups",
                "Deploy instances in a spread placement group across multiple AZs",
                "Deploy instances in a partition placement group with 7 partitions",
                "Deploy instances in multiple regions with Cross-Region Load Balancing"
            ],
            "answer": "Deploy instances in a spread placement group across multiple AZs"
        },
        {
            "question": "A company is deploying a large-scale Apache Hadoop cluster on Amazon EC2. The solution requires data locality awareness where compute nodes process data stored on local disks. They need logical grouping of instances while maintaining separation of hardware failures between task groups. Which placement strategy is most appropriate?",
            "options": [
                "Cluster placement group to minimize network latency",
                "Spread placement group to isolate potential failures",
                "Partition placement group with HDFS data nodes in separate partitions",
                "Deploy without placement groups but use Enhanced Networking",
                "Multi-AZ deployment with Cross-AZ replication"
            ],
            "answer": "Partition placement group with HDFS data nodes in separate partitions"
        },
        {
            "question": "A media streaming company is building a video processing pipeline that needs to transform raw video into multiple formats. The pipeline consists of several stages: video ingestion, transcoding, quality analysis, and distribution. Each stage has different infrastructure requirements, but all require high-speed networking. Which placement strategy provides the best balance of performance and fault tolerance?",
            "options": [
                "Single cluster placement group for all pipeline components",
                "Multiple cluster placement groups, one for each pipeline stage",
                "Spread placement group across all pipeline components",
                "Partition placement group with each stage in its own partition",
                "No placement group, but deploy across multiple AZs for fault tolerance"
            ],
            "answer": "Multiple cluster placement groups, one for each pipeline stage"
        },
        {
            "question": "A database system requires three EC2 instances for the primary database and two instances for critical monitoring tools. The primary database instances need low-latency network communication between them, while the monitoring tools should run on separate hardware to avoid being affected by database performance issues. What is the optimal EC2 deployment architecture?",
            "options": [
                "All five instances in a cluster placement group for lowest latency",
                "All five instances in a spread placement group for maximum separation",
                "Primary DB in a cluster placement group and monitoring in a separate spread placement group",
                "All five instances in a partition placement group with two partitions",
                "Primary DB instances across multiple AZs and monitoring instances in a third AZ"
            ],
            "answer": "Primary DB in a cluster placement group and monitoring in a separate spread placement group"
        }
    ],
    "amis_metadata": [
        {
            "question": "A company is implementing a CI/CD pipeline that automatically creates and tests EC2 instances. After successful testing, the instances need to be converted to AMIs for production deployment. The AMIs must contain specialized software and configuration. Which approach provides the most automated and reliable solution?",
            "options": [
                "Manually configure an EC2 instance and create an AMI using the AWS Console",
                "Use EC2 Instance Connect to SSH into instances and run configuration scripts",
                "Implement EC2 Image Builder with component documents for software installation",
                "Create a golden AMI and modify it for each deployment using CloudFormation",
                "Use AWS Backup to create AMIs from running instances on a schedule"
            ],
            "answer": "Implement EC2 Image Builder with component documents for software installation"
        },
        {
            "question": "A DevOps team needs to deploy EC2 instances that automatically join an Active Directory domain and install required software upon launch. The instances run in a private subnet without internet access. How can they ensure the instances are properly configured at launch?",
            "options": [
                "Use a public AMI and configure user data to download installation files from S3",
                "Create a custom AMI with pre-installed software and use instance metadata to retrieve AD credentials",
                "Use AWS Systems Manager to run commands after instance launch",
                "Create a custom AMI and use instance user data with a script that accesses instance metadata for configuration",
                "Deploy instances with EFS mounted and execute scripts stored in the file system"
            ],
            "answer": "Create a custom AMI and use instance user data with a script that accesses instance metadata for configuration"
        },
        {
            "question": "A company is migrating from on-premises infrastructure to AWS. They need to bring their existing virtual machine images and convert them to run on EC2. The images contain proprietary software with specific licensing. Which migration approach would be most efficient?",
            "options": [
                "Re-install all software on new EC2 instances from scratch",
                "Use VM Import/Export to import the VMs as AMIs and modify the license activation",
                "Launch EC2 instances from AWS Marketplace AMIs and reconfigure them",
                "Use AWS Application Migration Service with automated replication",
                "Create new AMIs using EC2 Image Builder and install software using Systems Manager"
            ],
            "answer": "Use VM Import/Export to import the VMs as AMIs and modify the license activation"
        },
        {
            "question": "A security-conscious organization needs to implement a solution where EC2 instances can retrieve temporary credentials for accessing other AWS services without embedding access keys in the instance. The credentials should be automatically rotated. Which configuration provides this capability?",
            "options": [
                "Store access keys in EC2 instance user data and access them at runtime",
                "Use AWS Secrets Manager and manually retrieve credentials when needed",
                "Configure an IAM role for the EC2 instance and access credentials via instance metadata service",
                "Store encrypted credentials in Parameter Store and decrypt them with a KMS key",
                "Use AWS Certificate Manager to generate and distribute credentials"
            ],
            "answer": "Configure an IAM role for the EC2 instance and access credentials via instance metadata service"
        },
        {
            "question": "A company needs to launch thousands of EC2 instances from a custom AMI across multiple AWS accounts and regions. The AMI contains proprietary software and should not be publicly accessible. What is the most secure and efficient method to distribute this AMI?",
            "options": [
                "Make the AMI public and restrict access using resource-based policies",
                "Share the AMI with specific AWS account IDs and use AWS Organizations for governance",
                "Export the AMI to each account using VM Export and re-import it",
                "Use Systems Manager to build identical instances in each account",
                "Create a copy script that uses cross-account IAM roles to create AMI copies"
            ],
            "answer": "Share the AMI with specific AWS account IDs and use AWS Organizations for governance"
        }
    ],
    "kms": [
        {
            "question": "A healthcare organization needs to encrypt sensitive patient data stored in EBS volumes. They require complete control over the encryption keys, including rotation policies and access auditing. Which key management solution provides the most control while meeting compliance requirements?",
            "options": [
                "Default EBS encryption with AWS managed keys",
                "Customer managed keys in KMS with automated rotation",
                "AWS managed keys with CloudTrail logging enabled",
                "Customer managed keys in an external HSM accessed via VPC endpoints",
                "AWS managed multi-tenant keys with restricted IAM policies"
            ],
            "answer": "Customer managed keys in KMS with automated rotation"
        },
        {
            "question": "A financial services company needs to encrypt data in multiple AWS services across different regions. They need to maintain separate encryption domains for development, testing, and production environments. Which KMS configuration provides the most secure isolation?",
            "options": [
                "Use a single customer managed key with aliases for different environments",
                "Create separate customer managed keys for each environment with distinct IAM policies",
                "Use default AWS managed keys with resource tags to distinguish environments",
                "Implement AWS managed keys with service control policies",
                "Use a single multi-region key with conditional key policies"
            ],
            "answer": "Create separate customer managed keys for each environment with distinct IAM policies"
        },
        {
            "question": "A company is implementing a disaster recovery strategy for their EC2-based application. They need to ensure that encrypted EBS snapshots from one region can be restored in a different region during a regional failure. Which encryption approach should they implement?",
            "options": [
                "Use default EBS encryption in both regions",
                "Create customer managed KMS keys in both regions and re-encrypt snapshots during copy",
                "Use multi-region KMS keys for EBS encryption",
                "Use AWS managed keys with cross-region snapshot copying",
                "Disable encryption for DR volumes to simplify recovery"
            ],
            "answer": "Use multi-region KMS keys for EBS encryption"
        },
        {
            "question": "A development team needs to encrypt application data at rest in DynamoDB and in transit to their application. They also need to store sensitive configuration parameters securely. Which combination of AWS services provides end-to-end encryption while simplifying key management?",
            "options": [
                "KMS for DynamoDB encryption and Secrets Manager with custom KMS keys for configuration",
                "S3 for encrypted storage and Parameter Store with default encryption for configuration",
                "CloudHSM for DynamoDB encryption and Secrets Manager for configuration",
                "KMS for DynamoDB and Systems Manager Parameter Store with SecureString type for configuration",
                "DynamoDB with default encryption and custom application-layer encryption"
            ],
            "answer": "KMS for DynamoDB and Systems Manager Parameter Store with SecureString type for configuration"
        },
        {
            "question": "A regulated company needs to implement encryption for data stored on EBS volumes attached to EC2 instances. They need to ensure that if an unauthorized user gains access to the EBS volumes, the data remains protected. Additionally, they must ensure data is encrypted during snapshot operations and when new volumes are created from snapshots. Which encryption approach meets these requirements with minimal operational overhead?",
            "options": [
                "Implement application-level encryption in the EC2 instance",
                "Mount encrypted file systems on top of unencrypted EBS volumes",
                "Enable default EBS encryption at the account level with a customer managed KMS key",
                "Use third-party volume encryption software within the EC2 instance",
                "Manually encrypt each volume after creation using AWS CLI"
            ],
            "answer": "Enable default EBS encryption at the account level with a customer managed KMS key"
        }
    ],
    "security": [
        {
            "question": "A company has implemented a microservices architecture on AWS using API Gateway, Lambda, and DynamoDB. They need to identify any unauthorized API calls or unusual access patterns that might indicate a security breach. Which AWS service and configuration would provide the most comprehensive security monitoring?",
            "options": [
                "Enable AWS Config rules to detect unauthorized API calls",
                "Deploy Amazon Inspector agents on all resources",
                "Configure CloudTrail with a multi-region trail sending logs to CloudWatch Logs with metric filters and alarms",
                "Implement GuardDuty with S3 protection enabled",
                "Use AWS Security Hub with all standard rule sets enabled"
            ],
            "answer": "Configure CloudTrail with a multi-region trail sending logs to CloudWatch Logs with metric filters and alarms"
        },
        {
            "question": "An e-commerce application hosted on EC2 instances behind an Application Load Balancer is experiencing sporadic HTTP flood attacks that degrade performance. The attacks come from constantly changing IP addresses but follow consistent patterns in request headers. Which AWS service configuration would best mitigate these attacks?",
            "options": [
                "Configure AWS Shield Standard with rate-based rules",
                "Implement AWS WAF with rate-based rules and HTTP header inspection",
                "Deploy AWS Network Firewall with stateful traffic inspection",
                "Use Security Groups with connection limiting",
                "Enable CloudFront with geo-restriction features"
            ],
            "answer": "Implement AWS WAF with rate-based rules and HTTP header inspection"
        },
        {
            "question": "A global media streaming service is experiencing large-scale DDoS attacks targeting both their network and application layers. The attacks have caused service outages in multiple regions. The company needs a comprehensive protection strategy that includes proactive monitoring and response. Which solution provides the most robust protection?",
            "options": [
                "Deploy AWS Shield Standard with CloudWatch alarms",
                "Implement AWS WAF with custom rules and Shield Advanced",
                "Subscribe to AWS Shield Advanced with the Shield Response Team (SRT) and implement WAF",
                "Configure AWS Firewall Manager with Shield Standard protection",
                "Use Amazon GuardDuty with CloudWatch Events for automated response"
            ],
            "answer": "Subscribe to AWS Shield Advanced with the Shield Response Team (SRT) and implement WAF"
        },
        {
            "question": "A multinational corporation has multiple AWS accounts managed through AWS Organizations. They need to enforce consistent security rules for AWS WAF, Shield Advanced, and security groups across all accounts and resources. New accounts should automatically inherit these protections. Which service and configuration would you recommend?",
            "options": [
                "Use AWS Config with organization-wide rules",
                "Implement Service Control Policies (SCPs) to enforce security configurations",
                "Deploy CloudFormation StackSets to all accounts",
                "Configure AWS Firewall Manager with security policies applied to the organization",
                "Use IAM Permission Boundaries across all accounts"
            ],
            "answer": "Configure AWS Firewall Manager with security policies applied to the organization"
        },
        {
            "question": "A company needs to investigate unexpected API calls in their AWS account. They need to determine who made specific calls, from which IP addresses, and when the calls occurred. Some of the API calls relate to network configuration changes made in the last 90 days. Where can they find this information?",
            "options": [
                "VPC Flow Logs filtered by API endpoint destinations",
                "CloudTrail logs stored in S3 with Athena queries for network changes",
                "CloudWatch Logs with custom metric filters for API calls",
                "AWS Config history for network resources",
                "GuardDuty findings related to API calls"
            ],
            "answer": "CloudTrail logs stored in S3 with Athena queries for network changes"
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
            image = load_image_from_url(aws_images["home"])
            if image:
                st.image(image, width=300)
        except:
            st.error("Unable to load image")
    
    with col2:
        st.title("AWS Solutions Architect - Associate")
        st.header("Content Review - Session 3")
        st.markdown("""
        Welcome to the AWS Partner Certification Readiness program. This interactive guide will help you prepare 
        for the Solutions Architect - Associate certification. Navigate through the topics using the tabs above.
        
        Each section contains key concepts and important takeaways. Test your knowledge with the Knowledge Checks tab.
        """)
    
    st.markdown("""
    <div class="aws-info-card">
        <h3>Topics covered:</h3>
        <ul>
            <li>AWS Caching & File Servers</li>
            <li>AWS Database Offerings</li>
            <li>AWS Elastic Compute Cloud (EC2)</li>
            <li>EC2 Placement Groups</li>
            <li>EC2 AMIs and Instance Metadata</li>
            <li>Amazon KMS & EBS Encryption</li>
            <li>AWS Security</li>
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

# Function for AWS Caching & File Servers page
def caching_page():
    st.title("AWS Caching & File Servers")
    
    try:
        image = load_image_from_url(aws_images["caching"])
        if image:
            st.image(image, width=600)
    except:
        st.warning("Image could not be displayed")
    
    st.header("Amazon ElastiCache")
    st.markdown("""
    Amazon ElastiCache is a fully managed, in-memory caching service supporting flexible, real-time use cases.

    **Key Features:**
    - Accelerates application performance with microsecond latency
    - Reduces pressure on backend databases by caching data
    - Stores non-durable datasets in memory for real-time applications

    **ElastiCache Engines:**
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Redis</h4>
            <ul>
                <li>Advanced data structures (lists, sets, sorted sets, hashes)</li>
                <li>Replication and high availability</li>
                <li>Snapshots for backup and recovery</li>
                <li>Transactions and Pub/Sub capabilities</li>
                <li><strong>Use Cases</strong>: Gaming leaderboards, chat/messaging, real-time analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Memcached</h4>
            <ul>
                <li>Simple design focused on simplicity</li>
                <li>Multi-threaded architecture</li>
                <li>Data partitioning</li>
                <li><strong>Use Cases</strong>: Caching database query results, session caching, page caching</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("Amazon Elastic File System (EFS)")
    st.markdown("""
    <div class="aws-card">
        <p>A simple, serverless, set-and-forget elastic file system for Linux-based workloads.</p>
        <h4>Key Features:</h4>
        <ul>
            <li>Fully managed Network File System (NFS) for Linux</li>
            <li>Highly available and durable (11 9's of durability)</li>
            <li>Automatically scales as files are added/removed</li>
            <li>Mount to Linux EC2 instances for shared file storage</li>
        </ul>
        <h4>Storage Classes:</h4>
        <ul>
            <li>EFS Standard</li>
            <li>EFS Standard-Infrequent Access</li>
            <li>One Zone Storage</li>
            <li>One Zone-Infrequent Access</li>
        </ul>
        <p><strong>Use Case:</strong> Modern application development with serverless architecture, allowing containerized or serverless applications to share and persist data.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("Amazon FSx for Windows File Server")
    st.markdown("""
    <div class="aws-card">
        <p>Fully managed file storage built on Windows Server.</p>
        <h4>Key Features:</h4>
        <ul>
            <li>Fully managed, highly reliable Windows file servers</li>
            <li>Uses Server Message Block (SMB) protocol</li>
            <li>Backed by a fully native Windows file system</li>
        </ul>
        <h4>Use Cases:</h4>
        <ul>
            <li>Migrate Windows file servers to AWS</li>
            <li>Run SQL Server workloads without SQL enterprise licensing</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Function for AWS Database Offerings page
def database_page():
    st.title("AWS Database Offerings")
    
    try:
        image = load_image_from_url(aws_images["database"])
        if image:
            st.image(image, width=600)
    except:
        st.warning("Image could not be displayed")
    
    st.header("Purpose-built Database Services")
    
    st.markdown("""
    <div class="aws-card">
        <p>AWS provides purpose-built database services designed for specific workloads and use cases:</p>
        <table class="dataframe">
            <thead>
                <tr>
                    <th>Database Category</th>
                    <th>Key Service</th>
                    <th>Best For</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Relational</td>
                    <td>Amazon RDS, Aurora</td>
                    <td>Structured data, transactions, complex queries</td>
                </tr>
                <tr>
                    <td>Key-Value</td>
                    <td>DynamoDB</td>
                    <td>High-throughput, low-latency applications</td>
                </tr>
                <tr>
                    <td>Document</td>
                    <td>DocumentDB</td>
                    <td>JSON document storage and queries</td>
                </tr>
                <tr>
                    <td>In-Memory</td>
                    <td>ElastiCache</td>
                    <td>Microsecond latency, caching</td>
                </tr>
                <tr>
                    <td>Graph</td>
                    <td>Neptune</td>
                    <td>Highly connected data, relationships</td>
                </tr>
                <tr>
                    <td>Time Series</td>
                    <td>Timestream</td>
                    <td>IoT data, metrics, analytics over time</td>
                </tr>
                <tr>
                    <td>Ledger</td>
                    <td>QLDB</td>
                    <td>Immutable, verifiable transaction logs</td>
                </tr>
                <tr>
                    <td>Wide Column</td>
                    <td>Keyspaces</td>
                    <td>High-speed data processing</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("Amazon RDS (Relational Database Service)")
    st.markdown("""
    <div class="aws-card">
        <p>Set up, operate, and scale a managed relational database with just a few clicks.</p>
        <h4>Key Features:</h4>
        <ul>
            <li>Available and durable (automated Multi-AZ replication, backups)</li>
            <li>Easy to administer (automated patching and maintenance)</li>
            <li>Scalable (compute and storage can scale independently)</li>
            <li>Secure (encryption at rest and in transit)</li>
        </ul>
        <h4>Supported Engines:</h4>
        <ul>
            <li>MySQL</li>
            <li>PostgreSQL</li>
            <li>MariaDB</li>
            <li>Oracle</li>
            <li>SQL Server</li>
            <li>Amazon Aurora</li>
        </ul>
        <h4>Important Features:</h4>
        <ul>
            <li>Multi-AZ deployments for high availability</li>
            <li>Read replicas for performance scaling</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("Amazon Aurora")
    st.markdown("""
    <div class="aws-feature-card">
        <p>MySQL and PostgreSQL-compatible relational database built for the cloud.</p>
        <h4>Key Features:</h4>
        <ul>
            <li>5x throughput of MySQL, 3x throughput of PostgreSQL</li>
            <li>Fault-tolerant, self-healing storage</li>
            <li>Six copies of data across three Availability Zones</li>
            <li>Continuous backup to Amazon S3</li>
            <li>Up to 15 low-latency read replicas</li>
        </ul>
        <h4>Aurora Global Databases:</h4>
        <ul>
            <li>Span multiple AWS Regions</li>
            <li>Global reads with local latency</li>
            <li>Fast recovery from region-wide outages</li>
            <li>Replication with typically under 1 second latency</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("Amazon DynamoDB")
    st.markdown("""
    <div class="aws-feature-card">
        <p>Fast and flexible NoSQL database service for any scale.</p>
        <h4>Key Features:</h4>
        <ul>
            <li>Fully managed key-value and document database</li>
            <li>Single-digit millisecond performance at any scale</li>
            <li>Can handle more than 10 trillion requests per day</li>
            <li>Supports both eventually consistent and strongly consistent reads</li>
        </ul>
        <h4>DynamoDB Accelerator (DAX):</h4>
        <ul>
            <li>Fully managed in-memory cache for DynamoDB</li>
            <li>Microsecond latency (10x performance improvement)</li>
            <li>Compatible with existing DynamoDB API calls</li>
            <li>Scales to millions of requests per second</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Function for EC2 page
def ec2_page():
    st.title("AWS Elastic Compute Cloud (EC2)")
    
    try:
        image = load_image_from_url(aws_images["ec2"])
        if image:
            st.image(image, width=600)
    except:
        st.warning("Image could not be displayed")
    
    st.header("Amazon EC2 Overview")
    st.markdown("""
    <div class="aws-card">
        <p>Amazon EC2 provides secure, resizable compute capacity in the AWS Cloud.</p>
        <h4>Key Features:</h4>
        <ul>
            <li>Increase or decrease capacity within minutes (99.99% availability per region)</li>
            <li>Complete control over computing resources</li>
            <li>Multiple security features and standards</li>
            <li>Various migration tools and paths to get started</li>
        </ul>
        <h4>EC2 Auto Scaling:</h4>
        <ul>
            <li>Add or remove compute capacity to meet changes in demand</li>
            <li>Scale based on schedules or dynamic metrics</li>
            <li>Maintain application availability during demand spikes</li>
        </ul>
        <h4>AWS Auto Scaling:</h4>
        <ul>
            <li>Monitors and automatically adjusts capacity for various AWS resources</li>
            <li>Predicts future traffic patterns, including regular spikes</li>
            <li>Works with EC2 Auto Scaling to manage dependent services</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("EC2 Billing Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>On-Demand Instances</h4>
            <ul>
                <li>Pay by the second with no commitments</li>
                <li>Ideal for short-term, irregular workloads</li>
                <li>Full control over instance lifecycle</li>
            </ul>
            <h4>Spot Instances</h4>
            <ul>
                <li>Use unused EC2 capacity at up to 90% discount</li>
                <li>Ideal for flexible, fault-tolerant workloads</li>
                <li>Instances can be interrupted with 2-minute notification</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Savings Plans</h4>
            <ul>
                <li>Lower prices for usage commitments (1 or 3 years)</li>
                <li>Flexible across instance families, sizes, OS, regions</li>
                <li>Available for EC2, Lambda, and Fargate</li>
            </ul>
            <h4>Dedicated Hosts</h4>
            <ul>
                <li>Physical servers dedicated to your use</li>
                <li>Allow BYOL (Bring Your Own License)</li>
                <li>Address compliance requirements</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("EC2 Instance Types")
    st.markdown("""
    <div class="aws-card">
        <table class="dataframe">
            <thead>
                <tr>
                    <th>Instance Type</th>
                    <th>Features</th>
                    <th>Use Cases</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>General Purpose</strong></td>
                    <td>Balanced compute, memory, networking</td>
                    <td>Web servers, development environments, small databases</td>
                </tr>
                <tr>
                    <td><strong>Compute Optimized</strong></td>
                    <td>High-performance processors</td>
                    <td>Batch processing, HPC, gaming servers, scientific modeling</td>
                </tr>
                <tr>
                    <td><strong>Memory Optimized</strong></td>
                    <td>Fast performance for memory-intensive workloads</td>
                    <td>High-performance databases, real-time big data analytics</td>
                </tr>
                <tr>
                    <td><strong>Storage Optimized</strong></td>
                    <td>Low latency, high IOPS</td>
                    <td>NoSQL databases, data warehousing, distributed file systems</td>
                </tr>
                <tr>
                    <td><strong>Accelerated Computing</strong></td>
                    <td>Hardware accelerators for data processing</td>
                    <td>ML/AI, graphics workloads, game streaming</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

# Function for EC2 Placement Groups page
def placement_groups_page():
    st.title("EC2 Placement Groups")
    st.markdown("""
    <div class="aws-card">
        <p>Placement groups influence how EC2 instances are placed on underlying hardware, affecting performance, availability, and fault tolerance.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Cluster Placement Group</h4>
            <p><strong>Description:</strong></p>
            <ul>
                <li>Instances packed close together inside a single AZ</li>
                <li>Low network latency, high throughput network performance</li>
            </ul>
            <p><strong>Best For:</strong></p>
            <ul>
                <li>High-performance computing (HPC)</li>
                <li>Applications requiring low-latency node-to-node communication</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.image("https://d1.awsstatic.com/product-marketing/EC2/Cluster%20placement%20group.b8d5681f46e1825c2a9336ef2ab3adc64d382db5.PNG", use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Spread Placement Group</h4>
            <p><strong>Description:</strong></p>
            <ul>
                <li>Instances placed on distinct underlying hardware</li>
                <li>Each instance on separate racks with independent power/network</li>
            </ul>
            <p><strong>Best For:</strong></p>
            <ul>
                <li>Critical applications requiring maximum availability</li>
                <li>Applications that need to minimize correlated failures</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.image("https://d1.awsstatic.com/product-marketing/EC2/Spread%20placement%20group.1c74c4a77af093c607e319aa3fc3e18860c9871e.PNG", use_container_width=True)
    
    with col3:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Partition Placement Group</h4>
            <p><strong>Description:</strong></p>
            <ul>
                <li>Instances grouped into logical partitions</li>
                <li>Each partition on distinct racks</li>
                <li>Partitions within a group don't share hardware</li>
            </ul>
            <p><strong>Best For:</strong></p>
            <ul>
                <li>Large distributed and replicated workloads</li>
                <li>Hadoop, Cassandra, and Kafka clusters</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.image("https://d1.awsstatic.com/product-marketing/EC2/Partition%20placement%20group.0dc869e45dedab443a6706764c71053c5cc9ceff.PNG", use_container_width=True)
    
    st.markdown("""
    <div class="aws-info-card">
        <h4>Key Takeaway</h4>
        <p>Choose your placement group strategy based on your application needs:</p>
        <ul>
            <li><strong>Cluster:</strong> For highest network performance and throughput</li>
            <li><strong>Spread:</strong> For highest availability and reducing correlated failures</li>
            <li><strong>Partition:</strong> For distributed applications that need to control partition placement</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Function for EC2 AMIs and Instance Metadata page
def amis_metadata_page():
    st.title("EC2 AMIs and Instance Metadata")
    
    st.header("Amazon Machine Images (AMI)")
    st.markdown("""
    <div class="aws-card">
        <p>An Amazon Machine Image (AMI) provides the information required to launch an EC2 instance.</p>
        <h4>AMI Types:</h4>
        <ul>
            <li><strong>Amazon EBS-backed AMI:</strong> Root device is an EBS volume created from an EBS snapshot</li>
            <li><strong>Instance store-backed AMI:</strong> Root device is an instance store volume created from a template in S3</li>
        </ul>
        <h4>What an AMI includes:</h4>
        <ul>
            <li>One or more EBS snapshots (or instance store template)</li>
            <li>Launch permissions controlling which AWS accounts can use the AMI</li>
            <li>Block device mapping that specifies volumes to attach when launched</li>
        </ul>
        <h4>Common AMI sources:</h4>
        <ul>
            <li>AWS-provided AMIs</li>
            <li>AWS Marketplace AMIs</li>
            <li>Community AMIs</li>
            <li>Custom AMIs you create</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("EC2 Instance Metadata")
    st.markdown("""
    <div class="aws-card">
        <p>Instance metadata is data about your instance that you can use to configure or manage the running instance.</p>
        <h4>Key Features:</h4>
        <ul>
            <li>Available from within the running instance</li>
            <li>No need to use AWS console or CLI for basic information</li>
            <li>Useful for writing scripts that run on the instance</li>
            <li>Accessed via a special endpoint: <code>http://169.254.169.254/latest/meta-data/</code></li>
        </ul>
        <h4>Common metadata categories:</h4>
        <ul>
            <li>Instance ID and type</li>
            <li>Hostname</li>
            <li>Local IP address</li>
            <li>IAM role information</li>
            <li>Security groups</li>
        </ul>
        <h4>Instance User Data:</h4>
        <ul>
            <li>Custom data provided at instance launch</li>
            <li>Used for configuration scripts that run on startup</li>
            <li>Limited to 16 KB before base64 encoding</li>
            <li>Accessed via <code>http://169.254.169.254/latest/user-data/</code></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="aws-info-card">
        <h4>Security Best Practice</h4>
        <p>With IMDSv2, you should use token-based requests to access
        instance metadata. This is more secure than the earlier IMDSv1 method which allows direct 
        requests. Always configure your EC2 instances to use IMDSv2 whenever possible.</p>
    </div>
    """, unsafe_allow_html=True)

# Function for KMS & EBS Encryption page
def kms_ebs_page():
    st.title("Amazon KMS & EBS Encryption")
    
    try:
        image = load_image_from_url(aws_images["kms"])
        if image:
            st.image(image, width=700)
    except:
        st.warning("Image could not be displayed")
    
    st.header("AWS Key Management Service (KMS)")
    st.markdown("""
    <div class="aws-card">
        <p>AWS KMS is a managed service that makes it easy to create and control cryptographic keys used to protect your data.</p>
        <h4>Key Features:</h4>
        <ul>
            <li>Secure and resilient service using FIPS 140-2 validated hardware security modules</li>
            <li>Centralized management of encryption keys</li>
            <li>Integrated with many AWS services</li>
            <li>Comprehensive logging and auditing via CloudTrail</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Types of KMS Keys")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Customer Managed Keys</h4>
            <ul>
                <li>Created and controlled by customers</li>
                <li>Full control over key policies and lifecycle</li>
                <li>All requests logged to CloudTrail</li>
                <li>Ideal for granular control</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>AWS Managed Keys</h4>
            <ul>
                <li>Created and managed by AWS</li>
                <li>Used for specific AWS services</li>
                <li>Cannot be modified by customers</li>
                <li>Key policies managed by AWS</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("Amazon EBS Encryption")
    st.markdown("""
    <div class="aws-card">
        <p>Amazon EBS encryption offers a simple encryption solution for your EBS resources.</p>
        <h4>When you create an encrypted EBS volume, the following is encrypted:</h4>
        <ul>
            <li>Data at rest inside the volume</li>
            <li>All data in transit between the volume and the instance</li>
            <li>All snapshots created from the volume</li>
            <li>All volumes created from those snapshots</li>
        </ul>
        <h4>Key Features:</h4>
        <ul>
            <li>Uses AES-256 encryption algorithm</li>
            <li>Encryption operations occur on EC2 host servers</li>
            <li>Minimal impact on performance</li>
            <li>Integrated with AWS KMS for key management</li>
        </ul>
        <h4>How It Works:</h4>
        <ol>
            <li>EBS encrypts your volume with a data key using AES-256</li>
            <li>The data key is generated by AWS KMS</li>
            <li>The data key is encrypted by your specified KMS key</li>
            <li>The encrypted data key is stored with your volume information</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="aws-info-card">
        <h4>Best Practice</h4>
        <p>Consider enabling encryption by default for all new EBS volumes and 
        snapshots in your account. This ensures all future storage resources are protected with minimal 
        operational overhead.</p>
    </div>
    """, unsafe_allow_html=True)

# Function for Security page
def security_page():
    st.title("AWS Security")
    
    try:
        image = load_image_from_url(aws_images["security"])
        if image:
            st.image(image, width=700)
    except:
        st.warning("Image could not be displayed")
    
    st.header("Amazon CloudTrail")
    st.markdown("""
    <div class="aws-card">
        <p>CloudTrail logs, monitors, and retains account activity related to actions across your AWS infrastructure.</p>
        <h4>Key Features:</h4>
        <ul>
            <li>Records user activity and API calls across your AWS account</li>
            <li>Enables auditing, security monitoring, and operational troubleshooting</li>
            <li>Logs can be stored in S3, CloudWatch Logs, or analyzed with Athena</li>
            <li>Helps prove compliance with regulatory standards</li>
        </ul>
        <h4>What are trails?</h4>
        <p>A trail is a configuration that enables delivery of CloudTrail events to an S3 bucket, CloudWatch Logs, and EventBridge.
        You can filter events, encrypt log files with KMS, and set up SNS notifications for log delivery.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("AWS WAF (Web Application Firewall)")
    st.markdown("""
    <div class="aws-card">
        <p>AWS WAF is a web application firewall that protects web applications from common web exploits.</p>
        <h4>Key Features:</h4>
        <ul>
            <li>Configure rules to allow, block, or monitor web requests</li>
            <li>Protects against common attacks like SQL injection and XSS</li>
            <li>Integrates with CloudFront, Application Load Balancer, API Gateway, and AppSync</li>
            <li>When used with CloudFront, rules run in all AWS Edge Locations globally</li>
        </ul>
        <h4>Protection Capabilities:</h4>
        <ul>
            <li>Block specific IP addresses</li>
            <li>Block specific countries</li>
            <li>Block specific request patterns</li>
            <li>Rate limiting to prevent DDoS attacks</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>AWS Shield</h4>
            <p>AWS Shield is a managed DDoS protection service that safeguards applications on AWS.</p>
            <p><strong>Shield Standard (Free):</strong></p>
            <ul>
                <li>Automatically enabled for all AWS customers</li>
                <li>Protects against common layer 3/4 attacks</li>
                <li>Supports high availability of applications</li>
            </ul>
            <p><strong>Shield Advanced (Paid):</strong></p>
            <ul>
                <li>Enhanced protection for EC2, ELB, CloudFront, Global Accelerator, and Route 53</li>
                <li>Real-time monitoring and notifications</li>
                <li>24/7 access to the Shield Response Team (with Business/Enterprise Support)</li>
                <li>DDoS cost protection</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>AWS Firewall Manager</h4>
            <p>Centrally configure and manage firewall rules across accounts and applications.</p>
            <h5>Key Features:</h5>
            <ul>
                <li>Set up protections once, automatically applied across accounts</li>
                <li>Protects resources across accounts in AWS Organizations</li>
                <li>Automatically protects new resources as they're added</li>
                <li>Supports multiple security services:
                    <ul>
                        <li>AWS WAF</li>
                        <li>AWS Shield Advanced</li>
                        <li>Security Groups</li>
                        <li>AWS Network Firewall</li>
                        <li>Route 53 Resolver DNS Firewall</li>
                    </ul>
                </li>
            </ul>
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
        "Caching & File Servers", 
        "Database Services", 
        "EC2 Basics", 
        "Placement Groups", 
        "AMIs & Metadata", 
        "KMS & Encryption",
        "Security"
    ])
    
    topic_keys = ["caching", "database", "ec2", "placement_groups", "amis_metadata", "kms", "security"]
    
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
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "🏠 Home",
    "💾 Caching & File Servers",
    "🗄️ Database Services",
    "🖥️ EC2 Basics",
    "📋 Placement Groups",
    "💿 AMIs & Metadata",
    "🔐 KMS & Encryption",
    "🛡️ Security",
    "📝 Knowledge Checks"
])

# Content for each tab
with tab1:
    home_page()

with tab2:
    caching_page()

with tab3:
    database_page()

with tab4:
    ec2_page()

with tab5:
    placement_groups_page()

with tab6:
    amis_metadata_page()

with tab7:
    kms_ebs_page()

with tab8:
    security_page()
    
with tab9:
    knowledge_checks_page()

# Footer
st.markdown("""
<div class="footer">
    © 2025 AWS Partner Certification Readiness. This application is designed to help you prepare for the AWS Solutions Architect - Associate certification.
</div>
""", unsafe_allow_html=True)
