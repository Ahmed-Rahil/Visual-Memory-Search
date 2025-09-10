# 🧠 Visual Memory Search

A powerful tool to search your screenshot history using natural language, understanding both text and visual content.

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Status](https://img.shields.io/badge/status-stable-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

<p align="center">
  <img src="file\image.png" alt="Visual Memory Search GUI" width="800"/>
</p>

## ✨ Features

- **🧠 Hybrid Search:** Combines AI analysis of image pixels and OCR text for highly accurate results.
- **🖥️ Intuitive GUI:** A simple and clean web interface built with Streamlit for easy searching.
- **⌨️ Powerful CLI:** A full-featured command-line interface for scripting and power users.
- **🤖 Automated Indexing:** A background "watcher" automatically detects and indexes new screenshots.
- **🔒 Local First:** All models and data are processed locally on your machine. Nothing is sent to the cloud.

---

## 🚀 Getting Started

Follow these steps to get the project running on your local machine.

### Prerequisites

- Python 3.9 or higher
- Git

### Installation

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/Ahmed-Rahil/Visual-Memory-Search.git

    cd visual-memory-search
    ```

2.  **Create and Activate a Virtual Environment:**

    ```bash
    # macOS / Linux
    python3 -m venv .venv
    source .venv/bin/activate

    # Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Add Your Screenshots:**
    Place any images you want to index into the `screenshots/` folder.

---

## 🖥️ How to Use

You can run this project in two ways. The GUI is recommended for the best experience.

### GUI Application (Recommended)

This method requires two separate terminals running simultaneously.

1.  **Start the Automated Watcher (Terminal 1):**
    This script monitors your `screenshots` folder and automatically indexes new images. Keep it running in the background.

    ```bash
    python watcher.py
    ```

2.  **Launch the GUI (Terminal 2):**
    This will start the Streamlit web server and open the application in your browser.
    ```bash
    streamlit run app.py
    ```

### Command-Line Interface (CLI)

For scripting or terminal-based workflows, use the unified CLI.

- **Index a Folder (One-Time Scan):**

  ```bash
  python vms/main.py index --path /path/to/screenshots
  ```

- **Search from the Terminal:**

  ```bash
  python vms/main.py search "a python function with a for loop"
  ```

- **Watch a Folder (CLI version):**
  ```bash
  python vms/main.py watch
  ```

---

## 🛠️ Configuration

Project settings can be modified in the `config.yaml` file:

- `embedding_model`: The AI model to use.
- `database`: The path for the vector database.
- `default_screenshots_folder`: The default folder to index and watch.

## Contibution

Contribution is most welcome. Create an Issue if you have suggestion and create a pull request if you have some contibution.
