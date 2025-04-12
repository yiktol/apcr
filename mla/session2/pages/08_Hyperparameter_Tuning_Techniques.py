
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification, load_diabetes
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.svm import SVC
import plotly.express as px
import plotly.graph_objects as go
from hyperopt import hp, fmin, tpe, STATUS_OK, Trials
from skopt import BayesSearchCV
from skopt.space import Real, Integer, Categorical
import time
import base64
from io import BytesIO
from PIL import Image
import requests
from streamlit_option_menu import option_menu
import warnings

warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Hyperparameter Tuning Explorer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# AWS-inspired color scheme
AWS_COLORS = {
    "primary": "#232F3E",        # AWS Dark Blue
    "secondary": "#FF9900",      # AWS Orange
    "accent1": "#0073BB",        # AWS Light Blue
    "accent2": "#D13212",        # AWS Red
    "light": "#FFFFFF",          # White
    "dark": "#161E2D",           # Dark Navy
    "background": "#F2F3F3",     # Light Gray Background
    "success": "#008296"         # Teal
}

# Apply AWS-inspired styling
def local_css():
    st.markdown("""
<style>
    /* Main styling */
    .main {
        background-color: #FFFFFF;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #FFFFFF;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #D5DBDB;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FF9900;
        color: #232F3E;
    }
    
    /* Card styling */
    .card {
        border-radius: 5px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: #F7F7F7;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #232F3E;
        color: white;
        text-align: center;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #FF9900;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
    }
    
    .stButton>button:hover {
        background-color: #E76D0C;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #232F3E;
    }
    
    h1 {
        font-weight: bold;
        border-bottom: 2px solid #FF9900;
        padding-bottom: 10px;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: #FF9900;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #232F3E;
        color: white;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #F0F8FF;
        border-left: 5px solid #1A73E8;
        padding: 10px;
        margin-bottom: 15px;
    }
    
    /* Algorithm description */
    .algorithm-description {
        background-color: #F5F5F5;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 20px;
        border-left: 5px solid #FF9900;
    }
    
    /* Code blocks */
    code {
        background-color: #F0F0F0;
        padding: 2px 5px;
        border-radius: 3px;
        font-family: monospace;
    }
    
    pre {
        background-color: #232F3E;
        color: #FFFFFF;
        padding: 15px;
        border-radius: 5px;
        overflow-x: auto;
    }
</style>
    """, unsafe_allow_html=True)

local_css()

# Initialize session state variables
def init_session_state():
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        # Data
        st.session_state.X_train = None
        st.session_state.X_test = None
        st.session_state.y_train = None
        st.session_state.y_test = None
        # Models
        st.session_state.best_grid_model = None
        st.session_state.best_random_model = None
        st.session_state.best_bayesian_model = None
        st.session_state.best_hyperband_model = None
        # Results
        st.session_state.grid_results = None
        st.session_state.random_results = None
        st.session_state.bayesian_results = None
        st.session_state.hyperband_results = None
        # Timing
        st.session_state.grid_time = 0
        st.session_state.random_time = 0
        st.session_state.bayesian_time = 0
        st.session_state.hyperband_time = 0
        # Task type
        st.session_state.task_type = "classification"

init_session_state()

# Sidebar
with st.sidebar:
    st.image("https://raw.githubusercontent.com/aws-samples/aws-machine-learning-university-accelerated-tab/main/images/aws-logo-color-pic.jpg", width=100)
    st.title("Hyperparameter Tuning")
    
    st.markdown("### Session Management")
    if st.button("🔄 Reset Session"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_session_state()
        st.success("Session reset successful!")
    
    st.markdown("### Task Selection")
    task_type = st.radio(
        "Choose a task type:",
        ["Classification", "Regression"],
        index=0 if st.session_state.task_type == "classification" else 1
    )
    st.session_state.task_type = task_type.lower()
    
    st.markdown("### About")
    st.info("""
    This interactive application demonstrates various hyperparameter tuning techniques 
    for machine learning models. Explore, learn, and compare different methods.
    """)

# Main content
st.title("✨ Hyperparameter Tuning Explorer")
st.markdown("""
<div class="card">
This interactive e-learning application helps you understand and compare different hyperparameter tuning techniques 
for machine learning models. Experiment with various methods and visualize their performance and efficiency.
</div>
""", unsafe_allow_html=True)

# Navigation Tabs
selected = option_menu(
    menu_title=None,
    options=["📚 Overview", "🔍 Grid Search", "🎲 Random Search", "🧠 Bayesian Optimization", "⚡ Hyperband"],
    # icons=["book", "grid", "shuffle", "graph-up", "lightning"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": f"{AWS_COLORS['light']}"},
        "icon": {"color": f"{AWS_COLORS['primary']}", "font-size": "18px"},
        "nav-link": {
            "font-size": "16px", 
            "text-align": "center", 
            "margin": "0px", 
            "--hover-color": f"{AWS_COLORS['background']}"
        },
        "nav-link-selected": {"background-color": f"{AWS_COLORS['secondary']}", "color": f"{AWS_COLORS['light']}"},
    }
)

# Helper functions
def load_dataset():
    if st.session_state.task_type == "classification":
        X, y = make_classification(
            n_samples=1000, n_features=20, n_informative=10, n_classes=2, random_state=42
        )
    else:
        diabetes = load_diabetes()
        X, y = diabetes.data, diabetes.target
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    st.session_state.X_train = X_train
    st.session_state.X_test = X_test
    st.session_state.y_train = y_train
    st.session_state.y_test = y_test
    
    return X_train, X_test, y_train, y_test

