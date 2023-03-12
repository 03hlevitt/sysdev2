"""common utils code used in the front end"""
from tkinter import (
    StringVar,
    N,
    E,
    S,
    W,
    ACTIVE,
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
    def __init__(self, fields, title):
        self.root = Tk()
        self.root.title(title)
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
            text = entry[1].get()
            inputs.append(text)
        self.add_order(inputs)
        self.cancel()

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


class BasePage:
    def __init__(self, title, geometry, title_text):
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

    def populate_listree(self, listtree, page):
        listtree.delete(*listtree.get_children())
        if page == "menu":
            orders = self.backend.view_menu()
        else:
            orders = self.backend.view_orders()

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


def create_details_frame(baseframe):
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


def create_list_frame(baseframe, column=0, row=1):
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


def create_cmdframe(detailsframe):
    cmdframe = ttk.Frame(detailsframe, borderwidth=0, width=100, height=50)

    # command frame
    cmdframe.grid(column=0, row=4, sticky=(N, E, S))
    return cmdframe


def configure_listree(listtree, listframe):
    listtree.tag_configure("font", font=("Arial", 10))
    listtree.grid(column=0, row=0, sticky=(N, W, E, S))

    treescrolly = ttk.Scrollbar(
        listframe, orient=VERTICAL, command=listtree.yview
    )
    listtree.configure(yscrollcommand=treescrolly.set)
    treescrolly.grid(column=3, row=0, sticky=(NS))
    return listtree
