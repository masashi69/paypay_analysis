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
import japanize_matplotlib
import japanize_kivy
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
#matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')

class Main(Screen):

    def open(self, path, filename):
        with open(os.path.join(path, filename[0]), encoding='utf-8-sig') as f:
            csvfile = f.readlines()

        return csvfile

    def createdb(self, afile):
        con = sqlite3.connect(':memory:')
        cur = con.cursor()

        app.insertData(afile, cur)
        dates, contents, t = app.shapeingData(cur)

        res = ''
        for x in contents:
            res += f'{x[0]} {x[1]} {x[2]} {x[3]}\n'

        self.manager.get_screen('analize').ids.result.text = res

        p = app.createGraph(dates, cur)

        widget = FigureCanvasKivyAgg(p.gcf())

        self.manager.get_screen('analize').ids.plot.add_widget(widget)
        #ids.plot = p.show()
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

