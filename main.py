import ttkbootstrap as ttk
from database import GradebookDB
from ui_components import GradebookGUI

if __name__ == "__main__":
    app = ttk.Window("Gradebook", "morph")
    app.state("zoomed")
    db = GradebookDB()
    GradebookGUI(app, db)
    app.mainloop()
