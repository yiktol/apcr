import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.impute import SimpleImputer
from sklearn.datasets import make_classification
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
import io

# Set page configuration
st.set_page_config(
    page_title="Data Cleaning for ML",
    page_icon="🧹",
    layout="wide"
)

# AWS color scheme
aws_colors = {
    'orange': '#FF9900',
    'dark_blue': '#232F3E',
    'light_blue': '#1A73E8',
    'teal': '#007DBC',
    'light_gray': '#F2F3F3',
    'dark_gray': '#545B64'
}

# Set custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #F2F3F3;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #F2F3F3;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        color: #232F3E;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF9900 !important;
        color: white !important;
    
    }
    div[data-testid="stSidebarNav"] li div a {
        margin-left: 1rem;
        padding: 0rem;
        width: 300px;
        border-radius: 0.5rem;
    }
    div[data-testid="stSidebarNav"] li div::focus-visible {
        background-color: rgba(151, 166, 195, 0.15);
    }
    div[data-baseweb="card"] {
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #e6e6e6;
    }
    .css-1y4p8pa {
        max-width: 100%;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for session management
st.sidebar.image("https://d0.awsstatic.com/logos/powered-by-aws.png", width=200)
st.sidebar.title("Session Management")

if st.sidebar.button("🔄 Reset Session", key="reset_session"):
    # Clear all session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()



# Header
st.title("🧹 Data Cleaning for Machine Learning")
st.markdown("Explore different data transformation techniques to prepare your data for ML models")

# Initialize sample data
def generate_sample_data(n_samples=100, seed=42):
    np.random.seed(seed)
    
    # Generate a DataFrame with some patterns and issues
    df = pd.DataFrame({
        'age': np.random.randint(18, 90, n_samples),
        'income': np.random.normal(50000, 15000, n_samples),
        'years_experience': np.random.randint(0, 40, n_samples),
        'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD', None], n_samples, 
                                    p=[0.3, 0.3, 0.2, 0.1, 0.1]),
        'job_category': np.random.choice(['Tech', 'Finance', 'Healthcare', 'Education', 'Other'], n_samples),
        'satisfaction': np.random.choice([1, 2, 3, 4, 5, None], n_samples, p=[0.1, 0.2, 0.3, 0.2, 0.1, 0.1]),
    })
    
    # Add some duplicates
    duplicate_indices = np.random.choice(range(n_samples), size=int(n_samples*0.1), replace=False)
    for idx in duplicate_indices:
        duplicate_idx = np.random.randint(0, n_samples)
        df.iloc[idx] = df.iloc[duplicate_idx]
    
    # Add some correlations
    df['bonus'] = df['income'] * np.random.uniform(0.05, 0.2, n_samples) + np.random.normal(0, 2000, n_samples)
    
    # Add some outliers
    outlier_indices = np.random.choice(range(n_samples), size=5, replace=False)
    df.loc[outlier_indices, 'income'] = np.random.normal(200000, 50000, len(outlier_indices))
    
    # Add some more missing values
    for col in ['age', 'income', 'years_experience']:
        missing_indices = np.random.choice(range(n_samples), size=int(n_samples*0.05), replace=False)
        df.loc[missing_indices, col] = np.nan
    
    # Add a target column for classification
    X, y = make_classification(n_samples=n_samples, n_features=1, n_informative=1, n_redundant=0,
                             n_classes=2, n_clusters_per_class=1, weights=[0.8, 0.2], random_state=seed)
    df['target'] = y
    
    return df

def reset_data():
    if 'df' in st.session_state:
        del st.session_state.df
    if 'df_original' in st.session_state:
        del st.session_state.df_original

if 'df' not in st.session_state:
    st.session_state.df = generate_sample_data()
    st.session_state.df_original = st.session_state.df.copy()


# Reset data button
if st.sidebar.button("Reset to Original Data", key="reset_2"):
    reset_data()
    st.rerun()
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("This application demonstrates various data cleaning techniques for machine learning.")

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📚 Introduction", 
    "❓ Missing Values", 
    "🔄 Duplicates", 
    "📏 Feature Scaling", 
    "🎯 Feature Selection", 
    "⚖️ Balance Dataset", 
    "🛠️ Feature Engineering",
    "🔀 Data Conversion"
])

