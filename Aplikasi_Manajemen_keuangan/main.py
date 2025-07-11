from tkinter import Tk
from ui import setup_ui

if __name__ == "__main__":
    root = Tk()
    root.title("Manajemen Keuangan Restoran - CRUD")
    root.geometry("800x500")
    setup_ui(root)
    root.mainloop()
