import ollama
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role":"user",
        }
    ]
)
print(response["message"]["content"])
