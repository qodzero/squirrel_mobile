from .view import MainWindow
from kivy.app import App

class MainApp(App):
    def build(self):
        return MainWindow()
