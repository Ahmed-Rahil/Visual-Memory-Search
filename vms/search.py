import chromadb
from sentence_transformers import SentenceTransformer
import argparse
import time

# --- Configuration ---
# MUST match the configuration in indexing.py
DB_PATH = "data/"
COLLECTION_NAME = "screenshots"
MODEL_NAME = 'clip-ViT-B-32'

class Searcher:
    """
    A class to handle searching the screenshot database.
    It loads the model once and manages the database connection.
    """
    def __init__(self, model_name: str, db_path: str, collection_name: str):
        print("Initializing Searcher...")
        self.db_path = db_path
        self.collection_name = collection_name
        
        # 1. Load the embedding model once
        self.model = self._load_embedding_model(model_name)
        
        # 2. Connect to the existing ChromaDB collection
        self.client = chromadb.PersistentClient(path=self.db_path)
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            print(f"✅ Connected to collection '{self.collection_name}' with {self.collection.count()} items.")
        except Exception as e:
            # Catch a more general exception to handle different chromadb errors
            print(f"❌ Error connecting to collection: {e}")
            print(f"❌ It seems the collection '{self.collection_name}' does not exist.")
            print("   Please run the 'indexing.py' script first to create and populate the database.")
            self.collection = None
        
        print("Searcher initialized successfully. 🚀")

    def _load_embedding_model(self, model_name: str):
        """Loads the SentenceTransformer model."""
        print(f"Loading embedding model: {model_name}")
        start_time = time.time()
        model = SentenceTransformer(model_name)
        end_time = time.time()
        print(f"✅ Model loaded in {end_time - start_time:.2f} seconds.")
        return model

    def search(self, query_text: str, top_n: int = 5):
        """
        Performs a search on the collection.
        Returns a list of results.
        """
        if not self.collection:
            print("Cannot perform search, collection not available.")
            return []

        print(f"\n🔎 Searching for: '{query_text}'")
        # 3. Create an embedding for the user's search query
        query_embedding = self.model.encode(query_text).tolist()

        # 4. Query the collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_n
        )
        
        return self._format_results(results)

    def _format_results(self, results: dict):
        """Formats the raw results from ChromaDB into a readable list."""
        formatted = []
        if not results['ids'][0]:
            return formatted

        ids = results['ids'][0]
        distances = results['distances'][0]
        metadatas = results['metadatas'][0]

        for id, distance, metadata in zip(ids, distances, metadatas):
            # Convert distance to a more intuitive confidence score (0-1)
            # This works well for cosine similarity where distance is 0 for identical, 2 for opposite.
            confidence = 1 - (distance / 2)
            
            formatted.append({
                "filepath": metadata.get('filepath', 'N/A'),
                "confidence": confidence,
                "id": id
            })
        return formatted

# 5. Main execution block to make the script a runnable CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for screenshots using natural language.")
    parser.add_argument("query", type=str, help="The natural language search query.")
    parser.add_argument(
        "--top_n", 
        type=int, 
        default=5, 
        help="The number of top results to return."
    )
    args = parser.parse_args()

    # Create an instance of our Searcher
    searcher = Searcher(model_name=MODEL_NAME, db_path=DB_PATH, collection_name=COLLECTION_NAME)

    # Perform the search if the searcher was initialized correctly
    if searcher.collection:
        search_results = searcher.search(args.query, top_n=args.top_n)

        print("\n--- Search Results ---")
        if not search_results:
            print("No matching screenshots found.")
        else:
            for result in search_results:
                print(f"📄 File:       {result['filepath']}")
                print(f"📈 Confidence: {result['confidence']:.2%}") # Formats as a percentage
                print("-" * 20)

