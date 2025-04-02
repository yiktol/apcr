
import streamlit as st
import base64
from PIL import Image
import os
import json
import random
from io import BytesIO
import requests

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

# Function to display quiz
def display_quiz(topic):
    if topic in quiz_data and quiz_data[topic]:
        st.subheader("💡 Knowledge Check")
        
        for i, quiz in enumerate(quiz_data[topic]):
            question = quiz["question"]
            options = quiz["options"]
            correct_answer = quiz["answer"]
            
            st.write(f"**Scenario {i+1}:** {question}")
            
            # Create a unique key for each radio button
            key = f"{topic}_quiz_{i}"
            
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
                if selected_answer == correct_answer:
                    st.success(f"✅ Correct! {correct_answer} is the right answer.")
                elif selected_answer is None:
                    st.warning("Please select an answer first.")
                else:
                    st.error(f"❌ Incorrect. The correct answer is {correct_answer}.")
            
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
        st.header("Content Review - Session 3")
        st.markdown("""
        Welcome to the AWS Partner Certification Readiness program. This interactive guide will help you prepare 
        for the Solutions Architect - Associate certification. Navigate through the topics using the sidebar menu.
        
        Each section contains key concepts, important takeaways, and interactive quizzes to reinforce your learning.
        
        **Topics covered:**
        - AWS Caching & File Servers
        - AWS Database Offerings
        - AWS Elastic Compute Cloud (EC2)
        - EC2 Placement Groups
        - EC2 AMIs and Instance Metadata
        - Amazon KMS & EBS Encryption
        - AWS Security
        """)
    
    st.info("""
    **Certification Preparation Tip:** Practice hands-on with the services covered in this guide. 
    The AWS Solutions Architect - Associate exam focuses on practical knowledge of AWS services 
    and how they can be used together to design resilient, cost-effective solutions.
    """)

# Function for AWS Caching & File Servers page
def caching_page():
    st.title("AWS Caching & File Servers")
    
    try:
        st.image(aws_images["caching"], width=600)
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
        st.subheader("Redis")
        st.markdown("""
        - Advanced data structures (lists, sets, sorted sets, hashes)
        - Replication and high availability
        - Snapshots for backup and recovery
        - Transactions and Pub/Sub capabilities
        - **Use Cases**: Gaming leaderboards, chat/messaging, real-time analytics
        """)
    
    with col2:
        st.subheader("Memcached")
        st.markdown("""
        - Simple design focused on simplicity
        - Multi-threaded architecture
        - Data partitioning
        - **Use Cases**: Caching database query results, session caching, page caching
        """)
    
    st.divider()
    
    st.header("Amazon Elastic File System (EFS)")
    st.markdown("""
    A simple, serverless, set-and-forget elastic file system for Linux-based workloads.

    **Key Features:**
    - Fully managed Network File System (NFS) for Linux
    - Highly available and durable (11 9's of durability)
    - Automatically scales as files are added/removed
    - Mount to Linux EC2 instances for shared file storage

    **Storage Classes:**
    - EFS Standard
    - EFS Standard-Infrequent Access
    - One Zone Storage
    - One Zone-Infrequent Access
    
    **Use Case:** Modern application development with serverless architecture, allowing containerized or serverless applications to share and persist data.
    """)
    
    st.divider()
    
    st.header("Amazon FSx for Windows File Server")
    st.markdown("""
    Fully managed file storage built on Windows Server.

    **Key Features:**
    - Fully managed, highly reliable Windows file servers
    - Uses Server Message Block (SMB) protocol
    - Backed by a fully native Windows file system

    **Use Cases:**
    - Migrate Windows file servers to AWS
    - Run SQL Server workloads without SQL enterprise licensing
    """)
    
    display_quiz("caching")

