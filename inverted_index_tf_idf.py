import json
import os
import statistics
from copy import deepcopy
from typing import Dict

from nltk.stem import PorterStemmer


def create_inverted_index(input_path: str, output_path: str) -> None:
    """
    create_inverted_index Creates an inverted index given input_path and output_path.
    Args:
        input_path (str): path to find the scraped files from.
        output_path (str): path to write the inverted index, max_freq_wc, tf_idf, and list_of_words to.
    """
    # contains inverted index, max frequencies & word count, and term frequencies & inverted document frequency
    data = {"inverted_index": dict(), "max_freq_wc": dict(),
            "tf_idf": dict(), "list_of_words": dict(), "urls": dict(), "idf": dict(), "title": dict()}
    data_stopwords = deepcopy(data)
    data_stemming = deepcopy(data)
    data_stopwords_stemming = deepcopy(data)
    STEMMING = PorterStemmer()
    STOPWORDS: set
    # gets stopwords
    with open(os.path.join(os.path.abspath(__file__), "..", "stopwords.txt"), 'r') as f:
        STOPWORDS = set([line.replace("\n", "") for line in f])
    # make output directory if doesn't exist
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    # change to output directory
    os.chdir(input_path)
    # for each page...
    for filename in os.listdir(input_path):
        # if a directory, do not open it
        if os.path.isdir(filename):
            continue
        # gets document number from filename
        document_number = filename[filename.find("_")+1:filename.find(".")]
        current_words: str
        print(f"Processing document #{document_number}")
        # reads words from file
        with open(filename, 'r') as f:
            lines = f.readlines()
        # if no text in file, skip.
        if len(lines) < 3:
            continue
        # gets urls
        data["urls"][document_number] = [
            line.replace("\n", "") for line in lines[0]]
        data_stopwords['urls'][document_number] = [
            line.replace("\n", "") for line in lines[0]]
        data_stemming['urls'][document_number] = [
            line.replace("\n", "") for line in lines[0]]
        data_stopwords_stemming['urls'][document_number] = [
            line.replace("\n", "") for line in lines[0]]

        # gets titles
        data["title"][document_number] = lines[2].replace("\n", "")
        data_stopwords['title'][document_number] = lines[2].replace("\n", "")
        data_stemming['title'][document_number] = lines[2].replace("\n", "")
        data_stopwords_stemming['title'][document_number] = lines[2].replace(
            "\n", "")

        # gets words
        current_words = [current_word.lower()
                         for current_word in lines[1].split(" ")]
        # puts word into dictionary
        for word in current_words:
            if word == "":
                continue
            stemmed_word = STEMMING.stem(word)

            '''Inverted Indexes'''
            # regular words
            if word in data["inverted_index"]:
                data["inverted_index"][word][document_number] = current_words.count(
                    word)
            else:
                data["inverted_index"][word] = {document_number: current_words.count(
                    word)}

            # stopwords
            if word in data_stopwords['inverted_index'] and word not in STOPWORDS:
                data_stopwords['inverted_index'][word][document_number] = current_words.count(
                    word)
            else:
                data_stopwords['inverted_index'][word] = {document_number: current_words.count(
                    word)}

            # stopwords stemming
            if stemmed_word in data_stopwords_stemming['inverted_index'] and stemmed_word not in STOPWORDS:
                data_stopwords_stemming['inverted_index'][stemmed_word][document_number] = current_words.count(
                    word)
            else:
                data_stopwords_stemming['inverted_index'][stemmed_word] = {document_number: current_words.count(
                    word)}

            # stemming
            if stemmed_word in data_stemming['inverted_index']:
                data_stemming['inverted_index'][stemmed_word][document_number] = current_words.count(
                    word)
            else:
                data_stemming['inverted_index'][stemmed_word] = {document_number: current_words.count(
                    word)}

        # puts each document into a set of words
        data["list_of_words"][document_number] = list(set(current_words))
        data_stopwords['list_of_words'][document_number] = [
            stop_word for stop_word in set(current_words) if stop_word not in STOPWORDS]
        data_stemming['list_of_words'][document_number] = [
            STEMMING.stem(stem_word) for stem_word in set(current_words)]
        data_stopwords_stemming['list_of_words'][document_number] = [
            stem_word for stem_word in set(data_stemming['list_of_words'][document_number]) if stem_word not in STOPWORDS]

        # gets mode to get the maximum frequency of the most common word.
        data["max_freq_wc"][document_number] = current_words.count(
            statistics.mode(current_words))
        data_stopwords['max_freq_wc'][document_number] = data_stopwords['list_of_words'][document_number].count(
            statistics.mode(data_stopwords['list_of_words'][document_number]))
        data_stopwords_stemming['max_freq_wc'][document_number] = data_stopwords_stemming['list_of_words'][document_number].count(
            statistics.mode(data_stopwords_stemming['list_of_words'][document_number]))
        data_stemming['max_freq_wc'][document_number] = data_stemming['list_of_words'][document_number].count(
            statistics.mode(data_stemming['list_of_words'][document_number]))

    # all datasets.
    all_data = {'': data, '_stopwords': data_stopwords,
                '_stemming': data_stemming, '_stopwords_stemming': data_stopwords_stemming}
    # for each dataset, get tf_idf.
    for file_extension, dataset in all_data.items():
        all_data[file_extension] = get_tf_idf(dataset)

    # dumps json.
    os.chdir(output_path)
    for file_extension, dataset in all_data.items():
        for keys, values in dataset.items():
            with open(f'{keys}{file_extension}.json', 'w') as f:
                json.dump(values, f, sort_keys=True, indent=4)


def get_tf_idf(data: Dict) -> Dict:
    """
    get_tf_idf Gets the TF idf data and returns the dictionary.
    Args:
        data (Dict): Dictionary containing inverted_index, max_freq_wc, and list_of_word keys.
    Returns:
        Dict: Dictionary containing given data, and tf_idf values.
    """
    NUMBER_OF_DOCUMENTS = len(data["max_freq_wc"])
    # for each document in the data.
    for document_number, freq_wc in data["max_freq_wc"].items():
        print(f'Document #{document_number}')
        # creates tf_idf dictionary at document_number
        data["tf_idf"][document_number] = dict()
        # for each word in the document.
        for word in data["list_of_words"][document_number]:
            if word == "":
                continue
            # if word's idf not generated, generate it.
            if word not in data["idf"].keys():
                data["idf"][word] = NUMBER_OF_DOCUMENTS / \
                    len(data["inverted_index"][word])
            # set tf_idf value.
            data["tf_idf"][document_number][word] = (
                data["inverted_index"][word][document_number]/freq_wc*data["idf"][word])
    return data
