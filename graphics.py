# imports required
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import mysql.connector
import random
from datetime import datetime, date
from tkcalendar import *

# setting up connection
mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="fbs")
mycursor = mydb.cursor()

# starting tkinter window
root = Tk()
root.title("Flyter - 12th Board Project")

# defining the needed globals
menu_listbox = Listbox(root, width=103, height=12, font=("Times New Roman", 13))
button_list = {}
booked_seats = {}
active_buttons = 0


# defining functions
def new_trip():
    # changing current location and then creating a new trip for the next day
    # which has the location and departure point reversed and date as next date
    pass


def final_page():
    thanks_window = Toplevel(root)
    thanks_window.geometry("500x500")
    thanks_window.title("Seat Selection Window")
    thanks_window.configure(bg="#dfe8e9")
    thanks_window.resizable(width=False, height=False)

    mycursor.execute('''SELECT *
                        FROM seats
                        WHERE passenger_id = {}'''
                     .format(pass_id))
    x = len(mycursor.fetchall())

    date = cal.get_date()

    Label(thanks_window, text="Thank you for choosing Flyter!", bg="#dfe8e9", font=("Times New Roman", 13)).pack()
    Label(thanks_window, text="{} seat(s) have been booked for date : {}".format(x, date), bg="#dfe8e9",
          font=("Times New Roman", 13)).pack()
    Label(thanks_window, text="We hope to see you again!", bg="#dfe8e9", font=("Times New Roman", 13)).pack()

    Button(thanks_window, text="End", bg="#545454", fg="#f6f6ef", pady="3", padx="4", font=("Times New Roman", 13),
           command=root.destroy).pack()


def select_seat(seat_number):
    global active_buttons
    if button_list[seat_number].cget("bg") == "#f2efe6":
        button_list[seat_number].config(bg="green", fg="green")
        active_buttons += 1
        booked_seats[seat_number] = seat_number
        # print(booked_seats)
        return 1
    else:
        return 0


def unselect_seat(seat_number):
    global active_buttons
    if button_list[seat_number].cget("bg") == "green":
        button_list[seat_number].config(bg="#f2efe6", fg="#f2efe6")
        active_buttons -= 1
        booked_seats.pop(seat_number)
        # print(booked_seats)


def book_seats(seat_number):
    c = int(size.get())
    if select_seat(seat_number) != 1:
        unselect_seat(seat_number)
    if active_buttons > c:
        unselect_seat(seat_number)


def confirm_booking(passenger_array, trip_id):
    global pass_id
    if active_buttons == int(size.get()):
        pass_id = random.randint(0, 99999999)
    # when we eventually create a login system a user id will be defined for that particular yser at time of sign up
        # so we can remove this
        i = 0
        for key in booked_seats:
            # print(i)
            # print(passenger_array[i])
            mycursor.execute('''UPDATE seats
                                SET status = {},passenger_name = "{}", passenger_id = {}
                                WHERE seat_number = {} 
                                AND trip_id = {}'''
                             .format(2, passenger_array[i], pass_id, key, trip_id))
            mydb.commit()
            i += 1

        mycursor.execute('''UPDATE trip
                            SET seats_left = seats_left - {}
                            where trip_id = {}'''
                         .format(i, trip_id))
        mydb.commit()

        new_trip()

        final_page()
    else:
        pass


def confirm_travellers(passenger_box_array, passenger_array):
    for i in range(0, len(passenger_box_array)):
        passenger_name = passenger_box_array[i].get("1.0", "end").strip()
        passenger_array.append(passenger_name)


def place_labels(seats_window):
    Label(seats_window, text="A", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=65, y=5)
    Label(seats_window, text="B", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=115, y=5)
    Label(seats_window, text="C", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=165, y=5)

    Label(seats_window, text="D", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=320, y=5)
    Label(seats_window, text="E", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=370, y=5)
    Label(seats_window, text="F", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=420, y=5)

    for i in range(0, 30):
        row_number = i + 1
        y_coord = row_number * 30
        Label(seats_window, text="{}".format(row_number), bg="#dfe8e9", font=("Times New Roman", 13)) \
            .place(x=10, y="{}".format(y_coord))


