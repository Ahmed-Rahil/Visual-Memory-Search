import os
from PIL import Image
import easyocr

def get_image_paths(folder_path: str):
  allowed_extensions = {".png", ".jpg", ".jpeg", ".bmp"}
  for root, _, files in os.walk(folder_path):
    for file in files:
      if os.path.splitext(file)[1].lower() in allowed_extensions:
        yield os.path.join(root, file)

def load_image(image_path: str):
  try:
    image = Image.open(image_path)
    print(f"✅ Successfully loaded image: {image_path}")
    return image
  except FileNotFoundError:
    print(f"❌ Error: The file at {image_path} was not found.")
    return None
  except Exception as e:
    print(f"❌ An unexpected error occurred while loading {image_path}: {e}")
    return None
  


reader = easyocr.Reader(['en'])

def extract_text_from_image(image_path: str):
  try:
    results = reader.readtext(image_path)
    extracted_text = " ".join([text for _, text, _ in results])
    return extracted_text
  except Exception as e:
    print(f"❌ Could not process image {image_path} with EasyOCR: {e}")
    return "error"
  



