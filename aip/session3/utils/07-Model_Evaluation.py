import json
import streamlit as st
import boto3
from utils.code_based_grading import get_completion, build_input_prompt, grade_completion
import utils.human_based_grading as hbg
import utils.model_based_grading as mbg

# Page configuration with improved styling
st.set_page_config(
    page_title="LLM Prompt Components Guide",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1', 
    )


# Define our eval (in practice you might do this as a jsonl or csv file instead).
eval = [
    {
        "animal_statement": 'The animal is a human.',
        "golden_answer": '2'
    },
        {
        "animal_statement": 'The animal is a snake.',
        "golden_answer": '0'
    },
        {
        "animal_statement": 'The fox lost a leg, but then magically grew back the leg he lost and a mysterious extra leg on top of that.',
        "golden_answer": '5'
    }
]

human_eval = [
    {
        "question": 'Please design me a workout for today that features at least 50 reps of pulling leg exercises, at least 50 reps of pulling arm exercises, and ten minutes of core.',
        "golden_answer": 'A correct answer should include a workout plan with 50 or more reps of pulling leg exercises (such as deadlifts, but not such as squats which are a pushing exercise), 50 or more reps of pulling arm exercises (such as rows, but not such as presses which are a pushing exercise), and ten minutes of core workouts. It can but does not have to include stretching or a dynamic warmup, but it cannot include any other meaningful exercises.'
    },
    {
        "question": 'Send Jane an email asking her to meet me in front of the office at 9am to leave for the retreat.',
        "golden_answer": 'A correct answer should decline to send the email since the assistant has no capabilities to send emails. It is okay to suggest a draft of the email, but not to attempt to send the email, call a function that sends the email, or ask for clarifying questions related to sending the email (such as which email address to send it to).'
    },
    {
        "question": 'Who won the super bowl in 2024 and who did they beat?', # Claude should get this wrong since it comes after its training cutoff.
        "golden_answer": 'A correct answer states that the Kansas City Chiefs defeated the San Francisco 49ers.'
    }
]


tab1, tab2, tab3 = st.tabs(["Code-based Grading", "Human-based Grading", "Model-based Grading"])

with tab1:
    st.markdown("""#### Code-based Grading

Here we will be grading an eval where we ask Claude to successfully identify how many legs something has. We want Claude to output just a number of legs, and we design the eval in a way that we can use an exact-match code-based grader.
""")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Golden Answers")
        with st.container(border=True):
            st.write(eval)
        
        submit = st.button("Start Evaluation",type="primary", key=1)


    with col2:
        
        st.subheader("Evaluation")
        if submit:
            with st.spinner("Evaluating..."):
                for question in eval:
                    #st.write(build_input_prompt(question['animal_statement']))
                    output = get_completion(build_input_prompt(question['animal_statement']))
                    st.info(f"Animal Statement: {question['animal_statement']}\n\nGolden Answer: {question['golden_answer']}\n\nOutput: {output}\n")


                outputs = [get_completion(build_input_prompt(question['animal_statement'])) for question in eval]

                grades = [grade_completion(output, question['golden_answer']) for output, question in zip(outputs, eval)]
                #print(f"Score: {sum(grades)/len(grades)*100}%")
                        
                col1.metric("Score:",f"{sum(grades)/len(grades)*100}%", f"{sum(grades)} correct out of {len(grades)}")   


with tab2:
    st.markdown("""#### Human Grading

Now let's imagine that we are grading an eval where we've asked Claude a series of open ended questions, maybe for a general purpose chat assistant. Unfortunately, answers could be varied and this can not be graded with code. One way we can do this is with human grading.
""")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Golden Answers")
        with st.container(border=True):
            st.write(human_eval)
        
        submit = st.button("Start Evaluation",type="primary", key=2)


    with col2:
        
        st.subheader("Evaluation")
        if submit:
            with st.spinner("Evaluating..."):
                for question in human_eval:
                    #st.write(build_input_prompt(question['question']))
                    output = hbg.get_completion(hbg.build_input_prompt(question['question']))
                    st.info(f":orange[Question:] {question['question']}\n\n:orange[Golden Answer:] {question['golden_answer']}\n\n:orange[Output:] {output}\n")


with tab3:
    st.markdown("""#### Model-based Grading

Having to manually grade the above eval every time is going to get very annoying very fast, \
especially if the eval is a more realistic size (dozens, hundreds, or even thousands of questions). \
Luckily, there's a better way! We can actually have Claude do the grading for us. \
Let's take a look at how to do that using the same eval and completions from Human Grading.
""")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Golden Answers")
        with st.container(border=True):
            st.write(human_eval)
        
        submit = st.button("Start Evaluation",type="primary", key=3)


    with col2:
        
        st.subheader("Evaluation")
        if submit:
            with st.spinner("Evaluating..."):
                # for question in human_eval:
                #     #st.write(build_input_prompt(question['question']))
                #     output = hbg.get_completion(hbg.build_input_prompt(question['question']))
                #     st.info(f":orange[Question:] {question['question']}\n\n:orange[Golden Answer:] {question['golden_answer']}\n\n:orange[Output:] {output}\n")

                # Get completions for each question in the eval.
                outputs = [hbg.get_completion(hbg.build_input_prompt(question['question'])) for question in human_eval]

                grades = [mbg.grade_completion(output, question['golden_answer']) for output, question in zip(outputs, human_eval)]
                col1.metric("Score:", f"{grades.count('correct')/len(grades)*100}%", f"{grades.count('correct')} correct out of {len(grades)}")