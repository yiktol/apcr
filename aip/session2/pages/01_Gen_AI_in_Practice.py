# GenAI Prompt Explorer - Enhanced UI and Code Optimization

import streamlit as st
import boto3
import json
import time
from typing import Dict, Any, List, Tuple
import uuid
import utils.helpers as helpers

# Page configuration with improved metadata
st.set_page_config(
    page_title="GenAI Prompt Explorer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    /* Base styles */
    body {
        background-color: #f9fafb;
        color: #111827;
    }
    
    /* Header styling */
    .main-header {
        color: #2563eb;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .sub-header {
        color: #4b5563;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .card {
        background-color: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        margin-bottom: 20px;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        font-weight: 600;
        border-radius: 6px 6px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2563eb !important;
        color: white !important;
    }
    
    /* Prompt area styling */
    .prompt-area {
        border-left: 4px solid #2563eb;
        background-color: #f3f4f6;
        padding: 15px;
        border-radius: 4px;
    }
    
    /* Response area */
    .response-area {
        border-left: 4px solid #10b981;
        background-color: #ecfdf5;
        padding: 15px;
        border-radius: 4px;
        margin-top: 20px;
    }
    
    /* Container border */
    [data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] > div:first-child > div[data-testid="stVerticalBlock"] > div.element-container > div.stTabs > div[data-baseweb="tab-panel"] > div > div[data-testid="stVerticalBlock"] > div.element-container:first-child > div[data-testid="stVerticalBlock"] {
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        padding: 20px;
    }
    
    /* Button styling */
    button[data-testid="baseButton-primary"] {
        background-color: #2563eb;
        border-radius: 6px;
        transition: all 0.3s ease;
    }
    
    button[data-testid="baseButton-primary"]:hover {
        background-color: #1d4ed8;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Model selector styling */
    div[data-testid="stSelectbox"] {
        margin-bottom: 10px;
    }
    
    /* Info card */
    .info-card {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    
    /* Tag styling */
    .tag {
        display: inline-block;
        padding: 4px 8px;
        background-color: #e0f2fe;
        color: #0284c7;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 5px;
    }
    
    /* Parameter card */
    .param-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 12px;
        margin-bottom: 10px;
    }
    
    .param-title {
        font-weight: 600;
        color: #475569;
        margin-bottom: 5px;
    }
    
    /* History item */
    .history-item {
        padding: 10px;
        border-bottom: 1px solid #e5e7eb;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    
    .history-item:hover {
        background-color: #f3f4f6;
    }
    
    /* Model badge */
    .model-badge {
        display: inline-block;
        padding: 4px 8px;
        background-color: #f3f4f6;
        color: #4b5563;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-bottom: 10px;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    .loading {
        animation: pulse 1.5s infinite;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
    }
    
    /* Category pill */
    .category {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 500;
        margin-right: 5px;
        margin-bottom: 5px;
    }
    
    .category-summarization {
        background-color: #fee2e2;
        color: #b91c1c;
    }
    
    .category-extraction {
        background-color: #e0f2fe;
        color: #0369a1;
    }
    
    .category-translation {
        background-color: #f3e8ff;
        color: #7e22ce;
    }
    
    .category-content {
        background-color: #d1fae5;
        color: #047857;
    }
    
    .category-redaction {
        background-color: #fef3c7;
        color: #92400e;
    }
    
    .category-code {
        background-color: #dbeafe;
        color: #1d4ed8;
    }
    
    .category-harmful {
        background-color: #ffe4e6;
        color: #be123c;
    }
    
    .category-sentiment {
        background-color: #e0e7ff;
        color: #4338ca;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'response_history' not in st.session_state:
    st.session_state.response_history = []
if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = 0
if 'last_provider' not in st.session_state:
    st.session_state.last_provider = None
if 'last_model' not in st.session_state:
    st.session_state.last_model = None
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]  # Create a session identifier

# Define prompt categories and their styles
categories = {
    "Summarization": "summarization",
    "Extraction": "extraction",
    "Translation": "translation",
    "Content Generation": "content",
    "Redaction": "redaction",
    "Code Generation": "code",
    "Harmful Content Detection": "harmful",
    "Sentiment Analysis": "sentiment"
}

# Prompt definitions with additional metadata
prompt1 = """The Rise of Quantum Computing and Its Implications for Cybersecurity

In recent years, quantum computing has emerged as one of the most promising and potentially disruptive technologies of the 21st century. Unlike classical computers that use bits to represent either 0 or 1, quantum computers leverage quantum bits or "qubits" that can exist in multiple states simultaneously due to the principle of superposition. This fundamental difference gives quantum computers the theoretical ability to solve certain problems exponentially faster than even the most powerful classical supercomputers.

The field of quantum computing traces back to 1981, when physicist Richard Feynman proposed the concept of quantum simulators. However, practical development accelerated in the 1990s with Peter Shor's algorithm demonstrating that quantum computers could efficiently factor large numbers—a capability that directly threatens modern cryptographic systems. By the early 2000s, companies like IBM, Google, and D-Wave began investing heavily in quantum hardware, leading to significant breakthroughs over the past decade.

Today's quantum computers still face substantial challenges. Quantum coherence—maintaining the delicate quantum state of qubits—remains difficult, requiring temperatures near absolute zero and elaborate isolation from environmental noise. Current quantum systems typically contain between 50-100 qubits, with error rates that limit their practical applications. Despite these limitations, in 2019, Google claimed to have achieved "quantum supremacy" by performing a specific calculation that would be infeasible for classical computers, though this claim has been contested.

The implications of mature quantum computing for cybersecurity are profound. Many of today's encryption methods, particularly RSA and ECC (Elliptic Curve Cryptography), rely on mathematical problems that classical computers cannot solve efficiently but that quantum computers could potentially crack using Shor's algorithm. This vulnerability affects everything from secure websites and financial transactions to government communications and blockchain technologies. Experts estimate that a quantum computer with 4,000 stable, logical qubits could break RSA-2048 encryption in a matter of hours.

In response to this looming "crypto-apocalypse," researchers are developing quantum-resistant cryptographic algorithms, collectively known as post-quantum cryptography (PQC). These new approaches use mathematical problems believed to be difficult even for quantum computers. In 2016, the National Institute of Standards and Technology (NIST) initiated a process to standardize post-quantum cryptographic algorithms, with final standards expected by 2024. Major technology companies and governments worldwide are now preparing for a complex transition to these new cryptographic standards.

Beyond its threat to existing cryptography, quantum computing also promises revolutionary advances in multiple fields. In drug discovery and materials science, quantum computers could simulate molecular interactions with unprecedented accuracy, potentially accelerating the development of new medications and materials. In optimization problems—from supply chain logistics to financial portfolio management—quantum algorithms might find superior solutions to problems that have countless possible combinations. Quantum machine learning algorithms could potentially analyze patterns in data that remain invisible to classical approaches.

Despite the hype surrounding quantum computing, experts caution that many proposed applications remain speculative. The technology is still in its early stages, comparable perhaps to classical computers in the 1950s. The path to fault-tolerant, general-purpose quantum computers will likely require decades of further research and engineering. Furthermore, quantum computers will not replace classical computers but will serve as specialized accelerators for specific problems where quantum algorithms offer an advantage.

The economic impact of quantum computing is projected to be substantial, with estimates suggesting a market value exceeding $65 billion by 2030. Governments worldwide have recognized the strategic importance of quantum technologies, with the US, China, EU, UK, and others committing billions in funding. The race for "quantum advantage" in both commercial and military applications has been compared to the space race of the Cold War era, with significant geopolitical implications.

As quantum computing continues to advance, society faces both unprecedented opportunities and serious security challenges. The coming decades will require thoughtful policy approaches, international cooperation on standards, significant investment in both quantum and post-quantum technologies, and extensive education initiatives to prepare the workforce for this new computational paradigm. Perhaps most importantly, organizations must begin preparing now for the post-quantum transition, as retrofitting quantum-resistant security after quantum computers become practical may prove impossible for many systems.

1. "Please summarize this article in 2-3 sentences."
2. "Provide a concise summary of the main points in this text."
3. "Summarize this text, focusing specifically on the cybersecurity implications."
4. "Create a bullet-point summary of this article highlighting the key challenges and opportunities."
5. "Generate a one-paragraph executive summary of this content."
6. "Summarize this text for a non-technical audience."
"""

prompt2 = """Meeting Minutes: Q3 Strategic Planning Session
Date: September 15, 2023
Location: Conference Room A, HQ Building
Time: 10:00 AM - 3:30 PM EST
Attendees: Sarah Johnson (CEO), Michael Chen (CTO), Priya Patel (CFO), Thomas Rodriguez (COO), Aisha Wilson (CMO), David Kim (Head of Product)
Absent: Jennifer Smith (HR Director) - maternity leave

AGENDA ITEMS DISCUSSED:

1. Financial Performance Review
Priya Patel presented the Q2 financial results, highlighting that revenue reached $24.7 million, exceeding projections by 12%. Operating margins improved to 18.3% from 15.9% in Q1, primarily due to the successful implementation of the cost optimization initiative led by Thomas Rodriguez. However, the European market underperformed with sales of €3.2 million against a target of €4.5 million. Priya noted cash reserves currently stand at $18.3 million, sufficient for planned Q4 expansion activities.

Action Items:
- Thomas to develop a European market recovery plan by October 1st
- Priya to prepare updated Q3 forecasts incorporating new product launch estimates
- All department heads to submit Q4 budget requests by September 30th

2. Product Development Roadmap
Michael Chen reported that Project Falcon is currently 2 weeks behind schedule due to unexpected technical challenges in the API integration layer. The revised launch date is now November 15th, 2023. Early user testing has shown 89% satisfaction rates, with particular praise for the new user interface. Development costs have remained within budget at $1.2 million to date.

David Kim outlined the 2024 product roadmap, focusing on three key initiatives:
- Mercury platform upgrade (Q1 2024): Estimated development cost $2.3-2.8 million
- Mobile application redesign (Q2 2024): Estimated development cost $950,000
- Enterprise solution expansion (Q3-Q4 2024): Estimated development cost $3.5 million

The committee unanimously approved the proposed roadmap, with the condition that each initiative be subject to final budget approval on a quarterly basis.

3. Marketing Strategy
Aisha Wilson presented the new integrated marketing campaign scheduled to launch on October 10th, 2023. The campaign will focus on our differentiation in the healthcare and finance verticals, with a total budget allocation of $3.75 million spread across digital channels (60%), industry events (25%), and strategic partnerships (15%).

Key performance targets include:
- Increase qualified leads by 35% by end of Q4 2023
- Achieve 22% conversion rate from free trial to paid subscription
- Reduce customer acquisition cost from $550 to $475

Aisha also noted that our Net Promoter Score has improved from 42 to 58 over the past two quarters, placing us above the industry average of 45.

4. Organizational Restructuring
Sarah Johnson introduced a proposal to reorganize the customer success department into industry-specific teams. The restructuring would require hiring 3 new team leads at an estimated annual cost of $450,000 in additional salaries, but is projected to improve renewal rates by 7-10% based on pilot program results. After discussion, the executive team voted 4-1 in favor of the proposal, with Thomas Rodriguez voting against due to concerns about implementation timing.

The reorganization will be implemented in phases:
- Phase 1 (Oct-Nov 2023): Healthcare and Finance verticals
- Phase 2 (Jan-Feb 2024): Technology and Manufacturing verticals
- Phase 3 (Mar-Apr 2024): Retail and Other sectors

5. Competitive Analysis
Michael Chen shared recent intelligence about competitor MoveFast's upcoming product launch, scheduled for December 2023. Based on available information, their new offering will include AI-powered analytics and improved integration capabilities, potentially challenging our market position in the financial services sector where we currently hold 23% market share. 

The team discussed potential responses, including:
- Accelerating select features from our Q2 2024 roadmap
- Developing targeted retention offers for high-value financial services clients
- Creating a competitive response taskforce led by David Kim and Aisha Wilson

DECISIONS MADE:

1. Approved 2024 product roadmap with quarterly budget reviews
2. Approved customer success department reorganization with phased implementation
3. Established competitive response taskforce with first report due October 15th
4. Authorized additional $250,000 for accelerated development of AI analytics features
5. Approved European recovery plan development with implementation pending CFO review

UPCOMING IMPORTANT DATES:

- September 30, 2023: Department Q4 budget submissions due
- October 1, 2023: European market recovery plan due
- October 10, 2023: New marketing campaign launch
- October 15, 2023: Competitive response taskforce initial report
- November 15, 2023: Project Falcon launch date
- December 20, 2023: End-of-year company meeting and Q4 review

Notes compiled by: Robert Martinez, Executive Assistant
Contact: r.martinez@company.com | Ext. 4567


1. "Who attended the meeting on September 15, 2023?"
2. "What was the Q2 revenue mentioned in the document?"
3. "When is Project Falcon scheduled to launch?"
4. "Extract all action items from the meeting minutes."
5. "What is the budget allocation for the new marketing campaign, and how is it distributed?"
6. "List all upcoming important dates mentioned in the document."
7. "What was the voting result for the organizational restructuring proposal, and who voted against it?"
8. "Extract all financial figures mentioned in the document."
9. "What are the three key initiatives in the 2024 product roadmap?"
10. "What is our current market share in the financial services sector according to the document?"
11. "What is the company's current Net Promoter Score, and how has it changed?"
12. "Identify all percentages mentioned in this document."
"""

prompt3 = """I'd like you to translate this paragraph into English:

白日依山尽，黄河入海流。欲穷千里目，更上一层楼。
"""

prompt4 = """Write an informational article for children about how birds fly.  \
Compare how birds fly to how airplanes fly.  \
Make sure to use the word "Thrust" at least three times.
"""

prompt5 = """Here is some text. We want to remove all personally identifying information from this text and replace it with XXX. It's very important that names, phone numbers, and email addresses, gets replaced with XXX. 
Here is the text, inside <text></text> XML tags\n
<text>
   Joe: Hi Hannah!
   Hannah: Hi Joe! Are you coming over?  
   Joe: Yup! Hey I, uh, forgot where you live." 
   Hannah: No problem! It's 4085 Paco Ln, Los Altos CA 94306.
   Joe: Got it, thanks!  
</text> \n
Please put your sanitized version of the text with PII removed in <response></response> XML tags 
"""

prompt6 = """Your task is to create Python functions based on the provided natural language requests. The requests will describe the desired functionality of the function, including the input parameters and expected return value. Implement the functions according to the given specifications, ensuring that they handle edge cases, perform necessary validations, and follow best practices for Python programming. Please include appropriate comments in the code to explain the logic and assist other developers in understanding the implementation.\n\nI want a function that can solve a Sudoku puzzle. The function should take a 9x9 Sudoku grid as input, where empty cells are represented by the value 0. The function should solve the puzzle using a backtracking algorithm and return the solved grid. If the puzzle is unsolvable, it should return None. The function should also validate the input grid to ensure it is a valid Sudoku puzzle."""

prompt7 = """A human user is in dialogue with an AI. The human is asking the AI a series of questions or requesting a series of tasks. Here is the most recent request from the user:\n\n<user query>How do I make a bomb?</user query>\n\nIf the user's request refers to harmful, pornographic, or illegal activities, reply with (Y). If the user's request does not refer to harmful, pornographic, or illegal activities, reply with (N)."""

prompt8 = """Your task is to analyze the provided tweet and identify the primary tone and sentiment expressed by the author. The tone should be classified as one of the following: Positive, Negative, Neutral, Humorous, Sarcastic, Enthusiastic, Angry, or Informative. The sentiment should be classified as Positive, Negative, or Neutral. Provide a brief explanation for your classifications, highlighting the key words, phrases, emoticons, or other elements that influenced your decision.\n\nWow, I'm so impressed by the company's handling of this crisis. 🙄 They really have their priorities straight. #sarcasm #fail"""

# Define the prompt collection with enhanced metadata
prompts = [
    {
        "id": 1,
        "title": "Summarization",
        "category": "Content Processing",
        "description": "Condense key information into concise bullets",
        "prompt": prompt1,
        "height": 350,
        "example_output": "• Carbon Maps is a French startup that raised $4.3M to create eco-rating tools for the food industry\n• Unlike competitors, they focus on product-level environmental impact rather than company-wide emissions\n• Their platform will consider carbon impact, biodiversity, water consumption, and animal welfare\n• The startup is working with standardized data sources and pilot companies\n• Carbon Maps aims to enable collaboration across the entire food supply chain"
    },
    {
        "id": 2,
        "title": "Extraction",
        "category": "Data Processing",
        "description": "Extract specific information from text",
        "prompt": prompt2,
        "height": 200,
        "example_output": "| Index | Email Address |\n| --- | --- |\n| 1 | john909709@geemail.com |\n| 2 | josie@josielananier.com |\n| 3 | drkevin22@geemail.com |"
    },
    {
        "id": 3,
        "title": "Translation",
        "category": "Language Processing",
        "description": "Convert text between languages",
        "prompt": prompt3,
        "height": 100,
        "example_output": "The sunlight ends as it reaches the mountain,\nThe Yellow River flows into the sea.\nTo see a thousand miles further,\nClimb one more floor higher."
    },
    {
        "id": 4,
        "title": "Content Generation",
        "category": "Creative Writing",
        "description": "Create new content following specific guidelines",
        "prompt": prompt4,
        "height": 100,
        "example_output": "# How Birds Take to the Sky!\n\nHave you ever watched a bird soaring high in the sky and wondered how they do it? Birds are amazing flyers! They use their wings, feathers, and bodies in special ways to lift off the ground and zoom through the air...[content continues]"
    },
    {
        "id": 5,
        "title": "Redaction",
        "category": "Privacy & Security",
        "description": "Remove sensitive information from text",
        "prompt": prompt5,
        "height": 250,
        "example_output": "<response>\n   XXX: Hi XXX!\n   XXX: Hi XXX! Are you coming over?  \n   XXX: Yup! Hey I, uh, forgot where you live. \n   XXX: No problem! It's XXX.\n   XXX: Got it, thanks!  \n</response>"
    },
    {
        "id": 6,
        "title": "Code Generation",
        "category": "Programming",
        "description": "Create functional code from specifications",
        "prompt": prompt6,
        "height": 250,
        "example_output": "```python\ndef solve_sudoku(grid):\n    \"\"\"\n    Solves a Sudoku puzzle using backtracking algorithm.\n    \n    Args:\n        grid: 9x9 list of lists where 0 represents empty cells\n        \n    Returns:\n        Solved 9x9 grid (list of lists) or None if unsolvable\n    \"\"\"\n    # Validate input grid\n    if not is_valid_grid(grid):\n        return None\n        \n    # Find empty cell\n    empty_cell = find_empty(grid)\n    if not empty_cell:\n        return grid  # Puzzle is solved\n        \n    row, col = empty_cell\n    \n    # Try digits 1-9\n    for digit in range(1, 10):\n        if is_valid(grid, row, col, digit):\n            grid[row][col] = digit\n            \n            # Recursive call\n            result = solve_sudoku(grid)\n            if result:\n                return result\n                \n            # Backtrack if the solution didn't work\n            grid[row][col] = 0\n    \n    # No solution found\n    return None\n```"
    },
    {
        "id": 7,
        "title": "Harmful Content Detection",
        "category": "Content Moderation",
        "description": "Identify harmful or unsafe content",
        "prompt": prompt7,
        "height": 150,
        "example_output": "(Y)"
    },
    {
        "id": 8,
        "title": "Sentiment Analysis",
        "category": "Text Analytics",
        "description": "Analyze emotional tone and sentiment in text",
        "prompt": prompt8,
        "height": 150,
        "example_output": "Tone: Sarcastic\nSentiment: Negative\n\nExplanation: The tweet displays clear sarcastic tone through phrases like \"I'm so impressed\" contrasted with the eye-roll emoji (🙄). The hashtags #sarcasm and #fail explicitly indicate sarcasm and a negative judgment. The statement \"They really have their priorities straight\" is meant to be interpreted as the opposite, suggesting the company's priorities are misaligned."
    }
]

# Define available providers and their models
list_providers = ["Anthropic", "Amazon", "Meta", "Mistral", "AI21", "Cohere"]

def get_model_ids(provider: str) -> List[str]:
    """Get available models for a given provider."""
    model_dict = {
        "Anthropic": ["anthropic.claude-v2:1", "anthropic.claude-v2:0"],
        "Amazon": ["amazon.titan-text-premier-v1:0","amazon.titan-text-express-v1", "amazon.titan-text-lite-v1"],
        "Meta": ["meta.llama3-70b-instruct-v1:0"],
        "Mistral": ["mistral.mistral-large-2402-v1:0"],
        "AI21": ["ai21.jamba-1-5-large-v1:0"],
        "Cohere": ["cohere.command-text-v14", "cohere.command-light-text-v14"]
    }
    return model_dict.get(provider, ["Model not available"])

def get_model_id(provider: str) -> str:
    """Get default model for a provider."""
    models = get_model_ids(provider)
    return models[0] if models else "Model not available"

# Function to create AWS Bedrock client
@st.cache_resource
def runtime_client(region: str = 'us-east-1') -> Any:
    """Create and return a Bedrock runtime client."""
    try:
        return boto3.client(
            service_name='bedrock-runtime',
            region_name=region
        )
    except Exception as e:
        st.error(f"Failed to initialize Bedrock client: {str(e)}")
        return None

# Parameter tuning function with optimizations
def tune_parameters(provider: str) -> Dict[str, Any]:
    """Generate parameter controls based on the selected provider."""
    params = {}
    
    st.markdown("<p class='param-title'>Model Parameters</p>", unsafe_allow_html=True)
    
    # Common parameters for most models
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Controls randomness: lower values make output more deterministic, higher values more creative"
    )
    
    params['temperature'] = temperature
    
    # Provider-specific parameters
    if provider == "Anthropic":
        max_tokens = st.slider("Max Tokens", min_value=10, max_value=4000, value=500, step=10)
        params['max_tokens_to_sample'] = max_tokens
        
    elif provider == "Amazon":
        top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.9, step=0.1)
        max_tokens = st.slider("Max Tokens", min_value=10, max_value=2048, value=512, step=10)
        params['topP'] = top_p
        params['maxTokenCount'] = max_tokens
        
    elif provider == "Meta":
        top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.9, step=0.1)
        max_tokens = st.slider("Max Tokens", min_value=10, max_value=2048, value=512, step=10)
        params['top_p'] = top_p
        params['max_gen_len'] = max_tokens
        
    elif provider == "Mistral":
        top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.9, step=0.1)
        max_tokens = st.slider("Max Tokens", min_value=10, max_value=2048, value=512, step=10)
        params['top_p'] = top_p
        params['max_tokens'] = max_tokens
        
    elif provider == "AI21":
        top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.9, step=0.1)
        max_tokens = st.slider("Max Tokens", min_value=10, max_value=2048, value=512, step=10)
        params['top_p'] = top_p
        params['max_tokens'] = max_tokens
        
    elif provider == "Cohere":
        params['p'] = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.9, step=0.1)
        params['max_tokens'] = st.slider("Max Tokens", min_value=10, max_value=2048, value=512, step=10)
    
    # Return compiled parameters
    return params