with tab1:
    st.header("Introduction to Data Cleaning")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Why Data Cleaning Matters
        
        Data cleaning is a critical step in the machine learning pipeline. Raw data often contains issues that can negatively impact model performance:
        
        - **Missing values** can lead to biased models
        - **Duplicates** can give undue weight to certain examples
        - **Outliers** can skew distributions and impact model training
        - **Inconsistent formats** can prevent the model from recognizing patterns
        - **Imbalanced data** can lead to biased predictions
        
        This application demonstrates various techniques to address these issues.
        """)
    
    with col2:
        st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2940&auto=format&fit=crop", 
                 caption="Data cleaning is an essential part of ML", use_container_width=True)
    
    st.subheader("Sample Dataset")
    st.dataframe(st.session_state.df)
    
    # Basic statistics about the dataset
    st.subheader("Data Statistics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Shape:", st.session_state.df.shape)
        st.write("Missing values:", st.session_state.df.isna().sum().sum())
        st.write("Duplicated rows:", st.session_state.df.duplicated().sum())
    
    with col2:
        # Create pie chart for target distribution
        fig = px.pie(
            values=st.session_state.df['target'].value_counts().values,
            names=st.session_state.df['target'].value_counts().index,
            title='Target Distribution',
            color_discrete_sequence=[aws_colors['teal'], aws_colors['orange']]
        )
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig)
    
    # Reset data button
    if st.button("Reset to Original Data"):
        reset_data()
        st.rerun()

with tab2:
    st.header("Handling Missing Values")
    
    st.markdown("""
    ### Missing Value Strategies
    
    Missing values can significantly affect your model's performance. Here are some common techniques for handling them:
    
    1. **Drop rows** with missing values (risky if you have limited data)
    2. **Impute values** using mean, median, mode, or more complex strategies
    3. **Use algorithms** that handle missing values natively
    
    The best approach depends on why the data is missing and how much data you have.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Visualize missing values
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(st.session_state.df.isnull(), cmap='viridis', yticklabels=False, cbar=False, ax=ax)
        plt.title('Missing Value Heatmap')
        st.pyplot(fig)
        
    with col2:
        # Missing value statistics
        missing_stats = pd.DataFrame({
            'Missing Values': st.session_state.df.isnull().sum(),
            'Percentage': st.session_state.df.isnull().sum() / len(st.session_state.df) * 100
        })
        fig = px.bar(
            missing_stats, 
            y=missing_stats.index, 
            x='Percentage',
            orientation='h',
            title='Percentage of Missing Values by Column',
            color_discrete_sequence=[aws_colors['teal']]
        )
        fig.update_layout(yaxis_title="", xaxis_title="Percent Missing")
        st.plotly_chart(fig)
    
    # Options for handling missing values
    st.subheader("Apply Missing Value Handling")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        missing_strategy = st.radio(
            "Choose a strategy for handling missing values:",
            ["Drop Rows", "Mean Imputation", "Median Imputation", "Mode Imputation"]
        )
        
        columns_to_handle = st.multiselect(
            "Select columns to handle missing values:",
            st.session_state.df.columns.tolist(),
            default=[col for col in st.session_state.df.columns if st.session_state.df[col].isnull().any()]
        )
    
    with col2:
        if st.button("Apply Missing Value Strategy"):
            if missing_strategy == "Drop Rows":
                st.session_state.df = st.session_state.df.dropna(subset=columns_to_handle)
                st.success(f"Dropped rows with missing values in selected columns. {len(st.session_state.df_original) - len(st.session_state.df)} rows removed.")
            else:
                for col in columns_to_handle:
                    if col in st.session_state.df.columns and st.session_state.df[col].isnull().any():
                        if st.session_state.df[col].dtype == 'object' or pd.api.types.is_categorical_dtype(st.session_state.df[col]):
                            # For categorical/text columns, use mode imputation regardless of selection
                            mode_val = st.session_state.df[col].mode()[0]
                            st.session_state.df[col].fillna(mode_val, inplace=True)
                            st.info(f"Column '{col}' is categorical - using mode imputation with value: {mode_val}")
                        else:
                            # For numeric columns, use the selected strategy
                            if missing_strategy == "Mean Imputation":
                                mean_val = st.session_state.df[col].mean()
                                st.session_state.df[col].fillna(mean_val, inplace=True)
                                st.info(f"Imputed missing values in '{col}' with mean: {mean_val:.2f}")
                            elif missing_strategy == "Median Imputation":
                                median_val = st.session_state.df[col].median()
                                st.session_state.df[col].fillna(median_val, inplace=True)
                                st.info(f"Imputed missing values in '{col}' with median: {median_val:.2f}")
                            elif missing_strategy == "Mode Imputation":
                                mode_val = st.session_state.df[col].mode()[0]
                                st.session_state.df[col].fillna(mode_val, inplace=True)
                                st.info(f"Imputed missing values in '{col}' with mode: {mode_val}")
    
    # Display the resulting dataframe
    st.subheader("Resulting Dataset")
    st.dataframe(st.session_state.df)
    
    # Show before and after statistics
    st.subheader("Before vs After")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Before:")
        st.write(f"Total rows: {len(st.session_state.df_original)}")
        st.write(f"Missing values: {st.session_state.df_original.isna().sum().sum()}")
    
    with col2:
        st.write("After:")
        st.write(f"Total rows: {len(st.session_state.df)}")
        st.write(f"Missing values: {st.session_state.df.isna().sum().sum()}")

