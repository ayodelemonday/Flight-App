import tkinter as tk
import tkinter.messagebox as message
import sqlite3
import subprocess
from tkinter import ttk
from tkinter import END

master = tk.Tk()
master.geometry("1000x1000+300+0")
master.title("Admin Dashboard")
master.configure(background= "#141444")

# CRUD
# C = CREATE
# R = READ
# U = UPDATE
# D = DELETE

def frontdesk():
    subprocess.popen(["python", "office.py"])



def fetch_data():
    con = sqlite3.connect("Airline.db")
    cur = con.cursor()
    cur.execute("""
                select * from flights
                """)
    rows = cur.fetchhall()
    con.close
    return rows



def display_data():
    for row in fetch_data():
        tree.insert("" ,END, value= row)


# C = CREAT
def add():
    flight_number = entry1.get()
    origin = entry2.get()
    departure_time = entry3.get()
    arrival_time = entry4.get()
    destination = entry5.get()

    if flight_number == "" or origin == "" or departure_time == "" or arrival_time == "" or destination == "":
        message.showinfo("prompt", "Empty Record Not Allowed, Please Fill The Form")
        
    elif flight_number and origin and departure_time and arrival_time and destination:
        con = sqlite3.connect("Airline.db")
        cur = con.cursor()
        cur.execute('''
                insert into flights(flight_number, origin, departure_time, arrival_time, destination)
                    values(?,?,?,?,?)''', (flight_number, origin, departure_time, arrival_time, destination))
        
        message.showinfo("Alert", "Record sent to Flights Table")
        con.commit()
        con.close()

        entry1.delete(0, tk.END)
        entry2.delete(0, tk.END)
        entry3.delete(0, tk.END)
        entry4.delete(0, tk.END)
        entry5.delete(0, tk.END)

# R = READ (search)
def search():
    flight_number = entry1.get()

    if flight_number:
        con = sqlite3.connect("Airline.db")
        cur = con.cursor() 
        cur.execute("""
                    select flight_number,origin, departure_time, arrival_time, destination
                    from flights where flight_number = ?
                    """, (flight_number,))
        


        result = cur.fetchone()
        con.close()


        if result:
            entry2.insert(0, result[1])
            entry3.insert(0, result[2])
            entry4.insert(0, result[3])
            entry5.insert(0, result[4])

        else:
            message.showinfo("promt", "record doesnt exist in the flight table")
            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)
            entry3.delete(0, tk.END)
            entry4.delete(0, tk.END)
            entry5.delete(0, tk.END)

# U = UPDATE(update flight button) get what we need from thr entries

def update():
    flight_number = entry1.get()
    origin = entry2.get()
    departure_time = entry3.get()
    arrival_time = entry4.get()
    destination = entry5.get()
    
    if flight_number and origin and departure_time and arrival_time and destination:
        con = sqlite3.connect("Airline.db")
        cur = con.cursor()
        cur.execute("""
                    update flights 
                    set origin = ?, departure_time = ?, arrival_time = ?, destination = ?
                    where flight_number = ?
                    """, (origin, departure_time, arrival_time, destination, flight_number))
        
        con.commit()
        con.close()

        if cur.rowcount > 0:
            message.showinfo("Alert", "Record update successfull")

            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)
            entry3.delete(0, tk.END)
            entry4.delete(0, tk.END)
            entry5.delete(0, tk.END)

        else:
            message.showinfo("prompt", "Record not found")
    else:message.showinfo("prompt", "please enter your number")        



        


label = tk.Label(master, text= "Flight Dashboard", font= ("verdana", 50, "bold"), fg= "#ffffff", bg= "#141444")
label.place(x= 250, y= 0)

leftframe = tk.Frame(master, width= 500, height= 1000)
leftframe.place(x= 0, y= 150)

label1 = tk.Label(leftframe, text= "Flight Number", fg= "#000000", font= ("verdana", 12, "bold"))
label1.place(x= 0, y= 30)

entry1 = tk.Entry(leftframe, width= 50, border= 5)
entry1.place(x= 150, y= 30)

label2 = tk.Label(leftframe, text= "Origin", fg= "#000000", font= ("verdana", 12, "bold"))
label2.place(x= 0, y= 60)

entry2 = tk.Entry(leftframe, width= 50, border= 5)
entry2.place(x= 150, y= 60)

label3 = tk.Label(leftframe, text= "Departure Time", fg= "#000000", font= ("verdana", 12, "bold"))
label3.place(x= 0, y= 90)

entry3 = tk.Entry(leftframe, width= 50, border= 5)
entry3.place(x= 150, y= 90)

label4 = tk.Label(leftframe, text= "Arrival Time", fg= "#000000", font= ("verdana", 12, "bold"))
label4.place(x= 0, y= 120)

entry4 = tk.Entry(leftframe, width= 50, bd= 5)
entry4.place(x= 150, y= 120)

label5 = tk.Label(leftframe, text= "Destination", fg= "#000000", font= ("verdana", 12, "bold"))
label5.place(x= 0, y= 150)

entry5 = tk.Entry(leftframe, width= 50, bd= 5)
entry5.place(x= 150, y= 150)

btnAdd = tk.Button(leftframe, text= "Add Flight", fg= "#000000", bg= "#ffffff", command= add)
btnAdd.place(x= 150, y= 180)

btnSearch = tk.Button(leftframe, text= "Search", bg= "#ffffff", fg= "#000000",command= search)
btnSearch.place(x= 230, y= 180)

btnUpdate = tk.Button(leftframe, text= "Update Flight", bg= "#ffffff", fg= "#000000",command= update)
btnUpdate.place(x= 290, y= 180)

btnDelete = tk.Button(leftframe, text= "Delete Flight", bg= "#ffffff", fg= "#000000")
btnDelete.place(x= 385, y= 180)


labelfront = tk.Button(master, text= "Go to front desk", font= ("verdana", 10, "bold"), bg= "white", fg= "#3b3b3f", command= frontdesk)
labelfront.place(x= 600, y= 80)

rightframe = tk.Frame(master, width= 500, height= 1000, bg= "#80184c")
rightframe.place(x= 500, y= 150)


labelright =  tk.Label(rightframe, text= "Flight Booking")
labelright.place(x= 0, y= 0)
cols = ("ID", "Flight number", "Origin", "Departure time", "Arrival_time", "Destination")
tree = ttk.Treeview(rightframe,columns= cols, show= "headings")

for col in cols:
    tree.heading(col, text= col)
    tree.column(col, width= 80)

tree.place(x= 0, y=50)


display_data()







master.mainloop()
