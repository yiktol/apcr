import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import base64
import io
from streamlit_option_menu import option_menu

# Set page config
st.set_page_config(
    page_title="ML Engineer - Associate Learning",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Home'
if 'quiz_score' not in st.session_state:
    st.session_state['quiz_score'] = 0
if 'quiz_attempted' not in st.session_state:
    st.session_state['quiz_attempted'] = False
if 'name' not in st.session_state:
    st.session_state['name'] = ""

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF9900;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #232F3E;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #232F3E;
        margin-top: 0.8rem;
        margin-bottom: 0.3rem;
    }
    .info-box {
        background-color: #F0F2F6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .success-box {
        background-color: #D1FAE5;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .warning-box {
        background-color: #FEF3C7;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .tip-box {
        background-color: #E0F2FE;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #0EA5E9;
    }
    .step-box {
        background-color: #FFFFFF;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .card {
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: white;
        transition: transform 0.3s;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .aws-orange {
        color: #FF9900;
    }
    .aws-blue {
        color: #232F3E;
    }
    hr {
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Function to display custom header
def custom_header(text, level="main"):
    if level == "main":
        st.markdown(f'<div class="main-header">{text}</div>', unsafe_allow_html=True)
    elif level == "sub":
        st.markdown(f'<div class="sub-header">{text}</div>', unsafe_allow_html=True)
    elif level == "section":
        st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)

# Function to create custom info box
def info_box(text, box_type="info"):
    if box_type == "info":
        st.markdown(f'<div class="info-box">{text}</div>', unsafe_allow_html=True)
    elif box_type == "success":
        st.markdown(f'<div class="success-box">{text}</div>', unsafe_allow_html=True)
    elif box_type == "warning":
        st.markdown(f'<div class="warning-box">{text}</div>', unsafe_allow_html=True)
    elif box_type == "tip":
        st.markdown(f'<div class="tip-box">{text}</div>', unsafe_allow_html=True)

# Function to reset session
def reset_session():
    st.session_state['quiz_score'] = 0
    st.session_state['quiz_attempted'] = False
    st.session_state['name'] = ""
    st.session_state['current_page'] = 'Home'
    st.experimental_rerun()

# Sidebar
with st.sidebar:
    st.image("https://d1.awsstatic.com/training-and-certification/certification-badges/AWS-Certified-Machine-Learning-Specialty_badge.5d259a8045a7d3c41ed927f8b3a9da3df1ec8a20.png", width=150)
    st.markdown("### ML Engineer - Associate")
    st.markdown("#### Domain 1: Data Preparation")
    
    # If user has provided their name, greet them
    if st.session_state['name']:
        st.success(f"Welcome, {st.session_state['name']}! 👋")
    else:
        name = st.text_input("Enter your name:")
        if name:
            st.session_state['name'] = name
            st.experimental_rerun()
    
    # Navigation menu
    selected = option_menu(
        "Navigate",
        ["Home", 
         "ML Lifecycle", 
         "Data Collection", 
         "Data Transformation", 
         "Feature Engineering", 
         "Data Integrity", 
         "Quiz", 
         "Resources"],
        icons=['house', 'diagram-3', 'database', 'arrow-repeat', 'gear', 'shield-check', 'patch-question', 'link'],
        menu_icon="cast",
        default_index=0,
    )
    
    st.session_state['current_page'] = selected
    
    # Reset button
    if st.button("Reset Session 🔄"):
        reset_session()

# Home page
if st.session_state['current_page'] == 'Home':
    custom_header("AWS Partner Certification Readiness")
    st.markdown("## Machine Learning Engineer - Associate")
    
    st.markdown("### Welcome to the interactive learning application for Domain 1: Data Preparation for Machine Learning")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        info_box("""
        This interactive e-learning application covers the main topics of Domain 1 from the AWS Machine Learning Engineer - Associate certification.
        
        Navigate through the content using the sidebar menu to learn about:
        - Machine Learning Lifecycle
        - Data Collection
        - Data Transformation
        - Feature Engineering
        - Data Integrity
        
        Test your knowledge with the quiz when you're ready!
        """, "info")
        
        st.markdown("### Learning Outcomes")
        st.markdown("""
        By the end of this module, you will be able to:
        - Explain the ML lifecycle and its key phases
        - Understand data collection and storage options on AWS
        - Perform data transformation and preprocessing
        - Apply feature engineering techniques
        - Ensure data integrity and prepare data for modeling
        """)
    
    with col2:
        st.image("https://d1.awsstatic.com/training-and-certification/certification-badges/AWS-Certified-Machine-Learning-Specialty_badge.5d259a8045a7d3c41ed927f8b3a9da3df1ec8a20.png", width=250)
        
        if st.session_state['quiz_attempted']:
            st.success(f"Current Quiz Score: {st.session_state['quiz_score']}/5")
        
        st.info("Use the sidebar to navigate through different sections!")

# ML Lifecycle page
elif st.session_state['current_page'] == 'ML Lifecycle':
    custom_header("Machine Learning Lifecycle")
    
    st.markdown("""
    The machine learning lifecycle encompasses all the stages involved in developing, deploying, and maintaining a machine learning model.
    Understanding this lifecycle is crucial for successful implementation of ML projects.
    """)
    
    # ML Lifecycle diagram
    col1, col2 = st.columns([3, 1])
    with col1:
        st.image("https://miro.medium.com/max/1400/1*RLwAD7UAtUgp6xrIl2XH0g.png", caption="Machine Learning Lifecycle")
    
    with col2:
        info_box("""
        Key phases in the ML Lifecycle:
        1. Frame the ML problem
        2. Prepare data
        3. Model development
        4. Deploy
        5. Monitor
        """, "tip")
    
    custom_header("Key Phases Explained", "sub")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 1. Frame the ML Problem
        - Identify business problem
        - Define ML objectives
        - Determine evaluation metrics
        - Establish success criteria
        
        ### 2. Prepare Data
        - Collect data
        - Pre-process data
        - Analysis and visualization
        - Feature Engineering
        - Split Dataset
        """)
    
    with col2:
        st.markdown("""
        ### 3. Model Development
        - Select algorithm
        - Train model
        - Evaluate performance
        - Tune hyperparameters
        
        ### 4. Deploy
        - Implement model in production
        - Integrate with applications
        - Set up inference endpoints
        
        ### 5. Monitor
        - Track model performance
        - Detect drift
        - Retrain as needed
        """)
    
    custom_header("AWS AI/ML Stack", "section")
    
    st.image("https://d1.awsstatic.com/diagrams/aws-ai-stack-big.7c4318d7617de8afd5ccea4285d06eb0559e5984.jpg", caption="AWS AI/ML Stack")
    
    info_box("""
    **The AWS Machine Learning Stack consists of 3 layers:**
    
    1. **AI Services Layer**: Requires no ML expertise. Pretrained and auto-trained models for specific ML problems.
    
    2. **ML Services Layer**: Amazon SageMaker enables labeling, building, training, and deploying machine learning models.
    
    3. **ML Frameworks and Infrastructure Layer**: Addresses highly complex ML problems with flexibility but requires ML expertise.
    """, "info")

# Data Collection page
elif st.session_state['current_page'] == 'Data Collection':
    custom_header("Data Collection")
    
    st.markdown("""
    Data collection is the foundation of any machine learning project. This phase involves gathering, storing,
    and organizing the data that will be used to train and test machine learning models.
    """)
    
    custom_header("Data Structure and Types", "sub")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Structured Data")
        st.image("https://miro.medium.com/v2/resize:fit:1400/1*Z8-9VTB1K9t2NCj1HW4c7Q.jpeg", width=200)
        st.markdown("- Organized in tabular format")
        st.markdown("- Examples: SQL databases, spreadsheets")
        st.markdown("- Well-defined schema")
    
    with col2:
        st.markdown("### Semi-structured Data")
        st.image("https://media.geeksforgeeks.org/wp-content/uploads/20230901230038/What-is-Semi-structured-data.webp", width=200)
        st.markdown("- Has organizational properties but not in relational databases")
        st.markdown("- Examples: XML, JSON, NoSQL databases")
        st.markdown("- Flexible schema")
    
    with col3:
        st.markdown("### Unstructured Data")
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTPOQ7oNvs98X8Yjo8lwGkZi92vZaHZPBdZbA&usqp=CAU", width=200)
        st.markdown("- No pre-defined model or organization")
        st.markdown("- Examples: Text files, social media posts, images, videos")
        st.markdown("- Requires advanced processing")
    
    custom_header("Storage Formats", "section")
    
    st.markdown("""
    Choosing the right storage format is crucial for efficiency in data processing and analysis.
    Each format has its own advantages and use cases:
    """)
    
    data = {
        'Features': ['Data storage', 'Write performance', 'Read performance', 'Block compression', 'Schema evolution', 'Use cases'],
        'CSV': ['Row', 'Fast', 'Slow', '', '', 'Simple data interchange, logs'],
        'Avro': ['Row', 'Medium', 'Medium', 'X', 'X', 'Machine learning data storage'],
        'ORC': ['Column', 'Slow', 'Fast', 'X', 'X', 'Big data processing, Hive/SQL optimizations'],
        'Parquet': ['Column', 'Slow', 'Fast', 'X', 'X', 'Big data processing, analytical queries'],
        'JSON': ['object-notation', 'Medium', 'Medium', '', '', 'Flexible data exchange, Web applications'],
        'JSONL': ['object-notation', 'Fast', 'Medium', '', '', 'Logs, stream processing']
    }
    
    df = pd.DataFrame(data)
    st.table(df)
    
    custom_header("AWS Storage Services", "section")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.image("https://d1.awsstatic.com/diagrams/product-page-diagrams/Product-Page-Diagram_Amazon-S3-DATA%20LAKE_HIW_1.51ec76dd97858c8fb6f509ca43db78a6b7d3097f.png", caption="AWS Storage Services")
    
    with col2:
        st.markdown("""
        **AWS provides various storage services for ML:**
        
        **Block Storage:**
        - Amazon EBS
        
        **File Storage:**
        - Amazon EFS
        - Amazon FSx for Windows File Server
        - Amazon FSx for Lustre
        - Amazon FSx for NetApp ONTAP
        - Amazon FSx for OpenZFS
        
        **Object Storage:**
        - Amazon S3
        """)
        
        info_box("Amazon S3 is commonly used for ML datasets due to its scalability, durability, and integration with other AWS services", "tip")
    
    custom_header("Data Ingestion Services", "section")
    
    st.markdown("""
    AWS provides several services for data ingestion, allowing you to collect and process data from various sources.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Real-time Data Streaming")
        st.markdown("""
        - **Amazon Kinesis**
          - Kinesis Data Streams
          - Kinesis Data Firehose
          - Managed Service for Apache Flink
        
        - **Amazon MSK**
          - Managed Streaming for Apache Kafka
          - MSK Connect
        """)
    
    with col2:
        st.markdown("### Batch Processing and Data Transfer")
        st.markdown("""
        - **AWS CLI & SDKs**
        - **AWS Lambda**
        - **AWS Glue**
        - **AWS Database Migration Service**
        - **AWS DataSync**
        - **AWS Snowball**
        - **Amazon S3 Transfer Acceleration**
        """)
    
    custom_header("Data Lakes and Warehouses", "section")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Data Lake")
        st.image("https://d1.awsstatic.com/s3-pdx.1a68536c0b5591ec0e2c7d5eddeb0f944436ca18.png", width=400)
        st.markdown("""
        - A central repository for all structured and unstructured data
        - Store data at any scale
        - No need to define schema upfront
        - Commonly built on Amazon S3
        - Suitable for machine learning workloads
        """)
    
    with col2:
        st.markdown("### Data Warehouse")
        st.image("https://d1.awsstatic.com/reInvent/reinvent-2022/redshift/Product-Page-Diagram_Amazon-Redshift-Data-Sharing-in-a-data-mesh_HIW%402x.15abcfb06a787375519723991baa168eec7c90d9.png", width=400)
        st.markdown("""
        - Optimized for analytics
        - Structured data with predefined schema
        - Used for business intelligence
        - Examples: Amazon Redshift
        - Complements ML workflows with prepared data
        """)

# Data Transformation page
elif st.session_state['current_page'] == 'Data Transformation':
    custom_header("Data Transformation")
    
    st.markdown("""
    Data transformation is the process of converting data from one format or structure to another.
    It is a crucial step in the data preparation phase of the machine learning lifecycle.
    """)
    
    custom_header("Data Cleaning", "sub")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        Data cleaning is the process of identifying and correcting (or removing) errors, inconsistencies, 
        and inaccuracies in datasets to improve data quality.
        
        Common data quality issues include:
        - Missing values
        - Duplicate records
        - Outliers
        - Inconsistent formatting
        - Data entry errors
        """)
        
        # Example of data with issues
        data = {
            'Age': [39, 25, 50, 38, 49, 52, 131, 54, 38, 40],
            'Workclass': ['State-gov', 'Private', 'Self-emp-not-inc', 'Private', 'Private', 'Self-emp-not-inc', 'Private', '', 'Private', 'Private'],
            'Education': ['Bachelors', 'Masters', 'Bach', 'HS-grad', '9th', 'HS-grad', 'masters', 'Some-college', 'HS-grad', 'Assoc-voc'],
            'Occupation': ['Adm-clerical', 'Farming-fishing', 'Exec-managerial', 'Handlers-cleaners', 'blank', 'Exec-managerial', 'Prof-specialty', '?', 'Handlers-cleaners', 'Craft-repair'],
            'Hours_per_week': [40, 99, 13, 40, 16, 45, 50, 60, 40, 40],
            'Income': ['<=50K', '>50K', '<=50K', '<=50K', '<=50K', '>50K', '>50K', '>50K', '<=50K', '>50K']
        }
        df = pd.DataFrame(data)
        
        st.markdown("### Example dataset with quality issues:")
        st.dataframe(df, use_container_width=True)
        
        st.markdown("""
        **Issues in this dataset:**
        - Missing values (blank, ?)
        - Inconsistent formatting (Bach vs. Bachelors, masters vs. Masters)
        - Outliers (Age 131, 99 hours per week)
        - Duplicate rows (rows 4 and 9 are similar)
        """)
    
    with col2:
        info_box("""
        **Data Cleaning Techniques:**
        
        1. **Handle Missing Values**
           - Remove rows/columns
           - Impute with mean, median, mode
           - Use advanced imputation methods
        
        2. **Remove Duplicates**
           - Identify exact or nearly identical records
           - Remove or merge duplicates
        
        3. **Handle Outliers**
           - Detect using statistical methods
           - Remove, cap, or transform outliers
        
        4. **Standardize Formats**
           - Consistent date formats
           - Consistent text case
           - Standardize categorical values
        
        5. **Correct Errors**
           - Fix typos
           - Validate values against constraints
        """, "info")
        
        st.image("https://miro.medium.com/max/1400/1*KzmIUYPmxgEHhXX7SlnpRw.jpeg", caption="Data Cleaning Process")
    
    custom_header("Categorical Encoding", "section")
    
    st.markdown("""
    Categorical encoding is the process of converting categorical variables into a format that machine learning algorithms can work with.
    Most ML algorithms require numerical input, so categorical data needs to be converted to numbers.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Types of Categorical Data")
        st.markdown("""
        - **Binary**: Yes/No, True/False
        - **Nominal**: Categories with no order (e.g., colors, cities)
        - **Ordinal**: Categories with natural order (e.g., small, medium, large)
        """)
    
    with col2:
        st.markdown("### Label Encoding")
        st.image("https://miro.medium.com/v2/resize:fit:640/format:webp/0*a3TcO_s-SUS3Xtmq.png", caption="Label Encoding")
        st.markdown("""
        - Maps each category to a number
        - Good for ordinal data
        - Example: Small → 1, Medium → 2, Large → 3
        - Warning: Can create false relationships
        """)
    
    with col3:
        st.markdown("### One-Hot Encoding")
        st.image("https://miro.medium.com/v2/resize:fit:720/format:webp/1*MBXp5nefzGYSIfpeMoax0Q.png", caption="One-Hot Encoding")
        st.markdown("""
        - Creates binary columns for each category
        - Good for nominal data
        - Avoids false relationships
        - Example: Red → [1,0,0], Green → [0,1,0], Blue → [0,0,1]
        """)
    
    info_box("""
    **When to use which encoding method:**
    
    - **Label Encoding**: Best for ordinal data where order matters
    
    - **One-Hot Encoding**: Best for nominal data with no inherent order
    
    - **Binary Encoding**: Useful when there are many categories (converts to binary representation)
    
    - **Frequency or Target Encoding**: Replaces categories with statistical measures
    """, "tip")
    
    custom_header("AWS Services for Data Transformation", "section")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Amazon SageMaker Data Wrangler")
        st.image("https://d1.awsstatic.com/lineage/product-page-diagram_SageMaker_Data-Wrangler-How-it-Works.01bbed559a60a547c410def9986bc8ab42445e1d.png", width=400)
        st.markdown("""
        - Visual interface for data preparation
        - 300+ built-in transformations
        - Connect to multiple data sources
        - No-code data preparation
        - Integration with SageMaker ecosystem
        """)
    
    with col2:
        st.markdown("### AWS Glue")
        st.image("https://d1.awsstatic.com/diagrams/product-page-diagram_aws-batch-how-it-works_110d1e1cedc264f07a985b4dfd1e390a03b9a04a.png", width=400)
        st.markdown("""
        - Fully managed ETL service
        - Connect to various data sources
        - Transform data with Apache Spark
        - Catalog data with AWS Glue Data Catalog
        - Create ETL jobs without complex coding
        """)
    
    st.markdown("### Other AWS Services for Data Transformation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### AWS Glue DataBrew")
        st.markdown("""
        - Visual data preparation tool
        - 250+ pre-built transformations
        - No coding required
        - Visualize data quality statistics
        """)
    
    with col2:
        st.markdown("#### AWS Lambda")
        st.markdown("""
        - Serverless compute service
        - Run lightweight data processing
        - Real-time data transformation
        - Event-driven architecture
        """)
    
    with col3:
        st.markdown("#### Amazon EMR")
        st.markdown("""
        - Managed Hadoop framework
        - Run Spark, Hive, Presto
        - Process large-scale data
        - Advanced data transformations
        """)

# Feature Engineering page
elif st.session_state['current_page'] == 'Feature Engineering':
    custom_header("Feature Engineering")
    
    st.markdown("""
    Feature engineering is the process of transforming raw data into features that better represent the underlying problem to predictive models,
    resulting in improved model accuracy on unseen data.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Feature engineering is often considered both an art and a science:
        
        - It requires domain knowledge and creativity
        - It involves transforming raw data into a format that ML algorithms can work with
        - Well-engineered features can significantly improve model performance
        - Feature engineering is often the most time-consuming part of ML projects
        """)
    
    with col2:
        info_box("""
        **Key Terminology:**
        
        - **Feature**: An attribute or independent variable used in a predictive model
        
        - **Target/Label**: What you're trying to predict (dependent variable)
        
        - **Feature Engineering**: Process of transforming raw data into features
        
        - **Feature Selection**: Process of selecting the most valuable features
        """, "info")
    
    custom_header("The Curse of Dimensionality", "section")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        The **curse of dimensionality** refers to the problems that arise when analyzing data in high-dimensional spaces.
        
        As the number of features increases:
        
        - The amount of data needed to generalize accurately grows exponentially
        - Models become more complex and prone to overfitting
        - Distance metrics become less meaningful
        - Computational resources required increase significantly
        
        **This is why feature selection and dimensionality reduction are important**
        """)
        
        st.image("https://miro.medium.com/v2/resize:fit:1400/1*qODKsRQQR_7XvJh_UwLDEA.png", caption="Curse of Dimensionality")
    
    with col2:
        st.markdown("### Impact on Model Performance")
        
        # Create sample data to show impact
        dims = np.arange(1, 101, 10)
        accuracy = 90 - 20 * np.log10(dims/10)
        
        # Create plot
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(dims, accuracy)
        ax.set_xlabel('Number of Features (Dimensions)')
        ax.set_ylabel('Model Performance')
        ax.set_title('Impact of Dimensionality on Performance')
        ax.grid(True)
        
        st.pyplot(fig)
        
        info_box("""
        Ideally, you should try to include as many meaningful features as possible before performance declines.
        
        Feature engineering and selection help balance this tradeoff.
        """, "tip")
    
    custom_header("Feature Engineering Techniques", "sub")
    
    st.markdown("""
    Different types of feature engineering techniques can be applied depending on the data type and the specific problem.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Feature Creation")
        st.markdown("""
        Creating new features based on:
        - Domain knowledge
        - Data patterns
        - Mathematical combinations
        
        **Examples:**
        - Ratio of height to weight
        - Days since last purchase
        - Distance between points
        """)
        
        st.markdown("### Feature Transformation")
        st.markdown("""
        Changing the scale or distribution of features:
        - Log transformation
        - Polynomial features
        - Box-Cox transformation
        
        **Examples:**
        - Log of income 
        - Square of age
        - Sine/cosine of cyclical features
        """)
    
    with col2:
        st.markdown("### Feature Selection")
        st.markdown("""
        Selecting the most relevant features:
        - Filter methods (correlation, chi-square)
        - Wrapper methods (recursive feature elimination)
        - Embedded methods (LASSO, decision trees)
        
        **Examples:**
        - Selecting top-k features by correlation
        - Using feature importance from tree-based models
        """)
        
        st.markdown("### Feature Scaling")
        st.markdown("""
        Normalizing feature ranges:
        - Min-Max Scaling
        - Standard Scaling (Z-score)
        - Robust Scaling
        
        **Examples:**
        - Scaling age to [0,1] range
        - Standardizing income to mean=0, std=1
        """)
    
    custom_header("Feature Scaling Methods Comparison", "section")
    
    # Generate sample data
    np.random.seed(42)
    data = np.random.normal(50, 10, 100)
    data = np.append(data, [5, 95])  # Add outliers
    
    # Create different scalers
    original = data
    min_max = (data - data.min()) / (data.max() - data.min())
    standard = (data - data.mean()) / data.std()
    robust = (data - np.median(data)) / (np.percentile(data, 75) - np.percentile(data, 25))
    
    # Plot the distributions
    fig, axs = plt.subplots(4, 1, figsize=(10, 8))
    
    axs[0].hist(original, bins=20, alpha=0.7)
    axs[0].set_title('Original Data')
    
    axs[1].hist(min_max, bins=20, alpha=0.7)
    axs[1].set_title('Min-Max Scaling [0,1]')
    
    axs[2].hist(standard, bins=20, alpha=0.7)
    axs[2].set_title('Standard Scaling (Z-score)')
    
    axs[3].hist(robust, bins=20, alpha=0.7)
    axs[3].set_title('Robust Scaling (using quartiles)')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    info_box("""
    **Scaling Method Selection:**
    
    - **Min-Max Scaling**: Best when you need values in a specific range [0,1]
    
    - **Standard Scaling**: Best for data with normal distribution
    
    - **Robust Scaling**: Best when outliers are present
    """, "tip")
    
    custom_header("Amazon SageMaker Feature Store", "section")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.image("https://d1.awsstatic.com/reInvent/reinvent-2022/sagemaker/Product-Page-Diagram_Amazon-SageMaker-Feature-Store%402x.d90936a516a0d6ce6ea7a4720769d080a4c8cf9b.png", width=500)
        
        st.markdown("""
        Amazon SageMaker Feature Store is a purpose-built repository for machine learning (ML) features.
        
        **Key capabilities:**
        - Store, discover, and share features securely
        - Online and offline feature storage
        - Millisecond latency for online inference
        - Consistent feature values across training and inference
        - Visual search for feature discovery
        - Sharing and collaboration across teams
        """)
    
    with col2:
        st.markdown("### Benefits of Feature Store")
        st.markdown("""
        - **Reuse features** across multiple models
        - **Reduce duplication** of feature engineering work
        - **Ensure consistency** between training and inference
        - **Track lineage** of features for governance
        - **Reduce latency** for real-time predictions
        - **Centralize feature management** for teams
        """)
        
        info_box("""
        Feature Store supports both online low-latency lookups for real-time inference, and offline storage for batch training.
        
        This dual storage pattern ensures feature consistency across the ML lifecycle.
        """, "success")

# Data Integrity page
elif st.session_state['current_page'] == 'Data Integrity':
    custom_header("Data Integrity and Preparation for Modeling")
    
    st.markdown("""
    Ensuring data integrity and properly preparing data for modeling are crucial steps before training a model.
    These processes help create high-quality datasets that lead to more accurate and reliable models.
    """)
    
    custom_header("Class Imbalance", "sub")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        **Class imbalance** occurs when the classes in your target variable are not represented equally in your dataset.
        
        For example, in a fraud detection dataset, fraudulent transactions might represent only 0.1% of all transactions.
        
        Class imbalance can lead to:
        - Models that always predict the majority class
        - Poor performance on minority classes
        - Misleading evaluation metrics
        
        **Why it matters:**
        - Models tend to focus on majority class
        - Risk of bias against minority groups
        - Critical events (like fraud) often belong to minority classes
        """)
        
        # Create a sample imbalanced dataset visualization
        labels = ['Not Fraud (99.9%)', 'Fraud (0.1%)']
        sizes = [999, 1]
        
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#5DADE2', '#EC7063'])
        ax.axis('equal')
        plt.title('Example: Imbalanced Fraud Detection Dataset')
        
        st.pyplot(fig)
    
    with col2:
        info_box("""
        **Detecting Class Imbalance:**
        
        1. Calculate the ratio of classes
        2. Visualize class distribution
        3. Check performance metrics by class
        
        **Metrics affected by imbalance:**
        - Accuracy can be misleading
        - Instead, use:
          - Precision
          - Recall
          - F1-score
          - Area Under ROC Curve (AUC)
        """, "warning")
        
        st.markdown("### Amazon SageMaker Clarify")
        st.image("https://d1.awsstatic.com/SageMaker-Clarify-How-it-works.3e1739db812b5d9ad35ec0f2164769565df7c749.png", width=400)
        
        st.markdown("""
        Amazon SageMaker Clarify helps detect bias in your data and models:
        
        - Identify imbalances during data preparation
        - Evaluate bias in trained models
        - Generate automated bias reports
        - Track bias drift over time
        """)
    
    custom_header("Techniques to Handle Class Imbalance", "section")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Random Oversampling")
        st.image("https://miro.medium.com/max/640/1*YPA2BrCmGpBMWy-M27yKKA.png", width=200)
        st.markdown("""
        - Duplicates examples from the minority class
        - Increases minority samples until balanced
        - Easy to implement
        - Risk of overfitting to minority samples
        """)
    
    with col2:
        st.markdown("### Random Undersampling")
        st.image("https://miro.medium.com/max/640/1*6Vq_7NT7_lXbmBIirJ_htg.png", width=200)
        st.markdown("""
        - Removes examples from the majority class
        - Reduces majority samples until balanced
        - May lose valuable information
        - Works well with abundant data
        """)
    
    with col3:
        st.markdown("### SMOTE")
        st.image("https://miro.medium.com/max/640/1*c87MvS3jzBY6Ja5xwBZbgA.png", width=200)
        st.markdown("""
        - Synthetic Minority Oversampling Technique
        - Creates synthetic examples from minority class
        - Uses interpolation between existing samples
        - Reduces overfitting compared to random oversampling
        """)
    
    st.markdown("""
    **Amazon SageMaker Data Wrangler** provides built-in transforms for handling class imbalance,
    including Random Oversampling, Random Undersampling, and SMOTE.
    """)
    
    custom_header("Dataset Splitting", "sub")
    
    st.markdown("""
    Dataset splitting is the process of dividing your dataset into subsets for training, validation, and testing.
    Proper splitting ensures your model generalizes well to new, unseen data.
    """)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.image("https://miro.medium.com/max/1400/1*Nv2NNALuokZEcV6hYEHdGA.png", caption="Training, Validation, and Test Splits")
        
        st.markdown("""
        **Common Splitting Ratios:**
        - 70% Training, 15% Validation, 15% Test
        - 80% Training, 10% Validation, 10% Test
        
        **Purpose of each split:**
        
        - **Training data**: Used to train the model parameters
        - **Validation data**: Used for tuning hyperparameters and preventing overfitting
        - **Test data**: Used for final evaluation of model performance
        """)
    
    with col2:
        st.markdown("### Splitting Techniques")
        
        st.markdown("#### Simple Hold-out")
        st.markdown("""
        - Random split into training, validation, and test sets
        - Simple and commonly used
        - Can be problematic with small datasets
        """)
        
        st.markdown("#### Cross-validation")
        st.markdown("""
        - Data is divided into k folds
        - Model trained k times, each time using k-1 folds for training and 1 fold for validation
        - Results are averaged across all runs
        - More robust estimate of performance
        - Computationally more expensive
        """)
        
        info_box("""
        **Best Practices for Splitting:**
        
        - Maintain same distribution across splits
        - Stratify splits for class balance
        - Consider time-based splits for time series
        - Use same random seed for reproducibility
        """, "tip")
    
    custom_header("Data Shuffling and Augmentation", "section")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Data Shuffling")
        st.markdown("""
        **Data shuffling** randomizes the order of examples in your dataset.
        
        **Benefits:**
        - Prevents model from learning order-dependent patterns
        - Helps with stochastic gradient descent optimization
        - Reduces bias from sequential patterns
        
        **Techniques:**
        - Random permutation (full dataset shuffle)
        - Epoch-based shuffling
        - Mini-batch shuffling
        """)
    
    with col2:
        st.markdown("### Data Augmentation")
        st.markdown("""
        **Data augmentation** creates new training examples by applying transformations to existing data.
        
        **Benefits:**
        - Increases dataset size
        - Improves model generalization
        - Reduces overfitting
        - Helps with class imbalance
        
        **Domain-specific techniques:**
        - Images: rotation, flipping, cropping, color changes
        - Text: synonym replacement, back-translation
        - Time series: time warping, jittering, scaling
        """)
    
    st.markdown("### Types of Data Augmentation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Image Augmentation")
        st.image("https://miro.medium.com/max/1400/1*mA1blos7f5LZbhWUHZI2dg.png", width=300)
        st.markdown("""
        - Rotation, flipping, zooming
        - Color space transformations
        - Random cropping
        - Noise injection
        - Image mixing (CutMix, MixUp)
        """)
    
    with col2:
        st.markdown("#### Text Augmentation")
        st.image("https://miro.medium.com/max/1400/1*zBXBfFMAH4gv-JBzhEDDkA.png", width=300)
        st.markdown("""
        - Synonym replacement
        - Random insertion/deletion
        - Word swapping
        - Back-translation
        - Text generation using language models
        """)
    
    with col3:
        st.markdown("#### Time Series Augmentation")
        st.image("https://miro.medium.com/max/1400/1*QpGO_DpGGgcj9c4UoFEQjA.png", width=300)
        st.markdown("""
        - Time warping
        - Magnitude warping
        - Window slicing
        - Jittering (adding noise)
        - Synthetic data generation
        """)

# Quiz page
elif st.session_state['current_page'] == 'Quiz':
    custom_header("Test Your Knowledge")
    
    st.markdown("""
    This quiz will test your understanding of the key concepts covered in Domain 1: Data Preparation for Machine Learning.
    """)
    
    # Define quiz questions
    questions = [
        {
            "question": "Which AWS storage service is commonly used for storing machine learning datasets?",
            "options": ["Amazon S3", "Amazon EBS", "Amazon RDS", "AWS Fargate"],
            "correct": "Amazon S3"
        },
        {
            "question": "What technique would you use to convert categorical data like ['Red', 'Blue', 'Green'] into numerical values for ML models?",
            "options": ["Feature scaling", "Data cleaning", "One-hot encoding", "Dimensionality reduction"],
            "correct": "One-hot encoding"
        },
        {
            "question": "Which technique is most suitable for handling class imbalance by creating synthetic examples of the minority class?",
            "options": ["Random undersampling", "SMOTE", "Feature scaling", "Cross-validation"],
            "correct": "SMOTE"
        },
        {
            "question": "What is the purpose of splitting a dataset into training, validation, and test sets?",
            "options": [
                "To ensure the model works with different types of data", 
                "To evaluate model performance on unseen data and prevent overfitting", 
                "To speed up the training process", 
                "To reduce the amount of data needed for training"
            ],
            "correct": "To evaluate model performance on unseen data and prevent overfitting"
        },
        {
            "question": "Which AWS service helps detect bias in ML models and understand model predictions?",
            "options": ["Amazon SageMaker Data Wrangler", "Amazon SageMaker Feature Store", "Amazon SageMaker Clarify", "Amazon Comprehend"],
            "correct": "Amazon SageMaker Clarify"
        }
    ]
    
    # Check if the quiz has been attempted
    if not st.session_state['quiz_attempted']:
        # Create a form for the quiz
        with st.form("quiz_form"):
            st.markdown("### Answer the following questions:")
            
            # Track user answers
            user_answers = []
            
            # Display each question
            for i, q in enumerate(questions):
                st.markdown(f"**Question {i+1}:** {q['question']}")
                answer = st.radio(f"Select your answer for question {i+1}:", q['options'], key=f"q{i}")
                user_answers.append(answer)
            
            # Submit button
            submitted = st.form_submit_button("Submit Quiz")
            
            if submitted:
                # Calculate score
                score = sum([1 for ua, q in zip(user_answers, questions) if ua == q['correct']])
                st.session_state['quiz_score'] = score
                st.session_state['quiz_attempted'] = True
                st.experimental_rerun()
    else:
        # Display results
        score = st.session_state['quiz_score']
        st.markdown(f"### Your Score: {score}/5")
        
        if score == 5:
            st.success("🎉 Perfect score! You've mastered the concepts of Data Preparation for ML!")
        elif score >= 3:
            st.success("👍 Good job! You have a solid understanding of the concepts.")
        else:
            st.warning("📚 You might want to review the content again to strengthen your understanding.")
        
        # Show correct answers
        st.markdown("### Review Questions and Answers:")
        
        for i, q in enumerate(questions):
            st.markdown(f"**Question {i+1}:** {q['question']}")
            st.markdown(f"**Correct Answer:** {q['correct']}")
            
            if i < len(questions) - 1:
                st.markdown("---")
        
        # Option to retake the quiz
        if st.button("Retake Quiz"):
            st.session_state['quiz_attempted'] = False
            st.experimental_rerun()

# Resources page
elif st.session_state['current_page'] == 'Resources':
    custom_header("Additional Resources")
    
    st.markdown("""
    Explore these resources to deepen your understanding of Data Preparation for Machine Learning.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### AWS Documentation")
        st.markdown("""
        - [Feature Engineering in Machine Learning](https://aws.amazon.com/what-is/feature-engineering/)
        - [Amazon SageMaker Data Wrangler](https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-transform.html)
        - [Amazon SageMaker Feature Store](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html)
        - [Amazon SageMaker Clarify](https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-detect-data-bias.html)
        - [AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/how-it-works.html)
        - [Amazon Redshift ML](https://docs.aws.amazon.com/redshift/latest/dg/machine_learning.html)
        - [AWS Lake Formation](https://docs.aws.amazon.com/lake-formation/latest/dg/what-is-lake-formation.html)
        """)
        
        st.markdown("### AWS Blog Posts")
        st.markdown("""
        - [Balance your data for machine learning with Amazon SageMaker Data Wrangler](https://aws.amazon.com/blogs/machine-learning/balance-your-data-for-machine-learning-with-amazon-sagemaker-data-wrangler/)
        - [Amazon Kinesis Data Firehose Zero Buffering](https://aws.amazon.com/about-aws/whats-new/2023/12/amazon-kinesis-data-firehose-zero-buffering/)
        """)
    
    with col2:
        st.markdown("### Training Courses")
        st.markdown("""
        - [AWS Technical Essentials](https://aws.amazon.com/training/learn-about/technical-essentials/)
        - [Getting Started with AWS Storage](https://aws.amazon.com/training/learn-about/storage/)
        - [AWS Cloud Quest: Machine Learning](https://aws.amazon.com/training/learn-about/cloud-quest/)
        - [AWS Machine Learning Specialty Certification](https://aws.amazon.com/certification/certified-machine-learning-specialty/)
        """)
        
        st.markdown("### Tools and Services")
        st.markdown("""
        - [Amazon SageMaker](https://aws.amazon.com/sagemaker/)
        - [AWS Glue](https://aws.amazon.com/glue/)
        - [Amazon S3](https://aws.amazon.com/s3/)
        - [Amazon Kinesis](https://aws.amazon.com/kinesis/)
        - [Amazon EMR](https://aws.amazon.com/emr/)
        - [AWS Lambda](https://aws.amazon.com/lambda/)
        - [Amazon Mechanical Turk](https://www.mturk.com/)
        """)
    
    st.markdown("### Additional Reading")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Data Collection")
        st.markdown("""
        - Data Lake vs. Data Warehouse
        - Structured vs. Unstructured Data
        - Data Storage Formats
        - Real-time Data Ingestion
        """)
    
    with col2:
        st.markdown("#### Data Transformation")
        st.markdown("""
        - Data Cleaning Best Practices
        - Categorical Encoding Techniques
        - Handling Missing Values
        - Outlier Detection and Treatment
        """)
    
    with col3:
        st.markdown("#### Feature Engineering")
        st.markdown("""
        - Feature Selection Methods
        - Dimensionality Reduction
        - Scaling and Normalization
        - Feature Store Architecture
        """)

# Footer
st.markdown("---")
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://d1.awsstatic.com/training-and-certification/certification-badges/AWS-Certified-Machine-Learning-Specialty_badge.5d259a8045a7d3c41ed927f8b3a9da3df1ec8a20.png", width=70)
with col2:
    st.markdown("**AWS Machine Learning Engineer - Associate | Domain 1: Data Preparation for ML**")
    st.markdown("© 2023 AWS Partner Certification Readiness")

# Progress tracking
if st.session_state['name']:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Your Progress")
    
    # Track visited pages
    visited_pages = [page for page in ["ML Lifecycle", "Data Collection", "Data Transformation", "Feature Engineering", "Data Integrity"] 
                     if st.session_state.get(f"visited_{page}", False)]
    
    progress = len(visited_pages) / 5
    st.sidebar.progress(progress)
    st.sidebar.markdown(f"**{len(visited_pages)}/5 sections completed**")
    
    # Track quiz score if attempted
    if st.session_state['quiz_attempted']:
        st.sidebar.markdown(f"**Quiz Score: {st.session_state['quiz_score']}/5**")

# Mark current page as visited
if st.session_state['current_page'] in ["ML Lifecycle", "Data Collection", "Data Transformation", "Feature Engineering", "Data Integrity"]:
    st.session_state[f"visited_{st.session_state['current_page']}"] = True
# ```

# To run this Streamlit application, you'll need to install the required packages:

# ```bash
# pip install streamlit pandas numpy matplotlib seaborn pillow streamlit_option_menu
# ```

# Then save the code as `app.py` and run it using:

# ```bash
# streamlit run app.py
# ```

# ## Application Overview

# This interactive e-learning application covers AWS Partner Certification Readiness for Machine Learning Engineer (Associate) with a focus on Domain 1: Data Preparation for Machine Learning. It's designed with a modern, user-friendly interface and includes the following features:

# 1. **Interactive Navigation**: A sidebar navigation menu allows users to easily move between different topics.

# 2. **Comprehensive Content Sections**:
#    - ML Lifecycle - Overview of the machine learning workflow
#    - Data Collection - Data sources, types, storage options
#    - Data Transformation - Cleaning and transforming data
#    - Feature Engineering - Creating and selecting features
#    - Data Integrity - Ensuring data quality and handling imbalance
#    - Quiz - Interactive assessment
#    - Resources - Additional learning materials

# 3. **Visual Learning**: The application includes diagrams, charts, and visualizations to explain complex concepts.

# 4. **Interactive Elements**: Progress tracking, quiz with immediate feedback, and user personalization.

# 5. **Modern Styling**: Clean, professional UI with consistent formatting, color schemes, and responsive layout.

# 6. **Session Management**: Users can reset their session at any time, and all session state variables are properly initialized.

# The application would be extremely helpful for AWS partners preparing for the Machine Learning Engineer certification, as it covers all the key concepts from Domain 1 in an engaging and interactive format.