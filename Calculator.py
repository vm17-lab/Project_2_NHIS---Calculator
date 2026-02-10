import tkinter as tk
from tkinter import messagebox
import math
import winsound
import re

# --- Logic Functions ---
def play_sound():
    try:
        winsound.Beep(1200, 20) 
    except:
        pass

def robust_eval(expression, mode):
    temp_expr = expression
    temp_expr = temp_expr.replace('×', '*').replace('÷', '/').replace('^', '**')
    temp_expr = temp_expr.replace('π', 'math.pi').replace('√', 'sqrt').replace('%', '/100')
    temp_expr = re.sub(r'\be\b', 'math.e', temp_expr)
    temp_expr = re.sub(r'(\d)([a-zA-Z\(π])', r'\1*\2', temp_expr)
    temp_expr = re.sub(r'([\)πe])(\d)', r'\1*\2', temp_expr)

    if mode == "DEG":
        sin, cos, tan = lambda x: math.sin(math.radians(x)), lambda x: math.cos(math.radians(x)), lambda x: math.tan(math.radians(x))
    else:
        sin, cos, tan = math.sin, math.cos, math.tan

    safe_namespace = {
        'math': math, 'sin': sin, 'cos': cos, 'tan': tan,
        'log': math.log10, 'ln': math.log, 'sqrt': math.sqrt,
        'factorial': math.factorial, 'abs': abs
    }
    return eval(temp_expr, {"__builtins__": None}, safe_namespace)

def on_click(text):
    play_sound()
    cur = display_var.get()
    try:
        if text == "=":
            res = robust_eval(cur, current_mode.get())
            display_var.set(int(res) if isinstance(res, float) and res.is_integer() else round(res, 8))
        elif text == "C": display_var.set("0")
        elif text == "DEL": display_var.set(cur[:-1] if len(cur) > 1 else "0")
        elif text == "±": display_var.set(cur[1:] if cur.startswith("-") else "-" + cur if cur != "0" else "0")
        elif text in ["sin", "cos", "tan", "log", "ln", "√", "x!"]:
            fn = "factorial" if text == "x!" else ("sqrt" if text == "√" else text)
            display_var.set(fn + "(" if cur == "0" else cur + fn + "(")
        else:
            display_var.set(text if cur == "0" and text not in "+-×÷.%()^" else cur + text)
    except:
        messagebox.showerror("Error", "Invalid Expression")
        display_var.set("0")

# --- UI Setup ---
win = tk.Tk()
win.title("Calculator")
win.geometry("400x700")
win.configure(bg="#0F111A") 

display_var = tk.StringVar(value="0")
current_mode = tk.StringVar(value="DEG")

# Color Palette 
COLORS = {
    "bg": "#0F111A",
    "disp_bg": "#1A1C25",
    "num": "#292D3E",      # Deep Slate
    "op": "#FFB627",       # Amber
    "fn": "#82AAFF",       # Soft Blue
    "special": "#F07178",  # Coral Red
    "equal": "#C3E88D",    # Pastel Green
    "mode_on": "#BB80FF",  # Electric Purple
    "text": "#EEFFFF"
}

# Hover Effects
def on_enter(e): e.widget['background'] = '#444B66'
def on_leave_num(e): e.widget['background'] = COLORS["num"]
def on_leave_fn(e): e.widget['background'] = COLORS["fn"]

# --- Mode Selector ---
mode_frame = tk.Frame(win, bg=COLORS["bg"])
mode_frame.pack(pady=20)

def update_mode_ui(mode):
    current_mode.set(mode)
    play_sound()
    if mode == "DEG":
        deg_btn.config(bg=COLORS["mode_on"], fg=COLORS["bg"])
        rad_btn.config(bg=COLORS["num"], fg=COLORS["text"])
    else:
        rad_btn.config(bg=COLORS["mode_on"], fg=COLORS["bg"])
        deg_btn.config(bg=COLORS["num"], fg=COLORS["text"])

deg_btn = tk.Button(mode_frame, text="DEGREES", width=12, relief="flat", font=("Consolas", 10),
                    command=lambda: update_mode_ui("DEG"), bg=COLORS["mode_on"], fg=COLORS["bg"])
deg_btn.pack(side="left", padx=5)

rad_btn = tk.Button(mode_frame, text="RADIANS", width=12, relief="flat", font=("Consolas", 10),
                    command=lambda: update_mode_ui("RAD"), bg=COLORS["num"], fg=COLORS["text"])
rad_btn.pack(side="left", padx=5)

# --- Display ---
display_container = tk.Frame(win, bg=COLORS["disp_bg"], bd=10)
display_container.pack(fill="x", padx=20, pady=10)

display = tk.Entry(display_container, textvariable=display_var, font=("Consolas", 36),
                   bg=COLORS["disp_bg"], fg=COLORS["text"], justify="right", borderwidth=0)
display.pack(fill="x")

# --- Buttons ---
btn_frame = tk.Frame(win, bg=COLORS["bg"])
btn_frame.pack(expand=True, fill="both", padx=15, pady=15)

buttons = [
    ('sin',0,0), ('cos',0,1), ('tan',0,2), ('log',0,3), ('ln',0,4),
    ('(',1,0),   (')',1,1),   ('x!',1,2),  ('e',1,3),   ('^',1,4),
    ('C',2,0),   ('DEL',2,1), ('%',2,2),   ('÷',2,3),   ('√',2,4),
    ('7',3,0),   ('8',3,1),   ('9',3,2),   ('×',3,3),   ('π',3,4),
    ('4',4,0),   ('5',4,1),   ('6',4,2),   ('-',4,3),   ('±',4,4),
    ('1',5,0),   ('2',5,1),   ('3',5,2),   ('+',5,3),   ('=',5,4),
    ('0',6,0),   ('.',6,2)
]

for t, r, c in buttons:
    # Assign specific colors and fonts
    curr_color = COLORS["fn"]
    curr_fg = COLORS["bg"]
    
    if t in '0123456789.': 
        curr_color = COLORS["num"]
        curr_fg = COLORS["text"]
    elif t in '+-×÷%': 
        curr_color = COLORS["op"]
    elif t in 'CDEL': 
        curr_color = COLORS["special"]
    elif t == '=': 
        curr_color = COLORS["equal"]

    btn = tk.Button(btn_frame, text=t, font=("Arial", 12, "bold"),
                    bg=curr_color, fg=curr_fg, activebackground="white",
                    relief="flat", bd=0, command=lambda x=t: on_click(x))
    
    # Glow/Hover logic
    if t in '0123456789.':
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave_num)

    if t == '0':
        btn.grid(row=r, column=c, columnspan=2, sticky="nsew", padx=4, pady=4)
    else:
        btn.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)

for i in range(5): btn_frame.grid_columnconfigure(i, weight=1)
for i in range(7): btn_frame.grid_rowconfigure(i, weight=1)

win.mainloop()