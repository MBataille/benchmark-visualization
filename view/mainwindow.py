from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import QTimer, QThread
import matplotlib.pyplot as plt
from view.mplwidget import MplWidget
from view.pygraphwidget import GraphWidget

class GUI(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
        
    def init_ui(self):
        self.layout = QVBoxLayout()
        
        self.plot_button = QPushButton('Start simulation')
        self.plot_button.clicked.connect(self.start_plotting)
        
        self.stop_button = QPushButton('Stop Plotting')
        self.stop_button.clicked.connect(self.stop_plotting)
        self.stop_button.setEnabled(False)
        
        # self.mainplot = MplWidget()
        self.mainplot = GraphWidget()
        self.mainplot.sigMouseClicked.connect(self.controller.on_mouse_click)
        
        self.layout.addWidget(self.mainplot)
        self.layout.addWidget(self.plot_button)
        self.layout.addWidget(self.stop_button)
        
        self.mainplot.plot(self.controller.get_initial_data()[0])
        
        self.setLayout(self.layout)
        
    def update_plot(self, vals):
        fields, time = vals
        self.mainplot.update(fields[0], time)
        
    def start_plotting(self):
        self.controller.start_thread()
        self.plot_button.setEnabled(False)
        self.stop_button.setEnabled(True)
    
    def stop_plotting(self):
        self.controller.stop_thread()
        self.plot_button.setEnabled(True)
        self.stop_button.setEnabled(False)