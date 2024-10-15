import sqlite3
import json

def fetch_data_from_db(db_path):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM songs")
    rows = cursor.fetchall()
    
    # Получаем названия колонок
    column_names = [description[0] for description in cursor.description]
    
    # Преобразуем данные в список словарей
    data = [dict(zip(column_names, row)) for row in rows]
    print(data)
    conn.close()
    return data

def convert_data_to_json(data):
    return json.dumps(data, indent=4)

if __name__ == "__main__":
    db_path = 'your_database.db'
    data = fetch_data_from_db(db_path)
    json_data = convert_data_to_json(data)
    
    # Сохраняем JSON данные в файл
    # with open('data.json', 'w') as json_file:
    #     json_file.write(json_data)
    
    # print("Данные успешно сохранены в JSON файл.")