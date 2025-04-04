# Landing Page for "Under Construction" Website using Streamlit

import streamlit as st
from PIL import Image
import base64
import time

# Page configuration
st.set_page_config(
    page_title="Coming Soon | Site Under Construction",
    page_icon="🚧",
    layout="wide"
)

# Custom CSS for modern design
def local_css():
    st.markdown("""
    <style>
        /* Overall page styling */
        .main {
            background-color: #f8f9fa;
            font-family: 'Roboto', sans-serif;
        }
        
        /* Container styling */
        .construction-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 2rem;
            text-align: center;
            animation: fadeIn 1.5s ease-in-out;
        }
        
        /* Heading styles */
        h1 {
            color: #2E4057;
            font-size: 3.5rem;
            margin-bottom: 1rem;
            font-weight: 700;
        }
        
        /* Paragraph styles */
        .subtitle {
            color: #5D5C61;
            font-size: 1.5rem;
            margin-bottom: 2rem;
            max-width: 800px;
            line-height: 1.6;
        }
        
        /* Progress bar styling */
        .progress-container {
            width: 70%;
            margin: 2rem auto;
        }
        
        .progress-bar {
            height: 10px;
            background: linear-gradient(to right, #11998e, #38ef7d);
            border-radius: 10px;
            animation: progressAnimation 3s ease-in-out infinite;
        }
        
        /* Button styling */
        .home-button {
            background: linear-gradient(to right, #11998e, #38ef7d);
            color: white;
            border: none;
            padding: 12px 30px;
            font-size: 1.2rem;
            border-radius: 50px;
            cursor: pointer;
            margin-top: 2rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            text-decoration: none;
        }
        
        .home-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(17, 153, 142, 0.3);
        }
        
        /* Image container */
        .image-container {
            max-width: 600px;
            margin: 2rem auto;
        }
        
        /* Animation keyframes */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes progressAnimation {
            0% { width: 10%; }
            50% { width: 70%; }
            100% { width: 10%; }
        }
        
        /* Footer styling */
        .footer {
            text-align: center;
            padding: 1rem;
            color: #777;
            font-size: 0.9rem;
            margin-top: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    local_css()
    
    # Main content
    st.markdown('<div class="construction-container">', unsafe_allow_html=True)
    
    # Animated icon (using Lottie animations as placeholder)
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 2rem;">
        <img src="https://cdn-icons-png.flaticon.com/512/6295/6295417.png" width="150" 
        style="animation: pulse 2s infinite ease-in-out;">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1>🚧 Under Construction 🚧</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="subtitle">
        We're currently working hard to bring you something amazing! 
        Our website is under construction, but we'll be back soon with a brand new look and improved features.
    </p>
    """, unsafe_allow_html=True)
    
    # Progress bar animation
    st.markdown("""
    <div class="progress-container">
        <div class="progress-bar"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display beautiful image
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.image("https://img.freepik.com/free-vector/web-development-programmer-engineering-coding-website-augmented-reality-interface-screens-developer-project-engineer-programming-software-application-design-cartoon-illustration_107791-3863.jpg?w=900", 
                 use_container_width=True)
    
    # Timer for coming soon
    current_time = time.localtime()
    launch_time = time.localtime(time.time() + 7 * 24 * 60 * 60)  # Launch in 7 days
    
    days_remaining = (time.mktime(launch_time) - time.mktime(current_time)) // (24 * 60 * 60)
    
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <h3>Estimated Time Until Launch: {int(days_remaining)} days</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Home button
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem;">
        <a href="/apcr-saa/" class="home-button">Return to Home Page</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact information
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem;">
        <h3>Stay Connected</h3>
        <div style="font-size: 2rem; margin: 1rem 0;">
            <a href="#" style="margin: 0 10px; color: #1DA1F2;"><i class="fab fa-twitter"></i></a>
            <a href="#" style="margin: 0 10px; color: #3b5998;"><i class="fab fa-facebook-f"></i></a>
            <a href="#" style="margin: 0 10px; color: #0e76a8;"><i class="fab fa-linkedin-in"></i></a>
            <a href="#" style="margin: 0 10px; color: #E1306C;"><i class="fab fa-instagram"></i></a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Second illustration
    # col1, col2, col3 = st.columns([1, 2, 1])
    
    # with col2:
    #     st.image("https://img.freepik.com/free-vector/site-stats-concept-illustration_114360-1434.jpg?w=740&t=st=1701615054~exp=1701615654~hmac=b901456a2a5e3b65939c8267663b07d9cc4c1fcf54e1cbe6010843f21a1a06e5", 
    #              use_container_width=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2025 Amazon Web Services. All rights reserved.</p>
        <p>This site is currently under development.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