with tab3:
    st.header("Handling Duplicates")
    
    st.markdown("""
    ### Why Handle Duplicates?
    
    Duplicate records in your dataset can:
    
    - Give unnecessary weight to certain examples during model training
    - Artificially inflate validation metrics
    - Leak information between training and testing sets
    
    It's important to identify and address duplicates before model training.
    """)
    
    # Identify duplicates
    duplicated = st.session_state.df.duplicated(keep=False)
    num_duplicates = duplicated.sum()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.metric("Total Duplicate Rows", num_duplicates)
        
        if num_duplicates > 0:
            st.subheader("Sample of Duplicated Records")
            st.dataframe(st.session_state.df[duplicated].head())
    
    with col2:
        # Visualization of duplicates
        labels = ['Unique', 'Duplicate']
        values = [len(st.session_state.df) - num_duplicates, num_duplicates]
        
        fig = px.pie(
            values=values,
            names=labels,
            title='Duplicate vs Unique Records',
            color_discrete_sequence=[aws_colors['teal'], aws_colors['orange']]
        )
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig)
    
    # Options for handling duplicates
    st.subheader("Apply Duplicate Handling")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        duplicate_strategy = st.radio(
            "Choose a strategy for handling duplicates:",
            ["Keep First Occurrence", "Keep Last Occurrence", "Drop All Duplicates"]
        )
        
        columns_for_dupes = st.multiselect(
            "Consider these columns when identifying duplicates (leave empty for all):",
            st.session_state.df.columns.tolist(),
            default=[]
        )
    
    with col2:
        if st.button("Remove Duplicates"):
            before_count = len(st.session_state.df)
            
            if duplicate_strategy == "Keep First Occurrence":
                st.session_state.df = st.session_state.df.drop_duplicates(
                    subset=columns_for_dupes if columns_for_dupes else None, 
                    keep='first'
                )
            elif duplicate_strategy == "Keep Last Occurrence":
                st.session_state.df = st.session_state.df.drop_duplicates(
                    subset=columns_for_dupes if columns_for_dupes else None, 
                    keep='last'
                )
            else:  # "Drop All Duplicates"
                st.session_state.df = st.session_state.df.drop_duplicates(
                    subset=columns_for_dupes if columns_for_dupes else None, 
                    keep=False
                )
                
            after_count = len(st.session_state.df)
            st.success(f"Removed {before_count - after_count} duplicate records.")
    
    # Display the resulting dataframe
    st.subheader("Resulting Dataset")
    st.dataframe(st.session_state.df)
    
    # Show the dataframe shape before and after
    st.subheader("Before vs After")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Before:")
        st.write(f"Total rows: {len(st.session_state.df_original)}")
        original_dups = st.session_state.df_original.duplicated().sum()
        st.write(f"Duplicate rows: {original_dups}")
    
    with col2:
        st.write("After:")
        st.write(f"Total rows: {len(st.session_state.df)}")
        current_dups = st.session_state.df.duplicated().sum()
        st.write(f"Duplicate rows: {current_dups}")

with tab4:
    st.header("Feature Scaling")
    
    st.markdown("""
    ### Why Scale Features?
    
    Feature scaling is crucial for many machine learning algorithms, especially:
    
    - Algorithms that use distance calculations (K-Nearest Neighbors, K-Means)
    - Algorithms with gradient descent optimization (Linear Regression, Neural Networks)
    - Algorithms that use regularization (Ridge, Lasso)
    
    Scaling puts features on a similar scale so that no feature dominates due to its range.
    """)
    
    # Select only numeric columns for scaling
    numeric_cols = st.session_state.df.select_dtypes(include=['number']).columns.tolist()
    
    # Visualize original distributions
    st.subheader("Original Numeric Feature Distributions")
    
    n_cols = 3
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
    
    fig = plt.figure(figsize=(15, 3 * n_rows))
    for i, col in enumerate(numeric_cols):
        ax = fig.add_subplot(n_rows, n_cols, i+1)
        sns.histplot(st.session_state.df[col], kde=True, ax=ax)
        ax.set_title(col)
    plt.tight_layout()
    st.pyplot(fig)
    
    # Scaling options
    st.subheader("Apply Feature Scaling")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        scaling_method = st.radio(
            "Choose a scaling method:",
            ["MinMax Scaling", "Standard Scaling", "Robust Scaling"]
        )
        
        columns_to_scale = st.multiselect(
            "Select numeric columns to scale:",
            numeric_cols,
            default=numeric_cols
        )
    
    with col2:
        st.markdown("""
        ### Scaling Methods Explained
        
        - **MinMax Scaling**: Transforms features to a range between 0 and 1
        - **Standard Scaling**: Transforms features to have mean=0 and standard deviation=1
        - **Robust Scaling**: Scales based on median and quantiles (less sensitive to outliers)
        """)
        
        if st.button("Apply Scaling"):
            if scaling_method == "MinMax Scaling":
                scaler = MinMaxScaler()
            elif scaling_method == "Standard Scaling":
                scaler = StandardScaler()
            else:  # "Robust Scaling"
                scaler = RobustScaler()
                
            scaled_data = scaler.fit_transform(st.session_state.df[columns_to_scale])
            
            # Replace the original columns with scaled values
            for i, col in enumerate(columns_to_scale):
                st.session_state.df[col] = scaled_data[:, i]
                
            st.success(f"Applied {scaling_method} to {len(columns_to_scale)} columns.")
    
    # Display the resulting dataframe
    st.subheader("Resulting Dataset")
    st.dataframe(st.session_state.df)
    
    # Visualize scaled distributions
    st.subheader("Scaled Numeric Feature Distributions")
    
    # Create new figure for scaled distributions
    fig = plt.figure(figsize=(15, 3 * n_rows))
    for i, col in enumerate(columns_to_scale):
        ax = fig.add_subplot(n_rows, n_cols, i+1)
        sns.histplot(st.session_state.df[col], kde=True, ax=ax)
        ax.set_title(col)
    plt.tight_layout()
    st.pyplot(fig)

