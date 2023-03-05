from tkinter import *
from tkinter import ttk
import sys

class HomePage:
    def __init__(self):
        self.root_home = Tk()
        self.root_home.title("home Page")
        self.root_home.geometry("600x400")
        self.frame = self.make_equal_weighted_frame(300, 200, 4, 2, self.root_home)
        self.window_title_label = ttk.Label(self.frame, text='Home Page', font=("Arial", 25))
        self.window_title_label.grid(column=0, row=0)
        self.user_name = self.make_basic_input_box(0, 1, "user name", self.frame)
        self.password = self.make_password_input_box(0, 2, "password", self.frame)
        self.ok_button = ttk.Button(self.frame, text="OK", default="active", command=self.home_attempt)
        self.ok_button.grid(column=0, row=3, pady=50)
        self.cancel_button = ttk.Button(self.frame, text="Cancel", default="active", command=sys.exit)
        self.cancel_button.grid(column=1, row=3)
        self.root_home.mainloop()


    def make_equal_weighted_frame(self, width, height, rows, columns, root_frame):
        frame = ttk.Frame(root_frame, width=width, height=height)
        frame.grid(column=1, row=1, sticky=(N, E, S))
        for i in range(columns):
            frame.columnconfigure(i, weight=1)
        for i in range(rows):
            frame.rowconfigure(i, weight=1)

    def make_basic_input_box(self, column, row, title, frame):
        label = ttk.Label(frame, text=title)
        label.grid(column=column, row=row)
        input_value = StringVar()
        user_input_box = ttk.Entry(frame, textvariable=input_value)
        user_input_box.grid(column=column + 1, row=row)
        return input_value

    def make_password_input_box(self, column, row, title, frame):
        label = ttk.Label(frame, text=title)
        label.grid(column=column, row=row)
        input_value = StringVar()
        user_input_box = ttk.Entry(frame, show="*", textvariable=input_value)
        user_input_box.grid(column=column + 1, row=row)
        return input_value
    
    def home_attempt(self):
        username = self.user_name.get()
        password = self.password.get()
        if username == "" or password == "":
            self.root_login.destroy()
        else:
            try:
                self.root_login.destroy()
                print("login successful")
            except Exception as E:
                print(E)
                self.root_login.destroy()


if __name__ == "__main__":
    HomePage()