from textwrap import fill
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
Do you wanna Save this Information at the {resort_selected} Resort (Subsidary of Himmapan Resorts):
    First Name: {fname}
    Last Name: {lname}
    Meal Plan: {meal_plan_selected}
    Number of Events Selected: {int(events_selected)}

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

#update the list box with all the pariticpants
def update_list_box(resort_name: str):
    global list_box_array
    #Get all the participants in the resort
    participants = get_participant_by_resort(resort_name)

    list_box_array = [] #empty the array 
    #add all the participants to the existing list
    for user in participants:
        new_participant = f"{user[0]} {user[1]} {user[2]}"
        list_box_array.append(new_participant)

    #set the list to the list box variable
    list_box_variable.set(list_box_array) 

def open_participant(value):
    """____Info Page Functionaility____"""
    #get the index / component user is on
    user_index = participant_listbox.curselection()[0]
    #get the string and ID of the participant
    user_string = list_box_array[user_index]
    #create list of user's details
    participant_details = get_participant_by_id(user_string.split()[0]) #gets the id from the user's string, split it to get the id by itself
    
    previous_resort = participant_details[0][7] #used to refresh when changed

    #set all the widget components to the participant's details
    def update_info_widgets():
        #set the first name and last name entries
        first_name_entry_info.insert(0, participant_details[0][1])
        last_name_entry_info.insert(0, participant_details[0][2])
        #set the meal plan radio button
        meal_plan_info.set(participant_details[0][3])
        #set the events check buttons
        events_selected = participant_details[0][4]
        events_selected = "{:.2f}".format(events_selected)
        events_selected = float(events_selected)
        if events_selected == 1: #Snorkling selected
            event1_check_button_info.select()
        elif events_selected == 1.1: #Massage selected
            event2_check_button_info.select()
        elif events_selected == 1.11: #fireworks / lightshow selected
            event3_check_button_info.select() 
        elif events_selected == 2.1: #snorkling & massage selected
            event1_check_button_info.select() 
            event2_check_button_info.select()
        elif events_selected == 2.11: #snorkling & fireworks selected
            event1_check_button_info.select()
            event3_check_button_info.select()
        elif events_selected == 2.21: #fireworks & snorkling selected
            event2_check_button_info.select()
            event3_check_button_info.select()
        elif events_selected == 3.21: #all selected
            event1_check_button_info.select()
            event2_check_button_info.select()
            event3_check_button_info.select()


        #Set the age for the radio button
        age_label_variable_info.set(f"Age: {participant_details[0][5]}")
        age_value_info.set(participant_details[0][5])
        #Set the option menu to the user's
        resort_selection_info.set(participant_details[0][7])


    #delete the participant's profile
    def delete_profile():
        delete_participant_by_id(participant_details[0][0]) #call delete function
        info_window.destroy() #exit the window
        change_title_text(participant_details[0][7]) #refresh main page

    #save and update the participant's profile
    def save_participant_detail():
        #Check age & set it to variable
        age = age_value_info.get()
        #get and save first 
        fname = first_name_info.get()
        #get and save last name
        lname = last_name_info.get()
        #check the spots avaiable
        resort_selected = resort_selection_info.get()
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
        
        #update and save the participant's details
        else:
            update_particpant_data(participant_details[0][0], first_name_info.get(), last_name_info.get(), meal_plan_info.get(), (event1_info.get() + event2_info.get() + event3_info.get()), age_value_info.get(), price_text_change(), resort_selection_info.get())
            #refresh main screen
            change_title_text(previous_resort)
            #exit info window
            info_window.destroy()

    #change age info label
    def change_age_info_label(value):
        age_label_variable_info.set(f"Age: {value}")


    """____Info Page Widgets____"""
    #window for new page
    info_window = Toplevel(root, bg="#A5A7A7")
    info_window.title("Himmapan Resort Participant") #set title of pop-up window

    #title frame
    title_grid_info = Frame(info_window, bg="Black")
    #Option Menu
    resort_selection_info = StringVar()
    resort_option_menu_info = OptionMenu(title_grid_info, resort_selection_info, *resorts)
    resort_option_menu_info.config(font=get_font_title(35), bg="Black", fg="White")
    resort_option_menu_info.config(bg="Black", fg="White")
    resort_option_menu_info["menu"].config(bg="Black", fg="White")

    #First name Grid
    first_name_grid_info = Frame(info_window, bg="#A5A7A7")
    #First Name Text Entry
    first_name_info = StringVar()
    first_name_entry_info = Entry(first_name_grid_info, textvariable=first_name_info, width=30)
    #First Name Label
    first_name_label_info = Label(first_name_grid_info, font=get_font_body(20), text="First Name: ", bg="#A5A7A7")

    #Last Name Grid
    last_name_grid_info = Frame(info_window, bg="#A5A7A7")
    #Last Name Text Entry
    last_name_info = StringVar()
    last_name_entry_info = Entry(last_name_grid_info, textvariable=last_name_info, width=30)
    #First Name Label
    last_name_label_info = Label(last_name_grid_info, font=get_font_body(20), text="Last Name: ", bg="#A5A7A7")

    #Meal Plan Radio Buttons
    meal_plan_info = StringVar()
    #Meal Plan Label Frame
    meal_plan_label_info = LabelFrame(info_window, text="Choose a Meal Plan", font=get_font_body(20), bg="#A5A7A7")
    #Radio Buttons
    meal_plan_deluxe_info = Radiobutton(meal_plan_label_info, text="Deluxe", variable=meal_plan_info, value="Deluxe", command=price_text_change, font=get_font_body(15), bg="#A5A7A7")
    meal_plan_premium_info = Radiobutton(meal_plan_label_info, text="Premium", variable=meal_plan_info, value="Premium", command=price_text_change, font=get_font_body(15), bg="#A5A7A7")
    meal_plan_business_info = Radiobutton(meal_plan_label_info, text="Business", variable=meal_plan_info, value="Business", command=price_text_change, font=get_font_body(15), bg="#A5A7A7")
    meal_plan_economy_info = Radiobutton(meal_plan_label_info, text="Economy", variable=meal_plan_info, value="Economy", command=price_text_change, font=get_font_body(15), bg="#A5A7A7")

    #Events Check Buttons
    event1_info = DoubleVar()
    event2_info = DoubleVar()
    event3_info = DoubleVar()
    #Event Label Frame
    event_label_info = LabelFrame(info_window, text="Choose What Event's to Apply To", font=get_font_body(20), bg="#A5A7A7")
    #Check Buttons
    event1_check_button_info = Checkbutton(event_label_info, variable=event1_info, text=events[0], onvalue=1, offvalue=0, font=get_font_body(15), bg="#A5A7A7")
    event2_check_button_info = Checkbutton(event_label_info, variable=event2_info, text=events[1], onvalue=1.1, offvalue=0, font=get_font_body(15), bg="#A5A7A7")
    event3_check_button_info = Checkbutton(event_label_info, variable=event3_info, text=events[2], onvalue=1.11, offvalue=0, font=get_font_body(15), bg="#A5A7A7")
    
    #Age Scale
    age_value_info = IntVar()
    age_scale_info = Scale(info_window, from_=0, to=150, width=20, length=500, tickinterval=50, variable=age_value_info, command=change_age_info_label, orient=HORIZONTAL, font=get_font_body(10), bg="#A5A7A7")
    #Age Label
    age_label_variable_info = StringVar()
    age_label_info = Label(info_window, font=get_font_body(20), textvariable=age_label_variable_info, bg="#A5A7A7")

    #Button Frame
    button_frame_info = Frame(info_window, bg="#A5A7A7")
    #Save 
    save_button_info = Button(button_frame_info, text="Save", command=save_participant_detail, font=get_font_body(15), bg="Black", fg="White")
    #Delete
    delete_button_info = Button(button_frame_info, text="Delete", command=delete_profile, font=get_font_body(15), bg="Black", fg="White")



    """____Grid Widgets____"""
    #Title
    title_grid_info.grid(column=0, row=0, sticky=NSEW)
    #Resort Name Option Menu
    resort_option_menu_info.pack(fill="x")

    #First Name
    first_name_grid_info.grid(column=0, row=1, pady=10)
    first_name_label_info.grid(column=0, row=0)
    first_name_entry_info.grid(column=1, row=0)

    #Last Name
    last_name_grid_info.grid(column=0, row=2, pady=10)
    last_name_label_info.grid(column=0, row=0)
    last_name_entry_info.grid(column=1, row=0)

    #Meal Plan Radio Buttons
    meal_plan_label_info.grid(column=0, row=3, ipadx = 10, ipady = 10, pady=10) #label frame
    meal_plan_deluxe_info.grid(sticky=W, padx=10)
    meal_plan_premium_info.grid(sticky=W, padx=10)
    meal_plan_business_info.grid(sticky=W, padx=10)
    meal_plan_economy_info.grid(sticky=W, padx=10)

    #Events Check Buttons
    event_label_info.grid(column=0, row=4, ipadx = 10, ipady = 10, padx=20, pady=10) #label frame
    event1_check_button_info.grid(sticky=W, padx=10)
    event2_check_button_info.grid(sticky=W, padx=10)
    event3_check_button_info.grid(sticky=W, padx=10)

    #Age Scale
    age_label_info.grid(column=0, row=5)
    age_scale_info.grid(column=0, row=6, pady=10)

    #Button Frame
    button_frame_info.grid(column=0, row=7, pady=10)
    #Save Button
    save_button_info.grid(column=0, row=0, padx=25)
    #Delete Button
    delete_button_info.grid(column=1, row=0, padx=25)


    change_age_info_label(age_value_info.get())
    #set all values
    update_info_widgets()
    
