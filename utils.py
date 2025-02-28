import pandas as pd
from dotenv import load_dotenv
import os
import zipfile

from chromadb import PersistentClient
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


# Dataset class
class Dataset:
    def __init__(self, file_path):
        self.file_path = file_path
        self.dataset = pd.read_csv(file_path)

    def get_dataset(self):
        return self.dataset

    def __len__(self):
        return len(self.dataset)


# Function to set environment variable
def set_env():
    try:
        if not os.environ.get("GROQ_API_KEY"):
            load_dotenv()
            os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
            print("Environment variable set successfully.")
        else:
            print("Environment variable already set.")
    except FileNotFoundError:
        print("Error setting environment variable.")
        print("Please create a .env file with the GROQ_API_KEY variable")


# Function to unzip zipped database
def unzip_database_file(zip_path, extract_to):
    try:
        # Check if extraction folder exists and is not empty
        if os.path.exists(extract_to) and os.listdir(extract_to):
            print(f"Skipping extraction: '{extract_to}' already contains files.")
            return

        # Ensure the extraction directory exists
        os.makedirs(extract_to, exist_ok=True)

        # Extract the ZIP file
        with zipfile.ZipFile(zip_path, "r") as zipf:
            zipf.extractall(extract_to)

        print(f"Extracted to: {extract_to}")

    except zipfile.BadZipFile:
        print(
            "Error: File could not be unzipped! It might be corrupted or not a valid ZIP file."
        )
    except FileNotFoundError:
        print("Error: ZIP file not found. Please check the path.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Function to retrieve chromadb collection
def retrive_chroma_collection(path: str):
    chroma_client = PersistentClient(path)
    collection = chroma_client.get_or_create_collection(
        "fashion_data",
        embedding_function=DefaultEmbeddingFunction(),
    )
    return collection


# Function to retrieve data similar to a given query
def get_similar_data(collection, question: str, top_k: int = 1):
    response = collection.query(
        query_texts=[question],
        n_results=top_k,
    )
    return response["metadatas"][0][0]["response"]
