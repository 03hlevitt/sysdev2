"""common utils code used in the front end"""
from tkinter import (
    N,
    E,
    S,
    W,
    Tk,
    TOP,
    BOTTOM,
    Button,
    Label,
    Entry,
    Frame,
    LEFT,
    RIGHT,
    BOTH,
    X,
    VERTICAL,
    NS,
    RAISED,
)
from tkinter import ttk
from backend.main import Backend


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
            from frontend.order_page import (
                OrderListForm,
            )  # here to prevent circular imports

            # but also to avoid repeated code

            OrderListForm()
        if self.page == "menu":
            from frontend.menu_page import (
                MenuPage,
            )  # here to prevent circular imports

            # but also to avoid repeated code

            MenuPage()

    def destroy_both(self):
        """destroy error message and input window"""
        self.root_error_msg.destroy()
        self.root.destroy()
        self.return_back()

    def cancel(self):
        """cancel action to go back to main page, on cancel button"""
        self.root.destroy()
        self.return_back()


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


class BasePage:
    """common code for displaying pages with a command area and listrees"""

    def __init__(self, title: str, geometry: str, title_text: str):
        """constructor for main page superclass

        Args:
            title (_type_): title of window
            geometry (_type_): size of window
            title_text (_type_): title text that is displayed
        """
        self.backend = Backend()

        self.root = Tk()
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.rowconfigure(0, weight=1)

        self.baseframe = ttk.Frame(self.root)
        self.baseframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.baseframe.rowconfigure(0, weight=1)
        self.baseframe.rowconfigure(1, weight=4)
        self.baseframe.columnconfigure(0, weight=3)
        self.baseframe.columnconfigure(1, weight=1)

        window_title_label = ttk.Label(
            self.baseframe, text=title_text, font=("Arial", 25)
        )
        window_title_label.grid(column=0, row=0)
        window_title_label.place(relx=0.0, rely=0.0)

        self.root.mainloop()

    def populate_listree(self, listtree: ttk.Treeview, page: str):
        """populate a tree view with data

        Args:
            listtree (ttk.Treeview): tk tree view to populate
            page (str): what type of page its in,
              to tell the function what type of data to populate with.
        """
        listtree.delete(*listtree.get_children())
        if page == "menu":
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


def create_details_frame(baseframe: Frame()) -> Frame():
    """create main command panel in the middle of the page

    Args:
        baseframe (Frame): base frame of the window to place in

    Returns:
        Frame: frame to use for cmd buttons etc.
    """
    details_frame = ttk.Frame(
        baseframe,
        borderwidth=10,
        relief="ridge",
        width=100,
        height=100,
    )
    details_frame.grid(column=1, row=1, sticky=(N, E, S))

    details_frame.columnconfigure(0, weight=1)
    details_frame.columnconfigure(1, weight=1)
    details_frame.rowconfigure(0, weight=1)
    details_frame.rowconfigure(1, weight=1)
    details_frame.rowconfigure(2, weight=1)
    details_frame.rowconfigure(3, weight=1)
    details_frame.rowconfigure(4, weight=1)
    return details_frame


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
