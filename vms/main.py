import argparse
import os
import yaml
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# If main.py is in the 'vms' folder with the other files, this will work.
from indexing import Indexer
from search import Searcher

# --- Watcher Logic (Integrated from watcher.py) ---

class ScreenshotHandler(FileSystemEventHandler):
    """A handler for newly created screenshot files."""
    def __init__(self, indexer_instance):
        self.indexer = indexer_instance
        self.allowed_extensions = {".png", ".jpg", ".jpeg", ".bmp"}

    def on_deleted(self, event):
        if event.is_directory:
            return
        self.indexer.delete_by_path(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        
        _, ext = os.path.splitext(event.src_path)
        if ext.lower() in self.allowed_extensions:
            print(f"\nNew image detected: {os.path.basename(event.src_path)}")
            time.sleep(1) 
            self.indexer.index_single_file(event.src_path)

# --- CLI Handler Functions ---

def handle_index(args, config):
    """Handler function for the 'index' command."""
    print("--- Running Indexer ---")
    path = args.path
    if not os.path.isdir(path):
        print(f"❌ Error: Provided path '{path}' is not a valid directory.")
        return
        
    indexer = Indexer(
        model_name=config['embedding_model'], 
        db_path=config['database']['path'], 
        collection_name=config['database']['collection_name']
    )
    indexer.run(path)

def handle_search(args, config):
    """Handler function for the 'search' command."""
    print("--- Running Searcher ---")
    searcher = Searcher(
        model_name=config['embedding_model'], 
        db_path=config['database']['path'], 
        collection_name=config['database']['collection_name']
    )

    if searcher.collection:
        search_results = searcher.search(args.query, top_n=args.top_n)

        print("\n--- Search Results ---")
        if not search_results:
            print("No matching screenshots found.")
        else:
            for result in search_results:
                print(f"📄 File:       {result['filepath']}")
                print(f"📈 Confidence: {result['confidence']:.2%}")
                print("-" * 20)

def handle_watch(args, config):
    """Handler function for the 'watch' command."""
    print("--- Starting Automated Indexer Watcher ---")
    indexer = Indexer(
        model_name=config['embedding_model'], 
        db_path=config['database']['path'], 
        collection_name=config['database']['collection_name']
    )
    
    path = args.path
    event_handler = ScreenshotHandler(indexer)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    
    print(f"👀 Watching folder: '{path}' for new screenshots...")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nWatcher stopped.")
    observer.join()

# --- Main Application Logic ---

def main():
    config = load_config()

    parser = argparse.ArgumentParser(
        description="Visual Memory Search: Index, search, and watch your screenshot history.",
        epilog="Example: python vms/main.py search 'error message about auth'"
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # --- Index Command ---
    parser_index = subparsers.add_parser("index", help="Perform a one-time indexing of a folder.")
    parser_index.add_argument(
        "--path",
        type=str,
        default=config['default_screenshots_folder'],
        help=f"Path to the folder of screenshots. Defaults to '{config['default_screenshots_folder']}'."
    )
    parser_index.set_defaults(func=handle_index)

    # --- Search Command ---
    parser_search = subparsers.add_parser("search", help="Search the indexed screenshots.")
    parser_search.add_argument("query", type=str, help="The natural language search query.")
    parser_search.add_argument("--top_n", type=int, default=5, help="Number of results to return.")
    parser_search.set_defaults(func=handle_search)
    
    # --- Watch Command ---
    parser_watch = subparsers.add_parser("watch", help="Watch a folder for new screenshots and index them automatically.")
    parser_watch.add_argument(
        "--path",
        type=str,
        default=config['default_screenshots_folder'],
        help=f"Path to the folder to watch. Defaults to '{config['default_screenshots_folder']}'."
    )
    parser_watch.set_defaults(func=handle_watch)
    
    args = parser.parse_args()
    args.func(args, config)

def load_config(config_path="config.yaml"):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    main()

