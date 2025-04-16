
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
    "vpc": "https://d1.awsstatic.com/diagrams/VPC-basic-diagram.4f85c7a5f4fb7cb3ebc811144e33b6365e9b6e08.png",
    "route53": "https://d1.awsstatic.com/Route53/product-page-diagram_Amazon-Route-53_HIW.b32d51ffd32c0adfb5d31838ccc18bc926d9af28.png",
    "direct_connect": "https://d1.awsstatic.com/product-marketing/Direct Connect/direct-connect-diagram.485815d1dd3169b913bd3d53e9628f81c29dae79.png",
    "transit_gateway": "https://d1.awsstatic.com/product-marketing/transit-gateway/tgw-after.25f7a5cc5e37b3d795a4844ddc75982af8ae24cf.png",
    "security": "https://d1.awsstatic.com/security-center/security-design.d7b4437babfcab9d5565825a8e3262f49e31253f.png",
    "global_accelerator": "https://d1.awsstatic.com/product-marketing/Globalaccelerator/product-page-diagram_Global-Accelrator_HIW@2x.dd86ff5530bd791a32c61a78b8b1979177e94558.png",
    "storage_gateway": "https://d1.awsstatic.com/cloud-storage/product-page-diagram_AWS-Storage-Gateway_HIW.82fe9f786706c1e2d928a40e0ac65c3736c6ee6c.png",
}

