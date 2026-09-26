import  ollama
import streamlit as st
st.title("Welcome to my chatbot app!!!")
if "messages" not in st.session_state:
    st.session_state.messages=[]
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
            st.write(msg["content"])
question=st.chat_input("You:")
if question:
    st.session_state.messages.append(
            {"role":"user",
            "content":question}
        )
    with st.chat_message("user"):
        st.write(question)
    with st.spinner("Thinking..."):
        response=ollama.chat(
            model="llama3.2:3b",
            messages=st.session_state.messages)
    st.session_state.messages.append(
            {"role": "assistant",
            "content":response["message"]["content"]}
        )
    with st.chat_message("assistant"):
        st.write(response["message"]["content"])
with st.sidebar:
    uploaded_file=st.file_uploader("uploaded a text file...")
    if uploaded_file:
        st.write("file uploaded successfully")
        context=uploaded_file.read().decode("utf-8")
        st.text(context)
    