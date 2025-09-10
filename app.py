import streamlit as st
from PIL import Image
import os

# Import your existing search logic
from vms.search import Searcher

# --- IMPORTANT: Load configuration dynamically ---
# In a real app, you would load this from your config.yaml
DB_PATH = "data/"
COLLECTION_NAME = "screenshots"
MODEL_NAME = 'clip-ViT-B-32'


# --- Page Configuration ---
# This should be the first Streamlit command in your script
st.set_page_config(
    page_title="Visual Memory Search",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Caching the Searcher ---
# This is a critical performance optimization. It ensures the heavy AI model
# is loaded only ONCE when the app starts, not on every user interaction.
@st.cache_resource
def get_searcher():
    """Loads the Searcher model and caches it."""
    try:
        # Note: Ensure the DB_PATH and other configs are correct.
        return Searcher(model_name=MODEL_NAME, db_path=DB_PATH, collection_name=COLLECTION_NAME)
    except Exception as e:
        st.error(f"Failed to initialize the search model: {e}", icon="🚨")
        st.error("Please make sure you have run the indexing script at least once to create the database.", icon="ℹ️")
        return None

# --- Main Application UI ---
st.title("🧠 Visual Memory Search")
st.markdown("Search your screenshot history using natural language. The system understands both the text within the images and their visual content.")

# Load the searcher using the cached function
searcher = get_searcher()

# Only proceed if the searcher was loaded successfully
if searcher:
    # --- Search Bar ---
    query = st.text_input(
        "Search your screenshots...",
        placeholder="e.g., a python function with an error, or a UI with a blue button",
        # label_visibility="collapsed"
    )

    if query:
        st.markdown("---")
        # Perform search and display results
        with st.spinner("Searching for the most relevant screenshots..."):
            results = searcher.search(query, top_n=5)

        if not results:
            st.warning("No results found. Try a different query or add more screenshots!", icon="⚠️")
        else:
            st.success(f"Found {len(results)} matching screenshots:")
            
            # Display results in a responsive grid
            cols = st.columns(5) 
            for i, result in enumerate(results):
                col = cols[i % 3]
                try:
                    image_path = result['filepath']
                    if os.path.exists(image_path):
                        image = Image.open(image_path)
                        col.image(image, width="stretch", caption=f"Confidence: {result['confidence']:.1%}")
                        # with col.expander("Details"):
                        #     st.text(f"File: {os.path.basename(image_path)}")
                    else:
                         col.error(f"File not found:\n{os.path.basename(image_path)}", icon="❌")

                except Exception as e:
                    col.error(f"Error loading image:\n{os.path.basename(image_path)}", icon="🖼️")

# # --- Sidebar Information ---
# with st.sidebar:
#     st.header("How It Works")
#     st.markdown(
#         """
#         1.  **Automated Indexing:** The `watcher.py` script runs in the background, automatically processing any new screenshot you save.
#         2.  **AI Analysis:** An AI model (CLIP) analyzes each screenshot, understanding both its visual content and any text it contains.
#         3.  **Semantic Search:** When you type a query, the system finds the screenshots that are most semantically similar to your description.
#         """
#     )
#     st.info("To add more images, simply save them to the `screenshots` folder. The `watcher.py` script will index them automatically if it's running.", icon="ℹ️")
#     st.markdown("---")
#     st.write("@Arsalaan Ahmed 2025")