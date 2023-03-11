from tkinter import StringVar
from tkinter import ttk


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
