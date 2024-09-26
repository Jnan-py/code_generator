import streamlit as st 
import google.generativeai as genai
# import torch 
# from diffusers import pipeline
import os
from dotenv import load_dotenv 

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.title("CodeGenerator")
st.write("**This is a CODE GENERATOR but not a CHAT BOT**")

code_lang = st.selectbox(
    "Select the coding language you are interested to solve",
    options= ["Python","Java","HTML","C+","CSS"],
)

if code_lang:
    if 'chats' not in st.session_state:
        st.session_state.chats = []
        st.session_state.chats.append({
            'role':'assistant','content': f'I am a Code generating Bot, Select the required language and Provide me the Questions to solve !!'
        })

    for msgs in st.session_state.chats:
        st.chat_message(msgs['role']).markdown(msgs['content'])


    prompt = st.chat_input("Enter the code you need to generate")

    if prompt:
        st.chat_message('user').markdown(prompt)
        st.session_state.chats.append({
            'role':'user','content':prompt
        })

        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction= f"You are a proficient and accurate {code_lang} code generating bot, and you can provide only the solutions related to {code_lang} language, you don't know any other language exceot {code_lang}",
            tools='code_execution'
        )
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                max_output_tokens=1000,
                # stop_sequences=[1]
            )
        )
    #         pipe = pipeline('text-generation',model = "GuillenLuis03/PyCodeGPT")
    #         gen_text = pipe(
    #              prompt,
    #              do_sample = True, 
    #              temperature = 0.7,
    #              max_length = 500
    #         )[0]['generated_text']

        st.subheader(f"The generated code in {code_lang}")
        st.chat_message('assistant').markdown(response.text)
        st.session_state.chats.append({
            'role':'assistant','content':response.text
        })