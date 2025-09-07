from sentence_transformers import SentenceTransformer
from PIL import Image
def load_model():
  model_name = 'clip-ViT-B-32'
  print(f"Loading sentence transformer model: {model_name}")
  model = SentenceTransformer(model_name, device='cpu', use_auth_token=None)
  print("Model loaded successfully.")
  return model

def embed_image(model: SentenceTransformer, image:Image.Image):
  embedding = model.encode(image)
  return embedding
