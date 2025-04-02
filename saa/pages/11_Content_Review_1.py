
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
    "global_infrastructure": "https://d1.awsstatic.com/global-infrastructure/maps/Global-Infrastructure-Map_1.20.2022.b2f0ad79c1230cb97f60bc904494f122758d24f1.png",
    "regions": "https://d1.awsstatic.com/diagrams/availability-zones_diagram-updated.40f601e2b6d81573dc88483c1fc2553ad0a1a25d.png",
    "cloudfront": "https://d1.awsstatic.com/product-marketing/CloudFront/CloudFront-Diagram.c3ef67291cc5a3929db2934739ae5e7ced7a9b25.png",
    "iam": "https://d1.awsstatic.com/product-marketing/IAM/iam-how-it-works-diagram.cce4e33da82c06b42d032684ef0b39615b8855c6.png",
    "iam_policies": "https://d1.awsstatic.com/security-center/IAM-policy-evaluation.648e2924e1f684ae3d759e940980e8adf7fa52ca.png",
    "s3": "https://d1.awsstatic.com/s3-pdp-redesign/product-page-diagram_Amazon-S3_HIW.cf4c2bd7aa02f1fe77be8aa120393993e08ac86d.png",
    "organizations": "https://d1.awsstatic.com/product-marketing/Organizations/Organizations-Diagram.f29c33e7758f599e9a362b644892558c67f5e60f.png",
    "sts": "https://d1.awsstatic.com/security-center/Security-STS.58d8dc26b43b2d5e5a3312afd45d02869a1e7577.png",
}

# Scenario-based quiz questions
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
        st.header("Content Review – Session 1")
        st.markdown("""
        Welcome to the AWS Partner Certification Readiness program. This interactive guide will help you prepare 
        for the Solutions Architect - Associate certification. Navigate through the topics using the sidebar menu.
        
        Each section contains key concepts, important takeaways, and interactive quizzes to reinforce your learning.
        
        **Topics covered:**
        - AWS Global Infrastructure
        - Amazon CloudFront
        - Identity and Access Management (IAM)
        - IAM Policies
        - Amazon S3
        - AWS Organizations
        - Security Token Service (STS)
        """)
    
    st.info("""
    **Certification Preparation Tip:** Practice hands-on with the services covered in this guide. 
    The AWS Solutions Architect - Associate exam focuses on practical knowledge of AWS services 
    and how they can be used together to design resilient, cost-effective solutions.
    """)

