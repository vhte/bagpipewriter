import tkinter as tk
from application import Application
from bagpipemanager.bagpipemanager import BagpipeManager

# Bagpipe Manager
bagpipe_manager = BagpipeManager()

# Application
app = Application(bagpipe_manager)
app.mainloop()