def pull_seats(seats_window, trip_det):
    route_id = get_route_id(trip_det[2], trip_det[4])
    # print(route_id)
    trip_id = get_trip_id(trip_det[0], route_id, trip_det[6])
    # print(trip_id)

    seat_number = 1
    for i in range(0, 30):
        for j in range(0, 6):
            mycursor.execute('''SELECT status
                                FROM seats
                                WHERE trip_id = {}
                                and seat_number = {}'''
                             .format(trip_id, seat_number))

            status = mycursor.fetchall()[0][0]
            seat_number += 1

            if j <= 2:
                a = 58 + (j * 50)
                b = ((i + 1) * 30)
                if status == 0:
                    x = i * 6 + j + 1
                    button = Button(seats_window, text=x, activebackground="#c7ffd8",
                                    activeforeground="#c7ffd8",
                                    bd=2, bg="#f2efe6", fg="#f2efe6", relief=RIDGE,
                                    height=1, width=3, command=lambda bound_x=x: book_seats(bound_x))
                    button.place(x="{}".format(a), y="{}".format(b))
                    button_list[x] = button

                elif status == 1:
                    button = Button(seats_window,
                                    bd=2, bg="red", fg="red", relief=RIDGE,
                                    height=1, width=3, state=DISABLED, command="")
                    button.place(x="{}".format(a), y="{}".format(b))

                elif status == 2:
                    button = Button(seats_window,
                                    bd=2, bg="blue", fg="blue", relief=RIDGE,
                                    height=1, width=3, state=DISABLED, command="")
                    button.place(x="{}".format(a), y="{}".format(b))

            else:
                a = 163 + (j * 50)
                b = ((i + 1) * 30)
                if status == 0:
                    x = i * 6 + j + 1
                    button = Button(seats_window, text=x, activebackground="#c7ffd8",
                                    activeforeground="#c7ffd8",
                                    bd=2, bg="#f2efe6", fg="#f2efe6", relief=RIDGE,
                                    height=1, width=3, command=lambda bound_x=x: book_seats(bound_x))
                    button.place(x="{}".format(a), y="{}".format(b))
                    button_list[x] = button
                elif status == 1:
                    button = Button(seats_window,
                                    bd=2, bg="red", fg="red", relief=RIDGE,
                                    height=1, width=3, state=DISABLED, command="")
                    button.place(x="{}".format(a), y="{}".format(b))

                elif status == 2:
                    button = Button(seats_window,
                                    bd=2, bg="blue", fg="blue", relief=RIDGE,
                                    height=1, width=3, state=DISABLED, command="")
                    button.place(x="{}".format(a), y="{}".format(b))
    # print(available_buttons)


def page2(trip_det):
    seats_window = Toplevel(root)
    seats_window.geometry("940x940")
    seats_window.title("Seat Selection Window")
    seats_window.configure(bg="#dfe8e9")
    seats_window.resizable(width=False, height=False)

    place_labels(seats_window)
    pull_seats(seats_window, trip_det)

    route_id = get_route_id(trip_det[2], trip_det[4])
    trip_id = get_trip_id(trip_det[0], route_id, trip_det[6])

    passenger_array = []
    passenger_box_array = []
    c = int(size.get())
    temp = ""
    for i in range(0, c):
        Label(seats_window, text="Passenger {}'s Full Name:".format(i + 1), bg="#dfe8e9",
              font=("Times New Roman", 13)).place(x=730, y=10 + i * 90)
        name = Text(seats_window, height=2, width=23)
        passenger_box_array.append(name)
        name.place(x=730, y=40 + i * 90)
        temp = 120 + i * 90

    Button(seats_window, text="Confirm Travellers", bg="#545454", fg="#f6f6ef", pady="3", padx="4",
           font=("Times New Roman", 13),
           command=lambda: confirm_travellers(passenger_box_array, passenger_array)).place(x=750, y=temp)

    Button(seats_window, text="Confirm Booking", bg="#545454", fg="#f6f6ef", pady="3", padx="9",
           font=("Times New Roman", 13),
           command=lambda: confirm_booking(passenger_array, trip_id)).place(x=750, y=890)


def call_trip(trip_det):
    page2(trip_det)


