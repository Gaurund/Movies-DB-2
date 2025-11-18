from tkinter import Tk
from src.controller import Controller
from src.view import View
from src.db_ops import DB_connection

root = Tk()
view = View(root)
engine: str = "sqlite:///movie.db"
db_conn = DB_connection(engine=engine)
controller = Controller(db_connection=db_conn, view=view)
root.mainloop()
