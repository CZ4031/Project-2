import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class BstNode:
    def __init__(self, key):
        self.key = key
        self.right = None
        self.left = None

    def insert(self, key):
        if self.key == key:
            return
        elif self.key < key:
            if self.right is None:
                self.right = BstNode(key)
            else:
                self.right.insert(key)
        else: # self.key > key
            if self.left is None:
                self.left = BstNode(key)
            else:
                self.left.insert(key)

    def display(self):
        lines, *_ = self._display_aux()
        count = 0
        my_str = ''
        for line in lines:
            #print(line)
            my_str += line + "\n"
            #count += 1

        #print(my_str)
        return my_str

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.key
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.key
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.key
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.key
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


# Functions for the application
def handle_selection_change(event):
    selected_indicies = schema_select.curselection()
    for i in selected_indicies:
        print(schema_select.get(i))

def take_input():
    input_content = inputBox.get("1.0","end")
    return input_content
    #print(input_content)

def print_output(annotation):
    outputBox.insert(END, annotation)

#plotting the graph
def plot():
    # the figure that will contain the plot
    fig = Figure(figsize=(5, 5),
                 dpi=100)

    # list of squares
    y = [i ** 2 for i in range(101)]

    # adding the subplot
    plot1 = fig.add_subplot(111)

    # plotting the graph
    plot1.plot(y)

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,root)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(row=0,column=1, padx=5, pady=5)
    #Label(right_frame, image=original_image).grid(row=0, column=0, padx=5, pady=5)

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                   window)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()


#Start Of the GUI
root = Tk()  # create root window
root.title("Assignment 2")  # title of the GUI window
root.maxsize(1980, 800)  # specify the max size the window can expand to
root.config(bg="skyblue")  # specify background color

#Add schema if have more
database_schema = ("TPC-H","none","Placeholder")
schema = tk.StringVar(value=database_schema)


# Create left and right frames
left_frame = Frame(root, width=200, height=800, bg='white')
left_frame.grid(row=0, column=0, padx=10, pady=5)

right_frame = Frame(root, width=100, height=60, bg='white')
right_frame.grid(row=0, column=1, padx=10, pady=5)
Tree = tk.Text(right_frame, height = 10,bg="light cyan")
Tree.grid(row=0, column=0, padx=10, pady=5)
b = BstNode(10)
for _ in range(10):
    b.insert(random.randint(0, 100))
val = b.display()
Tree.insert(END, val)



# NTU Image logo
image = PhotoImage(file="NTU_Logo.png")
original_image = image.subsample(10,10)  # resize image using subsample
Label(left_frame, image=original_image, bg='white').grid(row=0, column=0, padx=5, pady=5)

# Display Graph in right_frame
#Label(right_frame, text="Tree").grid(row=0,column=0, padx=5, pady=5)

# Create frame for SQL Query
SQL_bar = Frame(left_frame, width=180, height=185, bg='white')
SQL_bar.grid(row=2, column=0, padx=5, pady=5)

# Example labels that serve as placeholders for other widgets
Label(SQL_bar, text="Please Enter SQL Query", bg='white', font="Verdana 12 underline").grid(row=0, column=0)
schema_select = tk.Listbox(SQL_bar,listvariable=schema,height=6).grid(row=0,column=1)
inputBox = tk.Text(SQL_bar, height = 10,bg = "light yellow")
inputBox.grid(row=1, column=0, padx=5, pady=3, ipadx=10)
outputBox = tk.Text(SQL_bar, height = 10,bg="light cyan")
outputBox.grid(row=2, column=0, padx=5, pady=3, ipadx=10)
annotate_button = tk.Button(SQL_bar, text="Annotate Query", command=take_input).grid(row=1, column=1, padx=5, pady=3, ipadx=10)
#plot_button = Button(SQL_bar, command = plot,height = 2, width = 10, text = "Plot")
#plot_button.grid(row=2, column=1, padx=5, pady=3, ipadx=10)


root.mainloop()
