import streamlit as st
import random
import pandas as pd
import uuid
import time
from datetime import datetime

# Initialize session state
def initialize_session():
    if 'initialized' not in st.session_state:
        # Generate unique session ID
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
        
        # Initialize game states
        initialize_ml_decision_game()
        initialize_aws_ai_game()
        initialize_ml_types_game()
        
        st.session_state.initialized = True

# Reset individual games
def initialize_ml_decision_game():
    st.session_state.ml_decision_game = {
        'score': 0,
        'questions_asked': 0,
        'game_active': False,
        'current_scenario': None,
        'scenarios': [],
        'answer_submitted': False
    }

def initialize_aws_ai_game():
    st.session_state.aws_ai_game = {
        'score': 0,
        'questions_asked': 0,
        'game_active': False,
        'scenarios': [],
        'difficulty': "Easy (3 options)",
        'answer_submitted': False
    }

def initialize_ml_types_game():
    st.session_state.ml_types_game = {
        'score': 0,
        'questions_asked': 0,
        'game_active': False,
        'scenarios': [],
        'answer_submitted': False
    }

# Reset session state
def reset_session():
    for key in list(st.session_state.keys()):
        if key != 'session_id':
            del st.session_state[key]
    st.session_state.initialized = False
    initialize_session()
    st.rerun()

# Reset individual games
def reset_ml_decision_game():
    initialize_ml_decision_game()
    st.rerun()

def reset_aws_ai_game():
    initialize_aws_ai_game()
    st.rerun()

def reset_ml_types_game():
    initialize_ml_types_game()
    st.rerun()

# Function to handle next question in ML Decision Game
def next_question_ml_decision():
    st.session_state.ml_decision_game['questions_asked'] += 1
    st.session_state.ml_decision_game['answer_submitted'] = False

# Function to handle next question in AWS AI Game
def next_question_aws_ai():
    st.session_state.aws_ai_game['questions_asked'] += 1
    st.session_state.aws_ai_game['answer_submitted'] = False

# Function to handle next question in ML Types Game
def next_question_ml_types():
    st.session_state.ml_types_game['questions_asked'] += 1
    st.session_state.ml_types_game['answer_submitted'] = False

