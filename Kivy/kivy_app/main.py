from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import TwoLineListItem
import database_connector as db
import memory_database as mem_db
from client import client
from time import sleep
from kivy.properties import NumericProperty
import json

kivy_client = None

def init_kivy_client():
    global kivy_client
    kivy_client = client()

class ListScreen(Screen):
    load_more_trigger = NumericProperty(0.1) 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = kivy_client
        
    
    def on_enter(self):
        
        #Вывести все песни
        #self.musics = db.get_data()
        self.ids.scroll_view.bind(scroll_y=self.check_scroll_y)
        self.i = 0
        self.load_data(self.i)
        print("Загрузка даты в 1й раз")
       
    #Запрос на загрузку музыки с сервера  
    def load_data(self,count):
        print("def load_data started")
        self.client.send_data_request("get_music_data",count,callback=self.read_data_from_memdb )
        # musics = mem_db.read_more_data(self.i)
        # if musics:
        #     print("Элементы имеются")
        # else:
        #     print("Ничего нету в musics")
        # for music in musics:
        #     self.add_music_item(music)
        print("musics added")
        
    def add_music_item(self, music):
        print("ADDING MUSIC",music[0],music[2],music[3])
        self.ids.container.add_widget(
                TwoLineListItem(
                    id = str(music[0]),
                    text = f"{music[1]}",
                    secondary_text = f"{music[2]}",
                    #on_release = lambda x: client_instanse.send(str(x.id))
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
        self.client.send_data_request("get_music_data",self.i, callback=self.read_data_from_memdb)
    
    def read_data_from_memdb(self):
        print("start read_data_from_memdb")
        new_musics = mem_db.read_more_data(self.i)
        if new_musics:
            print("NEWMUSICS EXISTS")
        else:
            print("NEW_MUSICS нету")
        #new_musics = memory_db.get_more_data(self.i)  # Получаем новые данные
        #musics = self.client.send_more_data_request(count)
        for music in new_musics:
            self.add_music_item(music)
            print("adding music:", music)
        # Обновляем список musics, если это необходимо
        #self.musics.extend(new_musics)

class PlaylistsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    


class ScreenManager(ScreenManager):
    pass


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = kivy_client
        
        
              
class MainApp(MDApp):
    def build(self):
        init_kivy_client()
        self.manager = ScreenManager()
        self.manager.add_widget(MainScreen(name='main'))
        self.manager.add_widget(ListScreen(name='list'))
        self.manager.add_widget(PlaylistsScreen(name='playlists'))
        return self.manager

    
if __name__ == "__main__":
    MainApp().run()
    #client