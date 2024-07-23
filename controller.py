import time
from PySide6.QtCore import QThread, Signal, QObject, Slot, Signal
from PySide6.QtWidgets import QWidget
import numpy as np

class EquationWorker(QObject):
    update_signal = Signal(object)
    
    def __init__(self, equation):
        super().__init__()
        self.equation = equation
        self._running = False
    
    def start(self):
        self._running = True
        while self._running:
            # t0 = time.time()
            self.equation.step()
            # print(f'took {(time.time() - t0)*1e3:.2f} ms')
            data = self.equation.get_current_state()
            t = self.equation.get_current_time()
            self.update_signal.emit((data, t))
            # QThread.msleep(5)  # Sleep to control the update rate
    
    def stop(self):
        self._running = False
        
    @Slot(object)
    def change_intial_condition(self, initial_fields):
        self.equation.set_initial_condition(initial_fields)
        
        
class Controller(QWidget):
    sigInitCondChanged = Signal(object)
    
    def __init__(self, equation, gui=None):
        super().__init__()
        self.equation = equation
        self.gui = gui
        self.thread = None
        self.worker = None
        
    def set_gui(self, gui):
        self.gui = gui
        
    def start_thread(self):
        self.thread = QThread()
        self.worker = EquationWorker(self.equation)
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.start)
        self.worker.update_signal.connect(self.gui.update_plot)
        self.sigInitCondChanged.connect(self.worker.change_intial_condition)
        self.thread.start()
        
    def stop_thread(self):
        if self.worker:
            self.worker.stop()
        if self.thread:
            self.thread.quit()
            self.thread.wait()
        self.worker = None
        self.thread = None
        
    # def update(self):
    #     # t0 = time.time()
    #     self.equation.step()
    #     # print(f'One step took {(time.time()-t0)*1e3:.2f} ms')
        
    #     data = self.equation.get_current_state()
    #     t = self.equation.get_current_time()
        
    #     self.gui.update_plot(data, t)
        
    def set_data(self, new_data):
        self.equation.set_intial_condition(new_data)
        
    def get_initial_data(self):
        return self.equation.get_initial_condition()
    
    @Slot(object)
    def on_mouse_click(self, coords):
        x, y = coords.x(), coords.y()
        fields = self.equation.get_current_state()
        radius = 20
        N = self.equation.N
        j, i = int(np.round(x)), int(np.round(y))
        js = np.arange(N)
        I, J = np.meshgrid(js, js)
        for k in range(len(fields)):
            cond = (((I - i)) ** 2 + ((J - j)) ** 2) < radius ** 2
            fields[k][cond] = 0

        self.sigInitCondChanged.emit(fields)
        print(f'{x} {y}')