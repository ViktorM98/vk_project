from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import TwoLineListItem
import database_connector as db
import memory_database as memory_db
from client import client
from time import sleep
from kivy.properties import NumericProperty
import json

class ScreenManager(ScreenManager):
    pass


class MainScreen(Screen):
    # def build(self):
    #     self.theme_cls.theme_style = "Dark"
    pass 
    



class ListScreen(Screen):
    load_more_trigger = NumericProperty(0) 
    
    
    def on_enter(self):
        self.client = client()

        #Вывести все песни
        #self.musics = db.get_data()
        self.ids.scroll_view.bind(scroll_y=self.check_scroll_y)
        self.i = 6
        self.load_data(self.i)
       # client_instanse = client()
       
    def load_data(self,count):
        musics = self.client.send_data_request(count)
        for music in musics:
            self.add_music_item(music)
        
    def add_music_item(self, music):
        
        self.ids.container.add_widget(
                TwoLineListItem(
                    id = str(music[0]),
                    text = f"{music[1]}",
                    secondary_text = f"{music[2]}",
                    #on_release = lambda x: client_instanse.send(str(x.id))ё
                )
            )
        
    def check_scroll_y(self,instance, value):
        if value <= self.load_more_trigger:
            self.load_more_data()
            self.i+=6
            print(self.i)
            sleep(1)

    def load_more_data(self):
        #Запрос списка музыки из сервера 
        new_musics = memory_db.read_more_data(self.i)
        #new_musics = memory_db.get_more_data(self.i)  # Получаем новые данные
        #musics = self.client.send_more_data_request(count)
        for music in new_musics:
            self.add_music_item(music)
        # Обновляем список musics, если это необходимо
        self.musics.extend(new_musics)

# class PlaylistScreen(Screen):

            

class MainApp(MDApp):
    def build(self):
        return ScreenManager()
    
    
if __name__ == "__main__":
    MainApp().run()
    #client