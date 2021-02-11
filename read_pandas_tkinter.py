__author__ = "Lucas Blom"
__email__ = "lucas.blom@maine.edu"
__status__ = "beta"

'''
## UPDATE ME
This program gathers movie data from a csv file, creates a pandas data frame with it, and a tkinter application
to show all data or iterate through rows individually
'''

import tkinter as tk
import pandas as pd


# define variables and constants
frame_data = None
df2 = None
table = None
current_index = None

# used for data load into app
DATA_FILE = './data/IMDB-Movie-Data.csv'

# used in movie options menu UI/UX and on_select function
SELECT_ALL_TEXT = 'ALL THE MOVIES'
SELECTION_PARAMETER = 'Title'


# --- functions ---
def get_data(file_name):
    data = pd.read_csv(file_name, index_col=0)
    return data


# a function we call to display pandas data
def show_data():
    global table
    global df2

    # destroy old frame with table
    if table:
        table.destroy()

    # create new frame with table
    table = tk.Frame(frame_data)
    table.grid(row=1, column=1)

    # fill frame with table
    row, column = df2.shape
    for r in range(row):
        for c in range(column):
            e1 = tk.Entry(table)
            e1.insert(1, df2.iloc[r, c])
            e1.grid(row=r, column=c, padx=2, pady=2)
            e1.config(state='disabled')


# function executed when we click the dropdown menu
def on_select(val):
    global df2
    global current_index

    val = selected.get()
    if val == SELECT_ALL_TEXT:
        df2 = df
        next_button.grid_forget()
    else:
        df2 = df[df[SELECTION_PARAMETER] == val]
        # find index
        current_index = 0
        for ind in df.index:
            if df[SELECTION_PARAMETER][ind] == val:
                current_index = ind
                print('current_index', current_index)
        # put next button on the canvas
        next_button.grid(row=1, column=0)
    # DRY
    show_data()


def next_data():
    global current_index
    global df2

    if current_index < len(df)-1:
        current_index = current_index+1
    df2 = df.iloc[[current_index]]
    show_data()


# --- main ---
# here is the dataframe
df = get_data(DATA_FILE)

# here we start the GUI
root = tk.Tk()
root.title("Movie List")
root.geometry("1000x800")

# prepare list of values for drop down menu
# values is a list of unique movie titles and corresponding tuples from csv file
values = [SELECT_ALL_TEXT] + list(df[SELECTION_PARAMETER].unique())

# input variable has to be a StringVar, special var for Tkinter to grab user input
selected = tk.StringVar(value="Movie Choices")

# create drop down menu
# we have a function we execute on button click -- on_select from drop down menu
options = tk.OptionMenu(root, selected, *values, command=on_select)
options.grid(row=0, column=0, padx=15, pady=15)

# frame for table and button "Next Data"
frame_data = tk.Frame(root)
frame_data.grid(row=1, column=0, padx=15, pady=15)

# button "Next Data" - inside "frame_data" - without showing it
next_button = tk.Button(frame_data, text="Next Data", command=next_data)
# table with data - inside "frame_data" - without showing it
table = tk.Frame(frame_data)
table.grid(row=0, column=0)

exit_button = tk.Button(root, text="EXIT", command=root.destroy)
exit_button.grid(row=3, column=0, padx=15, pady=15)


root.mainloop()
