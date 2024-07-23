import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from controller import Controller
from equations.she import SwiftHohenberg
from equations.cgle import ComplexGinzburgLandau
from view.mainwindow import GUI

def main():
    app = QApplication()
    
    # equation = SwiftHohenberg()
    equation = ComplexGinzburgLandau()
    controller = Controller(equation, gui=None)
    gui = GUI(controller)
    controller.set_gui(gui)
    
    window = QMainWindow()
    window.setCentralWidget(gui)
    window.resize(800, 600)
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()