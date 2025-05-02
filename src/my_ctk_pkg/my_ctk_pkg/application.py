import tkinter as tk
from tkinter import ttk

class Application(tk.Tk):
    def __init__(self, node, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("GUI controller")
        self.node = node
        self.entry_var = tk.IntVar()
        ttk.Label(self, text='Enter a Integer').pack()
        number_entry = ttk.Entry(self, textvariable=self.entry_var)
        number_entry.pack()
        pub_button = ttk.Button(self, text='Publish', command=self._on_pub)
        pub_button.pack()

    def _on_pub(self, *_):
        self.node.publish_custom_number(self.entry_var.get())

