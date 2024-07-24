# Reference - https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps

# 1: Translation
# 2: Summarization
# 3. Question Answering
# 4. Definitions

import json
import requests
import streamlit as st

from PIL import Image

# Read OpenAI key
with open("apikey.txt") as file_reader:
    OPENAI_API_KEY = file_reader.read()

# Read sample data files
with open("data/loan_estimate.txt") as file_reader:
    loan_estimate_data = file_reader.read()

with open("data/closing_disclosure.txt") as file_reader:
    closing_disclosure_data = file_reader.read()

with open("data/seller_disclosure.txt") as file_reader:
    seller_disclosure_data = file_reader.read()


# Display Loan Buddy Logo
col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    image = Image.open('static/loanbuddylogo.jpg')
    new_image = image.resize((200, 200))
    st.image(new_image)

with col3:
    st.write(' ')


def chat(prompt):
    url = "<ADD_URL_HERE>"
    escaped_prompt = json.dumps(prompt)
    payload = "{\"messages\": [{\"role\": \"user\", \"content\":" + escaped_prompt + "}], \"model\": \"gpt-4\", \"temperature\": \"0.0\", \"max_tokens\": \"100\"}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + OPENAI_API_KEY
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()['choices'][0]['message']['content']


language = st.selectbox("Choose preferred language", ["English", "Español (Spanish)", "français (French)", "Deutsch (German)", "Italiano (Italian)"])

if language == "English":
    st.title("Welcome! I am Loan Buddy")

    document = st.selectbox("Choose document", ["Loan Estimate", "Closing Disclosure", "Seller Disclosure"])

    st.subheader("Capabilities")
    summarize = st.checkbox("Summarize")
    define = st.checkbox("Define")
    ask = st.checkbox("Ask")

    if document == "Loan Estimate":
        data_choice = loan_estimate_data
    elif document == "Closing Disclosure":
        data_choice = closing_disclosure_data
    elif document == "Seller Disclosure":
        data_choice = seller_disclosure_data

    # Pass loan document as part of the prompt
    if summarize:
        prompt = f""""Instructions: You are a loan buddy. Your job is to explain the content of the document to a first time home buyer. 
        1. Be conversational. 
        2. Do not repeat anything. 
        3. Keep it professional. 
        4. Do not start with a greeting.
        5. Do no start with a prefix called Summary:
        6. Generate summary in English in third person. 
        Content : {data_choice}"""
        response = chat(prompt)
        st.subheader("Summary")
        st.write(response)

    elif ask:
        # Add text box
        question = st.chat_input("Enter your question here")

    elif define:
        # Add text box
        question = st.chat_input("Enter term that you want to know more about here")
        prompt = f"""
              Instructions: You are a loan buddy. Your job is to explain the content of the document to a first time home buyer. 
              1. Be conversational. 
              2. Do not repeat anything. 
              3. Keep it professional. 
              4. Do not start with a greeting.
              5. Provide definition of the term only if you are confident otherwise say contact your loan term
              Term : {question} 
              """
        response = chat(prompt)
        st.subheader("Definition")
        st.write(response)


elif language == "Español (Spanish)":
    st.title("Bienvenido! Soy amigo de préstamo")

    document = st.selectbox("Elegir documento", ["Estimación de préstamo", "Divulgación final", "Divulgación del vendedor"])

    st.subheader("Capacidades")
    summarize = st.checkbox("Resumir")
    define = st.checkbox("Definir")
    ask = st.checkbox("Pregunta")

    # Pass loan document as part of the prompt
    if summarize:
        if document == "Estimación de préstamo":
            data_choice = loan_estimate_data
        elif document == "Divulgación final":
            data_choice = closing_disclosure_data
        elif document == "Divulgación del vendedor":
            data_choice = seller_disclosure_data

        prompt = f""""Instructions: You are a loan buddy. Your job is to explain the content of the document to a first time home buyer. 
        1. Be conversational. 
        2. Do not repeat anything. 
        3. Keep it professional. 
        4. Translate the document to Spanish.
        5. Generate summary only in Spanish in third person. 
        6. Do not start with a greeting.
        7. Do no start with a prefix called Summary:
        Contenido : {data_choice}"""
        response = chat(prompt)
        st.subheader("Resumen")
        st.write(response)
