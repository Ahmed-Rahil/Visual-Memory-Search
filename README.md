# Visual Memory Search 🧠

Search your screenshot history using natural language queries for both text content AND visual elements.

## What It Does

This tool indexes a folder of screenshots, extracting both the text content (via OCR) and the visual features of each image. It then allows you to perform powerful semantic searches like "a screenshot of an error message about authentication" or "a UI with a blue login button".

## Features

- **Hybrid Search:** Creates a combined vector from both image pixels and OCR text for highly accurate results.
- **Natural Language Queries:** Understands the intent behind your search, not just keywords.
- **Command-Line Interface:** Simple and scriptable interface for indexing and searching.
- **Local First:** All models and data are stored locally on your machine. No cloud required.

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Ahmed-Rahil/Visual-Memory-Search.git
    cd visual-memory-search
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

First, place any screenshots you want to index into the `screenshots/` folder.

1.  **Index Your Screenshots:**
    Run the index command. This only needs to be done once for new images.

    ```bash
    python vms/main.py index
    ```

2.  **Search Your History:**
    Use the search command with your query in quotes.
    ```bash
    python vms/main.py search "a python code snippet with a for loop"
    ```

## Configuration

You can modify the `config.yaml` file to change the model, database path, or default screenshot folder.
