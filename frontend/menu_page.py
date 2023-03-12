from tkinter import (
    StringVar,
    N,
    E,
    S,
    W,
    ACTIVE,
    VERTICAL,
    NS,
)
from tkinter import ttk
from backend.main import Backend
from frontend.order_page import orderListForm
from frontend.common import BaseAddForm, UpdateMsg, BasePage


class MenuPage(BasePage):
    def __init__(self):
        super().__init__("menu page", "1100x600", "menu page")
        self.backend = Backend()

        def create_detail_view(self, baseframe):
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

            details_lname_label = ttk.Label(detailsframe, text="Item")
            details_lname_label.grid(column=0, row=1)
            details_lname = ttk.Entry(detailsframe, textvariable=item_value)
            details_lname.grid(column=1, row=1)

            details_street_label = ttk.Label(detailsframe, text="Price")
            details_street_label.grid(column=0, row=2)
            details_street = ttk.Entry(detailsframe, textvariable=price_value)
            details_street.grid(column=1, row=2)

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
                cmdframe, text="Orders", state="enabled", command=got_to_orders
            )
            self.cmdOrders.grid(column=1, row=0)

            self.cmdAddorder = ttk.Button(
                cmdframe, text="add item", state="active", command=make_order
            )
            self.cmdAddorder.grid(column=2, row=0)

            self.cmd_delete_order = ttk.Button(
                cmdframe,
                text="delete item",
                state="active",
                command=delete_item,
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

            return listframe

        def update_buttons():
            self.cmdOk.config(state=ACTIVE)
            self.cmdOrders.config(state=ACTIVE)

        def got_to_orders():
            self.root.destroy()
            orderListForm()

        def make_order():
            self.root.destroy()
            fields = "item", "price"
            addOrderForm(fields)

        def clear_selected_from_input():
            item_value.set("")
            price_value.set("")
            update_buttons()

        def listtreeitem_selected(event):
            for selected_item in listtree.selection():
                item = self.get_existing_item(selected_item)

                item_value.set(selected_item)
                price_value.set(item.price)

            update_buttons()

        def update_order():
            # TODO: CHANGE THIS!
            dts_item = item_value.get()
            dts_price = price_value.get()

            self.update_item_backend(dts_item, dts_price)
            self.populate_listree(listtree)
            UpdateMsg("Update Successful!")

        def delete_item():
            dts_item = item_value.get()

            self.delete_item_backend(dts_item)
            clear_selected_from_input()
            self.populate_listree(listtree)
            UpdateMsg("Item Deleted!")

        item_value = StringVar()
        price_value = StringVar()

        list_frame = create_detail_view(self, self.baseframe)
        listtree = self.create_listTree(list_frame)

        listtree.bind("<<TreeviewSelect>>", listtreeitem_selected)

        self.populate_listree(listtree)

    def get_orders(self):
        return 

    def update_item_backend(self, item, price):
        item = self.backend.existing_item(item)
        item.update_price(price)
        item.save()

    def get_existing_item(self, item):
        return self.backend.existing_item(item)

    def delete_item_backend(self, item):
        item = self.backend.existing_item(item)
        item.delete_from_db()

    def create_listTree(self, listframe):
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
        listtree.tag_configure("font", font=("Arial", 10))
        listtree.grid(column=0, row=0, sticky=(N, W, E, S))

        treescrolly = ttk.Scrollbar(
            listframe, orient=VERTICAL, command=listtree.yview
        )
        listtree.configure(yscrollcommand=treescrolly.set)
        treescrolly.grid(column=3, row=0, sticky=(NS))

        return listtree


class addOrderForm(BaseAddForm):
    def __init__(self, fields):
        super().__init__(fields)
        self.root.title("Add Menu Item")

    def add_order(self, inputs):
        item = inputs[0]
        price = inputs[1]
        print(
            "making new order with item: "
            + item
            + " and price: "
            + price
            + " ."
        )
        backend = Backend()
        new_order = backend.new_item(item, price)
        new_order.save()

    def destroy(self):
        self.root_error_msg.destroy()

    def destroy_both(self):
        self.root_error_msg.destroy()
        self.root.destroy()
        orderListForm()

    def cancel(self):
        self.root.destroy()
        MenuPage()
