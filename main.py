import gc
import os

from inverted_index_tf_idf import create_inverted_index
from scrape import scrape_data

WEB_SCRAPE_OUTPUT = os.path.join(os.path.abspath(__file__), "..", "output")
JSON_OUTPUT = os.path.join(os.path.abspath(__file__), "..", "data")


def main() -> None:
    """
    main Main function for Final Project. Gets urls and creates tf_idf, inverted_index, and etc.
    """
    # enables garbage collection.
    gc.enable()
    # scrapes data.
    scrape_data("https://muhlenberg.edu/", 10_000, WEB_SCRAPE_OUTPUT)
    # creates tf_idf, inverted_index, and etc.
    create_inverted_index(WEB_SCRAPE_OUTPUT, JSON_OUTPUT)


if __name__ == "__main__":
    # cProfile.run("main()")
    main()