with tab5:
    st.header("Feature Selection")
    
    st.markdown("""
    ### Why Select Features?
    
    Feature selection helps to:
    
    - Reduce dimensionality and model complexity
    - Improve model performance and interpretability
    - Reduce training time and computational requirements
    - Avoid the "curse of dimensionality"
    
    This demo shows how to drop redundant features or those with high correlation.
    """)
    
    # Show correlation matrix
    numeric_cols = st.session_state.df.select_dtypes(include=['number']).columns.tolist()
    corr_matrix = st.session_state.df[numeric_cols].corr()
    
    st.subheader("Feature Correlation Matrix")
    
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale=px.colors.sequential.Blues
    )
    st.plotly_chart(fig)
    
    # Options for feature selection
    st.subheader("Apply Feature Selection")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        selection_method = st.radio(
            "Choose a feature selection method:",
            ["Drop Selected Features", "Drop Highly Correlated Features"]
        )
        
        if selection_method == "Drop Selected Features":
            features_to_drop = st.multiselect(
                "Select features to drop:",
                st.session_state.df.columns.tolist()
            )
        else:  # "Drop Highly Correlated Features"
            correlation_threshold = st.slider(
                "Correlation threshold (drop one feature from pairs exceeding this):",
                min_value=0.0,
                max_value=1.0,
                value=0.8,
                step=0.05
            )
    
    with col2:
        if selection_method == "Drop Selected Features":
            if st.button("Drop Selected Features"):
                if features_to_drop:
                    st.session_state.df = st.session_state.df.drop(columns=features_to_drop)
                    st.success(f"Dropped {len(features_to_drop)} selected features.")
                else:
                    st.warning("No features selected to drop.")
        else:  # "Drop Highly Correlated Features"
            if st.button("Drop Highly Correlated Features"):
                # Find pairs of highly correlated features
                features_to_drop = set()
                
                for i in range(len(numeric_cols)):
                    for j in range(i+1, len(numeric_cols)):
                        if abs(corr_matrix.iloc[i, j]) > correlation_threshold:
                            # Drop the feature with higher mean correlation with other features
                            corr_i = corr_matrix[numeric_cols[i]].abs().mean()
                            corr_j = corr_matrix[numeric_cols[j]].abs().mean()
                            
                            if corr_i > corr_j:
                                features_to_drop.add(numeric_cols[i])
                            else:
                                features_to_drop.add(numeric_cols[j])
                
                if features_to_drop:
                    st.session_state.df = st.session_state.df.drop(columns=list(features_to_drop))
                    st.success(f"Dropped {len(features_to_drop)} highly correlated features: {', '.join(features_to_drop)}")
                else:
                    st.info("No features found with correlation exceeding the threshold.")
    
    # Display the resulting dataframe
    st.subheader("Resulting Dataset")
    st.dataframe(st.session_state.df)
    
    # Show the dataframe shape before and after
    st.subheader("Before vs After")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Before:")
        st.write(f"Total features: {st.session_state.df_original.shape[1]}")
        st.write(f"Feature list: {', '.join(st.session_state.df_original.columns.tolist())}")
    
    with col2:
        st.write("After:")
        st.write(f"Total features: {st.session_state.df.shape[1]}")
        st.write(f"Feature list: {', '.join(st.session_state.df.columns.tolist())}")
        st.write(f"Features removed: {set(st.session_state.df_original.columns) - set(st.session_state.df.columns)}")