# ML Decision Game
def ml_decision_game():
    st.header("Machine Learning Decision Game")
    st.subheader("Can you decide when to use Machine Learning?")
    
    # Introduction
    st.markdown("""
    In this game, you'll be presented with various business scenarios.
    Your task is to decide whether machine learning would be an appropriate solution
    for each scenario based on the principles of when to use ML:
    
    - Use ML when you can't code it (complex tasks where deterministic solutions don't suffice)
    - Use ML when you can't scale it (replace repetitive tasks needing human-like expertise)
    - Use ML when you have to adapt/personalize
    - Use ML when you can't track it
    
    Test your knowledge and see if you can make the right decisions!
    """)
    
    game_state = st.session_state.ml_decision_game
    
    # Add restart button at the top if game is active
    if game_state['game_active']:
        if st.button("↺ Restart Game", key="restart_ml_decision", type="secondary"):
            reset_ml_decision_game()
    
    # Scenarios data - tuples of (scenario, should_use_ml, explanation)
    scenarios = [
        ("A bank needs to calculate compound interest for customer accounts.", 
         False, 
         "This is a deterministic calculation with clear mathematical formulas. Traditional programming is more appropriate."),
        
        ("An e-commerce website wants to recommend products based on customer browsing history.", 
         True, 
         "Personalization at scale is a perfect ML use case. The patterns are complex and need to adapt to individual users."),
        
        ("A healthcare provider needs to analyze medical images to detect abnormalities.", 
         True, 
         "Image recognition for medical diagnosis is complex and benefits greatly from ML, which can detect patterns humans might miss."),
        
        ("A car manufacturing company wants to automate quality control by detecting defects in parts.", 
         True, 
         "Visual inspection at scale involves complex pattern recognition that's ideal for ML."),
        
        ("A financial institution needs to detect potentially fraudulent transactions in real-time.", 
         True, 
         "Fraud detection involves complex patterns that change over time, making it perfect for ML."),
        
        ("A utility company needs to calculate monthly bills based on meter readings.", 
         False, 
         "This is a straightforward calculation with clear rules that can be handled by traditional programming."),
        
        ("A streaming service wants to suggest content based on what similar users have enjoyed.", 
         True, 
         "Content recommendation systems benefit from ML to identify complex patterns and personalize at scale."),
        
        ("A payroll system needs to calculate employee taxes based on current tax laws.", 
         False, 
         "Tax calculations follow explicit rules and formulas, making traditional programming more appropriate."),
        
        ("A social media platform wants to automatically moderate content to identify harmful posts.", 
         True, 
         "Content moderation involves complex language understanding and contextual awareness, ideal for ML."),
        
        ("A logistics company wants to optimize delivery routes across a city.", 
         True, 
         "Route optimization with multiple variables and constraints can benefit from ML, especially reinforcement learning."),
        
        ("An inventory system needs to track product counts and generate alerts when stock is low.", 
         False, 
         "Simple threshold-based alerting can be handled with traditional programming rules."),
        
        ("A customer support system needs to categorize incoming support tickets by department.", 
         True, 
         "Text classification for routing tickets benefits from ML, especially as the categories and language evolve."),
        
        ("A smart home device needs to understand and respond to voice commands.", 
         True, 
         "Speech recognition is a complex problem that benefits greatly from ML."),
        
        ("An HR system needs to track employee vacation days and enforce company policies.", 
         False, 
         "This involves clear business rules that can be coded directly without ML."),
        
        ("A vehicle needs to navigate autonomously in unpredictable real-world environments.", 
         True, 
         "Autonomous driving involves complex perception and decision-making that's ideal for ML and reinforcement learning.")
    ]
    
    # Start/Restart button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not game_state['game_active']:
            if st.button("Start Game", use_container_width=True, type="primary", key="start_ml_decision"):
                game_state['game_active'] = True
                game_state['score'] = 0
                game_state['questions_asked'] = 0
                game_state['scenarios'] = random.sample(scenarios, len(scenarios))  # Shuffle scenarios
                st.rerun()
    
    # Game logic
    if game_state['game_active']:
        # Display progress
        st.progress(game_state['questions_asked'] / 10)
        st.write(f"Question: {game_state['questions_asked'] + 1}/10")
        st.write(f"Score: {game_state['score']}")
        
        # Get current scenario
        if game_state['questions_asked'] < 10:
            current_scenario = game_state['scenarios'][game_state['questions_asked']]
            
            # Display scenario
            st.markdown(f"### Scenario:")
            st.markdown(f"**{current_scenario[0]}**")
            
            # Get user choice using radio button
            user_choice = st.radio(
                "Should you use Machine Learning for this scenario?",
                ["Use Machine Learning", "Don't Use Machine Learning"],
                key=f"ml_decision_choice_{game_state['questions_asked']}",
                index=None
            )
            
            # Convert user choice to boolean for comparison
            user_choice_bool = (user_choice == "Use Machine Learning")

            # Create columns for the buttons
            col1, col2 = st.columns(2)
            
            with col1:
            # Submit button
                if st.button("Submit Answer", key=f"ml_decision_submit_{game_state['questions_asked']}"):
                    correct = user_choice_bool == current_scenario[1]
                    
                    if correct:
                        st.success("Correct! 🎉")
                        game_state['score'] += 1
                    else:
                        st.error("Incorrect! 😕")
                    
                    # Show explanation
                    st.info(f"Explanation: {current_scenario[2]}")
                    
                    # Set submitted flag
                    game_state['answer_submitted'] = True
            
            with col2:
            # Next question button (only show after submitting)
                if game_state['answer_submitted']:
                    if st.button("Next Question", key=f"ml_decision_next_{game_state['questions_asked']}"):
                        next_question_ml_decision()
                        st.rerun()
        else:
            # Game over
            final_score = game_state['score']
            
            st.markdown(f"## Game Over!")
            st.markdown(f"### Your final score: {final_score}/10")
            
            # Provide feedback based on score
            if final_score == 10:
                st.balloons()
                st.success("Perfect score! You're an ML decision-making expert!")
            elif final_score >= 8:
                st.success("Great job! You have a strong understanding of when to apply ML!")
            elif final_score >= 6:
                st.info("Good effort! You understand the basics but might want to review some concepts.")
            else:
                st.warning("You might want to review the key principles of when to use ML vs traditional programming.")
            
            # Key takeaways
            st.markdown("""
            ### Key Takeaways:
            
            Remember to use Machine Learning when:
            - Tasks are too complex for explicit programming (image recognition, natural language understanding)
            - You need to scale human-like expertise (recommendations, content moderation)
            - Systems need to adapt and personalize (user preferences, dynamic environments)
            - Problems involve unpredictable environments or complex patterns (autonomous vehicles, fraud detection)
            
            Traditional programming is better when:
            - Problems have clear, unchanging rules (calculations, rule-based workflows)
            - Transparency and auditability are critical (financial calculations, compliance)
            - You have limited data
            - The solution requires perfect accuracy
            """)
            
            # Play Again button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Play Again", key="ml_decision_play_again", use_container_width=True):
                    reset_ml_decision_game()

