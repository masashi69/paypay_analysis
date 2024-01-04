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
import japanize_kivy

class Main(Screen):

    def open(self, path, filename):
        with open(os.path.join(path, filename[0]), encoding='utf-8-sig') as f:
            csvfile = f.readlines()

        return csvfile

    def createdb(self, afile):
        con = sqlite3.connect(':memory:')
        cur = con.cursor()

        app.insertData(afile, cur)
        #selected = app.shapeingData(cur)
        cur.execute('SELECT "利用日/キャンセル日", "利用店名・商品名", sum("支払総額"), \
                 count("利用店名・商品名") FROM pay GROUP BY "利用日/キャンセル日", \
                 "利用店名・商品名" ORDER BY "利用日/キャンセル日"')

        res = ''
        for x in cur.fetchall():
            res += f'{x[0]} {x[1]} {x[2]} {x[3]}\n'

        self.manager.get_screen('analize').ids.result.text = res

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

