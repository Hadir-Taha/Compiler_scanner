from tkinter import *
import tkinter as tk
import sys
from PyQt5.QtWidgets import QWidget,QApplication,QTableWidget,QTableWidgetItem,QVBoxLayout

class Scanner(object):

    def __init__(self):

        self.ReservedWords = ["if", "then", "else", "end", "repeat", "until", "read", "write"]
        self.SpecialSymbols = ["+", "-", "*", "/", "=", "<",">", "(", ")", ";"]
        self.token = []
        self.set_value = ""
        self.set_type = ""
        self.number = "0123456789"
        self.symbol = "abcdefghijklmnopqrstuvwxyz"
        self.myPosition = 0
        self.myState = 1
        self.error=[]

    def take_token(self, next_state):
        if self.myState == 1:
            if next_state == "{":
                self.myState = 2
            elif next_state == ":":
                self.set_type = "Assign operator"
                self.myState = 3
            elif next_state in self.SpecialSymbols:
                if next_state == "+":
                    self.set_type = "Addition operator"
                elif next_state == "-":
                    self.set_type = "Subtract operator"
                elif next_state == "*":
                    self.set_type = "Multiplication operator"
                elif next_state == "/":
                    self.set_type = "Division operator"
                elif next_state == "=":
                    self.set_type = "Equal operator"
                elif next_state == "<":
                    self.set_type = "Less than operator"
                elif next_state == ">":
                    self.set_type = "Greater than operator"
                elif next_state == "(":
                    self.set_type = "Open bracket"
                elif next_state == ")":
                    self.set_type = "Closed bracket"
                elif next_state == ";":
                    self.set_type = "Semicolon operator"
                self.set_value = next_state
                self.myState = 6
            elif next_state in self.symbol:
                self.set_type = "Identifier"
                self.set_value = next_state
                self.myState = 4
            elif next_state in self.number:
                self.set_type = "Number"
                self.set_value = next_state
                self.myState = 5
            elif next_state != " " and next_state != "\n":
                self.myState = -1
                self.error.append(next_state)
        elif self.myState == 2:
            if next_state == "}":
                self.myState = 1
                self.set_value = ""
        elif self.myState == 3:
            if next_state == "=":
                self.set_value = ":="
                self.myState = 6
        elif self.myState == 4:
            if next_state in self.symbol:
                self.set_value += next_state
                if self.set_value in self.ReservedWords:
                    self.set_type = "Reserved word"
                    # self.myPosition -= 1
            else:
                self.myState = 6
                self.myPosition -= 1

        elif self.myState == 5:
            if next_state in self.number:
                self.set_value += next_state
            else:
                self.myState = 6
                self.myPosition -= 1

        elif self.myState == 6:
            self.token.append((self.set_value, self.set_type))
            self.myPosition -= 1
            self.myState = 1
        self.myPosition += 1

myscanner=Scanner()

app = QApplication(sys.argv)
qwidget = QWidget()
qwidget.setWindowTitle("Table Of Tokens")
qwidget.resize(500, 700)
layout = QVBoxLayout()
tableWidget = QTableWidget()
tableWidget.setFixedSize(450,800)
tableWidget.columnWidth(800)
tableWidget.rowHeight(200)

root=Tk()
root.geometry('1000x800')
root.title("TINY scanner")
l1=Label(root,text="Enter your TINY code please",font=("Calibri",20))
l1.pack(fill=tk.X, padx=10, pady=20)
text1=Text(root)
text1.insert(INSERT,"TINKER CODE ...")
text1.pack()
l2 = Label(text="THERE IS AN ERROR !!!",font=("Calibri",20))
l2.configure(foreground="red")

def ShowTokens():

    mydata=text1.get(1.0,END)
    first_line=1
    lines = mydata.split('\n')
    for line in lines:
        line = line + " "
        end = len(line[:-1])
        while myscanner.myPosition <= end:
            myscanner.take_token(line[myscanner.myPosition])
        myscanner.myPosition = 0
        if myscanner.myState < 0:
            lenth = len(myscanner.token)
            for i in range(lenth):
                for j in range(2):
                    print(myscanner.token[i][j])
            tableWidget.setColumnCount(2)
            tableWidget.setRowCount(lenth)
            # adding item in table
            tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Token Value"))
            tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Token Type"))
            for i in range(lenth):
                for j in range(2):
                    tableWidget.setItem(i, j, QTableWidgetItem(myscanner.token[i][j]))
                    tableWidget.setColumnWidth(i, 200)
            layout.addWidget(tableWidget)
            qwidget.setLayout(layout)
            qwidget.show()
            print("THERE IS AN ERROR !!! ", first_line)
            l2.pack(fill=tk.X, padx=10, pady=10)
            break
        first_line += 1

    lenth = len(myscanner.token)
    for i in range(lenth):
        for j in range(2):
          print(myscanner.token[i][j])

    tableWidget.setColumnCount(2)
    tableWidget.setRowCount(lenth)
    # adding item in table
    tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Token Value"))
    tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Token Type"))
    for i in range(lenth):
        for j in range(2):
            tableWidget.setItem(i, j, QTableWidgetItem(myscanner.token[i][j]))
            tableWidget.setColumnWidth(i,200)
    layout.addWidget(tableWidget)
    qwidget.setLayout(layout)
    qwidget.show()
    print("PROCESS RUN SUCCESSFULLY !!!")

button1=Button(root, text="Show my tokens",font=("Calibri",12), command=ShowTokens).pack(padx=10, pady=15)

def clearCode():
    text1.delete('1.0', END)
    tableWidget.clear()
    myscanner.token.clear()
    l2.config(text="")

button2=Button(root, text="clear code",font=("Calibri",12), command=clearCode).pack()

tableWidget.setColumnWidth(0,250)

root.mainloop()

