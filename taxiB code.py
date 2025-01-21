import sqlite3
import datetime

class TaxiBookingSystem:
    def __init__(self, database_name="taxi_booking567.db"):
        self.conn = sqlite3.connect(database_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                address TEXT NOT NULL,
                phone_number TEXT NOT NULL, 
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                pickup TEXT NOT NULL,
                dropoff TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                payment_method TEXT NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        ''')
        self.conn.commit()

    def register_customer(self, title, name, email, address, phone_number, password):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO customers (title, name, email, address, phone_number, password)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, name, email, address, phone_number, password))
        self.conn.commit()

    def login_customer(self, email, password):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE email=? AND password=?', (email, password))
        customer = cursor.fetchone()
        return customer  # Returns customer details or None if not found

    def book_trip(self, customer_id, pickup, dropoff, payment_method):
        current_datetime = datetime.datetime.now()
        date = current_datetime.strftime('%Y-%m-%d')
        time = current_datetime.strftime('%H:%M:%S')

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO bookings (customer_id, pickup, dropoff, date, time, payment_method)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (customer_id, pickup, dropoff, date, time, payment_method))
        self.conn.commit()

    def view_booking(self, customer_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM bookings WHERE customer_id=?', (customer_id,))
        bookings = cursor.fetchall()
        for booking in bookings:
            print(f"Booking ID: {booking[0]}, Pickup: {booking[2]}, Dropoff: {booking[3]}, Date: {booking[4]}, Time: {booking[5]}, Payment Method: {booking[6]}")

    def cancel_booking(self, customer_id, booking_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM bookings WHERE customer_id=? AND booking_id=?', (customer_id, booking_id))
        self.conn.commit()
        print("Booking canceled successfully!")

    def amend_booking(self, customer_id, booking_id, new_pickup, new_dropoff, new_payment_method):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE bookings
            SET pickup=?, dropoff=?, payment_method=?
            WHERE customer_id=? AND booking_id=?
        ''', (new_pickup, new_dropoff, new_payment_method, customer_id, booking_id))
        self.conn.commit()
        print("Booking amended successfully!")

def registration():
    taxi_system = TaxiBookingSystem()

    registered = input("Welcome to Vice City Cabs! Get started with Registration. Already have an account? (YES/NO): ")
    if registered.upper() == "YES":
        login(taxi_system)
    elif registered.upper() == "NO":
        register(taxi_system)
    else:
        print("Invalid input. Please try again")

def register(taxi_system):
    title = input("Title: ")
    name = input("Name: ")
    email = input("Email: ")

    while "@" not in email or "." not in email:
        print("Invalid email format. Email must contain '@' and '.' symbols. Please try again")
        email = input("Please enter a valid email: ")

    telephone_number = input("Telephone number: ")

    password = input("Password: ")
    while len(password) < 8:
        print("Invalid password format. Password must be at least 8 characters long.")
        password = input("Please enter a valid password: ")

    address1 = input("Address1: ")
    town = input("Town: ")
    postcode = input("Postcode: ")
    payment_method = input("Payment method: ")

    # Store customer details in the database
    taxi_system.register_customer(title, name, email, address1, telephone_number, password)
    print(f"Well done! {name}, your registration was successful! Now you can login")
    login(taxi_system)

def login(taxi_system):
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    # Check if customer exists in the database and verify the password
    customer = taxi_system.login_customer(email, password)
    if customer:
        print("Login successful!")
        menu(taxi_system, customer[0])  # Pass customer_id to the menu
    else:
        print("Login failed. Please check your email and password.")
        login(taxi_system)

def menu(taxi_system, customer_id):
    while True:
        print("Welcome to Vice City Cabs! What would you like to do? ")
        print("1. Book a trip")
        print("2. View bookings")
        print("3. Cancel booking")
        print("4. Amend booking")
        print("5. Logout")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            book_trip(taxi_system, customer_id)
        elif choice == "2":
            taxi_system.view_booking(customer_id)
        elif choice == "3":
            cancel_booking(taxi_system, customer_id)
        elif choice == "4":
            amend_booking(taxi_system, customer_id)
        elif choice == "5":
            logout()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def book_trip(taxi_system, customer_id):
    pickup = input("Enter pickup location: ")
    dropoff = input("Enter dropoff location: ")
    payment_method = input("Enter payment method: ")

    taxi_system.book_trip(customer_id, pickup, dropoff, payment_method)
    print("Trip booked successfully!")

def cancel_booking(taxi_system, customer_id):
    booking_id = input("Enter the ID of the booking you want to cancel: ")
    taxi_system.cancel_booking(customer_id, booking_id)

def amend_booking(taxi_system, customer_id):
    booking_id = input("Enter the ID of the booking you want to amend: ")
    new_pickup = input("Enter new pickup location: ")
    new_dropoff = input("Enter new dropoff location: ")
    new_payment_method = input("Enter new payment method: ")

    taxi_system.amend_booking(customer_id, booking_id, new_pickup, new_dropoff, new_payment_method)
    print("Booking amended successfully!")

def logout():
    print("Logout successful!")

def main():
    registration()

if __name__ == "__main__":
    main()
