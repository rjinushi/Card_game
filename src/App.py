import pyxel
from src.settings import *

class App:
    def __init__(self):
        pyxel.init(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, fps=FPS, title=TITLE)
        pyxel.load("../assets/my_resource.pyxres")
        
        pyxel.run(self.update, self.draw)
        
    def update(self):
        pass
    
    def draw(self):
        pyxel.cls(0)