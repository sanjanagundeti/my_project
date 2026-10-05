
import re
from collections import Counter


class EmbeddingModel:

    def __init__(self):
        self.vocabulary = set()

    def create_vector(self, text):
        words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
        return Counter(words)

    def fit_transform(self, documents):

        for document in documents:
            words = re.findall(
                r"\b[a-zA-Z]+\b",
                document.lower()
            )

            self.vocabulary.update(words)

        return [
            self.create_vector(document)
            for document in documents
        ]

    def transform(self, documents):

        return [
            self.create_vector(document)
            for document in documents
        ]