# AWS AI Service Matchmaker Game
def aws_ai_game():
    st.header("AWS AI Service Matchmaker")
    st.subheader("Can you match the scenario to the correct AWS AI service?")
    
    # Introduction
    st.markdown("""
    In this game, you'll be presented with various business scenarios where AWS AI services can provide solutions.
    Your task is to select the most appropriate AWS AI service for each scenario.
    
    Test your knowledge of AWS AI capabilities and see how well you can match services to use cases!
    """)
    
    game_state = st.session_state.aws_ai_game
    
    # Add restart button at the top if game is active
    if game_state['game_active']:
        if st.button("↺ Restart Game", key="restart_aws_ai", type="secondary"):
            reset_aws_ai_game()
    
    # AWS AI Services scenarios - (scenario, correct_service, explanation, incorrect_options)
    scenarios = [
        (
            "A retail company wants to provide personalized product recommendations to customers based on their browsing history and purchase patterns.",
            "Amazon Personalize",
            "Amazon Personalize provides real-time personalization and recommendations using the same technology used by Amazon.com. It's ideal for product recommendations based on user behavior.",
            ["Amazon Rekognition", "Amazon Comprehend", "Amazon Kendra"]
        ),
        (
            "A media company needs to automatically identify celebrities in their video content to improve searchability.",
            "Amazon Rekognition",
            "Amazon Rekognition can analyze images and videos to identify objects, people, text, scenes, and activities, including celebrity recognition.",
            ["Amazon Textract", "Amazon Comprehend", "Amazon Kendra"]
        ),
        (
            "A financial institution wants to automatically extract information from scanned loan application documents.",
            "Amazon Textract",
            "Amazon Textract is designed to extract text and data from scanned documents. It goes beyond simple OCR to identify form fields and tables.",
            ["Amazon Rekognition", "Amazon Comprehend", "Amazon Transcribe"]
        ),
        (
            "A company wants to implement a search function for their internal knowledge base that can understand natural language queries.",
            "Amazon Kendra",
            "Amazon Kendra is an intelligent search service that uses natural language processing to return specific answers to questions, making it ideal for knowledge bases.",
            ["Amazon Comprehend", "Amazon Lex", "Amazon Personalize"]
        ),
        (
            "A healthcare provider wants to analyze patient records to identify key medical information and classify documents.",
            "Amazon Comprehend Medical",
            "Amazon Comprehend Medical is specifically designed to extract information from unstructured medical text using NLP.",
            ["Amazon Rekognition", "Amazon Textract", "Amazon Kendra"]
        ),
        (
            "A streaming service wants to automatically generate subtitles for their video content in multiple languages.",
            "Amazon Transcribe",
            "Amazon Transcribe automatically converts speech to text and can be combined with Amazon Translate for multilingual subtitling.",
            ["Amazon Polly", "Amazon Rekognition", "Amazon Textract"]
        ),
        (
            "An e-commerce company wants to detect potentially fraudulent activities in their online transactions.",
            "Amazon Fraud Detector",
            "Amazon Fraud Detector is specifically designed to identify potentially fraudulent online activities using machine learning.",
            ["Amazon Comprehend", "Amazon Macie", "Amazon Rekognition"]
        ),
        (
            "A company wants to build a chatbot that can communicate with customers and handle basic service requests.",
            "Amazon Lex",
            "Amazon Lex provides the advanced deep learning capabilities of automatic speech recognition (ASR) and natural language understanding (NLU) to build conversational interfaces like chatbots.",
            ["Amazon Polly", "Amazon Comprehend", "Amazon Connect"]
        ),
        (
            "A company needs to create realistic voice narrations for their training videos from text scripts.",
            "Amazon Polly",
            "Amazon Polly turns text into lifelike speech, allowing you to create applications that talk and build entirely new categories of speech-enabled products.",
            ["Amazon Transcribe", "Amazon Lex", "Amazon Connect"]
        ),
        (
            "A news organization wants to analyze articles to identify key phrases, sentiment, and entities mentioned.",
            "Amazon Comprehend",
            "Amazon Comprehend uses NLP to find insights and relationships in text, including sentiment analysis, entity recognition, and key phrase extraction.",
            ["Amazon Textract", "Amazon Kendra", "Amazon Rekognition"]
        ),
        (
            "A manufacturing company wants to implement predictive maintenance by analyzing data from their equipment sensors.",
            "Amazon Lookout for Equipment",
            "Amazon Lookout for Equipment analyzes sensor data to detect abnormal equipment behavior, helping identify potential failures before they occur.",
            ["Amazon Forecast", "Amazon Rekognition", "Amazon SageMaker"]
        ),
        (
            "A retailer wants to forecast product demand for the upcoming holiday season based on historical sales data.",
            "Amazon Forecast",
            "Amazon Forecast uses machine learning to deliver highly accurate forecasts based on historical time-series data.",
            ["Amazon Personalize", "Amazon Comprehend", "Amazon Lookout for Metrics"]
        ),
        (
            "A social media company wants to automatically moderate user-uploaded images and videos to detect inappropriate content.",
            "Amazon Rekognition",
            "Amazon Rekognition includes content moderation capabilities to detect inappropriate, unwanted, or offensive images and videos.",
            ["Amazon Comprehend", "Amazon Macie", "Amazon Textract"]
        ),
        (
            "A company needs to analyze customer support calls to identify common issues and customer sentiment.",
            "Amazon Transcribe Call Analytics",
            "Amazon Transcribe Call Analytics combines automatic speech recognition with natural language processing to transcribe and analyze customer service calls.",
            ["Amazon Connect", "Amazon Comprehend", "Amazon Lex"]
        ),
        (
            "A developer team wants to automatically review their code for quality issues and identify potential optimizations.",
            "Amazon CodeGuru",
            "Amazon CodeGuru provides intelligent recommendations to improve code quality and identify the most expensive lines of code in applications.",
            ["AWS Lambda", "Amazon Q Developer", "Amazon SageMaker"]
        )
    ]
    
    # Start/Restart button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not game_state['game_active']:
            difficulty = "Easy (3 options)"
            if st.button("Start Game", use_container_width=True, type="primary", key="start_aws_ai"):
                game_state['game_active'] = True
                game_state['score'] = 0
                game_state['questions_asked'] = 0
                game_state['difficulty'] = difficulty
                game_state['scenarios'] = random.sample(scenarios, 10)  # Pick 10 random scenarios
                st.rerun()
    
    # Game logic
    if game_state['game_active']:
        # Display progress
        st.progress(game_state['questions_asked'] / 10)
        st.write(f"Question: {game_state['questions_asked'] + 1}/10")
        st.write(f"Score: {game_state['score']}")
        
        # Get current scenario
        if game_state['questions_asked'] < 10:
            current_scenario = game_state['scenarios'][game_state['questions_asked']]
            scenario_text = current_scenario[0]
            correct_answer = current_scenario[1]
            explanation = current_scenario[2]
            incorrect_options = current_scenario[3]
            
            # Create answer options based on difficulty
            if game_state['difficulty'] == "Easy (3 options)":
                num_options = 4
            elif game_state['difficulty'] == "Medium (5 options)":
                num_options = 5
            else:  # Hard
                num_options = 7
                
            # Get additional incorrect options if needed
            all_services = list(set([s[1] for s in scenarios]))  # All possible services
            additional_options = [s for s in all_services if s != correct_answer and s not in incorrect_options]
            
            # Select options based on difficulty
            needed_incorrect = min(num_options - 1, len(incorrect_options))
            selected_incorrect = incorrect_options[:needed_incorrect]
            
            # If we need more options for higher difficulties
            if num_options - 1 > len(selected_incorrect):
                more_needed = num_options - 1 - len(selected_incorrect)
                if more_needed > 0 and additional_options:
                    selected_incorrect += random.sample(additional_options, min(more_needed, len(additional_options)))
            
            # Create final options list and shuffle
            options = [correct_answer] + selected_incorrect
            # random.shuffle(options)
            
            # Display scenario
            st.markdown("### Scenario:")
            st.markdown(f"**{scenario_text}**")
            
            # Display options
            st.markdown("##### Which AWS AI service is most appropriate for this scenario?")
            
            # Use radio button for service selection
            user_answer = st.radio("Select the best AWS service:", 
                                 options, 
                                 key=f"aws_ai_answer_{game_state['questions_asked']}",
                                 index=None)

            # Create columns for the buttons
            col1, col2 = st.columns(2)
            
            # Submit button in first column
            with col1:
                # Check answer button
                if st.button("Submit Answer", key=f"aws_ai_submit_{game_state['questions_asked']}"):
                    if user_answer == correct_answer:
                        st.success("✅ Correct! That's the right service for this scenario.")
                        game_state['score'] += 1
                    else:
                        st.error(f"❌ Incorrect. The right service is {correct_answer}.")
                    
                    # Show explanation
                    st.info(f"**Explanation**: {explanation}")
                    
                    # Set submitted flag
                    game_state['answer_submitted'] = True

            with col2:
                # Next question button
                if game_state['answer_submitted']:
                    if st.button("Next Question", key=f"aws_ai_next_{game_state['questions_asked']}"):
                        next_question_aws_ai()
                        st.rerun()
        else:
            # Game over
            final_score = game_state['score']
            
            st.markdown(f"## Game Over!")
            st.markdown(f"### Your final score: {final_score}/10")
            
            # Provide feedback based on score
            if final_score == 10:
                st.balloons()
                st.success("Perfect score! You're an AWS AI services expert!")
            elif final_score >= 8:
                st.success("Great job! You have a strong understanding of AWS AI services!")
            elif final_score >= 6:
                st.info("Good effort! You understand the basics but might want to review some AWS AI services.")
            else:
                st.warning("You might want to review the AWS AI services and their use cases.")
            
            # Display a summary table
            st.markdown("### AWS AI Services Summary")
            
            service_data = [
                {"Service": "Amazon Rekognition", "Use Case": "Image and video analysis, facial recognition, celebrity identification, content moderation"},
                {"Service": "Amazon Textract", "Use Case": "Extract text, data, and tables from scanned documents"},
                {"Service": "Amazon Comprehend", "Use Case": "Natural language processing to extract insights and relationships in text"},
                {"Service": "Amazon Comprehend Medical", "Use Case": "Extract information from unstructured medical text"},
                {"Service": "Amazon Transcribe", "Use Case": "Convert speech to text"},
                {"Service": "Amazon Polly", "Use Case": "Convert text to lifelike speech"},
                {"Service": "Amazon Translate", "Use Case": "Translate text between languages"},
                {"Service": "Amazon Lex", "Use Case": "Build conversational interfaces like chatbots"},
                {"Service": "Amazon Personalize", "Use Case": "Create real-time personalized recommendations"},
                {"Service": "Amazon Forecast", "Use Case": "Time-series forecasting service"},
                {"Service": "Amazon Kendra", "Use Case": "Intelligent search service with natural language understanding"},
                {"Service": "Amazon Fraud Detector", "Use Case": "Identify potentially fraudulent online activities"},
                {"Service": "Amazon CodeGuru", "Use Case": "Automated code reviews and application performance recommendations"},
                {"Service": "Amazon Lookout for Equipment", "Use Case": "Detect abnormal equipment behavior from sensor data"}
            ]
            
            df = pd.DataFrame(service_data)
            st.table(df)
            
            # Play Again button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Play Again", key="aws_ai_play_again", use_container_width=True):
                    reset_aws_ai_game()

