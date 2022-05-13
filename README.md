# Muhlenberg Search Engine

## Requirements

- Python must be installed on your machine
- In a terminal navigate the current directory run <code>pip install -r requirements.txt</code> or <code>pip install nltk</code>.

## Run Instructions
- Run executable from releases (**zip highly recommended**)
- Run in Python
  - Run 'main.py' to generate the data from muhlenberg.edu.
  - Run 'cli.py' for a CLI search.
  - Run 'gui.py' for a GUI search.

## Backend
- Uses nltk for Porter Stemming.
- Uses cosine similarity ranking for results.
  - Uses **Term Frequency** and **Inverted Document Frequency** as weights.
