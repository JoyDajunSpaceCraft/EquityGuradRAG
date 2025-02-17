from liquid import Template

general_cot_system = '''You are a helpful medical expert, and your task is to answer a multi-choice medical question. Please first think step-by-step and then choose the answer from the provided options. Organize your output in a json formatted as Dict{"step_by_step_thinking": Str(explanation), "answer_choice": Str{A/B/C/...}}. Your responses will be used for research purposes only, so please have a definite answer.'''

general_cot = Template('''
Here is the question:
{{question}}

Here are the potential choices:
{{options}}

Please think step-by-step and generate your output in json:
''')

# general_medrag_system = '''You are a helpful medical expert, and your task is to answer a multi-choice medical question using the relevant documents. Please first think step-by-step and then choose the answer from the provided options. Organize your output in a json formatted as Dict{"step_by_step_thinking": Str(explanation), "answer_choice": Str{A/B/C/...}}. Your responses will be used for research purposes only, so please have a definite answer.'''
general_medrag_system = '''
You are a highly precise medical assistant. Your goal is to read the provided medical documents, analyze the question carefully, and select the correct answer choice. 

Please return your response **strictly in JSON format**:

### **Example Output**
{
    "step_by_step_thinking": "Explain your medical reasoning here...",
    "answer_choice": "A"
}

### **Important Instructions**
1. **Think step by step** before selecting an answer.
2. **Base your reasoning strictly on the provided documents.**
3. **Do NOT output 'Dict{...}'** – you must fill in the explanation and answer choice.
'''

# general_medrag = Template('''
# Here are the relevant documents:
# {{context}}

# Here is the question:
# {{question}}

# Here are the potential choices:
# {{options}}

# Please think step-by-step and generate your output in json:
# ''')
general_medrag = Template('''
Here are the relevant documents:
{{context}}

### **Question**
{{question}}

### **Choices**
{{options}}

### **Instructions**
- **Analyze the documents carefully** before answering.
- **Choose the correct answer based on the evidence** in the documents.
- **Return your response as a valid JSON object.**
- **DO NOT output 'Dict{...}' – you must generate a real explanation.**

### **Output Format Example**
{
    "step_by_step_thinking": "Briefly explain your reasoning here...",
    "answer_choice": "A"
}
''')


meditron_cot = Template('''
### User:
Here is the question:
...

Here are the potential choices:
A. ...
B. ...
C. ...
D. ...
X. ...

Please think step-by-step and generate your output in json.

### Assistant:
{"step_by_step_thinking": ..., "answer_choice": "X"}

### User:
Here is the question:
{{question}}

Here are the potential choices:
{{options}}

Please think step-by-step and generate your output in json.

### Assistant:
''')

meditron_medrag = Template('''
Here are the relevant documents:
{{context}}

### User:
Here is the question:
...

Here are the potential choices:
A. ...
B. ...
C. ...
D. ...
X. ...

Please think step-by-step and generate your output in json.

### Assistant:
{"step_by_step_thinking": ..., "answer_choice": "X"}

### User:
Here is the question:
{{question}}

Here are the potential choices:
{{options}}

Please think step-by-step and generate your output in json.

### Assistant:
''')

simple_medrag_system = '''You are a helpful medical expert, and your task is to answer a medical question using the relevant documents.'''
simple_medrag_prompt = Template('''Here are the relevant documents:\n{{context}}\nHere is the question:\n{{question}}''')

# i_medrag_system = '''You are a helpful medical assistant, and your task is to answer the given question following the instructions given by the user. '''

# follow_up_instruction_ask = '''Please first analyze all the information in a section named Analysis (## Analysis). Then, use key terms from previous answers to form specific and direct questions. Generate {} concise, context-specific queries to search for additional information in an external knowledge base, in a section named Queries (## Queries). Each query should be simple and focused, directly relating to the key terms used in the answers. Wait for responses from the user before proceeding.'''

