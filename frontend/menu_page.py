from tkinter import *
from tkinter import ttk
import sys
from frontend.order_page import OrderPage

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
        OrderPage()


if __name__ == "__main__":
    menuPage()