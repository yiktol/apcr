
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

# Initialize session state
def init_session_state():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    # Initialize tracking for quizzes
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
    "global_infrastructure": "https://d1.awsstatic.com/global-infrastructure/maps/Global-Infrastructure-Map_1.20.2022.b2f0ad79c1230cb97f60bc904494f122758d24f1.png",
    "regions": "https://d1.awsstatic.com/diagrams/availability-zones_diagram-updated.40f601e2b6d81573dc88483c1fc2553ad0a1a25d.png",
    "cloudfront": "https://d1.awsstatic.com/product-marketing/CloudFront/CloudFront-Diagram.c3ef67291cc5a3929db2934739ae5e7ced7a9b25.png",
    "iam": "https://d1.awsstatic.com/product-marketing/IAM/iam-how-it-works-diagram.cce4e33da82c06b42d032684ef0b39615b8855c6.png",
    "iam_policies": "https://d1.awsstatic.com/security-center/IAM-policy-evaluation.648e2924e1f684ae3d759e940980e8adf7fa52ca.png",
    "s3": "https://d1.awsstatic.com/s3-pdp-redesign/product-page-diagram_Amazon-S3_HIW.cf4c2bd7aa02f1fe77be8aa120393993e08ac86d.png",
    "organizations": "https://d1.awsstatic.com/product-marketing/Organizations/Organizations-Diagram.f29c33e7758f599e9a362b644892558c67f5e60f.png",
    "sts": "https://d1.awsstatic.com/security-center/Security-STS.58d8dc26b43b2d5e5a3312afd45d02869a1e7577.png",
}

