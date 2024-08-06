import tkinter as tk
from tkinter.ttk import Notebook
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Slider

class PhasePortraitApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Phase Portrait and Eigenvalues')
        self.state('zoomed')

        self.menu = tk.Menu(self, bg='lightgrey', fg='black')
        self.file_menu = tk.Menu(self.menu, tearoff=0, bg='lightgrey', fg='black')
        self.file_menu.add_command(label='Quit', command=self.quit)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.config(menu=self.menu)

        self.notebook = Notebook(self)
        graph_tab = tk.Frame(self.notebook)
        self.graph_tab = tk.Canvas(graph_tab)
        self.graph_tab.pack(side=tk.TOP, expand=1)

        self.notebook.add(graph_tab, text='Graph')
        self.notebook.pack(fill=tk.BOTH, expand=1)

        self.fig = Figure(figsize=(9, 7))
        self.fig.subplots_adjust(wspace=0.4, bottom=0.45)
        graph = FigureCanvasTkAgg(self.fig, self.graph_tab)
        graph.get_tk_widget().pack(side='top', fill='both', expand=True)
        PhasePortraitSlider(self.fig)

    def quit(self):
        self.destroy()

class PhasePortraitSlider():
    def __init__(self, fig):
        self.fig = fig
        self.a11 = 10
        self.a12 = -8
        self.a21 = 10
        self.a22 = 10
        self.quiver_scale = 1000

        self.ax1 = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122)

        self.plot_phase_portrait()

        self.axcolor = 'lightgoldenrodyellow'
        self.slider_ax_a11 = self.fig.add_axes([0.25, 0.2, 0.65, 0.03], facecolor=self.axcolor)
        self.slider_ax_a12 = self.fig.add_axes([0.25, 0.15, 0.65, 0.03], facecolor=self.axcolor)
        self.slider_ax_a21 = self.fig.add_axes([0.25, 0.1, 0.65, 0.03], facecolor=self.axcolor)
        self.slider_ax_a22 = self.fig.add_axes([0.25, 0.05, 0.65, 0.03], facecolor=self.axcolor)

        self.slider_a11 = Slider(self.slider_ax_a11, '$a_{11}$', -20, 20, valinit=self.a11)
        self.slider_a12 = Slider(self.slider_ax_a12, '$a_{12}$', -20, 20, valinit=self.a12)
        self.slider_a21 = Slider(self.slider_ax_a21, '$a_{21}$', -20, 20, valinit=self.a21)
        self.slider_a22 = Slider(self.slider_ax_a22, '$a_{22}$', -20, 20, valinit=self.a22)

        self.slider_a11.on_changed(self.update)
        self.slider_a12.on_changed(self.update)
        self.slider_a21.on_changed(self.update)
        self.slider_a22.on_changed(self.update)

        self.create_input_fields()

    def universal_fields(self, name, x, y, bound):
        exec(f"""tk.Label(text='{name} bounds:').place(x=10, y={y})
self.{name}_min_entry = tk.Entry()
self.{name}_min_entry.place(x={x}+30, y={y}, width=50)
self.{name}_min_entry.insert(0, '-{bound}')

self.{name}_max_entry = tk.Entry()
self.{name}_max_entry.place(x={x}+90, y={y}, width=50)
self.{name}_max_entry.insert(0, '{bound}')

tk.Label(text='Step:').place(x=200, y={y})
self.{name}_step_entry = tk.Entry()
self.{name}_step_entry.place(x={x}+185, y={y}, width=50)
self.{name}_step_entry.insert(0, '1')""")

    def create_input_fields(self):
        self.universal_fields('a11', 50, 30, 20)
        self.universal_fields('a12', 50, 50, 20)
        self.universal_fields('a21', 50, 70, 20)
        self.universal_fields('a22', 50, 90, 20)

        tk.Button(text='Update Bounds and Step', command=self.update_bounds_and_step).place(x=10, y=120)

    def update_bounds_and_step(self):
        try:
            a11_min = float(self.a11_min_entry.get())
            a11_max = float(self.a11_max_entry.get())
            a11_step = float(self.a11_step_entry.get())
            
            a12_min = float(self.a12_min_entry.get())
            a12_max = float(self.a12_max_entry.get())
            a12_step = float(self.a12_step_entry.get())
            
            a21_min = float(self.a21_min_entry.get())
            a21_max = float(self.a21_max_entry.get())
            a21_step = float(self.a21_step_entry.get())
            
            a22_min = float(self.a22_min_entry.get())
            a22_max = float(self.a22_max_entry.get())
            a22_step = float(self.a22_step_entry.get())
            

            self.slider_a11.valmin = a11_min
            self.slider_a11.valmax = a11_max
            self.slider_a11.valstep = a11_step

            self.slider_a12.valmin = a12_min
            self.slider_a12.valmax = a12_max
            self.slider_a12.valstep = a12_step

            self.slider_a21.valmin = a21_min
            self.slider_a21.valmax = a21_max
            self.slider_a21.valstep = a21_step

            self.slider_a22.valmin = a22_min
            self.slider_a22.valmax = a22_max
            self.slider_a22.valstep = a22_step

            self.slider_a11.ax.set_xlim(a11_min, a11_max)
            self.slider_a12.ax.set_xlim(a12_min, a12_max)
            self.slider_a21.ax.set_xlim(a21_min, a21_max)
            self.slider_a22.ax.set_xlim(a22_min, a22_max)
            self.slider_a11.reset()
            self.fig.canvas.draw_idle()

        except ValueError:
            msg.showerror('Invalid input', 'Please enter valid numerical values.')

    def plot_phase_portrait(self):
        A = np.array([[self.a11, self.a12], [self.a21, self.a22]])
        eigvals, eigvecs = np.linalg.eig(A)

        def dx_dt(X):
            return A @ X

        x1 = np.linspace(-10, 10, 20)
        x2 = np.linspace(-10, 10, 20)
        X1, X2 = np.meshgrid(x1, x2)
        U, V = np.zeros(X1.shape), np.zeros(X2.shape)

        for i in range(X1.shape[0]):
            for j in range(X1.shape[1]):
                x = np.array([X1[i, j], X2[i, j]])
                dx = dx_dt(x)
                U[i, j] = dx[0]
                V[i, j] = dx[1]

        self.ax1.clear()
        self.ax1.quiver(X1, X2, U, V, color='b', scale=self.quiver_scale)

        for i in range(len(eigvecs)):
            eigvec = eigvecs[:, i]
            if np.iscomplexobj(eigvec):
                eigvec = eigvec.real
            eigvec = eigvec / np.linalg.norm(eigvec)
            scale = 20  
            self.ax1.plot([-scale * eigvec[0], scale * eigvec[0]], [-scale * eigvec[1], scale * eigvec[1]], label=f'Eigenvector {i+1}', linestyle='solid', color='purple')

        self.ax1.set_xlim([-10, 10])
        self.ax1.set_ylim([-10, 10])
        self.ax1.set_xlabel('$x_1$')
        self.ax1.set_ylabel('$x_2$')
        self.ax1.axhline(0, color='black', lw=1)
        self.ax1.axvline(0, color='black', lw=1)
        self.ax1.set_title('Phase Portrait')
        self.ax1.grid(False)

        self.ax2.clear()
        self.ax2.scatter(np.real(eigvals), np.imag(eigvals), color='red', s=100)
        self.ax2.axhline(0, color='black', lw=1)
        self.ax2.axvline(0, color='black', lw=1)
        self.ax2.set_xlabel('Real Part')
        self.ax2.set_ylabel('Imaginary Part')
        self.ax2.set_title('Eigenvalues')
        self.ax2.grid()
        
        eigvals_text = f"Eigenvalues:\n{np.array2string(eigvals, precision=5, separator=', ')}"
        eigvecs_text = f"Eigenvectors:\n{np.array2string(eigvecs, precision=5, separator=', ')}"
        self.fig.texts.clear()
        self.fig.text(0.1, 0.3, eigvals_text, fontsize=10, ha='left')
        self.fig.text(0.5, 0.3, eigvecs_text, fontsize=10, ha='left')
        self.fig.canvas.draw()

    def update(self, val):
        self.a11 = self.slider_a11.val
        self.a12 = self.slider_a12.val
        self.a21 = self.slider_a21.val
        self.a22 = self.slider_a22.val
        self.plot_phase_portrait()

if __name__ == '__main__':
    app = PhasePortraitApp()
    app.mainloop()
