import os
import json
from llama_index.core import Document, VectorStoreIndex, StorageContext, Settings
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.gemini import Gemini
import chromadb
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configuration
ENRICHED_DATA_FILE = "processed_data/enriched_content.json"
CHROMA_DB_DIR = "chroma_db"
COLLECTION_NAME = "uzio_docs"

def build_index():
    if not os.path.exists(ENRICHED_DATA_FILE):
        print("Enriched data not found. Run processor.py first.")
        return

    # 1. Setup Models
    # Using text-embedding-004 for cost/performance if available, else 001
    Settings.embed_model = GeminiEmbedding(model_name="models/text-embedding-004", api_key=GOOGLE_API_KEY)
    Settings.llm = Gemini(model="models/gemini-2.0-flash-001", api_key=GOOGLE_API_KEY)

    # 2. Prepare Documents
    with open(ENRICHED_DATA_FILE, "r") as f:
        data = json.load(f)
    
    documents = []
    print(f"Loading {len(data)} items...")
    
    for item in data:
        # Compatibility mapping for manual vs auto-generated data
        text_content = item.get("content", "")
        source = item.get("source", item.get("file_name", "Unknown File"))
        doc_type = item.get("type", item.get("section_title", "Section"))
        
        # Add metadata
        metadata = {
            "source": source,
            "type": doc_type,
        }
        if "image_path" in item:
            metadata["image_path"] = item["image_path"]
        
        if "generated_questions" in item:
            questions = item["generated_questions"]
            # Handle list format from external prompt
            if isinstance(questions, list):
                questions = "\n".join(questions)
            
            text_content += "\n\nRelated Questions:\n" + str(questions)
        
        doc = Document(text=text_content, metadata=metadata)
        documents.append(doc)

    # 3. Initialize ChromaDB
    print("Initializing Vector Store...")
    db = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    chroma_collection = db.get_or_create_collection(COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 4. Create Index (Processing & Embedding)
    print("Building Index (this may take a moment)...")
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )
    
    print(f"Index created successfully at {CHROMA_DB_DIR}")

if __name__ == "__main__":
    build_index()
