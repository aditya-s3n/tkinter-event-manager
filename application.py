from tkinter import * #tkinter package
import sqlite3

"""---------------------------------- App Functionality ----------------------------------"""
"""____Commands + Tkinter Functions____"""
def add_paricipant():
    pass

def change_price():
    pass 

def age_text_change():
    pass

"""____Database____"""
#create connection to database server (to CRUD the database)
def connect_to_server():
    return sqlite3.connect('/user.db')

#end the connection to the server when changes are made 
def end_connection_server(connection):
    connection.commit()
    connection.close()


#create the database if it doesn't exist already
def create_database_users():
    #create connection and editor
    connect = connect_to_server()
    cursor = connect.cursor()

    #Create the database with the fields the user can input
    command = """\
        CREATE TABLE IF NOT EXISTS users (
            id INT NOT NULL,
            first_name STRING,
            last_name STRING,
            meal_plan STRING,
            events INT,
            age INT,
            price MONEY,

            PRIMART KEY (id)
            )"""
    cursor.execute(command)

    #end the server connections
    end_connection_server(connect)

#insert a partipant into the SQL database
def enter_particpant(id: int, first_name: str, last_name: str, meal_plan: str, events: int, age: int, price: int):
    #create connection and editor
    connect = connect_to_server()
    cursor = connect.cursor()

    #insert values into SQL server of applicant
    command = """\
        INSERT INTO users
        VALUES (?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(command, (id, first_name, last_name, meal_plan, events, age, price)) #give values to the ? in the command

    #end connection to the server instance
    end_connection_server(connect)


#update a participants data in the SQL database
def update_particpant_data(id: int, first_name: str, last_name: str, meal_plan: str, events: int, age: int, price: int):
    #create connection and editor
    connect = connect_to_server()
    cursor = connect.cursor()

    #update the participants info
    command = """\
        UPDATE users
        SET first_name=?, last_name=?, meal_plan=?, events=?, age=?, price=?
        WHERE id=?"""
    cursor.execute(command, (first_name, last_name, meal_plan, events, age, price, id)) #give values to the ? in the command

    #end connection to database
    end_connection_server(connect)

#get values by id 
def get_participant_by_id(id: int):
    #create connection and editor
    connect = connect_to_server()
    cursor = connect.cursor()

    #Select Statement
    command = """\
        SELECT *
        FROM users
        WHERE id=?"""
    #get the parictipant with the ID
    participant = cursor.execute(command, (id)).fetchone() #give values to the ? in the command & fetch the one value / row

    #end connection to the server instance & return
    end_connection_server(connect)
    return participant

"""---------------------------------- Tkinter Front-End ----------------------------------"""
root = Tk()
place_names = ["Hawaii", ""]
events = ["Snorkling", "A", "B"]

font_title = ("Bauhaus 93", 30)
font_body = ("Arial Rounded MT Bold", 24)

"""____Make Widgets____"""
#First Name Text Entry
first_name = StringVar()
first_name_entry = Entry(root, textvariable=first_name)
#First Name Label
first_name_label = Label(root, font=font_body, text="First Name: ")

#Last Name Text Entry
last_name = StringVar()
last_name_entry = Entry(root, textvariable=last_name)
#First Name Label
last_name_label = Label(root, font=("Arial Rounded MT Bold", 24), text="Last Name: ")

#Meal Plan Radio Buttons
meal_plan = StringVar()
meal_plan.set("Deluxe") #set the default radio button selection to deluxe
#Meal Plan Label Frame
meal_plan_label = LabelFrame(root, text="Choose a Meal Plan")
#Radio Buttons
meal_plan_deluxe = Radiobutton(meal_plan_label, text="Deluxe", variable=meal_plan, value="Deluxe", command=change_price)
meal_plan_premium = Radiobutton(meal_plan_label, text="Premium", variable=meal_plan, value="Premium", command=change_price)
meal_plan_business = Radiobutton(meal_plan_label, text="Business", variable=meal_plan, value="Business", command=change_price)
meal_plan_economy = Radiobutton(meal_plan_label, text="Economy", variable=meal_plan, value="Economy", command=change_price)

#Events Check Buttons
event1 = IntVar()
event2 = IntVar()
event3 = IntVar()
#Event Label Frame
event_label = LabelFrame(root, text="Choose What Event's to Apply To")
#Check Buttons
event1_check_button = Checkbutton(event_label, variable=event1, text=events[0], onvalue=2, offvalue=0)
event2_check_button = Checkbutton(event_label, variable=event2, text=events[1], onvalue=2, offvalue=0)
event3_check_button = Checkbutton(event_label, variable=event3, text=events[2], onvalue=2, offvalue=0)

#Age Scale
age_value = IntVar()
age_scale = Scale(root, from_=0, to=150, variable=age_value, width=20, length=100, command=age_text_change, orient=HORIZONTAL)
#Age Label
age_label_variable = StringVar()
age_label = Label(root, font=("Arial Rounded MT Bold", 24), textvariable=age_label_variable)
age_text_change()

#Paricpants List Box

#Submit Button
sumbit_button = Button(root, text="Sumbit", command=add_paricipant)

#Event Name Option Menu

#Title

"""____Grid Widgets____"""
#First Name Text Entry
first_name_label.grid(column=0, row=3)
first_name_entry.grid(column=0, row=4)

#Last Name Text Entry
last_name_label.grid(column=0, row=5)
last_name_entry.grid(column=0, row=6)

#Meal Plan Radio Buttons
meal_plan_label.grid(column=0, row=7, ipadx = 10, ipady = 10) #label frame
meal_plan_deluxe.grid(sticky=W, padx=10)
meal_plan_premium.grid(sticky=W, padx=10)
meal_plan_business.grid(sticky=W, padx=10)
meal_plan_economy.grid(sticky=W, padx=10)

#Events Check Buttons
event_label.grid(column=0, row=8, ipadx = 10, ipady = 10)
event1_check_button.grid(sticky=W, padx=10)
event2_check_button.grid(sticky=W, padx=10)
event3_check_button.grid(sticky=W, padx=10)

#Age Scale
age_label.grid(column=0, row=9)
age_scale.grid(column=0, row=10)

#Paricpants List Box

#Submit Button

#Event Name Option Menu

#Title



"""---------------------------------- Run ----------------------------------"""
root.mainloop()