# Function for AWS Database Offerings page
def database_page():
    st.title("AWS Database Offerings")
    
    try:
        st.image(aws_images["database"], width=600)
    except:
        st.warning("Image could not be displayed")
    
    st.header("Purpose-built Database Services")
    
    st.markdown("""
    AWS provides purpose-built database services designed for specific workloads and use cases:
    
    | Database Category | Key Service | Best For |
    |------------------|-------------|----------|
    | Relational | Amazon RDS, Aurora | Structured data, transactions, complex queries |
    | Key-Value | DynamoDB | High-throughput, low-latency applications |
    | Document | DocumentDB | JSON document storage and queries |
    | In-Memory | ElastiCache | Microsecond latency, caching |
    | Graph | Neptune | Highly connected data, relationships |
    | Time Series | Timestream | IoT data, metrics, analytics over time |
    | Ledger | QLDB | Immutable, verifiable transaction logs |
    | Wide Column | Keyspaces | High-speed data processing |
    """)
    
    st.divider()
    
    st.header("Amazon RDS (Relational Database Service)")
    st.markdown("""
    Set up, operate, and scale a managed relational database with just a few clicks.

    **Key Features:**
    - Available and durable (automated Multi-AZ replication, backups)
    - Easy to administer (automated patching and maintenance)
    - Scalable (compute and storage can scale independently)
    - Secure (encryption at rest and in transit)

    **Supported Engines:**
    - MySQL
    - PostgreSQL
    - MariaDB
    - Oracle
    - SQL Server
    - Amazon Aurora

    **Important Features:**
    - Multi-AZ deployments for high availability
    - Read replicas for performance scaling
    """)
    
    st.divider()
    
    st.header("Amazon Aurora")
    st.markdown("""
    MySQL and PostgreSQL-compatible relational database built for the cloud.

    **Key Features:**
    - 5x throughput of MySQL, 3x throughput of PostgreSQL
    - Fault-tolerant, self-healing storage
    - Six copies of data across three Availability Zones
    - Continuous backup to Amazon S3
    - Up to 15 low-latency read replicas

    **Aurora Global Databases:**
    - Span multiple AWS Regions
    - Global reads with local latency
    - Fast recovery from region-wide outages
    - Replication with typically under 1 second latency
    """)
    
    st.divider()
    
    st.header("Amazon DynamoDB")
    st.markdown("""
    Fast and flexible NoSQL database service for any scale.

    **Key Features:**
    - Fully managed key-value and document database
    - Single-digit millisecond performance at any scale
    - Can handle more than 10 trillion requests per day
    - Supports both eventually consistent and strongly consistent reads
    
    **DynamoDB Accelerator (DAX):**
    - Fully managed in-memory cache for DynamoDB
    - Microsecond latency (10x performance improvement)
    - Compatible with existing DynamoDB API calls
    - Scales to millions of requests per second
    """)
    
    display_quiz("database")

