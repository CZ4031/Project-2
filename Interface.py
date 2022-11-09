from pathlib import Path
#from types import NoneType
NoneType = type(None)

from typing import Tuple, Union
from preprocessing import *
from annotation import *

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

# class SimpleNode():

#     # Construct a node
#     def __init__(self) -> None:
#         self.children: list[SimpleNode] = []
#         self.value = ""
#         self.annotations = ""

def countLeafNodes(node: PlanNode):
    leafNodesNum = 0
    queue = [node]
    while(len(queue) > 0):
        curNode = queue.pop()
        if(len(curNode.children)>0):
            for node in curNode.children:
                queue.append(node)
        else:
            leafNodesNum += 1
    return leafNodesNum



class DisplayNode():
    def __init__(self) -> None:
        self.children: list[DisplayNode] = []
        self.text = ""
        self.annotations = ""
        self.depth:int = 0
        self.left_bound:int = 0
        self.right_bound:int = 0

def createDisplayNode(root: PlanNode):
    maxBound = countLeafNodes(root)
    rootDisplay = DisplayNode()
    rootDisplay.left_bound = 0
    rootDisplay.right_bound = maxBound
    rootDisplay.text = root.attributes['Node Type']
    rootDisplay.annotations = root.annotations
    nodeQueue:list[Tuple[DisplayNode, PlanNode, Tuple[int, int]]] = [] # tuple of (displayNode parent, node child)
    if(len(root.children) == 1):
        nodeQueue.append((rootDisplay, root.children[0], (0, maxBound)))
    elif(len(root.children) == 2):
        nodeQueue.append((rootDisplay, root.children[0], (0, countLeafNodes(root.children[0]))))
        nodeQueue.append((rootDisplay, root.children[1], (countLeafNodes(root.children[0]), maxBound)))
    while(len(nodeQueue) > 0):
        curNode = nodeQueue.pop(0)
        newChild = DisplayNode()
        newChild.left_bound = curNode[2][0]
        newChild.right_bound = curNode[2][1]
        newChild.text = curNode[1].attributes['Node Type']
        newChild.annotations = curNode[1].annotations
        newChild.depth = curNode[0].depth + 1
        # append to parent
        curNode[0].children.append(newChild)
        if(len(curNode[1].children) == 1):
            nodeQueue.append((newChild, curNode[1].children[0], (newChild.left_bound, newChild.right_bound)))
        elif(len(curNode[1].children) == 2):
            nodeQueue.append((newChild, curNode[1].children[0], (newChild.left_bound, newChild.left_bound + countLeafNodes(curNode[1].children[0]))))
            nodeQueue.append((newChild, curNode[1].children[1], (newChild.left_bound + countLeafNodes(curNode[1].children[0]), newChild.right_bound)))
    return rootDisplay

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
        self.ipEntry = tk.Entry(ipFrame)
        self.ipEntry.pack(side=tk.RIGHT)

        portLabel = tk.Label(portFrame, text="Port: ")
        portLabel.pack(side=tk.LEFT)
        self.portEntry = tk.Entry(portFrame)
        self.portEntry.pack(side=tk.RIGHT)

        userLabel = tk.Label(userFrame, text="Username: ")
        userLabel.pack(side=tk.LEFT)
        self.userEntry = tk.Entry(userFrame)
        self.userEntry.pack(side=tk.RIGHT)

        pwdLabel = tk.Label(pwdFrame, text="Password: ")
        pwdLabel.pack(side=tk.LEFT)
        self.pwdEntry = tk.Entry(pwdFrame)
        self.pwdEntry.pack(side=tk.RIGHT)

        dbNameLabel = tk.Label(dbNameFrame, text="Database name: ")
        dbNameLabel.pack(side=tk.LEFT)
        self.dbNameEntry = tk.Entry(dbNameFrame)
        self.dbNameEntry.pack(side=tk.RIGHT)

        loginBtn = tk.Button(self.sqlLabelFrame, text="LOGIN", command=self.processLogin)
        loginBtn.pack()

    def scroll_move(self, event):
        self.planCanvas.scan_dragto(event.x, event.y, gain=1)
            
    def scroll_start(self, event):
        self.planCanvas.scan_mark(event.x, event.y)


    def onObjectClick(self, event):
        x = event.widget.canvasx(event.x)
        y = event.widget.canvasy(event.y)
        self.annoStr.set(self.dictExtraToID[event.widget.find_closest(x, y)[0]])
        if(self.dictExtraToID[event.widget.find_closest(x, y)[0]] != ""):
            self.open_popup(self.dictExtraToID[event.widget.find_closest(x, y)[0]])
        # self.annoStr.set(self.dictExtraToID[event.widget.find_closest(event.x, event.y)[0]])
        # if(self.dictExtraToID[event.widget.find_closest(event.x, event.y)[0]] != ""):
        #     self.open_popup(self.dictExtraToID[event.widget.find_closest(event.x, event.y)[0]])

    def createTextRectangle(self, text: str, canvas: tk.Canvas, x0: int, y0: int):
        rectangle = canvas.create_rectangle(x0, y0, x0+100, y0+50, fill = "#FFFFFF")
        textline = canvas.create_text(x0+50, y0+25, text=text, justify = 'center')
        self.planCanvas.tag_bind(rectangle, '<ButtonPress-1>', self.onObjectClick)
        self.planCanvas.tag_bind(textline, '<ButtonPress-1>', self.onObjectClick)
        return (rectangle, textline)

    def open_popup(self, text:str):
        top=tk.Toplevel(self)
        top.title("Annotation")
        lbl = tk.Label(top, text=text, font=('Arial', 12, ''), wraplength=300)
        lbl.pack()
        btn = tk.Button(top, text="Close", command=top.destroy)
        btn.pack()

    def drawCanvasPlan(self, root: PlanNode):
        self.planCanvas.delete("all")
        self.dictExtraToID = {}

        rootD = createDisplayNode(root)

        drawQueue:list[Tuple[DisplayNode, Union[DisplayNode, NoneType]]] = [(rootD, None)]
        while(len(drawQueue) >0 ):
            curTup = drawQueue.pop(0)
            curNode = curTup[0]
            for child in curNode.children:
                drawQueue.append((child, curNode))
            x = (curNode.left_bound*200 + curNode.right_bound*200)/2 - 50
            y = curNode.depth * 100 + 50 - 25
            (rect, line) = self.createTextRectangle(curNode.text + ":" + str(curNode.left_bound) +":" + str(curNode.right_bound), self.planCanvas, x, y)
            self.dictExtraToID[rect]=curNode.annotations
            self.dictExtraToID[line]=curNode.annotations
            if(curTup[1] != None):
                self.planCanvas.create_line((curNode.left_bound*200 + curNode.right_bound*200)/2, curNode.depth * 100 + 50 - 25, (curTup[1].left_bound*200 + curTup[1].right_bound*200)/2, (curNode.depth-1) * 100 + 50 + 25)

    def processQuery(self):
        with open('query3.txt', 'r') as file:
            data = file.read().replace('\n', ' ')
        query = data
        self.connect.getAllQueryPlans(query)
        print(self.connect.query_plans['chosen_plan'][1].print_tree())

        annotation = Annotation()
        annotation.traverseTree(self.connect.query_plans['chosen_plan'][1])

        self.drawCanvasPlan(self.connect.query_plans['chosen_plan'][1])
        print("QUERY:", self.queryTextBox.get("1.0",'end-1c'))

    def processLogin(self):
        self.connect = SetUp(self.ipEntry.get(), self.portEntry.get(), self.dbNameEntry.get(), self.userEntry.get(), self.pwdEntry.get())
        #query = "SELECT * FROM customer"
       
        # print("-------------------Best plan operator tree--------------")
        # print(self.connect.query_plans['chosen_plan'][1].print_tree())
        print("IP:", self.ipEntry.get())
        print("PORT:", self.portEntry.get())
        print("USER:", self.userEntry.get())
        print("PWD:", self.pwdEntry.get())
        print("DB NAME:", self.dbNameEntry.get())

    
    def __init__(self):
        super().__init__()
        self.dictExtraToID = {}
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


        # rootS = SimpleNode()

        # rootS.value="TEST"
        # rootS.annotations="LOLLOLLOLLOLLOLLOLLOLLOLLOLLOLLOLLOLLOLLOLLOLLOLLOLLOLLOLLOLLOLLOLLOLLOLLOLLOL"

        # node1 = SimpleNode()
        # node1.value = "1"

        # node2 = SimpleNode()
        # node2.value = "2"
        # rootS.children.append(node1)
        # rootS.children.append(node2)

        # node3 = SimpleNode()
        # node3.value = "3"

        # node4 = SimpleNode()
        # node4.value = "4"

        # node1.children.append(node3)
        # node1.children.append(node4)

        # node5 = SimpleNode()
        # node5.value = "5"

        # node6 = SimpleNode()
        # node6.value = "6"

        # node4.children.append(node5)
        # node4.children.append(node6)

        self.planCanvas.bind("<ButtonPress-1>", self.scroll_start)
        self.planCanvas.bind("<B1-Motion>", self.scroll_move)

        self.sqlLabelFrame = tk.LabelFrame(inputFrame, text="PostgreSQL login")
        self.sqlLabelFrame.pack(fill="both", expand="yes")

        self.createLoginDetails()

        queryLabel = tk.Label(inputFrame, text="Query:")
        queryLabel.pack(anchor=tk.W)

        self.queryTextBox = tk.Text(inputFrame, height=4, width=20)
        self.queryTextBox.pack()

        processBtn = tk.Button(inputFrame, text="Process query", command=self.processQuery)
        processBtn.pack()

        annoLabel = tk.Label(inputFrame, text="Annotation:")
        annoLabel.pack()
        self.annoStr = tk.StringVar()
        annoMsg = tk.Label(inputFrame, textvariable = self.annoStr, wraplength=150)
        annoMsg.pack()
        self.resizable(False, False)



# if __name__ == "__main__":
#     app = projectWindow()
#     app.mainloop()