# Scenario-based quiz questions
quiz_data = {
    "vpc": [
        {
            "question": "A financial services company is designing their VPC architecture to meet strict regulatory requirements for network isolation. They need to securely connect multiple environments (development, testing, and production) while ensuring that development traffic cannot directly access production resources. Which VPC design best meets these requirements?",
            "options": [
                "Create a single VPC with separate subnets for each environment and use Network ACLs to control traffic between subnets",
                "Create separate VPCs for each environment and use VPC peering with restrictive route tables to control access between environments",
                "Create a shared VPC using AWS Resource Access Manager and assign specific subnets to different accounts",
                "Create a single VPC with separate security groups for each environment and reference security group IDs to control access",
                "Create a Transit Gateway with route tables configured for each environment and enable appliance mode"
            ],
            "answer": "Create separate VPCs for each environment and use VPC peering with restrictive route tables to control access between environments"
        },
        {
            "question": "A company is planning their VPC CIDR block strategy. They currently have on-premises networks using 10.0.0.0/16 and 192.168.0.0/16 address spaces. They plan to connect these networks to AWS using Direct Connect in the future and potentially merge with another company that uses 172.16.0.0/16. What VPC CIDR block strategy should they adopt?",
            "options": [
                "Use 10.0.0.0/8 for their VPC to ensure they have enough IP addresses",
                "Use 172.31.0.0/16 as it's the default VPC CIDR and will avoid conflicts",
                "Use a CIDR block from the 100.64.0.0/10 range as it's specifically designed for cloud environments",
                "Use a public IP range to avoid any potential private IP conflicts",
                "Use a CIDR block from RFC 1918 private address space that doesn't overlap with current or potential future networks, such as 172.20.0.0/16"
            ],
            "answer": "Use a CIDR block from RFC 1918 private address space that doesn't overlap with current or potential future networks, such as 172.20.0.0/16"
        },
        {
            "question": "A company runs a multi-tier web application in AWS. The web tier needs to communicate with the internet, but the application and database tiers should not have direct internet access. The application tier does need to download updates from public repositories. Which architecture meets these requirements with the highest security?",
            "options": [
                "Place all tiers in public subnets with security groups restricting access",
                "Place web tier in public subnet, application and database tiers in private subnets with a NAT Gateway for outbound traffic",
                "Place all tiers in private subnets and use interface VPC endpoints for all communications",
                "Place web and application tiers in public subnets, and database tier in a private subnet",
                "Place all tiers in private subnets and use a proxy server in a public subnet"
            ],
            "answer": "Place web tier in public subnet, application and database tiers in private subnets with a NAT Gateway for outbound traffic"
        },
        {
            "question": "A healthcare company has strict compliance requirements that mandate all network traffic must be inspected for sensitive data before leaving their controlled environment. They need to allow their applications running on EC2 instances to access AWS services like S3 and DynamoDB. Which VPC connectivity option should they implement?",
            "options": [
                "Configure a NAT Gateway to route traffic to AWS services",
                "Use an Internet Gateway with restrictive security groups",
                "Set up Gateway VPC Endpoints for S3 and DynamoDB, and Interface VPC Endpoints for other services",
                "Deploy a proxy server to inspect all outbound traffic",
                "Use AWS PrivateLink to connect directly to AWS services"
            ],
            "answer": "Set up Gateway VPC Endpoints for S3 and DynamoDB, and Interface VPC Endpoints for other services"
        },
        {
            "question": "A company is deploying an application that handles sensitive financial data. They want to ensure that if one EC2 instance is compromised, an attacker cannot easily reach other instances in the same subnet. Which combination of security controls should they implement?",
            "options": [
                "Use security groups with tight inbound/outbound rules and implement host-based firewalls on each EC2 instance",
                "Place each EC2 instance in a separate subnet with different NACLs",
                "Use security groups that only allow communication to specific instance IDs and implement restrictive NACLs on the subnet level",
                "Deploy all instances in public subnets with different route tables",
                "Use a single security group for all instances but implement different IAM roles"
            ],
            "answer": "Use security groups that only allow communication to specific instance IDs and implement restrictive NACLs on the subnet level"
        }
    ],
    "route53": [
        {
            "question": "A global e-commerce company operates websites in multiple AWS regions to serve customers across the world. They want to route users to the closest region that has healthy infrastructure, but need a backup option if a regional outage occurs. Which Route 53 routing configuration provides this capability?",
            "options": [
                "Simple routing with multiple IP addresses to load balance across regions",
                "Geolocation routing with latency-based failover configured",
                "Weighted routing with health checks on regional endpoints",
                "Failover routing with active-passive configuration across regions",
                "Latency-based routing with health checks and failover records to a secondary region"
            ],
            "answer": "Latency-based routing with health checks and failover records to a secondary region"
        },
        {
            "question": "A financial services company needs to perform a blue/green deployment of a critical application that serves customers worldwide. They want to gradually shift traffic from the old version to the new version while monitoring for issues. Which Route 53 configuration best supports this requirement?",
            "options": [
                "Geolocation routing policy to target specific regions for the new deployment",
                "Simple routing with multiple IP addresses",
                "Weighted routing policy with adjustable weights between the old and new environments",
                "Latency-based routing to automatically direct users to the fastest environment",
                "Failover routing with health checks to automatically switch to the new environment"
            ],
            "answer": "Weighted routing policy with adjustable weights between the old and new environments"
        },
        {
            "question": "A multinational corporation must comply with data sovereignty regulations that require customer data to be processed within specific geographic regions. They have deployed replicated infrastructure in multiple AWS regions but need to ensure users are always routed to the legally appropriate region based on their country. Which Route 53 configuration should they use?",
            "options": [
                "Latency-based routing to send users to the fastest region",
                "Geolocation routing with rules defined for each country and continent",
                "IP-based routing with CIDR blocks mapping to different regions",
                "Weighted routing with health checks",
                "Multi-value answer routing with health checks on each regional endpoint"
            ],
            "answer": "Geolocation routing with rules defined for each country and continent"
        },
        {
            "question": "A gaming company runs a matchmaking service that needs to connect players to the game server with the least number of active connections to ensure balanced gameplay. The company has deployed game servers in multiple regions. Which Route 53 routing policy should they use in combination with other AWS services?",
            "options": [
                "Latency-based routing with CloudFront distribution in front of each region",
                "Geolocation routing with Lambda@Edge to count active connections",
                "Weighted routing with DynamoDB to store connection counts and Lambda to update weights",
                "Multivalue answer routing with health checks that verify connection capacity",
                "Failover routing with primary and secondary regions based on capacity"
            ],
            "answer": "Weighted routing with DynamoDB to store connection counts and Lambda to update weights"
        },
        {
            "question": "A company has a complex microservices architecture deployed across multiple VPCs in the same AWS region. They need internal services to discover and communicate with each other without exposing these endpoints to the internet. Which Route 53 feature should they use?",
            "options": [
                "Route 53 Resolver with forwarding rules",
                "Route 53 public hosted zones with VPC peering",
                "Route 53 private hosted zones associated with each VPC",
                "Route 53 traffic flow with private DNS records",
                "Route 53 health checks with private endpoints"
            ],
            "answer": "Route 53 private hosted zones associated with each VPC"
        }
    ],
    "direct_connect": [
        {
            "question": "A financial institution needs to establish a connection to AWS with guaranteed bandwidth, consistent latency, and enhanced security for their transaction processing systems. They process over 5TB of data daily between their on-premises data center and AWS. The connection must be redundant with no single point of failure. Which AWS Direct Connect configuration provides the most reliable solution?",
            "options": [
                "A single 1Gbps Direct Connect connection with a VPN backup",
                "Two 10Gbps Direct Connect connections from a single Direct Connect location to two different AWS regions",
                "Two Direct Connect connections from different Direct Connect locations to the same AWS region, each connecting to separate devices in the customer network",
                "One 10Gbps Direct Connect connection with AWS Transit Gateway for redundancy",
                "Multiple hosted Direct Connect connections from different providers aggregated using LAG"
            ],
            "answer": "Two Direct Connect connections from different Direct Connect locations to the same AWS region, each connecting to separate devices in the customer network"
        },
        {
            "question": "A company needs to connect their on-premises environment to multiple VPCs in different AWS regions for a global application deployment. They require consistent network performance and need to minimize network transit costs. The solution should scale as they add more VPCs in the future. Which Direct Connect architecture should they implement?",
            "options": [
                "Set up a Direct Connect gateway and connect multiple VPCs across regions through VPC peering",
                "Establish individual Direct Connect connections to each region where VPCs are located",
                "Configure a Direct Connect connection to one region and use inter-region VPC peering for connectivity to VPCs in other regions",
                "Implement a Direct Connect connection to a Transit Gateway in one region and use inter-region Transit Gateway peering",
                "Set up a Direct Connect gateway and connect it to multiple VPCs across different regions using Transit Virtual Interfaces"
            ],
            "answer": "Set up a Direct Connect gateway and connect it to multiple VPCs across different regions using Transit Virtual Interfaces"
        },
        {
            "question": "A healthcare organization needs to access AWS services from their on-premises network while meeting strict regulatory requirements that prohibit any data from traversing the public internet. They need to access both VPC resources and AWS public services like S3 and DynamoDB. Which Direct Connect configuration should they use?",
            "options": [
                "Set up a private VIF for VPC access and use VPC endpoints for AWS services",
                "Configure a private VIF for VPC access and a public VIF for AWS service access",
                "Use a transit VIF with Transit Gateway and configure VPC endpoints for AWS services",
                "Set up a private VIF with proxy servers in the VPC to access AWS services",
                "Use a hosted Direct Connect connection with a VPN overlay for encryption"
            ],
            "answer": "Configure a private VIF for VPC access and a public VIF for AWS service access"
        },
        {
            "question": "A company is migrating their data warehouse to AWS and needs to transfer 500TB of historical data initially, followed by incremental daily transfers of about 50GB. They want the most cost-effective solution that provides dedicated throughput. Which approach should they take?",
            "options": [
                "Use AWS Snowball for initial data transfer and set up a 1Gbps Direct Connect connection for ongoing transfers",
                "Set up a 10Gbps Direct Connect connection for both initial and ongoing transfers",
                "Use AWS DataSync over the internet for both initial and ongoing transfers",
                "Use AWS Snowmobile for initial transfer and a Site-to-Site VPN for ongoing transfers",
                "Set up a 1Gbps Direct Connect connection and use multiple parallel transfer sessions for the initial data"
            ],
            "answer": "Use AWS Snowball for initial data transfer and set up a 1Gbps Direct Connect connection for ongoing transfers"
        },
        {
            "question": "A multinational corporation with multiple data centers plans to implement Direct Connect for AWS connectivity. They need to ensure traffic between their on-premises network and AWS is encrypted while maintaining the performance benefits of Direct Connect. Which solution should they implement?",
            "options": [
                "Configure a private VIF and rely on application-level encryption for sensitive data",
                "Set up public VIFs and use SSL/TLS for all services accessed through AWS public endpoints",
                "Establish a Direct Connect connection and run a site-to-site VPN over the private VIF",
                "Use a hosted Direct Connect connection with MACsec encryption enabled",
                "Implement a transit VIF connected to a Transit Gateway and use AWS Network Firewall for inspection"
            ],
            "answer": "Establish a Direct Connect connection and run a site-to-site VPN over the private VIF"
        }
    ],
    "transit_gateway": [
        {
            "question": "A large enterprise has grown through acquisitions and now has 50+ VPCs across multiple AWS accounts. They need to centralize connectivity between these VPCs and to their on-premises network. They also require the ability to isolate certain environments from others. Which Transit Gateway configuration meets these requirements?",
            "options": [
                "Create a Transit Gateway with a single route table shared across all VPCs",
                "Create a Transit Gateway with multiple route tables, assigning VPCs to appropriate route tables based on security requirements",
                "Create multiple Transit Gateways, one for each security domain, and connect them via VPC peering",
                "Create a Transit Gateway and use security groups to control traffic between VPCs",
                "Use AWS Network Firewall with a single Transit Gateway route table to filter traffic between VPCs"
            ],
            "answer": "Create a Transit Gateway with multiple route tables, assigning VPCs to appropriate route tables based on security requirements"
        },
        {
            "question": "A company operates in multiple AWS regions and needs to connect all their VPCs together while minimizing network latency and operational overhead. They need to ensure that traffic between VPCs in the same region doesn't traverse between regions. Which architecture provides this connectivity model?",
            "options": [
                "Deploy a Transit Gateway in each region and connect them using Transit Gateway peering",
                "Use VPC peering between all VPCs across regions",
                "Deploy a Transit Gateway in a central region and connect all VPCs to it",
                "Use Direct Connect gateways to connect VPCs across regions",
                "Implement AWS Cloud WAN to manage global network connectivity"
            ],
            "answer": "Deploy a Transit Gateway in each region and connect them using Transit Gateway peering"
        },
        {
            "question": "A financial services company needs to inspect all traffic between their development and production VPCs for security compliance. They want to centralize inspection while maintaining high throughput. Which Transit Gateway configuration best meets these requirements?",
            "options": [
                "Configure VPC peering between development and production VPCs with security groups to filter traffic",
                "Deploy a Transit Gateway and use AWS Network Firewall in a security VPC as a centralized inspection point",
                "Enable Transit Gateway flow logs and use Amazon Detective for traffic analysis",
                "Configure Transit Gateway appliance mode and deploy a third-party firewall appliance in a security VPC",
                "Use Transit Gateway route tables to direct traffic to a VPC endpoint for AWS Firewall Manager"
            ],
            "answer": "Configure Transit Gateway appliance mode and deploy a third-party firewall appliance in a security VPC"
        },
        {
            "question": "A company has a hybrid cloud architecture with workloads in both AWS and on-premises data centers. They need a solution that provides consistent connectivity between all environments with the ability to centrally manage routing policies. The solution should support future expansion to additional cloud providers. Which architecture best meets these requirements?",
            "options": [
                "Use Transit Gateway connected to on-premises via Site-to-Site VPN",
                "Implement Direct Connect with private VIFs to each VPC",
                "Connect Transit Gateway to on-premises via Direct Connect and use Transit Gateway Connect for dynamic routing",
                "Use Transit Gateway connected to Direct Connect Gateway for on-premises connectivity and Transit Gateway peering for cross-region connectivity",
                "Implement Cloud WAN with core network policies to manage connectivity across all environments"
            ],
            "answer": "Use Transit Gateway connected to Direct Connect Gateway for on-premises connectivity and Transit Gateway peering for cross-region connectivity"
        },
        {
            "question": "A retail company is redesigning their network architecture to improve performance for cross-VPC communication. They have noticed that traffic between EC2 instances in different VPCs is experiencing higher than expected latency, especially for applications that require many small packets to be exchanged quickly. Which Transit Gateway feature should they enable to improve performance?",
            "options": [
                "Enable Transit Gateway flow logs to identify bottlenecks",
                "Use Transit Gateway Connect for higher bandwidth",
                "Enable multicast support on the Transit Gateway",
                "Configure Transit Gateway to use Equal Cost Multipath routing",
                "Enable appliance mode on the Transit Gateway attachment"
            ],
            "answer": "Enable appliance mode on the Transit Gateway attachment"
        }
    ],
    "security_groups_nacls": [
        {
            "question": "A company is designing a multi-tier web application in AWS with web, application, and database tiers. They need to implement security controls that provide defense-in-depth while minimizing administrative overhead. Which combination of security controls best meets these requirements?",
            "options": [
                "Create a single security group for all tiers and use NACLs to filter traffic between subnets",
                "Use separate security groups for each tier that reference the security group IDs of tiers they communicate with, and use default NACLs",
                "Create separate security groups and NACLs for each tier with identical rules to ensure consistent filtering",
                "Use a single NACL for all subnets and separate security groups with IP-based rules",
                "Implement security groups with broad allow rules and strict NACLs for precise control"
            ],
            "answer": "Use separate security groups for each tier that reference the security group IDs of tiers they communicate with, and use default NACLs"
        },
        {
            "question": "A financial services company needs to implement a solution that blocks specific IP addresses that have been identified as sources of malicious traffic. These IP addresses change frequently, and the blocks need to be applied to all resources in a subnet. Which security control should they use?",
            "options": [
                "Security groups with deny rules for each malicious IP address",
                "Network ACLs with deny rules for each malicious IP address",
                "VPC Flow Logs with automated remediation using Lambda",
                "Route tables that direct traffic from malicious IPs to a blackhole",
                "AWS WAF with IP-based rules applied to a load balancer"
            ],
            "answer": "Network ACLs with deny rules for each malicious IP address"
        },
        {
            "question": "An application running on EC2 instances processes sensitive healthcare data. The security team needs to implement controls that prevent any outbound connections to unauthorized external endpoints, regardless of port or protocol. Which combination of security controls achieves this with the least administrative overhead?",
            "options": [
                "Configure security group outbound rules to deny all traffic and explicitly allow required destinations",
                "Implement NACLs with deny rules for all external destinations except approved IP ranges",
                "Configure security group outbound rules to allow only specific destinations and use NACLs as a backup control",
                "Use VPC endpoints for AWS services and configure security groups to allow only VPC endpoint traffic",
                "Deploy a transit gateway with route tables that prevent external traffic"
            ],
            "answer": "Configure security group outbound rules to allow only specific destinations and use NACLs as a backup control"
        },
        {
            "question": "A company runs a multi-tenant SaaS application where each tenant's data must be strictly isolated from other tenants. They use a microservices architecture with multiple EC2 instances per tenant. The security team has identified a potential risk where a compromised service could access data from other tenants. Which security design best mitigates this risk?",
            "options": [
                "Assign each tenant to a separate VPC and use VPC peering for shared services",
                "Place all tenants in the same VPC but in different subnets with NACLs controlling access",
                "Use security groups that reference tenant-specific security group IDs rather than IP ranges",
                "Deploy a separate EC2 instance for each tenant and use instance-level firewall rules",
                "Implement IAM roles with tenant context and rely on API-level authorization"
            ],
            "answer": "Use security groups that reference tenant-specific security group IDs rather than IP ranges"
        },
        {
            "question": "A company is deploying an application that will receive traffic from thousands of unpredictable client IP addresses but should only send responses back to those clients. The security team wants to implement the principle of least privilege while minimizing the administrative overhead of maintaining security rules. Which security configuration is most appropriate?",
            "options": [
                "Configure NACLs to allow inbound traffic from 0.0.0.0/0 and outbound traffic to 0.0.0.0/0",
                "Configure security groups to allow inbound traffic from 0.0.0.0/0 on specific ports and rely on their stateful nature for outbound responses",
                "Implement both NACLs and security groups with explicit allow rules for both directions",
                "Configure NACLs with allow rules for inbound and outbound traffic to 0.0.0.0/0 on ephemeral ports",
                "Use security groups with specific IP-based allow rules that are automatically updated by Lambda"
            ],
            "answer": "Configure security groups to allow inbound traffic from 0.0.0.0/0 on specific ports and rely on their stateful nature for outbound responses"
        }
    ],
    "global_accelerator": [
        {
            "question": "A global gaming company has deployed their matchmaking service in multiple AWS regions to support players worldwide. They need to reduce latency and improve connection stability for players, especially during regional Internet disruptions. Which configuration of AWS Global Accelerator best meets these requirements?",
            "options": [
                "Configure Global Accelerator with endpoint groups in each region but set a higher traffic dial percentage for the newest AWS regions",
                "Use Global Accelerator with custom routing to send players to specific game servers based on their skill level",
                "Set up Global Accelerator with endpoint groups in each region and equal weights, with health checks configured to detect regional disruptions",
                "Deploy Global Accelerator with TCP/UDP listeners and implement client affinity to keep players connected to the same region",
                "Configure Global Accelerator with one endpoint group in the central US region to minimize maximum latency for all players"
            ],
            "answer": "Set up Global Accelerator with endpoint groups in each region and equal weights, with health checks configured to detect regional disruptions"
        },
        {
            "question": "A financial services company operates a trading platform that requires ultra-low latency and high availability. They currently use Route 53 with latency-based routing to direct users to the closest AWS region. Despite this, they're experiencing inconsistent performance during market volatility. Which solution would provide the most consistent low-latency experience?",
            "options": [
                "Change to Route 53 geolocation routing to ensure users connect to endpoints in their country",
                "Implement AWS Global Accelerator with static IP addresses and anycast routing to bring traffic onto the AWS global network as quickly as possible",
                "Deploy CloudFront distributions in front of application load balancers in each region",
                "Use inter-region VPC peering to route traffic internally within AWS",
                "Implement Route 53 health checks with faster failure detection thresholds"
            ],
            "answer": "Implement AWS Global Accelerator with static IP addresses and anycast routing to bring traffic onto the AWS global network as quickly as possible"
        },
        {
            "question": "A multinational company is migrating their customer-facing API platform to AWS. This platform serves mobile and web applications globally. The security team requires that all client applications use a fixed set of IP addresses to access the API for allowlisting purposes. The platform needs to be deployed in multiple regions for resiliency. Which solution best meets these requirements?",
            "options": [
                "Deploy Network Load Balancers in each region and use Route 53 latency-based routing",
                "Use Application Load Balancers in each region with static IP addresses through Elastic IPs",
                "Implement AWS Global Accelerator with two static IP addresses pointing to Application Load Balancers in each region",
                "Configure CloudFront distributions with AWS WAF for IP-based filtering",
                "Set up API Gateway regional endpoints with Route 53 geoproximity routing"
            ],
            "answer": "Implement AWS Global Accelerator with two static IP addresses pointing to Application Load Balancers in each region"
        },
        {
            "question": "A SaaS provider offers a data processing service that requires clients to upload large files and then receive processed results. Clients are distributed globally and have complained about inconsistent upload speeds. The provider wants to improve the upload performance while keeping a single entry point for their service. Which Global Accelerator configuration would best address this issue?",
            "options": [
                "Configure Global Accelerator with TCP listeners pointing to Network Load Balancers in each region",
                "Set up Global Accelerator with client affinity disabled to distribute uploads across regions",
                "Use Global Accelerator with UDP listeners for faster file transfers",
                "Implement Global Accelerator with endpoint weights favoring regions with more processing capacity",
                "Configure Global Accelerator with health checks that measure upload bandwidth capacity"
            ],
            "answer": "Configure Global Accelerator with TCP listeners pointing to Network Load Balancers in each region"
        },
        {
            "question": "A company provides real-time collaboration software and needs to improve their failover mechanism between AWS regions. Currently, they use Route 53 health checks with a 30-second failure detection threshold, but customers are reporting disruptions during regional issues. Which Global Accelerator feature would minimize client disruption during regional failures?",
            "options": [
                "Traffic dials to manually shift traffic during detected issues",
                "Custom routing to map specific users to specific regions",
                "Continuous health checks with 10-second intervals and automated failover within seconds",
                "CIDR IP address blocks for consistent routing",
                "Sticky sessions to maintain connection persistence"
            ],
            "answer": "Continuous health checks with 10-second intervals and automated failover within seconds"
        }
    ],
    "storage_gateway": [
        {
            "question": "A manufacturing company has 20TB of historic design files stored on a local NAS device that is running out of capacity. These files are rarely accessed but must be retained for compliance reasons. The engineering team occasionally needs read access to older files. They want to minimize on-premises storage while maintaining local access to recently used files. Which Storage Gateway configuration best meets these requirements?",
            "options": [
                "Deploy a Volume Gateway in stored mode to replicate the entire 20TB to S3",
                "Set up a File Gateway with a local cache size of 5TB and move all data to S3",
                "Use a Tape Gateway to back up all files to S3 Glacier Deep Archive",
                "Implement a Volume Gateway in cached mode with a 2TB local cache",
                "Deploy an FSx File Gateway to maintain SMB access to files"
            ],
            "answer": "Set up a File Gateway with a local cache size of 5TB and move all data to S3"
        },
        {
            "question": "A media production company has an on-premises workflow that generates 500GB of video files daily. These files need to be uploaded to AWS for processing and distribution. The company has a limited internet connection and needs to ensure that recently accessed files remain available locally during internet outages. Which Storage Gateway solution should they implement?",
            "options": [
                "Deploy a Volume Gateway in stored mode to maintain full copies locally",
                "Use a File Gateway with NFS mounts and configure a cache that can store 5 days of data",
                "Implement a Tape Gateway with virtual tapes for each day's content",
                "Set up AWS DataSync with scheduled transfers and local storage",
                "Use S3 Transfer Acceleration directly from the production workstations"
            ],
            "answer": "Use a File Gateway with NFS mounts and configure a cache that can store 5 days of data"
        },
        {
            "question": "A healthcare organization needs to store patient records in AWS for long-term retention while maintaining local access for recent records. They have a regulatory requirement to encrypt all data at rest and in transit, with keys managed by the organization. Which Storage Gateway configuration ensures compliance with these requirements?",
            "options": [
                "Deploy a Volume Gateway in cached mode with Amazon EBS encryption using customer-provided keys",
                "Use a File Gateway with S3 server-side encryption using AWS KMS customer managed keys",
                "Implement a Volume Gateway in stored mode with local encryption only",
                "Set up a File Gateway with NFS encryption and configure S3 bucket keys",
                "Use a Tape Gateway with client-side encryption before writing to virtual tapes"
            ],
            "answer": "Use a File Gateway with S3 server-side encryption using AWS KMS customer managed keys"
        },
        {
            "question": "A company is planning to migrate their legacy backup system to AWS. They currently use tape-based backups with a retention schedule requiring some tapes to be kept for 7 years. The IT team is familiar with their existing backup software and wants to minimize changes to their backup processes. Which Storage Gateway solution best fits this scenario?",
            "options": [
                "File Gateway mounted as a backup target with lifecycle policies to move older data to Glacier",
                "Volume Gateway in stored mode to create EBS snapshots on a backup schedule",
                "Tape Gateway integrated with the existing backup software, with virtual tapes stored in S3 Glacier and Deep Archive",
                "File Gateway with multiple file shares for different retention periods",
                "Direct backup to S3 using the backup software's cloud connector"
            ],
            "answer": "Tape Gateway integrated with the existing backup software, with virtual tapes stored in S3 Glacier and Deep Archive"
        },
        {
            "question": "A retail company has multiple branch locations each with local file servers. They want to implement a hybrid cloud solution that allows them to centrally manage these file servers in AWS while maintaining local access at each location. The solution should minimize storage costs and provide a familiar interface for users. Which approach meets these requirements?",
            "options": [
                "Deploy a Volume Gateway in each location connected to a central EBS volume",
                "Implement File Gateways at each location connected to a shared S3 bucket with appropriate IAM policies",
                "Use Amazon FSx File Gateway at each location connected to a centralized Amazon FSx for Windows File Server",
                "Set up a Direct Connect link from each location to a central Amazon EFS filesystem",
                "Deploy AWS Outposts with local S3 capability at each branch"
            ],
            "answer": "Use Amazon FSx File Gateway at each location connected to a centralized Amazon FSx for Windows File Server"
        }
    ]
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

# Function for home page
def home_page():
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(load_image_from_url(aws_images["home"]), width=300)
        except:
            st.error("Unable to load image")
    
    with col2:
        st.title("AWS Solutions Architect - Associate")
        st.header("Content Review – Session 2")
        st.markdown("""
        Welcome to the AWS Partner Certification Readiness program. This interactive guide will help you prepare 
        for the Solutions Architect - Associate certification. Navigate through the topics using the tabs above.
        
        Each section contains key concepts, important takeaways, and interactive quizzes to reinforce your learning.
        """)
    
    st.markdown("""
    <div class="aws-info-card">
        <h3>Topics covered:</h3>
        <p>
        • Virtual Private Cloud (VPC)<br>
        • Route 53 (DNS)<br>
        • AWS Direct Connect<br>
        • Transit Gateway<br>
        • Security Groups & NACLs<br>
        • AWS Global Accelerator<br>
        • AWS Storage Gateway
        </p>
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
    
    # Display overview section
    st.header("Overview")
    
    # Create a grid of service cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🌐 Networking Services</h4>
            <ul>
                <li><strong>VPC:</strong> Create isolated virtual networks</li>
                <li><strong>Route 53:</strong> Scalable DNS and domain registration</li>
                <li><strong>Direct Connect:</strong> Dedicated connectivity to AWS</li>
                <li><strong>Transit Gateway:</strong> Centralized connectivity hub</li>
                <li><strong>Global Accelerator:</strong> Improve global application availability</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>🔒 Security & Storage</h4>
            <ul>
                <li><strong>Security Groups:</strong> Instance-level virtual firewall</li>
                <li><strong>NACLs:</strong> Subnet-level security controls</li>
                <li><strong>Storage Gateway:</strong> Hybrid cloud storage integration</li>
                <li><strong>Encryption:</strong> Data protection in transit and at rest</li>
                <li><strong>AWS PrivateLink:</strong> Private connectivity to services</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Function for VPC page
def vpc_page():
    st.title("Virtual Private Cloud (VPC)")
    
    try:
        st.image(load_image_from_url(aws_images["vpc"]), width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is Amazon VPC?")
    st.markdown("""
    Amazon Virtual Private Cloud (Amazon VPC) is your network environment in the cloud. It enables you to provision a logically isolated section of the AWS Cloud where you can launch AWS resources in a virtual network that you define.
    
    **Key Features:**
    - Complete control over your virtual networking environment
    - Secure and isolated resources
    - Multiple connectivity options to meet your needs
    - Customizable network configurations
    """)
    
    st.header("VPC Components")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Core Components</h4>
            <ul>
                <li><strong>Subnets:</strong> Range of IP addresses in your VPC</li>
                <li><strong>Route Tables:</strong> Set of rules to determine where network traffic is directed</li>
                <li><strong>Internet Gateway:</strong> Enables communication between your VPC and the internet</li>
                <li><strong>NAT Gateway:</strong> Allows private subnet resources to access the internet</li>
                <li><strong>Security Groups:</strong> Virtual firewall controlling inbound and outbound traffic at the instance level</li>
                <li><strong>Network ACLs:</strong> Firewall controlling inbound and outbound traffic at the subnet level</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Advanced Components</h4>
            <ul>
                <li><strong>VPC Endpoints:</strong> Private connectivity to AWS services without internet gateway</li>
                <li><strong>VPC Peering:</strong> Connect VPCs to route traffic between them</li>
                <li><strong>Transit Gateway:</strong> Central hub to connect VPCs and on-premises networks</li>
                <li><strong>Shared VPC:</strong> Share subnets with other AWS accounts</li>
                <li><strong>Elastic IP:</strong> Static public IPv4 address for your instances</li>
                <li><strong>VPC Flow Logs:</strong> Capture network flow information for monitoring</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Public vs. Private Subnets")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h4>Public Subnet</h4>
            <ul>
                <li>Has a route to an Internet Gateway</li>
                <li>Resources can directly communicate with the internet</li>
                <li>Typically hosts public-facing resources like web servers</li>
                <li>Public IP addresses can be assigned to instances</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h4>Private Subnet</h4>
            <ul>
                <li>No direct route to an Internet Gateway</li>
                <li>Resources cannot directly communicate with the internet</li>
                <li>Requires a NAT Gateway for outbound internet access</li>
                <li>Typically hosts internal resources like databases</li>
                <li>Additional layer of security for sensitive workloads</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("IP Addressing")
    st.markdown("""
    <div class="aws-info-card">
        <h4>Key Considerations:</h4>
        <ul>
            <li>Plan your IP address space before creating a VPC</li>
            <li>VPC CIDR blocks can be between /16 and /28</li>
            <li>Consider future AWS region expansion</li>
            <li>Plan for connectivity to corporate networks</li>
            <li>Avoid overlapping IP spaces</li>
            <li>CIDR cannot be modified once created, but additional CIDRs can be added</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Security in VPC")
    st.subheader("Defense in Depth")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h4>Security Groups</h4>
            <p>Instance-level firewall (stateful)</p>
            <ul>
                <li>Allow rules only</li>
                <li>Evaluated as a whole</li>
                <li>Return traffic automatically allowed</li>
                <li>Can reference other security groups</li>
                <li>Attached to instances, not subnets</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h4>Network ACLs</h4>
            <p>Subnet-level firewall (stateless)</p>
            <ul>
                <li>Allow and deny rules</li>
                <li>Evaluated in order by rule number</li>
                <li>Return traffic must be explicitly allowed</li>
                <li>Can only reference IP addresses</li>
                <li>Automatically applied to all instances in subnet</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="aws-warning-card">
        <h4>Best Practice</h4>
        <p>Use both Security Groups and NACLs for a defense-in-depth approach. Security Groups are your primary defense for allowing specific traffic to instances, while NACLs provide a backup layer of defense at the subnet level.</p>
    </div>
    """, unsafe_allow_html=True)

# Function for Route 53 page
def route53_page():
    st.title("Amazon Route 53")
    
    try:
        st.image(load_image_from_url(aws_images["route53"]), width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is Amazon Route 53?")
    st.markdown("""
    Amazon Route 53 is a highly available and scalable cloud Domain Name System (DNS) web service. It connects user requests to AWS infrastructure and can route users to infrastructure outside of AWS.
    
    **Key Features:**
    - Domain registration
    - DNS routing
    - Health checking
    - 100% availability SLA
    - Global service
    """)
    
    st.header("DNS Functionality")
    st.markdown("""
    <div class="aws-card">
        <p>Route 53 translates user-friendly domain names (like www.example.com) into IP addresses (like 192.0.2.1) that computers use to connect to each other. It serves as the backbone for connecting users to your applications.</p>
        <h4>Primary Functions:</h4>
        <ol>
            <li><strong>Domain Registration:</strong> Register and manage domain names</li>
            <li><strong>DNS Routing:</strong> Direct traffic to the resources that host your applications</li>
            <li><strong>Health Checking:</strong> Monitor resource health and route traffic away from unhealthy resources</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Routing Policies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Basic Routing Policies</h4>
            <ul>
                <li><strong>Simple:</strong> Route traffic to a single resource</li>
                <li><strong>Weighted:</strong> Route traffic to multiple resources in proportions you specify</li>
                <li><strong>Failover:</strong> Route traffic to a primary resource or a standby resource if the primary is unavailable</li>
                <li><strong>Multivalue Answer:</strong> Respond to DNS queries with up to eight healthy records selected at random</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Advanced Routing Policies</h4>
            <ul>
                <li><strong>Latency-based:</strong> Route traffic to the region with the lowest latency</li>
                <li><strong>Geolocation:</strong> Route traffic based on the geographic location of your users</li>
                <li><strong>Geoproximity:</strong> Route traffic based on the geographic location of resources and optionally shift traffic from one location to another</li>
                <li><strong>IP-based:</strong> Route traffic based on users' IP addresses</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Public vs. Private Hosted Zones")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h4>Public Hosted Zones</h4>
            <ul>
                <li>Control how traffic is routed on the internet</li>
                <li>Accessible from the public internet</li>
                <li>Used for public-facing applications</li>
                <li>Requires domain registration</li>
                <li>Can be used with Route 53 health checks</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h4>Private Hosted Zones</h4>
            <ul>
                <li>Control routing within one or more VPCs</li>
                <li>Not accessible from the public internet</li>
                <li>Used for internal applications and services</li>
                <li>Requires enableDnsHostnames and enableDnsSupport VPC attributes</li>
                <li>Can be shared across VPCs (same or different accounts)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Health Checks")
    st.markdown("""
    <div class="aws-info-card">
        <p>Route 53 health checks monitor the health and performance of your web applications, web servers, and other resources.</p>
        <h4>Types of Health Checks:</h4>
        <ul>
            <li><strong>Endpoint monitoring:</strong> Check the health of a specified endpoint</li>
            <li><strong>Calculated health checks:</strong> Combine the results of multiple health checks into a single health check</li>
            <li><strong>CloudWatch alarm monitoring:</strong> Evaluate the state of a CloudWatch alarm</li>
        </ul>
        <p>Health checks can be used with DNS failover to route traffic away from unhealthy endpoints and to healthy endpoints.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="aws-warning-card">
        <h4>Important Note</h4>
        <p>Route 53 health checks can only monitor resources that are accessible from the public internet. For private resources, use CloudWatch metrics and alarms to trigger health check status changes.</p>
    </div>
    """, unsafe_allow_html=True)

# Function for Direct Connect page
def direct_connect_page():
    st.title("AWS Direct Connect")
    
    try:
        st.image(load_image_from_url(aws_images["direct_connect"]), width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is AWS Direct Connect?")
    st.markdown("""
    AWS Direct Connect is a cloud service that establishes a dedicated network connection from your premises to AWS, bypassing the public internet to deliver more consistent network performance and reduced bandwidth costs.
    
    **Key Benefits:**
    - Reduced bandwidth costs
    - Consistent network performance
    - Private connectivity to AWS services
    - Compatible with all AWS services
    - Scalable and redundant connections
    """)
    
    st.header("Connection Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h4>Dedicated Connection</h4>
            <ul>
                <li>1, 10, or 100 Gbps dedicated connection</li>
                <li>Ordered through AWS and provisioned by AWS Direct Connect Partners</li>
                <li>Physical ethernet port dedicated to a customer</li>
                <li>Multiple Virtual Interfaces can be configured</li>
                <li>Higher bandwidth and lowest latency</li>
                <li>Longer provisioning time (typically weeks)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h4>Hosted Connection</h4>
            <ul>
                <li>Capacity ranges from 50 Mbps to 10 Gbps</li>
                <li>Ordered through an AWS Direct Connect Partner</li>
                <li>Typically provisioned more quickly than Dedicated Connections</li>
                <li>Single Virtual Interface per connection</li>
                <li>More flexible bandwidth options</li>
                <li>Shorter deployment time</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Virtual Interfaces (VIFs)")
    st.markdown("""
    Virtual Interfaces (VIFs) enable access to AWS services through Direct Connect. Each VIF is a BGP connection configured for a specific purpose.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Private VIF</h4>
            <ul>
                <li>Connect to resources in your VPC using private IP addresses</li>
                <li>Bypasses the public internet</li>
                <li>Supports VPC resources access</li>
                <li>Uses private RFC1918 addresses</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Public VIF</h4>
            <ul>
                <li>Access all AWS public services using public IP addresses</li>
                <li>Still bypasses the public internet</li>
                <li>Used for S3, DynamoDB, etc.</li>
                <li>Uses public routable addresses</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Transit VIF</h4>
            <ul>
                <li>Connect to resources in your VPCs through a Transit Gateway</li>
                <li>Simplifies multiple VPC connectivity</li>
                <li>Used with Direct Connect Gateway</li>
                <li>Supports cross-region connectivity</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Direct Connect Gateway")
    st.markdown("""
    <div class="aws-info-card">
        <p>AWS Direct Connect Gateway is a globally available resource that allows you to connect your AWS Direct Connect connection to VPCs across different AWS regions and accounts.</p>
        <h4>Key Features:</h4>
        <ul>
            <li>Global resource (not region-specific)</li>
            <li>Connect to multiple VPCs across regions</li>
            <li>Connect to VPCs in different AWS accounts (within the same payer ID)</li>
            <li>Simplifies network architecture for global deployments</li>
            <li>Enables traffic flow from VPCs to Direct Connect connection</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Resilience and High Availability")
    st.markdown("""
    To ensure high availability, implement redundancy at multiple levels:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h4>Redundancy Options</h4>
            <ul>
                <li>Multiple Direct Connect connections</li>
                <li>Multiple Direct Connect locations</li>
                <li>Multiple customer routers</li>
                <li>Multiple AWS regions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h4>Common HA Designs</h4>
            <ul>
                <li>Single location, multiple connections</li>
                <li>Multiple locations, multiple connections</li>
                <li>Site-to-Site VPN as a backup to Direct Connect</li>
                <li>Direct Connect with Link Aggregation Groups (LAG)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="aws-warning-card">
        <h4>Best Practice</h4>
        <p>For critical workloads, establish connections to at least two Direct Connect locations for maximum resilience. Additionally, configure a Site-to-Site VPN as a backup option in case all Direct Connect connections become unavailable.</p>
    </div>
    """, unsafe_allow_html=True)

# Function for Transit Gateway page
def transit_gateway_page():
    st.title("AWS Transit Gateway")
    
    try:
        st.image(load_image_from_url(aws_images["transit_gateway"]), width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is AWS Transit Gateway?")
    st.markdown("""
    AWS Transit Gateway is a network transit hub that simplifies network architecture by connecting VPCs and on-premises networks through a central hub. It acts as a cloud router - each new connection is only made once.
    
    **Key Benefits:**
    - Simplified network architecture
    - Centralized connectivity management
    - Highly available and scalable
    - Reduced operational overhead
    - Cost-effective for multiple connections
    """)
    
    st.header("Core Functionality")
    st.markdown("""
    <div class="aws-card">
        <p>Transit Gateway serves as a hub that controls how traffic is routed among all connected networks, which act like spokes.</p>
        <h4>Key Features:</h4>
        <ul>
            <li>Connect thousands of VPCs and on-premises networks</li>
            <li>Highly available and scalable by default</li>
            <li>Region-specific service with cross-region peering capability</li>
            <li>Support for multicast traffic</li>
            <li>Up to 50 Gbps bandwidth per VPC connection (burst)</li>
            <li>Centralized network control and management</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Transit Gateway Route Tables")
    st.markdown("""
    <div class="aws-info-card">
        <p>Transit Gateway route tables determine where network traffic is directed.</p>
        <h4>Key Concepts:</h4>
        <ul>
            <li>Each Transit Gateway comes with a default route table</li>
            <li>Additional route tables can be created for traffic segregation</li>
            <li>Attachments (VPCs, VPN connections) can be associated with route tables</li>
            <li>Route propagation can be enabled or disabled per attachment</li>
            <li>Route tables enable network segmentation and isolation</li>
            <li>Similar to VPC route tables but control traffic between attachments</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Transit Gateway Attachments")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>VPC Attachments</h4>
            <ul>
                <li>Connect Transit Gateway to VPCs</li>
                <li>Specify one or more subnets (in different AZs) for the attachment</li>
                <li>Support for IPv4 and IPv6 traffic</li>
            </ul>
            <h4>VPN Attachments</h4>
            <ul>
                <li>Connect to on-premises networks using Site-to-Site VPN</li>
                <li>Support for static routes or dynamic routing using BGP</li>
                <li>Encrypted connection over the internet</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Direct Connect Gateway Attachments</h4>
            <ul>
                <li>Connect to on-premises networks using Direct Connect</li>
                <li>Provide private, dedicated connectivity</li>
                <li>Higher bandwidth and more consistent latency</li>
            </ul>
            <h4>Transit Gateway Peering Attachments</h4>
            <ul>
                <li>Connect Transit Gateways across regions</li>
                <li>Enable global network connectivity</li>
                <li>Traffic stays on AWS global network</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Centralized Network Architecture")
    st.markdown("""
    <div class="aws-card">
        <p>Transit Gateway enables a hub-and-spoke network topology, replacing complex mesh connections.</p>
        <h4>Architectural Benefits:</h4>
        <ul>
            <li><strong>Simplified Management:</strong> Centralized point of control for network traffic</li>
            <li><strong>Reduced Connection Complexity:</strong> N-to-1 connections instead of N-to-N mesh</li>
            <li><strong>Network Segmentation:</strong> Create isolated routing domains using multiple route tables</li>
            <li><strong>Streamlined Security:</strong> Centralized inspection and filtering of traffic</li>
            <li><strong>Consistent Policies:</strong> Apply consistent routing and security policies across the network</li>
            <li><strong>Scalable Design:</strong> Easily add new networks without reconfiguring existing connections</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="aws-success-card">
        <h4>Use Case Example</h4>
        <p>A company with 15 VPCs across 3 AWS accounts would typically require 105 VPC peering connections for full connectivity. With Transit Gateway, they only need 15 attachments (one per VPC), significantly simplifying the network architecture and reducing management overhead.</p>
    </div>
    """, unsafe_allow_html=True)

# Function for Security Groups and NACLs page
def security_groups_nacls_page():
    st.title("AWS Security Groups & Network ACLs")
    
    try:
        st.image(load_image_from_url(aws_images["security"]), width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("Security Groups vs. Network ACLs")
    st.markdown("""
    AWS provides two main firewall features for your VPC: Security Groups and Network Access Control Lists (NACLs). They operate at different levels of the network stack and have distinct characteristics.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h4>Security Groups</h4>
            <p><strong>Acts at the instance level (first line of defense)</strong></p>
            <ul>
                <li>Supports <strong>allow rules only</strong></li>
                <li><strong>Stateful:</strong> Return traffic automatically allowed</li>
                <li>All rules are <strong>evaluated</strong> before deciding to allow traffic</li>
                <li>Attached to AWS resources (EC2, RDS, etc.)</li>
                <li>Can reference other security groups or IP addresses</li>
                <li>Default security group allows all outbound traffic</li>
                <li>Multiple security groups can be attached to a resource</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h4>Network ACLs</h4>
            <p><strong>Acts at the subnet level (second line of defense)</strong></p>
            <ul>
                <li>Supports both <strong>allow and deny rules</strong></li>
                <li><strong>Stateless:</strong> Return traffic must be explicitly allowed</li>
                <li>Rules are <strong>evaluated in order</strong> by rule number</li>
                <li>Automatically applied to all instances in the subnet</li>
                <li>Can only reference IP addresses (not security groups)</li>
                <li>Default NACL allows all inbound and outbound traffic</li>
                <li>One NACL per subnet, but can be shared across subnets</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Security Group Rules")
    st.markdown("""
    <div class="aws-info-card">
        <p>Security group rules control the allowed inbound and outbound traffic for AWS resources.</p>
        <h4>Components of a Security Group Rule:</h4>
        <ul>
            <li><strong>Protocol:</strong> TCP, UDP, ICMP, or custom protocol</li>
            <li><strong>Port Range:</strong> Single port or range of ports</li>
            <li><strong>Source/Destination:</strong> IP ranges or references to other security groups</li>
            <li><strong>Description:</strong> Optional description for the rule</li>
        </ul>
        <h4>Key Points:</h4>
        <ul>
            <li>Security groups are stateful - if you allow an inbound port, the return traffic is automatically allowed</li>
            <li>You cannot block specific IP addresses using security groups - use NACLs instead</li>
            <li>You can create references between security groups, even across VPC peering connections</li>
            <li>Security groups evaluate all rules before allowing traffic</li>
            <li>Default is to deny all inbound traffic and allow all outbound traffic</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Network ACL Rules")
    st.markdown("""
    <div class="aws-info-card">
        <p>Network ACL rules control traffic entering and exiting subnets within your VPC.</p>
        <h4>Components of a NACL Rule:</h4>
        <ul>
            <li><strong>Rule Number:</strong> Determines the order of evaluation (1-32766)</li>
            <li><strong>Protocol:</strong> TCP, UDP, ICMP, or custom protocol</li>
            <li><strong>Port Range:</strong> Single port or range of ports</li>
            <li><strong>Source/Destination:</strong> IP ranges only</li>
            <li><strong>Allow/Deny:</strong> Specify whether to allow or deny the traffic</li>
        </ul>
        <h4>Key Points:</h4>
        <ul>
            <li>NACLs are stateless - you must create separate rules for inbound and outbound traffic</li>
            <li>Rules are processed in order, from lowest to highest number</li>
            <li>Once a rule matches traffic, it's applied immediately without checking other rules</li>
            <li>Include an explicit deny all rule at the end (highest number)</li>
            <li>Use NACLs to block specific IP addresses or port ranges</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Defense in Depth Strategy")
    st.markdown("""
    <div class="aws-success-card">
        <h4>Best Practices</h4>
        <ul>
            <li>Use security groups as your primary method of protecting resources</li>
            <li>Use NACLs as a secondary layer of defense at the subnet level</li>
            <li>Configure NACLs to block known bad actors or traffic patterns</li>
            <li>Keep security group rules as restrictive as possible</li>
            <li>Use security group referencing to allow services to communicate</li>
            <li>Document the purpose of each security group and NACL rule</li>
            <li>Regularly audit and clean up unused rules and groups</li>
            <li>Consider using AWS Firewall Manager to centrally configure and manage rules</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h4>Example Multi-Tier Application Security</h4>
            <ol>
                <li><strong>Web Tier Security Group:</strong>
                    <ul>
                        <li>Allow inbound HTTP/HTTPS from 0.0.0.0/0</li>
                        <li>Allow outbound to App Tier Security Group</li>
                    </ul>
                </li>
                <li><strong>App Tier Security Group:</strong>
                    <ul>
                        <li>Allow inbound from Web Tier Security Group</li>
                        <li>Allow outbound to Database Tier Security Group</li>
                    </ul>
                </li>
                <li><strong>Database Tier Security Group:</strong>
                    <ul>
                        <li>Allow inbound database port from App Tier Security Group</li>
                        <li>No outbound rules needed (default allows all)</li>
                    </ul>
                </li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-warning-card">
            <h4>Security Group Limits</h4>
            <ul>
                <li>Maximum of 10,000 security groups per Region (adjustable)</li>
                <li>Maximum of 60 inbound and 60 outbound rules per security group</li>
                <li>Maximum of 16 security groups per ENI (adjustable up to 25)</li>
                <li>Security group changes take effect immediately</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Function for Global Accelerator page
def global_accelerator_page():
    st.title("AWS Global Accelerator")
    
    try:
        st.image(load_image_from_url(aws_images["global_accelerator"]), width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is AWS Global Accelerator?")
    st.markdown("""
    AWS Global Accelerator is a networking service that improves the availability and performance of applications with local or global users. It provides static IP addresses that act as a fixed entry point to your applications and routes traffic to optimal endpoints worldwide.
    
    **Key Benefits:**
    - Improved availability and fault tolerance
    - Better performance and reduced latency
    - Static IP addresses for global routing
    - Fast regional failover
    - Simplified DNS management
    - Enhanced security with DDoS protection
    """)
    
    st.header("How Global Accelerator Works")
    st.markdown("""
    <div class="aws-card">
        <p>AWS Global Accelerator uses the AWS global network to route traffic from users to application endpoints through the most efficient path.</p>
        <h4>Traffic Flow:</h4>
        <ol>
            <li>User traffic enters the AWS network from the closest edge location using anycast IP addresses</li>
            <li>Traffic stays on the AWS global network backbone instead of the public internet</li>
            <li>Global Accelerator routes traffic to the optimal healthy endpoint in the nearest region</li>
            <li>If an endpoint becomes unhealthy, Global Accelerator quickly reroutes traffic to healthy endpoints</li>
        </ol>
        
        <p>This approach bypasses internet congestion and reduces latency by using AWS's private network backbone for most of the route.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Components")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Static IP Addresses</h4>
            <ul>
                <li>Two static anycast IPv4 addresses</li>
                <li>Serve as entry points for your application</li>
                <li>Remain fixed even if your architecture changes</li>
                <li>Can bring your own IP addresses (BYOIP)</li>
            </ul>
            
            <h4>Accelerator</h4>
            <ul>
                <li>Main Global Accelerator resource</li>
                <li>Contains listeners and endpoint groups</li>
                <li>Can be standard or custom routing type</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Listeners</h4>
            <ul>
                <li>Process inbound connections based on ports and protocols</li>
                <li>Support TCP and UDP protocols</li>
                <li>Define port ranges for client connections</li>
            </ul>
            <h4>Endpoint Groups</h4>
            <ul>
                <li>Collection of endpoints in a single region</li>
                <li>Control traffic distribution with traffic dials (0-100%)</li>
                <li>Enable gradual shifting of traffic between regions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="aws-info-card">
        <h4>Endpoints</h4>
        <p>Resources to which Global Accelerator routes traffic</p>
        <ul>
            <li><strong>Types:</strong> Application Load Balancers, Network Load Balancers, EC2 instances, Elastic IPs</li>
            <li><strong>Weight:</strong> Determines proportion of traffic (0-255)</li>
            <li><strong>Health Checks:</strong> Automatically detect and route away from unhealthy endpoints</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Global Accelerator vs. CloudFront")
    st.markdown("""
    While both services use the AWS global network and edge locations, they serve different purposes.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-card">
            <h4>Global Accelerator</h4>
            <ul>
                <li>Optimizes the path from users to applications</li>
                <li>Works with both HTTP and non-HTTP protocols (TCP/UDP)</li>
                <li>Provides static IP addresses for applications</li>
                <li>Ideal for non-cacheable content, gaming, IoT, or voice over IP</li>
                <li>Routes to the nearest healthy endpoint</li>
                <li>Faster failover (within seconds)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-card">
            <h4>CloudFront</h4>
            <ul>
                <li>Content delivery network (CDN) that caches content</li>
                <li>Primarily for HTTP/HTTPS traffic</li>
                <li>Optimizes delivery of cacheable content</li>
                <li>Dynamic DNS name, not static IPs</li>
                <li>Ideal for web applications, media, and file downloads</li>
                <li>Advanced features like Lambda@Edge, field-level encryption</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="aws-success-card">
        <h4>Use Case Examples</h4>
        <ul>
            <li><strong>Gaming applications:</strong> Low latency and low packet loss using UDP protocols</li>
            <li><strong>IoT devices:</strong> Reliable connectivity with fixed IP addresses</li>
            <li><strong>Voice assistants:</strong> Voice processing with real-time communication requirements</li>
            <li><strong>Financial applications:</strong> Consistent low latency for trading platforms</li>
            <li><strong>Global APIs:</strong> Predictable performance for microservice architectures</li>
            <li><strong>Multi-region failover:</strong> Fast automated detection and rerouting</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Function for Storage Gateway page
def storage_gateway_page():
    st.title("AWS Storage Gateway")
    
    try:
        st.image(load_image_from_url(aws_images["storage_gateway"]), width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("What is AWS Storage Gateway?")
    st.markdown("""
    AWS Storage Gateway is a hybrid cloud storage service that provides on-premises applications with access to virtually unlimited cloud storage. It bridges on-premises environments with cloud storage through a seamless integration.
    
    **Key Benefits:**
    - Extend on-premises storage to AWS
    - Low-latency access to cloud data
    - Cost-effective storage and archiving
    - Backup and disaster recovery
    - Simplified hybrid cloud storage management
    - Standard storage protocols (NFS, SMB, iSCSI)
    """)
    
    st.header("Gateway Types")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>File Gateway</h4>
            <p><strong>Key Features:</strong></p>
            <ul>
                <li>Provides SMB and NFS file interfaces</li>
                <li>Stores files as native S3 objects</li>
                <li>Local cache for frequently accessed data</li>
                <li>Supports S3 storage classes and lifecycle policies</li>
            </ul>
            <p><strong>Use Cases:</strong></p>
            <ul>
                <li>File share migrations to cloud</li>
                <li>Hybrid file storage</li>
                <li>Backup and archive repositories</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Volume Gateway</h4>
            <p><strong>Key Features:</strong></p>
            <ul>
                <li>Provides iSCSI block storage volumes</li>
                <li>Two modes: Cached or Stored</li>
                <li>EBS snapshots for backup</li>
            </ul>
            <p><strong>Use Cases:</strong></p>
            <ul>
                <li>On-premises block storage extension</li>
                <li>Backup and disaster recovery</li>
                <li>Cloud migration for block storage</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Tape Gateway</h4>
            <p><strong>Key Features:</strong></p>
            <ul>
                <li>Virtual tape library interface</li>
                <li>Compatible with backup software</li>
                <li>Stores data on S3 and Glacier</li>
                <li>Eliminates physical tape management</li>
            </ul>
            <p><strong>Use Cases:</strong></p>
            <ul>
                <li>Tape backup replacement</li>
                <li>Long-term data archiving</li>
                <li>Regulatory compliance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="aws-feature-card">
            <h4>Amazon FSx File Gateway</h4>
            <p><strong>Key Features:</strong></p>
            <ul>
                <li>Low-latency access to Amazon FSx for Windows File Server</li>
                <li>Full SMB support and Windows compatibility</li>
                <li>AD integration and ACL support</li>
            </ul>
            <p><strong>Use Cases:</strong></p>
            <ul>
                <li>Windows file share migrations</li>
                <li>Multi-site file collaboration</li>
                <li>On-premises access to FSx</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("Deployment Options")
    st.markdown("""
    <div class="aws-info-card">
        <p>Storage Gateway can be deployed in several ways to suit your environment:</p>
        <h4>Deployment Methods:</h4>
        <ul>
            <li><strong>VMware ESXi:</strong> Virtual appliance for VMware environments</li>
            <li><strong>Microsoft Hyper-V:</strong> Virtual appliance for Hyper-V environments</li>
            <li><strong>KVM:</strong> Virtual appliance for Linux KVM hypervisor</li>
            <li><strong>Amazon EC2:</strong> Deploy as an EC2 instance within AWS</li>
            <li><strong>Hardware Appliance:</strong> Physical hardware appliance for on-premises use</li>
        </ul>
        <p>Each gateway requires local storage for cache and, in some cases, upload buffer. Size appropriately based on workload characteristics.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Integration with AWS Services")
    st.markdown("""
    <div class="aws-card">
        <p>Storage Gateway integrates with many AWS services to provide a seamless hybrid experience:</p>
        <h4>Key Integrations:</h4>
        <ul>
            <li><strong>Amazon S3:</strong> Store files, volumes, and tapes as objects</li>
            <li><strong>Amazon S3 Glacier:</strong> Archive tape data for long-term retention</li>
            <li><strong>Amazon EBS:</strong> Create EBS snapshots from volumes</li>
            <li><strong>AWS Backup:</strong> Centrally manage backup of gateway volumes</li>
            <li><strong>Amazon CloudWatch:</strong> Monitor gateway performance and health</li>
            <li><strong>AWS IAM:</strong> Control access to gateway resources</li>
            <li><strong>AWS KMS:</strong> Encrypt data in transit and at rest</li>
            <li><strong>Amazon FSx:</strong> Access FSx for Windows File Server from on-premises</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="aws-warning-card">
        <h4>Performance Considerations</h4>
        <ul>
            <li>Size cache appropriately based on active working set</li>
            <li>Provision adequate bandwidth for data transfer needs</li>
            <li>Consider upload buffer size for Volume Gateway</li>
            <li>Monitor CloudWatch metrics to identify bottlenecks</li>
            <li>Consider deploying gateway in EC2 for large-scale migration projects</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Function for Knowledge Checks page
def knowledge_checks_page():
    st.title("Knowledge Checks")
    
    st.markdown("""
    <div class="aws-info-card">
        <h3>Test your knowledge</h3>
        <p>Answer the scenario-based questions below to check your understanding. Your progress is tracked at the bottom of this page.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for each topic's quizzes
    tabs = st.tabs([
        "🌐 VPC", 
        "🔍 Route 53", 
        "🔌 Direct Connect", 
        "🚉 Transit Gateway",
        "🔒 Security Groups & NACLs", 
        "🚀 Global Accelerator",
        "💾 Storage Gateway"
    ])
    
    # VPC Quiz Tab
    with tabs[0]:
        st.header("VPC Knowledge Check")
        for i, quiz in enumerate(quiz_data["vpc"]):
            handle_quiz("vpc", i, quiz)
    
    # Route 53 Quiz Tab
    with tabs[1]:
        st.header("Route 53 Knowledge Check")
        for i, quiz in enumerate(quiz_data["route53"]):
            handle_quiz("route53", i, quiz)
    
    # Direct Connect Quiz Tab
    with tabs[2]:
        st.header("Direct Connect Knowledge Check")
        for i, quiz in enumerate(quiz_data["direct_connect"]):
            handle_quiz("direct_connect", i, quiz)
    
    # Transit Gateway Quiz Tab
    with tabs[3]:
        st.header("Transit Gateway Knowledge Check")
        for i, quiz in enumerate(quiz_data["transit_gateway"]):
            handle_quiz("transit_gateway", i, quiz)
            
    # Security Groups & NACLs Quiz Tab
    with tabs[4]:
        st.header("Security Groups & NACLs Knowledge Check")
        for i, quiz in enumerate(quiz_data["security_groups_nacls"]):
            handle_quiz("security_groups_nacls", i, quiz)
            
    # Global Accelerator Quiz Tab
    with tabs[5]:
        st.header("Global Accelerator Knowledge Check")
        for i, quiz in enumerate(quiz_data["global_accelerator"]):
            handle_quiz("global_accelerator", i, quiz)
            
    # Storage Gateway Quiz Tab
    with tabs[6]:
        st.header("Storage Gateway Knowledge Check")
        for i, quiz in enumerate(quiz_data["storage_gateway"]):
            handle_quiz("storage_gateway", i, quiz)
    
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

st.sidebar.subheader("⚙️ Session Management")

# Reset button for session data
if st.sidebar.button("🔄 Reset Progress", key="reset_button"):
    reset_session()

# Show session ID
st.sidebar.caption(f"Session ID: {st.session_state.session_id[:8]}...")

st.sidebar.divider()

# Main content tabs
tabs = st.tabs([
    "🏠 Home", 
    "🌐 VPC", 
    "🔍 Route 53", 
    "🔌 Direct Connect", 
    "🚉 Transit Gateway",
    "🔒 Security Groups & NACLs", 
    "🚀 Global Accelerator", 
    "💾 Storage Gateway",
    "🧪 Knowledge Checks"
])

with tabs[0]:
    home_page()

with tabs[1]:
    vpc_page()

with tabs[2]:
    route53_page()

with tabs[3]:
    direct_connect_page()

with tabs[4]:
    transit_gateway_page()

with tabs[5]:
    security_groups_nacls_page()

with tabs[6]:
    global_accelerator_page()

with tabs[7]:
    storage_gateway_page()

with tabs[8]:
    knowledge_checks_page()

# Footer
st.markdown("""
<div class="footer">
    © 2025, Amazon Web Services, Inc. or its affiliates. All rights reserved.
</div>
""", unsafe_allow_html=True)
