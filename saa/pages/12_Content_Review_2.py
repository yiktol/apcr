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
        st.header("Content Review – Session 2")
        st.markdown("""
        Welcome to the AWS Partner Certification Readiness program. This interactive guide will help you prepare 
        for the Solutions Architect - Associate certification. Navigate through the topics using the sidebar menu.
        
        Each section contains key concepts, important takeaways, and interactive quizzes to reinforce your learning.
        
        **Topics covered:**
        - Virtual Private Cloud (VPC)
        - Route 53 (DNS)
        - AWS Direct Connect
        - Transit Gateway
        - Security Groups & NACLs
        - AWS Global Accelerator
        - AWS Storage Gateway
        """)
    
    st.info("""
    **Certification Preparation Tip:** Practice hands-on with the services covered in this guide. 
    The AWS Solutions Architect - Associate exam focuses on practical knowledge of AWS services 
    and how they can be used together to design resilient, cost-effective solutions.
    """)

# Function for VPC page
def vpc_page():
    st.title("Virtual Private Cloud (VPC)")
    
    try:
        st.image(aws_images["vpc"], width=800)
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
        st.subheader("Core Components")
        st.markdown("""
        - **Subnets**: Range of IP addresses in your VPC
        - **Route Tables**: Set of rules to determine where network traffic is directed
        - **Internet Gateway**: Enables communication between your VPC and the internet
        - **NAT Gateway**: Allows private subnet resources to access the internet
        - **Security Groups**: Virtual firewall controlling inbound and outbound traffic at the instance level
        - **Network ACLs**: Firewall controlling inbound and outbound traffic at the subnet level
        """)
    
    with col2:
        st.subheader("Advanced Components")
        st.markdown("""
        - **VPC Endpoints**: Private connectivity to AWS services without internet gateway
        - **VPC Peering**: Connect VPCs to route traffic between them
        - **Transit Gateway**: Central hub to connect VPCs and on-premises networks
        - **Shared VPC**: Share subnets with other AWS accounts
        - **Elastic IP**: Static public IPv4 address for your instances
        - **VPC Flow Logs**: Capture network flow information for monitoring
        """)
    
    st.header("Public vs. Private Subnets")
    st.markdown("""
    **Public Subnet:**
    - Has a route to an Internet Gateway
    - Resources can directly communicate with the internet
    - Typically hosts public-facing resources like web servers
    
    **Private Subnet:**
    - No direct route to an Internet Gateway
    - Resources cannot directly communicate with the internet
    - Requires a NAT Gateway for outbound internet access
    - Typically hosts internal resources like databases
    """)
    
    st.header("IP Addressing")
    st.markdown("""
    **Key Considerations:**
    - Plan your IP address space before creating a VPC
    - VPC CIDR blocks can be between /16 and /28
    - Consider future AWS region expansion
    - Plan for connectivity to corporate networks
    - Avoid overlapping IP spaces
    - CIDR cannot be modified once created, but additional CIDRs can be added
    """)
    
    st.header("Security in VPC")
    st.markdown("""
    **Defense in Depth:**
    1. **Security Groups**: Instance-level firewall (stateful)
       - Allow rules only
       - Evaluated as a whole
       - Return traffic automatically allowed
    
    2. **Network ACLs**: Subnet-level firewall (stateless)
       - Allow and deny rules
       - Evaluated in order by rule number
       - Return traffic must be explicitly allowed
    """)
    
    display_quiz("vpc")

