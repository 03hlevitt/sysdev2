from tkinter import Tk, TOP, BOTTOM, ttk


class UpdateMsg:
    """display message when something is succesfully updated or otherwise"""

    def __init__(self, message: str):
        """constructor for class for displaying update messages

        Args:
            message (str): message to be displayed
        """
        self.root_update_msg = Tk()
        self.root_update_msg.title("UPDATE")
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
