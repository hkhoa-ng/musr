from tools.rag_database import get_embedding_function

# from rag_database import get_embedding_function
from langchain_chroma import Chroma
from colorama import Fore
import re

import os

# Ensure paths are relative to the script's actual location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(BASE_DIR, "..", "CHROMA_DB")


def clean_text(text):
    # Remove excessive spaces between characters and words
    cleaned_text = re.sub(r"(\w) (\w)", r"\1\2", text)  # Join split words
    cleaned_text = re.sub(r" +", " ", cleaned_text)  # Remove extra spaces
    return cleaned_text.strip()


def get_related_context(query_text: str):
    """Using RAG technique to get related context from the vector database.The related information is from the company and project documents, e.g., product overview, company overview, tech stacks, product MVP, etc."""
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    return "\n\n---\n\n".join([doc.page_content for doc, _score in results])


def main():
    result = get_related_context(
        "Please provide context about the product ALFRED, its functionalities, and the target audience to help in grouping the user stories effectively."
    )
    print(type(result))
    print(result)


if __name__ == "__main__":
    main()
