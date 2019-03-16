"""System of linear equation solver application module.

Features:
    - parsing and solving user-entered systems of linear equations
    - generating random systems of linear equations
    - saving and loading equations from JSON files
    - visualizing equation variables

Prequisities:
    - tkinter
    - json
    - matplotlib
    - numpy
"""

import tkinter
import matplotlib.pyplot as plt
from tkinter import messagebox, filedialog
from solver import Equation, floatize_fractions2d

eq = Equation()


def about():
    """Show information about application."""
    messagebox.showinfo("About", "System of linear equations solver\nVersion 1.0\n\nCreated by Karol Oleszek and Krzysztof Olipra")


def solve_entered():
    """Parse and solve user-entered equations."""
    try:
        eq.load_from_string(MATRIX_DISPLAY.get("1.0", tkinter.END))
        result = str(eq)
        MATRIX_DISPLAY.delete("1.0", tkinter.END)
        MATRIX_DISPLAY.insert("1.0", result)
    except:
        messagebox.showinfo("Parsing error", "Wrong equation format. Please provide equation in correct format:\n1x1 +2x2 +3x3 = 4\n1x1 +2x2 +3x3 = 4\n1x1 +2x2 +3x3 = 4")    


def save_to_file():
    """Save current equations to file."""
    path = filedialog.asksaveasfilename(defaultextension=".json")
    eq.save_to_file(str(path))


def load_from_file():
    """Load equations from file."""
    path = filedialog.askopenfilename()
    eq.load_from_file(str(path))
    result = str(eq)
    MATRIX_DISPLAY.delete("1.0",tkinter.END)
    MATRIX_DISPLAY.insert("1.0", result)


def randomize():
    """Generate random equations."""
    eq.generate_random()
    result = str(eq)
    MATRIX_DISPLAY.delete("1.0",tkinter.END)
    MATRIX_DISPLAY.insert("1.0", result)


def visualize():
    """Visualize variable attributes."""
    plt.pcolor(floatize_fractions2d(eq.variable_matrix))
    plt.show()


# Main form initialization
MAIN_FORM = tkinter.Tk()
MAIN_FORM.state('zoomed')
MAIN_FORM.title('System of linear equations solver')
MATRIX_DISPLAY = tkinter.Text(MAIN_FORM)
MATRIX_DISPLAY.pack(expand=True, fill='both')

# Menu initialization
MENUBAR = tkinter.Menu(MAIN_FORM)
MATRIX_MENU = tkinter.Menu(MENUBAR, tearoff = 0)
MATRIX_MENU.add_command(label="Solve entered equation", command = solve_entered)
MATRIX_MENU.add_command(label = "Load equation from file", command = load_from_file)
MATRIX_MENU.add_command(label = "Save equation to file", command = save_to_file)
MATRIX_MENU.add_command(label = "Generate random equation", command = randomize)
MATRIX_MENU.add_command(label = "Visualize variable matrix", command = visualize)
MATRIX_MENU.add_separator()
MATRIX_MENU.add_command(label = "Exit", command = MAIN_FORM.quit)
MENUBAR.add_cascade(label = "Equation", menu = MATRIX_MENU)
MENUBAR.add_command(label = "About", command = about)
MAIN_FORM.config(menu = MENUBAR)

# Run an application
MAIN_FORM.mainloop()
