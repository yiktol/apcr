
import streamlit as st
import base64
from PIL import Image
import requests
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="AWS Certification Program Overview",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Function to load and cache images from URL
# @st.cache_data
def load_image_from_url(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

# Define AWS stock images URLs
aws_images = {
    "cert_path": "https://d1.awsstatic.com/training-and-certification/certification-badges/AWS-Certified-Solutions-Architect-Associate_badge.3419559c682629072f1eb968d59dea0741772c0f.png",
    "cert_levels": "https://d1.awsstatic.com/Training-and-Certification/certification-tiers-v2.094e632806f1962a5148f382fa477397372719be.png",
    "skillbuilder": "https://d1.awsstatic.com/training-and-certification/AWS-Digital-Training-Certification-Badge-v1.0.8cad9c0718e37c503a57a25cec86765d0cc27417.png",
    "exam_domains": "https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2021/11/12/SA-A-Domains.png",
    "program_path": "https://a0.awsstatic.com/libra-css/images/logos/aws_smile-header-desktop-en-white_59x35.png"
}

# Custom CSS to improve the appearance
st.markdown("""
<style>
    .main-header {
        font-size: 42px !important;
        font-weight: 700 !important;
        color: #232f3e !important;
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
    }
    .sub-header {
        font-size: 28px !important;
        font-weight: 600 !important;
        color: #232f3e !important;
        margin-top: 20px !important;
        margin-bottom: 10px !important;
    }
    .normal-text {
        font-size: 18px !important;
        line-height: 1.6 !important;
    }
    .highlight-box {
        background-color: #f0f5ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff9900;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .card {
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0px;
        background-color: #f9f9f9;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .orange-text {
        color: #ff9900 !important;
        font-weight: bold !important;
    }
    .step-container {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    .step-number {
        background-color: #ff9900;
        color: white;
        font-weight: bold;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 15px;
    }
    .icon-text {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }
    .aws-button {
        background-color: #ff9900;
        color: white !important;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        margin: 10px 0;
        text-align: center;
    }
    .timeline-container {
        border-left: 3px solid #ff9900;
        padding-left: 20px;
        margin-left: 20px;
        margin-bottom: 30px;
    }
    .timeline-item {
        position: relative;
        margin-bottom: 20px;
    }
    .timeline-item:before {
        content: '';
        position: absolute;
        left: -27px;
        top: 5px;
        width: 12px;
        height: 12px;
        background-color: #ff9900;
        border-radius: 50%;
    }
</style>
""", unsafe_allow_html=True)

# Header section with logo
col1, col2 = st.columns([1, 6])
with col1:
    aws_logo = load_image_from_url("https://a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_1200x630.png")
    if aws_logo:
        st.image(aws_logo, width=100)
with col2:
    st.markdown('<div class="main-header">AWS Solutions Architect - Associate</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 24px; font-weight: 500; color: #666;">Certification Program Overview</div>', unsafe_allow_html=True)

# Main content area
st.markdown("---")

# Program overview card
st.markdown('<div class="sub-header">Program Overview</div>', unsafe_allow_html=True)

# Two column layout for certification overview
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="normal-text">The <span class="orange-text">AWS Certified Solutions Architect - Associate</span> certification validates your ability to design secure, resilient, high-performing, and cost-optimized cloud architectures using AWS services.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    st.markdown("""
    <div class="normal-text"><strong>Key Certification Details:</strong></div>
    <ul class="normal-text">
        <li>130 minutes exam duration</li>
        <li>65 Questions (50 scored, 15 unscored)</li>
        <li>Passing score: 720/1000</li>
        <li>Multiple-choice questions only</li>
        <li>No negative marking</li>
        <li>Remote and in-person testing options</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    cert_image = load_image_from_url(aws_images["cert_path"])
    if cert_image:
        st.image(cert_image, width=300)
    st.markdown('<div style="text-align: center; font-style: italic; font-size: 14px;">AWS Solutions Architect - Associate Badge</div>', unsafe_allow_html=True)

# Certification levels
st.markdown('<div class="sub-header">AWS Certification Path</div>', unsafe_allow_html=True)
cert_levels_image = load_image_from_url(aws_images["cert_levels"])
if cert_levels_image:
    st.image(cert_levels_image, width=800)
    st.markdown('<div style="text-align: center; font-style: italic; font-size: 14px;">AWS Certification Levels</div>', unsafe_allow_html=True)

# Exam domains section
st.markdown('<div class="sub-header">Exam Content Domains</div>', unsafe_allow_html=True)

# Create columns for the content domains
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h3 style="color: #232f3e;">Domain 1: Design Secure Architectures (30%)</h3>
        <ul class="normal-text">
            <li>Design secure access to AWS resources</li>
            <li>Design secure workloads and applications</li>
            <li>Determine appropriate data security controls</li>
        </ul>
    </div>
    
    <div class="card">
        <h3 style="color: #232f3e;">Domain 2: Design Resilient Architectures (26%)</h3>
        <ul class="normal-text">
            <li>Design scalable and loosely coupled architectures</li>
            <li>Design highly available and fault-tolerant architectures</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3 style="color: #232f3e;">Domain 3: Design High-Performing Architectures (24%)</h3>
        <ul class="normal-text">
            <li>Determine high-performing and scalable storage solutions</li>
            <li>Design high-performing and elastic compute solutions</li>
            <li>Determine high-performing database solutions</li>
            <li>Design high-performing and scalable network architectures</li>
        </ul>
    </div>
    
    <div class="card">
        <h3 style="color: #232f3e;">Domain 4: Design Cost-Optimized Architectures (20%)</h3>
        <ul class="normal-text">
            <li>Design cost-optimized storage solutions</li>
            <li>Design cost-optimized compute solutions</li>
            <li>Design cost-optimized database solutions</li>
            <li>Design cost-optimized network architectures</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Program timeline
st.markdown('<div class="sub-header">Program Timeline</div>', unsafe_allow_html=True)

st.markdown("""
<div class="timeline-container">
    <div class="timeline-item">
        <h4>Week 1: Program Kickoff</h4>
        <p>Introduction to AWS Certifications, program overview, and basics of AWS Identity and Access Management (IAM).</p>
    </div>
    <div class="timeline-item">
        <h4>Week 2: Networking & Security</h4>
        <p>Virtual Private Cloud (VPC), security groups, NACLs, and AWS security services.</p>
    </div>
    <div class="timeline-item">
        <h4>Week 3: Compute & Storage</h4>
        <p>EC2, Lambda, S3, EFS, and other storage services.</p>
    </div>
    <div class="timeline-item">
        <h4>Week 4: Databases & Application Services</h4>
        <p>RDS, DynamoDB, SQS, SNS, and application integration services.</p>
    </div>
    <div class="timeline-item">
        <h4>Week 5: Review & Exam Preparation</h4>
        <p>Practice questions, exam strategies, and final review of key concepts.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Getting Started Section
st.markdown('<div class="sub-header">Getting Started</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h3 style="color: #232f3e;">Step 1: Register for AWS Partner Network (APN)</h3>
        <p class="normal-text">Register with your company email to access partner-exclusive training resources and link your AWS certification.</p>
        <a href="https://partnercentral.awspartner.com/" target="_blank" class="aws-button">Register for APN</a>
    </div>
    
    <div class="card">
        <h3 style="color: #232f3e;">Step 2: Access AWS Skill Builder</h3>
        <p class="normal-text">Login to AWS Skill Builder using your APN credentials to access digital training and practice exams.</p>
        <a href="https://explore.skillbuilder.aws/" target="_blank" class="aws-button">Access Skill Builder</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3 style="color: #232f3e;">Step 3: Enroll in Learning Plans</h3>
        <p class="normal-text">Complete the Solutions Architect Associate Learning Plan and optional Companion Learning Plan.</p>
        <a href="https://explore.skillbuilder.aws/learn/learning_plan/view/2107/aws-partner-certification-readiness-solutions-architect-associate" target="_blank" class="aws-button">Partner Learning Plan</a>
    </div>
    
    <div class="card">
        <h3 style="color: #232f3e;">Step 4: Schedule Your Exam</h3>
        <p class="normal-text">Register early to give yourself a deadline and goal to work towards. Both remote and in-person options are available.</p>
        <a href="https://www.aws.training/certification" target="_blank" class="aws-button">Schedule Exam</a>
    </div>
    """, unsafe_allow_html=True)

# Optional resources section
st.markdown('<div class="sub-header">Optional Resources</div>', unsafe_allow_html=True)

st.markdown("""
<div class="highlight-box">
    <h3 style="color: #232f3e;">AWS Skill Builder Subscription Benefits</h3>
    <p class="normal-text">Enhance your learning with a Skill Builder subscription (optional, $29/month or $449/year):</p>
    <ul class="normal-text">
        <li>Access to 600+ digital courses</li>
        <li>Official AWS practice exams</li>
        <li>AWS Cloud Quest (intermediate-advanced)</li>
        <li>Hands-on labs and challenges</li>
        <li>Enhanced exam preparation materials</li>
    </ul>
    <a href="https://explore.skillbuilder.aws/learn/signin" target="_blank" class="aws-button">Explore Subscription</a>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<div style="text-align: center; color: #666; font-size: 14px;">© 2025 AWS Partner Certification Readiness Program</div>', unsafe_allow_html=True)