#change the title to react to the resort option menu
def change_title_text(resort_name):
    title_variable.set(f"Welcome to the {resort_name} Resort!")
    change_spots_label(resort_name)
    price_text_change()
    update_list_box(resort_name)

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
    showinfo("Successful Added Participant", f"The Participant {first_name} {last_name} has been successfully added to the Himmapan Resort database")
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
    cursor.execute(command, (id,))

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


#get the details of participant by id
def get_participant_by_id(id: int) -> list:
    #create connection and editor
    connect = connect_to_server()
    cursor = connect.cursor()

    #select statement to see participants by id
    command = """\
        SELECT *
        FROM users
        WHERE id=?"""
    #get the list of all the participants
    list_of_participant = cursor.execute(command, (id,)).fetchall() #give values to the ? in the command & feteches a list of particpants

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
root.config(bg="Black") #change background to black
root.title("Himmapan Resorts") #set the title of the main page
events = ["Snorkling", "Massage", "Fireworks / Lightshow"]

#finction to get body font with custom size
def get_font_body(size: int):
    return ("Arial Rounded MT Bold", size)

#function to get custom size for title
def get_font_title(size: int):
    return ("Bauhaus 93", size)


"""____Make Widgets____"""
#seperate grid for the input data
input_data_frame = Frame(root, bg="#A5A7A7")
#seperate grid for the reading data / sumbit data
right_terminal_frame = Frame(root, bg="#4E4F4F")
#create the title frame
title_frame = Frame(root, bg="white")
#Title Option Menu frame
option_menu_frame = Frame(root, bg="Black")


