from tkinter import *
from tkinter import ttk
import sys
from frontend.order_page import orderListForm

class menuPage:
    def __init__(self):
        self.root_menu = Tk()
        self.root_menu.title("menu Page")
        self.root_menu.geometry("600x400")
        self.frame = self.make_equal_weighted_frame(300, 200, 4, 2, self.root_menu)
        self.window_title_label = ttk.Label(self.frame, text='menu Page', font=("Arial", 25))
        self.window_title_label.grid(column=0, row=0)
        self.ok_button = ttk.Button(self.frame, text="Make an Order", default="active", command=self.order_page)
        self.ok_button.grid(column=0, row=3, pady=50)
        self.cancel_button = ttk.Button(self.frame, text="Exit", default="active", command=sys.exit)
        self.cancel_button.grid(column=1, row=3)
        self.root_menu.mainloop()


    def make_equal_weighted_frame(self, width, height, rows, columns, root_frame):
        frame = ttk.Frame(root_frame, width=width, height=height)
        frame.grid(column=1, row=1, sticky=(N, E, S))
        for i in range(columns):
            frame.columnconfigure(i, weight=1)
        for i in range(rows):
            frame.rowconfigure(i, weight=1)
    
    def order_page(self):
        self.root_menu.destroy()
        orderListForm()


from tkinter import *
from tkinter import ttk
from backend.main import Backend


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
                order_details = self.get_existing_item(selected_item)

                item_value.set(order_details[0])
                price_value.set(order_details[1])

            update_buttons()

        def update_order():
            dts_item = item_value.get()
            dts_price = price_value.get()

            self.update_item_backend(dts_item, dts_price)
            root.destroy()
            UpdateMsg()

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
        return self.backend.get_existing_order(item)

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
        orderListForm()

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
        item = inputs[0]
        price = inputs[1]
        print("making new order with item: " + item + " and price: " + price + " .")
        new_order = self.backend.new_order(item, price)
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


if __name__ == "__main__":
    menuPage()