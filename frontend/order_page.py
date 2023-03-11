from tkinter import *
from tkinter import ttk
from backend.main import Backend


class orderListForm:
    def __init__(self):
        self.backend = Backend()

        def create_detail_view(self):
            detailsframe = ttk.Frame(
                baseframe,
                borderwidth=10,
                relief="ridge",
                width=100,
                height=100,
            )
            detailsframe.grid(column=1, row=1, sticky=(N, E, S))

            detailsframe.columnconfigure(0, weight=1)
            detailsframe.columnconfigure(1, weight=1)
            detailsframe.rowconfigure(0, weight=1)
            detailsframe.rowconfigure(1, weight=1)
            detailsframe.rowconfigure(2, weight=1)
            detailsframe.rowconfigure(3, weight=1)
            detailsframe.rowconfigure(4, weight=1)

            details_lname_label = ttk.Label(detailsframe, text="Customer")
            details_lname_label.grid(column=0, row=1)
            details_lname = ttk.Entry(
                detailsframe, textvariable=customer_value
            )
            details_lname.grid(column=1, row=2)

            details_street_label = ttk.Label(detailsframe, text="location")
            details_street_label.grid(column=0, row=2)
            details_street = ttk.Entry(
                detailsframe, textvariable=location_value
            )
            details_street.grid(column=1, row=3)

            cmdframe = ttk.Frame(
                detailsframe, borderwidth=0, width=100, height=50
            )

            # command frame
            cmdframe.grid(column=0, row=4, sticky=(N, E, S))
            self.cmdOk = ttk.Button(
                cmdframe, text="OK", state="disabled", command=update_order
            )
            self.cmdOk.grid(column=0, row=0)

            self.cmdOrders = ttk.Button(
                cmdframe, text="Orders", state="enabled", command=go_to_menu
            )
            self.cmdOrders.grid(column=1, row=0)

            self.cmdAddorder = ttk.Button(
                cmdframe, text="add order", state="active", command=make_order
            )
            self.cmdAddorder.grid(column=2, row=0)

            self.cmdAdd_item = ttk.Button(
                cmdframe, text="add item", state="active", command=add_item
            )
            self.cmdAdd_item.grid(column=4, row=0)

            self.cmdremove_item = ttk.Button(
                cmdframe,
                text="remove item",
                state="active",
                command=remove_item,
            )
            self.cmdremove_item.grid(column=5, row=0)

            self.cmd_delete_order = ttk.Button(
                cmdframe,
                text="delete item",
                state="active",
                command=delete_order,
            )
            self.cmd_delete_order.grid(column=3, row=0)

            listframe = ttk.Frame(
                baseframe,
                borderwidth=10,
                relief="ridge",
                width=100,
                height=100,
            )
            listframe.grid(column=0, row=1, sticky=(N, W, E, S))
            listframe.rowconfigure(0, weight=1)

            itemframe = ttk.Frame(
                baseframe,
                borderwidth=10,
                relief="ridge",
                width=100,
                height=100,
            )
            itemframe.grid(column=2, row=1, sticky=(N, W, E, S))
            itemframe.rowconfigure(0, weight=1)

            return listframe, itemframe

        def update_buttons():
            self.cmdOk.config(state=ACTIVE)
            self.cmdOrders.config(state=ACTIVE)

        def go_to_menu():
            root.destroy()
            from frontend.menu_page import MenuPage

            MenuPage()

        def make_order():
            root.destroy()
            addOrderForm()

        def clear_selected_from_input():
            customer_value.set("")
            location_value.set("")
            update_buttons()

        def itemtreeitem_selected(event):
            for selected_item in self.itemstree.selection():
                item_value.set(selected_item)
                update_buttons()

        def listtreeitem_selected(event):
            for selected_order in listtree.selection():
                order = self.backend.existing_order(selected_order)
                id_value.set(order.order_id)
                customer_value.set(order.customer)
                location_value.set(order.location_co_ords)
                self.populate_itemsTree(order.order_id)

            update_buttons()

        def update_order():
            dts_customer = customer_value.get()
            dts_location = location_value.get()
            dts_id = id_value.get()

            self.update_item_backend(dts_id, dts_customer, dts_location)
            self.populate_listree(listtree)
            UpdateMsg("Update Successful!")

        def add_item():
            dts_id = id_value.get()
            root.destroy()
            addItemForm(dts_id)

        def remove_item():
            dts_id = id_value.get()
            dts_item = item_value.get()
            order = self.backend.existing_order(dts_id)
            order.remove_items(dts_item)
            self.populate_itemsTree(dts_id)
            UpdateMsg("Item Deleted!")

        def delete_order():
            dts_id = id_value.get()
            self.delete_item_backend(dts_id)
            clear_selected_from_input()
            self.populate_listree(listtree)
            UpdateMsg("Item Deleted!")

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
        baseframe.columnconfigure(2, weight=1)

        window_title_label = ttk.Label(
            baseframe, text="Menu", font=("Arial", 25)
        )
        window_title_label.grid(column=0, row=0)
        window_title_label.place(relx=0.0, rely=0.0)

        item_value = StringVar()
        customer_value = StringVar()
        location_value = StringVar()
        id_value = StringVar()

        list_frame, item_frame = create_detail_view(self)
        listtree = self.create_listTree(list_frame)
        self.itemstree = self.create_itemsTree(item_frame)

        listtree.bind("<<TreeviewSelect>>", listtreeitem_selected)
        self.itemstree.bind("<<TreeviewSelect>>", itemtreeitem_selected)

        self.populate_listree(listtree)

        root.mainloop()

    def get_orders(self):
        return self.backend.view_orders()

    def update_item_backend(self, id, customer, location):
        item = self.backend.existing_order(id)
        item.customer = customer
        item.location_co_ords = location
        item.set_order_date()
        item.save()

    def delete_item_backend(self, id_value):
        item = self.backend.existing_order(id_value)
        item.delete()

    def get_items(self, order_id):
        order = self.backend.existing_order(order_id)
        return order.get_items()

    def populate_itemsTree(self, order_id):
        """get items from order and populate tree"""
        self.itemstree.delete(*self.itemstree.get_children())
        items = self.get_items(order_id)

        added_items = []
        for item in items:
            itemValues = list(item)
            if itemValues not in added_items:
                added_items.append(itemValues)
                self.itemstree.insert(
                    "",
                    index="end",
                    iid=itemValues[0],
                    text=itemValues[0],
                    values=(itemValues),
                )

    def populate_listree(self, listtree):
        listtree.delete(*listtree.get_children())
        orders = self.get_orders()  # TODO change this to string date at end

        added_orders = []
        for order in orders:
            orderValues = list(order)

            if orderValues not in added_orders:  # catching duplicates
                listtree.insert(
                    "",
                    index="end",
                    iid=orderValues[0],
                    text=orderValues[0],
                    values=(orderValues),
                )
                added_orders.append(orderValues)

    def create_listTree(self, listframe):
        listtree = ttk.Treeview(
            listframe,
            column=("id", "customer", "location", "order_date"),
            show="headings",
            selectmode="browse",
        )
        listtree.heading("id", text="id")
        listtree.heading("customer", text="customer")
        listtree.heading("location", text="location")
        listtree.heading("order_date", text="order date")
        listtree.column("id", width=70)
        listtree.column("customer", width=70)
        listtree.column("location", width=70)
        listtree.column("order_date", width=70)
        listtree.tag_configure("font", font=("Arial", 10))
        listtree.grid(column=0, row=0, sticky=(N, W, E, S))

        treescrolly = ttk.Scrollbar(
            listframe, orient=VERTICAL, command=listtree.yview
        )
        listtree.configure(yscrollcommand=treescrolly.set)
        treescrolly.grid(column=3, row=0, sticky=(NS))

        return listtree

    def create_itemsTree(self, listframe):
        listtree = ttk.Treeview(
            listframe,
            column=("order_id", "menu_item", "quantity"),
            show="headings",
            selectmode="browse",
        )
        listtree.heading("order_id", text="order_id")
        listtree.heading("menu_item", text="menu_item")
        listtree.heading("quantity", text="quantity")
        listtree.column("order_id", width=70)
        listtree.column("menu_item", width=70)
        listtree.column("quantity", width=70)
        listtree.tag_configure("font", font=("Arial", 10))
        listtree.grid(column=0, row=0, sticky=(N, W, E, S))

        treescrolly = ttk.Scrollbar(
            listframe, orient=VERTICAL, command=listtree.yview
        )
        listtree.configure(yscrollcommand=treescrolly.set)
        treescrolly.grid(column=3, row=0, sticky=(NS))

        return listtree