def get_route_id(dpt_city, arr_city):
    mycursor.execute('''SELECT route_id
                        FROM route
                        WHERE dpt_city = '{}' 
                        AND arr_city = '{}' '''
                     .format(dpt_city, arr_city))

    """because it will return a list fo tuples so double index"""
    return mycursor.fetchall()[0][0]


def get_trip_id(p_id, r_id, date):
    # print(">{}<".format(p_id))
    # print(">{}<".format(r_id))
    # print(">{}<".format(date))

    mycursor.execute('''SELECT trip_id
                        FROM trip
                        WHERE plane_id = {} 
                        AND route_id = {}
                        AND DATE(trip_date) = '{}'
                        '''
                     .format(p_id, r_id, date))

    return mycursor.fetchall()[0][0]


def check_trip(trip_details):
    trip_det = trip_details
    a = trip_details[0]
    b = get_route_id(trip_details[2], trip_details[4])
    c = cal.get_date()

    query1 = '''SELECT *
                FROM trip
                where (plane_id IS NOT NULL AND plane_id = {})
                AND (route_id IS NOT NULL AND route_id = {})
                AND (trip_date IS NOT NULL AND trip_date = "{}" ) '''.format(a, b, c)

    # print(query1)

    mycursor.execute(query1)
    if len(mycursor.fetchall()) > 0:
        call_trip(trip_det)
    else:
        pass
        # need to add a or some way to get back to main screen and inform user
        # that this trip does not exist


def proceed():
    selected = menu_listbox.curselection()
    selected_trip = ""
    if selected:
        selected_trip = menu_listbox.get(selected)
        check_trip(selected_trip)
    else :
        messagebox.showerror("ERROR: Nothing Selected", "No flight has been chosen. To continue please select the "
                                                        "same from the displayed options")
    # add an else clause to put up error boxes for multiple selections


def swap(loc, dst):
    a = loc.get()
    b = dst.get()

    dst.set(a)
    loc.set(b)

    menu_listbox.delete(0, "end")

    search(loc, dst, cal, size)


def establish(arr):
    Label(text="Flight Number", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=47, y=535)
    Label(text="Departure City", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=207, y=535)
    Label(text="Arrival City", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=357, y=535)
    Label(text="Departure Date", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=550, y=535)
    Label(text="Departure Time", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=745, y=535)
    Label(text="Arrival Time", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=885, y=535)

    menu_listbox.place(x=47, y=580)


    count = 0
    for val in arr:
        val_1 = val.copy()
        # [1, 2, 3, 4, 5, 6]
        val_1.insert(1, str((32 - len(str(val[0]))) * " "))
        # [1, , 2, 3, 4, 5, 6]
        val_1.insert(3, (26 - len(str(val[1]))) * ' ')
        val_1.insert(5, (35 - len(str(val[2]))) * ' ')
        val_1.insert(7, (32 - len(str(val[3]))) * ' ')
        val_1.insert(9, (25 - len(str(val[4]))) * ' ')
        menu_listbox.insert(END, val_1)
        count += 1

    if count == 0:
        messagebox.showerror("ERROR : NO SUCH TRIP", "No flights are available that fit the desired parameters. "
                                                     "Please consider checking again at a later date." )


def no_errors(a, b, d):
    if a == b:
        messagebox.showerror("ERROR : Location = Destination",
                             "The departure and arrival cities selected are the same. Please select different cities "
                             "to continue")
        return False

    elif a == "Departure City" or b == "Arrival City":
        messagebox.showerror("ERROR : Location and/or Destination not selected",
                             "The departure and/or arrival cities are not selected. Please select both cities "
                             "to continue")
        return False

    elif d == "Number of Tickets":
        messagebox.showerror("ERROR : Number of Tickets not selected",
                             "The number of tickets required has not been selected. Please select the same "
                             "to continue")

    elif a != "Departure City" and b != "Arrival City" and a != b and d != "Number of Tickets":
        return True


