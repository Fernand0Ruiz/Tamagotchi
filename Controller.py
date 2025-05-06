from View import View

class Controller: 
    def __init__(self):
        self.view = View()
        self.model = Model()

    def run(self):
        self.view.run()


