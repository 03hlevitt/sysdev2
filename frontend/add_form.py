"""customer facing add form"""
from tkinter import Tk, Frame, Button, Label, Entry, RAISED, BOTH, RIGHT, LEFT, X, VERTICAL, NS, N, E, S, W, TOP, BOTTOM
from backend.main import Backend
from frontend.handle_exceptions import handle_db_exceptions, handle_3words_exceptions
from frontend.pop_up import UpdateMsg


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
        from frontend.base_page import orderListForm
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
