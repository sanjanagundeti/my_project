import ollama
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role":"user",
            "content":"Name only main types of AI with 2 examples and single line discription of each"
        }
    ]
)
print(response["message"]["content"])
