import ollama
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role":"user",
            "content":"plan a trip to goa"
        }
    ]
)
print(response["message"]["content"])