with tab6:
    st.header("Balance Dataset")
    
    st.markdown("""
    ### Why Balance Your Dataset?
    
    Class imbalance is a common problem in machine learning where one class has significantly more examples than other classes.
    
    This can lead to:
    - Models that are biased toward the majority class
    - Poor performance on minority classes
    - Misleading evaluation metrics
    
    Balancing techniques help ensure the model learns equally from all classes.
    """)
    
    # Show class distribution
    if 'target' not in st.session_state.df.columns:
        st.warning("Target column not found in the dataset. Skipping balance demonstration.")
    else:
        # Calculate class distribution
        class_counts = st.session_state.df['target'].value_counts()
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Current Class Distribution")
            
            fig = px.bar(
                x=class_counts.index.astype(str),
                y=class_counts.values,
                labels={'x': 'Target Class', 'y': 'Count'},
                title='Class Distribution',
                color=class_counts.values,
                color_continuous_scale=px.colors.sequential.Viridis
            )
            st.plotly_chart(fig)
            
        with col2:
            # Calculate imbalance metrics
            total_samples = len(st.session_state.df)
            majority_class = class_counts.idxmax()
            majority_count = class_counts.max()
            minority_class = class_counts.idxmin()
            minority_count = class_counts.min()
            imbalance_ratio = majority_count / minority_count
            
            st.subheader("Imbalance Statistics")
            st.write(f"Total samples: {total_samples}")
            st.write(f"Majority class ({majority_class}): {majority_count} samples ({majority_count/total_samples:.1%})")
            st.write(f"Minority class ({minority_class}): {minority_count} samples ({minority_count/total_samples:.1%})")
            st.write(f"Imbalance ratio: {imbalance_ratio:.2f}:1")
        
        # Options for balancing
        st.subheader("Apply Balancing Technique")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            balancing_method = st.radio(
                "Choose a balancing method:",
                ["Random Oversampling", "Random Undersampling", "SMOTE (Synthetic Minority Over-sampling)"]
            )
            
        with col2:
            st.markdown("""
            ### Balancing Methods Explained
            
            - **Random Oversampling**: Randomly duplicate examples from minority classes
            - **Random Undersampling**: Randomly remove examples from majority classes
            - **SMOTE**: Generate synthetic examples for minority classes
            """)
            
            if st.button("Apply Balancing"):
                X = st.session_state.df.drop(columns=['target'])
                y = st.session_state.df['target']
                
                # Handle non-numeric features for SMOTE
                if balancing_method == "SMOTE (Synthetic Minority Over-sampling)":
                    categorical_cols = X.select_dtypes(include=['object', 'category']).columns
                    
                    # Create dummy variables for categorical columns
                    if not categorical_cols.empty:
                        X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
                        st.info(f"Created dummy variables for categorical columns: {', '.join(categorical_cols)}")
                
                # Apply balancing technique
                if balancing_method == "Random Oversampling":
                    sampler = RandomOverSampler(random_state=42)
                    X_resampled, y_resampled = sampler.fit_resample(X, y)
                elif balancing_method == "Random Undersampling":
                    sampler = RandomUnderSampler(random_state=42)
                    X_resampled, y_resampled = sampler.fit_resample(X, y)
                else:  # "SMOTE"
                    try:
                        sampler = SMOTE(random_state=42)
                        X_resampled, y_resampled = sampler.fit_resample(X, y)
                    except ValueError as e:
                        st.error(f"Error applying SMOTE: {e}")
                        st.info("SMOTE requires numeric features. Please convert categorical features first.")
                        X_resampled, y_resampled = X, y
                
                # Recreate the dataframe
                resampled_df = pd.concat([X_resampled, pd.Series(y_resampled, name='target')], axis=1)
                
                # Update the session state
                st.session_state.df = resampled_df
                
                # Show success message
                new_class_counts = st.session_state.df['target'].value_counts()
                st.success(f"Applied {balancing_method}. New class distribution: {dict(new_class_counts)}")
        
        # Display the resulting dataframe
        st.subheader("Resulting Dataset")
        st.dataframe(st.session_state.df)
        
        # Show before and after class distribution
        st.subheader("Before vs After Class Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            original_class_counts = st.session_state.df_original['target'].value_counts()
            fig = px.pie(
                values=original_class_counts.values,
                names=original_class_counts.index.astype(str),
                title='Before Balancing',
                color_discrete_sequence=[aws_colors['teal'], aws_colors['orange']]
            )
            fig.update_traces(textinfo='percent+label')
            st.plotly_chart(fig)
        
        with col2:
            current_class_counts = st.session_state.df['target'].value_counts()
            fig = px.pie(
                values=current_class_counts.values,
                names=current_class_counts.index.astype(str),
                title='After Balancing',
                color_discrete_sequence=[aws_colors['teal'], aws_colors['orange']]
            )
            fig.update_traces(textinfo='percent+label')
            st.plotly_chart(fig)

with tab7:
    st.header("Feature Engineering")
    
    st.markdown("""
    ### Why Engineer Features?
    
    Feature engineering is the process of creating new features from existing ones to:
    
    - Extract more signal from your data
    - Create features that better represent the underlying patterns
    - Improve model performance by providing more relevant information
    - Transform features into a format that better suits the modeling algorithm
    
    Good feature engineering requires domain knowledge and creativity.
    """)
    
    # Show original features
    st.subheader("Original Features")
    st.dataframe(st.session_state.df.head())
    
    # Feature engineering options
    st.subheader("Apply Feature Engineering")
    
    feature_engineering_options = [
        "Create Polynomial Features",
        "Create Interaction Features",
        "Create Ratio Features",
        "Bin Numeric Features",
        "Custom Feature (Mathematical Expression)"
    ]
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        engineering_method = st.selectbox(
            "Choose a feature engineering method:",
            feature_engineering_options
        )
        
        numeric_cols = st.session_state.df.select_dtypes(include=['number']).columns.tolist()
        
        if engineering_method == "Create Polynomial Features":
            degree = st.slider("Polynomial degree:", min_value=2, max_value=3, value=2)
            features_for_poly = st.multiselect(
                "Select numeric features for polynomial expansion:",
                numeric_cols,
                default=numeric_cols[:2] if len(numeric_cols) >= 2 else numeric_cols
            )
            
        elif engineering_method == "Create Interaction Features":
            features_for_interaction = st.multiselect(
                "Select features for interaction terms:",
                numeric_cols,
                default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols
            )
            
        elif engineering_method == "Create Ratio Features":
            numerator = st.selectbox("Select numerator feature:", numeric_cols)
            denominator = st.selectbox(
                "Select denominator feature:", 
                [col for col in numeric_cols if col != numerator],
                index=0 if len(numeric_cols) > 1 else None
            )
            
        elif engineering_method == "Bin Numeric Features":
            feature_to_bin = st.selectbox("Select feature to bin:", numeric_cols)
            num_bins = st.slider("Number of bins:", min_value=2, max_value=10, value=5)
            
        elif engineering_method == "Custom Feature (Mathematical Expression)":
            available_features = ", ".join(numeric_cols)
            st.info(f"Available features: {available_features}")
            custom_expression = st.text_input(
                "Enter a mathematical expression using available features:",
                value="age * income / 1000" if "age" in numeric_cols and "income" in numeric_cols else ""
            )
            new_feature_name = st.text_input("Name for the new feature:", "custom_feature")
    
    with col2:
        if st.button("Create New Features"):
            try:
                if engineering_method == "Create Polynomial Features":
                    if features_for_poly:
                        # Create polynomial features
                        for feature in features_for_poly:
                            for d in range(2, degree + 1):
                                new_feature_name = f"{feature}_power_{d}"
                                st.session_state.df[new_feature_name] = st.session_state.df[feature] ** d
                        
                        st.success(f"Created polynomial features of degree {degree} for {len(features_for_poly)} features.")
                    else:
                        st.warning("No features selected for polynomial expansion.")
                        
                elif engineering_method == "Create Interaction Features":
                    if len(features_for_interaction) >= 2:
                        # Create interaction terms
                        created = 0
                        for i in range(len(features_for_interaction)):
                            for j in range(i+1, len(features_for_interaction)):
                                feat1 = features_for_interaction[i]
                                feat2 = features_for_interaction[j]
                                new_feature_name = f"{feat1}_x_{feat2}"
                                st.session_state.df[new_feature_name] = st.session_state.df[feat1] * st.session_state.df[feat2]
                                created += 1
                                
                        st.success(f"Created {created} interaction features.")
                    else:
                        st.warning("Need at least 2 features to create interaction terms.")
                        
                elif engineering_method == "Create Ratio Features":
                    if numerator and denominator:
                        # Create ratio feature
                        new_feature_name = f"{numerator}_to_{denominator}"
                        # Handle division by zero
                        st.session_state.df[new_feature_name] = st.session_state.df[numerator] / (st.session_state.df[denominator] + 1e-8)
                        st.success(f"Created ratio feature: {new_feature_name}")
                    else:
                        st.warning("Both numerator and denominator must be selected.")
                        
                elif engineering_method == "Bin Numeric Features":
                    if feature_to_bin:
                        # Create binned feature
                        new_feature_name = f"{feature_to_bin}_binned"
                        st.session_state.df[new_feature_name] = pd.qcut(
                            st.session_state.df[feature_to_bin], 
                            q=num_bins, 
                            labels=[f"Bin_{i+1}" for i in range(num_bins)],
                            duplicates='drop'
                        )
                        st.success(f"Created binned feature: {new_feature_name} with {num_bins} bins.")
                    else:
                        st.warning("No feature selected for binning.")
                        
                elif engineering_method == "Custom Feature (Mathematical Expression)":
                    if custom_expression and new_feature_name:
                        # Replace feature names with dataframe references
                        for feature in numeric_cols:
                            custom_expression = custom_expression.replace(
                                feature, 
                                f"st.session_state.df['{feature}']"
                            )
                            
                        # Evaluate the expression
                        st.session_state.df[new_feature_name] = eval(custom_expression)
                        st.success(f"Created custom feature: {new_feature_name}")
                    else:
                        st.warning("Both expression and feature name are required.")
                        
            except Exception as e:
                st.error(f"Error creating features: {str(e)}")
    
    # Display the resulting dataframe
    st.subheader("Resulting Dataset with Engineered Features")
    st.dataframe(st.session_state.df)
    
    # Show feature statistics before and after
    st.subheader("Before vs After")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Before:")
        st.write(f"Number of features: {st.session_state.df_original.shape[1]}")
    
    with col2:
        st.write("After:")
        st.write(f"Number of features: {st.session_state.df.shape[1]}")
        new_features = set(st.session_state.df.columns) - set(st.session_state.df_original.columns)
        st.write(f"New features created: {', '.join(new_features)}")

with tab8:
    st.header("Data Conversion")
    
    st.markdown("""
    ### Why Convert Data Types?
    
    Converting data types is important for:
    
    - Ensuring compatibility with ML algorithms (many require numeric inputs)
    - Reducing memory usage and improving performance
    - Correctly representing the meaning of the data (e.g., categorical vs. continuous)
    - Enabling certain operations or transformations
    
    Common conversions include encoding categorical variables and normalizing text.
    """)
    
    # Show current data types
    st.subheader("Current Data Types")
    
    dtypes_df = pd.DataFrame({
        'Column': st.session_state.df.dtypes.index,
        'Data Type': st.session_state.df.dtypes.values.astype(str)
    })
    st.table(dtypes_df)
    
    # Data conversion options
    st.subheader("Apply Data Conversion")
    
    conversion_options = [
        "Encode Categorical Variables",
        "Convert Numeric Types",
        "Convert to Datetime",
        "Convert to String",
        "Extract from Datetime"
    ]
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        conversion_method = st.selectbox(
            "Choose a conversion method:",
            conversion_options
        )
        
        if conversion_method == "Encode Categorical Variables":
            categorical_cols = st.session_state.df.select_dtypes(include=['object', 'category']).columns.tolist()
            if not categorical_cols:
                st.warning("No categorical columns found in the dataset.")
            else:
                columns_to_encode = st.multiselect(
                    "Select categorical columns to encode:",
                    categorical_cols,
                    default=categorical_cols
                )
                
                encoding_type = st.radio(
                    "Select encoding type:",
                    ["One-Hot Encoding", "Label Encoding"]
                )
                
        elif conversion_method == "Convert Numeric Types":
            numeric_cols = st.session_state.df.select_dtypes(include=['number']).columns.tolist()
            columns_to_convert = st.multiselect(
                "Select columns to convert:",
                st.session_state.df.columns.tolist(),
                default=numeric_cols[:2] if len(numeric_cols) >= 2 else numeric_cols
            )
            
            target_dtype = st.selectbox(
                "Target data type:",
                ["int", "float", "int32", "float32", "int64", "float64"]
            )
            
        elif conversion_method == "Convert to Datetime":
            columns_for_datetime = st.multiselect(
                "Select columns to convert to datetime:",
                st.session_state.df.columns.tolist()
            )
            
            date_format = st.text_input(
                "Date format (optional, leave blank for auto-detection):",
                value=""
            )
            
        elif conversion_method == "Convert to String":
            columns_to_string = st.multiselect(
                "Select columns to convert to string:",
                st.session_state.df.columns.tolist()
            )
            
        elif conversion_method == "Extract from Datetime":
            datetime_cols = st.session_state.df.select_dtypes(include=['datetime']).columns.tolist()
            
            if not datetime_cols:
                st.warning("No datetime columns found in the dataset.")
            else:
                datetime_col = st.selectbox(
                    "Select datetime column:",
                    datetime_cols
                )
                
                extraction_type = st.multiselect(
                    "Select components to extract:",
                    ["Year", "Month", "Day", "Hour", "Minute", "Second", "Day of Week", "Quarter"]
                )
    
    with col2:
        if st.button("Apply Conversion"):
            try:
                if conversion_method == "Encode Categorical Variables":
                    if columns_to_encode:
                        if encoding_type == "One-Hot Encoding":
                            # Apply one-hot encoding
                            encoded_df = pd.get_dummies(
                                st.session_state.df, 
                                columns=columns_to_encode,
                                drop_first=True
                            )
                            st.session_state.df = encoded_df
                            st.success(f"Applied one-hot encoding to {len(columns_to_encode)} columns.")
                            
                        else:  # Label Encoding
                            # Apply label encoding
                            for col in columns_to_encode:
                                st.session_state.df[col] = pd.factorize(st.session_state.df[col])[0]
                            st.success(f"Applied label encoding to {len(columns_to_encode)} columns.")
                    else:
                        st.warning("No columns selected for encoding.")
                        
                elif conversion_method == "Convert Numeric Types":
                    if columns_to_convert:
                        for col in columns_to_convert:
                            try:
                                st.session_state.df[col] = st.session_state.df[col].astype(target_dtype)
                            except:
                                st.warning(f"Could not convert column '{col}' to {target_dtype}.")
                        st.success(f"Converted columns to {target_dtype}.")
                    else:
                        st.warning("No columns selected for conversion.")
                        
                elif conversion_method == "Convert to Datetime":
                    if columns_for_datetime:
                        for col in columns_for_datetime:
                            try:
                                if date_format:
                                    st.session_state.df[col] = pd.to_datetime(st.session_state.df[col], format=date_format)
                                else:
                                    st.session_state.df[col] = pd.to_datetime(st.session_state.df[col])
                            except:
                                st.warning(f"Could not convert column '{col}' to datetime.")
                        st.success(f"Converted {len(columns_for_datetime)} columns to datetime.")
                    else:
                        st.warning("No columns selected for datetime conversion.")
                        
                elif conversion_method == "Convert to String":
                    if columns_to_string:
                        for col in columns_to_string:
                            st.session_state.df[col] = st.session_state.df[col].astype(str)
                        st.success(f"Converted {len(columns_to_string)} columns to string.")
                    else:
                        st.warning("No columns selected for string conversion.")
                        
                elif conversion_method == "Extract from Datetime":
                    if datetime_col and extraction_type:
                        for component in extraction_type:
                            if component == "Year":
                                st.session_state.df[f"{datetime_col}_year"] = st.session_state.df[datetime_col].dt.year
                            elif component == "Month":
                                st.session_state.df[f"{datetime_col}_month"] = st.session_state.df[datetime_col].dt.month
                            elif component == "Day":
                                st.session_state.df[f"{datetime_col}_day"] = st.session_state.df[datetime_col].dt.day
                            elif component == "Hour":
                                st.session_state.df[f"{datetime_col}_hour"] = st.session_state.df[datetime_col].dt.hour
                            elif component == "Minute":
                                st.session_state.df[f"{datetime_col}_minute"] = st.session_state.df[datetime_col].dt.minute
                            elif component == "Second":
                                st.session_state.df[f"{datetime_col}_second"] = st.session_state.df[datetime_col].dt.second
                            elif component == "Day of Week":
                                st.session_state.df[f"{datetime_col}_dayofweek"] = st.session_state.df[datetime_col].dt.dayofweek
                            elif component == "Quarter":
                                st.session_state.df[f"{datetime_col}_quarter"] = st.session_state.df[datetime_col].dt.quarter
                        st.success(f"Extracted {len(extraction_type)} components from {datetime_col}.")
                    else:
                        st.warning("Both datetime column and components to extract must be selected.")
                        
            except Exception as e:
                st.error(f"Error during conversion: {str(e)}")
    
    # Display the resulting dataframe
    st.subheader("Resulting Dataset with Converted Data")
    st.dataframe(st.session_state.df)
    
    # Show data types after conversion
    st.subheader("Updated Data Types")
    
    new_dtypes_df = pd.DataFrame({
        'Column': st.session_state.df.dtypes.index,
        'Data Type': st.session_state.df.dtypes.values.astype(str)
    })
    st.table(new_dtypes_df)
    
    # Show changes
    st.subheader("Changes in Dataset Structure")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Before:")
        st.write(f"Shape: {st.session_state.df_original.shape}")
        st.write(f"Columns: {st.session_state.df_original.shape[1]}")
        st.write(f"Data types: {st.session_state.df_original.dtypes.value_counts().to_dict()}")
    
    with col2:
        st.write("After:")
        st.write(f"Shape: {st.session_state.df.shape}")
        st.write(f"Columns: {st.session_state.df.shape[1]}")
        st.write(f"Data types: {st.session_state.df.dtypes.value_counts().to_dict()}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center">
    <p>© 2025, Amazon Web Services, Inc. or its affiliates. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
# ```

# ## How to Run

# 1. Install the required packages:
# ```bash
# pip install streamlit pandas numpy matplotlib seaborn scikit-learn imbalanced-learn plotly
# ```

# 2. Save the code above in a file named `app.py`

# 3. Run the Streamlit application:
# ```bash
# streamlit run app.py
# ```

# ## Features of the Application

# The application is organized into tabs, each focusing on different data cleaning techniques:

# 1. **Introduction**: Overview of data cleaning and its importance in machine learning
# 2. **Missing Values**: Methods to handle missing values (dropping, imputation)
# 3. **Duplicates**: Identify and remove duplicate records
# 4. **Feature Scaling**: Techniques for scaling numerical features (MinMax, Standard, Robust)
# 5. **Feature Selection**: Methods to select relevant features and drop redundant ones
# 6. **Balance Dataset**: Techniques to handle class imbalance (oversampling, undersampling, SMOTE)
# 7. **Feature Engineering**: Create new features from existing ones
# 8. **Data Conversion**: Convert data types to suit ML algorithms

# Each tab includes:
# - Explanation of why the technique is important
# - Interactive controls to apply the technique to the sample data
# - Visualizations showing before and after effects
# - Results display showing transformed data

# The application uses AWS color scheme and modern UI elements for a professional look. Session management is included in the sidebar, allowing users to reset the session at any time.