#First Name Grid
first_name_grid = Frame(input_data_frame, bg="#A5A7A7")
#First Name Text Entry
first_name = StringVar()
first_name_entry = Entry(first_name_grid, textvariable=first_name, width=50)
#First Name Label
first_name_label = Label(first_name_grid, font=get_font_body(20), text="First Name: ", pady=10, bg="#A5A7A7")

#Last name grid
last_name_grid = Frame(input_data_frame, bg="#A5A7A7")
#Last Name Text Entry
last_name = StringVar()
last_name_entry = Entry(last_name_grid, textvariable=last_name, width=50)
#First Name Label
last_name_label = Label(last_name_grid, font=get_font_body(20), text="Last Name: ", pady=10, bg="#A5A7A7")

#Meal Plan Radio Buttons
meal_plan = StringVar()
meal_plan.set("Deluxe") #set the default radio button selection to deluxe
#Meal Plan Label Frame
meal_plan_label = LabelFrame(input_data_frame, text="Choose a Meal Plan", font=get_font_body(20), bg="#A5A7A7")
#Radio Buttons
meal_plan_deluxe = Radiobutton(meal_plan_label, text="Deluxe", variable=meal_plan, value="Deluxe", command=price_text_change, font=get_font_body(15), bg="#A5A7A7")
meal_plan_premium = Radiobutton(meal_plan_label, text="Premium", variable=meal_plan, value="Premium", command=price_text_change, font=get_font_body(15), bg="#A5A7A7")
meal_plan_business = Radiobutton(meal_plan_label, text="Business", variable=meal_plan, value="Business", command=price_text_change, font=get_font_body(15), bg="#A5A7A7")
meal_plan_economy = Radiobutton(meal_plan_label, text="Economy", variable=meal_plan, value="Economy", command=price_text_change, font=get_font_body(15), bg="#A5A7A7")

