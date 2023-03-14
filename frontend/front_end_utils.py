"""common utils code used in the front end"""
from tkinter import (
    N,
    E,
    S,
    W,
    Frame,
    VERTICAL,
    NS,
)
from tkinter import ttk


def create_list_frame(
    baseframe: Frame, column: int = 0, row: int = 1
) -> Frame:
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
