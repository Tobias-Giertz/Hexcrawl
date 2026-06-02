# This code is generated using PyUIbuilder: https://pyuibuilder.com

import os
import tkinter as tk
from tkinter import ttk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


main = tk.Tk()
main.title("Main Window")
main.config(bg="#FFFFFF")
main.geometry("1920x1280")
main.update_idletasks()

geometryX = 0
geometryY = 0

main.geometry("+%d+%d"%(geometryX, geometryY))


style = ttk.Style(main)
style.theme_use("clam")

menu = tk.Menu(main)
main.config(menu=menu)
menu_0 = tk.Menu(menu, tearoff=0)
menu_0.add_command(label="New", command=lambda: print("New clicked"))
menu_0.add_command(label="Open", command=lambda: print("Open clicked"))
menu.add_cascade(label="File", menu=menu_0)
menu_1 = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=menu_1)

frame = tk.Frame(master=main)
frame.config(bg="#EDECEC")
frame.pack(padx=10, pady=10, side=tk.TOP, anchor='n')

style.configure("action_input.TEntry", fieldbackground="#fff", foreground="#000")

action_input = ttk.Entry(master=main, style="action_input.TEntry")
action_input.pack(padx=10, pady=10, side=tk.TOP, anchor='n')

style.configure("advance.TButton", background="#E4E2E2", foreground="#000")
style.map("advance.TButton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

advance = ttk.Button(master=main, text="Advance", style="advance.TButton")
advance.pack(padx=10, pady=10, side=tk.TOP, anchor='n')


main.mainloop()