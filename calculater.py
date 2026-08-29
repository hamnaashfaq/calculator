from tkinter import *

# ----------------------------------------------------------------
# Creating functions to perform calculations
# ----------------------------------------------------------------
expression = ""
history = []


def get_digit(digit):
    global expression
    expression += str(digit)
    display.config(text=expression)


def backspace():
    global expression
    expression = expression[:-1]
    display.config(text=expression)


def Clear():
    global expression
    expression = ""
    display.config(text="")


def getOperator(op):
    global expression
    if expression == "":
        return
    if expression[-1] in "*/+-":
        expression = expression[:-1]+op
    else:
        expression += op
    display.config(text=expression)


def getCalculation():
    global expression
    if expression == "":
        return
    numbers = []
    operators = []
    num = ""
    for ch in expression:
        if ch.isdigit():
            num += ch
        else:
            numbers.append(float(num))
            operators.append(ch)
            num = ""
    numbers.append(float(num))
    i = 0
    while i < len(operators):
        if operators[i] == "*":
            numbers[i] = numbers[i]*numbers[i+1]
            del operators[i]
            del numbers[i+1]
        elif operators[i] == "/":
            if numbers[i+1] == 0:
                display.config(text="error")
                raise ZeroDivisionError
            numbers[i] = numbers[i]/numbers[i+1]
            del operators[i]
            del numbers[i+1]
        else:
            i += 1
    result = numbers[0]
    for i in range(len(operators)):
        if operators[i] == "+":
            result += numbers[i+1]
        else:
            result -= numbers[i+1]
    result = round(result, 2)
    if result == int(result):
        result = int(result)
    history.append(f"{expression}={result}")
    expression = str(result)
    display.config(text=str(result))


def historyOp():
    if len(history) == 0:
        display.config(text="No history")
    else:
        display.config(text="\n".join(history))


cal = Tk()
cal.geometry("396x600")
cal.resizable(False, False)
cal.configure(background='black')
cal.title("Hamna's Calculator")
main_frame = Frame(cal, bg='#212121', bd=0)
main_frame.pack(fill="both", expand=True, padx=17, pady=15)
display = Label(main_frame, text='', font=('Arial', 32, 'bold'), fg='#FFFFFF', bg='#2A2A2A', width=13, pady=10,
                bd=0, highlightthickness=1, highlightbackground='#333333', highlightcolor='#333333')
display.grid(pady=(15, 20), ipady=20, padx=10, columnspan=6)
# ----------------------------------------------------------------
# Creating buttons
# ----------------------------------------------------------------

NUM_BG = "#3F3D3D"     # background for plain digit buttons
NUM_FG = "white"
OP_BG = "#3A3A3C"     # background for + - x /
OP_FC = "#FF9F0C"
CLEAR_BG = "#971212"
EQUAL_BG = "#FF9F0A"
EQUAL_FC = "#000000"
BACKSPACE_FG = "#0000FF"


buttons_data = [
    # digits
    {"label": "7", "row": 1, "col": 0, "bg": NUM_BG,
        "fg": NUM_FG, "command": lambda: get_digit(7)},
    {"label": "8", "row": 1, "col": 1, "bg": NUM_BG,
        "fg": NUM_FG, "command": lambda: get_digit(8)},
    {"label": "9", "row": 1, "col": 2, "bg": NUM_BG,
        "fg": NUM_FG, "command": lambda: get_digit(9)},
    {"label": "4", "row": 2, "col": 0, "bg": NUM_BG,
        "fg": NUM_FG, "command": lambda: get_digit(4)},
    {"label": "5", "row": 2, "col": 1, "bg": NUM_BG,
        "fg": NUM_FG, "command": lambda: get_digit(5)},
    {"label": "6", "row": 2, "col": 2, "bg": NUM_BG,
        "fg": NUM_FG, "command": lambda: get_digit(6)},
    {"label": "1", "row": 3, "col": 0, "bg": NUM_BG,
        "fg": NUM_FG, "command": lambda: get_digit(1)},
    {"label": "2", "row": 3, "col": 1, "bg": NUM_BG,
        "fg": NUM_FG, "command": lambda: get_digit(2)},
    {"label": "3", "row": 3, "col": 2, "bg": NUM_BG,
        "fg": NUM_FG, "command": lambda: get_digit(3)},
    {"label": "0", "row": 4, "col": 1, "bg": NUM_BG,
        "fg": NUM_FG, "command": lambda: get_digit(0)},

    # clear + equals
    {"label": "C", "row": 4, "col": 0, "bg": CLEAR_BG,
        "fg": "white", "command": lambda: Clear()},
    {"label": "=", "row": 4, "col": 2, "bg": EQUAL_BG,
        "fg": EQUAL_FC, "command": lambda: getCalculation()},

    # operators
    {"label": "+", "row": 1, "col": 3, "bg": OP_BG,
        "fg": OP_FC, "command": lambda: getOperator('+')},
    {"label": "-", "row": 2, "col": 3, "bg": OP_BG,
        "fg": OP_FC, "command": lambda: getOperator('-')},
    {"label": "x", "row": 3, "col": 3, "bg": OP_BG,
        "fg": OP_FC, "command": lambda: getOperator('*')},
    {"label": "/", "row": 4, "col": 3, "bg": OP_BG,
        "fg": OP_FC, "command": lambda: getOperator('/')},

    # history (spans all 4 columns)
    {"label": "history", "row": 5, "col": 1, "colspan": 2,
        "bg": OP_BG, "fg": OP_FC, "command": lambda: historyOp()},
    {"label": "⌫", "row": 5, "col": 0,
     "bg": OP_BG, "fg": BACKSPACE_FG, "command": lambda: backspace()}
]


# ----------------------------------------------------------------------
# STEP 2: One loop that turns EVERY dictionary above into a real button.
# ----------------------------------------------------------------------
for data in buttons_data:
    # .get("colspan", 1) means: "use data['colspan'] if it exists,
    # otherwise just use 1 as a fallback." This avoids a crash for
    # the buttons that don't define "colspan" at all.
    colspan = data.get("colspan", 1)

    btn = Button(
        main_frame,
        text=data["label"],
        bg=data["bg"],
        fg=data["fg"],
        height=1,
        width=8 if data["label"] == "history" else 4,
        activebackground="#55555A",
        command=data["command"],
        font=('Arial', 20)
    )
    btn.grid(row=data["row"], column=data["col"],
             columnspan=colspan, padx=2, pady=2)


cal.mainloop()
