from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import hashlib
import sqlite3
import os
from time import sleep
import pickle

class audio_vk():
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        #self.options.set_preference("general.useragent.override",\
        #"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")

        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
        
        #self.options.add_argument("--headless")
        #self.options.add_argument('--ignore-certificate-errors')
        self.service = Service(executable_patch=ChromeDriverManager().install() )
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.get("D:\my_music.html")

    
    def start_connection(self):
        self.connection = sqlite3.connect("vk.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("DROP TABLE IF EXISTS playlists")
    
    def close_connection(self):
        self.connection.close()

    def playlist_database(self):
            playlists = self.driver.find_elements(By.CSS_SELECTOR, ".CatalogBlock__my_playlists .ui_gallery_item")
            for x in playlists:
                print(x.text)
            
            def create_playlist_db():
                self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS playlists(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL
                )
                """)
                print("playlists db created")
                #Добавление id и заголовка плейлиста
                for element_id in playlists:
                    element = element_id.find_element(By.CSS_SELECTOR, ".audio_pl_item2 ")
                    playlist_id = element.get_attribute("data-id").split('_')
                    id = int(playlist_id[1])
                    title = element_id.find_element(By.CSS_SELECTOR, "a.audio_item__title").text
                    self.cursor.execute("INSERT INTO playlists VALUES(?,?)",(id,title))
                    print(id,title, "added")
                self.cursor.execute("COMMIT")

            
            def create_playlist_songs():
                self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS playlist_songs(
                playlist_id INTEGER NOT NULL,
                song_id INTEGER NOT NULL,
                PRIMARY KEY(playlist_id,song_id),
                FOREIGN KEY (playlist_id) REFERENCES playlists(id)
                FOREIGN KEY (song_id) REFERENCES songs(id)
                )            
                """)
                print("playlist_songs db created")
            #Добавление id плейлиста и id песен из плейлиста
            def add_songs_into_playlist(playlist_id):
                for element in playlists:
                    
                    element_id = element.find_element(By.CSS_SELECTOR, "div.audio_pl_item2").get_attribute("data-id").split('_')
                    print(int(element_id[1]))
                    element_id = int(element_id[1])

                    if element_id == playlist_id:
                        print("Найдено")
                        named_element = element.find_element(By.CSS_SELECTOR, "a[href]")
                        named_element.click()
                        playlist_element = self.driver.find_elements(By.CSS_SELECTOR, ".AudioPlaylistSnippet__actionButton")
                        if playlist_element:
                            playlist_element[0].click()    
                             
                        break
                    else:
                        print("не найдено")
                playlist_songs = self.driver.find_elements(By.CSS_SELECTOR, ".AudioPlaylistSnippet__list .audio_row")
                #   
                #Проверка есть ли уже записи заданного плейлиста
                self.cursor.execute("SELECT COUNT(*) FROM playlist_songs WHERE playlist_id = ?", (playlist_id,))
                check_count_playlist = self.cursor.fetchone()
                print(check_count_playlist[0])
                if check_count_playlist[0] != len(playlist_songs):
                    print("Плейлиста нету в базе данных")
                    for x in playlist_songs:
                        # print(x.text)
                        try: 
                            self.cursor.execute("BEGIN TRANSACTION")
                            print("begin transaction")
                            attr_value = x.get_attribute("data-full-id").split('_')
                            song_id = int(attr_value[1])
                            self.cursor.execute("INSERT INTO playlist_songs VALUES(?,?)",(playlist_id,song_id))
                            print("add id ", song_id, "at", playlist_id)

                            self.cursor.execute("COMMIT")
                            print("Добавлено в базу данных")
                        except:
                            self.cursor.execute("ROLLBACK")
                            print("Ошибка")    
                else:
                    print("плейлист уже есть в базе")            

            create_playlist_db()
            create_playlist_songs()
            add_songs_into_playlist(60542045)

    def scroll_playlist(self):
        list_container = self.driver.find_element(By.CSS_SELECTOR, ".audio_pl_snippet__list")
        last_item_count = 0
        while True:
            items = list_container.find_elements(By.CSS_SELECTOR, ".audio_row")
            current_item_count = len(items)
            print(current_item_count)

            if current_item_count == last_item_count:
                print("все")
                break

            # Scroll down to the last item
            last_item = items[-1]
            actions = ActionChains(self.driver)
            actions.move_to_element(last_item).perform()
            actions.click_and_hold(list_container).move_by_offset(0, 280).release().perform()
            #actions.click_and_hold(list_container).move_by_offset(0, 200).release().perform()
            #actions.click_and_hold(list_container).move_by_offset(0, 100).release().perform()
            print("пролистано")
            #actions.move_t

            sleep(0.7)
            # Update the last item count
            last_item_count = current_item_count


    def scroll_item(self):

        list_container = self.driver.find_element(By.CSS_SELECTOR, ".ape_item_list")
        last_item_count = 0

        while True:
            items = list_container.find_elements(By.CSS_SELECTOR, "._ape_audio_item")
            current_item_count = len(items)
            print(current_item_count)

            if current_item_count == last_item_count:
                print("все")
                break

            # Scroll down to the last item
            last_item = items[-1]
            actions = ActionChains(self.driver)
            actions.move_to_element(last_item).perform()
            actions.click_and_hold(list_container).move_by_offset(0, 280).release().perform()
            actions.click_and_hold(list_container).move_by_offset(0, 200).release().perform()
            actions.click_and_hold(list_container).move_by_offset(0, 100).release().perform()
            print("пролистано")
            #actions.move_t

            sleep(0.7)
            # Update the last item count
            last_item_count = current_item_count


music = audio_vk()
music.start_connection()
music.playlist_database()
#music.add_playlist
sleep(3000)
