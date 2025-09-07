import os
import chromadb
import uuid
from PIL import Image
from sentence_transformers import SentenceTransformer
import easyocr
import time

# --- Configuration ---
# In a real app, this would come from a config.yaml file
SCREENSHOTS_FOLDER = "screenshots"
DB_PATH = "data/"
COLLECTION_NAME = "screenshots"
MODEL_NAME = 'clip-ViT-B-32'

class Indexer:
    """
    A class to handle the indexing of screenshots.
    It loads models once and manages the database connection.
    """
    def __init__(self, model_name: str, db_path: str, collection_name: str):
        print("Initializing Indexer...")
        self.db_path = db_path
        self.collection_name = collection_name
        
        # 1. Load models once during initialization
        self.model = self._load_embedding_model(model_name)
        self.reader = self._load_ocr_reader()
        
        # 2. Initialize ChromaDB client and collection
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
        print("Indexer initialized successfully. 🧠")

    def _load_embedding_model(self, model_name: str):
        print(f"Loading embedding model: {model_name}")
        start_time = time.time()
        model = SentenceTransformer(model_name)
        end_time = time.time()
        print(f"✅ Model loaded in {end_time - start_time:.2f} seconds.")
        return model

    def _load_ocr_reader(self):
        print("Loading OCR reader...")
        start_time = time.time()
        reader = easyocr.Reader(['en'])
        end_time = time.time()
        print(f"✅ OCR reader loaded in {end_time - start_time:.2f} seconds.")
        return reader

    def get_image_paths(self, folder_path: str):
        """Yields paths for all supported image files in a folder."""
        allowed_extensions = {".png", ".jpg", ".jpeg", ".bmp"}
        print(f"Scanning for images in '{folder_path}'...")
        for root, _, files in os.walk(folder_path):
            for file in files:
                if os.path.splitext(file)[1].lower() in allowed_extensions:
                    yield os.path.join(root, file)

    def process_and_embed(self, image_path: str):
        """Processes a single image to extract text and generate a combined embedding."""
        try:
            # 3. Graceful error handling for OCR
            ocr_results = self.reader.readtext(image_path, detail=0, paragraph=True)
            ocr_text = " ".join(ocr_results)
        except Exception:
            ocr_text = "" # If OCR fails, proceed without text

        # 4. The key step: creating the combined text for embedding
        combined_text = f"A screenshot showing text: {ocr_text}"

        # Generate embedding from the combined text
        embedding = self.model.encode(combined_text).tolist()
        
        return embedding, combined_text

    def run(self, folder_path: str):
        """Finds all images, processes them, and adds them to the database."""
        print("\n--- Starting Indexing Process ---")
        image_paths = list(self.get_image_paths(folder_path))
        total_images = len(image_paths)
        print(f"Found {total_images} images to process.")

        for i, path in enumerate(image_paths):
            print(f"\nProcessing [{i+1}/{total_images}]: {os.path.basename(path)}")
            
            # Check if this image has already been indexed
            if self.collection.get(where={"filepath": path})['ids']:
                print("   -> Already indexed. Skipping.")
                continue

            embedding, indexed_text = self.process_and_embed(path)
            
            self.collection.add(
                ids=[str(uuid.uuid4())], # Unique ID for each entry
                embeddings=[embedding],
                metadatas=[{"filepath": path, "indexed_text": indexed_text}]
            )
            print(f"   -> Successfully indexed and added to database. ✅")
        
        print(f"\n--- Indexing Complete. Total items in database: {self.collection.count()} ---")

# 5. Main execution block
if __name__ == "__main__":
    # This makes the script runnable from the command line
    if not os.path.exists(SCREENSHOTS_FOLDER):
        os.makedirs(SCREENSHOTS_FOLDER)
        print(f"Created '{SCREENSHOTS_FOLDER}' directory. Please add your screenshots there and run again.")
    else:
        # Create an instance of our Indexer
        indexer = Indexer(model_name=MODEL_NAME, db_path=DB_PATH, collection_name=COLLECTION_NAME)
        # Run the indexing process
        indexer.run(SCREENSHOTS_FOLDER)