#Events Check Buttons
event1 = DoubleVar()
event2 = DoubleVar()
event3 = DoubleVar()
#Event Label Frame
event_label = LabelFrame(input_data_frame, text="Choose What Events to Apply To", font=get_font_body(20), bg="#A5A7A7")
#Check Buttons
event1_check_button = Checkbutton(event_label, variable=event1, text=events[0], onvalue=1, offvalue=0, command=price_text_change, font=get_font_body(15), bg="#A5A7A7")
event2_check_button = Checkbutton(event_label, variable=event2, text=events[1], onvalue=1.1, offvalue=0, command=price_text_change, font=get_font_body(15), bg="#A5A7A7")
event3_check_button = Checkbutton(event_label, variable=event3, text=events[2], onvalue=1.11, offvalue=0, command=price_text_change, font=get_font_body(15), bg="#A5A7A7")

#Price for Participant
subtotal_variable = StringVar()
tax_variable = StringVar()
total_price_variable = StringVar()
subtotal_label = Label(right_terminal_frame, textvariable=subtotal_variable, font=get_font_body(15), bg="#4E4F4F", fg="White")
tax_label = Label(right_terminal_frame, textvariable=tax_variable, font=get_font_body(15), bg="#4E4F4F", fg="White")
total_price_label = Label(right_terminal_frame, textvariable=total_price_variable, font=get_font_body(15), bg="#4E4F4F", fg="White")

#List box frame
participant_listbox_frame = Frame(right_terminal_frame)
#Scrollbar for the listbox of participants
particpants_listbox_scrollbar = Scrollbar(participant_listbox_frame)
#Paricpants List Box
list_box_array = ["Use", "this", "participant"]
list_box_variable = StringVar()
list_box_variable.set(list_box_array)
participant_listbox = Listbox(participant_listbox_frame, listvariable=list_box_variable, selectmode=SINGLE, font=get_font_body(12))
#Participant Label
participant_label = Label(right_terminal_frame, text="Participants", font=get_font_body(20), bg="#4E4F4F", fg="White")
#Config for listbox and scrollbar
participant_listbox.config(yscrollcommand=particpants_listbox_scrollbar.set)
particpants_listbox_scrollbar.config(command=participant_listbox.yview)

#Submit Button
sumbit_button = Button(right_terminal_frame, text="Submit", command=add_paricipant, width=10, font=get_font_body(20), bg="White", fg="Black")

