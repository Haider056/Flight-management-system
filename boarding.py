from tkinter import *
from tkinter import ttk
import sqlite3
import random

def generate_random_flight_number():
    # Generate a random flight number
    return f"FL{random.randint(100, 999)}"

def display_boarding_pass(record):
    boarding_pass_window = Tk()
    boarding_pass_window.title("E-Ticket")
    boarding_pass_window.geometry('570x230')

    # Create frames for better organization
    one = Frame(boarding_pass_window, bg='#ED1B24', width=60, height=450)
    one.pack(side=LEFT)

    two = Frame(boarding_pass_window, bg='#1B1464', width=700, height=40)
    two.pack(side=TOP)

    # Insert image
    img = PhotoImage(file='TravelAir.png')
    lbl_logo = Label(one, image=img, bg='#ED1B24')
    lbl_logo.place(x=50, y=15, anchor=NE)

    # Boarding pass title
    lbl_title = Label(two, text='E-Ticket', font=(' ', 13), fg='#fff', bg='#1B1464')
    lbl_title.place(x=305, y=6, anchor=NE)

    # Display passenger details
    lbl_passenger_name = Label(boarding_pass_window, text=f"Passenger Name: {record[1]}", font=(' ', 9))
    lbl_passenger_name.place(x=230, y=70, width=160, anchor=NE)
     
    lbl_flight_number = Label(boarding_pass_window, text=f"Flight Number: {generate_random_flight_number()}", font=(' ', 9))
    lbl_flight_number.place(x=390, y=70, width=160, anchor=NE)

    lbl_from = Label(boarding_pass_window, text='From', font=(' ', 9))
    lbl_from.place(x=140, y=110, anchor=NE)
    lbl_from_code = Label(boarding_pass_window, text=record[7], font=(' ', 9))
    lbl_from_code.place(x=165, y=130, width=75, anchor=NE)

    lbl_to = Label(boarding_pass_window, text='To', font=(' ', 9))
    lbl_to.place(x=135, y=160, anchor=NE)
    lbl_to_code = Label(boarding_pass_window, text=record[6], font=(' ', 9))
    lbl_to_code.place(x=163, y=180, width=75, anchor=NE)

    
    lbl_flight = Label(boarding_pass_window, text='Flight', font=(' ', 9))
    lbl_flight.place(x=240, y=110, anchor=NE)
    lbl_flight_code = Label(boarding_pass_window, text=record[9], font=(' ', 13))
    lbl_flight_code.place(x=255, y=130, width=75, anchor=NE)

    lbl_food = Label(boarding_pass_window, text='Food', font=(' ', 9))
    lbl_food.place(x=240, y=160, anchor=NE)
    lbl_food_code = Label(boarding_pass_window, text=record[4], font=(' ', 13))
    lbl_food_code.place(x=255, y=180, width=75, anchor=NE)

    lbl_date = Label(boarding_pass_window, text='Date', font=(' ', 9))
    lbl_date.place(x=335, y=110, anchor=NE)
    lbl_date_info = Label(boarding_pass_window, text=record[8], font=(' ', 13))
    lbl_date_info.place(x=370, y=130, width=100, anchor=NE)

    lbl_seat = Label(boarding_pass_window, text='Seat', font=(' ', 9))
    lbl_seat.place(x=335, y=160, anchor=NE)
    lbl_seat_info = Label(boarding_pass_window, text=record[10], font=(' ', 13))
    lbl_seat_info.place(x=367, y=180, width=100, anchor=NE)

    boarding_pass_window.mainloop()

# Retrieve the latest ticket details from the database
conn = sqlite3.connect('passenger_details.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM passengers ORDER BY id DESC LIMIT 1')
record = cursor.fetchone()
conn.close()

# Call the function to display the boarding pass
if record:
    display_boarding_pass(record)
else:
    print("No passenger details found.")
