import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

import re
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import chromadb
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = Path(__file__).parent / "chroma_db"

ACTIVE_COLLECTION_FILE = Path(__file__).parent / ".active_collection"


def get_active_collection() -> str | None:
    """Returns the currently active collection name, or None if none exists."""
    if ACTIVE_COLLECTION_FILE.exists():
        return ACTIVE_COLLECTION_FILE.read_text().strip() or None
    return None


def set_active_collection(name: str):
    """Persists the active collection name to disk."""
    ACTIVE_COLLECTION_FILE.write_text(name)


def make_collection_name(filename: str) -> str:
    stem = Path(filename).stem                     
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", stem)    
    slug = slug.strip("_").lower()[:60]            
    return slug or "document"


def index_document(file_name: str = "Nodejs.pdf", display_name: str | None = None) -> str:
    """
    Loads a PDF, chunks it, and saves it to a NEW Chroma collection.
    Deletes the previous collection so only one PDF is active at a time.
    Returns the new collection name.
    """
    pdf_path = Path(file_name)
    if not pdf_path.is_absolute():
        pdf_path = Path.cwd() / file_name

    print(f"[INFO] Initializing indexing process for: {pdf_path}")

    CHROMA_PATH.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    new_collection = make_collection_name(display_name or pdf_path.name)

    try:
       
        previous = get_active_collection()
        if previous:
            existing = [c.name for c in client.list_collections()]
            if previous in existing:
                print(f"[INFO] Deleting previous collection: '{previous}'")
                client.delete_collection(previous)

        
        loader = PyPDFLoader(file_path=str(pdf_path))
        docs = loader.load()
        print(f"[INFO] Loaded {len(docs)} pages from {pdf_path.name}")

        
        print("[INFO] Executing text splitting sequence...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=400
        )
        chunks = text_splitter.split_documents(documents=docs)
        print(f"[INFO] Created {len(chunks)} chunks.")

        
        print(f"[INFO] Writing to new Chroma collection: '{new_collection}'")
        embedding_models = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        Chroma.from_documents(
            documents=chunks,
            embedding=embedding_models,
            collection_name=new_collection,
            persist_directory=str(CHROMA_PATH)
        )

       
        set_active_collection(new_collection)
        print(f"[SUCCESS] Indexing complete. Active collection is now '{new_collection}'.")
        return new_collection

    except FileNotFoundError:
        print(f"[ERROR] Could not locate {pdf_path}. Verify the file exists.")
        raise
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    index_document()