# Function for Route 53 page
def route53_page():
    st.title("Amazon Route 53")
    
    try:
        st.image(aws_images["route53"], width=800)
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
    Route 53 translates user-friendly domain names (like www.example.com) into IP addresses (like 192.0.2.1) that computers use to connect to each other. It serves as the backbone for connecting users to your applications.
    
    **Primary Functions:**
    1. **Domain Registration**: Register and manage domain names
    2. **DNS Routing**: Direct traffic to the resources that host your applications
    3. **Health Checking**: Monitor resource health and route traffic away from unhealthy resources
    """)
    
    st.header("Routing Policies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Basic Routing Policies")
        st.markdown("""
        - **Simple**: Route traffic to a single resource
        - **Weighted**: Route traffic to multiple resources in proportions you specify
        - **Failover**: Route traffic to a primary resource or a standby resource if the primary is unavailable
        - **Multivalue Answer**: Respond to DNS queries with up to eight healthy records selected at random
        """)
    
    with col2:
        st.subheader("Advanced Routing Policies")
        st.markdown("""
        - **Latency-based**: Route traffic to the region with the lowest latency
        - **Geolocation**: Route traffic based on the geographic location of your users
        - **Geoproximity**: Route traffic based on the geographic location of resources and optionally shift traffic from one location to another
        - **IP-based**: Route traffic based on users' IP addresses
        """)
    
    st.header("Public vs. Private Hosted Zones")
    st.markdown("""
    **Public Hosted Zones:**
    - Control how traffic is routed on the internet
    - Accessible from the public internet
    - Used for public-facing applications
    
    **Private Hosted Zones:**
    - Control routing within one or more VPCs
    - Not accessible from the public internet
    - Used for internal applications and services
    - Requires enableDnsHostnames and enableDnsSupport VPC attributes
    """)
    
    st.header("Health Checks")
    st.markdown("""
    Route 53 health checks monitor the health and performance of your web applications, web servers, and other resources.
    
    **Types of Health Checks:**
    - **Endpoint monitoring**: Check the health of a specified endpoint
    - **Calculated health checks**: Combine the results of multiple health checks into a single health check
    - **CloudWatch alarm monitoring**: Evaluate the state of a CloudWatch alarm
    
    Health checks can be used with DNS failover to route traffic away from unhealthy endpoints and to healthy endpoints.
    """)
    
    display_quiz("route53")

# Function for Direct Connect page
def direct_connect_page():
    st.title("AWS Direct Connect")
    
    try:
        st.image(aws_images["direct_connect"], width=800)
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
    st.markdown("""
    **Dedicated Connection:**
    - 1, 10, or 100 Gbps dedicated connection
    - Ordered through AWS and provisioned by AWS Direct Connect Partners
    - Physical ethernet port dedicated to a customer
    - Multiple Virtual Interfaces can be configured
    
    **Hosted Connection:**
    - Capacity ranges from 50 Mbps to 10 Gbps
    - Ordered through an AWS Direct Connect Partner
    - Typically provisioned more quickly than Dedicated Connections
    - Single Virtual Interface per connection
    """)
    
    st.header("Virtual Interfaces (VIFs)")
    st.markdown("""
    Virtual Interfaces (VIFs) enable access to AWS services through Direct Connect. Each VIF is a BGP connection configured for a specific purpose.
    
    **Types of VIFs:**
    - **Private VIF**: Connect to resources in your VPC using private IP addresses
    - **Public VIF**: Access all AWS public services using public IP addresses
    - **Transit VIF**: Connect to resources in your VPCs through a Transit Gateway
    """)
    
    st.header("Direct Connect Gateway")
    st.markdown("""
    AWS Direct Connect Gateway is a globally available resource that allows you to connect your AWS Direct Connect connection to VPCs across different AWS regions and accounts.
    
    **Key Features:**
    - Global resource (not region-specific)
    - Connect to multiple VPCs across regions
    - Connect to VPCs in different AWS accounts (within the same payer ID)
    - Simplifies network architecture for global deployments
    - Enables traffic flow from VPCs to Direct Connect connection
    """)
    
    st.header("Resilience and High Availability")
    st.markdown("""
    To ensure high availability, implement redundancy at multiple levels:
    
    **Redundancy Options:**
    - Multiple Direct Connect connections
    - Multiple Direct Connect locations
    - Multiple customer routers
    - Multiple AWS regions
    
    **Common HA Designs:**
    - Single location, multiple connections
    - Multiple locations, multiple connections
    - Site-to-Site VPN as a backup to Direct Connect
    
    BGP routing provides automatic failover when configured properly.
    """)
    
    display_quiz("direct_connect")

# Function for Transit Gateway page
def transit_gateway_page():
    st.title("AWS Transit Gateway")
    
    try:
        st.image(aws_images["transit_gateway"], width=800)
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
    Transit Gateway serves as a hub that controls how traffic is routed among all connected networks, which act like spokes.
    
    **Key Features:**
    - Connect thousands of VPCs and on-premises networks
    - Highly available and scalable by default
    - Region-specific service with cross-region peering capability
    - Support for multicast traffic
    - Up to 50 Gbps bandwidth per VPC connection (burst)
    - Centralized network control and management
    """)
    
    st.header("Transit Gateway Route Tables")
    st.markdown("""
    Transit Gateway route tables determine where network traffic is directed.
    
    **Key Concepts:**
    - Each Transit Gateway comes with a default route table
    - Additional route tables can be created for traffic segregation
    - Attachments (VPCs, VPN connections) can be associated with route tables
    - Route propagation can be enabled or disabled per attachment
    - Route tables enable network segmentation and isolation
    - Similar to VPC route tables but control traffic between attachments
    """)
    
    st.header("Transit Gateway Attachments")
    st.markdown("""
    Attachments are connections between Transit Gateway and your networks.
    
    **Types of Attachments:**
    - **VPC Attachments**: Connect Transit Gateway to VPCs
    - **VPN Attachments**: Connect to on-premises networks using Site-to-Site VPN
    - **Direct Connect Gateway Attachments**: Connect to on-premises networks using Direct Connect
    - **Transit Gateway Peering Attachments**: Connect Transit Gateways across regions
    - **Appliance Mode Attachments**: Support for specific routing needs like stateful inspection
    """)
    
    st.header("Centralized Network Architecture")
    st.markdown("""
    Transit Gateway enables a hub-and-spoke network topology, replacing complex mesh connections.
    
    **Architectural Benefits:**
    - **Simplified Management**: Centralized point of control for network traffic
    - **Reduced Connection Complexity**: N-to-1 connections instead of N-to-N mesh
    - **Network Segmentation**: Create isolated routing domains using multiple route tables
    - **Streamlined Security**: Centralized inspection and filtering of traffic
    - **Consistent Policies**: Apply consistent routing and security policies across the network
    - **Scalable Design**: Easily add new networks without reconfiguring existing connections
    """)
    
    display_quiz("transit_gateway")

