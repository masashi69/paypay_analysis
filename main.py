from kivy.app import App
#from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
#from kivy.uix.button import Button
#from kivy.uix.widget import Widget
from kivy.config import Config
import os
import app
import sqlite3

class Main(Screen):

    def open(self, path, filename):
        with open(os.path.join(path, filename[0]), encoding='utf-8-sig') as f:
            csvfile = f.readlines()

        return csvfile

    def createdb(self, afile):
        global cur

        con = sqlite3.connect(':memory:')
        cur = con.cursor()

        app.insertData(afile, cur)
        app.shapeingData(cur)

        con.close()

    pass

class Analized(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('my.kv')

class AnalizeApp(App):
    def build(self):

        return kv

if __name__ == '__main__':
    AnalizeApp().run()

