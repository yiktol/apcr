
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_curve, roc_curve, auc
from imblearn.over_sampling import SMOTE
import shap
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from PIL import Image
import io
import base64
import requests
from streamlit_lottie import st_lottie
import json

# Set page configuration
st.set_page_config(
    page_title="ML Bias & Explainability",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.smote_applied = False
    st.session_state.model_trained = False
    st.session_state.X = None
    st.session_state.y = None
    st.session_state.X_train = None
    st.session_state.X_test = None
    st.session_state.y_train = None
    st.session_state.y_test = None
    st.session_state.model = None
    st.session_state.shap_values = None
    st.session_state.shap_explainer = None

# Custom CSS for AWS-inspired styling
st.markdown("""
<style>
    .main {
        background-color: #FFFFFF;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #FFFFFF;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF9900 !important;
        color: white !important;
    }
    h1, h2, h3 {
        color: #232F3E;
    }
    .stButton>button {
        background-color: #FF9900;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #EC7211;
    }
    footer {
        visibility: hidden;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #232F3E;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }
    .highlight {
        background-color: #FFEBCC;
        padding: 10px;
        border-radius: 5px;
    }
    .card {
        border-radius: 5px;
        padding: 20px;
        margin: 10px 0px;
        background-color: #F8F8F8;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .aws-orange {
        color: #FF9900;
    }
    .aws-blue {
        color: #232F3E;
    }
</style>
<div class="footer">© 2025, Amazon Web Services, Inc. or its affiliates. All rights reserved.</div>
""", unsafe_allow_html=True)

# Load animation
def load_lottie(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Sidebar for session management
with st.sidebar:
    st.image("https://d0.awsstatic.com/logos/powered-by-aws.png", width=200)
    st.title("Session Management")
    
    if st.button("Reset Session 🔄"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.initialized = True
        st.session_state.smote_applied = False
        st.session_state.model_trained = False
        st.rerun()
    
    st.markdown("---")
    st.subheader("About This App")
    st.markdown("""
    This interactive e-learning application demonstrates two important concepts in responsible ML:
    
    1. **SMOTE**: Addressing class imbalance
    2. **SHAP**: Explaining model predictions
    
    Navigate through the tabs to learn and experiment with these techniques.
    """)

# Main content
st.title("Bias and Explainability in Machine Learning")
st.markdown("""
<div class="highlight">
Explore techniques to address bias and improve explainability in ML models through interactive examples.
</div>
""", unsafe_allow_html=True)

# Create tabs with emojis
tab1, tab2 = st.tabs(["🔄 SMOTE: Handling Imbalanced Data", "🔍 SHAP: Explaining Model Predictions"])

# Tab 1: SMOTE
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("SMOTE: Synthetic Minority Over-sampling Technique")
        st.markdown("""
        <div class="card">
        <h3 class="aws-orange">What is SMOTE?</h3>
        <p>SMOTE helps address class imbalance by creating synthetic samples of the minority class. 
        This technique improves model performance by providing a more balanced dataset for training.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
        <h3 class="aws-orange">Why is it important?</h3>
        <p>Imbalanced datasets can lead to biased models that perform poorly on minority classes. 
        This is particularly problematic in critical applications like fraud detection or medical diagnosis.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        smote_animation = load_lottie("https://assets8.lottiefiles.com/packages/lf20_l5qvxwtf.json")
        if smote_animation:
            st_lottie(smote_animation, height=300, key="smote_animation")
        else:
            st.image("https://miro.medium.com/max/1400/1*Y5TBKXAR71R0YL98TQ5TDQ.png", caption="SMOTE visualization")
    
    st.markdown("---")
    
    st.subheader("Interactive SMOTE Demonstration")
    
    # Dataset selection
    dataset_option = st.selectbox(
        "Select a dataset to explore:",
        ["Credit Card Fraud Detection", "Breast Cancer Detection"]
    )
    
    # Load and prepare data based on selection
    if dataset_option == "Credit Card Fraud Detection":
        if 'X' not in st.session_state or st.session_state.X is None:
            # Generate synthetic credit card fraud data
            X, y = make_classification(
                n_samples=1000, n_features=10, n_informative=5, n_redundant=2,
                n_classes=2, weights=[0.97, 0.03], random_state=42
            )
            feature_names = [f'Feature_{i+1}' for i in range(X.shape[1])]
            df = pd.DataFrame(X, columns=feature_names)
            df['Class'] = y
            df.rename(columns={'Class': 'Fraud'}, inplace=True)
            
            st.session_state.X = X
            st.session_state.y = y
            st.session_state.df = df
            st.session_state.feature_names = feature_names
            st.session_state.class_name = "Fraud"
    else:  # Breast Cancer Detection
        if 'X' not in st.session_state or st.session_state.X is None:
            # Load breast cancer dataset
            data = load_breast_cancer()
            X = data.data
            y = data.target
            feature_names = data.feature_names
            df = pd.DataFrame(X, columns=feature_names)
            df['Class'] = y
            df.rename(columns={'Class': 'Malignant'}, inplace=True)
            
            st.session_state.X = X
            st.session_state.y = y
            st.session_state.df = df
            st.session_state.feature_names = feature_names
            st.session_state.class_name = "Malignant"
    
    # Display dataset information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h4 class='aws-blue'>Dataset Overview</h4>", unsafe_allow_html=True)
        st.dataframe(st.session_state.df.head())
    
    with col2:
        st.markdown("<h4 class='aws-blue'>Class Distribution</h4>", unsafe_allow_html=True)
        class_counts = st.session_state.df[st.session_state.class_name].value_counts()
        fig = px.pie(
            values=class_counts.values, 
            names=class_counts.index.map({0: 'Negative', 1: 'Positive'}),
            title="Class Distribution",
            color_discrete_sequence=["#232F3E", "#FF9900"]
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Split data
    if 'X_train' not in st.session_state or st.session_state.X_train is None:
        X_train, X_test, y_train, y_test = train_test_split(
            st.session_state.X, st.session_state.y, test_size=0.3, random_state=42
        )
        st.session_state.X_train = X_train
        st.session_state.X_test = X_test
        st.session_state.y_train = y_train
        st.session_state.y_test = y_test
    
    # SMOTE application
    st.markdown("---")
    st.markdown("<h3 class='aws-orange'>Apply SMOTE to Balance the Dataset</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        smote_k = st.slider("SMOTE k neighbors", min_value=1, max_value=10, value=5)
        apply_smote = st.button("Apply SMOTE")
    
    with col2:
        if apply_smote or st.session_state.smote_applied:
            st.session_state.smote_applied = True
            
            # Apply SMOTE
            smote = SMOTE(k_neighbors=smote_k, random_state=42)
            X_train_smote, y_train_smote = smote.fit_resample(st.session_state.X_train, st.session_state.y_train)
            
            st.session_state.X_train_smote = X_train_smote
            st.session_state.y_train_smote = y_train_smote
            
            # Display class distribution before and after SMOTE
            fig = make_subplots(rows=1, cols=2, subplot_titles=("Before SMOTE", "After SMOTE"))
            
            # Before SMOTE
            before_counts = pd.Series(st.session_state.y_train).value_counts().sort_index()
            fig.add_trace(
                go.Bar(
                    x=['Negative', 'Positive'], 
                    y=before_counts.values, 
                    marker_color=["#232F3E", "#FF9900"]
                ),
                row=1, col=1
            )
            
            # After SMOTE
            after_counts = pd.Series(st.session_state.y_train_smote).value_counts().sort_index()
            fig.add_trace(
                go.Bar(
                    x=['Negative', 'Positive'], 
                    y=after_counts.values, 
                    marker_color=["#232F3E", "#FF9900"]
                ),
                row=1, col=2
            )
            
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Display feature space visualization (2D projection)
            st.markdown("<h4 class='aws-blue'>Feature Space Visualization</h4>", unsafe_allow_html=True)
            
            # Select two features for visualization
            features_to_plot = st.session_state.feature_names[:2]
            
            # Create dataframes for visualization
            df_original = pd.DataFrame({
                features_to_plot[0]: st.session_state.X_train[:, 0],
                features_to_plot[1]: st.session_state.X_train[:, 1],
                'Class': st.session_state.y_train,
                'Type': 'Original'
            })
            
            df_smote = pd.DataFrame({
                features_to_plot[0]: st.session_state.X_train_smote[:, 0],
                features_to_plot[1]: st.session_state.X_train_smote[:, 1],
                'Class': st.session_state.y_train_smote,
                'Type': 'SMOTE'
            })
            
            # Identify synthetic points (those in SMOTE but not in original)
            original_points = set(map(tuple, df_original[[features_to_plot[0], features_to_plot[1], 'Class']].values))
            
            df_smote_synthetic = pd.DataFrame([
                {features_to_plot[0]: row[0], features_to_plot[1]: row[1], 'Class': row[2], 'Type': 'Synthetic'}
                for row in df_smote[[features_to_plot[0], features_to_plot[1], 'Class']].values
                if (row[0], row[1], row[2]) not in original_points and row[2] == 1  # Only minority class
            ])
            
            df_viz = pd.concat([df_original, df_smote_synthetic])
            
            # Create scatter plot
            fig = px.scatter(
                df_viz, 
                x=features_to_plot[0], 
                y=features_to_plot[1],
                color='Class',
                symbol='Type',
                color_discrete_map={0: "#232F3E", 1: "#FF9900"},
                title="2D Feature Space: Original vs Synthetic Samples",
                labels={'Class': 'Class (1=Positive)'}
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Model training and evaluation
    st.markdown("---")
    st.markdown("<h3 class='aws-orange'>Model Performance Comparison</h3>", unsafe_allow_html=True)
    
    if st.session_state.smote_applied:
        train_model = st.button("Train and Compare Models")
        
        if train_model or st.session_state.model_trained:
            st.session_state.model_trained = True
            
            # Create progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Train model on original data
            status_text.text("Training model on original data...")
            progress_bar.progress(25)
            
            model_original = RandomForestClassifier(random_state=42)
            model_original.fit(st.session_state.X_train, st.session_state.y_train)
            y_pred_original = model_original.predict(st.session_state.X_test)
            
            # Train model on SMOTE data
            status_text.text("Training model on SMOTE-balanced data...")
            progress_bar.progress(50)
            
            model_smote = RandomForestClassifier(random_state=42)
            model_smote.fit(st.session_state.X_train_smote, st.session_state.y_train_smote)
            y_pred_smote = model_smote.predict(st.session_state.X_test)
            
            # Calculate metrics
            status_text.text("Calculating performance metrics...")
            progress_bar.progress(75)
            
            # Accuracy
            acc_original = accuracy_score(st.session_state.y_test, y_pred_original)
            acc_smote = accuracy_score(st.session_state.y_test, y_pred_smote)
            
            # Confusion matrices
            cm_original = confusion_matrix(st.session_state.y_test, y_pred_original)
            cm_smote = confusion_matrix(st.session_state.y_test, y_pred_smote)
            
            # Classification reports
            report_original = classification_report(st.session_state.y_test, y_pred_original, output_dict=True)
            report_smote = classification_report(st.session_state.y_test, y_pred_smote, output_dict=True)
            
            # ROC curve data
            fpr_original, tpr_original, _ = roc_curve(st.session_state.y_test, model_original.predict_proba(st.session_state.X_test)[:, 1])
            roc_auc_original = auc(fpr_original, tpr_original)
            
            fpr_smote, tpr_smote, _ = roc_curve(st.session_state.y_test, model_smote.predict_proba(st.session_state.X_test)[:, 1])
            roc_auc_smote = auc(fpr_smote, tpr_smote)
            
            # Store models
            st.session_state.model_original = model_original
            st.session_state.model_smote = model_smote
            
            progress_bar.progress(100)
            status_text.text("Model training and evaluation complete!")
            time.sleep(0.5)
            status_text.empty()
            progress_bar.empty()
            
            # Display results
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<h4 class='aws-blue'>Original Model Performance</h4>", unsafe_allow_html=True)
                
                # Confusion matrix
                fig = px.imshow(
                    cm_original, 
                    text_auto=True,
                    labels=dict(x="Predicted", y="Actual"),
                    x=['Negative', 'Positive'],
                    y=['Negative', 'Positive'],
                    color_continuous_scale=['#FFFFFF', '#232F3E']
                )
                fig.update_layout(title="Confusion Matrix")
                st.plotly_chart(fig, use_container_width=True)
                
                # Metrics
                st.metric("Accuracy", f"{acc_original:.4f}")
                st.metric("Precision (Positive Class)", f"{report_original['1']['precision']:.4f}")
                st.metric("Recall (Positive Class)", f"{report_original['1']['recall']:.4f}")
                st.metric("F1 Score (Positive Class)", f"{report_original['1']['f1-score']:.4f}")
            
            with col2:
                st.markdown("<h4 class='aws-blue'>SMOTE Model Performance</h4>", unsafe_allow_html=True)
                
                # Confusion matrix
                fig = px.imshow(
                    cm_smote, 
                    text_auto=True,
                    labels=dict(x="Predicted", y="Actual"),
                    x=['Negative', 'Positive'],
                    y=['Negative', 'Positive'],
                    color_continuous_scale=['#FFFFFF', '#FF9900']
                )
                fig.update_layout(title="Confusion Matrix")
                st.plotly_chart(fig, use_container_width=True)
                
                # Metrics
                st.metric("Accuracy", f"{acc_smote:.4f}")
                st.metric("Precision (Positive Class)", f"{report_smote['1']['precision']:.4f}")
                st.metric("Recall (Positive Class)", f"{report_smote['1']['recall']:.4f}")
                st.metric("F1 Score (Positive Class)", f"{report_smote['1']['f1-score']:.4f}")
            
            # ROC Curve comparison
            st.markdown("<h4 class='aws-blue'>ROC Curve Comparison</h4>", unsafe_allow_html=True)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=fpr_original, y=tpr_original,
                name=f'Original (AUC = {roc_auc_original:.4f})',
                line=dict(color='#232F3E', width=2)
            ))
            fig.add_trace(go.Scatter(
                x=fpr_smote, y=tpr_smote,
                name=f'SMOTE (AUC = {roc_auc_smote:.4f})',
                line=dict(color='#FF9900', width=2)
            ))
            fig.add_trace(go.Scatter(
                x=[0, 1], y=[0, 1],
                name='Random',
                line=dict(color='gray', width=1, dash='dash')
            ))
            fig.update_layout(
                title='ROC Curve Comparison',
                xaxis=dict(title='False Positive Rate'),
                yaxis=dict(title='True Positive Rate'),
                legend=dict(x=0.7, y=0.1)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Key insights
            st.markdown("""
            <div class="card">
            <h3 class="aws-orange">Key Insights</h3>
            <ul>
                <li><strong>Recall Improvement:</strong> SMOTE typically improves recall for the minority class, as the model becomes more sensitive to this class.</li>
                <li><strong>Precision Trade-off:</strong> There might be a slight decrease in precision as the model may generate more false positives.</li>
                <li><strong>Overall Performance:</strong> The F1-score often improves, indicating a better balance between precision and recall.</li>
                <li><strong>Business Impact:</strong> In cases like fraud detection or disease diagnosis, improved recall can be critical even at the cost of some precision.</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

# Tab 2: SHAP
with tab2:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("SHAP: SHapley Additive exPlanations")
        st.markdown("""
        <div class="card">
        <h3 class="aws-orange">What is SHAP?</h3>
        <p>SHAP values help explain individual predictions made by machine learning models. 
        They quantify the contribution of each feature to a prediction, based on cooperative game theory.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
        <h3 class="aws-orange">Why is it important?</h3>
        <p>Model explainability is crucial for:
        <ul>
            <li>Building trust in AI systems</li>
            <li>Identifying potential biases</li>
            <li>Meeting regulatory requirements</li>
            <li>Debugging and improving models</li>
        </ul>
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        shap_animation = load_lottie("https://assets4.lottiefiles.com/packages/lf20_ysrn2iwp.json")
        if shap_animation:
            st_lottie(shap_animation, height=300, key="shap_animation")
        else:
            st.image("https://raw.githubusercontent.com/shap/shap/master/docs/artwork/shap_header.png", caption="SHAP explanation")
    
    st.markdown("---")
    
    st.subheader("Interactive SHAP Demonstration")
    
    # Dataset selection for SHAP
    dataset_option = st.selectbox(
        "Select a dataset to explore:",
        ["Credit Card Fraud Detection", "Breast Cancer Detection"],
        key="shap_dataset"
    )
    
    # Load and prepare data based on selection
    if dataset_option == "Credit Card Fraud Detection":
        if 'X' not in st.session_state or st.session_state.X is None:
            # Generate synthetic credit card fraud data
            X, y = make_classification(
                n_samples=1000, n_features=10, n_informative=5, n_redundant=2,
                n_classes=2, weights=[0.97, 0.03], random_state=42
            )
            feature_names = [f'Feature_{i+1}' for i in range(X.shape[1])]
            df = pd.DataFrame(X, columns=feature_names)
            df['Class'] = y
            df.rename(columns={'Class': 'Fraud'}, inplace=True)
            
            st.session_state.X = X
            st.session_state.y = y
            st.session_state.df = df
            st.session_state.feature_names = feature_names
            st.session_state.class_name = "Fraud"
    else:  # Breast Cancer Detection
        if 'X' not in st.session_state or st.session_state.X is None:
            # Load breast cancer dataset
            data = load_breast_cancer()
            X = data.data
            y = data.target
            feature_names = data.feature_names
            df = pd.DataFrame(X, columns=feature_names)
            df['Class'] = y
            df.rename(columns={'Class': 'Malignant'}, inplace=True)
            
            st.session_state.X = X
            st.session_state.y = y
            st.session_state.df = df
            st.session_state.feature_names = feature_names
            st.session_state.class_name = "Malignant"
    
    # Split data if not already done
    if 'X_train' not in st.session_state or st.session_state.X_train is None:
        X_train, X_test, y_train, y_test = train_test_split(
            st.session_state.X, st.session_state.y, test_size=0.3, random_state=42
        )
        st.session_state.X_train = X_train
        st.session_state.X_test = X_test
        st.session_state.y_train = y_train
        st.session_state.y_test = y_test
    
    # Train model for SHAP if not already done
    if 'shap_model' not in st.session_state:
        with st.spinner("Training model for SHAP analysis..."):
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(st.session_state.X_train, st.session_state.y_train)
            st.session_state.shap_model = model
    
    # Calculate SHAP values if not already done
    if 'shap_explainer' not in st.session_state:
        with st.spinner("Calculating SHAP values..."):
            # Create a small subset for demonstration
            X_sample = st.session_state.X_test[:100]
            
            # Create explainer - using the updated SHAP API
            explainer = shap.Explainer(st.session_state.shap_model, st.session_state.X_train)
            shap_values = explainer(X_sample)
            
            # Store in session state
            st.session_state.shap_explainer = explainer
            st.session_state.shap_values = shap_values
            st.session_state.X_sample = X_sample
    
    # SHAP visualizations
    st.markdown("---")
    st.markdown("<h3 class='aws-orange'>SHAP Visualizations</h3>", unsafe_allow_html=True)
    
    # Select visualization type
    viz_type = st.radio(
        "Select visualization type:",
        ["Summary Plot", "Feature Importance", "Single Prediction Explanation"],
        horizontal=True
    )
    
    if viz_type == "Summary Plot":
        if 'model' not in locals():  # Check if model exists
            st.error("Please train or load a model first")
        else:
            st.markdown("""
            <div class="highlight">
            <strong>Summary Plot</strong> shows the distribution of SHAP values for each feature. 
            Features are ordered by their global importance, and colors indicate the feature value (red = high, blue = low).
            </div>
            """, unsafe_allow_html=True)

            # First, calculate SHAP values and create an Explanation object
            explainer = shap.Explainer(model, feature_names=feature_names)
            shap_explanation = explainer(X)  # X is your feature dataset

            # For multi-class/multi-output models, select a specific output class
            # Usually class 1 for binary classification
            if len(shap_explanation.shape) > 2:
                shap_values_plot = shap_explanation[:, :, 1]  # Select class 1
            else:
                shap_values_plot = shap_explanation

            # Create summary plot using the updated SHAP API
            fig, ax = plt.subplots(figsize=(10, 8))
            shap.plots.beeswarm(
                # st.session_state.shap_values,
                shap_explanation,
                show=False,
                max_display=10
            )
            st.pyplot(fig)
        
        st.markdown("""
        <div class="card">
        <h4 class="aws-orange">Interpretation</h4>
        <p>
        <ul>
            <li>Features at the top have the highest impact on predictions</li>
            <li>Red points represent high feature values, blue points represent low values</li>
            <li>Points to the right indicate a positive impact on the prediction (increasing the probability)</li>
            <li>Points to the left indicate a negative impact (decreasing the probability)</li>
        </ul>
        </p>
        </div>
        """, unsafe_allow_html=True)
        
    elif viz_type == "Feature Importance":
        st.markdown("""
        <div class="highlight">
        <strong>Feature Importance Plot</strong> shows the average absolute SHAP value for each feature, 
        providing a global view of feature importance across all predictions.
        </div>
        """, unsafe_allow_html=True)
        
        # Create feature importance plot using the updated SHAP API
        fig, ax = plt.subplots(figsize=(10, 8))
        shap.plots.bar(
            shap.Explanation(
                values=np.abs(st.session_state.shap_values.values).mean(0),
                feature_names=st.session_state.feature_names
            ),
            show=False
        )
        st.pyplot(fig)
        
        st.markdown("""
        <div class="card">
        <h4 class="aws-orange">Interpretation</h4>
        <p>
        <ul>
            <li>Bars represent the average magnitude of SHAP values for each feature</li>
            <li>Longer bars indicate features with higher overall impact on model predictions</li>
            <li>This helps identify which features are most influential for the model's decisions</li>
        </ul>
        </p>
        </div>
        """, unsafe_allow_html=True)
        
    else:  # Single Prediction Explanation
        st.markdown("""
        <div class="highlight">
        <strong>Single Prediction Explanation</strong> shows how each feature contributes to a specific prediction,
        helping understand why the model made a particular decision for an individual case.
        </div>
        """, unsafe_allow_html=True)
        
        # Let user select a sample to explain
        sample_index = st.slider(
            "Select a sample to explain:",
            min_value=0,
            max_value=len(st.session_state.X_sample)-1,
            value=0
        )
        
        # Get the prediction
        sample = st.session_state.X_sample[sample_index:sample_index+1]
        prediction = st.session_state.shap_model.predict_proba(sample)[0, 1]
        actual = st.session_state.y_test[sample_index]
        
        # Display prediction info
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Predicted Probability", f"{prediction:.4f}")
        with col2:
            st.metric("Actual Class", "Positive" if actual == 1 else "Negative")
        
        # Create waterfall plot using the updated SHAP API
        fig, ax = plt.subplots(figsize=(10, 8))
        shap.plots.waterfall(
            st.session_state.shap_values[sample_index],
            show=False,
            max_display=10
        )
        st.pyplot(fig)
        
        # Create force plot using the updated SHAP API
        fig, ax = plt.subplots(figsize=(10, 3))
        shap.plots.force(
            st.session_state.shap_values[sample_index],
            matplotlib=True,
            show=False
        )
        st.pyplot(fig)
        
        st.markdown("""
        <div class="card">
        <h4 class="aws-orange">Interpretation</h4>
        <p>
        <ul>
            <li>Red features push the prediction higher (toward positive class)</li>
            <li>Blue features push the prediction lower (toward negative class)</li>
            <li>The base value represents the average model output over the training dataset</li>
            <li>The final prediction is the sum of the base value and all SHAP values</li>
        </ul>
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    # SHAP practical applications
    st.markdown("---")
    st.markdown("<h3 class='aws-orange'>Practical Applications of SHAP</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
        <h4>Identifying Bias</h4>
        <p>SHAP values can reveal if sensitive attributes like gender or race are significantly influencing predictions,
        helping detect and address algorithmic bias.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
        <h4>Model Debugging</h4>
        <p>By understanding which features drive predictions, data scientists can identify potential issues in the model
        and refine feature engineering or model architecture.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
        <h4>Regulatory Compliance</h4>
        <p>In regulated industries like finance and healthcare, SHAP helps meet explainability requirements
        by providing transparent justifications for automated decisions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
        <h4>User Trust</h4>
        <p>Explaining predictions to end users builds trust in AI systems and helps people understand
        why certain recommendations or decisions were made.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Best practices
    st.markdown("---")
    st.markdown("<h3 class='aws-orange'>Best Practices for Model Explainability</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
    <ol>
        <li><strong>Combine global and local explanations</strong> - Understand both overall model behavior and individual predictions</li>
        <li><strong>Use multiple explanation techniques</strong> - SHAP, LIME, partial dependence plots, etc. provide complementary insights</li>
        <li><strong>Consider explanation fidelity</strong> - Ensure explanations accurately represent model behavior</li>
        <li><strong>Design for the audience</strong> - Technical explanations for data scientists, simplified visualizations for business users</li>
        <li><strong>Document limitations</strong> - Be transparent about what explanations can and cannot tell you</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