def get_model_and_params():
    if st.session_state.task_type == "classification":
        model = RandomForestClassifier(random_state=42)
        param_grid = {
            'n_estimators': [10, 50, 100],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        scoring = 'accuracy'
    else:
        model = RandomForestRegressor(random_state=42)
        param_grid = {
            'n_estimators': [10, 50, 100],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        scoring = 'neg_mean_squared_error'
    
    return model, param_grid, scoring

def evaluate_model(model, X_test, y_test):
    if st.session_state.task_type == "classification":
        y_pred = model.predict(X_test)
        score = accuracy_score(y_test, y_pred)
        metric_name = "Accuracy"
    else:
        y_pred = model.predict(X_test)
        score = -mean_squared_error(y_test, y_pred)
        metric_name = "Neg. MSE"
    
    return score, metric_name

def create_comparison_chart():
    methods = ["Grid Search", "Random Search", "Bayesian Optimization", "Hyperband"]
    
    # Collect available results
    scores = []
    times = []
    for method, time_key in zip(
        methods, 
        ["grid_time", "random_time", "bayesian_time", "hyperband_time"]
    ):
        if method == "Grid Search" and st.session_state.best_grid_model is not None:
            score, _ = evaluate_model(st.session_state.best_grid_model, st.session_state.X_test, st.session_state.y_test)
            scores.append(score)
            times.append(st.session_state[time_key])
        elif method == "Random Search" and st.session_state.best_random_model is not None:
            score, _ = evaluate_model(st.session_state.best_random_model, st.session_state.X_test, st.session_state.y_test)
            scores.append(score)
            times.append(st.session_state[time_key])
        elif method == "Bayesian Optimization" and st.session_state.best_bayesian_model is not None:
            score, _ = evaluate_model(st.session_state.best_bayesian_model, st.session_state.X_test, st.session_state.y_test)
            scores.append(score)
            times.append(st.session_state[time_key])
        elif method == "Hyperband" and st.session_state.best_hyperband_model is not None:
            score, _ = evaluate_model(st.session_state.best_hyperband_model, st.session_state.X_test, st.session_state.y_test)
            scores.append(score)
            times.append(st.session_state[time_key])
        else:
            # Skip methods that haven't been run
            pass
    
    # Create comparison chart if we have data
    if scores:
        methods = methods[:len(scores)]  # Only include methods with results
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=methods,
            y=scores,
            name='Performance Score',
            marker_color=AWS_COLORS["accent1"],
            text=[f"{s:.4f}" for s in scores],
            textposition='auto',
        ))
        
        # Add a secondary y-axis for time
        fig.add_trace(go.Scatter(
            x=methods,
            y=times,
            name='Time (s)',
            marker_color=AWS_COLORS["secondary"],
            mode='lines+markers',
            yaxis='y2'
        ))
        
        # Update layout with titles and secondary y-axis
        fig.update_layout(
            title="Comparison of Hyperparameter Tuning Methods",
            xaxis_title="Method",
            yaxis_title="Performance Score",
            yaxis2=dict(
                title="Time (seconds)",
                overlaying="y",
                side="right",
                showgrid=False,
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            template="plotly_white",
            height=500,
        )
        
        return fig
    
    return None

# Overview Tab
if selected == "📚 Overview":
    st.header("Understanding Hyperparameter Tuning")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
        <h3>What is Hyperparameter Tuning?</h3>
        <p>Hyperparameter tuning is the process of finding the optimal set of hyperparameters for a machine learning algorithm. 
        Hyperparameters are configuration variables that govern the training process and the topology of an ML model.</p>
        
        <p>Unlike model parameters which are learned during training, hyperparameters must be set before training begins.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.image("https://miro.medium.com/max/1400/1*mzNlxRJXRs8W2HjU-FSoEA.png", 
                 caption="Hyperparameter Tuning Process", 
                 use_container_width=True)
    
    st.markdown("""
    <div class="card">
    <h3>Tuning Techniques Comparison</h3>
    </div>
    """, unsafe_allow_html=True)
    
    comparison_data = {
        "Technique": ["Grid Search", "Random Search", "Bayesian Optimization", "Hyperband"],
        "Methodology": [
            "Exhaustively tries all combinations of predefined hyperparameter values", 
            "Randomly samples from the hyperparameter space",
            "Uses previous results to choose the next hyperparameters to evaluate",
            "Allocates resources adaptively, quickly eliminating poor performers"
        ],
        "Pros": [
            "Guaranteed to find the best combination within the defined grid",
            "More efficient than grid search for high-dimensional spaces",
            "Efficient exploration of the hyperparameter space",
            "Very efficient for deep learning models with long training times"
        ],
        "Cons": [
            "Computationally expensive, suffers from the curse of dimensionality",
            "May miss optimal combinations by chance",
            "More complex to implement, may get stuck in local optima",
            "May eliminate promising configurations too early"
        ]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.table(comparison_df)
    
    # If we have results, show comparison chart
    if (st.session_state.best_grid_model is not None or 
            st.session_state.best_random_model is not None or 
            st.session_state.best_bayesian_model is not None or 
            st.session_state.best_hyperband_model is not None):
        
        st.markdown("""
        <div class="card">
        <h3>Performance Comparison</h3>
        <p>Compare the different hyperparameter tuning methods you've tried so far:</p>
        </div>
        """, unsafe_allow_html=True)
        
        comparison_chart = create_comparison_chart()
        if comparison_chart:
            st.plotly_chart(comparison_chart, use_container_width=True)
        else:
            st.info("Run at least one tuning method to see comparison charts")
    
    st.markdown("""
    <div class="card">
    <h3>Getting Started</h3>
    <p>Select a tab above to explore each hyperparameter tuning technique. Each section includes:</p>
    <ul>
        <li>An explanation of the technique</li>
        <li>Interactive demo with visualizations</li>
        <li>Performance metrics and insights</li>
    </ul>
    <p>You can switch between classification and regression tasks using the sidebar.</p>
    </div>
    """, unsafe_allow_html=True)

# Grid Search Tab
elif selected == "🔍 Grid Search":
    st.header("Grid Search")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
        <h3>How Grid Search Works</h3>
        <p>Grid Search is an exhaustive search method that tries all possible combinations of the hyperparameter values specified.</p>
        <p>It works by:</p>
        <ol>
            <li>Defining a grid of hyperparameter values</li>
            <li>For each combination, training a model and evaluating its performance</li>
            <li>Selecting the combination that yields the best performance</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image("https://scikit-learn.org/stable/_images/grid_search_workflow.png", 
                 caption="Grid Search Workflow", 
                 use_container_width=True)
    
    st.markdown("""
    <div class="card">
    <h3>Advantages & Disadvantages</h3>
    <p><strong>Advantages:</strong></p>
    <ul>
        <li>Simple to implement</li>
        <li>Guaranteed to find the best combination within the defined grid</li>
        <li>Easily parallelizable</li>
    </ul>
    <p><strong>Disadvantages:</strong></p>
    <ul>
        <li>Computationally expensive</li>
        <li>Suffers from the curse of dimensionality (becomes inefficient with many hyperparameters)</li>
        <li>Requires discretization of continuous parameters</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Grid Search Demo")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        n_estimators_grid = st.multiselect(
            "Choose n_estimators values:",
            options=[10, 20, 50, 100, 200],
            default=[10, 50, 100],
            key="grid_n_estimators"
        )
        
        max_depth_grid = st.multiselect(
            "Choose max_depth values:",
            options=[None, 5, 10, 20, 30],
            default=[None, 10, 20],
            key="grid_max_depth"
        )
    
    with col2:
        min_samples_split_grid = st.multiselect(
            "Choose min_samples_split values:",
            options=[2, 5, 10, 15],
            default=[2, 5, 10],
            key="grid_min_samples_split"
        )
        
        min_samples_leaf_grid = st.multiselect(
            "Choose min_samples_leaf values:",
            options=[1, 2, 4, 6],
            default=[1, 2, 4],
            key="grid_min_samples_leaf"
        )
    
    # Compute total combinations
    total_combinations = (
        len(n_estimators_grid) * 
        len(max_depth_grid) * 
        len(min_samples_split_grid) * 
        len(min_samples_leaf_grid)
    )
    
    st.info(f"Total parameter combinations to evaluate: **{total_combinations}**")
    
    if st.button("Run Grid Search", key="run_grid_search"):
        # Load dataset if not already loaded
        if st.session_state.X_train is None:
            X_train, X_test, y_train, y_test = load_dataset()
        else:
            X_train = st.session_state.X_train
            X_test = st.session_state.X_test
            y_train = st.session_state.y_train
            y_test = st.session_state.y_test
        
        # Get base model
        model, _, scoring = get_model_and_params()
        
        # Create custom parameter grid
        param_grid = {
            'n_estimators': n_estimators_grid,
            'max_depth': max_depth_grid,
            'min_samples_split': min_samples_split_grid,
            'min_samples_leaf': min_samples_leaf_grid
        }
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Run grid search
        status_text.text("Running Grid Search...")
        start_time = time.time()
        
        grid_search = GridSearchCV(
            estimator=model,
            param_grid=param_grid,
            cv=3,
            n_jobs=-1,
            verbose=0,
            scoring=scoring,
            return_train_score=True
        )
        
        grid_search.fit(X_train, y_train)
        
        end_time = time.time()
        execution_time = end_time - start_time
        st.session_state.grid_time = execution_time
        
        progress_bar.progress(100)
        status_text.success(f"Grid Search completed in {execution_time:.2f} seconds")
        
        # Store results
        st.session_state.best_grid_model = grid_search.best_estimator_
        st.session_state.grid_results = pd.DataFrame(grid_search.cv_results_)
        
        # Show best hyperparameters
        st.markdown("### Best Hyperparameters")
        st.json(grid_search.best_params_)
        
        # Evaluate on test set
        test_score, metric_name = evaluate_model(grid_search.best_estimator_, X_test, y_test)
        st.markdown(f"### Test Set {metric_name}: {test_score:.4f}")
        
        # Visualization of results
        st.markdown("### Grid Search Results Visualization")
        
        tab1, tab2 = st.tabs(["Parameter Importance", "Score Distribution"])
        
        with tab1:
            # Parameter importance - sort parameters by their impact on score
            results_df = st.session_state.grid_results
            
            # Create parameter importance visualization
            param_importance = {}
            
            # For each parameter, calculate score variance when it changes
            for param in param_grid.keys():
                pivot_param = f'param_{param}'
                param_values = results_df[pivot_param].unique()
                
                if len(param_values) > 1:  # Only if we have multiple values to compare
                    mean_scores = []
                    for val in param_values:
                        mean_score = results_df[results_df[pivot_param] == val]['mean_test_score'].mean()
                        mean_scores.append(mean_score)
                    
                    # Variance of scores indicates importance
                    param_importance[param] = np.var(mean_scores)
            
            # Create bar chart of parameter importance
            if param_importance:
                importance_df = pd.DataFrame({
                    'Parameter': list(param_importance.keys()),
                    'Importance': list(param_importance.values())
                }).sort_values('Importance', ascending=False)
                
                fig = px.bar(
                    importance_df, 
                    x='Parameter', 
                    y='Importance',
                    title='Parameter Importance (Score Variance)',
                    color='Importance',
                    color_continuous_scale='Viridis'
                )
                
                fig.update_layout(
                    xaxis_title="Hyperparameter",
                    yaxis_title="Importance (Score Variance)",
                    template="plotly_white"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Not enough parameter values to calculate importance")
        
        with tab2:
            # Score distribution
            results_df = st.session_state.grid_results.sort_values('rank_test_score')
            
            # Create histogram of all scores
            fig = px.histogram(
                results_df, 
                x='mean_test_score',
                nbins=20,
                title='Distribution of Cross-Validation Scores',
                color_discrete_sequence=[AWS_COLORS["accent1"]]
            )
            
            fig.add_vline(
                x=results_df['mean_test_score'].max(),
                line_dash="dash", 
                line_color=AWS_COLORS["secondary"],
                annotation_text="Best score"
            )
            
            fig.update_layout(
                xaxis_title="Mean Test Score",
                yaxis_title="Count",
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Top 10 parameter combinations
            st.markdown("### Top 10 Parameter Combinations")
            top_results = results_df[['params', 'mean_test_score', 'std_test_score', 'rank_test_score']].head(10)
            st.dataframe(top_results)
    
    elif st.session_state.best_grid_model is not None:
        # If we already have results, display them
        st.success(f"Grid Search completed in {st.session_state.grid_time:.2f} seconds")
        
        # Show best hyperparameters
        st.markdown("### Best Hyperparameters")
        best_params = st.session_state.best_grid_model.get_params()
        
        # Filter to only show the tuned parameters
        tuned_params = {
            'n_estimators': best_params['n_estimators'],
            'max_depth': best_params['max_depth'],
            'min_samples_split': best_params['min_samples_split'],
            'min_samples_leaf': best_params['min_samples_leaf']
        }
        st.json(tuned_params)
        
        # Evaluate on test set
        test_score, metric_name = evaluate_model(st.session_state.best_grid_model, st.session_state.X_test, st.session_state.y_test)
        st.markdown(f"### Test Set {metric_name}: {test_score:.4f}")
    
    st.markdown("""
    <div class="card">
    <h3>When to Use Grid Search</h3>
    <ul>
        <li>When you have a small number of hyperparameters to tune</li>
        <li>When you have computational resources to spare</li>
        <li>When you need to be exhaustive in your search</li>
        <li>When the evaluation of each model is relatively quick</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Random Search Tab
elif selected == "🎲 Random Search":
    st.header("Random Search")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
        <h3>How Random Search Works</h3>
        <p>Random Search samples random combinations of hyperparameters from a defined search space, rather than testing all possible combinations.</p>
        <p>It works by:</p>
        <ol>
            <li>Defining distributions for each hyperparameter</li>
            <li>Randomly sampling a specified number of combinations from these distributions</li>
            <li>Training and evaluating models with each sampled combination</li>
            <li>Selecting the combination that yields the best performance</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image("https://scikit-learn.org/stable/_images/randomized_search.png",
                 caption="Random Search vs. Grid Search",
                 use_container_width=True)
    
    st.markdown("""
    <div class="card">
    <h3>Advantages & Disadvantages</h3>
    <p><strong>Advantages:</strong></p>
    <ul>
        <li>More efficient than grid search for high-dimensional spaces</li>
        <li>Can find good hyperparameters with fewer evaluations</li>
        <li>Allows continuous parameters without discretization</li>
    </ul>
    <p><strong>Disadvantages:</strong></p>
    <ul>
        <li>May miss optimal combinations by chance</li>
        <li>Less systematic than grid search</li>
        <li>Results may vary between runs due to randomness</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Random Search Demo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        n_iter = st.slider(
            "Number of random combinations to try:",
            min_value=5,
            max_value=100,
            value=20,
            step=5,
            help="Higher values provide better results but take longer to compute"
        )
        
        n_estimators_min = st.number_input("n_estimators min:", value=10, min_value=1, max_value=1000)
        n_estimators_max = st.number_input("n_estimators max:", value=200, min_value=1, max_value=1000)
    
    with col2:
        max_depth_choices = st.multiselect(
            "max_depth choices (None for unlimited):",
            options=["None", "5", "10", "20", "30", "40", "50"],
            default=["None", "10", "20", "30"]
        )
        
        min_samples_split_min = st.number_input("min_samples_split min:", value=2, min_value=2, max_value=20)
        min_samples_split_max = st.number_input("min_samples_split max:", value=20, min_value=2, max_value=50)
        
        min_samples_leaf_min = st.number_input("min_samples_leaf min:", value=1, min_value=1, max_value=10)
        min_samples_leaf_max = st.number_input("min_samples_leaf max:", value=10, min_value=1, max_value=50)
    
    if st.button("Run Random Search", key="run_random_search"):
        # Load dataset if not already loaded
        if st.session_state.X_train is None:
            X_train, X_test, y_train, y_test = load_dataset()
        else:
            X_train = st.session_state.X_train
            X_test = st.session_state.X_test
            y_train = st.session_state.y_train
            y_test = st.session_state.y_test
        
        # Get base model
        model, _, scoring = get_model_and_params()
        
        # Process max_depth choices
        max_depth_values = []
        for choice in max_depth_choices:
            if choice == "None":
                max_depth_values.append(None)
            else:
                max_depth_values.append(int(choice))
        
        # Create parameter distributions for random search
        param_distributions = {
            'n_estimators': list(range(n_estimators_min, n_estimators_max+1, 10)),
            'max_depth': max_depth_values,
            'min_samples_split': list(range(min_samples_split_min, min_samples_split_max+1)),
            'min_samples_leaf': list(range(min_samples_leaf_min, min_samples_leaf_max+1))
        }
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Run random search
        status_text.text("Running Random Search...")
        start_time = time.time()
        
        random_search = RandomizedSearchCV(
            estimator=model,
            param_distributions=param_distributions,
            n_iter=n_iter,
            cv=3,
            n_jobs=-1,
            verbose=0,
            scoring=scoring,
            return_train_score=True,
            random_state=42
        )
        
        random_search.fit(X_train, y_train)
        
        end_time = time.time()
        execution_time = end_time - start_time
        st.session_state.random_time = execution_time
        
        progress_bar.progress(100)
        status_text.success(f"Random Search completed in {execution_time:.2f} seconds")
        
        # Store results
        st.session_state.best_random_model = random_search.best_estimator_
        st.session_state.random_results = pd.DataFrame(random_search.cv_results_)
        
        # Show best hyperparameters
        st.markdown("### Best Hyperparameters")
        st.json(random_search.best_params_)
        
        # Evaluate on test set
        test_score, metric_name = evaluate_model(random_search.best_estimator_, X_test, y_test)
        st.markdown(f"### Test Set {metric_name}: {test_score:.4f}")
        
        # Visualization
        st.markdown("### Random Search Results Visualization")
        
        tab1, tab2, tab3 = st.tabs(["Score Distribution", "Parameter Importance", "Parallel Coordinates"])
        
        with tab1:
            # Score distribution
            results_df = st.session_state.random_results.sort_values('rank_test_score')
            
            fig = px.histogram(
                results_df, 
                x='mean_test_score',
                nbins=20,
                title='Distribution of Scores from Random Search',
                color_discrete_sequence=[AWS_COLORS["accent1"]]
            )
            
            fig.add_vline(
                x=results_df['mean_test_score'].max(),
                line_dash="dash", 
                line_color=AWS_COLORS["secondary"],
                annotation_text="Best score"
            )
            
            fig.update_layout(
                xaxis_title="Mean Test Score",
                yaxis_title="Count",
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Parameter importance through correlation with score
            results_df = st.session_state.random_results
            
            # Extract parameter values for correlation analysis
            param_columns = {}
            for param in param_distributions.keys():
                col_name = f'param_{param}'
                if col_name in results_df.columns:
                    # Convert to numeric when possible
                    if param != 'max_depth':  # max_depth can be None
                        param_columns[param] = pd.to_numeric(results_df[col_name])
                    else:
                        # Handle max_depth specially
                        param_columns[param] = results_df[col_name].map(lambda x: 1000 if x == 'None' else float(x))
            
            # Create dataframe for correlation
            corr_df = pd.DataFrame(param_columns)
            corr_df['score'] = results_df['mean_test_score']
            
            # Calculate correlations with score
            correlations = {}
            for param in param_columns.keys():
                correlations[param] = corr_df[param].corr(corr_df['score'])
            
            # Create bar chart of correlations
            corr_df = pd.DataFrame({
                'Parameter': list(correlations.keys()),
                'Correlation with Score': list(correlations.values())
            }).sort_values('Correlation with Score', key=abs, ascending=False)
            
            fig = px.bar(
                corr_df,
                x='Parameter',
                y='Correlation with Score',
                title='Parameter Correlation with Score',
                color='Correlation with Score',
                color_continuous_scale='RdBu_r',
                range_color=[-1, 1]
            )
            
            fig.update_layout(
                xaxis_title="Hyperparameter",
                yaxis_title="Correlation with Score",
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div style="font-size: 0.9em; color: #666;">
            <p><strong>Note:</strong> High positive correlation means higher values are better for performance. 
            High negative correlation means lower values are better for performance.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tab3:
            # Parallel coordinates plot
            results_df = st.session_state.random_results.sort_values('mean_test_score', ascending=False).head(10)
            
            # Process parameters for parallel coordinates
            params_to_plot = {}
            for param in param_distributions.keys():
                col_name = f'param_{param}'
                if col_name in results_df.columns:
                    if param != 'max_depth':
                        params_to_plot[param] = pd.to_numeric(results_df[col_name])
                    else:
                        # Special handling for max_depth
                        params_to_plot[param] = results_df[col_name].map(lambda x: 1000 if x == 'None' else float(x))
            
            # Create dataframe for parallel coordinates
            plot_df = pd.DataFrame(params_to_plot)
            plot_df['score'] = results_df['mean_test_score']
            
            # Create parallel coordinates plot
            dimensions = [{
                'label': col, 
                'values': plot_df[col]
            } for col in plot_df.columns]
            
            fig = go.Figure(data=
                go.Parcoords(
                    line=dict(
                        color=plot_df['score'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title='Score')
                    ),
                    dimensions=dimensions
                )
            )
            
            fig.update_layout(
                title='Top 10 Parameter Combinations',
                template="plotly_white",
                height=600
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Top 10 parameter combinations
            st.markdown("### Top 10 Parameter Combinations")
            top_results = results_df[['params', 'mean_test_score', 'std_test_score', 'rank_test_score']].head(10)
            st.dataframe(top_results)
    
    elif st.session_state.best_random_model is not None:
        # If we already have results, display them
        st.success(f"Random Search completed in {st.session_state.random_time:.2f} seconds")
        
        # Show best hyperparameters
        st.markdown("### Best Hyperparameters")
        best_params = st.session_state.best_random_model.get_params()
        
        # Filter to only show the tuned parameters
        tuned_params = {
            'n_estimators': best_params['n_estimators'],
            'max_depth': best_params['max_depth'],
            'min_samples_split': best_params['min_samples_split'],
            'min_samples_leaf': best_params['min_samples_leaf']
        }
        st.json(tuned_params)
        
        # Evaluate on test set
        test_score, metric_name = evaluate_model(st.session_state.best_random_model, st.session_state.X_test, st.session_state.y_test)
        st.markdown(f"### Test Set {metric_name}: {test_score:.4f}")
    
    st.markdown("""
    <div class="card">
    <h3>Why Random Search Often Outperforms Grid Search</h3>
    <p>Research by Bergstra and Bengio showed that random search often finds better hyperparameters in less time than grid search.</p>
    <p>This is because:</p>
    <ul>
        <li>Not all hyperparameters are equally important</li>
        <li>Random search tests more values for each hyperparameter</li>
        <li>Grid search wastes evaluations on unimportant parameters</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
    <h3>When to Use Random Search</h3>
    <ul>
        <li>When you have limited computational resources</li>
        <li>When you have many hyperparameters to tune</li>
        <li>When you don't know which ranges of hyperparameter values are optimal</li>
        <li>When you're doing preliminary exploration of the hyperparameter space</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Bayesian Optimization Tab
elif selected == "🧠 Bayesian Optimization":
    st.header("Bayesian Optimization")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
        <h3>How Bayesian Optimization Works</h3>
        <p>Bayesian Optimization is a sequential strategy for optimizing black-box functions that uses previous evaluations to determine the next points to evaluate.</p>
        <p>It works by:</p>
        <ol>
            <li>Building a probabilistic model of the objective function (surrogate model)</li>
            <li>Using an acquisition function to balance exploration and exploitation</li>
            <li>Selecting new hyperparameter values that maximize the acquisition function</li>
            <li>Updating the surrogate model with new evaluation results</li>
            <li>Repeating until convergence or a budget is exhausted</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image("https://miro.medium.com/max/1400/1*qWQ9SRRlSjIgr9bsCI-M5g.png", 
                 caption="Bayesian Optimization Process",
                 use_container_width=True)
    
    st.markdown("""
    <div class="card">
    <h3>Advantages & Disadvantages</h3>
    <p><strong>Advantages:</strong></p>
    <ul>
        <li>More efficient than random or grid search</li>
        <li>Works well for expensive-to-evaluate functions</li>
        <li>Makes informed choices about which hyperparameters to evaluate next</li>
        <li>Can handle continuous and discrete parameters</li>
    </ul>
    <p><strong>Disadvantages:</strong></p>
    <ul>
        <li>More complex to implement</li>
        <li>May get stuck in local optima</li>
        <li>Effectiveness depends on the quality of the surrogate model</li>
        <li>Less parallelizable than grid or random search</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Bayesian Optimization Demo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        n_iter_bayesian = st.slider(
            "Number of iterations:",
            min_value=5,
            max_value=50,
            value=20,
            step=5,
            help="Number of parameter settings that are sampled"
        )
        
        n_initial_points = st.slider(
            "Number of initial points:",
            min_value=3,
            max_value=20,
            value=5,
            step=1,
            help="Number of random points to evaluate before starting Bayesian optimization"
        )
    
    with col2:
        acq_func = st.selectbox(
            "Acquisition function:",
            options=["LCB", "EI", "PI"],
            index=1,
            help="""
            EI (Expected Improvement): Balance between exploration and exploitation
            PI (Probability of Improvement): More exploitative
            LCB (Lower Confidence Bound): More explorative
            """
        )
        
        random_state = st.number_input(
            "Random seed:",
            value=42,
            min_value=1,
            max_value=1000,
            help="Random seed for reproducibility"
        )
    
    if st.button("Run Bayesian Optimization", key="run_bayesian"):
        # Load dataset if not already loaded
        if st.session_state.X_train is None:
            X_train, X_test, y_train, y_test = load_dataset()
        else:
            X_train = st.session_state.X_train
            X_test = st.session_state.X_test
            y_train = st.session_state.y_train
            y_test = st.session_state.y_test
        
        # Get base model
        model, _, scoring = get_model_and_params()
        
        # Define search space
        search_space = {
            'n_estimators': Integer(10, 200),
            'max_depth': Integer(1, 30),  # Use Integer for max_depth and handle None in post-processing
            'min_samples_split': Integer(2, 20),
            'min_samples_leaf': Integer(1, 10)
        }
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Run Bayesian optimization
        status_text.text("Running Bayesian Optimization...")
        start_time = time.time()
        
        bayes_search = BayesSearchCV(
            estimator=model,
            search_spaces=search_space,
            n_iter=n_iter_bayesian,
            cv=3,
            n_jobs=-1,
            verbose=0,
            scoring=scoring,
            return_train_score=True,
            random_state=random_state,
            n_points=n_initial_points,
            optimizer_kwargs={'acq_func': acq_func}
        )
        
        bayes_search.fit(X_train, y_train)
        
        end_time = time.time()
        execution_time = end_time - start_time
        st.session_state.bayesian_time = execution_time
        
        progress_bar.progress(100)
        status_text.success(f"Bayesian Optimization completed in {execution_time:.2f} seconds")
        
        # Store results
        st.session_state.best_bayesian_model = bayes_search.best_estimator_
        st.session_state.bayesian_results = pd.DataFrame(bayes_search.cv_results_)
        
        # Post-process max_depth (convert 30 back to None)
        best_params = bayes_search.best_params_
        if 'max_depth' in best_params and best_params['max_depth'] == 30:
            best_params['max_depth'] = None
        
        # Show best hyperparameters
        st.markdown("### Best Hyperparameters")
        st.json(best_params)
        
        # Evaluate on test set
        test_score, metric_name = evaluate_model(bayes_search.best_estimator_, X_test, y_test)
        st.markdown(f"### Test Set {metric_name}: {test_score:.4f}")
        
        # Visualization
        st.markdown("### Bayesian Optimization Results Visualization")
        
        tab1, tab2 = st.tabs(["Convergence Plot", "Parameter Importance"])
        
        with tab1:
            # Convergence plot
            results_df = st.session_state.bayesian_results.sort_values('rank_test_score')
            
            # Extract iteration numbers and scores
            iterations = np.arange(len(results_df))
            scores = results_df['mean_test_score'].values
            
            # Sort by time/iteration to show improvement over time
            iter_scores = sorted(zip(iterations, scores), key=lambda x: x[0])
            iterations, scores = zip(*iter_scores)
            
            # Find best score at each iteration
            best_so_far = np.maximum.accumulate(scores)
            
            # Create convergence plot
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=iterations,
                y=scores,
                mode='markers',
                name='Iterations',
                marker=dict(color=AWS_COLORS["accent1"])
            ))
            
            fig.add_trace(go.Scatter(
                x=iterations,
                y=best_so_far,
                mode='lines+markers',
                name='Best So Far',
                marker=dict(color=AWS_COLORS["secondary"])
            ))
            
            fig.update_layout(
                title="Convergence of Bayesian Optimization",
                xaxis_title="Iteration",
                yaxis_title="Score",
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div style="font-size: 0.9em; color: #666;">
            <p><strong>Note:</strong> The plot shows how the model performance improves as the Bayesian optimization 
            explores the hyperparameter space. The orange line shows the best score found so far at each iteration.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tab2:
            # Parameter importance through feature importance
            results_df = st.session_state.bayesian_results
            
            # Extract parameter values
            params = ['param_n_estimators', 'param_max_depth', 'param_min_samples_split', 'param_min_samples_leaf']
            
            # Create a simple model to predict scores from parameters
            param_values = results_df[params].copy()
            
            # Convert to numeric
            for col in params:
                param_values[col] = pd.to_numeric(param_values[col], errors='coerce')
                param_values[col].fillna(30, inplace=True)  # Replace None with 30 for max_depth
            
            # Train a simple RandomForest to predict scores from parameters
            X_params = param_values.values
            y_scores = results_df['mean_test_score'].values
            
            param_importance_model = RandomForestRegressor(n_estimators=50, random_state=42)
            param_importance_model.fit(X_params, y_scores)
            
            # Get feature importances
            importances = param_importance_model.feature_importances_
            param_names = ['n_estimators', 'max_depth', 'min_samples_split', 'min_samples_leaf']
            
            # Create bar chart of feature importances
            importance_df = pd.DataFrame({
                'Parameter': param_names,
                'Importance': importances
            }).sort_values('Importance', ascending=False)
            
            fig = px.bar(
                importance_df,
                x='Parameter',
                y='Importance',
                title='Parameter Importance for Performance',
                color='Importance',
                color_continuous_scale='Viridis'
            )
            
            fig.update_layout(
                xaxis_title="Hyperparameter",
                yaxis_title="Importance",
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div style="font-size: 0.9em; color: #666;">
            <p><strong>Note:</strong> Parameter importance is estimated by training a model to predict scores 
            from parameters and extracting feature importances. Higher values indicate parameters that have a
            stronger influence on model performance.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Optimal parameter ranges
            st.markdown("### Optimal Parameter Ranges")
            st.markdown("""
            This visualization shows where in the parameter space the best models were found.
            """)
            
            # Get top 25% of models
            threshold = np.percentile(results_df['mean_test_score'], 75)
            top_models = results_df[results_df['mean_test_score'] >= threshold]
            
            # Create pair plot of parameters for top models
            param_data = {}
            for param in param_names:
                col_name = f'param_{param}'
                if col_name in top_models:
                    param_data[param] = pd.to_numeric(top_models[col_name], errors='coerce')
                    # Fill NaN values (which could be None for max_depth)
                    if param == 'max_depth':
                        param_data[param].fillna(30, inplace=True)
            
            if param_data:
                param_df = pd.DataFrame(param_data)
                param_df['score'] = top_models['mean_test_score']
                
                # Create scatter plot for each parameter pair
                for i, param1 in enumerate(param_names):
                    if param1 in param_df.columns:
                        for j, param2 in enumerate(param_names[i+1:], i+1):
                            if param2 in param_df.columns:
                                fig = px.scatter(
                                    param_df,
                                    x=param1,
                                    y=param2,
                                    color='score',
                                    color_continuous_scale='Viridis',
                                    title=f"Best models: {param1} vs {param2}",
                                    height=400
                                )
                                
                                fig.update_layout(template="plotly_white")
                                st.plotly_chart(fig, use_container_width=True)
    
    elif st.session_state.best_bayesian_model is not None:
        # If we already have results, display them
        st.success(f"Bayesian Optimization completed in {st.session_state.bayesian_time:.2f} seconds")
        
        # Show best hyperparameters
        st.markdown("### Best Hyperparameters")
        best_params = st.session_state.best_bayesian_model.get_params()
        
        # Filter to only show the tuned parameters
        tuned_params = {
            'n_estimators': best_params['n_estimators'],
            'max_depth': best_params['max_depth'],
            'min_samples_split': best_params['min_samples_split'],
            'min_samples_leaf': best_params['min_samples_leaf']
        }
        st.json(tuned_params)
        
        # Evaluate on test set
        test_score, metric_name = evaluate_model(st.session_state.best_bayesian_model, st.session_state.X_test, st.session_state.y_test)
        st.markdown(f"### Test Set {metric_name}: {test_score:.4f}")
    
    st.markdown("""
    <div class="card">
    <h3>How It Works: The Surrogate Model</h3>
    <p>The surrogate model is typically a Gaussian Process that provides:</p>
    <ul>
        <li>A prediction of the objective function value for any point in the parameter space</li>
        <li>An uncertainty estimate for that prediction</li>
    </ul>
    <p>The acquisition function uses both the predicted value and uncertainty to select new points, balancing:</p>
    <ul>
        <li><strong>Exploitation</strong>: Sampling where the surrogate model predicts good values</li>
        <li><strong>Exploration</strong>: Sampling where the surrogate model is uncertain</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
    <h3>When to Use Bayesian Optimization</h3>
    <ul>
        <li>When evaluating each hyperparameter combination is expensive (e.g., training deep neural networks)</li>
        <li>When you need to find good hyperparameters with minimal evaluations</li>
        <li>When the objective function is noisy</li>
        <li>When you want more informed exploration than random search</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Hyperband Tab
elif selected == "⚡ Hyperband":
    st.header("Hyperband")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
        <h3>How Hyperband Works</h3>
        <p>Hyperband is a resource allocation strategy for hyperparameter optimization. It focuses on allocating more resources to promising configurations.</p>
        <p>It works by:</p>
        <ol>
            <li>Sampling many configurations randomly</li>
            <li>Evaluating all configurations with a small budget (e.g., few training iterations)</li>
            <li>Eliminating the worst performing configurations</li>
            <li>Allocating more resources to survivors</li>
            <li>Repeating until finding the best configuration</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image("https://miro.medium.com/max/1400/0*Z9GuqmrpIvIo-MvY", 
                 caption="Hyperband Elimination Process",
                 use_container_width=True)
    
    st.markdown("""
    <div class="card">
    <h3>Advantages & Disadvantages</h3>
    <p><strong>Advantages:</strong></p>
    <ul>
        <li>Extremely efficient for deep learning models</li>
        <li>Spends more time evaluating promising configurations</li>
        <li>Quickly eliminates poor performing configurations</li>
        <li>Can be combined with other search strategies</li>
    </ul>
    <p><strong>Disadvantages:</strong></p>
    <ul>
        <li>May eliminate promising configurations that start slow</li>
        <li>Requires configurations that can be trained with varying resources</li>
        <li>More complex implementation</li>
        <li>Initial random sampling can be inefficient</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Hyperband Demo")
    
    st.markdown("""
    <div class="card">
    <p>For this demo, we'll simulate Hyperband's early stopping approach with a simplified implementation.
    We'll train random forest models with different hyperparameters, evaluating them with increasing subsets 
    of the training data to mimic resource allocation.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        n_configs = st.slider(
            "Number of initial configurations:",
            min_value=10,
            max_value=50,
            value=20,
            step=5,
            help="Number of random configurations to start with"
        )
        
        reduction_factor = st.slider(
            "Reduction factor (η):",
            min_value=2,
            max_value=4,
            value=3,
            step=1,
            help="Factor by which the number of configurations is reduced in each round"
        )
    
    with col2:
        min_resource = st.slider(
            "Minimum resource (%):",
            min_value=10,
            max_value=50,
            value=20,
            step=10,
            help="Minimum percentage of training data to use in first round"
        )
        
        max_resource = st.slider(
            "Maximum resource (%):",
            min_value=60,
            max_value=100,
            value=100,
            step=10,
            help="Maximum percentage of training data to use in final round"
        )
    
    if st.button("Run Hyperband Simulation", key="run_hyperband"):
        # Load dataset if not already loaded
        if st.session_state.X_train is None:
            X_train, X_test, y_train, y_test = load_dataset()
        else:
            X_train = st.session_state.X_train
            X_test = st.session_state.X_test
            y_train = st.session_state.y_train
            y_test = st.session_state.y_test
        
        # Initialize Hyperband parameters
        min_resource_fraction = min_resource / 100
        max_resource_fraction = max_resource / 100
        
        # Define parameter space
        param_space = {
            'n_estimators': list(range(10, 201, 10)),
            'max_depth': [None, 3, 5, 10, 15, 20, 30],
            'min_samples_split': list(range(2, 21)),
            'min_samples_leaf': list(range(1, 11)),
        }
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Start Hyperband simulation
        status_text.text("Running Hyperband Simulation...")
        start_time = time.time()
        
        # Generate initial random configurations
        np.random.seed(42)
        configs = []
        
        for _ in range(n_configs):
            config = {
                'n_estimators': np.random.choice(param_space['n_estimators']),
                'max_depth': np.random.choice(param_space['max_depth']),
                'min_samples_split': np.random.choice(param_space['min_samples_split']),
                'min_samples_leaf': np.random.choice(param_space['min_samples_leaf'])
            }
            configs.append(config)
        
        # Calculate the number of brackets needed
        max_resource_per_config = len(X_train) * max_resource_fraction
        min_resource_per_config = len(X_train) * min_resource_fraction
        s_max = int(np.log(max_resource_per_config / min_resource_per_config) / np.log(reduction_factor))
        
        # For visualization purposes, we'll track all results
        all_results = []
        
        # Create columns for displaying intermediate results
        col1, col2 = st.columns(2)
        with col1:
            round_header = st.empty()
        with col2:
            configs_header = st.empty()
        
        results_container = st.container()
        
        # Simulate Successive Halving (the core algorithm in Hyperband)
        n = n_configs  # number of initial configs
        r = min_resource_per_config  # initial resource per config
        
        # Keep track of the best model and its score
        best_model = None
        best_score = float('-inf')
        
        # Track configurations and scores for each round
        rounds_data = []
        
        # Run successive halving
        round_num = 0
        remaining_configs = configs.copy()
        
        while len(remaining_configs) > 0:
            round_num += 1
            
            # Update progress
            progress = min(0.9, round_num / (s_max + 1))
            progress_bar.progress(progress)
            
            # Display round information
            round_header.markdown(f"### Round {round_num}")
            configs_header.markdown(f"#### Configurations remaining: {len(remaining_configs)}")
            
            round_results = []
            
            # Resource for this round
            resource_size = int(r * len(X_train))
            resource_percent = int(r * 100 / max_resource_fraction)
            
            # Use only a subset of the training data
            indices = np.random.choice(len(X_train), resource_size, replace=True)
            X_train_subset = X_train[indices]
            y_train_subset = y_train[indices]
            
            # Evaluate each configuration
            for i, config in enumerate(remaining_configs):
                # Create and train model with current config
                if st.session_state.task_type == "classification":
                    model = RandomForestClassifier(random_state=42, **config)
                else:
                    model = RandomForestRegressor(random_state=42, **config)
                
                model.fit(X_train_subset, y_train_subset)
                
                # Evaluate on validation set (using remaining training data)
                val_indices = np.setdiff1d(np.arange(len(X_train)), indices)
                if len(val_indices) > 0:
                    X_val = X_train[val_indices]
                    y_val = y_train[val_indices]
                    
                    if st.session_state.task_type == "classification":
                        score = accuracy_score(y_val, model.predict(X_val))
                        metric_name = "Accuracy"
                    else:
                        score = -mean_squared_error(y_val, model.predict(X_val))
                        metric_name = "Neg. MSE"
                else:
                    # If all training data was used, evaluate on test set
                    score, metric_name = evaluate_model(model, X_test, y_test)
                
                # Keep track of best model overall
                if score > best_score:
                    best_score = score
                    best_model = model
                
                # Store results
                round_results.append({
                    'config': config,
                    'score': score,
                    'resource': resource_percent,
                    'model': model
                })
                
                all_results.append({
                    'round': round_num,
                    'config_id': i,
                    'n_estimators': config['n_estimators'],
                    'max_depth': str(config['max_depth']),
                    'min_samples_split': config['min_samples_split'],
                    'min_samples_leaf': config['min_samples_leaf'],
                    'score': score,
                    'resource': resource_percent
                })
            
            # Sort configs by score
            round_results.sort(key=lambda x: x['score'], reverse=True)
            
            # Save round data for visualization
            rounds_data.append({
                'round': round_num,
                'resource_percent': resource_percent,
                'configs': len(remaining_configs),
                'results': round_results
            })
            
            # Display top configs in this round
            with results_container:
                st.markdown(f"#### Results for Round {round_num} (Using {resource_percent}% of training data)")
                top_k = min(5, len(round_results))
                display_df = pd.DataFrame([
                    {
                        'Config ID': i + 1,
                        'n_estimators': res['config']['n_estimators'],
                        'max_depth': str(res['config']['max_depth']),
                        'min_samples_split': res['config']['min_samples_split'],
                        'min_samples_leaf': res['config']['min_samples_leaf'],
                        f'{metric_name}': f"{res['score']:.4f}"
                    }
                    for i, res in enumerate(round_results[:top_k])
                ])
                st.dataframe(display_df)
            
            # Determine how many configs to keep
            k = int(len(remaining_configs) / reduction_factor)
            if k == 0:  # We've reached the end
                break
                
            # Keep top k configs
            remaining_configs = [res['config'] for res in round_results[:k]]
            
            # Increase resource for next round
            r = min(r * reduction_factor, max_resource_fraction)
        
        # Final evaluation on full test set
        end_time = time.time()
        execution_time = end_time - start_time
        st.session_state.hyperband_time = execution_time
        
        # Store results
        st.session_state.best_hyperband_model = best_model
        st.session_state.hyperband_results = pd.DataFrame(all_results)
        
        progress_bar.progress(100)
        status_text.success(f"Hyperband Simulation completed in {execution_time:.2f} seconds")
        
        # Show best hyperparameters
        st.markdown("### Best Hyperparameters Found")
        best_params = best_model.get_params()
        
        # Filter to only show the tuned parameters
        tuned_params = {
            'n_estimators': best_params['n_estimators'],
            'max_depth': best_params['max_depth'],
            'min_samples_split': best_params['min_samples_split'],
            'min_samples_leaf': best_params['min_samples_leaf']
        }
        st.json(tuned_params)
        
        # Evaluate on test set
        test_score, metric_name = evaluate_model(best_model, X_test, y_test)
        st.markdown(f"### Test Set {metric_name}: {test_score:.4f}")
        
        # Visualizations
        st.markdown("### Hyperband Results Visualization")
        
        tab1, tab2 = st.tabs(["Elimination Process", "Performance vs. Resources"])
        
        with tab1:
            # Create visualization of the elimination process
            round_summary = pd.DataFrame([
                {
                    'Round': rd['round'],
                    'Resource (%)': rd['resource_percent'],
                    'Configurations': rd['configs'],
                    'Best Score': max([r['score'] for r in rd['results']])
                }
                for rd in rounds_data
            ])
            
            fig = go.Figure()
            
            # Add configurations bar
            fig.add_trace(go.Bar(
                x=round_summary['Round'],
                y=round_summary['Configurations'],
                name='Configurations',
                marker_color=AWS_COLORS["accent1"]
            ))
            
            # Add resource line
            fig.add_trace(go.Scatter(
                x=round_summary['Round'],
                y=round_summary['Resource (%)'],
                mode='lines+markers',
                name='Resource (%)',
                marker=dict(color=AWS_COLORS["secondary"]),
                yaxis='y2'
            ))
            
            # Add best score line
            fig.add_trace(go.Scatter(
                x=round_summary['Round'],
                y=round_summary['Best Score'],
                mode='lines+markers',
                name='Best Score',
                marker=dict(color=AWS_COLORS["success"]),
                yaxis='y3'
            ))
            
            fig.update_layout(
                title="Hyperband Elimination Process",
                xaxis=dict(
                    title="Round",
                    tickmode='linear',
                    tick0=1,
                    dtick=1
                ),
                yaxis=dict(
                    title="Configurations",
                    range=[0, n_configs * 1.1]
                ),
                yaxis2=dict(
                    title="Resource (%)",
                    overlaying='y',
                    side='right',
                    range=[0, 105]
                ),
                yaxis3=dict(
                    title=f"{metric_name}",
                    overlaying='y',
                    side='right',
                    anchor='free',
                    position=1,
                    range=[0, 1.1] if st.session_state.task_type == "classification" else None
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                template="plotly_white",
                height=500,
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div style="font-size: 0.9em; color: #666;">
            <p><strong>Note:</strong> This chart shows how Hyperband eliminates poor performing configurations 
            in each round while allocating more resources to promising ones. The number of configurations 
            decreases while the allocated resources increase.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tab2:
            # Create scatter plot showing performance vs resources
            results_df = st.session_state.hyperband_results
            
            fig = px.scatter(
                results_df,
                x="resource", 
                y="score",
                color="round",
                hover_data=["n_estimators", "max_depth", "min_samples_split", "min_samples_leaf"],
                title=f"Performance vs. Resources",
                color_continuous_scale="Viridis"
            )
            
            fig.update_layout(
                xaxis_title="Resources Used (%)",
                yaxis_title=f"{metric_name}",
                template="plotly_white",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div style="font-size: 0.9em; color: #666;">
            <p><strong>Note:</strong> This scatter plot shows how performance changes with increased resources
            for different configurations. Each color represents a different round of the Hyperband algorithm.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Top configurations
            st.markdown("### Top Configurations by Round")
            
            for rd in rounds_data:
                st.markdown(f"#### Round {rd['round']} (Resource: {rd['resource_percent']}%)")
                
                top_configs = pd.DataFrame([
                    {
                        'n_estimators': res['config']['n_estimators'],
                        'max_depth': str(res['config']['max_depth']),
                        'min_samples_split': res['config']['min_samples_split'],
                        'min_samples_leaf': res['config']['min_samples_leaf'],
                        f'{metric_name}': res['score']
                    }
                    for res in rd['results'][:3]  # Show top 3 for each round
                ])
                
                st.dataframe(top_configs)
    
    elif st.session_state.best_hyperband_model is not None:
        # If we already have results, display them
        st.success(f"Hyperband Simulation completed in {st.session_state.hyperband_time:.2f} seconds")
        
        # Show best hyperparameters
        st.markdown("### Best Hyperparameters")
        best_params = st.session_state.best_hyperband_model.get_params()
        
        # Filter to only show the tuned parameters
        tuned_params = {
            'n_estimators': best_params['n_estimators'],
            'max_depth': best_params['max_depth'],
            'min_samples_split': best_params['min_samples_split'],
            'min_samples_leaf': best_params['min_samples_leaf']
        }
        st.json(tuned_params)
        
        # Evaluate on test set
        test_score, metric_name = evaluate_model(st.session_state.best_hyperband_model, st.session_state.X_test, st.session_state.y_test)
        st.markdown(f"### Test Set {metric_name}: {test_score:.4f}")
    
    st.markdown("""
    <div class="card">
    <h3>Successive Halving: The Core of Hyperband</h3>
    <p>Hyperband is built on Successive Halving, which works as follows:</p>
    <ol>
        <li>Start with n configurations, each using r resources</li>
        <li>Evaluate all configurations and keep the top 1/η performing ones</li>
        <li>Increase the resource allocation by a factor of η for the remaining configurations</li>
        <li>Repeat until only one configuration remains or maximum resource is reached</li>
    </ol>
    <p>Hyperband runs multiple brackets of successive halving with different allocations of configurations and resources.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
    <h3>When to Use Hyperband</h3>
    <ul>
        <li>When training models with very long training times (e.g., deep neural networks)</li>
        <li>When computational resources are limited</li>
        <li>When you can evaluate a model's potential with partial resources</li>
        <li>When you want to efficiently explore many configurations</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 40px; padding: 20px; background-color: #f5f5f5; border-radius: 10px;">
<p>Created with 💙 using Streamlit and Python | AWS ML University</p>
</div>
""", unsafe_allow_html=True)
# ```

# ## Application Description

# This Streamlit application provides an interactive e-learning environment for understanding various hyperparameter tuning techniques in machine learning. Here's what the application offers:

# ### Key Features

# 1. **Interactive demonstrations** of four hyperparameter tuning techniques:
#    - Grid Search
#    - Random Search
#    - Bayesian Optimization
#    - Hyperband

# 2. **Task flexibility** - supports both classification and regression tasks

# 3. **Visual explanations** with charts, tables, and interactive elements for each tuning technique

# 4. **Session management** with ability to reset at any time via the sidebar

# 5. **Modern UI/UX** using AWS-inspired color scheme and responsive layout

# 6. **Comparison tools** to see which techniques perform best for your specific task

# ### Technical Implementation

# - Uses the latest Streamlit features for responsive UI
# - Implements popular ML libraries (scikit-learn, hyperopt, scikit-optimize)
# - Visualizations with Plotly for interactive charts
# - Tabbed navigation with emoji icons for intuitive user experience
# - Session state management to preserve results between tab switches

# ### Learning Experience

# The application walks users through each hyperparameter tuning technique with:
# 1. Conceptual explanations
# 2. Visual diagrams
# 3. Interactive demos where users can adjust parameters
# 4. Result visualizations and performance metrics
# 5. Comparative analysis between methods

# This creates a comprehensive learning environment where users can not only read about hyperparameter tuning but actively explore and experiment with different approaches.