# Function for Security Groups and NACLs page
def security_groups_nacls_page():
    st.title("AWS Security Groups & Network ACLs")
    
    try:
        st.image(aws_images["security"], width=800)
    except:
        st.warning("Image could not be displayed")
    
    st.header("Security Groups vs. Network ACLs")
    st.markdown("""
    AWS provides two main firewall features for your VPC: Security Groups and Network Access Control Lists (NACLs). They operate at different levels of the network stack and have distinct characteristics.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Security Groups")
        st.markdown("""
        **Key Characteristics:**
        - Acts at the **instance level** (first line of defense)
        - Supports **allow rules only**
        - **Stateful**: Return traffic automatically allowed
        - All rules are **evaluated** before deciding to allow traffic
        - Attached to AWS resources (EC2, RDS, etc.)
        - Can reference other security groups or IP addresses
        - Default security group allows all outbound traffic
        """)
    
    with col2:
        st.subheader("Network ACLs")
        st.markdown("""
        **Key Characteristics:**
        - Acts at the **subnet level** (second line of defense)
        - Supports both **allow and deny rules**
        - **Stateless**: Return traffic must be explicitly allowed
        - Rules are **evaluated in order** by rule number
        - Automatically applied to all instances in the subnet
        - Can only reference IP addresses (not security groups)
        - Default NACL allows all inbound and outbound traffic
        """)
    
    st.header("Security Group Rules")
    st.markdown("""
    Security group rules control the allowed inbound and outbound traffic for AWS resources.
    
    **Components of a Security Group Rule:**
    - **Protocol**: TCP, UDP, ICMP, or custom protocol
    - **Port Range**: Single port or range of ports
    - **Source/Destination**: IP ranges or references to other security groups
    - **Description**: Optional description for the rule
    
    **Key Points:**
    - Security groups are stateful - if you allow an inbound port, the return traffic is automatically allowed
    - You cannot block specific IP addresses using security groups - use NACLs instead
    - You can create references between security groups, even across VPC peering connections
    - Security groups evaluate all rules before allowing traffic
    - Default is to deny all inbound traffic and allow all outbound traffic
    """)
    
    st.header("Network ACL Rules")
    st.markdown("""
    Network ACL rules control traffic entering and exiting subnets within your VPC.
    
    **Components of a NACL Rule:**
    - **Rule Number**: Determines the order of evaluation (1-32766)
    - **Protocol**: TCP, UDP, ICMP, or custom protocol
    - **Port Range**: Single port or range of ports
    - **Source/Destination**: IP ranges only
    - **Allow/Deny**: Specify whether to allow or deny the traffic
    
    **Key Points:**
    - NACLs are stateless - you must create separate rules for inbound and outbound traffic
    - Rules are processed in order, from lowest to highest number
    - Once a rule matches traffic, it's applied immediately without checking other rules
    - Include an explicit deny all rule at the end (highest number)
    - Use NACLs to block specific IP addresses or port ranges
    """)
    
    st.header("Defense in Depth Strategy")
    st.markdown("""
    Implement both security groups and NACLs as complementary controls for defense in depth.
    
    **Best Practices:**
    - Use security groups as your primary method of protecting resources
    - Use NACLs as a secondary layer of defense at the subnet level
    - Configure NACLs to block known bad actors or traffic patterns
    - Keep security group rules as restrictive as possible
    - Use security group referencing to allow services to communicate
    - Document the purpose of each security group and NACL rule
    - Regularly audit and clean up unused rules and groups
    - Consider using AWS Firewall Manager to centrally configure and manage rules
    """)
    
    display_quiz("security_groups_nacls")

# Function for Global Accelerator page
def global_accelerator_page():
    st.title("AWS Global Accelerator")
    
    try:
        st.image(aws_images["global_accelerator"], width=800)
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
    AWS Global Accelerator uses the AWS global network to route traffic from users to application endpoints through the most efficient path.
    
    **Traffic Flow:**
    1. User traffic enters the AWS network from the closest edge location using anycast IP addresses
    2. Traffic stays on the AWS global network backbone instead of the public internet
    3. Global Accelerator routes traffic to the optimal healthy endpoint in the nearest region
    4. If an endpoint becomes unhealthy, Global Accelerator quickly reroutes traffic to healthy endpoints
    
    This approach bypasses internet congestion and reduces latency by using AWS's private network backbone for most of the route.
    """)
    
    st.header("Components")
    st.markdown("""
    **1. Static IP Addresses**
    - Two static anycast IPv4 addresses
    - Serve as entry points for your application
    - Remain fixed even if your architecture changes
    - Can bring your own IP addresses (BYOIP)
    
    **2. Accelerator**
    - Main Global Accelerator resource
    - Contains listeners and endpoint groups
    - Can be standard or custom routing type
    
    **3. Listeners**
    - Process inbound connections based on ports and protocols
    - Support TCP and UDP protocols
    - Define port ranges for client connections
    
    **4. Endpoint Groups**
    - Collection of endpoints in a single region
    - Control traffic distribution with traffic dials (0-100%)
    - Enable gradual shifting of traffic between regions
    
    **5. Endpoints**
    - Resources to which Global Accelerator routes traffic
    - Types: Application Load Balancers, Network Load Balancers, EC2 instances, Elastic IPs
    - Weight determines proportion of traffic (0-255)
    """)
    
    st.header("Global Accelerator vs. CloudFront")
    st.markdown("""
    While both services use the AWS global network and edge locations, they serve different purposes.
    
    **Global Accelerator:**
    - Optimizes the path from users to applications
    - Works with both HTTP and non-HTTP protocols (TCP/UDP)
    - Provides static IP addresses for applications
    - Ideal for non-cacheable content, gaming, IoT, or voice over IP
    - Routes to the nearest healthy endpoint
    
    **CloudFront:**
    - Content delivery network (CDN) that caches content
    - Primarily for HTTP/HTTPS traffic
    - Optimizes delivery of cacheable content
    - Dynamic DNS name, not static IPs
    - Ideal for web applications, media, and file downloads
    """)
    
    display_quiz("global_accelerator")