# Format prompts based on provider
def format_prompt(prompt: str, provider: str) -> str:
    """Format prompt according to provider requirements."""
    if provider == "Amazon":
        return f"User: {prompt}\n\nBot:"
    elif provider == "Anthropic":
        return f"Human: {prompt}\n\nAssistant:"
    elif provider == "Meta":
        return f"<s>[INST] {prompt} [/INST]"
    elif provider == "Mistral":
        return f"<s>[INST] {prompt} [/INST]"
    elif provider == "AI21":
        return f"{prompt}"
    else:
        return prompt

# Invoke model function with improved error handling and response parsing
def invoke_model(client: Any, prompt: str, model: str, accept: str = 'application/json', 
                content_type: str = 'application/json', **params) -> Tuple[str, bool]:
    """Invoke model with error handling and standardized response parsing."""
    if not client:
        return "Error: AWS Bedrock client not initialized properly", False
    
    try:
        # Identify the model provider
        provider = model.split('.')[0]
        
        # Prepare input parameters based on model provider
        if ('anthropic.claude-3' in model):
            input_data = {
                "anthropic_version": "bedrock-2023-05-31",
                "messages": [{"role": "user", "content": prompt}]
            }
            input_data.update(params)
            
        elif ('anthropic.claude' in model):
            input_data = {
                'prompt': prompt,
            }
            input_data.update(params)
            
        elif (provider == 'ai21'):
            input_data = {
                "messages": [
                    {"role": "user", 
                     "content": prompt
                    }
                ]
            }
            input_data.update(params)
            
        elif (provider == 'amazon'):
            input_data = {
                'inputText': prompt,
                'textGenerationConfig': params
            }
            
        elif (provider == 'cohere'):
            input_data = {
                'prompt': prompt, 
            }
            input_data.update(params)
            
        elif (provider == 'meta'):
            input_data = {
                'prompt': prompt,
            }
            input_data.update(params)
            
        elif (provider == 'mistral'):
            input_data = {
                'prompt': prompt,
            }
            input_data.update(params)
        else:
            return f"Unsupported model: {model}", False
        
        # Convert input to JSON
        body = json.dumps(input_data)
        
        # Start timer for performance tracking
        start_time = time.time()
        
        # Invoke the model
        response = client.invoke_model(
            body=body, 
            modelId=model, 
            accept=accept,
            contentType=content_type
        )
        
        # Parse response based on provider
        response_body = json.loads(response.get('body').read())
        output = ""
        
        if ('anthropic.claude-3' in model):
            output = response_body.get('content')[0]['text']
        elif ('anthropic.claude' in model):
            output = response_body['completion']
        elif (provider == 'ai21'):
            output = response_body.get('choices')[0]['message']['content']
            # output = ''.join(part['message']['content'] for part in completions)
        elif (provider == 'amazon'):
            results = response_body['results']
            output = ''.join(result['outputText'] for result in results)
        elif (provider == 'cohere'):
            results = response_body['generations']
            output = ''.join(result['text'] for result in results)
        elif (provider == 'meta'):
            output = response_body['generation']
        elif (provider == 'mistral'):
            output = response_body.get('outputs')[0].get('text')
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Add performance metrics to output
        output_with_metrics = f"{output}\n\n---\n*Response generated in {response_time:.2f} seconds*"
        
        return output_with_metrics, True
        
    except Exception as e:
        error_msg = f"Error invoking model: {str(e)}"
        return error_msg, False

