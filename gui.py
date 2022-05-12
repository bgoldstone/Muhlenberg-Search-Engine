import os
import webbrowser
from tkinter import (LEFT, RIGHT, Button, Checkbutton, E, Entry, Frame, IntVar,
                     Label, Tk, W)

from query import query_website

# Global Variables
DATA = os.path.join(os.path.abspath(__file__), "..", "data")
VIEW = 0
URLS = {}
CURRENT_SEARCH = ''
INDEX = ''
BTN = []
LABEL = []
SPACES = ' ' * 200


def search():
    """
    search Searches website for given term.
    """
    global CURRENT_SEARCH, VIEW, BTN, LABEL, URLS
    postfix = ''
    # gets stopwords and/or stemming if required by user.
    if STEMMED.get() == 1 and STOPWORDS.get() == 1:
        postfix = '_stopwords_stemming'
    elif STEMMED.get() == 1:
        postfix = '_stemming'
    elif STOPWORDS.get() == 1:
        postfix = '_stopwords'
    # get search term
    search_term = field.get()
    # if search term is different, reset VIEW to 0.
    if search_term != CURRENT_SEARCH:
        VIEW = 0
    # query data
    URLS = query_website(DATA, postfix, search_term)
    CURRENT_SEARCH = search_term
    start_row = 4
    # if current Buttons, delete them.
    if len(BTN) > 0:
        for i in range(10):
            try:
                BTN[i].grid_forget()
                LABEL[i].grid_forget()
            except AttributeError:
                break
    # new empty BTN/LABEL,current_urls list.
    BTN = [i for i in range(10)]
    LABEL = [i for i in range(10)]
    current_urls = [i for i in range(10)]
    # for the first 10 links based on view number, load them in.
    for i in range(10):
        try:
            current_urls[i] = URLS[VIEW+i][1]
        # if less than 10 links appear on page, render empty Labels.
        except IndexError:
            LABEL[i] = Label(app, text=SPACES)
            LABEL[i].grid(row=start_row, column=0, columnspan=2)
            Label(app, text=SPACES).grid(row=start_row+1, columnspan=2)
            start_row += 2
            continue
        # render Title
        Label(app, text=URLS[VIEW+i][0],
              width=90).grid(row=start_row, column=0)
        # Render button to goto page.
        BTN[i] = Button(app, text="Visit Page", width=5, padx=10,
                        borderwidth=1, bg='green', fg='white')
        BTN[i].grid(row=start_row, column=1)
        # render empty label for spacing.
        LABEL[i] = Label(app, text="")
        LABEL[i].grid(row=start_row+1, column=0)
        start_row += 2
    # put previous button and next button in place.
    prev_btn = Button(app, text="Previous", width=5, padx=10, borderwidth=1,
                      command=decrease_results, bg='blue', fg='white')

    next_btn = Button(app, text="Next", width=5, padx=10, borderwidth=1,
                      command=increase_results, bg='blue', fg='white')
    prev_btn.grid(row=start_row, padx=15, sticky=E)
    next_btn.grid(row=start_row, column=1, sticky=W)
    try:
        BTN[0].configure(command=lambda: webbrowser.open(current_urls[0]))
        BTN[1].configure(command=lambda: webbrowser.open(current_urls[1]))
        BTN[2].configure(command=lambda: webbrowser.open(current_urls[2]))
        BTN[3].configure(command=lambda: webbrowser.open(current_urls[3]))
        BTN[4].configure(command=lambda: webbrowser.open(current_urls[4]))
        BTN[5].configure(command=lambda: webbrowser.open(current_urls[5]))
        BTN[6].configure(command=lambda: webbrowser.open(current_urls[6]))
        BTN[7].configure(command=lambda: webbrowser.open(current_urls[7]))
        BTN[8].configure(command=lambda: webbrowser.open(current_urls[8]))
        BTN[9].configure(command=lambda: webbrowser.open(current_urls[9]))
    # if button invalid, end function call.
    except AttributeError:
        return


def increase_results():
    """
    increase_results Increases VIEW variable to allow for different results.
    """
    global VIEW
    # If VIEW + 10 is not longer than length of URLS, increment VIEW.
    if len(URLS) >= VIEW + 10:
        VIEW += 10
    search()


def decrease_results():
    """
    decrease_results Decreases VIEW variable to allow for different results.
    """
    global VIEW
    # if VIEW is not below 0, decrement VIEW.
    if 0 <= VIEW - 10:
        VIEW -= 10
    search()


app = Tk()
# set empty variables for boolean
# set app title.
app.title('Muhlenberg Search')
# set window size.
app.geometry('800x700+10+40')
# set Icon in top left corner.
app.iconbitmap(os.path.join(os.path.dirname(__file__), 'muhlenberg.ico'))
# set heading label
heading = Label(
    app, text='Welcome to Muhlenberg search!  Please enter a query to begin.', justify='center', font=('Comic Sans MS', 12), highlightthickness=2, padx=10, pady=10)
heading.config(highlightbackground='#a41e34', highlightcolor='#a41e34')
heading.grid(row=0, column=0, columnspan=3, pady=10)
# stem and stopwords checkbox.
STEMMED = IntVar()
STOPWORDS = IntVar()
checkbox_frame = Frame(app, highlightthickness=2)
stem_checkbox = Checkbutton(
    checkbox_frame, text="Stemmed", variable=STEMMED, onvalue=1, offvalue=0)
stopwords_checkbox = Checkbutton(
    checkbox_frame, text="Stopwords", variable=STOPWORDS, onvalue=1, offvalue=0)
stem_checkbox.pack(side=LEFT)
stopwords_checkbox.pack(side=RIGHT)
checkbox_frame.config(highlightbackground='orange',
                      highlightcolor='orange')
checkbox_frame.grid(row=1, columnspan=2, padx=15, pady=10)
# entry field.
field = Entry(app, textvariable="Search Muhlenberg.edu",
              justify='center', width=100)
field.grid(row=2, column=0, columnspan=1, padx=10)
# search button with muhlenberg red background.
search_btn = Button(app, text="Search", command=search,
                    fg='white', bg='#a41e34')
search_btn.grid(row=2, column=1, columnspan=2, sticky=E, padx=5)
app.bind('<Return>', lambda event: search_btn.invoke())
empty_label = Label(app, text='')
empty_label.grid(row=3)
# run app
if __name__ == '__main__':
    app.mainloop()
