import uuid # Generate unique GUIDs for messages
from openai import OpenAI
import streamlit as st
from streamlit_chat import message

client = OpenAI(
    api_key="your api key"
)

st.set_page_config(page_title='Chat', page_icon=':whale2:')
st.markdown('# Welcome to Chat')
st.sidebar.header("Instruction")
st.sidebar.write('You have to type your question and wait for the answer from our respective ChatBot')


if 'messages' not in st.session_state:
    st.session_state['messages'] = []


def submit():
    user_input = st.session_state.input
    if user_input:
        user_msg = { # I must emphasize that messages from the user are tagged with ‘role = user’, while responses from the AI are tagged with ‘role = assistant’.
            'role': 'user', 
            'content': f'{user_input}' }
        st.session_state.messages.append(user_msg)

        res = get_answer(user_input)
        if res:
            generated_msg = { 
                'content': res['choices'][0]['message']['content'].strip(), 
                'role': 'assistant' }
            st.session_state.messages.append(generated_msg)
    st.session_state.input = ''


def get_answer(user_input):
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello world"}]
    )

st.text_input(label = 'Question', key = 'input', on_change=submit)


if st.session_state['messages']:
    for msg in reversed(st.session_state['messages']):
        key = f'{uuid.uuid4().hex}'
        if msg['role'] != 'user':
            message(msg['content'], avatar_style = 'bottts', key=key)
        else:
            message(msg['content'], avatar_style = 'lorelei-neutral', is_user=True, key=key)
