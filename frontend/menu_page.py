from tkinter import *
from tkinter import ttk
from backend.main import Backend
from frontend.order_page import orderListForm


class MenuPage:

    def __init__(self):
        self.backend = Backend()
        

        def create_detail_view(self):
            detailsframe = ttk.Frame(baseframe, borderwidth=10, relief="ridge", width=100, height=100)
            detailsframe.grid(column=1, row=1, sticky=(N, E, S))

            detailsframe.columnconfigure(0, weight=1)
            detailsframe.columnconfigure(1, weight=1)
            detailsframe.rowconfigure(0, weight=1)
            detailsframe.rowconfigure(1, weight=1)
            detailsframe.rowconfigure(2, weight=1)
            detailsframe.rowconfigure(3, weight=1)
            detailsframe.rowconfigure(4, weight=1)

            details_lname_label = ttk.Label(detailsframe, text='item')
            details_lname_label.grid(column=0, row=1)
            details_lname = ttk.Entry(detailsframe, textvariable=item_value)
            details_lname.grid(column=1, row=1)

            details_street_label = ttk.Label(detailsframe, text='price')
            details_street_label.grid(column=0, row=2)
            details_street = ttk.Entry(detailsframe, textvariable=price_value)
            details_street.grid(column=1, row=2)

            cmdframe = ttk.Frame(detailsframe, borderwidth=0, width=100, height=50)

            # command frame
            cmdframe.grid(column=0, row=4, sticky=(N, E, S))
            self.cmdOk = ttk.Button(cmdframe, text="OK", state="disabled", command=update_order)
            self.cmdOk.grid(column=0, row=0)

            self.cmdOrders = ttk.Button(cmdframe, text="Orders", state="enabled", command=got_to_orders)
            self.cmdOrders.grid(column=1, row=0)

            self.cmdAddorder = ttk.Button(cmdframe, text="add item", state="active", command=make_order)
            self.cmdAddorder.grid(column=2, row=0)

            self.cmd_delete_order = ttk.Button(cmdframe, text="delete item", state="active", command=delete_item)
            self.cmd_delete_order.grid(column=3, row=0)

            listframe = ttk.Frame(baseframe, borderwidth=10, relief="ridge", width=100, height=100)
            listframe.grid(column=0, row=1, sticky=(N, W, E, S))
            listframe.rowconfigure(0, weight=1)

            return listframe

        def update_buttons():
            self.cmdOk.config(state=ACTIVE)
            self.cmdOrders.config(state=ACTIVE)

        def got_to_orders():
            root.destroy()
            orderListForm()

        def make_order():
            root.destroy()
            addOrderForm()

        def listtreeitem_selected(event):
            for selected_item in listtree.selection():
                item = self.get_existing_item(selected_item)

                item_value.set(selected_item)
                price_value.set(item.price)

            update_buttons()

        def update_order():
            dts_item = item_value.get()
            dts_price = price_value.get()

            self.update_item_backend(dts_item, dts_price)
            self.populate_listree(listtree)
            UpdateMsg('Update Successful!')

        def delete_item():
            dts_item = item_value.get()

            self.delete_item_backend(dts_item)
            self.populate_listree(listtree)
            UpdateMsg('Item Deleted!')

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

        window_title_label = ttk.Label(baseframe, text='Menu', font=("Arial", 25))
        window_title_label.grid(column=0, row=0)
        window_title_label.place(relx=0.0, rely=0.0)

        item_value = StringVar()
        price_value = StringVar()

        list_frame = create_detail_view(self)
        listtree = self.create_listTree(list_frame)

        listtree.bind('<<TreeviewSelect>>', listtreeitem_selected)

        self.populate_listree(listtree)

        root.mainloop()

    def get_orders(self):
        return self.backend.view_menu()

    def update_item_backend(self, item, price):
        item = self.backend.existing_item(item)
        item.update_price(price)
        item.save()

    def get_existing_item(self, item):
        return self.backend.existing_item(item)
    
    def delete_item_backend(self, item):
        item = self.backend.existing_item(item)
        item.delete_from_db()

    def populate_listree(self, listtree):
        listtree.delete(*listtree.get_children())
        orders = self.get_orders()

        added_orders = []
        for order in orders:
            orderValues = list(order)

            if orderValues not in added_orders:  # catching duplicates
                listtree.insert('', index='end', iid=orderValues[0], text=orderValues[0], values=(orderValues))
                added_orders.append(orderValues)

    def create_listTree(self, listframe):
        listtree = ttk.Treeview(listframe,
                                column=("item", "price"),
                                show='headings', selectmode='browse')
        listtree.heading('item', text='item')
        listtree.heading('price', text='price')
        listtree.column('item', width=70)
        listtree.column('price', width=70)
        listtree.tag_configure('font', font=('Arial', 10))
        listtree.grid(column=0, row=0, sticky=(N, W, E, S))

        treescrolly = ttk.Scrollbar(listframe, orient=VERTICAL, command=listtree.yview)
        listtree.configure(yscrollcommand=treescrolly.set)
        treescrolly.grid(column=3, row=0, sticky=(NS))

        return listtree


class UpdateMsg:
    def __init__(self, message):
        self.root_update_msg = Tk()
        self.root_update_msg.title("Success.")
        self.root_update_msg.geometry("400x100")
        self.window_title_label = ttk.Label(self.root_update_msg, text=message, font=("Arial", 15))
        self.window_title_label.pack(side=TOP, pady=10)
        self.ok_button = ttk.Button(self.root_update_msg, text="OK", default="active", command=self.destroy)
        self.ok_button.pack(side=BOTTOM, pady=10)
        self.root_update_msg.mainloop()

    def destroy(self):
        self.root_update_msg.destroy()


fields = 'item', 'price'


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
        self.okButton = Button(self.root, text="OK", command=(lambda e=self.entries: self.fetch(e)))
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
        item = inputs[0]
        price = inputs[1]
        print("making new order with item: " + item + " and price: " + price + " .")
        backend = Backend()
        new_order = backend.new_item(item, price)
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
        MenuPage()


if __name__ == "__main__":
    MenuPage()