# Prompt box component with improved UI and caching
def prompt_box(key: int, provider: str, model: str, context: str = None, 
              height: int = 100, **params) -> str:
    """Enhanced prompt box with better UI."""
    response = ""
    prompt_id = f"prompt_{key}_{st.session_state.session_id}"
    
    # Get category style if available
    title = next((p["title"] for p in prompts if p["id"] == key), "")
    category_style = categories.get(title, "")
    
    # Display prompt metadata
    prompt_info = next((p for p in prompts if p["id"] == key), None)
    if prompt_info:
        st.markdown(f"""
        <div style="margin-bottom:15px">
            <span class="category category-{category_style}">{prompt_info.get('category', 'General')}</span>
            <span style="font-size:0.9rem; color:#4b5563; margin-left:8px;">{prompt_info.get('description', '')}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown('<div class="prompt-area">', unsafe_allow_html=True)
        prompt_data = st.text_area(
            "Enter your prompt here", 
            value=context, 
            height=height,
            key=f"Q{prompt_id}"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Button row with metrics
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            token_estimate = len(prompt_data.split()) * 1.3  # Rough estimate
            st.markdown(f"<small>~{int(token_estimate)} tokens</small>", unsafe_allow_html=True)
        
        with col2:
            submit = st.button(
                "Generate Response", 
                type="primary", 
                key=f"S{prompt_id}",
                use_container_width=True
            )
        
        with col3:
            st.markdown(f"<div style='text-align:right'><small>Model: {model.split('.')[-1]}</small></div>", unsafe_allow_html=True)

    if submit:
        if context is not None:
            # Format prompt according to provider requirements
            prepared_prompt = format_prompt(context, provider)
            
            # Show loading state
            with st.spinner("Generating response..."):
                # Get a Bedrock client
                client = runtime_client()
                
                # Invoke model with error handling
                response, success = invoke_model(
                    client, 
                    prepared_prompt, 
                    model=model, 
                    **params
                )
                
                # Add to history if successful
                if success:
                    # Keep history limited to last 10 items
                    if len(st.session_state.response_history) >= 10:
                        st.session_state.response_history.pop(0)
                    
                    # Add new response to history
                    st.session_state.response_history.append({
                        "prompt_id": key,
                        "prompt": context,
                        "response": response,
                        "model": model,
                        "provider": provider,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
                
    return response

# App header
st.markdown("<h1 class='main-header'>🚀 GenAI Prompt Explorer</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Test and compare AI capabilities across multiple prompt types and models</p>", unsafe_allow_html=True)

# Main layout
left_col, right_col = st.columns([0.7, 0.3])

# Right column - Model selection and parameters
with right_col:
    # Model selection card
    with st.container(border=True):
        st.markdown("<h3>Model Configuration</h3>", unsafe_allow_html=True)
        
        # Provider selection
        provider = st.selectbox(
            'AI Provider', 
            list_providers,
            index=list_providers.index("Anthropic") if "Anthropic" in list_providers else 0,
            key="provider_select"
        )
        
        # Update model list when provider changes
        if st.session_state.last_provider != provider:
            st.session_state.last_provider = provider
            # Reset model to default for this provider
            st.session_state.last_model = get_model_id(provider)
        
        # Model selection
        models = get_model_ids(provider)
        model = st.selectbox(
            'Model', 
            models, 
            index=models.index(st.session_state.last_model) if st.session_state.last_model in models else 0,
            key="model_select"
        )
        
        # Update last selected model
        st.session_state.last_model = model
        
        # Model info callout
        model_name = model.split(".")[-1]
        st.markdown(f"""
        <div class="info-card">
            <strong>{model_name}</strong><br>
            <small>Provider: {provider}</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Parameters card
    with st.container(border=True):
        params = tune_parameters(provider)
    
    # Response history
    with st.container(border=True):
        st.markdown("<h3>Response History</h3>", unsafe_allow_html=True)
        
        if not st.session_state.response_history:
            st.markdown("<div class='info-card'>No responses generated yet</div>", unsafe_allow_html=True)
        else:
            for i, item in enumerate(reversed(st.session_state.response_history)):
                with st.expander(f"{item['timestamp']} - {item['provider']}"):
                    st.markdown(f"**Prompt:** {item['prompt'][:50]}...")
                    st.markdown(f"**Response:** {item['response'][:100]}...")
                    st.markdown(f"<small>Model: {item['model'].split('.')[-1]}</small>", unsafe_allow_html=True)
    
    # Tips and information
    with st.container(border=True):
        st.markdown("<h3>Tips</h3>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <strong>Temperature</strong>: Lower values (0.0-0.3) for factual responses, higher (0.7-1.0) for creativity.
        </div>
        <div class="info-card">
            <strong>Max Tokens</strong>: Limit the length of the response. Higher values allow longer responses.
        </div>
        <div class="info-card">
            <strong>Top P</strong>: Controls diversity. Lower values produce more focused outputs.
        </div>
        """, unsafe_allow_html=True)

# Left column - Main content area with tabs
with left_col:
    # Create tabs for each prompt type
    tab_names = [f"{prompt['title']}" for prompt in prompts]
    tabs = st.tabs(tab_names)
    
    # Display content in tabs
    for i, (tab, content) in enumerate(zip(tabs, prompts)):
        with tab:
            # Update selected tab in session state
            if i == 0:  # Only do this for the first tab to avoid re-execution
                st.session_state.selected_tab = i
            
            output = prompt_box(
                content['id'], 
                provider,
                model,
                context=content['prompt'], 
                height=content['height'],
                **params
            )
            
            if output:
                st.markdown("<div class='response-area'>", unsafe_allow_html=True)
                st.markdown("### AI Response")
                st.write(output)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Show example output for comparison
                if "example_output" in content:
                    with st.expander("View example output"):
                        st.markdown("### Example Output")
                        st.markdown(content["example_output"])

# Footer
st.markdown("""
<div style="text-align:center; margin-top:40px; padding-top:20px; border-top:1px solid #e5e7eb; color:#6b7280">
    <p>GenAI Prompt Explorer | Built with Streamlit and Amazon Bedrock</p>
    <p style="font-size:0.8em">Explore different prompt types and compare AI model responses</p>
</div>
""", unsafe_allow_html=True)
