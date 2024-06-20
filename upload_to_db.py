import psycopg2
import json
import os

def upload_to_db(json_file, db_config_file):
    # Загрузка конфигурации базы данных из файла
    with open(db_config_file, "r", encoding="utf-8") as f:
        db_config = json.load(f)

    # Создание подключения к базе данных
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Создание таблицы, если она не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id SERIAL PRIMARY KEY,
        title TEXT,
        title_img TEXT,
        description TEXT,
        ingredients JSONB,
        proteins TEXT,
        fats TEXT,
        carbohydrates TEXT,
        calories TEXT,
        instructions JSONB
    )
    ''')

    # Загрузка данных из JSON-файла
    with open(json_file, "r", encoding="utf-8") as f:
        recipes = json.load(f)

    # Вставка данных в таблицу
    for recipe in recipes:
        cursor.execute('''
        INSERT INTO recipes (title, title_img, description, ingredients, proteins, fats, carbohydrates, calories, instructions)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            recipe['title'],
            recipe['title_img'],
            recipe['description'],
            json.dumps(recipe['ingredients'], ensure_ascii=False),
            recipe['proteins'],
            recipe['fats'],
            recipe['carbohydrates'],
            recipe['calories'],
            json.dumps(recipe['instructions'], ensure_ascii=False)
        ))

    # Сохранение изменений и закрытие подключения
    conn.commit()
    cursor.close()
    conn.close()

    print(f"Данные успешно загружены в базу данных")

if __name__ == "__main__":
    json_file = os.path.join("output", "recipes.json")
    db_config_file = "db_config.json"
    upload_to_db(json_file, db_config_file)

