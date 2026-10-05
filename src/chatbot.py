import ollama


def generate_answer(question, context):

    prompt = f"""
You are an AI Study Assistant.

Answer the student's question using the study notes provided below.

If the answer is not present in the notes, clearly say:
"I could not find the answer in the provided study material."

Study Notes:
{context}

Student Question:
{question}

Give the answer in simple and easy-to-understand language.
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]