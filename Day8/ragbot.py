
from sentence_transformers import SentenceTransformer
import chromadb,ollama,streamlit as st
@st.cache_resource
def load_model():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model
model=load_model()
st.title("My chatbot")
if "messages" not in st.session_state:
    st.session_state.messages=[]
with st.sidebar:
    with st.sidebar:
        st.subheader(":blue[chat setting]")
        if st.button("clear chat 🚮"):
            st.session_state.messages=[ ]
            st.success("chat cleared successfully ✅")
        personalities={
            "kid" : "answer the question like you are explaining to a 5 year old kid.give me anser in 2 lines only",
            "friend" : "answer the question in a friendly and casual manner.give me answer in 2 lines only"
        }
        personality=st.selectbox("select a personality",personalities.keys())
        uploaded_file=st.file_uploader("Upload a file")
    if uploaded_file:
        text=uploaded_file.read().decode("utf-8")
        with st.expander("Preview"):
            st.text(text)
        chunks = []
        chunk_size = 25
        chunk_overalap = 10
        step = chunk_size - chunk_overalap
        for  i in range(0, len(text), step):
            chunk =  text[i:i+chunk_size]
            chunks.append(chunk)
        embeddings = model.encode(chunks)
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_or_create_collection(name="my_documents")
        ids=[] 
        for i in range(len(chunks)):
            ids.append(f"{uploaded_file.name}_{i}")
        collection.add(
            ids = ids,
            documents = chunks,
            embeddings=embeddings.tolist()
        )

#query phase
question = st.chat_input("Enter a question:")
if question:
    if uploaded_file:

        with st.chat_message("user"):
            st.write(question)
        question_embedding = model.encode(question)
        results=collection.query(
            query_embeddings=[question_embedding.tolist()],
            n_results=3
        )
        retrieved_result = results['documents'][0]
        retrieved_ids=results['ids'][0]
        # prompting 
        context ='\n'.join (retrieved_result)


        prompt=  f'''
        Answer the question using the context provided below.
        Question : {question}
        Context : {context}
        Answer:
        '''
        #Connecting to Local Model
        response = ollama.chat(
            model="llama3.2:3b",
            messages = [{
                "role":"user",
                "content":prompt
            }]
        )
        with st.chat_message("assistant"):
            st.write(response["message"]["content"])
    else:
        with st.chat_message("user"):
            st.write(question)
        with st.spinner("Thinking..."):
            response=ollama.chat(
                model="llama3.2:3b",
                messages=[
                    {"role": "system","content":"give answer in 2 lines only."}]
                        + st.session_state.messages)
        st.session_state.messages.append(
                {"role": "assistant",
                "content":response["message"]["content"]}
            )
        with st.chat_message("assistant"):
            st.write(response["message"]["content"])