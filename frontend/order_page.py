"""order page ui"""
from tkinter import StringVar, ACTIVE
from tkinter import ttk
from common import (
    UpdateMsg,
    BaseAddForm,
    BasePage,
    create_details_frame,
    configure_listree,
    create_list_frame,
    create_cmdframe,
)


class OrderListForm(BasePage):
    """base order page"""

    def __init__(self):
        """constructure for the order page class"""
        super().__init__("Orders", "1600", "Orders")

        def create_detail_view(self, baseframe):
            """create three panels with control panel in the middle"""
            detailsframe = create_details_frame(baseframe)

            details_customer_label = ttk.Label(detailsframe, text="customer")
            details_customer_label.grid(column=0, row=1)
            details_customer = ttk.Entry(
                detailsframe, textvariable=customer_value
            )
            details_customer.grid(column=1, row=2)

            details_location_label = ttk.Label(detailsframe, text="location")
            details_location_label.grid(column=0, row=2)
            details_location = ttk.Entry(
                detailsframe, textvariable=location_value
            )
            details_location.grid(column=1, row=3)

            cmdframe = create_cmdframe(detailsframe)
            self.cmdOk = ttk.Button(
                cmdframe, text="OK", state="disabled", command=update_order
            )
            self.cmdOk.grid(column=0, row=0)

            self.cmdOrders = ttk.Button(
                cmdframe, text="Menu", state="enabled", command=go_to_menu
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

            listframe = create_list_frame(baseframe)

            itemframe = create_list_frame(baseframe, 2, 1)

            return listframe, itemframe

        def update_buttons():
            """set buttons to an active state"""
            self.cmdOk.config(state=ACTIVE)
            self.cmdOrders.config(state=ACTIVE)

        def go_to_menu():
            """go to the menu page"""
            self.root.destroy()
            from frontend.menu_page import MenuPage

            MenuPage()

        def make_order():
            """generate the add order page"""
            self.root.destroy()
            fields = "customer", "location"
            BaseAddForm("order", fields, "Add_order")

        def clear_selected_from_input():
            """clear text from input boxes"""
            customer_value.set("")
            location_value.set("")
            update_buttons()

        def itemtreeitem_selected(event: object):
            """populate input boxes with values selected in item list tree

            Args:
                event (object): event when clicking on item list tree
            """
            for selected_item in self.itemstree.selection():
                item_value.set(selected_item)
                update_buttons()

        def listtreeitem_selected(event):
            """populate input boxes with values selected in order list tree

            Args:
                event (object): event when clicking on order list tree
            """
            for selected_order in listtree.selection():
                order = self.backend.existing_order(selected_order)
                id_value.set(order.order_id)
                customer_value.set(order.customer)
                location_value.set(order.location_co_ords)
                self.populate_items_tree(order.order_id)
            update_buttons()

        def update_order():
            """update the values attributed to an order by order id"""
            dts_customer = customer_value.get()
            dts_location = location_value.get()
            dts_id = id_value.get()

            self.update_item_backend(dts_id, dts_customer, dts_location)
            self.populate_listree(listtree, "order")
            UpdateMsg("Update Successful!")

        def add_item():
            """add an item to an order"""
            dts_id = id_value.get()
            self.root.destroy()
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
            UpdateMsg("Item Deleted!")

        item_value = StringVar()
        customer_value = StringVar()
        location_value = StringVar()
        id_value = StringVar()

        list_frame, item_frame = create_detail_view(self, self.baseframe)
        listtree = self.create_list_tree(list_frame)
        self.itemstree = self.create_items_tree(item_frame)

        listtree.bind("<<TreeviewSelect>>", listtreeitem_selected)
        self.itemstree.bind("<<TreeviewSelect>>", itemtreeitem_selected)

        self.populate_listree(listtree)

    def update_item_backend(self, order_id: int, customer: str, location: str):
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
        item.save()

    def delete_order_backend(self, id_value: str):
        """delete an order from the order DB

        Args:
            id_value (str): selected order id from listtree
        """
        item = self.backend.existing_order(id_value)
        item.delete()

    def populate_items_tree(self, order_id: str):
        """get items from order and populate tree

        Args:
            order_id (string): order id to populate
        """
        self.itemstree.delete(*self.itemstree.get_children())
        items = self.backend.existing_order(order_id)

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

    def create_list_tree(self, listframe: object) -> ttk.Treeview:
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
        listtree = configure_listree(listtree, listframe)
        return listtree
