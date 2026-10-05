
from sentence_transformers import SentenceTransformer
import chromadb,ollama
model = SentenceTransformer("all-MiniLM-L6-v2")
file_name="sample1.txt"
with open("sample1.txt","r") as file:
    text = file.read()
chunks = []
chunk_size = 25
chunk_overalap = 10
step = chunk_size - chunk_overalap
for  i in range(0, len(text), step):
    chunk =  text[i:i+chunk_size]
    chunks.append(chunk)
embeddings = model.encode(chunks)
client = chromadb.PersistentClient(path="./chroma_db")
client.delete_collection("my_documents")
collection = client.create_collection(name="my_documents")
ids=[] 
for i in range(len(chunks)):
    ids.append(f"{file_name}_{i}")
collection.add(
    ids = ids,
    documents = chunks,
    embeddings=embeddings
)

#query phase
question = input("enter a questions:")
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
print(response["message"]["content"])