# Machine Learning Types Game
def ml_types_game():
    st.header("Machine Learning Types Matcher")
    st.subheader("Can you identify the correct machine learning approach for each scenario?")
    
    # Introduction
    st.markdown("""
    In this game, you'll be presented with various scenarios where machine learning can be applied.
    Your task is to identify which type of machine learning would be most appropriate:
    
    - **Supervised Learning**: Training with labeled data to make predictions or classifications
    - **Unsupervised Learning**: Finding patterns in unlabeled data
    - **Reinforcement Learning**: Learning through trial and error with rewards and penalties
    - **Self-Supervised Learning**: Creating labels from the data itself for pretraining
    
    Test your knowledge of machine learning fundamentals!
    """)
    
    game_state = st.session_state.ml_types_game
    
    # Add restart button at the top if game is active
    if game_state['game_active']:
        if st.button("↺ Restart Game", key="restart_ml_types", type="secondary"):
            reset_ml_types_game()
    
    # ML Type scenarios - (scenario, correct_type, explanation)
    scenarios = [
        (
            "A company wants to predict future sales based on historical sales data where each data point includes the date, marketing spend, and resulting sales numbers.",
            "Supervised Learning",
            "This is a supervised learning problem because we have labeled data (historical sales with known outcomes) and need to predict a specific target value (future sales)."
        ),
        (
            "An e-commerce website wants to group their customers into distinct segments based on purchasing behaviors without any predefined categories.",
            "Unsupervised Learning",
            "This is an unsupervised learning problem (specifically clustering) because we're looking for patterns and segments in the data without having predefined labels."
        ),
        (
            "A company is developing an AI system for a self-driving car that needs to learn optimal driving behaviors through interactions with a simulated environment.",
            "Reinforcement Learning",
            "This is a reinforcement learning problem because the system learns by interacting with an environment (driving conditions), receiving feedback (rewards for safe driving, penalties for accidents), and adjusting behavior accordingly."
        ),
        (
            "A research team wants to train a language model by having it predict the next word in sentences from a large corpus of text.",
            "Self-Supervised Learning",
            "This is a self-supervised learning problem because the model creates its own supervision signal from the data (predicting masked or future words) without requiring external labels."
        ),
        (
            "A medical team has thousands of labeled X-ray images categorized as 'pneumonia' or 'no pneumonia' and wants to build a model to classify new X-rays.",
            "Supervised Learning",
            "This is a supervised learning problem (specifically binary classification) because we have labeled training data (X-rays with known diagnoses) and need to classify new images into one of two categories."
        ),
        (
            "A data scientist wants to detect unusual patterns in network traffic that might indicate security breaches without knowing in advance what those patterns look like.",
            "Unsupervised Learning",
            "This is an unsupervised learning problem (specifically anomaly detection) because we're looking for unusual patterns without having labeled examples of what constitutes 'normal' vs 'abnormal'."
        ),
        (
            "A large language model is being trained by masking random words in sentences and having the model predict what those words should be.",
            "Self-Supervised Learning",
            "This is self-supervised learning because the task creates its own labels from the input data by masking words and using the original unmasked text as the supervision signal."
        ),
        (
            "A robotics engineer is developing an algorithm to teach a robot arm to pick up and sort objects of different shapes and weights through trial and error.",
            "Reinforcement Learning",
            "This is a reinforcement learning problem because the robot learns optimal behaviors through trial and error, receiving rewards for successful grasps and penalties for drops or mistakes."
        ),
        (
            "A financial services company has customer transaction histories labeled as 'fraudulent' or 'legitimate' and wants to build a model to detect fraud in new transactions.",
            "Supervised Learning",
            "This is a supervised learning classification problem because we have labeled examples of fraudulent and legitimate transactions to train a model that can classify new transactions."
        ),
        (
            "A streaming service wants to group movies into genres based on their content, dialogue, and visual style without using predefined genre categories.",
            "Unsupervised Learning",
            "This is an unsupervised learning clustering problem because we're looking to identify natural groupings in the data without predefined labels."
        ),
        (
            "An AI researcher is developing a system where an agent learns to play chess by playing against itself and improving based on game outcomes.",
            "Reinforcement Learning",
            "This is a reinforcement learning problem because the agent learns optimal strategies through trial and error gameplay, receiving rewards for winning and penalties for losing."
        ),
        (
            "A company wants to build a recommendation system based on past user ratings of products to predict what ratings users would give to products they haven't seen yet.",
            "Supervised Learning",
            "This is a supervised learning problem because we have labeled data (known user ratings) that we use to predict unknown values (ratings for unseen products)."
        ),
        (
            "A video platform is training an AI system by having it predict what happens next in video sequences.",
            "Self-Supervised Learning",
            "This is self-supervised learning because the model creates its own supervision signal from the data (using earlier frames to predict later frames) without requiring external labels."
        ),
        (
            "A data analyst has a large dataset of customer purchase records and wants to discover underlying patterns without looking for anything specific.",
            "Unsupervised Learning",
            "This is an unsupervised learning problem because we're exploring data to find patterns and structures without having labeled examples or specific target variables."
        ),
        (
            "A conversational AI is being trained by predicting masked portions of dialogue based on surrounding context from millions of conversations.",
            "Self-Supervised Learning",
            "This is self-supervised learning because the model creates supervision signals from the raw data itself by predicting masked content based on context."
        ),
        (
            "A gaming company is developing an AI that learns to play a new video game by maximizing its score through repeated gameplay attempts.",
            "Reinforcement Learning",
            "This is a reinforcement learning problem because the AI learns optimal strategies through trial and error, receiving rewards (points in the game) and adjusting behavior accordingly."
        ),
        (
            "An image analysis tool is being trained by having it predict the original color of black and white images.",
            "Self-Supervised Learning",
            "This is self-supervised learning because the model creates its own supervision (the original color) from the input data (grayscale version) without external labeling."
        ),
        (
            "A grocery chain wants to predict daily sales for each product category based on historical sales data that includes day of week, promotions, and holidays.",
            "Supervised Learning",
            "This is a supervised learning problem (specifically regression) because we have labeled historical data (past sales figures) and need to predict a numerical target value."
        ),
        (
            "A research team wants to identify potential new drug compounds by having an AI generate molecular structures that maximize certain biological properties.",
            "Reinforcement Learning",
            "This is a reinforcement learning problem because the model learns to generate structures that maximize a reward function (biological effectiveness) through an iterative process of generation and evaluation."
        ),
        (
            "A social network wants to analyze user connections to identify communities of closely connected individuals without predefined groupings.",
            "Unsupervised Learning",
            "This is an unsupervised learning problem (specifically community detection) because we're looking for natural groupings in network data without labeled examples."
        )
    ]
    
    # Start/Restart button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not game_state['game_active']:
            if st.button("Start Game", use_container_width=True, type="primary", key="start_ml_types"):
                game_state['game_active'] = True
                game_state['score'] = 0
                game_state['questions_asked'] = 0
                game_state['scenarios'] = random.sample(scenarios, 10)  # Pick 10 random scenarios
                st.rerun()
    
    # Game logic
    if game_state['game_active']:
        # Display progress
        st.progress(game_state['questions_asked'] / 10)
        st.write(f"Question: {game_state['questions_asked'] + 1}/10")
        st.write(f"Score: {game_state['score']}")
        
        # Get current scenario
        if game_state['questions_asked'] < 10:
            current_scenario = game_state['scenarios'][game_state['questions_asked']]
            scenario_text = current_scenario[0]
            correct_answer = current_scenario[1]
            explanation = current_scenario[2]
            
            # ML types options
            ml_types = ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Self-Supervised Learning"]
            
            # Display scenario
            st.markdown("### Scenario:")
            st.markdown(f"**{scenario_text}**")
            
            # Display options
            st.markdown("##### What type of machine learning would be most appropriate for this scenario?")
            
            # Use radio button for ML type selection
            user_answer = st.radio("Select the best approach:", 
                                 ml_types, 
                                 key=f"ml_types_answer_{game_state['questions_asked']}",
                                 index=None)

            # Create columns for the buttons
            col1, col2 = st.columns(2)
            
            # Submit button in first column
            with col1:
                if st.button("Submit Answer", key=f"ml_types_submit_{game_state['questions_asked']}"):
                    if user_answer == correct_answer:
                        st.success("✅ Correct! That's the right machine learning type for this scenario.")
                        game_state['score'] += 1
                    else:
                        st.error(f"❌ Incorrect. The right approach is {correct_answer}.")
                    
                    # Show explanation
                    st.info(f"**Explanation**: {explanation}")
                    game_state['answer_submitted'] = True

            # Next question button in second column
            with col2:
                if game_state['answer_submitted']:
                    if st.button("Next Question", key=f"ml_types_next_{game_state['questions_asked']}"):
                        next_question_ml_types()
                        st.rerun()
        else:
            # Game over
            final_score = game_state['score']
            
            st.markdown(f"## Game Over!")
            st.markdown(f"### Your final score: {final_score}/10")
            
            # Provide feedback based on score
            if final_score == 10:
                st.balloons()
                st.success("Perfect score! You're a machine learning expert!")
            elif final_score >= 8:
                st.success("Great job! You have a strong understanding of machine learning types!")
            elif final_score >= 6:
                st.info("Good effort! You understand the basics but might want to review some concepts.")
            else:
                st.warning("You might want to review the different types of machine learning approaches.")
            
            # Display a summary table
            st.markdown("### Machine Learning Types Summary")
            
            ml_types_data = [
                {"Type": "Supervised Learning", "Description": "Learning from labeled data to make predictions or classifications", "Examples": "Image classification, speech recognition, regression problems, spam detection"},
                {"Type": "Unsupervised Learning", "Description": "Finding patterns or structures in unlabeled data", "Examples": "Clustering, anomaly detection, dimensionality reduction, recommendation systems"},
                {"Type": "Reinforcement Learning", "Description": "Learning optimal behaviors through trial and error with rewards and penalties", "Examples": "Game playing, robotics, autonomous driving, resource management"},
                {"Type": "Self-Supervised Learning", "Description": "Creating supervision signals from the data itself for pretraining", "Examples": "Language models predicting masked words, contrastive learning, pretext tasks"},
            ]
            
            df = pd.DataFrame(ml_types_data)
            st.table(df)
            
            # Key characteristics
            st.markdown("### Key Characteristics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Supervised Learning:**")
                st.markdown("- Requires labeled training data")
                st.markdown("- Has a clear target variable to predict")
                st.markdown("- Includes classification and regression")
                st.markdown("- Evaluation is straightforward with test data")
                
                st.markdown("**Unsupervised Learning:**")
                st.markdown("- Uses unlabeled data")
                st.markdown("- Finds hidden patterns or structures")
                st.markdown("- Includes clustering and dimensionality reduction")
                st.markdown("- Evaluation can be more subjective")
            
            with col2:
                st.markdown("**Reinforcement Learning:**")
                st.markdown("- Agent interacts with environment")
                st.markdown("- Learns through trial and error")
                st.markdown("- Receives rewards and penalties")
                st.markdown("- Optimizes for long-term reward")
                
                st.markdown("**Self-Supervised Learning:**")
                st.markdown("- Creates its own supervision from data")
                st.markdown("- Often used for pretraining large models")
                st.markdown("- Can learn from massive unlabeled datasets")
                st.markdown("- Includes techniques like masked language modeling")
            
            # Play Again button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Play Again", key="ml_types_play_again", use_container_width=True):
                    reset_ml_types_game()

