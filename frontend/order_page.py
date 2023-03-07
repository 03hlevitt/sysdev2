from tkinter import *
from tkinter import ttk
from backend.main import Backend


class orderListForm:

    def __init__(self):
        self.backend = Backend()
        

        def create_detailView(self):
            detailsframe = ttk.Frame(baseframe, borderwidth=10, relief="ridge", width=100, height=100)
            detailsframe.grid(column=1, row=1, sticky=(N, E, S))

            detailsframe.columnconfigure(0, weight=1)
            detailsframe.columnconfigure(1, weight=1)
            detailsframe.rowconfigure(0, weight=1)
            detailsframe.rowconfigure(1, weight=1)
            detailsframe.rowconfigure(2, weight=1)
            detailsframe.rowconfigure(3, weight=1)
            detailsframe.rowconfigure(4, weight=1)

            # details_fname_label = ttk.Label(detailsframe, text='Order ID')
            # details_fname_label.grid(column=0, row=0)
            # details_fname = ttk.Entry(detailsframe, textvariable=order_id_value)
            # details_fname.grid(column=1, row=0)

            details_lname_label = ttk.Label(detailsframe, text='Customer')
            details_lname_label.grid(column=0, row=1)
            details_lname = ttk.Entry(detailsframe, textvariable=customer_value)
            details_lname.grid(column=1, row=1)

            details_street_label = ttk.Label(detailsframe, text='Location')
            details_street_label.grid(column=0, row=2)
            details_street = ttk.Entry(detailsframe, textvariable=location_value)
            details_street.grid(column=1, row=2)

            # details_town_label = ttk.Label(detailsframe, text='Date')
            # details_town_label.grid(column=0, row=3)
            # details_town = ttk.Entry(detailsframe, textvariable=date_value)
            # details_town.grid(column=1, row=3)

            cmdframe = ttk.Frame(detailsframe, borderwidth=0, width=100, height=50)

            # command frame
            cmdframe.grid(column=0, row=4, sticky=(N, E, S))
            self.cmdOk = ttk.Button(cmdframe, text="OK", state="disabled", command=update_order)
            self.cmdOk.grid(column=0, row=0)

            self.cmdOrders = ttk.Button(cmdframe, text="Menu", state="enabled", command=go_to_menu)
            self.cmdOrders.grid(column=1, row=0)

            self.cmdAddorder = ttk.Button(cmdframe, text="Add order", state="active", command=make_order)
            self.cmdAddorder.grid(column=2, row=0)

            listframe = ttk.Frame(baseframe, borderwidth=10, relief="ridge", width=100, height=100)
            listframe.grid(column=0, row=1, sticky=(N, W, E, S))
            listframe.rowconfigure(0, weight=1)

            return listframe

        def update_buttons():
            self.cmdOk.config(state=ACTIVE)
            self.cmdOrders.config(state=ACTIVE)

        def go_to_menu():
            root.destroy()
            from frontend.menu_page import menuPage
            menuPage()

        def make_order():
            root.destroy()
            addOrderForm()

        def listtreeitem_selected(event):
            for selected_item in listtree.selection():
                order_details = self.get_Oneorder(selected_item)

                order_id_value.set(order_details[0])
                customer_value.set(order_details[1])
                location_value.set(order_details[2])
                date_value.set(order_details[3])

            update_buttons()

        def update_order():
            dts_id = order_id_value.get()
            dts_customer = customer_value.get()
            dts_location = location_value.get()
            dts_date = date_value.get()

            self.update_order_backend(dts_id, dts_customer, dts_location, dts_date)
            root.destroy()
            UpdateMsg(self.engine)

        root = Tk()
        root.title("order List")
        root.geometry("1100x600")
        root.rowconfigure(0, weight=1)

        baseframe = ttk.Frame(root)
        baseframe.grid(column=0, row=0, sticky=(N, W, E, S))
        baseframe.rowconfigure(0, weight=1)
        baseframe.rowconfigure(1, weight=4)
        baseframe.columnconfigure(0, weight=3)
        baseframe.columnconfigure(1, weight=1)

        window_title_label = ttk.Label(baseframe, text='orders', font=("Arial", 25))
        window_title_label.grid(column=0, row=0)
        window_title_label.place(relx=0.0, rely=0.0)

        order_id_value = StringVar()
        customer_value = StringVar()
        location_value = StringVar()
        date_value = StringVar()

        listtframe = create_detailView(self)
        listtree = self.create_listTree(listtframe)

        listtree.bind('<<TreeviewSelect>>', listtreeitem_selected)

        self.populate_listree(listtree)

        root.mainloop()

    def get_orders(self):
        return self.backend.view_orders()

    def update_order_backend(self, order_id, customer, location, date):
        self.backend.update_order(order_id, customer, location, date)

    def get_existing_order(self, order_id):
        return self.backend.get_existing_order(order_id)

    def populate_listree(self, listtree):
        orders = self.get_orders()

        added_orders = []
        for order in orders:
            orderValues = list(order)

            if orderValues not in added_orders:  # catching duplicates
                listtree.insert('', index='end', iid=orderValues[0], text=orderValues[0], values=(orderValues))
                added_orders.append(orderValues)

    def create_listTree(self, listframe):
        listtree = ttk.Treeview(listframe,
                                column=("id", "customer", "location", "date"),
                                show='headings', selectmode='browse')
        listtree.heading('id', text='Id')
        listtree.heading('customer', text='customer')
        listtree.heading('location', text='location')
        listtree.heading('date', text='date')
        listtree.column('id', width=30)
        listtree.column('customer', width=70)
        listtree.column('location', width=70)
        listtree.column('date', width=40)
        listtree.tag_configure('font', font=('Arial', 10))
        listtree.grid(column=0, row=0, sticky=(N, W, E, S))

        treescrolly = ttk.Scrollbar(listframe, orient=VERTICAL, command=listtree.yview)
        listtree.configure(yscrollcommand=treescrolly.set)
        treescrolly.grid(column=3, row=0, sticky=(NS))

        return listtree


