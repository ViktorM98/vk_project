
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import os
import hashlib
from sqlite import *
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
        
        #Регистрация(вставить своё)
        with open('D:\\Projects/verification.txt', 'r') as file:
            lines = file.readlines()
            gmail = lines[0]  # prints the second line
            password = lines[1]

        self.gmail = gmail
        self.password = password
        
        self.authorization_vk()
        #self.open_vk()
        # self.music_on()
        # self.take_music()
    
    def start_connection(self):
        self.connection = sqlite3.connect("vk.db")
        self.cursor = self.connection.cursor()
    
    def close_connection(self):
        self.connection.close()
    
    #cookie
    def authorization_vk(self):
        print("---def authorization_vk---")
    #    self.driver.maximize_window()
        self.driver.get("https://vk.com")
        sleep(1)
        index_email = self.driver.find_element(By.ID, "index_email" )
        index_email.send_keys(self.gmail)
        index_email.send_keys(Keys.ENTER)
        sleep(6)

        self.driver.find_element('xpath',  "//button[@data-test-id='other-verification-methods']").click()
        sleep(1.5)

        self.driver.find_element('xpath',  "//div[@data-test-id='verificationMethod_password']").click()
    
        password_name = self.driver.find_element(By.NAME, "password") 
        password_name.send_keys(self.password)
        password_name.send_keys(Keys.ENTER)

        

        sleep(3)
        #print("300 сек прошло")
        pickle.dump(self.driver.get_cookies(), open("Сookies", "wb"))
        print("куки сохранены")
        #sleep(3)
        

    #Открыть вк через куки
    def open_vk(self):
        print("start")
        self.driver.get("https://vk.com")
        self.driver.delete_all_cookies()
        try:
            for cookies in pickle.load(open("Сookies", "rb")):
                self.driver.add_cookie(cookies)
            print("загрузка завершена")
        except:
            print("Cookie error")
               
        
        sleep(2)
        self.driver.refresh()
        print("готово")
        #sleep(4)
        

    #взять значения музыки
    def get_music(self):
        print("---def get_music---")
        self.driver.get("https://vk.com/id0")
        sleep(1)
        self.personal_id = self.driver.find_element(By.ID, "top_profile_link")
        sleep(1)
        self.driver.get(f"https://vk.com/audios{self.personal_id}")
        print(self.personal_id)
        sleep(1)
    
    
        
    #Переход в аудиозаписи
    def music_on(self):
        print("music_on start")
        music = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Музыка")

        music.click()
        print("click")
        sleep(4)

        my_music = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Моя музыка").click()
  
        sleep(2)

        self.driver.execute_script("window.scrollBy(0,550)")
        sleep(1)
        # random = self.driver.find_element(By.CLASS_NAME, "audio_page__shuffle_all_button").click()
    
    #переход во все плейлисты
    def playlist_on(self):
        print("playlist")
        all_playlists = self.driver.find_element(By.CSS_SELECTOR, ".CatalogBlock__recent_audios_header .audio_page_block__show_all_link")
        if all_playlists:
            all_playlists.click()
        else:
            print("Элемент не найден")
    
    #Взять информацию обо всех плейлистах
    def information_about_playlists(self):
        all_playlists = self.driver.find_elements(By.CSS_SELECTOR, "._audio_page__playlists .ui_gallery_item")
        for element in all_playlists:
            attr_value = element.get_attribute("data-full-id").split('_')
            id = int(attr_value[1])
        playlists_name = [element.find_element(By.TAG_NAME, "a") for element in all_playlists]    
        for playlist in playlists_name:
            print(playlist.text)

    def playlist_database(self):
        playlists = self.driver.find_elements(By.CSS_SELECTOR, ".CatalogBlock__my_playlists .ui_gallery_item")
        
      
            
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
            
            
    #Добавить плейлист
    def add_playlist(self):
        print("adding playlist")
        add_playlist = self.driver.find_element(By.CSS_SELECTOR, ".audio_page__add_playlist_btn")
        self.driver.execute_script("arguments[0].click();", add_playlist)

        def name_assign():
            print("name_assigning")
            playlist_name = "ljlj"
            name_assign = self.driver.find_element(By.ID, "ape_pl_name")
            name_assign.send_keys(playlist_name)
            print("done")

        def add_songs_into_playlist():
            print("переход в добавление песен в плейлист")
            self.driver.find_element(By.ID, "ape_add_audios_btn").click()
            #self.driver.execute_script("arguments[0].click();", add_songs_btn)

        def get_songs():
            print("def get_songs")
            sleep(0.8)
            self.scroll_item()
            playlist_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.ape_item_list .audio_row")
            if len(playlist_elements) > 0:
                for x in playlist_elements:
                    attr_value = x.get_attribute("data-full-id").split("_")
                    #print(attr_value)
                print("end get songs")
            else:
                print("elements = 0")
            #print(playlist_elements)
        #def select_song(song_id):
            
        name_assign()
        add_songs_into_playlist()
        get_songs()

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
    
    def take_music(self):

        print("--find music--")
        self.scroll()
        sleep(2)
        self.elements = self.driver.find_elements(By.CSS_SELECTOR, "div.CatalogSection__columns .audio_row") # Название песни, группа, пролоджительность
        
        

        # for x in elem:
        #     attr_value = x.get_attribute("data-full-id").split('_')
        #     id = int(attr_value[1])
            
        #     info = x.text.split('\n')
        #     # info.append(attr_value)

        #     music_info_tuple = (id,info[0],info[1])
        #     vk_database.insert(music_info_tuple[0], music_info_tuple[1],music_info_tuple[2])
        #     # music_info.append(music_info_tuple)
        #     print(music_info_tuple)

    #
    def drop_database(self):
        self.cursor.execute("DROP TABLE songs")
    
    def send_music(self):

        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS songs (
                        song_id TEXT,
                        music_group TEXT,
                        music_name TEXT,
                        lenght TEXT
        )""")
        #Проверка существующей таблицы
        self.cursor.execute('SELECT 1 FROM songs LIMIT 1')
        if self.cursor.fetchone() is None:
            print('Таблица пустая')
            comparing_result = self.comparing_music(self.elements, self.cursor.execute("""SELECT * FROM songs""").fetchall())
            print("Comparing_result:", comparing_result)
            #Если данныхе из сущестующей таблицы не равны данным с сайта
            if  comparing_result == False:
                print("return FALSE")
                #self.db_create

                self.cursor.execute("BEGIN")
                print("BEGIN")
                for x in self.elements:
                    try:
                        attr_value = x.get_attribute("data-full-id").split('_')
                        id = int(attr_value[1])
                        
                        info = x.text.split('\n')
                        if len(info) >= 3:
                            music_info_tuple = (id,info[0], info[1], info[2])
                            self.cursor.execute("INSERT INTO songs VALUES(?,?,?,?)",(music_info_tuple[0],music_info_tuple[1],music_info_tuple[2],music_info_tuple[3]))
                            print(music_info_tuple)
                            
                        else:
                            print("Недостаточно инормации для песни:", info)

                    except:
                        self.cursor.execute("ROLLBACK")
                        print("Ошибка")
                else:
                    self.cursor.execute("COMMIT")
                    print("Добавлено в базу данных")

        else:
            print('Таблица не пустая')
        print("добавление завершено")
    
    #Проверка бд на изменения
    def comparing_music(self, data_from_site, data_from_table):
        #Сравнение хеша столбца сайта и хеша столбца базы данных
        # for row_from_site, row_from_table in zip(data_from_site, data_from_table):
        #     hash_from_site = hashlib.md5(str(row_from_site).encode()).hexdigest()
        #     hash_from_table = hashlib.md5(str(row_from_table).encode()).hexdigest()
        #     if hash_from_table != hash_from_site:
        #         return False
        #     else:
        #         print("data from site = data from table")
        #         return True
            
        return False
                    
    # def db_create(self):
    #     with sqlite3.connect("vk.db") as con:
    #         self.cursor = con.cursor()

    #         self.cursor.execute("""CREATE TABLE IF NOT EXISTS songs (
    #             song_id TEXT PRIMARY KEY,
    #             song_info TEXT NOT NULL
    #             length TEXT NOT NULL
    #         )
    #         """)
    

    def scroll(self):
    
        last_height = self.driver.execute_script("return document.body.scrollHeight") 
        while True: 
            # Прокрутка вниз 
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
            # Пауза, пока загрузится страница. 
            sleep(0.5)
            # Вычисляем новую высоту прокрутки и сравниваем с последней высотой прокрутки. 
            new_height = self.driver.execute_script("return document.body.scrollHeight") 
            if new_height == last_height: 
                break 
                
            last_height = new_height
            # print("Появился новый контент, прокручиваем дальше")
    
        print("Прокрутка завершена") 



    def pause(self):
        self.driver.find_element('xpath',  "//button[@class='top_audio_player_btn top_audio_player_play _top_audio_player_play']").click()

    def start_song(self,music_id):
        try:
            button = self.driver.find_element(By.CSS_SELECTOR, f"div.CatalogSection__columns  ._audio_row_299606378_{music_id} ._audio_row__play_btn")
            self.driver.execute_script("arguments[0].click();", button)
        
        except Exception:
            print("error")

        #print(By.CSS_SELECTOR, f"div.CatalogSection__columns .{self.personal_id}_456239999 .audio_row_play_pause_button")

    def next(self):
        self.driver.find_element('xpath',  "//button[@class='top_audio_player_btn top_audio_player_next']").click()

    def on_start(self):  
        self.driver.find_element('xpath',  "//button[@class='top_audio_player_btn top_audio_player_play _top_audio_player_play']").click()
    
    def prev(self):
        print('start music')
        prev = self.driver.find_element('xpath',  "//button[@class='top_audio_player_btn top_audio_player_prev']").click()
        prev.click()
        sleep(0.8)
        prev.click()


if __name__ == "__main__":
    music = audio_vk()
    
    music.open_vk()
    music.music_on()
    #music.add_playlist()
    music.start_connection()
    #music.playlist_database()
    #music.playlist_on()
    #загрузка музыки в дб
    music.drop_database()
    music.take_music()
    music.send_music()

    #music.start_song()
    music.close_connection()
    sleep(100000)
    exit()