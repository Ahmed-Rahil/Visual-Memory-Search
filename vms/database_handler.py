import chromadb

def setup_database(collection_name: str = "visual_memory"):
  client = chromadb.PersistentClient(path='.')
  collection = client.get_or_create_collection(name=collection_name)
  print(f"✅ ChromaDB collection '{collection_name}' is ready.")
  return collection

