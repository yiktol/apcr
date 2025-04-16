
import streamlit as st
import random
from datetime import datetime
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="AWS AI Practitioner Quiz - Domain 2",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# AWS color scheme
AWS_ORANGE = "#FF9900"
AWS_BLUE = "#232F3E"
AWS_LIGHT_BLUE = "#1A73E8"
AWS_LIGHT_GRAY = "#F5F5F5"
AWS_GRAY = "#666666"
AWS_WHITE = "#FFFFFF"
AWS_GREEN = "#008000"
AWS_RED = "#D13212"

# Initialize session state variables
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'quiz_complete' not in st.session_state:
    st.session_state.quiz_complete = False
if 'questions_selected' not in st.session_state:
    st.session_state.questions_selected = False
if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = []
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 5
if 'time_started' not in st.session_state:
    st.session_state.time_started = datetime.now()
if 'auto_advance' not in st.session_state:
    st.session_state.auto_advance = True

# Domain 2 - Fundamentals of Generative AI scenario-based questions
all_questions = [
    {
        "id": 1,
        "question": "A retail company wants to explore how AI can improve their product recommendations and customer service. The CTO asks you to explain foundation models and how they might apply to their business. Which explanation best addresses their needs?",
        "options": {
            "A": "Foundation models are pre-trained AI algorithms that can be quickly deployed to production and run on EC2 instances without additional training, saving operational costs through immediate deployment.",
            "B": "Foundation models are pre-built machine learning models trained on large-scale datasets that can be adapted to various downstream tasks with minimal additional training, enabling efficient operationalization of AI capabilities.",
            "C": "Foundation models use proprietary AWS hardware like Trainium to provide internet-scale AI capabilities but require complete retraining for each new use case, making them operationally expensive but technically superior.",
            "D": "Foundation models are best deployed using Amazon Q Business for retail applications since it's preconfigured for inventory management and doesn't require any modification to meet specific business needs."
        },
        "correct_answer": "B",
        "explanation": {
            "A": "While foundation models can accelerate deployment compared to building models from scratch, they typically do require some adaptation for specific business needs and aren't simply 'plug and play' solutions. This explanation overstates the immediate deployability without additional training.",
            "B": "Correct! Foundation models are indeed pre-built machine learning models trained on large amounts of data that can be adapted to various tasks with minimal additional training. This explanation accurately reflects how foundation models can provide operational benefits through efficient adaptation to specific business needs.",
            "C": "This explanation contains several inaccuracies. While AWS does offer specialized hardware like Trainium, foundation models don't require complete retraining for each use case—that would negate their primary benefit of transfer learning. This mischaracterizes their operational advantages.",
            "D": "This explanation is misleading. Amazon Q Business is a generative AI assistant, not a specific implementation of foundation models for retail. Foundation models are underlying technologies that can power various applications and aren't limited to a single product implementation."
        },
        "category": "Foundation Models"
    },
    {
        "id": 2,
        "question": "A fintech startup is developing a solution that needs to analyze relationships between words in customer support queries to understand context and route tickets appropriately. The team is debating which underlying architecture would be most efficient. Which solution would you recommend?",
        "options": {
            "A": "Implement Recurrent Neural Networks (RNNs) because they process sequences one element at a time, conserving computational resources while maintaining adequate performance for text analysis.",
            "B": "Deploy Transformer architecture which analyzes relationships between words using parallel processing and attention mechanisms, optimizing computational resource utilization and scaling efficiently with demand.",
            "C": "Use traditional rule-based Natural Language Processing (NLP) systems since they require less computational resources than deep learning approaches and provide sufficient accuracy for simple ticket routing.",
            "D": "Implement a hybrid CNN-LSTM model which balances computational costs with effectiveness by processing text in chunks, making it more resource-efficient than full Transformer implementations."
        },
        "correct_answer": "B",
        "explanation": {
            "A": "While RNNs can analyze sequences, they process data sequentially rather than in parallel, creating computational bottlenecks for longer sequences. This makes them less efficient than Transformers for this use case.",
            "B": "Correct! Transformer architecture employs parallel processing and self-attention mechanisms that allow it to analyze relationships between words efficiently. This architecture optimizes computational resources and enables better scaling for demand spikes in customer support.",
            "C": "Traditional rule-based NLP systems may use fewer computational resources but often fall short in understanding context and nuanced language, requiring extensive manual rule creation and maintenance. This would likely result in poor ticket routing accuracy, especially as language evolves.",
            "D": "While hybrid CNN-LSTM models exist, they don't typically outperform Transformers for understanding relationships between words in a sequence. This option contains plausible-sounding but technically misleading information about resource efficiency."
        },
        "category": "Transformer Architecture"
    },
    {
        "id": 3,
        "question": "A media production company needs to implement AI capabilities for both script generation and creating concept art based on those scripts. They want to minimize infrastructure complexity while maximizing creative output. Which approach should they consider?",
        "options": {
            "A": "Deploy separate foundation models for each task: Claude for text generation and Amazon Titan for image generation, as task-specialized models are always more cost-effective than general-purpose ones.",
            "B": "Implement a single multimodal foundation model that handles both text and images, reducing infrastructure complexity while potentially sacrificing some quality in specialized tasks.",
            "C": "Use text-to-text foundation models for script generation and text-to-image foundation models for concept art creation, balancing specialized capabilities with infrastructure efficiency.",
            "D": "Build custom small language and image models from scratch on SageMaker, as proprietary models will be more cost-efficient in the long term than using foundation model APIs."
        },
        "correct_answer": "C",
        "explanation": {
            "A": "This option incorrectly suggests that Claude is specialized only for text generation and Titan only for image generation. It also makes an incorrect blanket statement about specialized models always being more cost-effective, which isn't necessarily true when considering infrastructure and maintenance costs.",
            "B": "While multimodal models exist, they may not provide the best quality for both text generation and image creation tasks. This approach might actually increase costs if the results require significant human refinement due to lower quality output.",
            "C": "Correct! Using text-to-text foundation models for script generation and text-to-image models for concept art creation selects the right tools for each job while maintaining infrastructure efficiency. This approach avoids overprovisioning resources while still delivering high-quality outputs.",
            "D": "Building custom models from scratch would require significant upfront investment in data collection, preparation, and training, along with ongoing maintenance costs. This is likely to be much more expensive than using existing foundation models."
        },
        "category": "Types of Foundation Models"
    },
    {
        "id": 4,
        "question": "A marketing team is using an AWS-hosted generative AI service to create varied content ideas for different audience segments. They need consistent quality but with appropriate creativity for each segment. Which parameter configuration approach should they implement?",
        "options": {
            "A": "Set temperature to 0.2 for corporate clients and 0.8 for creative campaigns, while maintaining a constant top_p value of 0.9 across all generation tasks to ensure baseline reliability with segment-appropriate creativity.",
            "B": "Configure top_k filtering to 50 for all content generation to ensure output reliability, while modifying response length based on audience segment, as shorter outputs are inherently more reliable across all audience types.",
            "C": "Apply a consistent temperature setting of 0.7 for all content generation as this single configuration provides the optimal balance of reliability and creativity across all possible audience segments.",
            "D": "Use automated parameter adjustment through Amazon Bedrock Guardrails that dynamically modifies temperature and top_p based on audience segment profiles to optimize for reliability without manual intervention."
        },
        "correct_answer": "A",
        "explanation": {
            "A": "Correct! This approach intelligently varies the temperature parameter based on the audience needs (lower for corporate clients where predictability is valued, higher for creative campaigns where uniqueness matters) while maintaining a consistent top_p value as a reliability baseline. This ensures consistent quality appropriate to each segment.",
            "B": "While top_k filtering can help with reliability, this approach incorrectly assumes that output length correlates with reliability. Shorter outputs aren't inherently more reliable, and content length should be determined by communication needs rather than reliability concerns.",
            "C": "Using a single temperature setting for all content generation fails to account for different audience needs and segment-specific requirements. This rigid approach doesn't allow for adaptation to different audience expectations.",
            "D": "While this sounds plausible, Amazon Bedrock Guardrails don't automatically adjust temperature and top_p parameters based on audience segments. This option describes a capability that doesn't exist in the current service, making it misleading."
        },
        "category": "Inference Parameters"
    },
    {
        "id": 5,
        "question": "A healthcare SaaS provider is developing a system where medical professionals can interact with an AI assistant to generate treatment options. The system needs to produce diverse yet medically sound responses. Which approach to controlling token selection is most appropriate?",
        "options": {
            "A": "Implement only temperature control set to 1.0 to maximize response diversity, then use separate downstream validation services to ensure medical accuracy of all generated content.",
            "B": "Configure both top_k=50 and top_p=0.95 parameters while maintaining a low temperature of 0.3, creating boundaries for token selection that balances diversity and reliability.",
            "C": "Apply a combination of top_k=40, top_p=0.85, and temperature=0.7, while also implementing response filtering through Amazon Bedrock Guardrails to enforce acceptable medical terminology and prevent harmful suggestions.",
            "D": "Use solely maximum likelihood sampling (temperature=0) to ensure deterministic outputs that can be pre-validated against medical knowledge bases, sacrificing response diversity for maximum safety."
        },
        "correct_answer": "C",
        "explanation": {
            "A": "Setting temperature to 1.0 maximizes randomness, which could produce medically unsound or potentially harmful suggestions. Relying solely on downstream validation creates risks as inappropriate content would still be generated before being filtered.",
            "B": "While this approach uses multiple parameters, the combination of high top_k and top_p values with a low temperature is contradictory. The high token selection parameters would allow diversity that the low temperature would then suppress. Additionally, there's no mention of healthcare-specific safeguards.",
            "C": "Correct! This approach uses a balanced combination of top_k, top_p, and temperature parameters to control diversity while implementing domain-specific guardrails to prevent harmful medical suggestions. This provides multiple layers of controls to protect patient safety while still allowing useful diversity in responses.",
            "D": "Using only maximum likelihood sampling (temperature=0) would produce deterministic outputs that lack necessary diversity for considering various patient factors and treatment options. This approach is too restrictive and would limit the system's utility while creating a false sense of safety."
        },
        "category": "Inference Parameters"
    },
    {
        "id": 6,
        "question": "A customer service AI assistant for a multinational bank needs to maintain conversation context across multiple interactions about complex financial products. What design approach best addresses the context management requirements?",
        "options": {
            "A": "Implement a stateless design where each customer query is processed independently without previous context, ensuring system stability by eliminating context-related memory failures.",
            "B": "Store the complete conversation history in browser cookies on the customer's device, retrieving it when needed to maintain perfect context continuity without server-side storage concerns.",
            "C": "Design the system with conversation state management in a persistent data store while implementing token limits and summarization techniques for long conversations to handle context within technical constraints.",
            "D": "Configure the foundation model with unlimited context windows by provisioning dedicated GPU instances for each active conversation, ensuring complete conversation history is always available regardless of length."
        },
        "correct_answer": "C",
        "explanation": {
            "A": "A stateless design would force customers to repeatedly provide the same information about their financial situation in every interaction, creating a poor user experience and reducing the reliability of the service from the customer perspective.",
            "B": "Storing conversation history in browser cookies creates multiple reliability issues: cookies have size limitations, can be cleared by users, don't persist across devices, and create security concerns for sensitive financial information. This approach fails to provide reliable context management.",
            "C": "Correct! This design acknowledges the technical constraints of context windows while implementing solutions (persistent storage, token limits, and summarization) to manage them effectively. This approach accounts for limitations while meeting business requirements.",
            "D": "Foundation models have inherent token limits in their architecture that cannot be eliminated simply by adding more computing resources. Suggesting that dedicated GPU instances can provide unlimited context windows is technically inaccurate and would create unrealistic expectations about system capabilities."
        },
        "category": "Context in Foundation Models"
    },
    {
        "id": 7,
        "question": "A legal services company is implementing a generative AI solution to assist paralegals with document analysis and case research. During the risk assessment phase, stakeholders raise concerns about factual accuracy. Which design approach best addresses this concern?",
        "options": {
            "A": "Use direct API integration with authoritative legal databases and implement Retrieval Augmented Generation (RAG) to ground model responses in verified sources, while clearly identifying any content that remains speculative.",
            "B": "Set the model's temperature parameter to 0 for all legal analysis tasks to eliminate hallucinations, as the model will only produce the single most statistically likely response based on its training data.",
            "C": "Implement a multi-model ensemble approach where three separate foundation models analyze each document, and only information agreed upon by all three models is presented to paralegals.",
            "D": "Use Amazon Bedrock's confidence scores to automatically filter out responses below 95% confidence, ensuring only highly confident answers reach the legal team."
        },
        "correct_answer": "A",
        "explanation": {
            "A": "Correct! Retrieval Augmented Generation grounds model outputs in authoritative sources, improving factual accuracy for legal content. Clearly marking speculative content aligns with transparency principles. This approach addresses reliability through verified information sourcing while acknowledging inherent limitations.",
            "B": "Setting temperature to 0 doesn't eliminate hallucinations; it only makes outputs more deterministic. The model can still produce factual errors with high confidence, especially in specialized legal domains that may be underrepresented in its training data. This approach creates a false sense of reliability.",
            "C": "While ensemble approaches can improve certain aspects of model performance, there's no guarantee that agreement between multiple models indicates factual accuracy. All models could share the same erroneous information from their training data, creating a misleading consensus.",
            "D": "This option contains misleading information, as Amazon Bedrock doesn't provide explicit confidence scores that can be used to filter responses at a 95% threshold. This approach suggests capabilities that don't exist in the current service."
        },
        "category": "Generative AI Concerns"
    },
    {
        "id": 8,
        "question": "A digital health startup is building an application that will use generative AI to provide personalized wellness plans. They need to select an AWS service that provides access to multiple foundation models, allows customization for health-specific terminology, and includes responsible AI features. Which recommendation is most appropriate?",
        "options": {
            "A": "Deploy each foundation model on separate Amazon EC2 instances with GPUs, allowing maximum control over optimization and performance tuning for each model while keeping costs predictable with reserved instances.",
            "B": "Use Amazon SageMaker to host all models, implementing auto-scaling based on usage patterns and custom containers for health-specific optimizations, enabling granular cost management across the model lifecycle.",
            "C": "Implement Amazon Bedrock to access multiple foundation models through a single API, utilizing consumption-based pricing for development and testing phases before committing to a specific model for production deployment.",
            "D": "Deploy a hybrid solution with Amazon Q for conversational interfaces and Amazon Rekognition for image analysis, minimizing development costs by utilizing fully managed services instead of working directly with foundation models."
        },
        "correct_answer": "C",
        "explanation": {
            "A": "Deploying separate EC2 instances for each foundation model would create significant operational overhead and higher costs due to maintaining multiple infrastructure components. This approach requires paying for compute resources even during periods of low usage.",
            "B": "While SageMaker provides excellent capabilities for hosting models, this approach would still require managing individual model endpoints and would be more complex and costly than necessary if the team primarily needs API access to pre-trained foundation models rather than custom model training.",
            "C": "Correct! Amazon Bedrock provides access to multiple foundation models through a single API with consumption-based pricing, perfect for this use case. It allows the team to experiment with different models before committing to one, only paying for what they use while gaining access to responsible AI features.",
            "D": "This hybrid approach doesn't address the need to access and customize foundation models for health-specific terminology. Amazon Q and Rekognition are specialized services that wouldn't provide the flexibility needed for generating personalized wellness plans."
        },
        "category": "AWS Infrastructure for Generative AI"
    },
    {
        "id": 9,
        "question": "A research institution plans to develop specialized natural language processing models for scientific literature analysis. They need to experiment with different foundation models before selecting one for fine-tuning with their domain-specific data. Which service would best meet their requirements?",
        "options": {
            "A": "Amazon Comprehend Medical, as it's pre-trained for scientific and medical documents and eliminates the need for model selection or fine-tuning while providing high performance.",
            "B": "Amazon SageMaker with JumpStart, providing access to foundation models with automated fine-tuning pipelines and optimized instance selection for scientific workloads.",
            "C": "Amazon Q Developer, as it can generate model selection recommendations and optimize code for scientific NLP tasks based on researcher requirements.",
            "D": "Amazon EC2 P5 instances with manual model installation, as direct hardware access enables maximum performance optimization for specialized scientific language processing."
        },
        "correct_answer": "B",
        "explanation": {
            "A": "Amazon Comprehend Medical is designed for medical text analysis but doesn't provide access to general foundation models for experimentation or customization. It's specialized for specific healthcare tasks rather than general scientific literature analysis.",
            "B": "Correct! Amazon SageMaker with JumpStart provides access to a variety of foundation models with infrastructure optimized for machine learning workloads. It offers tools to experiment with different models efficiently and create automated fine-tuning pipelines tailored to scientific literature.",
            "C": "Amazon Q Developer is a generative AI coding assistant that helps with coding tasks but doesn't provide foundation model selection or scientific NLP optimization capabilities as described. This option attributes capabilities to the service that it doesn't possess.",
            "D": "While EC2 P5 instances provide powerful computing resources, manually installing and configuring models would require significant expertise and time, reducing productivity and efficiency for the research team."
        },
        "category": "AWS Infrastructure for Generative AI"
    },
    {
        "id": 10,
        "question": "A pharmaceutical company is developing an AI-driven drug discovery platform. They need to process massive datasets of molecular structures and research publications. Which components are most essential for building effective foundation models in this domain?",
        "options": {
            "A": "Small curated datasets of validated drug compounds paired with a standard model architecture, as the quality of pharma data matters more than quantity for operational success.",
            "B": "Unlabeled research data combined with supervised fine-tuning on clinical outcomes, with model size limited to 1B parameters to ensure interpretability for regulatory compliance.",
            "C": "Large volumes of unlabeled molecular and research data paired with significant computing infrastructure capable of training billion-parameter models with specialized pharma knowledge.",
            "D": "Pre-labeled datasets with explicit molecule-effect relationships, using reinforcement learning rather than traditional foundation model architectures for better operational control."
        },
        "correct_answer": "C",
        "explanation": {
            "A": "While quality data is important, foundation models typically require large volumes of data to develop broad capabilities. Small curated datasets would be more appropriate for fine-tuning rather than building foundation models. This approach mischaracterizes the data requirements for foundation models.",
            "B": "Limiting model size to 1B parameters could unnecessarily constrain model capabilities for complex pharmaceutical applications. Additionally, interpretability for regulatory compliance isn't directly related to model size. This option includes misleading connections between model size and regulatory requirements.",
            "C": "Correct! Foundation models require two key components: large volumes of unlabeled data and significant computing infrastructure to train large models with billions of parameters. This approach correctly identifies the essential components needed for the pharmaceutical use case.",
            "D": "While reinforcement learning has applications in drug discovery, it isn't typically a replacement for foundation model architectures. Pre-labeled datasets with explicit relationships would be better suited for supervised learning approaches rather than foundation model development."
        },
        "category": "Components of Foundation Models"
    },
    {
        "id": 11,
        "question": "A machine learning team at a financial services company needs to train large language models for financial document analysis. They're evaluating AWS compute options to optimize both performance and cost. Which approach would you recommend?",
        "options": {
            "A": "Deploy training workloads on AWS Inferentia chips, reserving them for 3 years to maximize the discount while ensuring consistent performance for financial compliance requirements.",
            "B": "Utilize AWS Trainium chips for model training tasks while implementing on-demand AWS Inferentia instances for inference, matching the right hardware to each phase of the ML workflow.",
            "C": "Standardize on NVIDIA A10G GPUs on Amazon EC2 for both training and inference to simplify architecture and reduce operational complexity, improving overall cost efficiency.",
            "D": "Implement a hybrid approach using Amazon SageMaker for model training with automatic hardware selection and AWS Lambda for serverless inference to eliminate idle capacity costs."
        },
        "correct_answer": "B",
        "explanation": {
            "A": "This option contains a critical misconception: AWS Inferentia chips are designed for inference, not training workloads. Additionally, reserving specialized hardware for 3 years might not be cost-effective as AI hardware evolves rapidly. This approach misaligns specialized hardware with its intended purpose.",
            "B": "Correct! AWS Trainium is purpose-built for training machine learning models while AWS Inferentia is optimized for inference. This approach matches specialized hardware to specific workload requirements, improving performance while reducing costs compared to general-purpose solutions.",
            "C": "While standardizing on a single GPU type might simplify architecture, it fails to take advantage of purpose-built chips that offer better price-performance ratios for specific ML tasks. This approach prioritizes operational simplicity over cost optimization.",
            "D": "AWS Lambda has limitations for machine learning inference, including maximum execution time and memory constraints that make it unsuitable for large language model inference. SageMaker's automatic hardware selection might not always choose the most cost-effective options for specialized financial workloads."
        },
        "category": "AWS Infrastructure for Generative AI"
    },
    {
        "id": 12,
        "question": "A startup is planning to create an AI playground where non-technical users can experiment with building simple AI applications using generative AI capabilities. Which AWS service would best support this requirement?",
        "options": {
            "A": "Amazon SageMaker Canvas, as it provides a visual interface for creating machine learning models without requiring coding experience but still allows for production deployment of resulting applications.",
            "B": "PartyRock, an Amazon Bedrock playground that enables users to experiment with prompt engineering and build shareable AI apps without requiring deep technical expertise.",
            "C": "AWS Cloud9, since it provides a cloud-based integrated development environment that can be preconfigured with AI templates for users to modify with minimal coding requirements.",
            "D": "Amazon Lex, because it enables the creation of conversational interfaces using a visual workflow designer that non-technical users can master for building AI-powered chatbots."
        },
        "correct_answer": "B",
        "explanation": {
            "A": "Amazon SageMaker Canvas is designed for creating traditional machine learning models rather than generative AI applications. While it does provide a visual interface, it doesn't focus on foundation models or generative AI experimentation as required in the scenario.",
            "B": "Correct! PartyRock is specifically designed as a playground for experimenting with generative AI through Amazon Bedrock. It allows non-technical users to build, share, and remix AI apps for various tasks using foundation models, perfectly matching the startup's requirements for an accessible AI experimentation platform.",
            "C": "AWS Cloud9 is a development environment requiring coding expertise, not an AI playground for non-technical users. While it could be used for AI development, it wouldn't provide the simplified experience needed for the target audience in this scenario.",
            "D": "Amazon Lex is specifically for building conversational interfaces and chatbots, not for general generative AI applications. While it does have a visual workflow designer, it's limited to conversational AI rather than the broader generative AI capabilities described in the scenario."
        },
        "category": "AWS Services for Generative AI"
    },
    {
        "id": 13,
        "question": "A media analytics company wants to implement AI capabilities to analyze customer sentiment in social media posts about their clients' brands. They have limited ML expertise but need a solution that can be adapted as their requirements evolve. Which approach to foundation model customization would you recommend?",
        "options": {
            "A": "Implement continued pre-training on social media data using multiple Amazon EC2 P4d instances to build the most accurate model possible, maximizing resource utilization through parallel training.",
            "B": "Begin with prompt engineering techniques, then implement RAG as needs become more complex, progressing to fine-tuning only if necessary to minimize computational resource consumption.",
            "C": "Immediately deploy fine-tuned models for each client brand to maximize accuracy, implementing automatic scaling to ensure resources are used only when needed for each brand's analysis.",
            "D": "Create a custom language model from scratch focused specifically on social media sentiment analysis, as domain-specific models ultimately require fewer computational resources over their lifecycle."
        },
        "correct_answer": "B",
        "explanation": {
            "A": "Continued pre-training is the most computationally intensive customization approach, requiring massive resources and energy consumption. Starting with this approach uses maximum resources before exploring more efficient alternatives.",
            "B": "Correct! This approach follows a progressively more complex customization path, starting with low-resource techniques like prompt engineering before moving to more computationally intensive approaches only if necessary. This minimizes resource consumption while still meeting business requirements.",
            "C": "Immediately deploying fine-tuned models for each client would consume unnecessary computational resources when simpler approaches might suffice. This approach fails to consider the environmental impact of training multiple specialized models when more efficient alternatives exist.",
            "D": "Creating a custom language model from scratch would require enormous computational resources compared to adapting existing models. The claim that domain-specific models require fewer resources over their lifecycle is generally incorrect, as maintenance and updating of custom models typically requires significant ongoing resources."
        },
        "category": "Model Customization"
    },
    {
        "id": 14,
        "question": "An enterprise customer experience team is implementing an AI assistant to help employees answer customer queries across multiple departments. Which Amazon service would best meet their requirements?",
        "options": {
            "A": "Deploy Amazon SageMaker endpoints running open-source LLMs with custom knowledge bases for each department, allowing complete customization without ongoing API fees.",
            "B": "Implement Amazon Bedrock with custom RAG for company knowledge, providing flexible foundation model access with consumption-based pricing that aligns costs to actual usage patterns.",
            "C": "Utilize Amazon Q Business, which provides an enterprise-ready AI assistant with built-in connectors to company data sources and role-based access controls for different departments.",
            "D": "Develop a custom solution using Amazon EC2 instances with spot pricing, deploying open-source models that can be customized for each department's knowledge domain."
        },
        "correct_answer": "C",
        "explanation": {
            "A": "Running SageMaker endpoints for LLMs would require managing model deployments, scaling, and infrastructure, creating operational overhead. While it eliminates API fees, it would likely increase total cost of ownership through infrastructure and maintenance expenses.",
            "B": "While Amazon Bedrock provides excellent foundation model access, implementing a custom RAG system would require significant development work to connect to company knowledge bases and build the necessary infrastructure, increasing initial development costs.",
            "C": "Correct! Amazon Q Business is specifically designed as an enterprise AI assistant with built-in capabilities to connect to company data sources and role-based access controls. This provides a ready-to-use solution that minimizes development costs while delivering the required functionality.",
            "D": "Developing a custom solution on EC2, even with spot pricing, would require significant development and ongoing maintenance resources. Managing infrastructure, scaling, and ensuring reliability would increase total costs compared to using purpose-built managed services."
        },
        "category": "AWS Services for Generative AI"
    },
    {
        "id": 15,
        "question": "A healthcare technology company is developing an AI system to assist medical researchers in analyzing clinical trial data. They need to customize foundation models for medical terminology and compliance requirements. Which model customization approach should they implement?",
        "options": {
            "A": "Implement prompt engineering with strict guardrails, as it doesn't require sharing sensitive patient data with the model and allows clear control over permitted outputs through prompt constraints.",
            "B": "Use fine-tuning with synthetic patient data that preserves statistical patterns while eliminating personally identifiable information, deploying the model in a private VPC with encrypted data stores.",
            "C": "Apply continued pre-training on de-identified medical literature and aggregate trial results to improve domain knowledge without exposing individual patient data, implementing additional security layers.",
            "D": "Deploy a RAG architecture that retrieves from encrypted and access-controlled clinical databases, combining foundation model capabilities with secure access to validated medical information through established authorization protocols."
        },
        "correct_answer": "D",
        "explanation": {
            "A": "While prompt engineering can provide some control through guardrails, it doesn't address the need to customize the model for medical terminology. Additionally, prompt constraints aren't sufficient to ensure compliance with healthcare security requirements.",
            "B": "Fine-tuning requires sharing data with the model during training, even if synthetic. This approach still creates potential security risks if the synthetic data retains any patterns that could be reverse-engineered to identify individuals. The private VPC adds security but doesn't address the fundamental data sharing concern.",
            "C": "Continued pre-training would help with medical terminology but requires extensive computational resources. While using de-identified literature reduces privacy risks, this approach doesn't address how the model will securely access trial data during operation.",
            "D": "Correct! A RAG architecture allows the model to access and utilize medical information without requiring sensitive data for model training. By implementing proper encryption and access controls on the retrieval sources, this approach maintains security while enabling the model to work with accurate medical information."
        },
        "category": "Model Customization"
    }
]

