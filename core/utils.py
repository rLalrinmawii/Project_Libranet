# libranet/utils.py
import openai
from .models import Book
import numpy as np
from langchain_openai import OpenAIEmbeddings

import os
from dotenv import load_dotenv

load_dotenv()  # Loads environment variables from .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# openai_key = "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"

## Turn texts into vectors/numbers in the database
def generate_embeddings_for_books():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    books = Book.objects.all()
    for book in books:
        text = f"{book.title} {book.description or ''} {book.categories or ''}"
        book_embedding = embeddings.embed_query(text)
        # Save or update the embedding in the database
        book.embedding = book_embedding
        book.save()
        print("the embeddings are sucessfully saved")

def search_similar_books(user_query):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    query_embedding = embeddings.embed_query(user_query)

    books = Book.objects.all()
    similarities = []

    for book in books:
        if book.embedding:  # Ensure the book has an embedding
            similarity = np.dot(query_embedding, book.embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(book.embedding)
            )
            similarities.append((book, similarity))

    # Sort books by similarity score, descending
    similarities.sort(key=lambda x: x[1], reverse=True)
    recommended_books = [book for book, _ in similarities[:10]]  # Top 7 recommendations
    return recommended_books