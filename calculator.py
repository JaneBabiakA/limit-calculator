import tkinter as tk
from tkinter import *


def lexer(form_input, mystring, x):  # make this work with negative numbers
    mystring = [j for j in mystring]
    to_add = []
    while len(mystring) > 0:
        try:
            mystring[0] = int(mystring[0])
        except:  # i could us an isalpha or isnumeric here, maybe a later problem ?
            pass
        if mystring[0] == "(":
            mystring.pop(0)
            myfunction = lexer([], mystring, x)
            form_input.append(myfunction[0])
            mystring = myfunction[1]
        elif mystring[0] == ")":
            form_input.append(to_add)
            mystring.pop(0)
            return form_input, mystring
        elif mystring[0] in ["+", "-", "*", "/"]:
            if to_add:
                form_input.append("".join(to_add))
            to_add = []
            form_input.append(mystring[0])
            mystring.pop(0)
        elif mystring[0] == "^":
            if to_add:
                form_input[len(form_input)] = "".join(to_add) * pow(form_input, mystring[1])
            mystring.pop(0)
            mystring.pop(0)
        else:
            if mystring[0] == "x":
                if to_add:
                    print("".join(to_add), x)
                    to_add = ["".join(to_add) * x]
            else:
                to_add.append(str(mystring[0]))
            mystring.pop(0)
    if to_add:
        form_input.append("".join(to_add))
    return form_input


def infinity(mylist, x, left_hand, right_hand):
    if right_hand and left_hand:
        if infinity(mylist, x, True, False) == infinity(mylist, x, False, True):  # TODO: switch these to variables
            return infinity(mylist, x, True, False)
        else:
            return "DNE"
    elif right_hand:
        x += 0.001
    elif left_hand:
        x -= 0.001
    limit = plug(mylist[::])
    if limit > 0:
        print("voila", limit)
        return 'INF'
    else:
        print("voilall", limit)
        return "NINF"


def plug(mylist):
    if type(mylist) == list:
        print(mylist)
        result = float(plug(mylist[0]))
    else:
        result = mylist
        mylist = [mylist]
    for j in range(len(mylist)):
        if mylist[j] == "+":
            result += float(plug(mylist[j + 1]))
        elif mylist[j] == "-":
            result -= float(plug(mylist[j + 1]))
        elif mylist[j] == "*":
            print("before", result)
            result = result * float(plug(mylist[j + 1]))
            print("after", result)
        elif mylist[j] == "/":
            dvdby = float(plug(mylist[j + 1]))
            result = result / dvdby
        elif type(mylist[0]) == int:
            result = mylist[0]
    return result


def inputList(input, equation_input):
    if input == "DEL":
        if len(equation_input) > 0:
            equation_input.pop()
    elif input == "=":  # if 1, then True, if 0, then False
        l_hand = left_hand.get()
        r_hand = right_hand.get()
        lim = int(limEntry.get())
        if l_hand == 1 and r_hand == 1:
            left_result = myround(plug(lexer([], "".join(equation_input), lim - 0.00001)))
            right_result = myround(plug(lexer([], "".join(equation_input), lim + 0.00001)))
            if left_result == right_result:
                result = left_result
            else:
                result = "DNE"
        elif l_hand == 1:
            result = myround(plug(lexer([], "".join(equation_input), lim - 0.001)))
        elif r_hand == 1:
            result = myround(plug(lexer([], "".join(equation_input), lim + 0.001)))
        equation_input.append(input)
        equation_input.append(result)
    else:
        equation_input.append(input)
    calculator.configure(text=equation_input)
    return equation_input


def myround(number):
    print("hi")
    if number >= 1000:
        number = "INF"
    elif number <= -1000:
        number = "NINF"
    else:
        print("hi")
        number = round(number, 2)
    return number


# TODO: if DNE, cos, tan, sin, cot, csc, sec, x^2, sqrt, log/ln


equation_input = []
window = tk.Tk()
left_hand = tk.IntVar()
right_hand = tk.IntVar()
operationsFrame = tk.Frame(bg="pink")
operationsFrame.pack(side=BOTTOM)
buttonFrame = tk.Frame(bg="pink", master=operationsFrame)
buttonFrame.pack(side=BOTTOM)
displayFrame = tk.Frame(bg="pink", borderwidth=6, relief=tk.SUNKEN)
displayFrame.pack(side=TOP, fill="x")
settingsFrame = tk.Frame(bg="pink", master=operationsFrame)
settingsFrame.pack(side=TOP)
message = ""
calculator = tk.Label(text=message, bg='pink', master=displayFrame)
calculator.pack()
rightBox = tk.Checkbutton(master=settingsFrame, text="RH", bg="pink", variable=right_hand)
rightBox.grid(row=0, column=1)
leftBox = tk.Checkbutton(master=settingsFrame, text="LH", bg="pink", variable=left_hand)
leftBox.grid(row=0, column=0)
limLabel = tk.Label(master=settingsFrame, text="lim as x->", bg="pink")
limLabel.grid(row=1, column=0)
limEntry = tk.Entry(master=settingsFrame)
limEntry.grid(row=1, column=1)

buttons = ["s", "c", "t", "^", "r", "7", "8", "9", "(", ")", "4", "5", "6", "*", "/", "1", "2", "3", "+", "-", "0", ".",
           'D', "x", "="]

row = -1
for i in range(len(buttons)):
    if i % 5 == 0:
        row += 1
    column = (i) % 5
    newButton = tk.Button(text=buttons[i], master=buttonFrame, relief=tk.RAISED, borderwidth=3)
    newButton.grid(column=column, row=row)
    newButton.bind("<Button-1>", lambda e, i=i: inputList(buttons[i], equation_input))
    # tkinter passes an object to the first parameter when using bind, so u gotta create a second param for urself

window.mainloop()