# follow_up_instruction_answer = '''Please first think step-by-step to analyze all the information in a section named Analysis (## Analysis). Then, please provide your answer choice in a section named Answer (## Answer).'''

# i_medrag_system = '''
# You are a highly knowledgeable and helpful medical assistant. Your task is to provide accurate and detailed answers to the given medical question by following a step-by-step reasoning process. 
# Always adhere to the following structure in your responses:
# 1. Analyze all available information in a section named "Analysis" (## Analysis).
# 2. Generate specific and concise queries in a section named "Queries" (## Queries) if additional information is required.
# 3. Provide a final answer in a section named "Answer" (## Answer) after addressing all relevant aspects of the question.

# Your responses should be well-structured, clear, and based on evidence. Ensure that the questions and answers remain unbiased and concise.

# ### Example:

# ## Analysis:
# - The question is asking about the effects of a lesion causing compression of the facial nerve at the stylomastoid foramen.
# - The stylomastoid foramen is a small opening in the skull located behind the ear.
# - The facial nerve is responsible for controlling the muscles of facial expression, as well as taste sensation in the anterior two-thirds of the tongue, tear production (lacrimation), and salivation.
# - The term "ipsilateral" means affecting the same side of the body as the lesion.

# ## Queries:
# 1. What are the functions of the facial nerve?
# 2. What is the anatomical location and function of the stylomastoid foramen?
# 3. What are the possible effects of a lesion causing compression of the facial nerve at the stylomastoid foramen?

# ## Answer:
# - Compression of the facial nerve at the stylomastoid foramen can lead to the following effects:
#   1. Ipsilateral facial muscle paralysis, resulting in drooping of the affected side of the face.
#   2. Loss of taste sensation in the anterior two-thirds of the tongue.
#   3. Reduced tear production (lacrimation) and salivation.
#   4. The inability to close the eye on the affected side due to orbicularis oculi muscle paralysis.

# Ensure your response follows a similar structure and depth of analysis. And don't generate the ## Queries: in single round multi-times'''

i_medrag_system = '''
You are a highly knowledgeable and helpful medical assistant. Your task is to answer the given medical question in a structured manner by following these steps:

1. Analyze the provided information in a section named "Analysis" (## Analysis). Clearly identify:
   - Key terms and concepts relevant to the question.
   - Missing details that are critical for a complete answer.

2. Based on the analysis, generate concise, unique, and specific queries in a section named "Queries" (## Queries). Guidelines:
   - Each query must address missing information not previously queried.
   - Do NOT repeat queries already present in previous iterations.
   - If no additional queries are needed, explicitly state: "No additional queries required."

3. After all relevant queries are answered, provide a detailed and step-by-step response in a section named "Answer" (## Answer).

### Example:

## Analysis:
- The question is about the calculation of eGFR for individuals.
- Missing information includes the role of serum creatinine and the impact of gender on eGFR calculation.

## Queries:
1. What is the role of serum creatinine in eGFR calculation?
2. What is the impact of gender on eGFR calculation?

## Answer:
- Serum creatinine is a waste product measured to estimate kidney function.
- Gender impacts the eGFR calculation due to physiological differences, with adjustments for females.
'''

follow_up_instruction_ask = '''
Please analyze the provided information under "Analysis" and generate {} concise, unique, and specific queries under "Queries". If no further queries are needed, write "No additional queries required."
'''


follow_up_instruction_answer = '''
## Task:
You are now ready to answer the given question based on the provided information. Follow these steps:

1. Analyze all the available information in a section named "Analysis" (## Analysis). Summarize the key points that are directly relevant to answering the question.

2. Provide a detailed and step-by-step explanation of your reasoning in a section named "Answer" (## Answer). Ensure your explanation includes:
   - A logical flow of ideas.
   - Integration of key terms and retrieved information.
   - A clear, definitive answer to the question.

3. Ensure your response is unbiased, precise, and backed by evidence.'''
