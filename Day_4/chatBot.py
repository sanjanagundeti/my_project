import  ollama
import streamlit as st
st.markdown("# Welcome to my chatbot app!!!")
with st.sidebar:
    st.subheader(":blue[chat setting]")
    if st.button("clear chat 🗑️"):
        st.session_state.messages=[ ]
        st.success("chat cleared successfully 🗑️")
    personalities={
        "kid": "answer the question like you are explaining to a 5 year old kid.give me answer in 2 lines only",
        "friend": "answer the question in a friendly and in a casual manner.give me answer in 2 lines only",
        "proffessor": "answer the question like you are answering to a proffessor.give me ansswer in 2 lines only"
    }
    uploaded_file=st.file_uploader("uploaded a text file...")
    personality=st.selectbox("select a personality",personalities.keys())
    try:
        if uploaded_file:
            context=uploaded_file.read().decode("utf-8")
            st.success("file uploaded successfully")
            if st.button("Display"):
                st.text(context)
    except:
        st.error("change the file")
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
            messages= [ 
                {"role":"system","content":personalities[personality]}
            ] + st.session_state.messages)s
    st.session_state.messages.append(
            {"role": "assistant",
            "content":response["message"]["content"]}
        )
    with st.chat_message("assistant"):
        st.write(response["message"]["content"])



    
    