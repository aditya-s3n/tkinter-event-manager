from tkinter import * #tkinter package
from tkinter.messagebox import * #warning & info message / pop-up
import sqlite3 #SQL database connection

"""---------------------------------- App Functionality ----------------------------------"""
"""____Commands + Tkinter Functions____"""
#function to save/submit the participant's information to the SQL database -- connection between Tkinter and SQL
def add_paricipant():
    #Check age & set it to variable
    age = age_value.get()
    #get and save first 
    fname = first_name.get()
    #get and save last name
    lname = last_name.get()
    #check the spots avaiable
    resort_selected = resort_selection.get()
    spots_total = get_spots_of_resort(resort_selected)
    participants = get_participant_by_resort(resort_selected)

    #Check if either last name, first name are empty, or age is 0
    if len(fname) == 0 or len(lname) == 0 or age <= 0 or spots_total[0] <= len(participants):
        #show warning to check for first name, last name, or age
        showwarning("Error: Insufficient Information OR No Available Space", """\
One (or more) of these is causing a problem submitting the client's information:
    1. First Name Entry is Empty
    2. Last Name Entry is Empty
    3. Age is set to 0
    4. All the spots are filled up
        """)
    
    #sumbit and save the participant's information
    else:
        #get all the values of the user
        #meal plan
        meal_plan_selected = meal_plan.get()
        #events
        events_selected = event1.get() + event2.get() + event3.get()
        #price
        total_price = price_text_change()
        total_price_formatted = "{:0,.2f}".format(total_price) #formatted text

        #show a message asking if you wanna save this information
        result = askquestion("Save Data?", f"""\
Do you wanna Save this Information at the {resort_selected} Resort:
    First Name: {fname}
    Last Name: {lname}
    Meal Plan: {meal_plan_selected}
    Number of Events Selected: {events_selected}

    Price: ${total_price_formatted}
            """)
        
        if result == "yes":
            #enter into SQL database
            enter_particpant(fname, lname, meal_plan_selected, events_selected, age, total_price, resort_selected)

#change age label
def age_text_change(value):
    age_label_variable.set(f"Age: {value}")
    price_text_change()

#change price label
def price_text_change():
    #get subtotal
    #get tax value by checking where the resort is & base price of resort
    resort = resort_selection.get()
    if resort == "Hawaii":
        tax_percentage = 0.1
        base_price = 2000
    elif resort == "Chile":
        tax_percentage = 0.02
        base_price = 1000
    elif resort == "Greece":
        tax_percentage = 0.05
        base_price = 1250
    else:
        tax_percentage = 0.08
        base_price = 1750

    #event price each event costs $100 (get the values of each event)
    event_price = (event1.get() + event2.get() + event3.get()) * 100
    #get the value of meal plan and set the meal plan price
    meal_plan_selection = meal_plan.get()
    if meal_plan_selection == "Economy":
        meal_plan_price = 100
    elif meal_plan_selection == "Business":
        meal_plan_price = 300
    elif meal_plan_selection == "Premium":
        meal_plan_price = 400
    else:
        meal_plan_price = 500
    #get the age and set the age price to 25 if they're older than 18
    age = age_value.get()
    if age >= 18:
        age_price = 25
    else:
        age_price = 0
    
    #calculate the subtotal price by adding all the variables up
    subtotal_price = event_price + meal_plan_price + age_price + base_price
    subtotal_price_formatted = "{:0,.2f}".format(subtotal_price)
    #set subtotal label
    subtotal_variable.set(f"Subtotal: ${subtotal_price_formatted}")
    #calculate the tax price by multiplying the tax percentage by the subtotal price
    tax_price = subtotal_price * tax_percentage
    tax_price_formatted = "{:0,.2f}".format(tax_price)
    #set tax label
    tax_variable.set(f"Tax: ${tax_price_formatted}")
    
    #get total price by adding the tax to the subtotal price
    total_price = tax_price + subtotal_price
    total_price_formatted = "{:0,.2f}".format(total_price) #format to money 
    #set tax price label
    total_price_variable.set(f"TOTAL: ${total_price_formatted}")

    return total_price

