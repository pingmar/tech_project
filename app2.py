import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from phaseportrait import PhasePortrait2D
import sympy as sp

class FunctionGrapherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Function Grapher and Phase Flow')
        self.state('zoomed')

        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.alpha = 1.0
        self.create_left_frame()
        self.create_right_frame()

        self.update_graphs()

    def create_left_frame(self):
        tk.Label(self.left_frame, text="Variable Change Intervals and Graph Limits", font=("Arial", 12)).pack(pady=10)

        self.start_label = tk.Label(self.left_frame, text="Start:")
        self.start_label.pack(pady=5)
        self.start_entry = tk.Entry(self.left_frame)
        self.start_entry.pack(pady=5)
        self.start_entry.insert(0, "-20")

        self.end_label = tk.Label(self.left_frame, text="End:")
        self.end_label.pack(pady=5)
        self.end_entry = tk.Entry(self.left_frame)
        self.end_entry.pack(pady=5)
        self.end_entry.insert(0, "20")

        self.ylim_label = tk.Label(self.left_frame, text="Y-axis Limit:")
        self.ylim_label.pack(pady=5)
        self.ylim_entry = tk.Entry(self.left_frame)
        self.ylim_entry.pack(pady=5)
        self.ylim_entry.insert(0, "20")

        self.func_label = tk.Label(self.left_frame, text="Function:")
        self.func_label.pack(pady=5)
        self.func_entry = tk.Entry(self.left_frame)
        self.func_entry.pack(pady=5)
        self.func_entry.insert(0, "x")

        self.alpha_slider = tk.Scale(self.left_frame, from_=-5, to=20, resolution=0.1, orient=tk.HORIZONTAL, label='alpha', length=300)
        self.alpha_slider.pack(pady=10)
        self.alpha_slider.set(1.0)

        self.update_button = tk.Button(self.left_frame, text="Update Graphs", command=self.update_graphs)
        self.update_button.pack(pady=20)

        self.roots_label = tk.Label(self.left_frame, text="Roots of the Function", font=("Arial", 12))
        self.roots_label.pack(pady=10)

        self.real_roots_label = tk.Label(self.left_frame, text="Real Roots:", font=("Arial", 10))
        self.real_roots_label.pack(pady=5)
        self.real_roots_text = tk.Text(self.left_frame, height=5, width=30)
        self.real_roots_text.pack(pady=5)

        self.complex_roots_label = tk.Label(self.left_frame, text="Complex Roots:", font=("Arial", 10))
        self.complex_roots_label.pack(pady=5)
        self.complex_roots_text = tk.Text(self.left_frame, height=5, width=30)
        self.complex_roots_text.pack(pady=5)

        self.fig_left, self.ax_left = plt.subplots(figsize=(6, 6))
        self.canvas_left = FigureCanvasTkAgg(self.fig_left, master=self.left_frame)
        self.canvas_left.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def create_right_frame(self):
        self.function_view_label = tk.Label(self.right_frame, text="", font=("Arial", 12))
        self.function_view_label.pack(pady=10)

        self.fig_right, self.ax_right = plt.subplots(figsize=(4, 4))
        self.canvas_right = FigureCanvasTkAgg(self.fig_right, master=self.right_frame)
        self.canvas_right.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.phase_frame = tk.Frame(self.right_frame)
        self.phase_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def update_graphs(self):
        start = float(self.start_entry.get())
        end = float(self.end_entry.get())
        ylim = float(self.ylim_entry.get())
        self.alpha = self.alpha_slider.get()

        x = np.linspace(start, end, 400)
        func_str = self.func_entry.get()
        y = self.function(x, func_str)

        self.ax_right.clear()
        self.ax_right.plot(x, y, label='Function')
        self.ax_right.set_title('Function')
        self.ax_right.set_xlabel('x')
        self.ax_right.set_ylabel('F(x)')
        self.ax_right.grid()
        self.ax_right.legend()

        roots = self.find_roots(func_str)
        real_roots = [root.evalf() for root in roots if sp.im(root) == 0]
        complex_roots = [root.evalf() for root in roots if sp.im(root) != 0]

        self.real_roots_text.delete('1.0', tk.END)
        for root in real_roots:
            self.real_roots_text.insert(tk.END, f"{root}\n")

        self.complex_roots_text.delete('1.0', tk.END)
        for root in complex_roots:
            self.complex_roots_text.insert(tk.END, f"{root}\n")

        self.ax_left.clear()
        self.ax_left.scatter([sp.re(root) for root in real_roots], [0]*len(real_roots), color='red', s=100, label='Real Roots')
        self.ax_left.scatter([sp.re(root) for root in complex_roots], [sp.im(root) for root in complex_roots], color='blue', s=100, label='Complex Roots')
        self.ax_left.axhline(0, color='black', lw=1)
        self.ax_left.axvline(0, color='black', lw=1)
        self.ax_left.set_title('Roots of the Function')
        self.ax_left.set_xlabel('Re(x)')
        self.ax_left.set_ylabel('Im(x)')
        self.ax_left.grid()
        self.ax_left.legend()

        function_view = f"Function: {func_str} with alpha = {self.alpha}"
        self.function_view_label.config(text=function_view)

        self.ax_right.set_xlim(start, end)
        self.ax_right.set_ylim(-ylim, ylim)

        self.update_phase_portrait(start, end)

        self.canvas_right.draw()
        self.canvas_left.draw()
        self.canvas_phase.draw()

    def update_phase_portrait(self, start, end):
        def dF_1(x, y, *, alpha = self.alpha):
            return eval(self.func_entry.get()), 0

        pp = PhasePortrait2D(dF_1, [start, end])
        fig_phase, ax_phase = pp.plot()

        for widget in self.phase_frame.winfo_children():
            widget.destroy()

        canvas_phase = FigureCanvasTkAgg(fig_phase, master=self.phase_frame)
        canvas_phase.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas_phase = canvas_phase

    def function(self, x, func_str):
        alpha = self.alpha
        return eval(func_str)

    def find_roots(self, func_str):
        x = sp.symbols('x')
        alpha = self.alpha
        func = eval(func_str)
        roots = sp.solve(func, x)
        return roots

if __name__ == '__main__':
    app = FunctionGrapherApp()
    app.mainloop()
