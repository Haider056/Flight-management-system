import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from queue import Queue
import random
import os
import subprocess
# Create a SQLite database and a table
conn = sqlite3.connect('passenger_details.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS passengers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE,
    special_requirements TEXT,
    food_preference TEXT,
    seat_preference TEXT,
    destination_country TEXT,
    departure_airport TEXT,
    travel_date TEXT,
    airline TEXT,
    seat_allocated TEXT
)
''')
conn.commit()

class PassengerDetailsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Passenger Details")

        # Create tabs
        self.notebook = ttk.Notebook(root)

        self.personal_tab = ttk.Frame(self.notebook, style='danger.TFrame')
        self.food_tab = ttk.Frame(self.notebook)
        self.flight_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.personal_tab, text="Personal",image="image.png")
        self.notebook.add(self.food_tab, text="Food")
        self.notebook.add(self.flight_tab, text="Flight")
        self.notebook.add(self.view_tab, text="View Ticket")

        self.notebook.pack(padx=50, pady=50)
       

        # Personal tab
        self.name_label = tk.Label(self.personal_tab, text="Name:")
        self.name_entry = tk.Entry(self.personal_tab)
        self.email_label = tk.Label(self.personal_tab, text="Email:")
        self.email_entry = tk.Entry(self.personal_tab)
        self.special_requirements_label = tk.Label(self.personal_tab, text="Special Requirements:")
        self.special_requirements_entry = tk.Entry(self.personal_tab)
        self.seat_preference_label = tk.Label(self.personal_tab, text="Seat Preference:")
        self.seat_preference_combobox = ttk.Combobox(self.personal_tab, values=["Window", "Aisle", "Middle"])

        self.name_label.grid(row=0, column=0, sticky="e", pady=5)
        self.name_entry.grid(row=0, column=1, pady=5)
        self.email_label.grid(row=1, column=0, sticky="e", pady=5)
        self.email_entry.grid(row=1, column=1, pady=5)
        self.special_requirements_label.grid(row=2, column=0, sticky="e", pady=5)
        self.special_requirements_entry.grid(row=2, column=1, pady=5)
        self.seat_preference_label.grid(row=3, column=0, sticky="e", pady=5)
        self.seat_preference_combobox.grid(row=3, column=1, pady=5)

        # Food tab
        self.food_label = tk.Label(self.food_tab, text="Food Preference:")
        self.food_combobox = ttk.Combobox(self.food_tab, values=["Vegan", "Meat", "Chicken"])

        self.food_label.grid(row=0, column=0, sticky="e", pady=5)
        self.food_combobox.grid(row=0, column=1, pady=5)

        # Flight tab
        self.destination_label = tk.Label(self.flight_tab, text="Destination Country:")
        self.destination_entry = tk.Entry(self.flight_tab)
        self.departure_label = tk.Label(self.flight_tab, text="Departure Airport:")
        self.departure_entry = tk.Entry(self.flight_tab)
        self.travel_date_label = tk.Label(self.flight_tab, text="Travel Date:")
        self.travel_date_entry = tk.Entry(self.flight_tab)
        self.airline_label = tk.Label(self.flight_tab, text="Airline:")
        self.airline_entry = tk.Entry(self.flight_tab)

        self.destination_label.grid(row=0, column=0, sticky="e", pady=5)
        self.destination_entry.grid(row=0, column=1, pady=5)
        self.departure_label.grid(row=1, column=0, sticky="e", pady=5)
        self.departure_entry.grid(row=1, column=1, pady=5)
        self.travel_date_label.grid(row=2, column=0, sticky="e", pady=5)
        self.travel_date_entry.grid(row=2, column=1, pady=5)
        self.airline_label.grid(row=3, column=0, sticky="e", pady=5)
        self.airline_entry.grid(row=3, column=1, pady=5)

        # View/Update tab
        self.email_to_search_label = tk.Label(self.view_tab, text="Enter Email to Search:")
        self.email_to_search_entry = tk.Entry(self.view_tab)
        self.search_button = tk.Button(self.view_tab, text="Search",fg='white', bg='red', command=self.search_record)

        self.email_to_search_label.grid(row=0, column=0, sticky="e", pady=5)
        self.email_to_search_entry.grid(row=0, column=1, pady=5)
        self.search_button.grid(row=1, column=1, pady=5)

        # Button
        self.submit_button = tk.Button(root, text="Submit",fg='white', bg='green' , command=self.submit_details)
        self.submit_button.pack(pady=10)
       



    
    def search_record(self):
        email_to_search = self.email_to_search_entry.get()

        # Connect to the database and search for the record
        conn = sqlite3.connect('passenger_details.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM passengers WHERE email=?', (email_to_search,))
        record = cursor.fetchone()

        conn.close()

        if record:
            # Open a new window to view and update the record
            print(record)
            self.show_record_window(record)
        else:
            messagebox.showinfo("Record not found", "No record found for the provided email.")

    def show_record_window(self, record):
        record_window = tk.Toplevel(self.root)
        record_window.title("View/Update Record")

        # Display the details of the record
        record_labels = ["Name:", "Email:", "Special Requirements:", "Food Preference:",
                          "Seat Preference:", "Destination Country:", "Departure Airport:",
                          "Travel Date:", "Airline:", "Seat Allocated:"]

        for i, label in enumerate(record_labels):
            tk.Label(record_window, text=label).grid(row=i, column=0, sticky="e", pady=5)
            tk.Label(record_window, text=record[i+1]).grid(row=i, column=1, pady=5)

    def format_seat_allocation(self, seat_allocated):
        # Format the seat allocation string to include window, aisle, or middle information
        seat_mapping = {
            "A": "Window",
            "B": "Middle",
            "C": "Aisle",
            "D": "Aisle",
            "E": "Middle",
            "F": "Window"
        }

        seat_type = seat_mapping.get(seat_allocated, "Unknown")
        return "{} ({})".format(seat_allocated, seat_type)


    def submit_details(self):
        # Get data from the widgets
        name = self.name_entry.get()
        email = self.email_entry.get()
        special_requirements = self.special_requirements_entry.get()
        food_preference = self.food_combobox.get()
        seat_preference = self.seat_preference_combobox.get()
        destination_country = self.destination_entry.get()
        departure_airport = self.departure_entry.get()
        travel_date = self.travel_date_entry.get()
        airline = self.airline_entry.get()

        # Check if the user with the same email already exists
        if self.user_already_exists(email):
            messagebox.showerror("Error", "User with the same email already booked.")
            return

        # Allocate seat based on preference
        seat_allocated = self.auto_allocate_seat(seat_preference)

        # Update the database with the selected seat
        self.save_to_database(name, email, special_requirements, food_preference, seat_preference,
                              destination_country, departure_airport, travel_date, airline, seat_allocated)

        messagebox.showinfo("Seat Allocated", f"Seat {seat_allocated} allocated successfully.")

        
        subprocess.Popen(['python', 'boarding.py', name, email, departure_airport, special_requirements, airline, destination_country, seat_allocated])
    
    def save_to_database(self, name, email, special_requirements, food_preference, seat_preference,
                         destination_country, departure_airport, travel_date, airline, seat_allocated):
        conn = sqlite3.connect('passenger_details.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO passengers (name, email, special_requirements, food_preference, seat_preference,'
                       ' destination_country, departure_airport, travel_date, airline, seat_allocated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (name, email, special_requirements, food_preference, seat_preference,
                        destination_country, departure_airport, travel_date, airline, seat_allocated))
        conn.commit()
        conn.close()
        
    def user_already_exists(self, email):
        conn = sqlite3.connect('passenger_details.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM passengers WHERE email=?', (email,))
        result = cursor.fetchone()

        conn.close()

        return result is not None

  
    def auto_allocate_seat(self, preferred_seat):
    # Use a queue to auto-allocate seats based on the specified rules
     window_seats = Queue()
     aisle_seats = Queue()
     middle_seats = Queue()
 
     # Fetch all seats and put them in queues if they are not already reserved
     for row in range(1, 34):
         window_seat_A = f"A{row}"
         window_seat_F = f"F{row}"
         aisle_seat_C = f"C{row}"
         aisle_seat_D = f"D{row}"
         middle_seat_B = f"B{row}"
         middle_seat_E = f"E{row}"
 
         if self.check_seat_availability(window_seat_A):
             window_seats.put(window_seat_A)
         if self.check_seat_availability(window_seat_F):
             window_seats.put(window_seat_F)
         if self.check_seat_availability(aisle_seat_C):
             aisle_seats.put(aisle_seat_C)
         if self.check_seat_availability(aisle_seat_D):
             aisle_seats.put(aisle_seat_D)
         if self.check_seat_availability(middle_seat_B):
             middle_seats.put(middle_seat_B)
         if self.check_seat_availability(middle_seat_E):
             middle_seats.put(middle_seat_E)
 
     # Allocate seat based on preference
     if preferred_seat == "Window":
         allocated_seat = self.get_next_available_seat(window_seats)
     elif preferred_seat == "Middle":
         allocated_seat = self.get_next_available_seat(middle_seats)
     elif preferred_seat == "Aisle":
         allocated_seat = self.get_next_available_seat(aisle_seats)
     else:
         # If preference is not specified or recognized, try to allocate any available seat
         allocated_seat = self.get_next_available_seat(window_seats)
         if allocated_seat is None:
             allocated_seat = self.get_next_available_seat(middle_seats)
         if allocated_seat is None:
             allocated_seat = self.get_next_available_seat(aisle_seats)
 
     # If no seats are available in the queues, assign a random seat from A to F
     if allocated_seat is None:
         available_seats = [f"A{i}" for i in range(1, 34)] + [f"F{i}" for i in range(1, 34)]
         allocated_seat = random.choice(available_seats)
 
     # Ensure the randomly assigned seat is not reserved
     while not self.check_seat_availability(allocated_seat):
         allocated_seat = random.choice(available_seats)
 
     return allocated_seat

    def check_seat_availability(self, seat):
        conn = sqlite3.connect('passenger_details.db')
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM passengers WHERE seat_allocated=?', (seat,))
        count = cursor.fetchone()[0]

        conn.close()

        return count == 0

    def generate_new_seat(self, preferred_seat, window_seats, aisle_seats, middle_seats):
        # Generate a new seat based on the preferred seat type
        if preferred_seat.startswith("A") or preferred_seat.startswith("F"):
            return self.get_next_available_seat(window_seats)
        elif preferred_seat.startswith("B") or preferred_seat.startswith("E"):
            return self.get_next_available_seat(middle_seats)
        elif preferred_seat.startswith("C") or preferred_seat.startswith("D"):
            return self.get_next_available_seat(aisle_seats)

    def get_next_available_seat(self, seat_queue):
        if not seat_queue.empty():
            return seat_queue.get()
        else:
            return None  # No available seats
    def update_database_with_seat(self, name, email, special_requirements, food_preference, seat_preference,
                                  destination_country, departure_airport, travel_date, airline, seat_allocated):
        conn = sqlite3.connect('passenger_details.db')
        cursor = conn.cursor()

        # Insert the details into the database, including the allocated seat
        cursor.execute('INSERT INTO passengers (name, email, special_requirements, food_preference, seat_preference,'
                       ' destination_country, departure_airport, travel_date, airline, seat_allocated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (name, email, special_requirements, food_preference, seat_preference,
                        destination_country, departure_airport, travel_date, airline, seat_allocated))

        conn.commit()
        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = PassengerDetailsApp(root)
    root.mainloop()