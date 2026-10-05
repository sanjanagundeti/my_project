from sentence_transformers import SentenceTransformer
import chromadb
model =SentenceTransformer("all-MiniLM-L6-v2")
with open("ai_sample.txt", "r") as f:
    text = f.read()
#for line in text:
#  print(line)
# print(text)
# print("no.of characters",len(text))
chunks=[]
chunk_size=25
chunk_overlap=10
step=chunk_size - chunk_overlap
for i in range(0, len(text), chunk_size):
    chunk=text[i:i+chunk_size]
    chunks.append(chunk)
# print("no.of chunks:",len(chunks))
# for chunk in chunks:
#     print(f"chunk{i} -> {chunks[i]}")

#embedding
embeddings= model.encode(chunks)
# print("embedding created successfully")
# print("no.of embeddings",len(embeddings))
# print(embeddings[0])
#print(embeddings.shape)

#chroma db
client =chromadb.Client()
collection = client.create_collection(name="My_documents")
print("colection created successfully.")
ids=[]
for i in range(len(chunks)):
    ids.append(str(i))
collection.add(
    ids = ids,
    documents=chunks,
    embeddings=embeddings.tolist()
)
print("no.of collections:",collection.count())
result=collection.get()
for i in range(len(result["ids"])):
    print(f"ID:{result['ids'][i]} -> chunk : {result['documents'][i]}")
chunk1=collection.get(ids=['0'])
print(chunk1)