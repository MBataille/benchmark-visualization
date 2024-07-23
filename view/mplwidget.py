from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib
import numpy as np

# Ensure using PyQt5 backend
matplotlib.use('QT5Agg')

# Matplotlib canvas class to create figure
class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)


# Matplotlib widget
class MplWidget(QtWidgets.QWidget):
    sigMouseClicked = Signal(object)
    
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
        self.canvas = MplCanvas()                  # Create canvas object
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.toolbar)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

        self.im = None
        self.txt = None

    def plot(self, data, **kwargs):
        self.im = self.canvas.ax.imshow(data, **kwargs)
        self.txt = self.canvas.ax.set_title('t = 0')
        
        self.canvas.draw()

    def set_lims(self, xlims, ylims):
        self.canvas.ax.set_xlim(*xlims)
        self.canvas.ax.set_ylim(*ylims)

    def update(self, data, time, *args, auto_lims=True, **kwargs):
        self.im.set_data(data)
        self.txt.set_text(f't = {time:.3f}')
        if auto_lims:
            vmin = data.min()
            vmax = data.max()
            self.im.set_clim(vmin=vmin, vmax=vmax)

        self.canvas.draw()