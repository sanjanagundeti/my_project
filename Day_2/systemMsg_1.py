import ollama
question=input("Ask a question")
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role":"system",
            "content":"give answers in 2 lines only"
         },
         {
             "role":"user",
             "content":question
         }
    ]
)
print(response["message"]["content"])

