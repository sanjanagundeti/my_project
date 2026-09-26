import streamlit as st
st.title("My first Streamlit App!!!")
st.header("simple application")
st.subheader("streamlit")
st.write("Welcome to my AI application!")
name=st.text_input("Enter your name: ")
st.write("Hello",name)