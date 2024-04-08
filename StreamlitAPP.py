import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils  import read_file, get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

with open("C:\Users\Richa\OneDrive\Documents\Projects\Deployments\mcq_gen_ai\Response.json") as file:
    RESPONSE_JSON = json.load(file)

st.title("MCQ Generator")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Choose a file")
    mcq_count = st.number_input("Enter the number of MCQ's", min_value=3, value=50)
    subject = st.text_input("Enter the subject")
    tone = st.text_input("Enter the tone", placeholder="simple")
    button = st.form_submit_button("Generate MCQ's")

    if button and uploaded_file:
        with st.spinner("loading..."):
            try:
                text = read_file(uploaded_file)

                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dump(RESPONSE_JSON)
                        }
                    )
                
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total cost:{cb.total_cost}")

                if isinstance(response, dict):
                    quiz = response.get("quiz")
                    if quiz is not None:
                        table_data  = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Error getting table data")
                else:
                    st.write(response)