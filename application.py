from tkinter import * #tkinter package
import sqlite3 #sql database package

"""---------------------------------- Tkinter ----------------------------------"""
root = Tk()

"""____Make Widgets____"""


"""____Grid Widgets____"""


"""---------------------------------- App Functionality ----------------------------------"""
"""____Commands + Tkinter Functions____"""


"""____Database____"""
#create connection to database server (to CRUD the database)
def connect_to_server():
    return sqlite3.connect('/user.db')



"""---------------------------------- Run ----------------------------------"""
if __name__ == "__main__":
    root.mainloop()