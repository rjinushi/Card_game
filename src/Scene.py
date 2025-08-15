import pyxel

class Scene:
    def __init__(self, app):
        self.app = app
        
    def update(self):
        pass
    
    def draw(self):
        pyxel.cls(0)
    
class TitleScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        
    def update(self):
        super().update()
    
    def draw(self):
        super().draw()

class GameScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        
    def update(self):
        super().update()
    
    def draw(self):
        super().draw()

class ResultScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        
    def update(self):
        super().update()
    
    def draw(self):
        super().draw()