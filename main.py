from kivy.garden.iconfonts import register
from app import MainApp

from os.path import join, dirname
import sys

register('matIcons', join(dirname(__file__), 'app/assets/fonts/Material-Design-Iconic-Font.ttf'), join(dirname(__file__), 'app/assets/fonts/zmd.fontd'))

MainApp().run()