# Main application
def main():
    # Set page configuration
    st.set_page_config(
        page_title="AI Learning Games",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Apply custom CSS for AWS style
    st.markdown("""
        <style>
        .stApp {
            background-color: #FFFFFF;
        }
        .stButton button {
            background-color: #FF9900;
            color: white;
        }
        .stProgress .st-ey {
            background-color: #FF9900;
        }
        .stSuccess {
            background-color: #D5EEDB;
            color: #037B49;
        }
        .stError {
            background-color: #FFE0E4;
            color: #CF1124;
        }
        .stInfo {
            background-color: #EFF8FF;
            color: #006DEE;
        }
        footer {visibility: hidden;}
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #F8F9FA;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 15px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .stTabs [data-baseweb="tab"] {
            height: 60px;
            white-space: pre-wrap;
            border-radius: 6px;
            font-weight: 600;
            background-color: #FFFFFF;
            color: #232F3E;
            border: 1px solid #E9ECEF;
            padding: 5px 15px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #FF9900 !important;
            color: #FFFFFF !important;
            border: 1px solid #FF9900 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session()
    
    # Sidebar
    with st.sidebar:
        st.subheader("Session Management")
        
        # Reset session button
        if st.button("Reset All Games", type="primary"):
            reset_session()
            
        # About this App (collapsed by default)
        with st.expander("About this App"):
            st.write("""
                This application offers three interactive educational games to help you learn about AI and machine learning concepts:
                
                1. **ML Decision Game**: Learn when to use machine learning vs. traditional programming
                2. **AWS AI Service Matchmaker**: Match business scenarios to the appropriate AWS AI service
                3. **ML Types Matcher**: Identify the correct type of machine learning for different scenarios
                
                Play these games to test and improve your knowledge of AI concepts and applications!
            """)
        
        # Show session ID
        st.caption(f"Session ID: {st.session_state.session_id[:8]}...")
    
    # Main content area with tabs
    tab1, tab2, tab3 = st.tabs([
        "🤔 ML Decision Game", 
        "🧩 AWS AI Service Matchmaker",
        "🔍 ML Types Matcher"
    ])
    
    with tab1:
        ml_decision_game()
    
    with tab2:
        aws_ai_game()
    
    with tab3:
        ml_types_game()
    
    # Footer
    st.markdown("""
        <div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; background-color: white;'>
        <p style='color: #666; font-size: 12px;'>© 2025, Amazon Web Services, Inc. or its affiliates. All rights reserved.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
