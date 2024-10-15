from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import TwoLineListItem
import database_connector as db
#from client import client

class ScreenManager(ScreenManager):
    pass

class MainScreen(Screen):
    pass

class ListScreen(Screen):
    
    def on_enter(self):
        # Создаем ScrollView и BoxLayout для содержимого
        scroll_view = ScrollView()
        content_box = BoxLayout(orientation='vertical', size_hint_y=None)
        content_box.bind(minimum_height=content_box.setter('height'))
        
        # Добавляем BoxLayout в ScrollView
        scroll_view.add_widget(content_box)
        self.add_widget(scroll_view)
        
        # Загружаем начальный набор данных
        self.load_more_data(content_box)

        # Привязываем метод load_more_data к событию прокрутки
        scroll_view.bind(scroll_y=self.check_scroll)

    def check_scroll(self, instance, value):
        # Проверяем, достигли ли мы конца ScrollView
        if value <= 0.1:  # Можно настроить пороговое значение
            self.load_more_data(instance.children[0])

    def load_more_data(self, box_layout):
        # Получаем данные из базы данных
        musics = db.run_process()
        
        
        # Добавляем элементы в BoxLayout
        for music in musics:
            box_layout.add_widget(
                TwoLineListItem(
                    id=str(music[0]),
                    text=f"{music[1]}",
                    secondary_text=f"{music[2]}",
                   # on_release=lambda x: client_instance.send(str(x.id))
                )
            )

class MainApp(MDApp):
    def build(self):
        return ScreenManager()

if __name__ == "__main__":
    MainApp().run()