class UpdateMsg:
    def __init__(self, message):
        self.root_update_msg = Tk()
        self.root_update_msg.title("Success.")
        self.root_update_msg.geometry("400x100")
        self.window_title_label = ttk.Label(
            self.root_update_msg, text=message, font=("Arial", 15)
        )
        self.window_title_label.pack(side=TOP, pady=10)
        self.ok_button = ttk.Button(
            self.root_update_msg,
            text="OK",
            default="active",
            command=self.destroy,
        )
        self.ok_button.pack(side=BOTTOM, pady=10)
        self.root_update_msg.mainloop()

    def destroy(self):
        self.root_update_msg.destroy()


class addOrderForm:
    def __init__(self):
        fields = "customer", "location"
        self.root = Tk()
        self.root.title("Nympton Add_order")
        self.entries = self.initUI(self.root, fields)
        self.root.bind(
            "<Return>", (lambda event, e=self.entries: self.fetch(e))
        )
        self.frame = Frame(self.root, relief=RAISED, borderwidth=1)
        self.frame.pack(fill=BOTH, expand=True)

        self.closeButton = Button(
            self.root, text="Cancel", command=self.cancel
        )
        self.closeButton.pack(side=RIGHT, padx=5, pady=5)
        self.okButton = Button(
            self.root,
            text="OK",
            command=(lambda e=self.entries: self.fetch(e)),
        )
        self.okButton.pack(side=RIGHT)
        self.root.mainloop()

    def fetch(self, entries):
        inputs = []
        for entry in entries:
            field = entry[0]
            text = entry[1].get()
            inputs.append(text)
        self.add_order(inputs)
        self.cancel()

    def add_order(self, inputs):
        customer = inputs[0]
        location = inputs[1]
        print(
            "making new order with customer: "
            + customer
            + " and location: "
            + location
            + " ."
        )
        backend = Backend()
        new_order = backend.new_order(customer, location)
        new_order.set_order_date()
        new_order.save()

    def initUI(self, root, fields):
        entries = []
        for field in fields:
            frame = Frame(root)
            frame.pack(fill=X)

            lbl = Label(frame, text=field, width=20, anchor="w")
            lbl.pack(side=LEFT, padx=5, pady=5)

            entry = Entry(frame)
            entry.pack(fill=X, padx=5, expand=True)

            entries.append((field, entry))
        return entries

    def message(self, message, command):
        self.root_error_msg = Tk()
        self.root_error_msg.title(message)
        self.root_error_msg.geometry("400x100")
        self.window_title_label = Label(
            self.root_error_msg, text=message, font=("Arial", 15)
        )
        self.window_title_label.pack(side=TOP, pady=10)
        self.ok_button = Button(
            self.root_error_msg, text="OK", default="active", command=command
        )
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