# Function for Storage Gateway page
def storage_gateway_page():
    st.title("AWS Storage Gateway")
    
    try:
        st.image(aws_images["storage_gateway"], width=800)
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
        st.subheader("File Gateway")
        st.markdown("""
        **Key Features:**
        - Provides SMB and NFS file interfaces
        - Stores files as native S3 objects
        - Local cache for frequently accessed data
        - Supports S3 storage classes and lifecycle policies
        
        **Use Cases:**
        - File share migrations to cloud
        - Hybrid file storage
        - Backup and archive repositories
        """)
        
        st.subheader("Volume Gateway")
        st.markdown("""
        **Key Features:**
        - Provides iSCSI block storage volumes
        - Two modes: Cached or Stored
        - EBS snapshots for backup
        
        **Use Cases:**
        - On-premises block storage extension
        - Backup and disaster recovery
        - Cloud migration for block storage
        """)
    
    with col2:
        st.subheader("Tape Gateway")
        st.markdown("""
        **Key Features:**
        - Virtual tape library interface
        - Compatible with backup software
        - Stores data on S3 and Glacier
        - Eliminates physical tape management
        
        **Use Cases:**
        - Tape backup replacement
        - Long-term data archiving
        - Regulatory compliance
        """)
        
        st.subheader("Amazon FSx File Gateway")
        st.markdown("""
        **Key Features:**
        - Low-latency access to Amazon FSx for Windows File Server
        - Full SMB support and Windows compatibility
        - AD integration and ACL support
        
        **Use Cases:**
        - Windows file share migrations
        - Multi-site file collaboration
        - On-premises access to FSx
        """)
    
    st.header("Deployment Options")
    st.markdown("""
    Storage Gateway can be deployed in several ways to suit your environment:
    
    **Deployment Methods:**
    - **VMware ESXi**: Virtual appliance for VMware environments
    - **Microsoft Hyper-V**: Virtual appliance for Hyper-V environments
    - **KVM**: Virtual appliance for Linux KVM hypervisor
    - **Amazon EC2**: Deploy as an EC2 instance within AWS
    - **Hardware Appliance**: Physical hardware appliance for on-premises use
    
    Each gateway requires local storage for cache and, in some cases, upload buffer. Size appropriately based on workload characteristics.
    """)
    
    st.header("Integration with AWS Services")
    st.markdown("""
    Storage Gateway integrates with many AWS services to provide a seamless hybrid experience:
    
    **Key Integrations:**
    - **Amazon S3**: Store files, volumes, and tapes as objects
    - **Amazon S3 Glacier**: Archive tape data for long-term retention
    - **Amazon EBS**: Create EBS snapshots from volumes
    - **AWS Backup**: Centrally manage backup of gateway volumes
    - **Amazon CloudWatch**: Monitor gateway performance and health
    - **AWS IAM**: Control access to gateway resources
    - **AWS KMS**: Encrypt data in transit and at rest
    - **Amazon FSx**: Access FSx for Windows File Server from on-premises
    """)
    
    display_quiz("global_accelerator")

