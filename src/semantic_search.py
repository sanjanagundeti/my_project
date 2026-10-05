
import math


def cosine_similarity(vector1, vector2):

    common_words = set(vector1) & set(vector2)

    numerator = sum(
        vector1[word] * vector2[word]
        for word in common_words
    )

    magnitude1 = math.sqrt(
        sum(value ** 2 for value in vector1.values())
    )

    magnitude2 = math.sqrt(
        sum(value ** 2 for value in vector2.values())
    )

    if magnitude1 == 0 or magnitude2 == 0:
        return 0

    return numerator / (magnitude1 * magnitude2)


def search(query, documents, embedding_model, document_vectors, top_k=3):

    query_vector = embedding_model.transform([query])[0]

    similarities = []

    for document_vector in document_vectors:

        score = cosine_similarity(
            query_vector,
            document_vector
        )

        similarities.append(score)

    ranked_indexes = sorted(
        range(len(similarities)),
        key=lambda i: similarities[i],
        reverse=True
    )

    results = []

    for index in ranked_indexes[:top_k]:

        results.append({
            "text": documents[index],
            "score": similarities[index]
        })

    return results