class UpdateMsg:
    def __init__(self, engine):
        self.engine = engine
        self.root_update_msg = Tk()
        self.root_update_msg.title("Success.")
        self.root_update_msg.geometry("400x100")
        self.window_title_label = ttk.Label(self.root_update_msg, text='Update Successful!', font=("Arial", 15))
        self.window_title_label.pack(side=TOP, pady=10)
        self.ok_button = ttk.Button(self.root_update_msg, text="OK", default="active", command=self.destroy)
        self.ok_button.pack(side=BOTTOM, pady=10)
        self.root_update_msg.mainloop()
        orderListForm(self.engine)

    def destroy(self):
        self.root_update_msg.destroy()


fields = 'customer', 'location'


class addOrderForm:
    def __init__(self):
        self.root = Tk()
        self.root.title("Nympton Add_order")
        self.entries = self.initUI(self.root, fields)
        self.root.bind('<Return>', (lambda event, e=self.entries: self.fetch(e)))
        self.frame = Frame(self.root, relief=RAISED, borderwidth=1)
        self.frame.pack(fill=BOTH, expand=True)

        self.closeButton = Button(self.root, text="Cancel", command=self.cancel)
        self.closeButton.pack(side=RIGHT, padx=5, pady=5)
        self.okButton = Button(self.root, text="OK", command=(lambda e=self.entries: self.fetch))
        self.okButton.pack(side=RIGHT)
        self.root.mainloop()

    def fetch(self, entries):
        inputs = []
        for entry in entries:
            field = entry[0]
            text = entry[1].get()
            inputs.append(text)
        self.add_order(inputs)

    def add_order(self, inputs):
        customer = inputs[0]
        location = inputs[1]
        print("making new order with customer: " + customer + " and location: " + location + " .")
        new_order = self.backend.new_order(customer, location)
        new_order.set_order_date()
        new_order.save()

    def initUI(self, root, fields):
        entries = []
        for field in fields:
            frame = Frame(root)
            frame.pack(fill=X)

            lbl = Label(frame, text=field, width=20, anchor='w')
            lbl.pack(side=LEFT, padx=5, pady=5)

            entry = Entry(frame)
            entry.pack(fill=X, padx=5, expand=True)

            entries.append((field, entry))
        return entries

    def message(self, message, command):
        self.root_error_msg = Tk()
        self.root_error_msg.title(message)
        self.root_error_msg.geometry("400x100")
        self.window_title_label = Label(self.root_error_msg, text=message, font=("Arial", 15))
        self.window_title_label.pack(side=TOP, pady=10)
        self.ok_button = Button(self.root_error_msg, text="OK", default="active", command=command)
        self.ok_button.pack(side=BOTTOM, pady=10)
        self.root_error_msg.mainloop()

    def destroy(self):
        self.root_error_msg.destroy()

    def destroy_both(self):
        self.root_error_msg.destroy()
        self.root.destroy()
        orderListForm()

    def cancel(self):
        self.root.destroy()
        orderListForm()