# Sidebar menu
st.sidebar.title("AWS Solutions Architect")
st.sidebar.image("https://a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_1200x630.png", width=200)

menu = st.sidebar.radio(
    "Navigation",
    ["Home", 
     "Virtual Private Cloud (VPC)", 
     "Route 53 (DNS)", 
     "AWS Direct Connect", 
     "Transit Gateway",
     "Security Groups & NACLs", 
     "AWS Global Accelerator", 
     "AWS Storage Gateway"]
)

# Display selected page
if menu == "Home":
    home_page()
elif menu == "Virtual Private Cloud (VPC)":
    vpc_page()
elif menu == "Route 53 (DNS)":
    route53_page()
elif menu == "AWS Direct Connect":
    direct_connect_page()
elif menu == "Transit Gateway":
    transit_gateway_page()
elif menu == "Security Groups & NACLs":
    security_groups_nacls_page()
elif menu == "AWS Global Accelerator":
    global_accelerator_page()
elif menu == "AWS Storage Gateway":
    storage_gateway_page()

# Footer
st.sidebar.divider()

# Progress tracking
if "total_score" not in st.session_state:
    st.session_state["total_score"] = 0
    st.session_state["total_attempted"] = 0

topics = ["vpc", "route53", "direct_connect", "transit_gateway", "security_groups_nacls", "global_accelerator", "storage_gateway"]
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
