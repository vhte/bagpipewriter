import tkinter as tk
from application import Application
from bagpipewriter.bagpipewriter import BagpipeWriter

# Bagpipe Writer
bagpipe_writer = BagpipeWriter()

# Application
app = Application(bagpipe_writer)
app.mainloop()
