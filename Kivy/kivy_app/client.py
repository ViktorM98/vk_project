import socket 
import json
import memory_database as mem_db
from time import sleep

HEADER = 64
PORT = 5050 
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

class client():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        print("connection succseed")
        mem_db.memory_database_init()


    # Отправка ID музыки для проигрывания
    def send_data_request(self,type, count, callback):
        request = json.dumps({"type": f"{type}","count": f"{count}"})
        message = request.encode(FORMAT)
        
        # Получаем длину сообщения и кодируем ее
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))

        self.client.send(send_length)

        self.client.send(request.encode(FORMAT))
        print(request)
        print("request sended")
        response = self.client.recv(1024).decode(FORMAT)
        data = json.loads(response)
        
        if data ['status'] == 'success':
            mem_db.add_data(data['data'])
            print("Got data from SERVER:", data['data'] )
            callback()
        
        elif data ['status'] == 'error':
            print(['message'])
            print("нету vk.db")
    
        else:
            print('ошибка получения данных')
            
        #print("data from server",json.dumps(data,indent=2))
        


        # message = msg.encode(FORMAT)  
        # msg_length = len(message)
        # send_length = str(msg_length).encode(FORMAT)
        # send_length += b' ' * (HEADER - len(send_length))
        # self.client.send(send_length)
        # self.client.send(message)
    # def send_more_data_request(self,count):
    #     request =

    #def database_request()
        
    def disconnect(self):
        self.client.send(DISCONNECT_MESSAGE.encode(FORMAT))
        self.client.close()
        print("Disconnected from server")
    
if __name__ == "__main__": 
    myclient = client()
    myclient.send_data_request("get_music_data",1)
    