class addItemForm:
    def __init__(self, order_id):
        fields = "menu_item", "quantity"
        self.root = Tk()
        self.root.title("Add_item")
        self.entries = self.initUI(self.root, fields)
        self.root.bind(
            "<Return>", (lambda event, e=self.entries: self.fetch(e))
        )
        self.frame = Frame(self.root, relief=RAISED, borderwidth=1)
        self.frame.pack(fill=BOTH, expand=True)
        self.order_id = order_id
        self.closeButton = Button(
            self.root, text="Cancel", command=self.cancel
        )
        self.closeButton.pack(side=RIGHT, padx=5, pady=5)
        self.okButton = Button(
            self.root,
            text="OK",
            command=(lambda e=self.entries: self.fetch(e)),
        )
        self.okButton.pack(side=RIGHT)
        self.root.mainloop()

    def fetch(self, entries):
        inputs = []
        for entry in entries:
            field = entry[0]
            text = entry[1].get()
            inputs.append(text)
        self.add_item(inputs)
        self.cancel()

    def add_item(self, inputs):
        item = inputs[0]
        quantity = inputs[1]
        print(
            "making new order with item: "
            + item
            + " and quantity: "
            + quantity
            + " ."
        )
        backend = Backend()
        existing_order = backend.existing_order(self.order_id)
        existing_order.add_items(item, quantity)

    def initUI(self, root, fields):
        entries = []
        for field in fields:
            frame = Frame(root)
            frame.pack(fill=X)

            lbl = Label(frame, text=field, width=20, anchor="w")
            lbl.pack(side=LEFT, padx=5, pady=5)

            entry = Entry(frame)
            entry.pack(fill=X, padx=5, expand=True)

            entries.append((field, entry))
        return entries

    def message(self, message, command):
        self.root_error_msg = Tk()
        self.root_error_msg.title(message)
        self.root_error_msg.geometry("400x100")
        self.window_title_label = Label(
            self.root_error_msg, text=message, font=("Arial", 15)
        )
        self.window_title_label.pack(side=TOP, pady=10)
        self.ok_button = Button(
            self.root_error_msg, text="OK", default="active", command=command
        )
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


if __name__ == "__main__":
    orderListForm()
