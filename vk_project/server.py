import socket
import threading 
import time
import json
import sqlite3
import os
from vk_musc import audio_vk

HEADER = 64
PORT = 5050 
#SERVER = "192.168.0.102"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT" 

print(SERVER)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
class MyServer():

    def __init__(self):
        self.vk = None
        

    #старт потоков файла вк, запуска сервера
    def start_threads(self):
        print("Запуск задач...")
        thread_one = threading.Thread(target=self.create_vk_instance)
        thread_two = threading.Thread(target=self.start_server)
        
        thread_one.start()
        thread_two.start()


    def create_vk_instance(self):
        print("создание экземпляра VK...")
        self.vk = audio_vk()
        self.vk.open_vk()
        self.vk.music_on()
        self.vk.take_music()
        print("вк запущен..")
    
    
    def get_id_music_from_db(self,cursor, count):
        
        cursor.execute("SELECT * FROM songs")
        data = cursor.fetchall()
        # Проверяем, что индекс находится в пределах списка
        if 0 <= count < len(data):
            print("music_id:", data[count][0])
            return data[count][0]
            
        else:
            return None  
    
    def get_data_from_db(self,cursor,count):
        return cursor.execute(f"SELECT * FROM songs LIMIT 6 OFFSET {count}").fetchall()

                           
        
    # Получение сообщение, определение типа
    def handle_client(self, conn, addr):
        db_path = 'vk.db'

        if not os.path.exists(db_path):
            print(f"[ERROR] {db_path} does not exist. Closing connection.")
            conn.send(json.dumps({"status": "error", "message": f"{db_path} does not exist."}).encode(FORMAT))
            conn.close()
            return
        

        db_connection = sqlite3.connect(db_path)
        cursor = db_connection.cursor()
        
        print(f"[NEW CONNECTION] {addr} connected.")
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

        connected = True
        while connected:
            msg_lenght = conn.recv(HEADER).decode(FORMAT)
            if msg_lenght:
                print("got message")
                msg_lenght = int(msg_lenght)
                msg = conn.recv(msg_lenght).decode(FORMAT)
                print(msg)
                #self.song_id = msg
                #self.vk.start_song(self.song_id)
                msg = json.loads(msg)
                #Если тип get_id_music, то 
                if msg['type'] == 'get_id_music':
                    print("got_message and decode it")
                    count =  int(msg['count'])

                    data = self.get_id_music_from_db(cursor,count)
                    if self.vk != None:
                        self.vk.start_song(data)
                    response = json.dumps(data)
                    conn.send(response.encode(FORMAT))
                    print("response:", response)
                    
                elif msg['type'] == 'get_music_data':
                    print("Got music_data")
                    count = int(msg['count'])
                    #получение из базы данных 6 песен и отправка их ответом
                    data = self.get_data_from_db(cursor,count)
                    response = json.dumps({"status": "success", "data":data})

                    print(response)
                    print("кол-во байт:", len(response))


                elif msg == DISCONNECT_MESSAGE:
                    connected = False
                    print(f"[{addr}] {msg}")
                else:       
                    print("Ошибка")
                    conn.close()
                    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
            
                conn.send(response.encode(FORMAT))
        
        #conn.send(response.encode(FORMAT))
        conn.close()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    def play_music():
        print('fds')

    #Старт сервера
    def start_server(self):
        server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
            
            
if __name__=="__main__":
    print("[STARTING] SERVER IS STARTING...")
    server_instance = MyServer()
    #server_instance.start_threads()
    server_instance.start_server()