def search(loc, dst, cl, s):
    possible_flights = []
    a = loc.get()
    b = dst.get()
    c = cl.get_date()
    d = s.get()

    truth_val = no_errors(a, b, d)
    route_id = 0

    if truth_val == True:
        mycursor.execute(''' SELECT route_id 
                             FROM route 
                             WHERE dpt_city = '{}' 
                             AND arr_city = '{}' 
                             '''.format(a.strip(), b.strip()))
        for x in mycursor.fetchone():
            route_id = x

        mycursor.execute('''SELECT trip.plane_id, route.dpt_city, route.arr_city,
                            DATE(trip.trip_date), route.dpt_time, route.arr_time
                            FROM route
                            JOIN trip ON trip.route_id = route.route_id
                            WHERE trip.seats_left > {}
                            AND trip.route_id = {}
                            AND trip.trip_date = "{}"
                    '''.format(int(d), route_id, c))

        for x in mycursor.fetchall():
            x = list(x)
            possible_flights.append(x)

        menu_listbox.delete(0, "end")

        establish(possible_flights)
    # else:
    #   messagebox.showwarning("WARNING", "An unknown error has occurred. Please try again")


def page1():
    global swap_photo
    global banner
    global cal
    global size

    root.geometry("1200x900")
    root.resizable(width=False, height=False)
    root.configure(bg="#dfe8e9")

    banner = ImageTk.PhotoImage(Image.open(r"C:\Users\Dell\Proj\FlightSystem\images\Flyter_Banner.png"))
    Label(image=banner).place(x=0, y=0)

    Label(text="Leaving From", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=47, y=422)
    location = StringVar(root)
    location.set("Departure City")
    lt = OptionMenu(root, location, "kolkata", "bengaluru", "chennai", "mumbai")
    lt.place(x=47, y=452)
    lt.config(pady="3", padx="4", font=("Times New Roman", 13))
    lt["menu"].config(font=("Times New Roman", 13))

    Label(text="Destination", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=327, y=422)
    destination = StringVar(root)
    destination.set("Arrival City")
    dt = OptionMenu(root, destination, "kolkata", "bengaluru", "chennai", "mumbai")
    dt.place(x=327, y=452)
    dt.config(pady="3", padx="4", font=("Times New Roman", 13))
    dt["menu"].config(font=("Times New Roman", 13))

    Label(text="Departure Date", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=560, y=422)
    cal = DateEntry(root, selectmode="day", year=2022, month=4, day=1, font=("Times New Roman", 13),
                    date_pattern="yyyy-mm-dd", height=3, width=18)
    cal.place(x=560, y=452)

    Label(text="No. Of Tickets", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=793, y=422)
    size = StringVar(root)
    st = OptionMenu(root, size, "1", "2", "3", "4", "5", "6", "7", "8", "9")
    size.set("Number of Tickets")
    st.place(x=793, y=452)
    st.config(pady="3", padx="4", font=("Times New Roman", 13))
    st["menu"].config(font=("Times New Roman", 12))

    # clicked = StringVar()
    # sort_menu = OptionMenu(root, clicked, "Earliest", "Cheapest", "Quickest", "Most Seats Left")
    # sort_menu.config(bg="#545454", fg="#f6f6ef", pady="3", padx="4", font=("Times New Roman", 13))
    # sort_menu["menu"].config(bg="#545454", fg="#f6f6ef", font=("Times New Roman", 12))
    # clicked.set("Sort By")
    # sort_menu.place(x=1040, y=540)

    swap_photo = PhotoImage(file=r"C:\Users\Dell\Proj\FlightSystem\images\finalSwap.png")
    swap_button = Button(root, image=swap_photo, height=25, width=30,
                         command=lambda: swap(location, destination))
    swap_button.place(x=245, y=452)

    Button(text="Search", bg="#545454", fg="#f6f6ef", pady="3", padx="4", font=("Times New Roman", 13),
           command=lambda: search(location, destination, cal, size)).place(x=1050, y=452)

    Button(text="Exit", bg="#545454", fg="#f6f6ef", pady="3", padx="4", font=("Times New Roman", 13),
           command=quit).place(x=47, y=850)

    Button(text="Proceed", bg="#545454", fg="#f6f6ef", pady="3", padx="4", font=("Times New Roman", 13),
           command=lambda: proceed()).place(x=1050, y=850)


# main
page1()
root.mainloop()