#Title
title_variable = StringVar()
title_label = Label(title_frame, textvariable=title_variable, font=get_font_body(35), bg="White")
#Open spots
open_spots_variable = StringVar()
open_spots_label = Label(title_frame, textvariable=open_spots_variable, font=get_font_body(20), bg="White")

#Resort Name Option Menu
resorts = ["Hawaii", "Greece", "Chile", "Thailand"]
resort_selection = StringVar()
resort_selection.set("Hawaii")
resort_option_menu = OptionMenu(option_menu_frame, resort_selection, *resorts, command=change_title_text)
#change color of menu + font
resort_option_menu.config(bg="Black", fg="White", font=get_font_title(35))
resort_option_menu["menu"].config(bg="Black", fg="White")

#Age Scale
age_value = IntVar()
age_scale = Scale(input_data_frame, from_=0, to=150, variable=age_value, width=20, length=500, tickinterval=50,command=age_text_change, orient=HORIZONTAL, font=get_font_body(10), bg="#A5A7A7")
#Age Label
age_label_variable = StringVar()
age_label = Label(input_data_frame, font=get_font_body(20), textvariable=age_label_variable, bg="#A5A7A7")
age_text_change(age_value.get())


#set price to price labels
price_text_change()
change_title_text(resort_selection.get())


"""____Grid Widgets____"""
#Input Data Frame
input_data_frame.grid(column=0, row=2, sticky=NSEW)
#Right Terminal Frame
right_terminal_frame.grid(column=1, row=2, sticky=NSEW)
#title frame
title_frame.grid(column=0, row=1, columnspan=2, sticky=NSEW)
#Option Menu Title Frame
option_menu_frame.grid(column=0, row=0, columnspan=2)

#test
#First Name Text Entry
first_name_grid.grid(column=0, row=3)
first_name_label.grid(column=0, row=0, padx=10)
first_name_entry.grid(column=1, row=0, padx=10)

#Last Name Text Entry
last_name_grid.grid(column=0, row=4)
last_name_label.grid(column=0, row=0, padx=10)
last_name_entry.grid(column=1, row=0, padx=10)

#Meal Plan Radio Buttons
meal_plan_label.grid(column=0, row=5, ipadx = 10, ipady = 10) #label frame
meal_plan_deluxe.grid(sticky=W, padx=10)
meal_plan_premium.grid(sticky=W, padx=10)
meal_plan_business.grid(sticky=W, padx=10)
meal_plan_economy.grid(sticky=W, padx=10)

#Events Check Buttons
event_label.grid(column=0, row=6, ipadx = 10, ipady = 10, pady=10)
event1_check_button.grid(sticky=W, padx=10)
event2_check_button.grid(sticky=W, padx=10)
event3_check_button.grid(sticky=W, padx=10)

#Age Scale
age_label.grid(column=0, row=7, pady=5, sticky=S)
age_scale.grid(column=0, row=8, pady=10, sticky=N)

#Paricpants List Box
participant_label.grid(column=1, row=0, pady=10)
participant_listbox_frame.grid(column=1, row=1, pady=20, sticky=N, padx=25)
participant_listbox.pack(side="left", fill=BOTH) #list box
particpants_listbox_scrollbar.pack(side="right", fill=BOTH) #scroll bar for list box

#Submit Button
sumbit_button.grid(column=1, row=5, pady=50)

#Price for Participant
subtotal_label.grid(column=1, row=2, pady=10, sticky=S)
tax_label.grid(column=1, row=3, sticky=N)
total_price_label.grid(column=1, row=4, pady=10)

#Resort Name Option Menu
resort_option_menu.grid(row=0, column=0, columnspan=2, pady=10)

#Title
title_label.grid(column=0, row=1, pady=10, padx=20)
open_spots_label.grid(column=0, row=2, pady=10)


"""---------------------------------- Run + Binds ----------------------------------"""
#listbox
participant_listbox.bind("<Double-Button>", open_participant)

root.mainloop()