# Function for EC2 page
def ec2_page():
    st.title("AWS Elastic Compute Cloud (EC2)")
    
    try:
        st.image(aws_images["ec2"], width=600)
    except:
        st.warning("Image could not be displayed")
    
    st.header("Amazon EC2 Overview")
    st.markdown("""
    Amazon EC2 provides secure, resizable compute capacity in the AWS Cloud.

    **Key Features:**
    - Increase or decrease capacity within minutes (99.99% availability per region)
    - Complete control over computing resources
    - Multiple security features and standards
    - Various migration tools and paths to get started

    **EC2 Auto Scaling:**
    - Add or remove compute capacity to meet changes in demand
    - Scale based on schedules or dynamic metrics
    - Maintain application availability during demand spikes
    
    **AWS Auto Scaling:**
    - Monitors and automatically adjusts capacity for various AWS resources
    - Predicts future traffic patterns, including regular spikes
    - Works with EC2 Auto Scaling to manage dependent services
    """)
    
    st.divider()
    
    st.header("EC2 Billing Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("On-Demand Instances")
        st.markdown("""
        - Pay by the second with no commitments
        - Ideal for short-term, irregular workloads
        - Full control over instance lifecycle
        """)
        
        st.subheader("Spot Instances")
        st.markdown("""
        - Use unused EC2 capacity at up to 90% discount
        - Ideal for flexible, fault-tolerant workloads
        - Instances can be interrupted with 2-minute notification
        """)
    
    with col2:
        st.subheader("Savings Plans")
        st.markdown("""
        - Lower prices for usage commitments (1 or 3 years)
        - Flexible across instance families, sizes, OS, regions
        - Available for EC2, Lambda, and Fargate
        """)
        
        st.subheader("Dedicated Hosts")
        st.markdown("""
        - Physical servers dedicated to your use
        - Allow BYOL (Bring Your Own License)
        - Address compliance requirements
        """)
    
    st.divider()
    
    st.header("EC2 Instance Types")
    st.markdown("""
    | Instance Type | Features | Use Cases |
    |--------------|----------|-----------|
    | **General Purpose** | Balanced compute, memory, networking | Web servers, development environments, small databases |
    | **Compute Optimized** | High-performance processors | Batch processing, HPC, gaming servers, scientific modeling |
    | **Memory Optimized** | Fast performance for memory-intensive workloads | High-performance databases, real-time big data analytics |
    | **Storage Optimized** | Low latency, high IOPS | NoSQL databases, data warehousing, distributed file systems |
    | **Accelerated Computing** | Hardware accelerators for data processing | ML/AI, graphics workloads, game streaming |
    """)
    
    display_quiz("ec2")

# Function for EC2 Placement Groups page
def placement_groups_page():
    st.title("EC2 Placement Groups")
    st.markdown("""
    Placement groups influence how EC2 instances are placed on underlying hardware, affecting performance, availability, and fault tolerance.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Cluster Placement Group")
        st.markdown("""
        **Description:**
        - Instances packed close together inside a single AZ
        - Low network latency, high throughput network performance
        
        **Best For:**
        - High-performance computing (HPC)
        - Applications requiring low-latency node-to-node communication
        """)
        
        st.image("https://d1.awsstatic.com/product-marketing/EC2/Cluster%20placement%20group.b8d5681f46e1825c2a9336ef2ab3adc64d382db5.PNG", use_column_width=True)
    
    with col2:
        st.subheader("Spread Placement Group")
        st.markdown("""
        **Description:**
        - Instances placed on distinct underlying hardware
        - Each instance on separate racks with independent power/network
        
        **Best For:**
        - Critical applications requiring maximum availability
        - Applications that need to minimize correlated failures
        """)
        
        st.image("https://d1.awsstatic.com/product-marketing/EC2/Spread%20placement%20group.1c74c4a77af093c607e319aa3fc3e18860c9871e.PNG", use_column_width=True)
    
    with col3:
        st.subheader("Partition Placement Group")
        st.markdown("""
        **Description:**
        - Instances grouped into logical partitions
        - Each partition on distinct racks
        - Partitions within a group don't share hardware
        
        **Best For:**
        - Large distributed and replicated workloads
        - Hadoop, Cassandra, and Kafka clusters
        """)
        
        st.image("https://d1.awsstatic.com/product-marketing/EC2/Partition%20placement%20group.0dc869e45dedab443a6706764c71053c5cc9ceff.PNG", use_column_width=True)
    
    st.info("""
    **Key Takeaway**: Choose your placement group strategy based on your application needs:
    - **Cluster**: For highest network performance and throughput
    - **Spread**: For highest availability and reducing correlated failures
    - **Partition**: For distributed applications that need to control partition placement
    """)
    
    display_quiz("placement_groups")

# Function for EC2 AMIs and Instance Metadata page
def amis_metadata_page():
    st.title("EC2 AMIs and Instance Metadata")
    
    st.header("Amazon Machine Images (AMI)")
    st.markdown("""
    An Amazon Machine Image (AMI) provides the information required to launch an EC2 instance.

    **AMI Types:**
    - **Amazon EBS-backed AMI**: Root device is an EBS volume created from an EBS snapshot
    - **Instance store-backed AMI**: Root device is an instance store volume created from a template in S3

    **What an AMI includes:**
    - One or more EBS snapshots (or instance store template)
    - Launch permissions controlling which AWS accounts can use the AMI
    - Block device mapping that specifies volumes to attach when launched

    **Common AMI sources:**
    - AWS-provided AMIs
    - AWS Marketplace AMIs
    - Community AMIs
    - Custom AMIs you create
    """)
    
    st.divider()
    
    st.header("EC2 Instance Metadata")
    st.markdown("""
    Instance metadata is data about your instance that you can use to configure or manage the running instance.

    **Key Features:**
    - Available from within the running instance
    - No need to use AWS console or CLI for basic information
    - Useful for writing scripts that run on the instance
    - Accessed via a special endpoint: `http://169.254.169.254/latest/meta-data/`

    **Common metadata categories:**
    - Instance ID and type
    - Hostname
    - Local IP address
    - IAM role information
    - Security groups

    **Instance User Data:**
    - Custom data provided at instance launch
    - Used for configuration scripts that run on startup
    - Limited to 16 KB before base64 encoding
    - Accessed via `http://169.254.169.254/latest/user-data/`
    """)
    
    st.info("""
    **Security Best Practice**: With IMDSv2, you should use token-based requests to access
    instance metadata. This is more secure than the earlier IMDSv1 method which allows direct 
    requests. Always configure your EC2 instances to use IMDSv2 whenever possible.
    """)
    
    display_quiz("amis_metadata")

# Function for KMS & EBS Encryption page
def kms_ebs_page():
    st.title("Amazon KMS & EBS Encryption")
    
    try:
        st.image(aws_images["kms"], width=700)
    except:
        st.warning("Image could not be displayed")
    
    st.header("AWS Key Management Service (KMS)")
    st.markdown("""
    AWS KMS is a managed service that makes it easy to create and control cryptographic keys used to protect your data.

    **Key Features:**
    - Secure and resilient service using FIPS 140-2 validated hardware security modules
    - Centralized management of encryption keys
    - Integrated with many AWS services
    - Comprehensive logging and auditing via CloudTrail

    **Types of KMS Keys:**
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Customer Managed Keys")
        st.markdown("""
        - Created and controlled by customers
        - Full control over key policies and lifecycle
        - All requests logged to CloudTrail
        - Ideal for granular control
        """)
    
    with col2:
        st.subheader("AWS Managed Keys")
        st.markdown("""
        - Created and managed by AWS
        - Used for specific AWS services
        - Cannot be modified by customers
        - Key policies managed by AWS
        """)
    
    st.divider()
    
    st.header("Amazon EBS Encryption")
    st.markdown("""
    Amazon EBS encryption offers a simple encryption solution for your EBS resources.

    **When you create an encrypted EBS volume, the following is encrypted:**
    - Data at rest inside the volume
    - All data in transit between the volume and the instance
    - All snapshots created from the volume
    - All volumes created from those snapshots

    **Key Features:**
    - Uses AES-256 encryption algorithm
    - Encryption operations occur on EC2 host servers
    - Minimal impact on performance
    - Integrated with AWS KMS for key management
    
    **How It Works:**
    1. EBS encrypts your volume with a data key using AES-256
    2. The data key is generated by AWS KMS 
    3. The data key is encrypted by your specified KMS key
    4. The encrypted data key is stored with your volume information
    """)
    
    st.info("""
    **Best Practice**: Consider enabling encryption by default for all new EBS volumes and 
    snapshots in your account. This ensures all future storage resources are protected with minimal 
    operational overhead.
    """)
    
    display_quiz("kms")

# Function for Security page
def security_page():
    st.title("AWS Security")
    
    try:
        st.image(aws_images["security"], width=700)
    except:
        st.warning("Image could not be displayed")
    
    st.header("Amazon CloudTrail")
    st.markdown("""
    CloudTrail logs, monitors, and retains account activity related to actions across your AWS infrastructure.

    **Key Features:**
    - Records user activity and API calls across your AWS account
    - Enables auditing, security monitoring, and operational troubleshooting
    - Logs can be stored in S3, CloudWatch Logs, or analyzed with Athena
    - Helps prove compliance with regulatory standards
    
    **What are trails?**
    
    A trail is a configuration that enables delivery of CloudTrail events to an S3 bucket, CloudWatch Logs, and EventBridge.
    You can filter events, encrypt log files with KMS, and set up SNS notifications for log delivery.
    """)
    
    st.divider()
    
    st.header("AWS WAF (Web Application Firewall)")
    st.markdown("""
    AWS WAF is a web application firewall that protects web applications from common web exploits.

    **Key Features:**
    - Configure rules to allow, block, or monitor web requests
    - Protects against common attacks like SQL injection and XSS
    - Integrates with CloudFront, Application Load Balancer, API Gateway, and AppSync
    - When used with CloudFront, rules run in all AWS Edge Locations globally
    
    **Protection Capabilities:**
    - Block specific IP addresses
    - Block specific countries
    - Block specific request patterns
    - Rate limiting to prevent DDoS attacks
    """)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("AWS Shield")
        st.markdown("""
        AWS Shield is a managed DDoS protection service that safeguards applications on AWS.

        **Shield Standard (Free):**
        - Automatically enabled for all AWS customers
        - Protects against common layer 3/4 attacks
        - Supports high availability of applications

        **Shield Advanced (Paid):**
        - Enhanced protection for EC2, ELB, CloudFront, Global Accelerator, and Route 53
        - Real-time monitoring and notifications
        - 24/7 access to the Shield Response Team (with Business/Enterprise Support)
        - DDoS cost protection
        """)
    
    with col2:
        st.header("AWS Firewall Manager")
        st.markdown("""
        Centrally configure and manage firewall rules across accounts and applications.

        **Key Features:**
        - Set up protections once, automatically applied across accounts
        - Protects resources across accounts in AWS Organizations
        - Automatically protects new resources as they're added
        - Supports multiple security services:
          - AWS WAF
          - AWS Shield Advanced
          - Security Groups
          - AWS Network Firewall
          - Route 53 Resolver DNS Firewall
        """)
    
    display_quiz("security")

# Sidebar menu
st.sidebar.title("AWS Solutions Architect")
st.sidebar.image("https://a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_1200x630.png", width=200)

menu = st.sidebar.radio(
    "Navigation",
    ["Home", 
     "AWS Caching & File Servers", 
     "AWS Database Offerings", 
     "EC2 Overview", 
     "EC2 Placement Groups", 
     "EC2 AMIs & Metadata", 
     "KMS & EBS Encryption",
     "AWS Security"]
)

# Display selected page
if menu == "Home":
    home_page()
elif menu == "AWS Caching & File Servers":
    caching_page()
elif menu == "AWS Database Offerings":
    database_page()
elif menu == "EC2 Overview":
    ec2_page()
elif menu == "EC2 Placement Groups":
    placement_groups_page()
elif menu == "EC2 AMIs & Metadata":
    amis_metadata_page()
elif menu == "KMS & EBS Encryption":
    kms_ebs_page()
elif menu == "AWS Security":
    security_page()

# Footer
st.sidebar.divider()
st.sidebar.markdown("© 2025 AWS Partner Certification Readiness")
st.sidebar.info("This application is designed to help you prepare for the AWS Solutions Architect - Associate certification.")
