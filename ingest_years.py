import os
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge_base"
PERSIST_DIR = BASE_DIR / "data" / "chroma"

COLLECTION_NAME = "vardhaman-docs"

def ingest_year_files():
    client = chromadb.PersistentClient(path=str(PERSIST_DIR))

    embedding_function = OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small",
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
    )

    documents = []
    metadatas = []
    ids = []

    for year_file in KNOWLEDGE_DIR.glob("year*.txt"):
        year = year_file.stem  # year1, year2, etc.

        with open(year_file, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            continue

        documents.append(content)
        metadatas.append({"year": year})
        ids.append(year)

    if not documents:
        raise ValueError("No year-wise text files found or files are empty.")

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
    )

    print("✅ Year-wise data successfully ingested into ChromaDB")

if __name__ == "__main__":
    ingest_year_files()
