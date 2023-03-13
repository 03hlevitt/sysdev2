"""order page ui"""
from tkinter import *
from tkinter import ttk
from backend.main import Backend
from custom.exceptions import NoKeyError, WhatThreeWordsError
from functools import wraps

def handle_3words_exceptions(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            UpdateMsg("Please enter valid co ordinates!")
            print(error)
        except NoKeyError as error:
            UpdateMsg("Please Ensure there is a valid api key!")
            print(error)
        except WhatThreeWordsError as error:
            UpdateMsg("Something went wrong with the what three words api!")
            print(error)
        except Exception as error:
            UpdateMsg("Something went wrong!")
            print(error)
    return decorated

def handle_db_exceptions(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotImplementedError as error:
            print(error)
            UpdateMsg("Item does not exist! - check the Menu!")
        except Exception as error:
            UpdateMsg("Something went wrong!")
            print(error)
    return decorated

def create_list_frame(baseframe: Frame, column=0, row=1) -> Frame:
    """create a frame for tree views

    Args:
        baseframe (Frame): base window frame ot put into
        column (int, optional): column to place this into in the baseframe.
          Defaults to 0.
        row (int, optional): row to place this into in the baseframe.
          Defaults to 1.

    Returns:
        Frame: frame for tree views
    """
    listframe = ttk.Frame(
        baseframe,
        borderwidth=10,
        relief="ridge",
        width=100,
        height=100,
    )
    listframe.grid(column=column, row=row, sticky=(N, W, E, S))
    listframe.rowconfigure(0, weight=1)
    return listframe


def create_cmdframe(detailsframe: Frame) -> Frame:
    """command frame to put buttons into

    Args:
        detailsframe (Frame): control panel to place into

    Returns:
        Frame: a command frame
    """
    cmdframe = ttk.Frame(detailsframe, borderwidth=0, width=100, height=50)

    # command frame
    cmdframe.grid(column=0, row=4, sticky=(N, E, S))
    return cmdframe


def configure_listree(
    listtree: ttk.Treeview, listframe: Frame
) -> ttk.Treeview:
    """configure a tree view for the main pages

    Args:
        listtree (ttk.Treeview): tree view to configure
        listframe (Frame): frame which tree veiw is placed

    Returns:
        ttk.Treeview: configured tree view
    """
    listtree.tag_configure("font", font=("Arial", 10))
    listtree.grid(column=0, row=0, sticky=(N, W, E, S))

    treescrolly = ttk.Scrollbar(
        listframe, orient=VERTICAL, command=listtree.yview
    )
    listtree.configure(yscrollcommand=treescrolly.set)
    treescrolly.grid(column=3, row=0, sticky=(NS))
    return listtree



class orderListForm:
    """base order page"""

    def __init__(self, page_type):
        """constructure for the order page class"""
        self.backend = Backend()
        self.page_type = page_type

        def create_detail_view(self):
            """create three panels with control panel in the middle"""
            if page_type == "order":
                cmdframe_config = {
                    "Update":update_order,
                    "Back":go_to_menu,
                    "Create":make_order,
                    "Delete":delete_order,
                }
                input1 = "Customer"
                input2 = "Location"
            else:
                cmdframe_config = {
                    "Update":update_menu_item,
                    "Back":go_to_orders,
                    "Create":add_menu_item,
                    "Delete":delete_menu_item,
                }
                input1 = "Item"
                input2 = "Price"
            detailsframe = ttk.Frame(
                baseframe, borderwidth=10, relief="ridge", width=100, height=100)
            detailsframe.grid(column=1, row=1, sticky=(N, E, S))

            detailsframe.columnconfigure(0, weight=1)
            detailsframe.columnconfigure(1, weight=1)
            detailsframe.rowconfigure(0, weight=1)
            detailsframe.rowconfigure(1, weight=1)
            detailsframe.rowconfigure(2, weight=1)
            detailsframe.rowconfigure(3, weight=1)
            detailsframe.rowconfigure(4, weight=1)

            details_lname_label = ttk.Label(detailsframe, text=input1)
            details_lname_label.grid(column=0, row=1)
            details_lname = ttk.Entry(
                detailsframe, textvariable=input1_variable)
            details_lname.grid(column=1, row=1)

            details_street_label = ttk.Label(detailsframe, text=input2)
            details_street_label.grid(column=0, row=2)
            details_street = ttk.Entry(
                detailsframe, textvariable=input2_variable)
            details_street.grid(column=1, row=2)
            cmdframe = create_cmdframe(detailsframe)
            self.cmd_update = ttk.Button(
                cmdframe, text="Update", state="disabled", command=cmdframe_config["Update"]
            )
            self.cmd_update.grid(column=0, row=0)

            self.cmd_back = ttk.Button(
                cmdframe, text="Return", state="active", command=cmdframe_config["Back"]
            )
            self.cmd_back.grid(column=1, row=0)

            self.cmd_add = ttk.Button(
                cmdframe, text="Create", state="active", command=cmdframe_config["Create"]
            )
            self.cmd_add.grid(column=2, row=0)

            self.cmd_delete = ttk.Button(
                cmdframe, text="Delete", state="disabled", command=cmdframe_config["Delete"]
            )
            self.cmd_delete.grid(column=3, row=0)

            if page_type == "order":
                self.cmd_remove_item = ttk.Button(
                    cmdframe,
                    text="remove items from an order",
                    state="disabled",
                    command=remove_item,
                )
                self.cmd_remove_item.grid(column=5, row=0)

                self.cmd_add_item = ttk.Button(
                    cmdframe,
                    text="add items to an order",
                    state="disabled",
                    command=add_item,
                )
                self.cmd_add_item.grid(column=4, row=0)

            listframe = create_list_frame(baseframe)

            if page_type == "order":
                itemframe = create_list_frame(baseframe, 2, 1)
            else:
                itemframe = None

            return listframe, itemframe

        def update_buttons_list_tree(page):
            """sets buttons to desired state when an order/menu item is selected"""
            self.cmd_update.config(state="active")
            self.cmd_delete.config(state="active")
            if page == "order":
                self.cmd_add_item.config(state="active")

        def update_buttons_items_tree():
            """sets buttons to desired state when an order item is selected"""
            self.cmd_remove_item.config(state="active")

        def update_buttons_to_default():
            """sets buttons to default state"""
            self.cmd_update.config(state="disabled")
            self.cmd_delete.config(state="disabled")
            self.cmd_remove_item.config(state="disabled")
            self.cmd_add_item.config(state="disabled")

        def go_to_menu():
            """go to the menu page"""
            root.destroy()
            orderListForm("menu")

        def go_to_orders():
            """go to the order page"""
            root.destroy()
            orderListForm("order")

        def make_order():
            """generate the add order page"""
            root.destroy()
            fields = "customer", "location"
            BaseAddForm("order", fields, "Make an Order")

        def add_menu_item():
            """generate the add item page"""
            root.destroy()
            fields = "item", "price"
            BaseAddForm("menu", fields, "order")

        def clear_selected_from_input():
            """clear text from input boxes and reset buttons"""
            input1_variable.set('')
            input2_variable.set('')
            update_buttons_to_default()

        def items_tree_selected(event: object):
            """populate input boxes with values selected in item list tree
            Args:
                event (object): event when clicking on item list tree
            """
            for selected_item in self.itemstree.selection():
                item_value.set(selected_item)
                update_buttons_items_tree()

        def order_tree_selected(event: object):
            """populate input boxes with values selected in order list tree
            Args:
                event (object): event when clicking on order list tree
            """
            for selected_order in listtree.selection():
                order = self.backend.existing_order(selected_order)
                id_value.set(order.order_id)
                input1_variable.set(order.customer)
                input2_variable.set(order.location_co_ords)
                self.populate_items_tree(order.order_id)

            update_buttons_list_tree("order")

        def menu_tree_selected(event: object):
            """set values for later inputs when selecting the listree

            Args:
                event (object): user selecting the listree
            """
            for selected_item in listtree.selection():
                item = self.backend.existing_item(selected_item)

                input1_variable.set(selected_item)
                input2_variable.set(item.price)

            update_buttons_list_tree("menu")

        @handle_3words_exceptions
        def update_order():
            """update the values attributed to an order by order id"""
            dts_customer = input1_variable.get()
            dts_location = input2_variable.get()
            dts_id = id_value.get()
            self.update_order_backend(dts_id, dts_customer, dts_location)
            self.populate_listree(listtree)
            UpdateMsg("Update Successful!")

        def add_item():
            """add an item to an order"""
            dts_id = id_value.get()
            root.destroy()
            fields = "menu_item", "quantity"
            BaseAddForm("item", fields, "Add_item", dts_id)

        def remove_item():
            """remove an item and all of its quantity from an order"""
            dts_id = id_value.get()
            dts_item = item_value.get()
            order = self.backend.existing_order(dts_id)
            order.remove_items(dts_item)
            self.populate_items_tree(dts_id)
            UpdateMsg("Item Deleted!")

        def delete_order():
            """delete and order entirely"""
            dts_id = id_value.get()
            self.delete_order_backend(dts_id)
            clear_selected_from_input()
            self.populate_listree(listtree)
            UpdateMsg("Order Deleted!")

        def delete_menu_item():
            """delete a menu item from the backend"""
            dts_item = input1_variable.get()

            self.delete_menu_item_backend(dts_item)
            clear_selected_from_input()
            self.populate_listree(listtree)
            UpdateMsg("Item Deleted!")

        def update_menu_item():
            """update the price of an item in the backend"""
            dts_item = input1_variable.get()
            dts_price = input2_variable.get()

            self.update_menu_item_backend(dts_item, dts_price)
            self.populate_listree(listtree)
            UpdateMsg("Update Successful!")


        root = Tk()
        if self.page_type == "order":
            root.title("Order Page")
            root.geometry("1400x600")
            item_value = StringVar()
        else:
            root.title("Menu Page")
            root.geometry("900x600")
        root.rowconfigure(0, weight=1)

        baseframe = ttk.Frame(root)
        baseframe.grid(column=0, row=0, sticky=(N, W, E, S))
        baseframe.rowconfigure(0, weight=1)
        baseframe.rowconfigure(1, weight=4)
        baseframe.columnconfigure(0, weight=3)
        baseframe.columnconfigure(1, weight=1)
        baseframe.columnconfigure(2, weight=1)

        window_title_label = ttk.Label(
            baseframe, text=self.page_type, font=("Arial", 25))
        window_title_label.grid(column=0, row=0)
        window_title_label.place(relx=0.0, rely=0.0)

        input1_variable = StringVar()
        input2_variable = StringVar()
        id_value = StringVar()
            

        list_frame, item_frame = create_detail_view(self)

        if self.page_type == "order":
            self.itemstree = self.create_items_tree(item_frame)
            self.itemstree.bind('<<TreeviewSelect>>', items_tree_selected)

            listtree = self.create_order_tree(list_frame)
            listtree.bind('<<TreeviewSelect>>', order_tree_selected)
        else:
            listtree = self.create_menu_tree(list_frame)
            listtree.bind('<<TreeviewSelect>>', menu_tree_selected)

        self.populate_listree(listtree)

        root.mainloop()
    
    def update_menu_item_backend(self, item, price):
        """update the price of an item in the backend"""
        item = self.backend.existing_item(item)
        item.update_price(price)
        item.save()

    def update_order_backend(self, order_id: int, customer: str, location: str):
        """backend methods to update an item in the db
        Args:
            id (int): order if
            customer (str): name of customer (unique)
            location (str): location placed with order (unique)
        """
        item = self.backend.existing_order(order_id)
        item.customer = customer
        item.location_co_ords = location
        item.set_order_date()
        item.update_order()

    def delete_order_backend(self, id_value: str):
        """delete an order from the order DB
        Args:
            id_value (str): selected order id from listtree
        """
        item = self.backend.existing_order(id_value)
        item.delete()

    def delete_menu_item_backend(self, item):
        """deete an item from the db"""
        item = self.backend.existing_item(item)
        item.delete_from_db()

    def populate_items_tree(self, order_id: str):
        """get items from order and populate tree
        Args:
            order_id (string): order id to populate
        """
        self.itemstree.delete(*self.itemstree.get_children())
        order = self.backend.existing_order(order_id)
        items = order.view_order_items()

        added_items = []
        for item in items:
            item_values = list(item)
            if item_values not in added_items:
                added_items.append(item_values)
                self.itemstree.insert(
                    "",
                    index="end",
                    iid=item_values[0],
                    text=item_values[0],
                    values=(item_values),
                )

    def populate_listree(self, listtree: ttk.Treeview):
        """populate a tree view with data
        Args:
            listtree (ttk.Treeview): tk tree view to populate
            page (str): what type of page its in,
              to tell the function what type of data to populate with.
        """
        listtree.delete(*listtree.get_children())
        if self.page_type == "menu":
            orders = self.backend.view_menu()
        else:
            orders = self.backend.view_orders()

        added_orders = []
        for order in orders:
            values = list(order)

            if values not in added_orders:  # catching duplicates
                listtree.insert(
                    "",
                    index="end",
                    iid=values[0],
                    text=values[0],
                    values=(values),
                )
                added_orders.append(values)

    def create_menu_tree(self, listframe: object) -> ttk.Treeview:
        """create tkinter treeview of menu

        Args:
            listframe (object): tk inter frame to put list tree in

        Returns:
            ttk.Treeview: list tree
        """
        listtree = ttk.Treeview(
            listframe,
            column=("item", "price"),
            show="headings",
            selectmode="browse",
        )
        listtree.heading("item", text="item")
        listtree.heading("price", text="price")
        listtree.column("item", width=70)
        listtree.column("price", width=70)
        listtree = configure_listree(listtree, listframe)
        return listtree

    def create_order_tree(self, listframe: object) -> ttk.Treeview:
        """create list tree for orders
        Args:
            listframe (object): frame to put list tree into
        Returns:
            ttk.Treeview: list tree full of orders
        """
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
        listtree = configure_listree(listtree, listframe)
        return listtree

    def create_items_tree(self, listframe: object) -> ttk.Treeview:
        """create list tree full of items
        Args:
            listframe (object): frame to put list tree into
        Returns:
            ttk.Treeview: tree view full of items
        """
        listtree = ttk.Treeview(
            listframe,
            column=("menu_item", "quantity"),
            show="headings",
            selectmode="browse",
        )
        listtree.heading("menu_item", text="menu_item")
        listtree.heading("quantity", text="quantity")
        listtree.column("menu_item", width=70)
        listtree.column("quantity", width=70)
        listtree = configure_listree(listtree, listframe)
        return listtree

class UpdateMsg:
    """display message when something is succesfully updated or otherwise"""

    def __init__(self, message: str):
        """constructor for class for displaying update messages

        Args:
            message (str): message to be displayed
        """
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
        """destroy window"""
        self.root_update_msg.destroy()


class BaseAddForm:
    """base form for adding things to the db"""

    def __init__(self, page, fields, title, order_id=None):
        self.order_id = order_id
        self.page = page
        self.root = Tk()
        self.root.title(title)
        self.entries = self.init_ui(self.root, fields)
        self.root.bind(
            "<Return>", (lambda event, e=self.entries: self.fetch(e))
        )
        self.frame = Frame(self.root, relief=RAISED, borderwidth=1)
        self.frame.pack(fill=BOTH, expand=True)

        self.close_button = Button(
            self.root, text="Cancel", command=self.cancel
        )
        self.close_button.pack(side=RIGHT, padx=5, pady=5)
        self.ok_button = Button(
            self.root,
            text="OK",
            command=(lambda e=self.entries: self.fetch(e)),
        )
        self.ok_button.pack(side=RIGHT)
        self.root.mainloop()

    def fetch(self, entries: tuple):
        """get input text to list to input to backend

        Args:
            entries (tuple): tkinter input fields, .get() transforms to strings
        """
        inputs = []
        for entry in entries:
            text = entry[1].get()
            inputs.append(text)
        self.add(inputs)
        self.cancel()

    @handle_3words_exceptions
    @handle_db_exceptions
    def add(self, inputs: list):
        """add the item to backend

        Args:
            inputs (list): inputs from the form
        """
        input_1 = inputs[0]
        input_2 = inputs[1]
        backend = Backend()
        if self.page == "menu":
            new_order = backend.new_item(input_1, input_2)
            new_order.save()
        if self.page == "order":
            new_order = backend.new_order(input_1, input_2)
            new_order.set_order_date()
            new_order.save()
        if self.page == "item":
            existing_order = backend.existing_order(self.order_id)
            existing_order.add_items(input_1, input_2)

    def init_ui(self, root: Frame, fields: tuple) -> tuple:
        """initialise what is shown in the window namely labels and input boxes

        Args:
            root (Frame): root frame
            fields (tuple): fields to be labled

        Returns:
            tuple: _description_
        """
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

    def message(self, message: str, command: object):
        """displays message to user

        Args:
            message (str): message to be displayed ot the user
            command (object): command after pressing the ok button
        """
        self.root_error_msg = Tk()  # defined outside init
        # as we only want to show when somethign goes wrong!
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
        """destroy root error message"""
        self.root_error_msg.destroy()

    def return_back(self):
        """go back to main page"""
        if self.page in ("order", "item"):
            orderListForm("order")
        if self.page == "menu":
            orderListForm("menu")

    def destroy_both(self):
        """destroy error message and input window"""
        self.root_error_msg.destroy()
        self.root.destroy()
        self.return_back()

    def cancel(self):
        """cancel action to go back to main page, on cancel button"""
        self.root.destroy()
        self.return_back()


if __name__ == "__main__":
    orderListForm("order")