def open_participant(value):
    """____Info Page Widgets____"""
    #window for new page
    info_window = Toplevel(root)

    #title
    title_info = Label(info_window, text="Participant")

    #First Name Text Entry
    first_name_info = StringVar()
    first_name_entry_info = Entry(info_window, textvariable=first_name_info)
    #First Name Label
    first_name_label_info = Label(info_window, font=font_body, text="First Name: ")

    #Last Name Text Entry
    last_name_info = StringVar()
    last_name_entry_info = Entry(info_window, textvariable=last_name_info)
    #First Name Label
    last_name_label_info = Label(info_window, font=("Arial Rounded MT Bold", 24), text="Last Name: ")

    #Meal Plan Radio Buttons
    meal_plan_info = StringVar()
    meal_plan_info.set("Deluxe") #set the default radio button selection to deluxe
    #Meal Plan Label Frame
    meal_plan_label_info = LabelFrame(info_window, text="Choose a Meal Plan")
    #Radio Buttons
    meal_plan_deluxe_info = Radiobutton(meal_plan_label_info, text="Deluxe", variable=meal_plan_info, value="Deluxe", command=price_text_change)
    meal_plan_premium_info = Radiobutton(meal_plan_label_info, text="Premium", variable=meal_plan_info, value="Premium", command=price_text_change)
    meal_plan_business_info = Radiobutton(meal_plan_label_info, text="Business", variable=meal_plan_info, value="Business", command=price_text_change)
    meal_plan_economy_info = Radiobutton(meal_plan_label_info, text="Economy", variable=meal_plan_info, value="Economy", command=price_text_change)

    #Events Check Buttons
    event1_info = IntVar()
    event2_info = IntVar()
    event3_info = IntVar()
    #Event Label Frame
    event_label_info = LabelFrame(info_window, text="Choose What Event's to Apply To")
    #Check Buttons
    event1_check_button_info = Checkbutton(event_label_info, variable=event1_info, text=events[0], onvalue=1, offvalue=0)
    event2_check_button_info = Checkbutton(event_label_info, variable=event2_info, text=events[1], onvalue=1, offvalue=0)
    event3_check_button_info = Checkbutton(event_label_info, variable=event3_info, text=events[2], onvalue=1, offvalue=0)
    
    #Age

    #Save 

    #Delete

    """____Grid Widgets____"""
    #Title
    title_info.grid(column=0, row=0, columnspan=2)

    #First Name
    first_name_label_info.grid(column=0, row=1)
    first_name_entry_info.grid(column=1, row=1)

    #Last Name
    last_name_label_info.grid(column=0, row=2)
    last_name_entry_info.grid(column=1, row=2)

    #Meal Plan Radio Buttons
    meal_plan_label_info.grid(column=0, row=7, ipadx = 10, ipady = 10, columnspan=2) #label frame
    meal_plan_deluxe_info.grid(sticky=W, padx=10)
    meal_plan_premium_info.grid(sticky=W, padx=10)
    meal_plan_business_info.grid(sticky=W, padx=10)
    meal_plan_economy_info.grid(sticky=W, padx=10)

    #Events Check Buttons
    event_label_info.grid(column=0, row=8, ipadx = 10, ipady = 10)
    event1_check_button_info.grid(sticky=W, padx=10)
    event2_check_button_info.grid(sticky=W, padx=10)
    event3_check_button_info.grid(sticky=W, padx=10)
    

#change the title to react to the resort option menu
def change_title_text(resort_name):
    title_variable.set(f"Welcome to the {resort_name} Resort!")
    change_spots_label(resort_name)
    price_text_change()

def change_spots_label(resort_name):
    spots_total = get_spots_of_resort(resort_name)
    participants = get_participant_by_resort(resort_name)

    open_spots_variable.set(f"There are {spots_total[0] - len(participants)} spots open")


"""____Database____"""
#create connection to database server (to CRUD the database)
def connect_to_server():
    return sqlite3.connect('participants.db')

#end the connection to the server when changes are made 
def end_connection_server(connection):
    connection.commit()
    connection.close()


