from tkinter import *
from tkinter import messagebox     #imports nessesary modules
from database import Database, MoneyBase


customer_db = Database('customersdatabase.db')      #This initilizes the 2 databases i used in my program, one for the listbox and the other for the money
money_base = MoneyBase('money.db')
window = Tk()
window.title("Customer Manager")  #initilizes the tkinter window
window.geometry("785x700")


class Widget:     #i created a parent class called Widget to hold the basic blueprints of most widgets i will use in code

    def __init__(self, widget_text):

        self.widget_text = widget_text    #init function holds the widget text and font size
        self.font_size = 14

    
    def draw(self, row_num, col_num):

        pad_x = 14
        pad_y = 20
        self.widget.grid(row=row_num, column=col_num, padx=pad_x, pady=pad_y)
        

class Labels(Widget):

    def __init__(self, widget_text):

        super().__init__(widget_text)
        self.widget = Label(text=self.widget_text, font=('times', self.font_size))      #label widget inherits from widget class and will be used to make labels


class EntryField(Widget):

    def __init__(self):

        self.font_size=12
        self.data_text = StringVar()   #used to hold the value in the entryfield
        self.widget = Entry(font=("times", self.font_size), textvariable=self.data_text)       
 

class Buttons(Widget):

    def __init__(self, widget_text, button_type):
        super().__init__(widget_text)
        self.button_type = button_type  #this attribute holds the command each button will use
        self.widget = Button(text=self.widget_text, font=('times', self.font_size), width=8, command = self.button_type)


def addToList():
    
    customer_list.delete(0, END)
    for rows in customer_db.grab():     #this function will constantly update the listbox with the new customer values 
        customer_list.insert(END, rows)

def update_money(updated):   #  This function is used to update the value in the money label
    global total_money
    total_money.destroy()
    if answer.get() == "Yes":
        money_base.update_money(updated)  #gets the updated value for the money

    total_money = Label(text=f"Money Earned: ${money_base.grab_money()[0]}", font=("times", 14), borderwidth=1, relief="solid")  #recreates the label with the new money value
    total_money.grid(row=0, column=3, ipadx=3, ipady=3, pady=10)


def item_select(event):
    
    global item
    index = customer_list.curselection()[0]   #this function allows the selected value in list box to be seen in the entry fields
    item = customer_list.get(index)
    
    remove_entries()
    c_entry.widget.insert(END, item[1])
    c_location_entry.widget.insert(END, item[2])
    mac_entry.widget.insert(END, item[3])
    portal_entry.widget.insert(END, item[4])
    payment_entry.widget.insert(END, item[5])
    answer.set(item[6])


def remove_entries():
    c_entry.widget.delete(0,'end')
    c_location_entry.widget.delete(0,'end')
    portal_entry.widget.delete(0,'end')
    mac_entry.widget.delete(0,'end')
    payment_entry.widget.delete(0,'end')

def add_customer():
    if c_entry.data_text.get() == "" or c_location_entry.data_text.get() == "" or mac_entry.data_text.get() == "" or portal_entry.data_text.get() == "" or payment_entry.data_text.get() == "":

        messagebox.showerror("Error", "Please fill the textbox.")   #if any of the entryfields are empty, it will alert an error

    else: #if not, it will add the new customer info into the database and update the listbox
        update_money(float(payment_entry.data_text.get()) + money_base.grab_money()[0])
        customer_db.add(c_entry.data_text.get(), c_location_entry.data_text.get(), mac_entry.data_text.get(), portal_entry.data_text.get(),payment_entry.data_text.get(), answer.get()) #uses the database add method to add the info into the customer database in SQL
        customer_list.insert(END, (c_entry.data_text.get(), c_location_entry.data_text.get(), mac_entry.data_text.get(), portal_entry.data_text.get(),payment_entry.data_text.get(), answer.get()))
        addToList()
        remove_entries()  #clears the entry field after button click

def remove_customer():

    customer_db.remove(item[0])
    update_money(money_base.grab_money()[0] - float(payment_entry.data_text.get()) )     #this gets the index of the clicked item and it will remove it from database and listbox
    remove_entries()
    addToList()

    
def edit_customer():  #allows you to edit the selected customers info and update the changes into the database and listbox

    update_money(float(payment_entry.data_text.get()) + money_base.grab_money()[0])
    customer_db.update(item[0], c_entry.data_text.get(), c_location_entry.data_text.get(), mac_entry.data_text.get(), portal_entry.data_text.get(),payment_entry.data_text.get(), answer.get())
    addToList()
    remove_entries()

    
def clear_all():

    for rows in customer_db.grab():   #it uses the grab method in the database to see all the customers. Then it will remove each one from the database - clearing the database
        customer_db.remove(rows[0])

    update_money(0.0)
    remove_entries() 
    addToList()  


total_money = Label(text=f"Money Earned: ${money_base.grab_money()[0]}", font=("times", 14), borderwidth=1, relief="solid")
total_money.grid(row=0, column=3, ipadx=3, ipady=3, pady=10)

#Customer name label
c_name = Labels("Customer Name: ")
c_name.draw(1,0)

#Customer name entryfield
c_entry = EntryField()
c_entry.draw(1,1)

#Customer Username
c_location_label = Labels("Customer Location: ")
c_location_label.draw(1,2)

#Customer name entryfield
c_location_entry = EntryField()
c_location_entry.draw(1,3)

#M.A.C ID Label
mac_id_label = Labels("M.A.C ID: ")
mac_id_label.draw(2,0)

#mac id entry field
mac_entry = EntryField()
mac_entry.draw(2, 1)

#Portal
portal_name = Labels("Portal Name: ")
portal_name.draw(2,2)

#portal Entry
portal_entry = EntryField()
portal_entry.draw(2, 3)

#sub time label
sub_time_label = Labels("Payment Received: ")
sub_time_label.draw(3,2)

#sub time dropdown
answer = StringVar(window)
answer.set("No")
sub_time_dropdown = OptionMenu(window, answer, "Yes", "No")
sub_time_dropdown.grid(row=3, column=3)

#Payment
payment_label = Labels("Payment: ")
payment_label.draw(3,0)

#Payment Entry
payment_entry = EntryField()
payment_entry.draw(3, 1)

#Database Test Area
customer_list = Listbox(height=15, width = 80, font=("times", 14))
customer_list.grid(row=5, column=0, columnspan=4, rowspan=5, padx=15, pady=5)

#bind
customer_list.bind('<<ListboxSelect>>', item_select)

#scrollbar
scrollbar = Scrollbar()
scrollbar.grid(row=5, column=4)
customer_list.configure(yscrollcommand =scrollbar.set)
scrollbar.configure(command=customer_list.yview)

hscrollbar = Scrollbar(orient="horizontal")
hscrollbar.grid(row=10, column=0, pady=5)
customer_list.configure(xscrollcommand =hscrollbar.set)
hscrollbar.configure(command=customer_list.xview)

#buttons
add_button = Buttons("Add", add_customer)
add_button.draw(4, 0)

remove_button = Buttons("Remove", remove_customer)
remove_button.draw(4, 1)

edit_button = Buttons("Edit", edit_customer)
edit_button.draw(4, 2)

clear_button = Buttons("Clear", clear_all)
clear_button.draw(4, 3)

addToList()
window.mainloop()





