import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_chroma import Chroma


import os

# Ensure paths are relative to the script's actual location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(
    BASE_DIR, "..", "CHROMA_DB"
)  # Assuming CHROMA_DB should be in /src/app
DATA_PATH = os.path.join(BASE_DIR, "..", "data")  # Resolves to /src/app/data


# CHROMA_PATH = "../CHROMA_DB"
# DATA_PATH = "../data"


def main():
    # Check if the database should be cleared (using the --clear flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)


def check_and_update_rag_database(chroma_path=CHROMA_PATH, data_path=DATA_PATH):
    # Check if the folder named chroma_path exists. If already exists, we will not create a new one.
    if not os.path.exists(chroma_path):
        print("Creating Chroma database...")
        # Create (or update) the data store.
        documents = load_documents(data_path)
        chunks = split_documents(documents)
        add_to_chroma(chunks=chunks, chroma_path=chroma_path)
        print("Chroma database created!")
    else:
        print("Chroma database already exists!")


def load_documents(data_path=DATA_PATH):
    # Print all the files in the data_path
    print(f"Loading documents from {data_path}")
    for root, dirs, files in os.walk(data_path):
        for file in files:
            print(os.path.join(root, file))
    document_loader = PyPDFDirectoryLoader(data_path)
    return document_loader.load()


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list[Document], chroma_path=CHROMA_PATH):
    # Load the existing database.
    db = Chroma(
        persist_directory=chroma_path, embedding_function=get_embedding_function()
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ No new documents to add")


from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
import openai
from langchain_openai import OpenAIEmbeddings
import os

# Get the key from OPENAI_API_KEY file
if os.path.exists("OPENAI_API_KEY"):
    with open("OPENAI_API_KEY", "r") as f:
        OPENAI_API_KEY = f.read().strip()
else:
    # If the file does not exist, check the environment variable
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")


def get_embedding_function():
    # embeddings = OllamaEmbeddings(model="nomic-embed-text")
    embeddings = OpenAIEmbeddings(
        api_key=OPENAI_API_KEY, model="text-embedding-3-small"
    )
    return embeddings


def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database(chroma_path=CHROMA_PATH):
    if os.path.exists(chroma_path):
        shutil.rmtree(chroma_path)


if __name__ == "__main__":
    main()
