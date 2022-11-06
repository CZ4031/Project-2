from pathlib import Path

#from tkinter import *
# Explicit imports to satisfy Flake8
import tkinter as tk
#from tkinter.ttk import *

#Functions for the appication
#def delete():
#   entry_1.delete("1.0","end")

#def submitSQL():
#    query = entry_1.get("1.0", "end-1c")
#    print(query)

#def displayAnnotation():
#    newWindow = Toplevel(window)
#    # Toplevel widget
#    newWindow.title("QEP")
# 
#    # sets the geometry of toplevel
#    newWindow.geometry("600x600")
#    Label(newWindow,
#          text ="Alternative Query Plan").pack()
#    displayTree = Text(newWindow,height = 100,width=100,bg="light cyan")
#    displayTree.pack()

class projectWindow(tk.Tk):
    def createLoginDetails(self):
        ipFrame = tk.Frame(self.sqlLabelFrame)
        ipFrame.pack(anchor=tk.W)
        portFrame = tk.Frame(self.sqlLabelFrame)
        portFrame.pack(anchor=tk.W)
        dbNameFrame = tk.Frame(self.sqlLabelFrame)
        dbNameFrame.pack(anchor=tk.W)
        userFrame = tk.Frame(self.sqlLabelFrame)
        userFrame.pack(anchor=tk.W)
        pwdFrame = tk.Frame(self.sqlLabelFrame)
        pwdFrame.pack(anchor=tk.W)

        ipLabel = tk.Label(ipFrame, text="IP address: ")
        ipLabel.pack(side=tk.LEFT)
        ipEntry = tk.Entry(ipFrame)
        ipEntry.pack(side=tk.RIGHT)

        portLabel = tk.Label(portFrame, text="Port: ")
        portLabel.pack(side=tk.LEFT)
        portEntry = tk.Entry(portFrame)
        portEntry.pack(side=tk.RIGHT)

        userLabel = tk.Label(userFrame, text="Username: ")
        userLabel.pack(side=tk.LEFT)
        userEntry = tk.Entry(userFrame)
        userEntry.pack(side=tk.RIGHT)

        pwdLabel = tk.Label(pwdFrame, text="Password: ")
        pwdLabel.pack(side=tk.LEFT)
        pwdEntry = tk.Entry(pwdFrame)
        pwdEntry.pack(side=tk.RIGHT)

        dbNameLabel = tk.Label(dbNameFrame, text="Database name: ")
        dbNameLabel.pack(side=tk.LEFT)
        dbNameEntry = tk.Entry(dbNameFrame)
        dbNameEntry.pack(side=tk.RIGHT)

    def scroll_move(self, event):
        self.planCanvas.scan_dragto(event.x, event.y, gain=1)
            
    def scroll_start(self, event):
        self.planCanvas.scan_mark(event.x, event.y)


    def onObjectClick(self, event):                  
        print('Got object click', event.x, event.y)
        print(event.widget.find_closest(event.x, event.y))

    def __init__(self):
        super().__init__()
        self.title("CZ4031 Database Project 2")
        #window.geometry("843x891")
        #window.configure(bg = "#FFFFFF")

        #mainFrame = tk.Frame(window)
        #mainFrame.pack()

        inputFrame = tk.Frame(self)
        inputFrame.pack(side=tk.LEFT)

        planFrame = tk.Frame(self)
        planFrame.pack(side=tk.RIGHT)

        planLabel = tk.Label(planFrame, text="Query:")
        planLabel.pack(anchor=tk.W)
        self.planCanvas = tk.Canvas(planFrame, height=600, width=600, bg="#FFFFFF")
        self.planCanvas.pack()

        self.planCanvas.bind("<ButtonPress-1>", self.scroll_start)
        self.planCanvas.bind("<B1-Motion>", self.scroll_move)

        o = self.planCanvas.create_oval(150, 10, 100, 60, fill='red')
        self.planCanvas.tag_bind(o, '<ButtonPress-1>', self.onObjectClick)

        self.sqlLabelFrame = tk.LabelFrame(inputFrame, text="PostgreSQL login")
        self.sqlLabelFrame.pack(fill="both", expand="yes")

        self.createLoginDetails()

        queryLabel = tk.Label(inputFrame, text="Query:")
        queryLabel.pack(anchor=tk.W)

        queryTextBox = tk.Text(inputFrame, height=4, width=20)
        queryTextBox.pack()

        self.resizable(False, False)



if __name__ == "__main__":
    app = projectWindow()
    app.mainloop()