# Scenario-based quiz questions (using from the original code)
quiz_data = {
    "global_infrastructure": [
        {
            "question": "A financial services company is launching a new global application that requires low latency access for users across North America, Europe, and Asia. The application's data must comply with regional data sovereignty laws. Which AWS Global Infrastructure deployment strategy should they use?",
            "options": [
                "Deploy the application in a single AWS Region with the most central geographic location and use Route 53 for routing",
                "Deploy the application in AWS Regions in each continent and use Amazon CloudFront as the content delivery network",
                "Deploy the application in every available AWS Region and use AWS Global Accelerator to route traffic",
                "Deploy the application in a single AWS Region with multiple Availability Zones and use Edge Locations for caching",
                "Use AWS Outposts to deploy the application in on-premises data centers in each country"
            ],
            "answer": "Deploy the application in AWS Regions in each continent and use Amazon CloudFront as the content delivery network"
        },
        {
            "question": "A global e-commerce company is redesigning their application architecture to improve fault tolerance. The architecture currently runs in a single Availability Zone in the us-east-1 Region. Which of the following designs would provide the HIGHEST level of fault tolerance while maintaining performance?",
            "options": [
                "Migrate all resources to multiple Edge Locations worldwide",
                "Deploy resources across multiple Availability Zones in us-east-1",
                "Deploy resources in multiple AWS Regions with cross-region replication",
                "Deploy resources in a single Availability Zone in each of multiple AWS Regions",
                "Deploy resources using AWS Outposts in multiple on-premises data centers"
            ],
            "answer": "Deploy resources across multiple Availability Zones in us-east-1"
        },
        {
            "question": "A healthcare company must ensure their patient data processing application complies with local regulations requiring data to remain within the country's borders. The application will serve users across Asia, Europe, and North America. Which deployment strategy meets these requirements while optimizing for performance?",
            "options": [
                "Use a single Global AWS Region with multiple Edge Locations in each country",
                "Deploy the application in a Local Zone in each country",
                "Deploy separate application instances in AWS Regions within each required country and use Route 53 geolocation routing",
                "Use AWS Outposts to deploy infrastructure in local data centers in each country",
                "Deploy the application in a single Region and use AWS Wavelength for country-specific access"
            ],
            "answer": "Deploy separate application instances in AWS Regions within each required country and use Route 53 geolocation routing"
        },
        {
            "question": "An online gaming company is designing their new game's infrastructure to minimize latency for players worldwide. The game requires real-time interactions between players, but player data can be partitioned by geographic region. Which architectural approach best meets these requirements?",
            "options": [
                "Deploy game servers in every available AWS Region and use Global Accelerator to route players to the closest region",
                "Deploy game servers in a single centrally-located Region and use CloudFront to reduce latency",
                "Use AWS Wavelength to deploy game servers at the edge of 5G networks in major cities",
                "Deploy game servers in select Regions by continent and use Route 53 latency-based routing with Regional data partitioning",
                "Deploy all game infrastructure in the us-east-1 Region with multiple Availability Zones"
            ],
            "answer": "Deploy game servers in select Regions by continent and use Route 53 latency-based routing with Regional data partitioning"
        },
        {
            "question": "A company running a critical application wants to design for high availability while minimizing costs. The application consists of web, application, and database tiers. Which architecture provides the best balance of high availability and cost-efficiency?",
            "options": [
                "Deploy the entire application stack across multiple AWS Regions",
                "Deploy the application across multiple Availability Zones in a single Region",
                "Deploy the web tier in Edge Locations, the application tier in a single AZ, and the database in another AZ",
                "Deploy the web and application tiers in one AZ and the database tier with Multi-AZ configuration",
                "Deploy the entire application in a single Availability Zone with redundant instances"
            ],
            "answer": "Deploy the application across multiple Availability Zones in a single Region"
        }
    ],
    "cloudfront": [
        {
            "question": "An international news website experiences traffic spikes when breaking news occurs. The site consists of static HTML, CSS, JavaScript files, and dynamic API calls to fetch personalized content. Users have reported slow page loads during high-traffic events. Which CloudFront configuration would BEST improve performance while managing costs?",
            "options": [
                "Configure CloudFront with S3 Origin for all content and set a TTL of 24 hours for all objects",
                "Configure CloudFront with both S3 and API Gateway origins, cache static content for 24 hours, and use Lambda@Edge to personalize content",
                "Configure CloudFront with both S3 and API Gateway origins, with cache behaviors that apply different caching policies for static assets versus API calls",
                "Configure CloudFront with a custom origin pointing to an Application Load Balancer and disable caching entirely",
                "Use S3 Transfer Acceleration instead of CloudFront to improve global content delivery"
            ],
            "answer": "Configure CloudFront with both S3 and API Gateway origins, with cache behaviors that apply different caching policies for static assets versus API calls"
        },
        {
            "question": "A company hosts video content that should only be accessible to paying subscribers. They want to distribute this content globally using CloudFront while preventing unauthorized access. Which combination of features should they implement?",
            "options": [
                "Enable CloudFront public access and implement client-side encryption in the video player",
                "Store videos in a public S3 bucket and use CloudFront with no signed URLs",
                "Store videos in a private S3 bucket, use Origin Access Identity with CloudFront, and implement signed URLs with appropriate expiration times",
                "Use Lambda@Edge to authenticate all users at the CloudFront edge location before serving content",
                "Configure CloudFront Field-Level Encryption to encrypt the video content for each subscriber"
            ],
            "answer": "Store videos in a private S3 bucket, use Origin Access Identity with CloudFront, and implement signed URLs with appropriate expiration times"
        },
        {
            "question": "A global e-commerce platform needs to optimize their product image delivery to mobile and desktop users worldwide. The images are stored in Amazon S3. During peak shopping seasons, they experience significant load on their origin servers. Which CloudFront configuration would most effectively reduce origin load while ensuring users receive optimized images?",
            "options": [
                "Use CloudFront with default settings and configure S3 Transfer Acceleration",
                "Configure CloudFront with Origin Shield in a central region, implement cache behaviors with high TTLs, and use Lambda@Edge to transform images based on the device type",
                "Set up multiple CloudFront distributions for different regions and implement separate origins for mobile and desktop images",
                "Use CloudFront Continuous Deployment to test different cache settings during peak seasons",
                "Implement S3 Cross-Region Replication instead of CloudFront to distribute images globally"
            ],
            "answer": "Configure CloudFront with Origin Shield in a central region, implement cache behaviors with high TTLs, and use Lambda@Edge to transform images based on the device type"
        },
        {
            "question": "A company has a web application that serves users globally. They want to implement a content delivery strategy that optimizes for both static and dynamic content while providing protection against DDoS attacks. Which architecture should they implement?",
            "options": [
                "CloudFront distribution with AWS Shield Advanced, WAF for security, and separate cache behaviors for static and dynamic content",
                "Multiple regional load balancers with Shield Standard protection and no CDN",
                "Global Accelerator with Shield Advanced but no content caching",
                "CloudFront with Regional Edge Caches disabled and Route 53 latency-based routing",
                "Direct S3 access with bucket policies to restrict access by geography"
            ],
            "answer": "CloudFront distribution with AWS Shield Advanced, WAF for security, and separate cache behaviors for static and dynamic content"
        },
        {
            "question": "A media streaming service needs to deliver live video content to viewers worldwide with minimal latency. They also need to convert the original high-resolution stream into multiple formats and resolutions. Which AWS services and CloudFront configuration would best meet these requirements?",
            "options": [
                "Store pre-encoded videos in S3 and use standard CloudFront distribution",
                "Use MediaLive to encode streams, MediaStore as origin, and CloudFront with real-time logging and minimal TTL settings",
                "Use EC2 instances to transcode video and CloudFront with regional edge caches disabled",
                "Configure CloudFront with Lambda@Edge to transcode videos on-demand at the edge",
                "Use MediaPackage for format conversion, MediaStore as origin, and CloudFront with field-level encryption"
            ],
            "answer": "Use MediaLive to encode streams, MediaStore as origin, and CloudFront with real-time logging and minimal TTL settings"
        }
    ],
    "iam": [
        {
            "question": "A large enterprise is implementing a new AWS environment and needs to design their IAM strategy. They have multiple departments with different access requirements, and security audit requirements mandate separation of duties and least privilege access. Which approach should they take?",
            "options": [
                "Create a single AWS account with IAM groups for each department and assign users to appropriate groups",
                "Create multiple AWS accounts organized into an AWS Organization with OUs by department, and implement SCPs for broad guardrails along with IAM policies for fine-grained control",
                "Create a single AWS account and give all developers PowerUser access to simplify administration",
                "Create one AWS account per user to ensure complete isolation",
                "Implement IAM roles only with no IAM users to force federation through their corporate identity provider"
            ],
            "answer": "Create multiple AWS accounts organized into an AWS Organization with OUs by department, and implement SCPs for broad guardrails along with IAM policies for fine-grained control"
        },
        {
            "question": "A company wants to allow their mobile application to directly upload images to an S3 bucket without exposing AWS credentials in the application code. The solution must maintain security and scale to millions of users. Which approach should they implement?",
            "options": [
                "Create an IAM user for the mobile app and embed access keys in the application code",
                "Use Amazon Cognito Identity Pools to provide temporary credentials through IAM roles to unauthenticated users with limited permissions to upload to specific S3 prefixes",
                "Create a Lambda function with an API Gateway endpoint that uses the Lambda execution role to upload to S3",
                "Generate presigned URLs on a backend server and deliver them to the mobile application",
                "Set the S3 bucket policy to allow public write access but restrict the IP range to mobile carriers"
            ],
            "answer": "Use Amazon Cognito Identity Pools to provide temporary credentials through IAM roles to unauthenticated users with limited permissions to upload to specific S3 prefixes"
        },
        {
            "question": "A DevOps team needs to automate the deployment of resources across multiple AWS accounts while maintaining security best practices. They want developers to deploy code but not modify IAM permissions or access production databases directly. Which combination of services and features should they use?",
            "options": [
                "AWS CloudFormation with service roles and AWS Organizations SCP to prevent IAM modifications",
                "IAM users with direct cross-account access using access keys",
                "Amazon EC2 instances with instance profiles containing administrative permissions",
                "AWS SSO with custom permission sets for each developer",
                "IAM roles with wildcard resources in the trust policy"
            ],
            "answer": "AWS CloudFormation with service roles and AWS Organizations SCP to prevent IAM modifications"
        },
        {
            "question": "A financial services company needs to implement a security model where AWS administrators can manage infrastructure without having access to the sensitive financial data stored in their applications. Which IAM strategy achieves this separation of duties?",
            "options": [
                "Grant administrators the AWS managed AdministratorAccess policy but request they don't access sensitive data",
                "Implement IAM permissions boundaries on administrator roles that explicitly deny access to data services like S3, DynamoDB and RDS",
                "Create custom IAM policies for administrators that allow all actions except data access operations, and use KMS with key policies that prevent administrator access to encryption keys",
                "Store all sensitive data on-premises and only use AWS for compute resources",
                "Require all administrators to use temporary credentials that expire after 1 hour"
            ],
            "answer": "Create custom IAM policies for administrators that allow all actions except data access operations, and use KMS with key policies that prevent administrator access to encryption keys"
        },
        {
            "question": "A company is migrating from on-premises Active Directory to AWS. They have 5,000 employees who need access to AWS resources across development, testing, and production environments. Which solution provides secure, scalable access management with the least ongoing administrative overhead?",
            "options": [
                "Create IAM users for each employee with appropriate permissions",
                "Set up AWS IAM Identity Center (successor to AWS SSO) integrated with AWS Managed Microsoft AD, create permission sets aligned with job functions, and map to appropriate OUs in the directory",
                "Configure SAML federation directly between each AWS account and Active Directory Federation Services",
                "Create shared IAM users for each department with strong password policies",
                "Use Amazon Cognito User Pools for employee authentication to AWS resources"
            ],
            "answer": "Set up AWS IAM Identity Center (successor to AWS SSO) integrated with AWS Managed Microsoft AD, create permission sets aligned with job functions, and map to appropriate OUs in the directory"
        }
    ],
    "iam_policies": [
        {
            "question": "A security team needs to implement a policy that allows developers to create and manage EC2 instances but prevents them from stopping or terminating instances tagged as 'Environment: Production'. Which policy statement would accomplish this requirement?",
            "options": [
                "A policy with Allow for ec2:* and Deny for ec2:StopInstances and ec2:TerminateInstances with a condition for the tag Environment:Production",
                "A policy that only allows ec2:RunInstances without any statements for stop or terminate actions",
                "A policy with Deny for ec2:* with a condition for the tag Environment:Production",
                "A policy with Allow for ec2:RunInstances and explicit Deny for all other EC2 actions",
                "A resource-based policy attached to each EC2 instance with Production tags"
            ],
            "answer": "A policy with Allow for ec2:* and Deny for ec2:StopInstances and ec2:TerminateInstances with a condition for the tag Environment:Production"
        },
        {
            "question": "A company manages multiple AWS accounts through AWS Organizations. They need to ensure that all EC2 instances created in any account have tags for cost allocation. Which combination of AWS services and features should they use?",
            "options": [
                "Create an IAM policy in each account that requires tags and attach it to all users",
                "Implement a Service Control Policy (SCP) at the organization root level that denies the ec2:RunInstances action if the request does not include specific tags",
                "Use AWS Config rules to delete untagged instances automatically",
                "Set up CloudWatch Events to monitor for instance creation and add tags automatically",
                "Create an IAM permissions boundary that restricts instance creation without tags"
            ],
            "answer": "Implement a Service Control Policy (SCP) at the organization root level that denies the ec2:RunInstances action if the request does not include specific tags"
        },
        {
            "question": "A financial services application stores sensitive customer data in an S3 bucket. The security team needs to ensure this data is only accessible over encrypted connections. Which S3 bucket policy statement would enforce this requirement?",
            "options": [
                "A statement that allows s3:GetObject with a condition that aws:SecureTransport is true",
                "A statement that denies s3:* with a condition that aws:SecureTransport is false",
                "A statement that allows s3:GetObject only from specific IP addresses",
                "A statement that requires aws:PrincipalOrgID to match the organization ID",
                "A statement that allows access only if the request includes specific headers"
            ],
            "answer": "A statement that denies s3:* with a condition that aws:SecureTransport is false"
        },
        {
            "question": "A company has implemented cross-account access where a role in Account A needs to access an S3 bucket in Account B. Despite configuring permissions, access is being denied. Assuming the S3 bucket policy allows the role's access and the role's trust policy is correctly configured, what could be causing this issue?",
            "options": [
                "The S3 bucket is not configured for cross-region access",
                "The IAM role in Account A does not have an explicit Allow policy for the S3 actions on the specific bucket in Account B",
                "Cross-account access requires the use of access keys instead of roles",
                "AWS Organizations SCP is blocking cross-account access",
                "The S3 bucket owner has not enabled ACLs"
            ],
            "answer": "The IAM role in Account A does not have an explicit Allow policy for the S3 actions on the specific bucket in Account B"
        },
        {
            "question": "An administrator is designing a permissions strategy for a data analytics team. The team needs to query data in Amazon Athena but should not be able to modify the underlying tables or access the raw data in S3. Which combination of IAM policies and resource configurations achieves this requirement with the principle of least privilege?",
            "options": [
                "Attach the AmazonAthenaFullAccess managed policy to the analytics team role",
                "Create a customer managed policy that allows athena:StartQueryExecution and athena:GetQueryResults, but denies s3:PutObject and glue:UpdateTable, and use Lake Formation for fine-grained access control on the underlying data",
                "Use S3 bucket policies to restrict access to the data team's IP address range",
                "Create a resource-based policy on the Athena workgroup that restricts actions to queries only",
                "Set up attribute-based access control using tags on all resources"
            ],
            "answer": "Create a customer managed policy that allows athena:StartQueryExecution and athena:GetQueryResults, but denies s3:PutObject and glue:UpdateTable, and use Lake Formation for fine-grained access control on the underlying data"
        }
    ],
    "s3": [
        {
            "question": "A video streaming service stores original high-resolution video files that are rarely accessed after the initial processing but must be retained indefinitely for legal reasons. The files average 10GB in size, and about 100 new videos are added daily. Which S3 storage class and lifecycle configuration would be most cost-effective while maintaining compliance requirements?",
            "options": [
                "Store the files directly in S3 Glacier Deep Archive",
                "Use S3 Standard for 30 days, then transition to S3 One Zone-IA for 60 days, and finally to S3 Glacier Deep Archive",
                "Use S3 Intelligent-Tiering and let AWS automatically move the objects between tiers",
                "Use S3 Standard-IA for 90 days and then transition to S3 Glacier Flexible Retrieval",
                "Store the files in S3 Standard with no lifecycle policy to ensure immediate access if needed"
            ],
            "answer": "Use S3 Standard for 30 days, then transition to S3 One Zone-IA for 60 days, and finally to S3 Glacier Deep Archive"
        },
        {
            "question": "A global retail company needs to allow their mobile application to upload customer images directly to S3. The solution must support millions of users worldwide with minimal latency, ensure the uploads are secure, and prevent unauthorized access to other customers' images. Which combination of S3 features should they use?",
            "options": [
                "Configure a public S3 bucket and rely on client-side encryption in the mobile app",
                "Use S3 Transfer Acceleration with presigned URLs that include user-specific path prefixes and expire after 1 hour",
                "Create a single S3 bucket with public write access but enable default encryption",
                "Set up S3 Cross-Region Replication to multiple regions and allow direct public access",
                "Use CloudFront with signed cookies to allow uploads to S3"
            ],
            "answer": "Use S3 Transfer Acceleration with presigned URLs that include user-specific path prefixes and expire after 1 hour"
        },
        {
            "question": "A financial institution needs to store customer transaction records for regulatory compliance. The data must be immutable, encrypted, and retained for exactly 7 years, after which it must be automatically deleted. What combination of S3 features should they implement?",
            "options": [
                "Enable S3 Versioning, apply a bucket policy to prevent deletions, and set lifecycle rules to expire objects after 7 years",
                "Use S3 Object Lock in Compliance mode with a retention period of 7 years, server-side encryption with KMS, and lifecycle rules to permanently delete expired objects",
                "Store objects in S3 Glacier with a vault lock policy set for 7 years",
                "Enable S3 Replication across regions with a custom lambda function to delete objects after 7 years",
                "Use S3 Intelligent-Tiering with custom metadata to track retention requirements"
            ],
            "answer": "Use S3 Object Lock in Compliance mode with a retention period of 7 years, server-side encryption with KMS, and lifecycle rules to permanently delete expired objects"
        },
        {
            "question": "A media company allows users to upload large video files through their web application. They're experiencing slow upload times and incomplete transfers for users in remote locations with unreliable internet connections. Which S3 feature or configuration would best address this issue?",
            "options": [
                "Enable S3 Multipart Upload with appropriate part size and implement client-side retry logic",
                "Switch to S3 Express One Zone storage class for faster uploads",
                "Implement S3 Batch Operations to handle the uploads in bulk",
                "Set up CloudFront distribution as an intermediary for all uploads",
                "Use S3 Transfer Acceleration with direct uploads to S3"
            ],
            "answer": "Enable S3 Multipart Upload with appropriate part size and implement client-side retry logic"
        },
        {
            "question": "A company stores sensitive customer data in S3 and must implement a comprehensive security strategy that includes encryption, access logging, and protection against accidental deletion. Which combination of S3 features provides the most complete security posture?",
            "options": [
                "Enable default encryption with S3-managed keys, S3 Access Logs, and S3 Versioning",
                "Implement server-side encryption with KMS customer managed keys, enable S3 Access Logs to a separate logging bucket, enable Versioning, implement MFA Delete, and configure appropriate bucket policies and IAM policies",
                "Enable client-side encryption and restrict access through IP-based bucket policies",
                "Use S3 Object Lock in Governance mode for all objects and CloudTrail for logging",
                "Implement VPC Endpoints for S3 and restrict access to the VPC only"
            ],
            "answer": "Implement server-side encryption with KMS customer managed keys, enable S3 Access Logs to a separate logging bucket, enable Versioning, implement MFA Delete, and configure appropriate bucket policies and IAM policies"
        }
    ],
    "organizations": [
        {
            "question": "A company is designing their AWS Organizations structure for their expanding cloud footprint. They have development, testing, and production workloads, along with separate teams for security, networking, and operations. Which organizational structure would provide the best balance of governance and flexibility?",
            "options": [
                "Create a single account for all environments and use IAM roles to separate access",
                "Create separate accounts for each team and use resource tagging for environments",
                "Create an organization with OUs for Security, Infrastructure, and Workloads, with the Workloads OU containing nested OUs for Dev, Test, and Prod, and implement appropriate SCPs at each level",
                "Create an organization with OUs based on geographic regions, and use tags to distinguish between environments",
                "Create separate AWS Organizations for each department to ensure complete isolation"
            ],
            "answer": "Create an organization with OUs for Security, Infrastructure, and Workloads, with the Workloads OU containing nested OUs for Dev, Test, and Prod, and implement appropriate SCPs at each level"
        },
        {
            "question": "A healthcare company must ensure compliance with data protection regulations across their AWS environment. They need to prevent any AWS account in their organization from disabling encryption or security logging. Which combination of AWS Organizations features should they implement?",
            "options": [
                "Apply IAM policies to the root users of all accounts",
                "Implement Service Control Policies at the organization root level that deny actions to disable AWS Config, CloudTrail, and KMS encryption features",
                "Use AWS Config rules in each account with auto-remediation",
                "Create a dedicated security account and grant it administrative access to all other accounts",
                "Implement a Tag Policy that requires security tags on all resources"
            ],
            "answer": "Implement Service Control Policies at the organization root level that deny actions to disable AWS Config, CloudTrail, and KMS encryption features"
        },
        {
            "question": "A global enterprise with subsidiaries in multiple countries needs to design an AWS Organizations structure that accommodates local regulations while maintaining centralized governance. Each subsidiary needs some autonomy for their specific requirements. Which approach would be most effective?",
            "options": [
                "Create a single AWS account with separate VPCs for each subsidiary",
                "Create a multi-account organization with OUs based on geographic regions, with nested OUs for business functions, and implement region restriction SCPs at the appropriate level",
                "Create separate AWS Organizations for each country to ensure complete isolation",
                "Use one account per subsidiary with consolidated billing only and no organizational policies",
                "Create a flat organization structure with all accounts at the same level and use resource tags to distinguish subsidiaries"
            ],
            "answer": "Create a multi-account organization with OUs based on geographic regions, with nested OUs for business functions, and implement region restriction SCPs at the appropriate level"
        },
        {
            "question": "A company is implementing a cost control strategy across their AWS organization. They want to allow innovation in development accounts while preventing expensive services in test accounts and enforcing strict budget controls in production. Which approach using AWS Organizations would best achieve this?",
            "options": [
                "Apply the same budget across all accounts using AWS Budgets",
                "Implement SCPs at the organization level to deny access to expensive services in all accounts",
                "Deploy different SCPs at the OU level - minimal restrictions for Dev OU, service restrictions for Test OU (blocking ML and other expensive services), and instance size limitations for Prod OU",
                "Use consolidated billing features only and manually review costs",
                "Create separate organizations for each environment type with different payment methods"
            ],
            "answer": "Deploy different SCPs at the OU level - minimal restrictions for Dev OU, service restrictions for Test OU (blocking ML and other expensive services), and instance size limitations for Prod OU"
        },
        {
            "question": "A security team needs to implement a defense-in-depth strategy for their AWS multi-account organization. They want to ensure consistent security controls, centralized security monitoring, and the ability to quickly respond to incidents across all accounts. Which architecture using AWS Organizations and security services would be most effective?",
            "options": [
                "Enable all security services in each individual account and manage them separately",
                "Create a dedicated security account, enable organization-wide features for AWS Config, GuardDuty, and Security Hub with delegated administration to the security account, implement SCPs to prevent disabling these services, and establish automated remediation workflows",
                "Consolidate all security-related resources into a single account and provide cross-account access",
                "Implement CloudTrail in a central account and share the logs with all accounts",
                "Use IAM policies in each account to restrict security changes"
            ],
            "answer": "Create a dedicated security account, enable organization-wide features for AWS Config, GuardDuty, and Security Hub with delegated administration to the security account, implement SCPs to prevent disabling these services, and establish automated remediation workflows"
        }
    ],
    "sts": [
        {
            "question": "A company uses AWS Organizations with multiple accounts. A data analytics team needs temporary access to data stored in S3 buckets across different accounts for processing. The security team requires that all access be logged and credentials should expire after the minimum necessary time. Which approach provides the most secure cross-account access?",
            "options": [
                "Create IAM users in each account and share access keys with the analytics team",
                "Create a cross-account IAM role in each account with appropriate S3 permissions, configure trust relationships to allow assumption from the analytics account, and use STS AssumeRole API with an external ID and limited session duration",
                "Make the S3 buckets public with IP-based restrictions",
                "Create IAM roles with administrator access in each account",
                "Use AWS SSO to provide console access to each account"
            ],
            "answer": "Create a cross-account IAM role in each account with appropriate S3 permissions, configure trust relationships to allow assumption from the analytics account, and use STS AssumeRole API with an external ID and limited session duration"
        },
        {
            "question": "A financial services application needs to integrate with a third-party data provider. The provider needs limited access to specific resources in your AWS account. The security team is concerned about potential security risks from this integration. Which STS implementation provides the strongest security controls?",
            "options": [
                "Create an IAM user for the provider and share the access keys",
                "Create an IAM role that can be assumed by the provider, include an external ID condition in the trust policy that is known only to you and the provider, and implement a permissions boundary limiting the role's access",
                "Use a lambda function to generate temporary credentials on demand",
                "Provide the third-party with your AWS account root user credentials",
                "Create a VPC endpoint and restrict access to the VPC only"
            ],
            "answer": "Create an IAM role that can be assumed by the provider, include an external ID condition in the trust policy that is known only to you and the provider, and implement a permissions boundary limiting the role's access"
        },
        {
            "question": "A security incident has been detected where an IAM role in your account may have been compromised, and unauthorized access could still be ongoing through active temporary credentials. Which immediate action would be most effective to revoke all active sessions using this role?",
            "options": [
                "Delete and recreate the IAM role with the same permissions",
                "Modify the trust policy to prevent new role assumptions, and add an inline policy with a deny statement that includes the AWSRevokeOlderSessions condition",
                "Change the maximum session duration for the role to 1 hour",
                "Contact AWS Support to invalidate the credentials",
                "Delete all current policies attached to the role"
            ],
            "answer": "Modify the trust policy to prevent new role assumptions, and add an inline policy with a deny statement that includes the AWSRevokeOlderSessions condition"
        },
        {
            "question": "A company is implementing a CI/CD pipeline that needs to deploy resources across multiple AWS accounts. The pipeline must securely assume different IAM roles based on the environment (development, staging, production) and maintain least privilege. Which approach using STS provides the most secure and maintainable solution?",
            "options": [
                "Store access keys for each account in the CI/CD system's secrets management",
                "Create a shared role with full access across all accounts",
                "Create a deployment role in each account with permissions specific to that environment's requirements, configure trust relationships to allow assumption from the CI/CD account, and use role session tags to further control permissions based on deployment context",
                "Use the AWS account root users to perform deployments to ensure sufficient permissions",
                "Create one powerful role that can be assumed by anyone in the organization"
            ],
            "answer": "Create a deployment role in each account with permissions specific to that environment's requirements, configure trust relationships to allow assumption from the CI/CD account, and use role session tags to further control permissions based on deployment context"
        },
        {
            "question": "A multinational corporation needs to integrate their on-premises Active Directory with AWS for employee access management. Employees should be able to use their existing credentials to obtain temporary access to AWS resources based on their AD group membership. Which architecture provides secure federation while maintaining least privilege?",
            "options": [
                "Create IAM users that match employee usernames and manage permissions manually",
                "Set up AWS IAM Identity Center with AD Connector integration, create permission sets aligned with job functions, and map AD groups to IAM Identity Center permission sets",
                "Configure SAML federation between AD FS and AWS, create IAM roles that map to AD groups, and implement STS token vending with appropriate session policies",
                "Create one IAM role with administrative access that all employees can assume",
                "Use Amazon Cognito User Pools for employee federation"
            ],
            "answer": "Configure SAML federation between AD FS and AWS, create IAM roles that map to AD groups, and implement STS token vending with appropriate session policies"
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
        st.header("Content Review – Session 1")
        st.markdown("""
        Welcome to the AWS Partner Certification Readiness program. This interactive guide will help you prepare 
        for the Solutions Architect - Associate certification. Navigate through the topics using the tabs above.
        
        Each section contains key concepts and important takeaways. Test your understanding with the Knowledge Checks tab.
        """)
    
    st.markdown("""
    <div class="aws-info-card">
        <h3>Topics covered:</h3>
        <p>
            • AWS Global Infrastructure<br>
            • Amazon CloudFront<br>
            • Identity and Access Management (IAM)<br>
            • IAM Policies<br>
            • Amazon S3<br>
            • AWS Organizations<br>
            • Security Token Service (STS)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display tips
    st.markdown("""
    <div class="aws-card">
        <h3>📝 Certification Preparation Tips</h3>
        <p>Practice hands-on with the services covered in this guide. The AWS Solutions Architect - Associate exam focuses on practical knowledge of AWS services and how they can be used together to design resilient, cost-effective solutions.</p>
        <ul>
            <li><strong>Focus on scenario-based learning:</strong> The exam tests your ability to apply AWS services to real-world scenarios</li>
            <li><strong>Understand service integrations:</strong> Know how different AWS services work together</li>
            <li><strong>Master IAM concepts:</strong> Security and access control are critical components of the exam</li>
            <li><strong>Know global infrastructure:</strong> Understand regions, availability zones, and edge locations</li>
            <li><strong>Practice with hands-on labs:</strong> Reinforce concepts with practical experience</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Overview section
    st.header("Overview")
    
    # Create a grid of service cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🌐 Global Infrastructure</h4>
            <ul>
                <li><strong>Regions:</strong> Physical locations around the world</li>
                <li><strong>Availability Zones:</strong> Isolated data centers in a region</li>
                <li><strong>Edge Locations:</strong> Content delivery network endpoints</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔐 Identity & Access Management</h4>
            <ul>
                <li><strong>Users & Groups:</strong> Entity management</li>
                <li><strong>Roles:</strong> Temporary security credentials</li>
                <li><strong>Policies:</strong> Define permissions for resources</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🗄️ Amazon S3</h4>
            <ul>
                <li><strong>Storage Classes:</strong> Options for different use cases</li>
                <li><strong>Security Features:</strong> Encryption, policies, and access control</li>
                <li><strong>Performance:</strong> Transfer acceleration and multi-part uploads</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🌍 Amazon CloudFront</h4>
            <ul>
                <li><strong>Content Delivery:</strong> Global distribution of content</li>
                <li><strong>Origin Shield:</strong> Reducing load on origin servers</li>
                <li><strong>Security:</strong> Protecting content and applications</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Function for Global Infrastructure page
def global_infrastructure_page():
    st.title("AWS Global Infrastructure")
    
    try:
        image = load_image_from_url(aws_images["global_infrastructure"])
        if image:
            st.image(image, width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("AWS Regions")
    st.markdown("""
    A physical location around the world where AWS clusters data centers.
    """)
    
    st.markdown("""
    <div class="aws-card">
        <h3>Key Points</h3>
        <ul>
            <li>Each AWS Region consists of multiple, isolated, and physically separate Availability Zones</li>
            <li>Currently 34 AWS Regions worldwide with 99+ Availability Zones</li>
            <li>Factors to consider when selecting a Region:
                <ul>
                    <li><strong>Compliance:</strong> Local regulations and data residency laws</li>
                    <li><strong>Latency:</strong> Proximity to users for better experience</li>
                    <li><strong>Cost:</strong> Pricing varies between Regions</li>
                    <li><strong>Service availability:</strong> Newer services and features may not be available in all Regions</li>
                </ul>
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Availability Zones (AZs)")
    
    try:
        image = load_image_from_url(aws_images["regions"])
        if image:
            st.image(image, width=700)
    except:
        st.warning("Image could not be displayed")
        
    st.markdown("""
    One or more discrete data centers with redundant power, networking, and connectivity in an AWS Region.
    """)
    
    st.markdown("""
    <div class="aws-card">
        <h3>Key Points</h3>
        <ul>
            <li>AZs are physically separated (several kilometers apart, but within 100km)</li>
            <li>Connected via low-latency, high-bandwidth, redundant networking</li>
            <li>Enable high availability through multi-AZ deployments</li>
            <li>Protect applications from datacenter-level failures</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="aws-info-card">
        <h3>Service Scopes</h3>
        <ul>
            <li><strong>Zonal services:</strong> Resources tied to specific AZs (EC2 instances, RDS, etc.)</li>
            <li><strong>Regional services:</strong> Automatically span multiple AZs (S3, DynamoDB, etc.)</li>
            <li><strong>Global services:</strong> Single instance serving all regions (IAM, Route 53, CloudFront)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Points of Presence (PoP)")
    st.markdown("""
    Edge locations and regional edge caches that bring content closer to end users.
    """)
    
    st.markdown("""
    <div class="aws-card">
        <h3>Key Points</h3>
        <ul>
            <li>600+ Edge Locations and 13 regional mid-tier regional cache servers worldwide</li>
            <li>Enable Amazon CloudFront to deliver content with low latency</li>
            <li>Used by CloudFront, Route 53, AWS WAF, and AWS Shield</li>
            <li>Help reduce latency for global users by caching content closer to them</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Function for CloudFront page
def cloudfront_page():
    st.title("Amazon CloudFront")
    
    try:
        image = load_image_from_url(aws_images["cloudfront"])
        if image:
            st.image(image, width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("Content Delivery Network (CDN)")
    st.markdown("""
    Amazon CloudFront is a fast content delivery network (CDN) service that securely delivers data, videos, applications, and APIs to customers globally with low latency and high transfer speeds.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🚀 Key Benefits</h4>
            <ul>
                <li><strong>Improved Performance:</strong> Delivers content from edge locations closest to users</li>
                <li><strong>High Availability:</strong> Built on AWS's global infrastructure</li>
                <li><strong>Cost-Effective:</strong> Pay only for the content delivered</li>
                <li><strong>Security Integration:</strong> Works with AWS Shield, AWS WAF, and Route 53</li>
                <li><strong>Programmable:</strong> Customize with Lambda@Edge</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔄 How CloudFront Works</h4>
            <ol>
                <li>User requests content from your website/application</li>
                <li>DNS routes request to nearest CloudFront edge location</li>
                <li>CloudFront checks its cache for requested object</li>
                <li>If object is in cache, CloudFront returns it to user</li>
                <li>If not in cache, CloudFront forwards request to origin server</li>
                <li>Origin server sends object to edge location</li>
                <li>CloudFront delivers object to user and caches it for future requests</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Regional Edge Caches")
    st.markdown("""
    Regional edge caches sit between your origin servers and global edge locations.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h3>Key Points</h3>
            <ul>
                <li>Larger than individual edge locations</li>
                <li>Help cache content that isn't popular enough to stay at edge locations</li>
                <li>Reduce load on origin servers</li>
                <li>Content stays in regional edge caches longer</li>
                <li>Particularly useful for:
                    <ul>
                        <li>User-generated content</li>
                        <li>E-commerce assets</li>
                        <li>News and event-related content</li>
                    </ul>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h3>How Regional Edge Caches Work</h3>
            <ol>
                <li>If content isn't at the edge location, request goes to nearest regional edge cache</li>
                <li>If content is at regional edge cache, it's forwarded to the edge location</li>
                <li>If not at regional cache, request goes to origin server</li>
                <li>Content is cached at both regional edge cache and edge location for future requests</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🛡️ Security Features</h4>
            <ul>
                <li>Origin Access Identity (OAI)</li>
                <li>Signed URLs and Cookies for private content</li>
                <li>Field-level encryption</li>
                <li>AWS WAF integration</li>
                <li>AWS Shield integration</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>⚙️ Performance Features</h4>
            <ul>
                <li>Origin Shield</li>
                <li>Cache behaviors</li>
                <li>Compression support</li>
                <li>HTTP/2 and HTTP/3 support</li>
                <li>Origin failover</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>📊 Monitoring & Customization</h4>
            <ul>
                <li>Real-time logs</li>
                <li>Lambda@Edge</li>
                <li>CloudFront Functions</li>
                <li>Origin request policies</li>
                <li>Cache key policies</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="aws-warning-card">
        <h4>Important Consideration</h4>
        <p>When using CloudFront with an S3 origin, it's best practice to use Origin Access Identity (OAI) or Origin Access Control (OAC) to restrict access to the S3 bucket, ensuring users can only access content through CloudFront and not directly from S3.</p>
    </div>
    """, unsafe_allow_html=True)

# Function for IAM page
def iam_page():
    st.title("Identity and Access Management (IAM)")
    
    try:
        image = load_image_from_url(aws_images["iam"])
        if image:
            st.image(image, width=700)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is IAM?")
    st.markdown("""
    AWS Identity and Access Management (IAM) helps you securely control access to AWS resources by managing who is authenticated and authorized to use them.
    """)
    
    st.markdown("""
    <div class="aws-card">
        <h3>Key Concepts</h3>
        <ul>
            <li><strong>Authentication:</strong> Verifying identity (who you are)</li>
            <li><strong>Authorization:</strong> Determining access rights (what you can do)</li>
            <li><strong>Principal:</strong> Entity requesting access (user, role, application)</li>
            <li><strong>Request:</strong> Action on a resource (API call to AWS)</li>
            <li><strong>Evaluation:</strong> Checking permissions for the request</li>
            <li><strong>Decision:</strong> Allow or deny based on policies</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Principle of Least Privilege")
    st.markdown("""
    A core security best practice that involves granting only the permissions required to perform a task.
    """)
    
    st.markdown("""
    <div class="aws-info-card">
        <h3>Key Points</h3>
        <ul>
            <li>Start with minimum permissions and grant additional as needed</li>
            <li>Regularly review and remove unused permissions</li>
            <li>Use permission boundaries to set maximum permissions</li>
            <li>Implement just-in-time access rather than permanent permissions</li>
            <li>Helps reduce security risks and potential blast radius</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("IAM Users and Groups")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>👤 IAM Users</h4>
            <ul>
                <li>Entities that represent people or applications that interact with AWS</li>
                <li>Each user has a unique name and credentials</li>
                <li>Can access AWS via:
                    <ul>
                        <li>Console (username/password)</li>
                        <li>API/CLI (access keys)</li>
                        <li>SDK (access keys)</li>
                    </ul>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>👥 IAM Groups</h4>
            <ul>
                <li>Collections of IAM users</li>
                <li>Used to assign permissions to multiple users at once</li>
                <li>Users can belong to multiple groups</li>
                <li>Groups cannot be nested (no groups within groups)</li>
                <li>Simplify permission management</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("AWS Organizations")
    
    try:
        image = load_image_from_url(aws_images["organizations"])
        if image:
            st.image(image, width=700)
    except:
        st.warning("Image could not be displayed")
        
    st.markdown("""
    An account management service that enables consolidation and organization of multiple AWS accounts.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔑 Key Features</h4>
            <ul>
                <li><strong>Centralized Management:</strong> Manage multiple accounts from a single place</li>
                <li><strong>Consolidated Billing:</strong> Single payment for all accounts</li>
                <li><strong>Hierarchical Organization:</strong> Group accounts into organizational units (OUs)</li>
                <li><strong>Service Control Policies (SCPs):</strong> Apply permission guardrails across accounts</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>💼 Best Practices</h4>
            <ul>
                <li>Organize OUs by function rather than company structure</li>
                <li>Create dedicated accounts for security, audit, and billing</li>
                <li>Use SCPs to enforce compliance requirements</li>
                <li>Implement a multi-account strategy for better isolation and security</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Function for IAM Policies page
def iam_policies_page():
    st.title("IAM Policies")
    
    try:
        image = load_image_from_url(aws_images["iam_policies"])
        if image:
            st.image(image, width=700)
    except:
        st.warning("Image could not be displayed")
    
    st.header("Policy Types")
    st.markdown("""
    IAM policies define permissions and are used to manage access in AWS.
    """)
    
    st.markdown("""
    <div class="aws-card">
        <h3>Major Policy Types</h3>
        <ul>
            <li><strong>Identity-based policies:</strong> Attached to IAM users, groups, or roles</li>
            <li><strong>Resource-based policies:</strong> Attached to resources (e.g., S3 bucket policies)</li>
            <li><strong>Permissions boundaries:</strong> Set maximum permissions for an IAM entity</li>
            <li><strong>Service control policies (SCPs):</strong> Used with AWS Organizations to limit permissions</li>
            <li><strong>Access control lists (ACLs):</strong> Legacy, control access to resources</li>
            <li><strong>Session policies:</strong> Passed during role assumption to further restrict permissions</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Policy Evaluation Logic")
    st.markdown("""
    How AWS evaluates policies to determine if a request should be allowed or denied:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Evaluation Steps</h4>
            <ol>
                <li>Default denial: All requests start as implicitly denied</li>
                <li>Evaluate applicable policies: Identity-based, resource-based, etc.</li>
                <li>Any explicit DENY? If yes, final decision is DENY</li>
                <li>Any explicit ALLOW? If yes, final decision is ALLOW, otherwise DENY</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Important Rules</h4>
            <ul>
                <li>There is no "implicit allow" - access must be explicitly allowed</li>
                <li>An explicit deny always overrides any allows</li>
                <li>Resource-based policies are evaluated in parallel with identity-based policies</li>
                <li>Permissions boundaries limit the maximum permissions an identity can have</li>
                <li>SCPs limit the maximum permissions for accounts in an organization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Example IAM Policy")
    
    st.markdown("""
    <div class="aws-info-card">
        <h4>This policy allows S3 list and read operations on a specific bucket but denies access to the confidential folder</h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.code('''
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    "arn:aws:s3:::my-bucket",
                    "arn:aws:s3:::my-bucket/*"
                ]
            },
            {
                "Effect": "Deny",
                "Action": "s3:*",
                "Resource": "arn:aws:s3:::my-bucket/confidential/*"
            }
        ]
    }
    ''', language="json")
    
    st.header("Amazon Resource Names (ARNs)")
    st.markdown("""
    Unique identifiers for AWS resources that are used in IAM policies.
    """)
    
    st.markdown("""
    <div class="aws-card">
        <h3>ARN Format</h3>
        <code>arn:partition:service:region:account-id:resource-type/resource-id</code>
        
        <h4>Examples</h4>
        <ul>
            <li>S3 bucket: <code>arn:aws:s3:::my-bucket</code></li>
            <li>EC2 instance: <code>arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef0</code></li>
            <li>IAM user: <code>arn:aws:iam::123456789012:user/username</code></li>
        </ul>
        
        <p><strong>Note:</strong> Some global resources omit region and/or account ID in their ARNs.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("IAM Roles")
    st.markdown("""
    IAM roles provide temporary security credentials for AWS resources or external identities.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Key Characteristics</h4>
            <ul>
                <li>Not associated with a specific person</li>
                <li>Assumed by users, applications, or services</li>
                <li>Temporary credentials with defined lifetime</li>
                <li>No long-term credentials like passwords or access keys</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Common Use Cases</h4>
            <ul>
                <li>EC2 instance roles</li>
                <li>Lambda execution roles</li>
                <li>Cross-account access</li>
                <li>Federation with external identity providers</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Function for STS page
def sts_page():
    st.title("AWS Security Token Service (STS)")
    
    try:
        image = load_image_from_url(aws_images["sts"])
        if image:
            st.image(image, width=700)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is STS?")
    st.markdown("""
    AWS Security Token Service (STS) enables you to request temporary, limited-privilege credentials for AWS IAM users or users from external identity providers.
    """)
    
    st.markdown("""
    <div class="aws-feature-card">
        <h4>Key Features</h4>
        <ul>
            <li><strong>Temporary Credentials:</strong> Short-lived access keys that expire automatically</li>
            <li><strong>Limited Privileges:</strong> Define specific permissions for the session</li>
            <li><strong>Secure Federation:</strong> Integrate with external identity systems</li>
            <li><strong>Delegation:</strong> Allow services to act on your behalf</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Common STS Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h3>Role-Based Operations</h3>
            <ul>
                <li><strong>AssumeRole:</strong> Get temporary credentials to access AWS resources</li>
                <li><strong>AssumeRoleWithWebIdentity:</strong> Federation with OIDC providers like Google, Facebook, etc.</li>
                <li><strong>AssumeRoleWithSAML:</strong> Federation with SAML 2.0 providers</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h3>User-Based Operations</h3>
            <ul>
                <li><strong>GetSessionToken:</strong> Get temporary credentials for an IAM user</li>
                <li><strong>GetFederationToken:</strong> Get temporary credentials for a federated user</li>
                <li><strong>GetCallerIdentity:</strong> Returns details about the IAM identity making the call</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Trust Policies")
    st.markdown("""
    A trust policy defines which principals (users, services, accounts) can assume a role.
    """)
    
    st.markdown("""
    <div class="aws-info-card">
        <h4>Example Trust Policy</h4>
        <p>This policy allows a specific AWS account to assume this role when providing the correct external ID:</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.code('''
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "AWS": "arn:aws:iam::123456789012:root"
          },
          "Action": "sts:AssumeRole",
          "Condition": {
            "StringEquals": {
              "sts:ExternalId": "unique-id-assigned-by-third-party"
            }
          }
        }
      ]
    }
    ''', language="json")
    
    st.markdown("""
    <div class="aws-card">
        <h3>Security Best Practices</h3>
        <ul>
            <li>Use external IDs for third-party access</li>
            <li>Apply conditions like source IP restrictions</li>
            <li>Set appropriate maximum session duration</li>
            <li>Implement MFA for role assumption</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Revoking Temporary Credentials")
    st.markdown("""
    How to handle situations where temporary credentials need to be revoked before expiration:
    """)
    
    st.markdown("""
    <div class="aws-card">
        <h3>Options</h3>
        <ol>
            <li><strong>Modify trust policy</strong> to prevent new role assumptions (doesn't affect active sessions)</li>
            <li><strong>Add inline deny policy</strong> with the <code>AWSRevokeOlderSessions</code> condition key</li>
            <li><strong>Change permissions</strong> attached to the role (affects all new and existing sessions)</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="aws-warning-card">
        <h4>Example Deny Policy for Revocation</h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.code('''
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Deny",
          "Action": "*",
          "Resource": "*",
          "Condition": {
            "DateLessThan": {
              "aws:TokenIssueTime": "2023-07-01T00:00:00Z"
            }
          }
        }
      ]
    }
    ''', language="json")

# Function for S3 page
def s3_page():
    st.title("Amazon Simple Storage Service (S3)")
    
    try:
        image = load_image_from_url(aws_images["s3"])
        if image:
            st.image(image, width=700)
    except:
        st.warning("Image could not be displayed")
    
    st.header("S3 Overview")
    st.markdown("""
    Amazon S3 (Simple Storage Service) provides infinitely scalable, highly durable object storage in the AWS Cloud.
    """)
    
    st.markdown("""
    <div class="aws-card">
        <h3>Key Concepts</h3>
        <ul>
            <li><strong>Object-based storage:</strong> Store any type of file up to 5TB</li>
            <li><strong>Buckets:</strong> Containers for objects with globally unique names</li>
            <li><strong>Objects:</strong> Files and metadata stored in S3</li>
            <li><strong>Keys:</strong> Unique identifiers for objects within a bucket</li>
            <li><strong>Durability:</strong> 99.999999999% (11 nines) durability</li>
            <li><strong>Availability:</strong> Varies by storage class (typically 99.99%)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("S3 Storage Classes")
    st.markdown("""
    Different storage classes to optimize costs based on access patterns.
    """)
    
    st.markdown("""
    <div style="overflow-x: auto;">
        <table>
            <thead>
                <tr>
                    <th>Storage Class</th>
                    <th>Use Case</th>
                    <th>Availability</th>
                    <th>Retrieval Time</th>
                    <th>Minimum Storage Duration</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>S3 Standard</td>
                    <td>Active, frequently accessed data</td>
                    <td>99.99%</td>
                    <td>Milliseconds</td>
                    <td>None</td>
                </tr>
                <tr>
                    <td>S3 Intelligent-Tiering</td>
                    <td>Data with changing access patterns</td>
                    <td>99.9%</td>
                    <td>Milliseconds</td>
                    <td>None</td>
                </tr>
                <tr>
                    <td>S3 Standard-IA</td>
                    <td>Infrequently accessed data</td>
                    <td>99.9%</td>
                    <td>Milliseconds</td>
                    <td>30 days</td>
                </tr>
                <tr>
                    <td>S3 One Zone-IA</td>
                    <td>Re-creatable, infrequently accessed</td>
                    <td>99.5%</td>
                    <td>Milliseconds</td>
                    <td>30 days</td>
                </tr>
                <tr>
                    <td>S3 Glacier Instant Retrieval</td>
                    <td>Archive data needing immediate access</td>
                    <td>99.9%</td>
                    <td>Milliseconds</td>
                    <td>90 days</td>
                </tr>
                <tr>
                    <td>S3 Glacier Flexible Retrieval</td>
                    <td>Archive data with flexible retrieval</td>
                    <td>99.99%</td>
                    <td>Minutes to hours</td>
                    <td>90 days</td>
                </tr>
                <tr>
                    <td>S3 Glacier Deep Archive</td>
                    <td>Long-term archiving, rare access</td>
                    <td>99.99%</td>
                    <td>Hours</td>
                    <td>180 days</td>
                </tr>
                <tr>
                    <td>S3 Express One Zone</td>
                    <td>High-performance data, single AZ</td>
                    <td>99.5%</td>
                    <td>Single-digit ms</td>
                    <td>None</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("S3 Bucket Policies")
    st.markdown("""
    Resource-based policies attached to S3 buckets that grant or deny access permissions.
    """)
    
    st.markdown("""
    <div class="aws-card">
        <h3>Key Elements</h3>
        <ul>
            <li><strong>Principal:</strong> Who the policy applies to (users, roles, accounts)</li>
            <li><strong>Effect:</strong> Allow or Deny</li>
            <li><strong>Action:</strong> S3 operations (GetObject, PutObject, etc.)</li>
            <li><strong>Resource:</strong> Buckets and objects the policy applies to</li>
            <li><strong>Condition:</strong> Optional restrictions on when policy applies</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="aws-info-card">
        <h4>Example Policy</h4>
        <p>This policy allows a specific IAM user to list and get objects from a bucket:</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.code('''
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": "arn:aws:iam::123456789012:user/username"},
                "Action": ["s3:GetObject", "s3:ListBucket"],
                "Resource": [
                    "arn:aws:s3:::my-bucket",
                    "arn:aws:s3:::my-bucket/*"
                ]
            }
        ]
    }
    ''', language="json")
    
    st.header("S3 Performance Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>S3 Transfer Acceleration</h4>
            <p>Feature that enables fast, easy, and secure transfers of files over long distances between your client and an S3 bucket.</p>
            <ul>
                <li>Uses AWS CloudFront's globally distributed edge locations</li>
                <li>Routes data through AWS backbone network</li>
                <li>Optimizes network protocols for long-distance transfers</li>
                <li>Especially useful for global uploads to centralized buckets</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Multipart Upload</h4>
            <p>Feature that allows uploading large objects in parts for improved throughput and resilience.</p>
            <ul>
                <li>Parallel uploads of parts for faster performance</li>
                <li>Improved recovery from network issues</li>
                <li>Pause and resume uploads</li>
                <li>Required for objects over 5GB</li>
                <li>Recommended for objects larger than 100MB</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("S3 Security Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Access Management</h4>
            <ul>
                <li>Bucket policies</li>
                <li>ACLs (less recommended now)</li>
                <li>IAM policies</li>
                <li>Block Public Access settings</li>
                <li>Access Points</li>
                <li>VPC Endpoints</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Data Protection</h4>
            <ul>
                <li>Encryption (SSE-S3, SSE-KMS, SSE-C)</li>
                <li>Object Lock</li>
                <li>Versioning</li>
                <li>MFA Delete</li>
                <li>S3 Object Lambda</li>
                <li>CORS configuration</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Monitoring & Logging</h4>
            <ul>
                <li>Access Logs</li>
                <li>Event notifications</li>
                <li>AWS CloudTrail integration</li>
                <li>S3 Storage Lens</li>
                <li>S3 Inventory</li>
                <li>S3 Analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Function for Organizations page
def organizations_page():
    st.title("AWS Organizations")
    
    try:
        image = load_image_from_url(aws_images["organizations"])
        if image:
            st.image(image, width=700)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What are AWS Organizations?")
    st.markdown("""
    AWS Organizations is an account management service that enables you to consolidate multiple AWS accounts into an organization that you create and centrally manage.
    """)
    
    st.markdown("""
    <div class="aws-card">
        <h3>Core Components</h3>
        <ul>
            <li><strong>Organization:</strong> Entity that consolidates AWS accounts</li>
            <li><strong>Management account:</strong> The account that created the organization (formerly called "master account")</li>
            <li><strong>Member accounts:</strong> All other accounts in the organization</li>
            <li><strong>Organizational Units (OUs):</strong> Containers for accounts to group them in a hierarchy</li>
            <li><strong>Root:</strong> The parent container for all accounts and OUs in the organization</li>
            <li><strong>Service Control Policies (SCPs):</strong> Policies that control permissions for accounts within the organization</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Management Features</h4>
            <ul>
                <li><strong>Centralized account management:</strong> Create and manage accounts from a central location</li>
                <li><strong>Hierarchical organization:</strong> Group accounts into OUs for easier management</li>
                <li><strong>Automated account creation:</strong> Use APIs to automate account provisioning</li>
                <li><strong>Delegated administration:</strong> Assign administrative responsibilities for specific AWS services</li>
                <li><strong>API access:</strong> Programmatically manage your organization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Control Features</h4>
            <ul>
                <li><strong>Service Control Policies (SCPs):</strong> Set permission guardrails that apply to all accounts</li>
                <li><strong>Tag policies:</strong> Standardize tags across resources in your organization</li>
                <li><strong>Backup policies:</strong> Define backup schedules and retention periods</li>
                <li><strong>AI services opt-out policies:</strong> Control AI service data usage</li>
                <li><strong>Consolidated billing:</strong> Single payment for all accounts with volume discounts</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Service Control Policies (SCPs)")
    st.markdown("""
    SCPs offer central control over the maximum available permissions for all accounts in your organization.
    """)
    
    st.markdown("""
    <div class="aws-card">
        <h3>Key Points</h3>
        <ul>
            <li>SCPs don't grant permissions; they define guardrails</li>
            <li>Accounts still need IAM permissions to perform actions</li>
            <li>SCPs affect all users and roles in attached accounts, including the root user</li>
            <li>SCPs don't affect service-linked roles</li>
            <li>SCPs don't affect the management account (limitations can only be applied to member accounts)</li>
            <li>SCPs use the same language format as IAM policies</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="aws-info-card">
        <h4>Example SCP</h4>
        <p>This SCP prevents member accounts from leaving the organization:</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.code('''
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Deny",
                "Action": [
                    "organizations:LeaveOrganization"
                ],
                "Resource": "*"
            }
        ]
    }
    ''', language="json")
    
    st.header("Best Practices")
    st.markdown("""
    <div class="aws-card">
        <h3>Organization Structure</h3>
        <ul>
            <li>Create dedicated accounts for shared services, security, and logging</li>
            <li>Use OUs based on function, not organizational structure</li>
            <li>Apply SCPs based on the principle of least privilege</li>
            <li>Start with "Deny lists" rather than "Allow lists" for SCPs</li>
            <li>Use AWS Control Tower to set up and govern a secure, multi-account environment</li>
            <li>Implement standardized tagging strategy across the organization</li>
            <li>Enable AWS CloudTrail in all accounts with centralized logging</li>
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
    
    # Display quiz section tabs
    tab_names = ["Global Infrastructure", "CloudFront", "IAM", "IAM Policies", "S3", "Organizations", "STS"]
    topic_keys = ["global_infrastructure", "cloudfront", "iam", "iam_policies", "s3", "organizations", "sts"]
    
    tabs = st.tabs(tab_names)
    
    # Loop through each tab and display corresponding quiz
    for i, tab in enumerate(tabs):
        with tab:
            st.header(f"{tab_names[i]} Knowledge Check")
            topic = topic_keys[i]
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

# Sidebar for session management
st.sidebar.subheader("⚙️ Session Management")

# Reset button for session data
if st.sidebar.button("🔄 Reset Progress", key="reset_button"):
    reset_session()

# Show session ID
st.sidebar.caption(f"Session ID: {st.session_state.session_id[:8]}...")

st.sidebar.divider()

# Main navigation with tabs using emojis
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "🏠 Home", 
    "🌐 Global Infrastructure", 
    "🌍 CloudFront", 
    "🔐 IAM", 
    "📜 IAM Policies",
    "🗄️ S3", 
    "🏢 Organizations", 
    "🔑 STS",
    "📝 Knowledge Check"
])


# Display content based on selected tab
with tab1:
    home_page()

with tab2:
    global_infrastructure_page()

with tab3:
    cloudfront_page()

with tab4:
    iam_page()

with tab5:
    iam_policies_page()

with tab6:
    s3_page()

with tab7:
    organizations_page()

with tab8:
    sts_page()

with tab9:
    knowledge_checks_page()

# Footer
st.markdown("""
<div class="footer">
    © 2025 AWS Partner Certification Readiness. All rights reserved.
</div>
""", unsafe_allow_html=True)