# Function for Global Infrastructure page
def global_infrastructure_page():
    st.title("AWS Global Infrastructure")
    
    try:
        st.image(aws_images["global_infrastructure"], width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("AWS Regions")
    st.markdown("""
    A physical location around the world where AWS clusters data centers.
    
    **Key Points:**
    - Each AWS Region consists of multiple, isolated, and physically separate Availability Zones
    - Currently 34 AWS Regions worldwide with 99+ Availability Zones
    - Factors to consider when selecting a Region:
      - **Compliance:** Local regulations and data residency laws
      - **Latency:** Proximity to users for better experience
      - **Cost:** Pricing varies between Regions
      - **Service availability:** Newer services and features may not be available in all Regions
    """)
    
    st.header("Availability Zones (AZs)")
    
    try:
        st.image(aws_images["regions"], width=700)
    except:
        st.warning("Image could not be displayed")
        
    st.markdown("""
    One or more discrete data centers with redundant power, networking, and connectivity in an AWS Region.
    
    **Key Points:**
    - AZs are physically separated (several kilometers apart, but within 100km)
    - Connected via low-latency, high-bandwidth, redundant networking
    - Enable high availability through multi-AZ deployments
    - Protect applications from datacenter-level failures
    
    **Service Scopes:**
    - **Zonal services:** Resources tied to specific AZs (EC2 instances, RDS, etc.)
    - **Regional services:** Automatically span multiple AZs (S3, DynamoDB, etc.)
    - **Global services:** Single instance serving all regions (IAM, Route 53, CloudFront)
    """)
    
    st.header("Points of Presence (PoP)")
    st.markdown("""
    Edge locations and regional edge caches that bring content closer to end users.
    
    **Key Points:**
    - 600+ Edge Locations and 13 regional mid-tier regional cache servers worldwide
    - Enable Amazon CloudFront to deliver content with low latency
    - Used by CloudFront, Route 53, AWS WAF, and AWS Shield
    - Help reduce latency for global users by caching content closer to them
    """)
    
    display_quiz("global_infrastructure")

# Function for CloudFront page
def cloudfront_page():
    st.title("Amazon CloudFront")
    
    try:
        st.image(aws_images["cloudfront"], width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("Content Delivery Network (CDN)")
    st.markdown("""
    Amazon CloudFront is a fast content delivery network (CDN) service that securely delivers data, videos, applications, and APIs to customers globally with low latency and high transfer speeds.
    
    **Key Benefits:**
    - **Improved Performance:** Delivers content from edge locations closest to users
    - **High Availability:** Built on AWS's global infrastructure
    - **Cost-Effective:** Pay only for the content delivered
    - **Security Integration:** Works with AWS Shield, AWS WAF, and Route 53
    - **Programmable:** Customize with Lambda@Edge
    
    **How CloudFront Works:**
    1. User requests content from your website/application
    2. DNS routes request to nearest CloudFront edge location
    3. CloudFront checks its cache for requested object
    4. If object is in cache, CloudFront returns it to user
    5. If not in cache, CloudFront forwards request to origin server
    6. Origin server sends object to edge location
    7. CloudFront delivers object to user and caches it for future requests
    """)
    
    st.header("Regional Edge Caches")
    st.markdown("""
    Regional edge caches sit between your origin servers and global edge locations.
    
    **Key Points:**
    - Larger than individual edge locations
    - Help cache content that isn't popular enough to stay at edge locations
    - Reduce load on origin servers
    - Content stays in regional edge caches longer
    - Particularly useful for:
      - User-generated content
      - E-commerce assets
      - News and event-related content
    
    **How Regional Edge Caches Work:**
    1. If content isn't at the edge location, request goes to nearest regional edge cache
    2. If content is at regional edge cache, it's forwarded to the edge location
    3. If not at regional cache, request goes to origin server
    4. Content is cached at both regional edge cache and edge location for future requests
    """)
    
    st.header("Key Features")
    st.markdown("""
    - **Origin Shield:** Additional caching layer to reduce load on origins
    - **Cache Behaviors:** Different caching strategies for different content paths
    - **Security Features:** 
      - Origin Access Identity (OAI)
      - Signed URLs and Cookies for private content
      - Field-level encryption
    - **Real-time Logs:** Monitor and analyze viewer behavior
    - **Edge Computing:** Lambda@Edge for customized content delivery
    """)
    
    display_quiz("cloudfront")

# Function for IAM page
def iam_page():
    st.title("Identity and Access Management (IAM)")
    
    try:
        st.image(aws_images["iam"], width=700)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is IAM?")
    st.markdown("""
    AWS Identity and Access Management (IAM) helps you securely control access to AWS resources by managing who is authenticated and authorized to use them.
    
    **Key Concepts:**
    - **Authentication:** Verifying identity (who you are)
    - **Authorization:** Determining access rights (what you can do)
    - **Principal:** Entity requesting access (user, role, application)
    - **Request:** Action on a resource (API call to AWS)
    - **Evaluation:** Checking permissions for the request
    - **Decision:** Allow or deny based on policies
    """)
    
    st.header("Principle of Least Privilege")
    st.markdown("""
    A core security best practice that involves granting only the permissions required to perform a task.
    
    **Key Points:**
    - Start with minimum permissions and grant additional as needed
    - Regularly review and remove unused permissions
    - Use permission boundaries to set maximum permissions
    - Implement just-in-time access rather than permanent permissions
    - Helps reduce security risks and potential blast radius
    """)
    
    st.header("IAM Users and Groups")
    st.markdown("""
    **IAM Users:**
    - Entities that represent people or applications that interact with AWS
    - Each user has a unique name and credentials
    - Can access AWS via:
      - Console (username/password)
      - API/CLI (access keys)
      - SDK (access keys)
    
    **IAM Groups:**
    - Collections of IAM users
    - Used to assign permissions to multiple users at once
    - Users can belong to multiple groups
    - Groups cannot be nested (no groups within groups)
    - Simplify permission management
    """)
    
    st.header("AWS Organizations")
    
    try:
        st.image(aws_images["organizations"], width=700)
    except:
        st.warning("Image could not be displayed")
        
    st.markdown("""
    An account management service that enables consolidation and organization of multiple AWS accounts.
    
    **Key Features:**
    - **Centralized Management:** Manage multiple accounts from a single place
    - **Consolidated Billing:** Single payment for all accounts
    - **Hierarchical Organization:** Group accounts into organizational units (OUs)
    - **Service Control Policies (SCPs):** Apply permission guardrails across accounts
    
    **Best Practices:**
    - Organize OUs by function rather than company structure
    - Create dedicated accounts for security, audit, and billing
    - Use SCPs to enforce compliance requirements
    - Implement a multi-account strategy for better isolation and security
    """)
    
    display_quiz("iam")

# Function for IAM Policies page
def iam_policies_page():
    st.title("IAM Policies")
    
    try:
        st.image(aws_images["iam_policies"], width=700)
    except:
        st.warning("Image could not be displayed")
    
    st.header("Policy Types")
    st.markdown("""
    IAM policies define permissions and are used to manage access in AWS.
    
    **Major Policy Types:**
    - **Identity-based policies:** Attached to IAM users, groups, or roles
    - **Resource-based policies:** Attached to resources (e.g., S3 bucket policies)
    - **Permissions boundaries:** Set maximum permissions for an IAM entity
    - **Service control policies (SCPs):** Used with AWS Organizations to limit permissions
    - **Access control lists (ACLs):** Legacy, control access to resources
    - **Session policies:** Passed during role assumption to further restrict permissions
    """)
    
    st.header("Policy Evaluation Logic")
    st.markdown("""
    How AWS evaluates policies to determine if a request should be allowed or denied:
    
    1. **Default denial:** All requests start as implicitly denied
    2. **Evaluate applicable policies:** Identity-based, resource-based, etc.
    3. **Any explicit DENY?** If yes, final decision is DENY
    4. **Any explicit ALLOW?** If yes, final decision is ALLOW, otherwise DENY
    
    **Important Rules:**
    - There is no "implicit allow" - access must be explicitly allowed
    - An explicit deny always overrides any allows
    - Resource-based policies are evaluated in parallel with identity-based policies
    """)
    
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
    
    **ARN Format:**
    ```
    arn:partition:service:region:account-id:resource-type/resource-id
    ```
    
    **Examples:**
    - S3 bucket: `arn:aws:s3:::my-bucket`
    - EC2 instance: `arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef0`
    - IAM user: `arn:aws:iam::123456789012:user/username`
    
    **Note:** Some global resources omit region and/or account ID in their ARNs.
    """)
    
    st.header("IAM Roles")
    st.markdown("""
    IAM roles provide temporary security credentials for AWS resources or external identities.
    
    **Key Characteristics:**
    - Not associated with a specific person
    - Assumed by users, applications, or services
    - Temporary credentials with defined lifetime
    - No long-term credentials like passwords or access keys
    
    **Common Use Cases:**
    - EC2 instance roles
    - Lambda execution roles
    - Cross-account access
    - Federation with external identity providers
    """)
    
    display_quiz("iam_policies")

# Function for STS page
def sts_page():
    st.title("AWS Security Token Service (STS)")
    
    try:
        st.image(aws_images["sts"], width=700)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is STS?")
    st.markdown("""
    AWS Security Token Service (STS) enables you to request temporary, limited-privilege credentials for AWS IAM users or users from external identity providers.
    
    **Key Features:**
    - **Temporary Credentials:** Short-lived access keys that expire automatically
    - **Limited Privileges:** Define specific permissions for the session
    - **Secure Federation:** Integrate with external identity systems
    - **Delegation:** Allow services to act on your behalf
    """)
    
    st.header("Common STS Operations")
    st.markdown("""
    - **AssumeRole:** Get temporary credentials to access AWS resources
    - **AssumeRoleWithWebIdentity:** Federation with OIDC providers like Google, Facebook, etc.
    - **AssumeRoleWithSAML:** Federation with SAML 2.0 providers
    - **GetSessionToken:** Get temporary credentials for an IAM user
    - **GetFederationToken:** Get temporary credentials for a federated user
    """)
    
    st.header("Trust Policies")
    st.markdown("""
    A trust policy defines which principals (users, services, accounts) can assume a role.
    
    **Example Trust Policy:**
    ```json
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
    ```
    
    **Security Best Practices:**
    - Use external IDs for third-party access
    - Apply conditions like source IP restrictions
    - Set appropriate maximum session duration
    - Implement MFA for role assumption
    """)
    
    st.header("Revoking Temporary Credentials")
    st.markdown("""
    How to handle situations where temporary credentials need to be revoked before expiration:
    
    **Options:**
    1. **Modify trust policy** to prevent new role assumptions (doesn't affect active sessions)
    2. **Add inline deny policy** with the `AWSRevokeOlderSessions` condition key
    3. **Change permissions** attached to the role (affects all new and existing sessions)
    
    **Example Deny Policy for Revocation:**
    ```json
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
    ```
    """)
    
    display_quiz("sts")

# Function for S3 page
def s3_page():
    st.title("Amazon Simple Storage Service (S3)")
    
    try:
        st.image(aws_images["s3"], width=700)
    except:
        st.warning("Image could not be displayed")
    
    st.header("S3 Overview")
    st.markdown("""
    Amazon S3 (Simple Storage Service) provides infinitely scalable, highly durable object storage in the AWS Cloud.
    
    **Key Concepts:**
    - **Object-based storage:** Store any type of file up to 5TB
    - **Buckets:** Containers for objects with globally unique names
    - **Objects:** Files and metadata stored in S3
    - **Keys:** Unique identifiers for objects within a bucket
    - **Durability:** 99.999999999% (11 nines) durability
    - **Availability:** Varies by storage class (typically 99.99%)
    """)
    
    st.header("S3 Storage Classes")
    st.markdown("""
    | Storage Class | Use Case | Availability | Retrieval Time | Minimum Storage Duration |
    |---------------|----------|--------------|----------------|-------------------------|
    | S3 Standard | Active, frequently accessed data | 99.99% | Milliseconds | None |
    | S3 Intelligent-Tiering | Data with changing access patterns | 99.9% | Milliseconds | None |
    | S3 Standard-IA | Infrequently accessed data | 99.9% | Milliseconds | 30 days |
    | S3 One Zone-IA | Re-creatable, infrequently accessed | 99.5% | Milliseconds | 30 days |
    | S3 Glacier Instant Retrieval | Archive data needing immediate access | 99.9% | Milliseconds | 90 days |
    | S3 Glacier Flexible Retrieval | Archive data with flexible retrieval | 99.99% | Minutes to hours | 90 days |
    | S3 Glacier Deep Archive | Long-term archiving, rare access | 99.99% | Hours | 180 days |
    | S3 Express One Zone | High-performance data, single AZ | 99.5% | Single-digit ms | None |
    """)
    
    st.header("S3 Bucket Policies")
    st.markdown("""
    Resource-based policies attached to S3 buckets that grant or deny access permissions.
    
    **Key Elements:**
    - **Principal:** Who the policy applies to (users, roles, accounts)
    - **Effect:** Allow or Deny
    - **Action:** S3 operations (GetObject, PutObject, etc.)
    - **Resource:** Buckets and objects the policy applies to
    - **Condition:** Optional restrictions on when policy applies
    
    **Example Policy:**
    ```json
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
    ```
    """)
    
    st.header("S3 Transfer Acceleration")
    st.markdown("""
    Feature that enables fast, easy, and secure transfers of files over long distances between your client and an S3 bucket.
    
    **Key Points:**
    - Uses AWS CloudFront's globally distributed edge locations
    - Routes data through AWS backbone network
    - Optimizes network protocols for long-distance transfers
    - Especially useful for:
      - Global uploads to centralized buckets
      - Regular transfers across continents
      - Utilizing available bandwidth
      - Applications uploading from many global locations
    """)
    
    st.header("S3 Security Features")
    st.markdown("""
    - **Bucket policies:** Resource-based policies for access control
    - **ACLs:** Legacy access control (less recommended now)
    - **IAM policies:** Identity-based policies for access control
    - **Block Public Access:** Settings to prevent public access
    - **Encryption:** Server-side (SSE-S3, SSE-KMS, SSE-C) and client-side options
    - **Object Lock:** Prevent deletion or overwriting for fixed time or indefinitely
    - **Versioning:** Maintain multiple versions of objects
    - **Access Points:** Named network endpoints with specific permissions
    - **VPC Endpoints:** Private connections from VPC to S3
    """)
    
    display_quiz("s3")

# Sidebar menu
st.sidebar.title("AWS Solutions Architect")
st.sidebar.image("https://a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_1200x630.png", width=200)

menu = st.sidebar.radio(
    "Navigation",
    ["Home", 
     "AWS Global Infrastructure", 
     "Amazon CloudFront", 
     "Identity and Access Management", 
     "IAM Policies",
     "Amazon S3", 
    #  "AWS Organizations", 
     "Security Token Service (STS)"]
)

# Display selected page
if menu == "Home":
    home_page()
elif menu == "AWS Global Infrastructure":
    global_infrastructure_page()
elif menu == "Amazon CloudFront":
    cloudfront_page()
elif menu == "Identity and Access Management":
    iam_page()
elif menu == "IAM Policies":
    iam_policies_page()
elif menu == "Amazon S3":
    s3_page()
# elif menu == "AWS Organizations":
#     organizations_page()
elif menu == "Security Token Service (STS)":
    sts_page()

# Footer
st.sidebar.divider()

# Progress tracking
if "total_score" not in st.session_state:
    st.session_state["total_score"] = 0
    st.session_state["total_attempted"] = 0

topics = ["global_infrastructure", "cloudfront", "iam", "iam_policies", "s3", "organizations", "sts"]
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
