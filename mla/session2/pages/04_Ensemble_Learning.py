
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification, make_regression, load_breast_cancer, load_diabetes
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, StackingClassifier, BaggingClassifier
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor, StackingRegressor, BaggingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score, classification_report, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
import plotly.express as px
import plotly.graph_objects as go
import time
from PIL import Image
import base64
import io
from st_clickable_images import clickable_images

# AWS Color Palette
AWS_COLORS = {
    "squid_ink": "#232F3E",
    "anchor": "#0073BB",
    "anchor_light": "#00A1C9",
    "activation": "#FF9900",
    "activation_light": "#FFAC31",
    "lime": "#7AA116",
    "slate": "#687078",
    "red": "#D13212",
    "white": "#FFFFFF",
    "background": "#F8F8F8"
}

# Set page configuration
st.set_page_config(
    page_title="Ensemble Learning Explorer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling for modern UI
st.markdown("""
<style>
    .main {
        background-color: #F8F8F8;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #FFFFFF;
        border-radius: 4px;
        padding: 10px 16px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF9900 !important;
        color: white !important;
    }
    h1, h2, h3 {
        color: #232F3E;
    }
    .highlight {
        background-color: #0073BB;
        color: white;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }
    .card {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
    }
    .button {
        background-color: #FF9900;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        cursor: pointer;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
    }
    .button:hover {
        background-color: #FFAC31;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'dataset' not in st.session_state:
    st.session_state.dataset = None
if 'X_train' not in st.session_state:
    st.session_state.X_train = None
if 'X_test' not in st.session_state:
    st.session_state.X_test = None 
if 'y_train' not in st.session_state:
    st.session_state.y_train = None
if 'y_test' not in st.session_state:
    st.session_state.y_test = None
if 'task_type' not in st.session_state:
    st.session_state.task_type = 'classification'
if 'model_results' not in st.session_state:
    st.session_state.model_results = {}

# Sidebar for session management
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Amazon_Web_Services_Logo.svg/1200px-Amazon_Web_Services_Logo.svg.png", width=200)
    st.title("E-Learning Session")
    st.markdown("---")
    
    # Session management
    st.subheader("🔄 Session Management")
    if st.button("Reset Session"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.page = 'home'
        st.rerun()
    
    # Data generation options
    st.subheader("🛠️ Configuration")
    task = st.radio("Select Task Type:", ["Classification", "Regression"])
    st.session_state.task_type = task.lower()
    
    dataset_option = st.selectbox(
        "Select Dataset:",
        ["Generated Data", "Breast Cancer (Classification)", "Diabetes (Regression)"]
    )
    
    if st.button("Generate Data"):
        with st.spinner("Generating dataset..."):
            if dataset_option == "Generated Data":
                if st.session_state.task_type == 'classification':
                    X, y = make_classification(
                        n_samples=1000, n_features=20, n_informative=10,
                        n_redundant=5, random_state=42
                    )
                else:
                    X, y = make_regression(
                        n_samples=1000, n_features=20, n_informative=10,
                        random_state=42, noise=0.1
                    )
            elif dataset_option == "Breast Cancer (Classification)":
                data = load_breast_cancer()
                X, y = data.data, data.target
                st.session_state.task_type = 'classification'
            elif dataset_option == "Diabetes (Regression)":
                data = load_diabetes()
                X, y = data.data, data.target
                st.session_state.task_type = 'regression'
                
            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Store in session state
            st.session_state.X_train = X_train
            st.session_state.X_test = X_test
            st.session_state.y_train = y_train
            st.session_state.y_test = y_test
            st.session_state.dataset = dataset_option
            
            st.success("✅ Data generated successfully!")
    
    st.markdown("---")
    st.info("📚 This application provides interactive examples of ensemble learning methods in machine learning.")

# Main content
st.title("🤖 Ensemble Learning Explorer")
st.markdown("""
<div class="card">
    <h3>Welcome to the Interactive Ensemble Learning Explorer!</h3>
    <p>Explore different ensemble learning techniques through interactive examples and visualizations. 
    Use the tabs below to navigate between different methods.</p>
    <p><strong>First step:</strong> Generate a dataset using the sidebar options.</p>
</div>
""", unsafe_allow_html=True)

# Create tabs for different ensemble methods
tabs = st.tabs([
    "🏠 Home", 
    "🌲 Bagging", 
    "🚀 Boosting", 
    "🏗️ Stacking"
])

# Home tab
with tabs[0]:
    st.header("Understanding Ensemble Learning")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>What is Ensemble Learning?</h3>
            <p>Ensemble learning is a machine learning paradigm where multiple models (called "weak learners") 
            are trained to solve the same problem and combined to get better results. The main hypothesis is that 
            when weak models are correctly combined, we can obtain more accurate and/or robust models.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3>Why Use Ensemble Methods?</h3>
            <ul>
                <li><strong>Improved accuracy:</strong> Combining multiple models often yields better predictions</li>
                <li><strong>Reduced overfitting:</strong> Ensembles help in reducing model variance</li>
                <li><strong>Increased stability:</strong> Less sensitive to peculiarities of the data</li>
                <li><strong>Better insights:</strong> Different models may capture different aspects of the data</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image("https://miro.medium.com/max/1200/1*4G__SV580CxFj-xlBw_Zvg.png", caption="Ensemble Learning Concept")
        
        st.markdown("""
        <div class="card">
            <h3>Main Categories:</h3>
            <ul>
                <li><strong>Bagging:</strong> Train models in parallel on random subsets</li>
                <li><strong>Boosting:</strong> Train models sequentially, each focusing on previous errors</li>
                <li><strong>Stacking:</strong> Combine predictions using another learning algorithm</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("Getting Started")
    st.markdown("""
    <ol>
        <li>Use the sidebar to select a dataset and task type (classification or regression)</li>
        <li>Click "Generate Data" to prepare your dataset</li>
        <li>Navigate through the tabs to explore different ensemble learning techniques</li>
        <li>Experiment with parameters and observe how they affect model performance</li>
    </ol>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="card" style="background-color: #F0F7FF;">
            <h3 style="color: #0073BB;">🌲 Bagging</h3>
            <p>Bootstrap Aggregating - trains multiple models on random subsets of the training data.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card" style="background-color: #FFF8F0;">
            <h3 style="color: #FF9900;">🚀 Boosting</h3>
            <p>Sequentially trains models, with each new model focusing on the errors of previous ones.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card" style="background-color: #F0FFF4;">
            <h3 style="color: #7AA116;">🏗️ Stacking</h3>
            <p>Combines multiple models using another meta-model to optimize the outputs.</p>
        </div>
        """, unsafe_allow_html=True)

# Bagging tab
with tabs[1]:
    st.header("🌲 Bagging (Bootstrap Aggregating)")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>What is Bagging?</h3>
            <p>Bagging, short for Bootstrap Aggregating, is an ensemble technique that involves training multiple instances 
            of the same model on different subsets of the training data and then combining their predictions.</p>
            <p>The key idea is to reduce variance and avoid overfitting by creating multiple versions of the base model 
            that are different due to the randomness in the bootstrap sampling.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3>How Bagging Works:</h3>
            <ol>
                <li>Create multiple random subsets (bootstrap samples) of the training data</li>
                <li>Train a base model on each subset</li>
                <li>Combine predictions by voting (classification) or averaging (regression)</li>
            </ol>
            <p>Popular examples include Random Forests, which use bagging with decision trees.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image("https://miro.medium.com/max/1200/1*_NJ9oPKK1BnCYLMxmVgA_w.png", caption="Bagging Process")
        
        st.markdown("""
        <div class="card">
            <h3>Advantages of Bagging:</h3>
            <ul>
                <li>Reduces variance without increasing bias</li>
                <li>Reduces overfitting</li>
                <li>Provides more stable predictions</li>
                <li>Models can be trained in parallel</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Interactive Bagging Demo
    st.subheader("Interactive Bagging Demo")
    
    if st.session_state.X_train is not None:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            n_estimators = st.slider(
                "Number of Base Estimators", 
                min_value=1, 
                max_value=100, 
                value=10,
                key="bagging_n_estimators"
            )
            
            max_samples = st.slider(
                "Max Samples (% of training data)", 
                min_value=10, 
                max_value=100, 
                value=80,
                key="bagging_max_samples"
            ) / 100.0
            
            max_features = st.slider(
                "Max Features (% of features used)", 
                min_value=10, 
                max_value=100, 
                value=80,
                key="bagging_max_features"
            ) / 100.0
            
            bootstrap = st.checkbox("Bootstrap", value=True, key="bagging_bootstrap")
            
            if st.button("Train Bagging Model", key="train_bagging"):
                with st.spinner("Training..."):
                    if st.session_state.task_type == 'classification':
                        # Base model
                        base_model = DecisionTreeClassifier(max_depth=3)
                        base_model.fit(st.session_state.X_train, st.session_state.y_train)
                        base_preds = base_model.predict(st.session_state.X_test)
                        base_accuracy = accuracy_score(st.session_state.y_test, base_preds)
                        
                        # Bagging model
                        bagging_model = BaggingClassifier(
                            estimator=DecisionTreeClassifier(max_depth=3),
                            n_estimators=n_estimators,
                            max_samples=max_samples,
                            max_features=max_features,
                            bootstrap=bootstrap,
                            random_state=42
                        )
                        
                        bagging_model.fit(st.session_state.X_train, st.session_state.y_train)
                        bagging_preds = bagging_model.predict(st.session_state.X_test)
                        bagging_accuracy = accuracy_score(st.session_state.y_test, bagging_preds)
                        
                        # Store results
                        st.session_state.model_results["bagging"] = {
                            "base_accuracy": base_accuracy,
                            "bagging_accuracy": bagging_accuracy,
                            "conf_matrix": confusion_matrix(st.session_state.y_test, bagging_preds),
                            "classification_report": classification_report(st.session_state.y_test, bagging_preds, output_dict=True)
                        }
                        
                    else:  # regression
                        # Base model
                        base_model = DecisionTreeRegressor(max_depth=3)
                        base_model.fit(st.session_state.X_train, st.session_state.y_train)
                        base_preds = base_model.predict(st.session_state.X_test)
                        base_mse = mean_squared_error(st.session_state.y_test, base_preds)
                        base_r2 = r2_score(st.session_state.y_test, base_preds)
                        
                        # Bagging model
                        bagging_model = BaggingRegressor(
                            estimator=DecisionTreeRegressor(max_depth=3),
                            n_estimators=n_estimators,
                            max_samples=max_samples,
                            max_features=max_features,
                            bootstrap=bootstrap,
                            random_state=42
                        )
                        
                        bagging_model.fit(st.session_state.X_train, st.session_state.y_train)
                        bagging_preds = bagging_model.predict(st.session_state.X_test)
                        bagging_mse = mean_squared_error(st.session_state.y_test, bagging_preds)
                        bagging_r2 = r2_score(st.session_state.y_test, bagging_preds)
                        
                        # Store results
                        st.session_state.model_results["bagging"] = {
                            "base_mse": base_mse,
                            "base_r2": base_r2,
                            "bagging_mse": bagging_mse,
                            "bagging_r2": bagging_r2
                        }
                
                st.success("✅ Bagging model trained successfully!")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if "bagging" in st.session_state.model_results:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                if st.session_state.task_type == 'classification':
                    # Get results
                    results = st.session_state.model_results["bagging"]
                    
                    # Create a comparison bar chart
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=['Base Model', 'Bagging Model'],
                        y=[results["base_accuracy"] * 100, results["bagging_accuracy"] * 100],
                        text=[f'{results["base_accuracy"]:.2%}', f'{results["bagging_accuracy"]:.2%}'],
                        textposition='auto',
                        marker_color=[AWS_COLORS["slate"], AWS_COLORS["anchor"]]
                    ))
                    fig.update_layout(
                        title='Model Accuracy Comparison',
                        yaxis_title='Accuracy (%)',
                        yaxis=dict(range=[0, 100]),
                        height=350
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display confusion matrix
                    st.subheader("Confusion Matrix")
                    class_report = results["classification_report"]
                    cm = results["conf_matrix"]
                    
                    fig = px.imshow(
                        cm, 
                        text_auto=True,
                        color_continuous_scale=px.colors.sequential.Blues,
                        labels=dict(x="Predicted Label", y="True Label"),
                        x=['Class 0', 'Class 1'],
                        y=['Class 0', 'Class 1']
                    )
                    fig.update_layout(height=350)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display classification report
                    st.subheader("Classification Report")
                    report_df = pd.DataFrame(class_report).transpose()
                    st.dataframe(report_df.style.highlight_max(axis=0))
                    
                else:  # regression
                    # Get results
                    results = st.session_state.model_results["bagging"]
                    
                    # Create plots
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # MSE Comparison
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            x=['Base Model', 'Bagging Model'],
                            y=[results["base_mse"], results["bagging_mse"]],
                            text=[f'{results["base_mse"]:.4f}', f'{results["bagging_mse"]:.4f}'],
                            textposition='auto',
                            marker_color=[AWS_COLORS["slate"], AWS_COLORS["anchor"]]
                        ))
                        fig.update_layout(
                            title='Mean Squared Error (Lower is Better)',
                            yaxis_title='MSE',
                            height=350
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # R² Comparison
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            x=['Base Model', 'Bagging Model'],
                            y=[results["base_r2"], results["bagging_r2"]],
                            text=[f'{results["base_r2"]:.4f}', f'{results["bagging_r2"]:.4f}'],
                            textposition='auto',
                            marker_color=[AWS_COLORS["slate"], AWS_COLORS["anchor"]]
                        ))
                        fig.update_layout(
                            title='R² Score (Higher is Better)',
                            yaxis_title='R²',
                            height=350
                        )
                        st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("""
                <div class="card">
                    <h3>Interpreting the Results:</h3>
                    <ul>
                        <li>Bagging typically improves performance by reducing variance</li>
                        <li>Increasing the number of estimators generally helps but with diminishing returns</li>
                        <li>The optimal max_samples and max_features values depend on the dataset</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Train the model to see the results!")
    else:
        st.warning("Please generate a dataset first using the sidebar options.")

    st.markdown("---")
    
    st.subheader("Real-World Applications")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>Random Forests</h3>
            <p>Random Forests are the most popular implementation of bagging. They combine bagging with random feature selection 
            to create diverse decision trees.</p>
            <ul>
                <li>Used in finance for credit risk assessment</li>
                <li>Medical diagnosis and disease prediction</li>
                <li>Customer churn prediction in telecommunications</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>Pasting</h3>
            <p>A variation of bagging that samples without replacement instead of bootstrap sampling</p>
            <ul>
                <li>Image classification tasks</li>
                <li>Text categorization systems</li>
                <li>Anomaly detection in network security</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Boosting Tab
with tabs[2]:
    st.header("🚀 Boosting")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>What is Boosting?</h3>
            <p>Boosting is an ensemble technique that combines multiple weak learners into a strong learner 
            by training models sequentially, with each new model focusing on the errors of the previous ones.</p>
            <p>The key idea is to give more weight to observations that were previously misclassified, 
            forcing subsequent models to focus on difficult cases.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3>How Boosting Works:</h3>
            <ol>
                <li>Train a base model on the original data</li>
                <li>Identify misclassified instances</li>
                <li>Increase the weight of misclassified instances</li>
                <li>Train a new model on the weighted data</li>
                <li>Continue this process sequentially</li>
                <li>Combine models using weighted voting</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image("https://miro.medium.com/max/1200/1*Vc4vmEPwQfPP1qkDzFGnMQ.png", caption="Boosting Process")
        
        st.markdown("""
        <div class="card">
            <h3>Popular Boosting Algorithms:</h3>
            <ul>
                <li><strong>AdaBoost:</strong> One of the first boosting algorithms</li>
                <li><strong>Gradient Boosting:</strong> Uses gradient descent to minimize errors</li>
                <li><strong>XGBoost:</strong> Optimized implementation with regularization</li>
                <li><strong>LightGBM:</strong> Faster implementation focused on efficiency</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Interactive Boosting Demo
    st.subheader("Interactive Boosting Demo")
    
    if st.session_state.X_train is not None:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            boosting_algorithm = st.selectbox(
                "Boosting Algorithm",
                ["AdaBoost", "Gradient Boosting"],
                key="boosting_algorithm"
            )
            
            n_estimators = st.slider(
                "Number of Estimators", 
                min_value=10, 
                max_value=200, 
                value=50,
                step=10,
                key="boosting_n_estimators"
            )
            
            learning_rate = st.slider(
                "Learning Rate", 
                min_value=0.01, 
                max_value=1.0, 
                value=0.1,
                step=0.05,
                key="boosting_learning_rate"
            )
            
            if boosting_algorithm == "Gradient Boosting":
                max_depth = st.slider(
                    "Max Depth of Base Estimators", 
                    min_value=1, 
                    max_value=10, 
                    value=3,
                    key="boosting_max_depth"
                )
            
            if st.button("Train Boosting Model", key="train_boosting"):
                with st.spinner("Training..."):
                    if st.session_state.task_type == 'classification':
                        # Base model
                        base_model = DecisionTreeClassifier(max_depth=1)
                        base_model.fit(st.session_state.X_train, st.session_state.y_train)
                        base_preds = base_model.predict(st.session_state.X_test)
                        base_accuracy = accuracy_score(st.session_state.y_test, base_preds)
                        
                        # Boosting model
                        if boosting_algorithm == "AdaBoost":
                            boosting_model = AdaBoostClassifier(
                                n_estimators=n_estimators,
                                learning_rate=learning_rate,
                                random_state=42
                            )
                        else:
                            boosting_model = GradientBoostingClassifier(
                                n_estimators=n_estimators,
                                learning_rate=learning_rate,
                                max_depth=max_depth,
                                random_state=42
                            )
                        
                        boosting_model.fit(st.session_state.X_train, st.session_state.y_train)
                        
                        # Track performance across iterations
                        staged_scores = []
                        if boosting_algorithm == "Gradient Boosting":
                            for i, y_pred in enumerate(boosting_model.staged_predict(st.session_state.X_test)):
                                staged_scores.append(accuracy_score(st.session_state.y_test, y_pred))
                        
                        boosting_preds = boosting_model.predict(st.session_state.X_test)
                        boosting_accuracy = accuracy_score(st.session_state.y_test, boosting_preds)
                        
                        # Store results
                        st.session_state.model_results["boosting"] = {
                            "base_accuracy": base_accuracy,
                            "boosting_accuracy": boosting_accuracy,
                            "conf_matrix": confusion_matrix(st.session_state.y_test, boosting_preds),
                            "classification_report": classification_report(st.session_state.y_test, boosting_preds, output_dict=True),
                            "staged_scores": staged_scores,
                            "feature_importance": boosting_model.feature_importances_
                        }
                        
                    else:  # regression
                        # Base model
                        base_model = DecisionTreeRegressor(max_depth=1)
                        base_model.fit(st.session_state.X_train, st.session_state.y_train)
                        base_preds = base_model.predict(st.session_state.X_test)
                        base_mse = mean_squared_error(st.session_state.y_test, base_preds)
                        base_r2 = r2_score(st.session_state.y_test, base_preds)
                        
                        # Boosting model
                        if boosting_algorithm == "AdaBoost":
                            boosting_model = AdaBoostRegressor(
                                n_estimators=n_estimators,
                                learning_rate=learning_rate,
                                random_state=42
                            )
                        else:
                            boosting_model = GradientBoostingRegressor(
                                n_estimators=n_estimators,
                                learning_rate=learning_rate,
                                max_depth=max_depth,
                                random_state=42
                            )
                        
                        boosting_model.fit(st.session_state.X_train, st.session_state.y_train)
                        
                        # Track performance across iterations
                        staged_scores = []
                        if boosting_algorithm == "Gradient Boosting":
                            for i, y_pred in enumerate(boosting_model.staged_predict(st.session_state.X_test)):
                                staged_scores.append(mean_squared_error(st.session_state.y_test, y_pred))
                        
                        boosting_preds = boosting_model.predict(st.session_state.X_test)
                        boosting_mse = mean_squared_error(st.session_state.y_test, boosting_preds)
                        boosting_r2 = r2_score(st.session_state.y_test, boosting_preds)
                        
                        # Store results
                        st.session_state.model_results["boosting"] = {
                            "base_mse": base_mse,
                            "base_r2": base_r2,
                            "boosting_mse": boosting_mse,
                            "boosting_r2": boosting_r2,
                            "staged_scores": staged_scores,
                            "feature_importance": boosting_model.feature_importances_
                        }
                
                st.success(f"✅ {boosting_algorithm} model trained successfully!")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if "boosting" in st.session_state.model_results:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                
                results = st.session_state.model_results["boosting"]
                
                if st.session_state.task_type == 'classification':
                    # Create a comparison bar chart
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=['Base Model', f'{boosting_algorithm}'],
                        y=[results["base_accuracy"] * 100, results["boosting_accuracy"] * 100],
                        text=[f'{results["base_accuracy"]:.2%}', f'{results["boosting_accuracy"]:.2%}'],
                        textposition='auto',
                        marker_color=[AWS_COLORS["slate"], AWS_COLORS["activation"]]
                    ))
                    fig.update_layout(
                        title='Model Accuracy Comparison',
                        yaxis_title='Accuracy (%)',
                        yaxis=dict(range=[0, 100]),
                        height=350
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Learning curve
                    if len(results["staged_scores"]) > 0:
                        fig = px.line(
                            x=list(range(1, len(results["staged_scores"]) + 1)),
                            y=results["staged_scores"],
                            labels={'x': 'Number of Trees', 'y': 'Accuracy'},
                            title='Learning Curve: Effect of Adding More Trees'
                        )
                        fig.update_traces(line_color=AWS_COLORS["anchor"])
                        st.plotly_chart(fig, use_container_width=True)
                    
                else:  # regression
                    # MSE Comparison
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=['Base Model', f'{boosting_algorithm}'],
                        y=[results["base_mse"], results["boosting_mse"]],
                        text=[f'{results["base_mse"]:.4f}', f'{results["boosting_mse"]:.4f}'],
                        textposition='auto',
                        marker_color=[AWS_COLORS["slate"], AWS_COLORS["activation"]]
                    ))
                    fig.update_layout(
                        title='Mean Squared Error (Lower is Better)',
                        yaxis_title='MSE',
                        height=350
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Learning curve
                    if len(results["staged_scores"]) > 0:
                        fig = px.line(
                            x=list(range(1, len(results["staged_scores"]) + 1)),
                            y=results["staged_scores"],
                            labels={'x': 'Number of Trees', 'y': 'MSE'},
                            title='Learning Curve: Effect of Adding More Trees'
                        )
                        fig.update_traces(line_color=AWS_COLORS["anchor"])
                        st.plotly_chart(fig, use_container_width=True)
                
                # Feature importance
                feature_imp = results["feature_importance"]
                indices = np.argsort(feature_imp)[-10:]  # Top 10 features
                
                fig = px.bar(
                    x=feature_imp[indices],
                    y=[f"Feature {i}" for i in indices],
                    orientation='h',
                    title='Top 10 Feature Importance',
                    labels={'x': 'Importance', 'y': 'Feature'},
                )
                fig.update_traces(marker_color=AWS_COLORS["activation"])
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("Train the model to see the results!")
    else:
        st.warning("Please generate a dataset first using the sidebar options.")

    st.markdown("---")
    
    st.subheader("Boosting Algorithms Compared")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>AdaBoost</h3>
            <p>Adaptive Boosting focuses on misclassified samples by increasing their weights.</p>
            <p><strong>Best for:</strong></p>
            <ul>
                <li>Datasets with moderate dimensions</li>
                <li>Problems where interpretability matters</li>
                <li>Clean datasets with minimal noise</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>Gradient Boosting</h3>
            <p>Uses gradient descent optimization to minimize the loss function.</p>
            <p><strong>Best for:</strong></p>
            <ul>
                <li>Regression problems</li>
                <li>Complex relationships in data</li>
                <li>Datasets where you need very high accuracy</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h3>XGBoost / LightGBM</h3>
            <p>Optimized implementations with advanced regularization and efficiency features.</p>
            <p><strong>Best for:</strong></p>
            <ul>
                <li>Production systems that need high performance</li>
                <li>Large-scale machine learning problems</li>
                <li>Kaggle competitions and real-world applications</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h3>Real-World Applications:</h3>
        <ul>
            <li><strong>Finance:</strong> Credit scoring, fraud detection, stock price prediction</li>
            <li><strong>Retail:</strong> Sales forecasting, customer segmentation, recommendation systems</li>
            <li><strong>Healthcare:</strong> Disease prediction, patient risk stratification</li>
            <li><strong>Marketing:</strong> Click-through rate prediction, customer churn prediction</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Stacking Tab
with tabs[3]:
    st.header("🏗️ Stacking (Stacked Generalization)")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>What is Stacking?</h3>
            <p>Stacking, or Stacked Generalization, is an ensemble technique that combines multiple classification or 
            regression models via a meta-model. The base models are trained on the original dataset, then 
            a meta-model is trained on the outputs of the base models.</p>
            <p>Unlike bagging and boosting, stacking uses different types of models and combines them using another learning algorithm.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3>How Stacking Works:</h3>
            <ol>
                <li>Split the dataset into training and validation sets</li>
                <li>Train multiple base models on the training data</li>
                <li>Make predictions on the validation data with each base model</li>
                <li>Use these predictions as features for a meta-model</li>
                <li>Train the meta-model to optimally combine the base models</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image("https://miro.medium.com/max/1400/1*7WySMBrq9A13Zkq7Q_o3uw.jpeg", caption="Stacking Architecture")
        
        st.markdown("""
        <div class="card">
            <h3>Advantages of Stacking:</h3>
            <ul>
                <li>Leverages strengths of different algorithms</li>
                <li>Often provides better predictions than any single model</li>
                <li>Reduces the risk of selecting the wrong model</li>
                <li>Can capture different aspects of the underlying patterns</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Interactive Stacking Demo
    st.subheader("Interactive Stacking Demo")
    
    if st.session_state.X_train is not None:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            # Model selection
            st.subheader("Select Base Models")
            
            if st.session_state.task_type == 'classification':
                use_rf = st.checkbox("Random Forest", value=True, key="stacking_use_rf")
                use_svm = st.checkbox("Support Vector Machine", value=True, key="stacking_use_svm")
                use_lr = st.checkbox("Logistic Regression", value=True, key="stacking_use_lr")
                use_gb = st.checkbox("Gradient Boosting", value=True, key="stacking_use_gb")
                
                st.subheader("Meta-Model")
                meta_model = st.selectbox(
                    "Choose Meta-Model",
                    ["Logistic Regression", "Random Forest"],
                    key="stacking_meta_model"
                )
            else:
                use_rf = st.checkbox("Random Forest", value=True, key="stacking_use_rf")
                use_svr = st.checkbox("SVR", value=True, key="stacking_use_svr")
                use_lr = st.checkbox("Linear Regression", value=True, key="stacking_use_lr")
                use_gb = st.checkbox("Gradient Boosting", value=True, key="stacking_use_gb")
                
                st.subheader("Meta-Model")
                meta_model = st.selectbox(
                    "Choose Meta-Model",
                    ["Linear Regression", "Random Forest"],
                    key="stacking_meta_model"
                )
            
            cv_folds = st.slider(
                "Cross-Validation Folds", 
                min_value=2, 
                max_value=10, 
                value=5,
                key="stacking_cv_folds"
            )
            
            if st.button("Train Stacking Ensemble", key="train_stacking"):
                with st.spinner("Training stacking ensemble..."):
                    if st.session_state.task_type == 'classification':
                        # Create list of base models
                        estimators = []
                        if use_rf:
                            estimators.append(('rf', RandomForestClassifier(n_estimators=100, random_state=42)))
                        if use_svm:
                            estimators.append(('svm', SVC(probability=True, random_state=42)))
                        if use_lr:
                            estimators.append(('lr', LogisticRegression(max_iter=1000, random_state=42)))
                        if use_gb:
                            estimators.append(('gb', GradientBoostingClassifier(n_estimators=100, random_state=42)))
                        
                        if len(estimators) == 0:
                            st.error("Please select at least one base model!")
                            st.stop()
                        
                        # Create and train individual models for comparison
                        individual_scores = {}
                        for name, model in estimators:
                            model.fit(st.session_state.X_train, st.session_state.y_train)
                            y_pred = model.predict(st.session_state.X_test)
                            score = accuracy_score(st.session_state.y_test, y_pred)
                            individual_scores[name] = score
                        
                        # Create meta-model
                        if meta_model == "Logistic Regression":
                            final_estimator = LogisticRegression(max_iter=1000)
                        else:
                            final_estimator = RandomForestClassifier(n_estimators=100)
                        
                        # Create and train stacking model
                        stacking_model = StackingClassifier(
                            estimators=estimators,
                            final_estimator=final_estimator,
                            cv=cv_folds,
                            stack_method='predict_proba',
                            n_jobs=-1
                        )
                        
                        stacking_model.fit(st.session_state.X_train, st.session_state.y_train)
                        stacking_pred = stacking_model.predict(st.session_state.X_test)
                        stacking_score = accuracy_score(st.session_state.y_test, stacking_pred)
                        
                        # Store results
                        st.session_state.model_results["stacking"] = {
                            "individual_scores": individual_scores,
                            "stacking_score": stacking_score,
                            "conf_matrix": confusion_matrix(st.session_state.y_test, stacking_pred),
                            "classification_report": classification_report(st.session_state.y_test, stacking_pred, output_dict=True)
                        }
                        
                    else:  # regression
                        # Create list of base models
                        estimators = []
                        if use_rf:
                            estimators.append(('rf', RandomForestRegressor(n_estimators=100, random_state=42)))
                        if use_svr:
                            estimators.append(('svr', SVR()))
                        if use_lr:
                            estimators.append(('lr', LinearRegression()))
                        if use_gb:
                            estimators.append(('gb', GradientBoostingRegressor(n_estimators=100, random_state=42)))
                        
                        if len(estimators) == 0:
                            st.error("Please select at least one base model!")
                            st.stop()
                        
                        # Create and train individual models for comparison
                        individual_scores_mse = {}
                        individual_scores_r2 = {}
                        for name, model in estimators:
                            model.fit(st.session_state.X_train, st.session_state.y_train)
                            y_pred = model.predict(st.session_state.X_test)
                            mse = mean_squared_error(st.session_state.y_test, y_pred)
                            r2 = r2_score(st.session_state.y_test, y_pred)
                            individual_scores_mse[name] = mse
                            individual_scores_r2[name] = r2
                        
                        # Create meta-model
                        if meta_model == "Linear Regression":
                            final_estimator = LinearRegression()
                        else:
                            final_estimator = RandomForestRegressor(n_estimators=100)
                        
                        # Create and train stacking model
                        stacking_model = StackingRegressor(
                            estimators=estimators,
                            final_estimator=final_estimator,
                            cv=cv_folds,
                            n_jobs=-1
                        )
                        
                        stacking_model.fit(st.session_state.X_train, st.session_state.y_train)
                        stacking_pred = stacking_model.predict(st.session_state.X_test)
                        stacking_mse = mean_squared_error(st.session_state.y_test, stacking_pred)
                        stacking_r2 = r2_score(st.session_state.y_test, stacking_pred)
                        
                        # Store results
                        st.session_state.model_results["stacking"] = {
                            "individual_scores_mse": individual_scores_mse,
                            "individual_scores_r2": individual_scores_r2,
                            "stacking_mse": stacking_mse,
                            "stacking_r2": stacking_r2
                        }
                
                st.success("✅ Stacking ensemble trained successfully!")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if "stacking" in st.session_state.model_results:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                
                results = st.session_state.model_results["stacking"]
                
                if st.session_state.task_type == 'classification':
                    # Add stacking to individual scores for comparison
                    all_scores = results["individual_scores"].copy()
                    all_scores["stacking"] = results["stacking_score"]
                    
                    # Create bar chart for model comparison
                    models = list(all_scores.keys())
                    scores = list(all_scores.values())
                    
                    # Highlight stacking model with different color
                    colors = [AWS_COLORS["anchor"] if model != "stacking" else AWS_COLORS["activation"] for model in models]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=models,
                        y=[score * 100 for score in scores],
                        marker_color=colors,
                        text=[f'{score:.2%}' for score in scores],
                        textposition='auto'
                    ))
                    fig.update_layout(
                        title='Model Accuracy Comparison',
                        xaxis_title='Model',
                        yaxis_title='Accuracy (%)',
                        yaxis=dict(range=[0, 100]),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display confusion matrix
                    st.subheader("Confusion Matrix (Stacking Model)")
                    cm = results["conf_matrix"]
                    fig = px.imshow(
                        cm, 
                        text_auto=True,
                        color_continuous_scale=px.colors.sequential.Greens,
                        labels=dict(x="Predicted Label", y="True Label"),
                        x=['Class 0', 'Class 1'],
                        y=['Class 0', 'Class 1']
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                else:  # regression
                    # Add stacking to individual scores for comparison
                    all_scores_mse = results["individual_scores_mse"].copy()
                    all_scores_mse["stacking"] = results["stacking_mse"]
                    
                    all_scores_r2 = results["individual_scores_r2"].copy()
                    all_scores_r2["stacking"] = results["stacking_r2"]
                    
                    # Create bar charts for model comparison
                    models = list(all_scores_mse.keys())
                    mse_scores = list(all_scores_mse.values())
                    r2_scores = list(all_scores_r2.values())
                    
                    # Highlight stacking model with different color
                    colors = [AWS_COLORS["anchor"] if model != "stacking" else AWS_COLORS["activation"] for model in models]
                    
                    # MSE comparison
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=models,
                        y=mse_scores,
                        marker_color=colors,
                        text=[f'{score:.4f}' for score in mse_scores],
                        textposition='auto'
                    ))
                    fig.update_layout(
                        title='Mean Squared Error Comparison (Lower is better)',
                        xaxis_title='Model',
                        yaxis_title='MSE',
                        height=350
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # R² comparison
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=models,
                        y=r2_scores,
                        marker_color=colors,
                        text=[f'{score:.4f}' for score in r2_scores],
                        textposition='auto'
                    ))
                    fig.update_layout(
                        title='R² Score Comparison (Higher is better)',
                        xaxis_title='Model',
                        yaxis_title='R²',
                        height=350
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Insights section
                st.markdown("""
                <div class="card">
                    <h3>Key Insights:</h3>
                    <ul>
                        <li>Stacking often outperforms individual models by leveraging their strengths</li>
                        <li>The meta-model learns which base model performs best in different situations</li>
                        <li>Diverse base models typically lead to better stacking performance</li>
                        <li>Cross-validation prevents overfitting in the stacking process</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Train the ensemble to see the results!")
    else:
        st.warning("Please generate a dataset first using the sidebar options.")

    st.markdown("---")
    
    st.subheader("Stacking in Practice")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>When to Use Stacking</h3>
            <ul>
                <li>When you have models with complementary strengths</li>
                <li>For critical applications where accuracy is paramount</li>
                <li>In competitions like Kaggle, where small improvements matter</li>
                <li>When you have sufficient data to train multiple models</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>Real-World Applications</h3>
            <ul>
                <li><strong>Healthcare:</strong> Combining multiple diagnostic models for better disease prediction</li>
                <li><strong>Finance:</strong> Credit default prediction with multiple risk assessments</li>
                <li><strong>Natural Language Processing:</strong> Ensemble of different text classifiers</li>
                <li><strong>Computer Vision:</strong> Combining different object detection approaches</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h3>Tips for Effective Stacking:</h3>
        <ol>
            <li><strong>Use diverse base models</strong> that capture different aspects of the data</li>
            <li><strong>Include both high-bias and high-variance models</strong> in your ensemble</li>
            <li><strong>Use cross-validation</strong> when generating meta-features to avoid overfitting</li>
            <li><strong>Consider feature selection</strong> to reduce dimensionality at the meta-level</li>
            <li><strong>Start simple</strong> with a linear meta-model before trying more complex approaches</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center">
    <p>Ensemble Learning Explorer | Created with ❤️ using Streamlit | 2023</p>
</div>
""", unsafe_allow_html=True)
# ```

# This Streamlit application provides a comprehensive and interactive exploration of ensemble learning techniques with the following features:

# 1. **Modern UI with tab-based navigation** using emojis (🏠 Home, 🌲 Bagging, 🚀 Boosting, 🏗️ Stacking)
# 2. **Session management** in the sidebar allowing users to reset their session
# 3. **Interactive data generation** with options for classification and regression tasks
# 4. **Detailed explanations** of each ensemble method with visuals and real-world applications
# 5. **Interactive examples** where users can:
#    - Select different parameters
#    - Train models
#    - Visualize results with modern charts and comparisons
# 6. **Engaging visuals** using Plotly for interactive charts with the AWS color scheme
# 7. **Helpful insights** about when and how to use each technique

# The application has been optimized for web responsiveness with clean layouts and mobile-friendly design principles. It's structured to provide a seamless learning experience while allowing users to experiment with different ensemble techniques and see their effects on model performance.