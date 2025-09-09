import argparse
import os
import yaml

# Function to load config
def load_config(config_path = "config.yaml"):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)
    
    

# If main.py is in the 'vms' folder with the other files, this will work.
from indexing import Indexer
from search import Searcher


def handle_index(args):
    """Handler function for the 'index' command."""
    print("--- Running Indexer ---")
    path = args.path
    if not os.path.isdir(path):
        print(f"❌ Error: Provided path '{path}' is not a valid directory.")
        return
        
    indexer = Indexer(model_name=config['embedding_model'], db_path=config['database']['path'], collection_name=config['database']['collection_name'])
    indexer.run(path)

def handle_search(args):
    """Handler function for the 'search' command."""
    print("--- Running Searcher ---")
    searcher = Searcher(model_name=config['embedding_model'], db_path=config['database']['path'], collection_name=config['database']['collection_name'])

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

def main():
    #config = load_config()

    """Main function to set up and parse arguments."""
    parser = argparse.ArgumentParser(
        description="Visual Memory Search: Index and search your screenshot history.",
        epilog="Example: python vms/main.py search 'error message about auth'"
    )
    
    # Using subparsers to handle different commands (index, search)
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # --- Index Command ---
    parser_index = subparsers.add_parser("index", help="Index a folder of screenshots.")
    parser_index.add_argument(
        "--path",
        type=str,
        default=config['default_screenshots_folder'],
        help=f"Path to the folder of screenshots to index. Defaults to '{config['default_screenshots_folder']}'."
    )
    parser_index.set_defaults(func=handle_index)

    # --- Search Command ---
    parser_search = subparsers.add_parser("search", help="Search the indexed screenshots.")
    parser_search.add_argument("query", type=str, help="The natural language search query.")
    parser_search.add_argument(
        "--top_n",
        type=int,
        default=5,
        help="The number of top results to return."
    )
    parser_search.set_defaults(func=handle_search)
    
    args = parser.parse_args()
    args.func(args) # Call the appropriate handler function (handle_index or handle_search)

if __name__ == "__main__":
    config = load_config()
    main()