# Define CSS for better styling with AWS color scheme
st.markdown(f"""
<style>
    .main-header {{
        font-size: 2.5rem;
        color: {AWS_ORANGE};
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }}
    .sub-header {{
        font-size: 1.5rem;
        color: {AWS_BLUE};
        margin-bottom: 1rem;
    }}
    .question-card {{
        background-color: {AWS_WHITE};
        padding: 25px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 5px solid {AWS_ORANGE};
    }}
    .option-button {{
        width: 100%;
        text-align: left;
        margin: 8px 0;
        padding: 12px 15px;
        border-radius: 5px;
        border: 1px solid #ddd;
        background-color: {AWS_WHITE};
        transition: all 0.3s ease;
    }}
    .option-button:hover {{
        background-color: #f5f5f5;
        border-color: {AWS_ORANGE};
    }}
    .selected-option {{
        background-color: #e6f7ff;
        border-color: {AWS_LIGHT_BLUE};
    }}
    .correct-option {{
        background-color: #d4edda;
        border-color: {AWS_GREEN};
    }}
    .incorrect-option {{
        background-color: #f8d7da;
        border-color: {AWS_RED};
    }}
    .category-tag {{
        background-color: {AWS_BLUE};
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 15px;
    }}
    .explanation-box {{
        padding: 18px;
        border-radius: 5px;
        background-color: #f0f8ff;
        margin-top: 20px;
        border-left: 4px solid {AWS_LIGHT_BLUE};
    }}
    .stats-box {{
        background-color: {AWS_LIGHT_GRAY};
        border-radius: 8px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    .aws-button {{
        background-color: {AWS_ORANGE};
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 18px;
        margin: 8px 5px;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    .aws-button:hover {{
        background-color: #ec7211;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }}
    .aws-secondary-button {{
        background-color: {AWS_BLUE};
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 18px;
        margin: 8px 5px;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    .aws-secondary-button:hover {{
        background-color: #1a2530;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }}
    .progress-container {{
        margin: 20px 0;
        padding: 15px;
        background-color: {AWS_WHITE};
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    .progress-label {{
        font-weight: 600;
        color: {AWS_BLUE};
        margin-bottom: 8px;
    }}
    .stProgress > div > div > div > div {{
        background-color: {AWS_ORANGE};
    }}
    .footer {{
        text-align: center;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #eee;
        color: {AWS_GRAY};
        font-size: 0.8rem;
    }}
    .sidebar .sidebar-content {{
        background-color: {AWS_LIGHT_GRAY};
    }}
    /* Responsive styling */
    @media (max-width: 768px) {{
        .main-header {{
            font-size: 2rem;
        }}
        .sub-header {{
            font-size: 1.2rem;
        }}
        .question-card {{
            padding: 15px;
        }}
        .option-button {{
            padding: 10px;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# Navigation and state management functions
def select_random_questions(num_questions=10):
    # Check if we need to select questions
    if not st.session_state.questions_selected:
        # Reset time when new questions are selected
        st.session_state.time_started = datetime.now()
        
        # Make a copy of all questions to avoid modifying the original
        available_questions = all_questions.copy()
        random.shuffle(available_questions)
        
        # Ensure we have at least one question from each category
        selected_questions = []
        categories = set(q["category"] for q in available_questions)
        
        for category in categories:
            category_questions = [q for q in available_questions if q["category"] == category]
            if category_questions:
                selected = random.choice(category_questions)
                selected_questions.append(selected)
                available_questions.remove(selected)
        
        # Fill the rest randomly
        remaining_needed = num_questions - len(selected_questions)
        if remaining_needed > 0:
            random.shuffle(available_questions)
            selected_questions.extend(available_questions[:remaining_needed])
        
        # Update IDs to be sequential
        for i, question in enumerate(selected_questions):
            question["id"] = i + 1
        
        # Update session state
        st.session_state.selected_questions = selected_questions
        st.session_state.questions_selected = True
        st.session_state.total_questions = len(selected_questions)
        st.session_state.score = 0  # Reset score when new questions are selected
        st.session_state.answers = {}  # Reset answers

def go_to_next_question():
    if st.session_state.current_question_index < len(st.session_state.selected_questions) - 1:
        st.session_state.current_question_index += 1
    else:
        st.session_state.quiz_complete = True

def go_to_previous_question():
    if st.session_state.current_question_index > 0:
        st.session_state.current_question_index -= 1

def reset_quiz():
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.answers = {}
    st.session_state.quiz_complete = False
    st.session_state.questions_selected = False
    st.session_state.selected_questions = []
    st.session_state.time_started = datetime.now()

def answer_selected(option_key, question_id):
    q_id = str(question_id)
    question = next((q for q in st.session_state.selected_questions if str(q["id"]) == q_id), None)
    
    # Check if this question has already been answered
    already_answered = q_id in st.session_state.answers
    
    # Record the answer
    st.session_state.answers[q_id] = option_key
    
    # Update score if correct and not already answered
    if not already_answered and option_key == question["correct_answer"]:
        st.session_state.score += 1
    
    # Auto-advance to next question if enabled
    if st.session_state.auto_advance:
        # Wait 1 second to show the answer before advancing
        # (We can't actually delay in Streamlit, but the rerun will create a small pause)
        if st.session_state.current_question_index < len(st.session_state.selected_questions) - 1:
            st.session_state.current_question_index += 1

# Calculate score based on answered questions
def calculate_score():
    correct_count = 0
    for q_id, user_answer in st.session_state.answers.items():
        question = next((q for q in st.session_state.selected_questions if str(q["id"]) == q_id), None)
        if question and user_answer == question["correct_answer"]:
            correct_count += 1
    return correct_count

# Select random questions if not already done
select_random_questions(st.session_state.total_questions)

# Main application
def main():
    # Sidebar
    with st.sidebar:
        st.image("images/AWS-Certified-AI-Practitioner_badge.png", width=100)
        st.markdown("## Session Management")
        
        # Quiz settings
        st.markdown("### Quiz Settings")
        # Number of questions selector
        num_questions = st.slider("Number of Questions", min_value=10, max_value=15, value=st.session_state.total_questions, step=1)
        if num_questions != st.session_state.total_questions:
            st.session_state.total_questions = num_questions
            st.session_state.questions_selected = False  # Force reselection of questions
            select_random_questions(num_questions)
            st.rerun()
        
        # Auto-advance toggle
        auto_advance = st.checkbox("Auto-advance to next question", value=st.session_state.auto_advance)
        if auto_advance != st.session_state.auto_advance:
            st.session_state.auto_advance = auto_advance
        
        # Quiz controls
        st.markdown("### Quiz Controls")
        if st.button("Reset Quiz", key="reset_quiz"):
            reset_quiz()
            select_random_questions(st.session_state.total_questions)
            st.rerun()
            
        if not st.session_state.quiz_complete and len(st.session_state.answers) > 0:
            if st.button("Skip to Results", key="skip_results"):
                st.session_state.quiz_complete = True
                st.rerun()
        
        # Navigation
        if not st.session_state.quiz_complete:
            st.markdown("### Navigation")
            question_nav = st.selectbox(
                "Jump to Question",
                [f"Question {i+1}" for i in range(len(st.session_state.selected_questions))],
                index=st.session_state.current_question_index
            )
            if st.button("Go", key="go_btn"):
                q_idx = int(question_nav.split()[1]) - 1
                st.session_state.current_question_index = q_idx
                st.rerun()
        
        # Quiz progress
        st.markdown("### Quiz Progress")
        total_questions = len(st.session_state.selected_questions)
        answered_questions = len(st.session_state.answers)
        progress_percentage = (answered_questions / total_questions) if total_questions > 0 else 0
        
        st.progress(progress_percentage)
        st.write(f"Completed: {answered_questions}/{total_questions} questions ({progress_percentage*100:.0f}%)")
        
        # Recalculate score from answers
        correct_answers = calculate_score()
        st.session_state.score = correct_answers  # Update the session state score
        
        # Score
        accuracy = (correct_answers / answered_questions) * 100 if answered_questions > 0 else 0
        st.write(f"Score: {correct_answers}/{answered_questions} correct ({accuracy:.1f}%)")
        
        # Time elapsed
        time_elapsed = datetime.now() - st.session_state.time_started
        minutes = time_elapsed.seconds // 60
        seconds = time_elapsed.seconds % 60
        st.write(f"Time: {minutes}m {seconds}s")
    
    # Header with AWS logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 class='main-header'>AWS AI Practitioner Quiz</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center'>Domain 2: Fundamentals of Generative AI</p>", unsafe_allow_html=True)
    
    # If quiz is complete, show results
    if st.session_state.quiz_complete:
        display_results()
    else:
        # Display current question
        display_question(st.session_state.current_question_index)
    
    # Footer
    st.markdown("<div class='footer'>© 2025 AWS AI Practitioner Quiz. Created for learning purposes.</div>", unsafe_allow_html=True)

# Display a question
def display_question(q_index):
    question = st.session_state.selected_questions[q_index]
    q_id = str(question["id"])
    
    st.markdown(f"<div class='question-card'>", unsafe_allow_html=True)
    
    # Display category tag
    category = question.get("category", "General")
    st.markdown(f"<span class='category-tag'>{category}</span>", unsafe_allow_html=True)
    
    # Display question
    st.markdown(f"<h2 class='sub-header'>Question {q_index + 1} of {len(st.session_state.selected_questions)}</h2>", unsafe_allow_html=True)
    st.write(question["question"])
    
    # Check if user has already answered
    user_answered = q_id in st.session_state.answers
    
    if not user_answered:
        for option_key, option_text in question["options"].items():
            # Use a consistent key without random numbers
            button_key = f"option_{q_id}_{option_key}"
            
            # Add a container for better button handling
            button_container = st.container()
            with button_container:
                if st.button(f"{option_key}: {option_text}", key=button_key):
                    # Call the answer_selected function
                    answer_selected(option_key, q_id)
                    # Force rerun to update the UI
                    st.rerun()
   
    else:
        user_answer = st.session_state.answers[q_id]
        for option_key, option_text in question["options"].items():
            is_correct = option_key == question["correct_answer"]
            user_selected = option_key == user_answer
            
            if user_selected and is_correct:
                st.success(f"{option_key}: {option_text} ✓")
            elif user_selected and not is_correct:
                st.error(f"{option_key}: {option_text} ✗")
            elif not user_selected and is_correct:
                st.warning(f"{option_key}: {option_text} (Correct Answer)")
            else:
                st.write(f"{option_key}: {option_text}")
        
        # Show explanation
        st.markdown("<div class='explanation-box'>", unsafe_allow_html=True)
        st.markdown("### Explanation")
        st.markdown(question["explanation"][user_answer])
        
        if user_answer != question["correct_answer"]:
            st.markdown("### Correct Answer")
            st.markdown(question["explanation"][question["correct_answer"]])
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.current_question_index > 0:
            if st.button("⬅️ Previous", key="prev_btn", help="Go to previous question"):
                go_to_previous_question()
                st.rerun()
    
    with col3:
        if st.session_state.current_question_index < len(st.session_state.selected_questions) - 1:
            next_text = "Next ➡️"
            if user_answered:
                if st.button(next_text, key="next_btn", help="Go to next question"):
                    go_to_next_question()
                    st.rerun()
            else:
                st.info("Please select an answer to continue")
        else:
            if user_answered:
                if st.button("Finish Quiz 🏁", key="finish_btn"):
                    st.session_state.quiz_complete = True
                    st.rerun()
            else:
                st.info("Please select an answer to complete the quiz")

# Display quiz results
def display_results():
    st.markdown("<div class='question-card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Quiz Results</h2>", unsafe_allow_html=True)
    
    # Calculate score directly from answers
    total_questions = len(st.session_state.selected_questions)
    answered_questions = len(st.session_state.answers)
    
    # Recalculate correct answers to ensure accuracy
    correct_answers = calculate_score()
    
    # Calculate percentage based on answered questions
    accuracy = (correct_answers / answered_questions) * 100 if answered_questions > 0 else 0
    
    # Calculate percentage based on total questions
    completion_percentage = (answered_questions / total_questions) * 100 if total_questions > 0 else 0
    
    # Time taken
    time_elapsed = datetime.now() - st.session_state.time_started
    minutes = time_elapsed.seconds // 60
    seconds = time_elapsed.seconds % 60
    
    # Display score
    st.markdown(f"<div class='stats-box'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### Your Score: {correct_answers}/{answered_questions}")
        st.markdown(f"### Accuracy: {accuracy:.1f}%")
    
    with col2:
        st.markdown(f"### Time Taken: {minutes}m {seconds}s")
        st.markdown(f"### Questions Answered: {answered_questions}/{total_questions} ({completion_percentage:.1f}%)")
    
    # Performance assessment
    if accuracy >= 80:
        st.success("Excellent! You have a strong understanding of AWS AI Practitioner concepts related to Generative AI.")
    elif accuracy >= 60:
        st.info("Good job! You have a reasonable understanding, but some areas of Generative AI need improvement.")
    else:
        st.warning("You might need more study on AWS AI Practitioner Generative AI concepts.")
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Category breakdown
    st.markdown("### Performance by Category")
    
    # Group answers by category
    category_performance = {}
    for question in st.session_state.selected_questions:
        q_id = str(question["id"])
        category = question.get("category", "General")
        
        if category not in category_performance:
            category_performance[category] = {"correct": 0, "total": 0, "answered": 0}
        
        if q_id in st.session_state.answers:
            category_performance[category]["answered"] += 1
            if st.session_state.answers[q_id] == question["correct_answer"]:
                category_performance[category]["correct"] += 1
        
        category_performance[category]["total"] += 1
    
    # Create DataFrame for category performance
    if category_performance:
        data = []
        for category, stats in category_performance.items():
            accuracy = (stats["correct"] / stats["answered"]) * 100 if stats["answered"] > 0 else 0
            data.append({
                "Category": category,
                "Questions": stats["total"],
                "Answered": stats["answered"],
                "Correct": stats["correct"],
                "Accuracy": f"{accuracy:.1f}%"
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    
    # Question breakdown
    st.markdown("### Question Breakdown")
    
    for question in st.session_state.selected_questions:
        q_id = str(question["id"])
        user_answer = st.session_state.answers.get(q_id, "Not answered")
        is_correct = user_answer == question["correct_answer"] if q_id in st.session_state.answers else False
        
        with st.expander(f"Question {question['id']}: {question['question'][:100]}..."):
            st.write(question["question"])
            st.write(f"**Your answer:** Option {user_answer}")
            st.write(f"**Correct answer:** Option {question['correct_answer']}")
            st.write(f"**Result:** {'✓ Correct' if is_correct else '✗ Incorrect' if user_answer != 'Not answered' else '⚠️ Not Answered'}")
            
            # Show explanation
            st.markdown("### Explanation")
            if q_id in st.session_state.answers:
                st.markdown(question["explanation"][user_answer])
                
                if user_answer != question["correct_answer"]:
                    st.markdown("### Correct Answer")
                    st.markdown(question["explanation"][question["correct_answer"]])
            else:
                st.markdown(question["explanation"][question["correct_answer"]])
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Review Questions", key="review_btn", help="Review your answers"):
            st.session_state.quiz_complete = False
            st.session_state.current_question_index = 0
            st.rerun()
    
    with col2:
        if st.button("New Quiz", key="new_quiz_btn", help="Start a new quiz with different questions"):
            reset_quiz()
            select_random_questions(st.session_state.total_questions)
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
