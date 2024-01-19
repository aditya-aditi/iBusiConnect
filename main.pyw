import customtkinter as ctk
from tkinter import ttk
from tkinter.messagebox import showinfo
import welcomewin as ww
from bson import ObjectId
import pymongo

ww.startingWinFunc()

ctk.set_appearance_mode("dark")

#connect to database
myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iBusiConnect"]
print("Connecting to MongoDB")

#creating a collection
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["ibusiconnect"]

myclientcol = mydb["clients"]
mysalescol = mydb["sales"]

def addingclient():
    # Find the maximum _id in the collection and increment it by 1
    max_id = myclientcol.find_one(sort=[("_id", pymongo.DESCENDING)])
    new_id = 1 if max_id is None else max_id["_id"] + 1

    clientInfo = {"_id": new_id, "client_name": nameEntry.get(), "client_address": addressEntry.get(), "client_phone": phoneEntry.get()}
    myclientcol.insert_one(clientInfo)
    
    showinfo('Alert!', 'Client Added Successfully')



def addSales():
    salesInfo = {"client_id": clientIdEntry.get(), "sale_date": saleDateEntry.get(), "item_bought": itemBoughtEntry.get()}
    mysalescol.insert_one(salesInfo)

    showinfo('Alert!', 'Sale Added Successfully')

def refresh_data_clients():
    # Clear the Treeview
    view_client_table.delete(*view_client_table.get_children())

    # Fetch updated data from MongoDB
    client_datas = myclientcol.find()

    # Insert the updated data into the Treeview
    i = 0
    for client_data in client_datas:
        if client_data['client_name'] == "Dummy":
            continue
        else:
            client_id = client_data['_id']
            client_name = client_data['client_name']
            client_address = client_data['client_address']
            client_phone = client_data['client_phone']
            data = (client_id, client_name, client_address, client_phone)
            view_client_table.insert(parent="", index=i, values=data)
            i += 1

def refresh_data_sales():
     # Clear the Treeview
    view_sales_table.delete(*view_sales_table.get_children())

    # Fetch updated data from MongoDB
    sales_datas = mysalescol.find()

    # Insert the updated data into the Treeview
    h = 0
    for sales_data in sales_datas:
        client_id = sales_data['client_id']
        sale_date = sales_data['sale_date']
        item_bought = sales_data['item_bought']
        sale_data = (client_id, sale_date, item_bought)
        view_sales_table.insert(parent="", index=h, values=sale_data)
        h = h + 1

def change_theme(choice):
    print(choice)
    if choice == 'System':
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("green")
    elif choice == 'Dark Theme':
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    elif choice == 'Light Theme':
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("iBusiConnect")
window.geometry("896x510")

basicFuncTabView = ctk.CTkTabview(window, width=890, height=504)
basicFuncTabView.pack(fill = "both", expand = True)

tab1 = basicFuncTabView.add("Add Client")
tab2 = basicFuncTabView.add("Add Sales")
tab3 = basicFuncTabView.add("View Client")
tab4 = basicFuncTabView.add("View Sales")
tab5 = basicFuncTabView.add("Settings")

# Add Client tab
nameEntry = ctk.CTkEntry(tab1, placeholder_text="Client Name", width=600)
nameEntry.pack(pady=30, padx=15)

addressEntry = ctk.CTkEntry(tab1, placeholder_text="Client Address", width=600)
addressEntry.pack(pady=30, padx=15)

phoneEntry = ctk.CTkEntry(tab1, placeholder_text="Client Phone Number", width=600)
phoneEntry.pack(pady=30, padx=15)

addClientBtn = ctk.CTkButton(tab1, text="Add Client", width=200, command=addingclient)
addClientBtn.pack(pady=10)


# Add Sales Tab
clientIdEntry = ctk.CTkEntry(tab2, placeholder_text="Client ID", width=600)
clientIdEntry.pack(pady=30)

saleDateEntry = ctk.CTkEntry(tab2, placeholder_text="Sale Date", width=600)
saleDateEntry.pack(pady=30)

itemBoughtEntry = ctk.CTkEntry(tab2, placeholder_text="Item Bought", width=600)
itemBoughtEntry.pack(pady=30)

addSaleBtn = ctk.CTkButton(tab2, text="Add Sale", width=200, command=addSales)
addSaleBtn.pack(pady=10)

#table style
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="#2a2d2e",
                foreground="white",
                rowheight=35,
                fieldbackground="#343638",
                bordercolor="#343638",
                borderwidth=0)
style.map('Treeview', background=[('selected', '#22559b')])

style.configure("Treeview.Heading",
                background="#565b5e",
                foreground="white",
                relief="flat")
style.map("Treeview.Heading",
            background=[('active', '#3484F0')])

# View Clients Table
view_client_table = ttk.Treeview(tab3, columns=('client_id', 'client_name', 'client_address', 'client_phone'), show='headings')
view_client_table.heading('client_id', text="Client ID")
view_client_table.heading('client_name', text="Client Name")
view_client_table.heading('client_address', text="Client Address")
view_client_table.heading('client_phone', text="Client Phone")
view_client_table.pack(fill='both', expand=True)

#Refresh Data button
refresh_btn = ctk.CTkButton(tab3, text="Refresh Data", command=refresh_data_clients)
refresh_btn.pack()

client_datas = myclientcol.find()

i = 0
for client_data in client_datas:
    if client_data['client_name'] == "Dummy":
        continue
    else:
        client_id = client_data['_id']
        client_name = client_data['client_name']
        client_address = client_data['client_address']
        client_phone = client_data['client_phone']
        data = (client_id, client_name, client_address, client_phone)
        view_client_table.insert(parent="", index=i, values=data, iid=client_id)
        i = i + 1

# View Sales Table
view_sales_table = ttk.Treeview(tab4, columns=('client_id', 'sale_date', 'item_bought'), show='headings')
view_sales_table.heading('client_id', text="Client ID")
view_sales_table.heading('sale_date', text="Sale Date")
view_sales_table.heading('item_bought', text="Item Bought")
view_sales_table.pack(fill='both', expand=True)

#Refresh Data button
refresh_btn = ctk.CTkButton(tab4, text="Refresh Data", command=refresh_data_sales)
refresh_btn.pack()

sales_datas = mysalescol.find()

h = 0
for sales_data in sales_datas:
    client_id = sales_data['client_id']
    sale_date = sales_data['sale_date']
    item_bought = sales_data['item_bought']
    sale_data = (client_id, sale_date, item_bought)
    view_sales_table.insert(parent="", index=h, values=sale_data)
    h = h + 1

# Settings Tab
change_theme_optmenu = ctk.CTkOptionMenu(tab5, values=['Dark Theme', 'Light Theme'], command=change_theme)
change_theme_optmenu.set('Select..')
change_theme_optmenu.pack()

window.mainloop()