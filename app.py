import streamlit as st

from src.document_loader import load_text_file
from src.chunking import split_text
from src.embedding import EmbeddingModel
from src.semantic_search import search
from src.chatbot import generate_answer


st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)


st.title("📚 AI Study Assistant")
st.write("Upload your study material and ask questions using semantic search.")


# Initialize session state
if "documents" not in st.session_state:
    st.session_state.documents = []

if "embedding_model" not in st.session_state:
    st.session_state.embedding_model = EmbeddingModel()

if "document_vectors" not in st.session_state:
    st.session_state.document_vectors = None


# Sidebar
st.sidebar.header("📂 Study Material")

uploaded_file = st.sidebar.file_uploader(
    "Upload a TXT file",
    type=["txt"]
)


if uploaded_file is not None:

    if st.sidebar.button("Process Notes"):

        text = load_text_file(uploaded_file)

        chunks = split_text(text)

        if not chunks:

            st.error("The uploaded file is empty.")

        else:

            embedding_model = st.session_state.embedding_model

            vectors = embedding_model.fit_transform(chunks)

            st.session_state.documents = chunks
            st.session_state.document_vectors = vectors

            st.success(
                f"{len(chunks)} study chunks created successfully!"
            )


# Show uploaded notes
if st.session_state.documents:

    st.subheader("📄 Study Material")

    st.write(
        f"Number of chunks: {len(st.session_state.documents)}"
    )


# Question section
st.subheader("💬 Ask a Question")

question = st.text_input(
    "Enter your question:"
)


if st.button("Ask AI"):

    if not st.session_state.documents:

        st.warning("Please upload and process your study material first.")

    elif not question:

        st.warning("Please enter a question.")

    else:

        embedding_model = st.session_state.embedding_model

        results = search(
            question,
            st.session_state.documents,
            embedding_model,
            st.session_state.document_vectors,
            top_k=3
        )

        context = "\n\n".join(
            result["text"]
            for result in results
        )

        with st.spinner("Thinking..."):

            answer = generate_answer(
                question,
                context
            )

        st.subheader("🤖 AI Answer")

        st.write(answer)


        st.subheader("🔎 Relevant Study Material")

        for i, result in enumerate(results):

            with st.expander(
                f"Result {i + 1} - Similarity: {result['score']:.2f}"
            ):

                st.write(result["text"])