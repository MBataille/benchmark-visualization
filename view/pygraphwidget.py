from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Signal
import pyqtgraph as pg

class GraphWidget(QWidget):
    sigMouseClicked = Signal(object)
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.vbl = QVBoxLayout()
        self.image_widget = pg.ImageView()
        self.image_widget.scene.sigMouseClicked.connect(self.mouse_clicked)
        self.viewbox = self.image_widget.getView()
        self.imageitem = self.image_widget.imageItem 
        self.txt = pg.TextItem('t = 0', anchor=(0.1, 0.1))
        self.viewbox.addItem(self.txt)
        self.cm = pg.colormap.get('viridis')
        self.image_widget.setColorMap(self.cm)
        
        self.vbl.addWidget(self.image_widget)
        self.setLayout(self.vbl)
        
        self.image_widget.show()
        
    def plot(self, data, **kwargs):
        self.image_widget.setImage(data, **kwargs)
        
    def update(self, data, time):
        self.image_widget.setImage(data)
        self.image_widget.autoLevels()
        self.txt.setText(f't = {time:.3f}')

    def mouse_clicked(self, mouseClickEvent):
        scene_pos = mouseClickEvent.scenePos()
        if self.imageitem.sceneBoundingRect().contains(scene_pos):
            coords = self.viewbox.mapSceneToView(scene_pos)
            self.sigMouseClicked.emit(coords)
