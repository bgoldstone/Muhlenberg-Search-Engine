from query import query_website
import os
DATA = os.path.join(os.path.abspath(__file__), "..", "data")
'''Main Runner for searching'''
if __name__ == '__main__':
    inp = ''
    print('Welcome to the Muhlenberg Search Engine!!\n\n')
    while inp.lower() != 'exit':
        postfix = ''

        inp = input(
            '\nWhat is your new search term? (type \'exit\' to exit program) ')
        if inp == 'exit':
            continue
        stopwords = input('\nWould you like stopwords? (y/n)')
        stemming = input('\nWould you like stemming? (y/n)')
        print()
        if stemming == 'y' and stopwords == 'y':
            postfix = '_stopwords_stemming'
        if stemming == 'y':
            postfix = '_stemming'
        if stopwords == 'y':
            postfix = '_stopwords'
        q = query_website(DATA, postfix, inp)
        quit_search = ''
        if len(q) == 0:
            print('\nNo results found, please try again.\n\n')
        for index, url in enumerate(q):
            if quit_search == 'n':
                break
            print(f'\nTitle: {url[0]}\nLink: {url[1]}\n\n')
            if index % 10 == 0 and index != 0:
                quit_search = input('\nDo you want to see more links? (y/n)')
            if index == len(q):
                print(
                    "\nNo more results! Please enter a new search term if you would like below.\n\n")
