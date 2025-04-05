import streamlit as st
import jsonlines  
import boto3


def set_page_config():
    st.set_page_config( 
    page_title="Fine Tuning",  
    page_icon=":rock:",
    layout="wide",
    initial_sidebar_state="expanded",
)
    
def bedrock_runtime_client(region='us-east-1'):
    bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name=region, 
    )
    return bedrock_runtime

def bedrock_client(region='us-east-1'):
    bedrock = boto3.client(
    service_name='bedrock',
    region_name=region, 
    )
    return bedrock

def load_jsonl(file_path):
    d = []
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            d.append(obj)
    return d

def initsessionkeys(dataset):
    for key in dataset.keys():
        # print(key)
        if key not in st.session_state:
            st.session_state[key] = dataset[key]
    # print(st.session_state)
    return st.session_state

def update_options(dataset,item_num):
    for key in dataset[item_num]:
        if key in ["model","temperature","top_p","top_k","max_tokens"]:
            continue
        else:
            st.session_state[key] = dataset[item_num][key]
        # print(key, dataset[item_num][key])

def load_options(dataset,item_num):    
    # dataset = load_jsonl('mistral.jsonl')
    st.write("Prompt:",dataset[item_num]["prompt"])
    if "negative_prompt" in dataset[item_num].keys():
        st.write("Negative Prompt:", dataset[item_num]["negative_prompt"])
    st.button("Load Prompt", key=item_num, on_click=update_options, args=(dataset,item_num))  

bedrock = bedrock_client()

def get_provisioned_models():
    
    try:
        provisioned_model_throughput_id = bedrock.list_provisioned_model_throughputs()
        models = []
        for model in provisioned_model_throughput_id['provisionedModelSummaries']:
            if model['status'] in ['InService']:
                models.append(model['provisionedModelArn'])
    except Exception as e:
        # print(e)
        models = []
        pass    
    return models

def get_provisioned_model_id():
    try:
        provisioned_model_throughput_id = bedrock.list_provisioned_model_throughputs()
        
        status =  provisioned_model_throughput_id['provisionedModelSummaries'][0]['status']
        
        if status in ['Creating', 'Updating', 'InService']:
            id = provisioned_model_throughput_id['provisionedModelSummaries'][0]['provisionedModelArn']
        else:
            id = None
    except Exception as e:
        # print(e)
        id = None
        pass
        
    return id

def get_models(provider):

   # Let's see all available Amazon Models
    available_models = bedrock.list_foundation_models()

    models = []

    for each_model in available_models['modelSummaries']:
        if provider in each_model['providerName']:
            models.append(each_model['modelId'])
    models.pop(0)

    return models

def list_jobs(customizationType):
    try:
        list_jobs = []
        jobs = bedrock.list_model_customization_jobs()
        for job in jobs['modelCustomizationJobSummaries']:
            if job['customizationType'] == customizationType:
                list_jobs.append(job['jobName'])
    
    except Exception as e:
        st.warning(f"Error, {str(e)}")
        st.stop()

    return list_jobs[0:2]

def set_defaults():
    for key in st.session_state.keys():
        del st.session_state[key]
        
        
def getmodelparams(providername):
    model_mapping = {
        "Amazon": {
            "maxTokenCount": 1024,
            "stopSequences": [],
            "temperature": 0.1,
            "topP": 0.9
        },
        "Anthropic": {
            "max_tokens_to_sample": 1024,
            "temperature": 0.1,
            "top_k": 50,
            "top_p": 0.9,
            "stop_sequences": ["\n\nHuman"],
        },
        "Claude 3": {
            "max_tokens": 1024,
            "temperature": 0.1,
            "top_k": 50,
            "top_p": 0.9,
            "stop_sequences": ["\n\nHuman"],
            
        },
        "AI21": {
            "maxTokens": 1024,
            "temperature": 0.1,
            "topP": 0.9,
            "stopSequences": [],
            "countPenalty": {
                "scale": 0
            },
            "presencePenalty": {
                "scale": 0
            },
            "frequencyPenalty": {
                "scale": 0
            }
        },
        "Cohere": {
            "max_tokens": 1024,
            "temperature": 0.1,
            "p": 0.9,
            "k": 50,
            "stop_sequences": [],
            "return_likelihoods": "NONE"
        },
        "Meta": {
            'max_gen_len': 1024,
            'top_p': 0.9,
            'temperature': 0.1
        },
        "Mistral": {
            'max_tokens': 1024,
            'temperature': 0.1,
            'top_p': 0.9
        }
    }

    return model_mapping[providername]

list_providers = ['Amazon', 'Anthropic',
                  'Claude 3', 'Cohere', 'Meta', 'Mistral']

def getmodelId(providername):
    model_mapping = {
        "Amazon": "amazon.titan-tg1-large",
        "Titan Image": "amazon.titan-image-generator-v1",
        "Anthropic": "anthropic.claude-v2:1",
        "Claude 3": "anthropic.claude-3-sonnet-20240229-v1:0",
        'Cohere': "cohere.command-text-v14",
        'Meta': "meta.llama2-70b-chat-v1",
        "Mistral": "mistral.mixtral-8x7b-instruct-v0:1",
        "Stability AI": "stability.stable-diffusion-xl-v1",
        "Anthropic Claude 3": "anthropic.claude-3-sonnet-20240229-v1:0"
    }

    return model_mapping[providername]


def getmodelIds(providername):
    models = []
    bedrock = client()
    available_models = bedrock.list_foundation_models()

    if providername == "Claude 3":
        for model in available_models['modelSummaries']:
            if 'claude-3' in model['modelId'].split('.')[1]:
                models.append(model['modelId'])
    else:
        for model in available_models['modelSummaries']:
            if providername in model['providerName']:
                models.append(model['modelId'])

    return models

def client(region='us-east-1'):
    return boto3.client(
        service_name='bedrock',
        region_name=region
    )