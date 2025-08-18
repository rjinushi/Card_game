import pyxel
from src.settings import *
from src.Scene import *

class App:
    def __init__(self):
        pyxel.init(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, fps=FPS, title=TITLE)
        pyxel.load("../assets/my_resource.pyxres")
        self.scene = dict()
        self.scene["title"] = TitleScene(self)
        self.scene["game"] = GameScene(self)
        self.scene["result"] = ResultScene(self)
        
        self.current_scene = self.scene["game"]
        
        pyxel.mouse(True)
        
        pyxel.run(self.update, self.draw)
        
    def update(self):
        self.current_scene.update()
    
    def draw(self):
        pyxel.cls(0)
        self.current_scene.draw()