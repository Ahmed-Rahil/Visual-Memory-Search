from indexing import *
from database_handler import setup_database
from vectorizer import load_model, embed_image


def main():
  image_folder = "screenshots"
  collection_name = "visual_memory"

  model = load_model()
  collection = setup_database(collection_name)
  image_paths = get_image_paths(image_folder)

  for path in image_paths:


    print(f"\n--- Processing: {path} ---")

    existing_entry = collection.get(ids=[path])
    if existing_entry['ids']:
      print(f"✅ Skipping '{path}', already in database.")
      continue

    image_obj = load_image(path)
    if not image_obj:
      continue
    text = extract_text_from_image(path)
    print(f"🔍 Extracted Text: {text[:100]}...")

    embedding = embed_image(model, image_obj)

    collection.add(
      embeddings=[embedding.tolist()],
      metadatas=[{"path" : path, "text" : text}],
      ids=[path]
    )

    print(f"✅ Stored embedding for {path} in ChromaDB.")
  print(f"\n🎉 Process complete! Added {collection.count()} items to the '{collection_name}' collection.")

if __name__ == "__main__":
  main()