#insert a partipant into the SQL database
def enter_particpant(first_name: str, last_name: str, meal_plan: str, events: int, age: int, price: int, resort: str):
    #create connection and editor
    connect = connect_to_server()
    cursor = connect.cursor()

    #insert values into SQL server of applicant
    command = """\
        INSERT INTO users (first_name, last_name, meal_plan, events, age, price, resort)
        VALUES (?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(command, (first_name, last_name, meal_plan, events, age, price, resort)) #give values to the ? in the command

    #end connection to the server instance
    end_connection_server(connect)

    #Show Successful message for User
    showinfo("Successful Added Participant", f"The Participant {first_name} {last_name} has been successfully added to the database")
    change_title_text(resort)

#update a participants data in the SQL database
def update_particpant_data(id: int, first_name: str, last_name: str, meal_plan: str, events: int, age: int, price: int, resort: str):
    #create connection and editor
    connect = connect_to_server()
    cursor = connect.cursor()

    #update the participants info
    command = """\
        UPDATE users
        SET first_name=?, last_name=?, meal_plan=?, events=?, age=?, price=?, resort=?
        WHERE id=?"""
    cursor.execute(command, (first_name, last_name, meal_plan, events, age, price, resort, id)) #give values to the ? in the command

    #end connection to database
    end_connection_server(connect)


#Delete a paricipant
def delete_participant_by_id(id: int):
    #create connection and editor
    connect = connect_to_server()
    cursor = connect.cursor()

    #delete participant Info
    command = """\
        DELETE FROM users
        WHERE id=?"""
    cursor.execute(command, (id))

    #end connection to database
    end_connection_server(connect)


#get values by id 
def get_participant_by_resort(resort: str) -> list:
    #create connection and editor
    connect = connect_to_server()
    cursor = connect.cursor()

    #Select Statement to see participants at a certain resort
    command = """\
        SELECT *
        FROM users
        WHERE resort=?"""
    #gets a list of all the partipants
    list_of_participant = cursor.execute(command, (resort,)).fetchall() #give values to the ? in the command & feteches a list of particpants

    #end connection to the server instance & return
    end_connection_server(connect)
    return list_of_participant


#get the total spots of the resort
def get_spots_of_resort(resort_name: str) -> int:
    #create connection and editor
    connect = connect_to_server()
    cursor = connect.cursor()

    #Select Statement to get the spots by the name
    command = """\
        SELECT (spots)
        FROM resorts
        WHERE name=?"""
    #get the get the value of spots
    spots_avaliable = cursor.execute(command, (resort_name,)).fetchone() #give values to the ? in the command & fetch the one value / row

    #end connection to the server instance & return
    end_connection_server(connect)
    return spots_avaliable

"""---------------------------------- Tkinter Front-End ----------------------------------"""
root = Tk()
place_names = ["Hawaii", ""]
events = ["Snorkling", "Massage", "Fireworks / Lightshow"]

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
meal_plan_deluxe = Radiobutton(meal_plan_label, text="Deluxe", variable=meal_plan, value="Deluxe", command=price_text_change)
meal_plan_premium = Radiobutton(meal_plan_label, text="Premium", variable=meal_plan, value="Premium", command=price_text_change)
meal_plan_business = Radiobutton(meal_plan_label, text="Business", variable=meal_plan, value="Business", command=price_text_change)
meal_plan_economy = Radiobutton(meal_plan_label, text="Economy", variable=meal_plan, value="Economy", command=price_text_change)

#Events Check Buttons
event1 = IntVar()
event2 = IntVar()
event3 = IntVar()
#Event Label Frame
event_label = LabelFrame(root, text="Choose What Event's to Apply To")
#Check Buttons
event1_check_button = Checkbutton(event_label, variable=event1, text=events[0], onvalue=1, offvalue=0, command=price_text_change)
event2_check_button = Checkbutton(event_label, variable=event2, text=events[1], onvalue=1, offvalue=0, command=price_text_change)
event3_check_button = Checkbutton(event_label, variable=event3, text=events[2], onvalue=1, offvalue=0, command=price_text_change)

#Price for Participant
subtotal_variable = StringVar()
tax_variable = StringVar()
total_price_variable = StringVar()
subtotal_label = Label(root, textvariable=subtotal_variable)
tax_label = Label(root, textvariable=tax_variable)
total_price_label = Label(root, textvariable=total_price_variable)

#Paricpants List Box
list_box_array = ["Use", "this", "participant"]
list_box_variable = StringVar()
list_box_variable.set(list_box_array)
participant_listbox = Listbox(root, listvariable=list_box_variable, selectmode=SINGLE)
#Participant Label
participant_label = Label(text="Participants")

#Submit Button
sumbit_button = Button(root, text="Sumbit", command=add_paricipant)

#Title
title_variable = StringVar()
title_label = Label(textvariable=title_variable, font=font_body)
#Open spots
open_spots_variable = StringVar()
open_spots_label = Label(textvariable=open_spots_variable, font=font_body)

#Resort Name Option Menu
resorts = ["Hawaii", "Greece", "Chile", "Thailand"]
resort_selection = StringVar()
resort_selection.set("Hawaii")
resort_option_menu = OptionMenu(root, resort_selection, *resorts, command=change_title_text)

#Age Scale
age_value = IntVar()
age_scale = Scale(root, from_=0, to=150, variable=age_value, width=20, length=100, command=age_text_change, orient=HORIZONTAL)
#Age Label
age_label_variable = StringVar()
age_label = Label(root, font=("Arial Rounded MT Bold", 24), textvariable=age_label_variable)
age_text_change(age_value.get())

#set price to price labels
price_text_change()
change_title_text(resort_selection.get())


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
participant_label.grid(column=1, row=3)
participant_listbox.grid(column=1, row=4)

#Submit Button
sumbit_button.grid(column=1, row=8)

#Price for Participant
subtotal_label.grid(column=1, row=5)
tax_label.grid(column=1, row=6)
total_price_label.grid(column=1, row=7)

#Resort Name Option Menu
resort_option_menu.grid(row=0, column=0, columnspan=2)

#Title
title_label.grid(column=0, row=1, columnspan=2)
open_spots_label.grid(column=0, row=2, columnspan=2)


"""---------------------------------- Run + Binds ----------------------------------"""
#listbox
participant_listbox.bind("<Double-Button>", open_participant)

root.mainloop()