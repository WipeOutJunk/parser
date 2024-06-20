import os
import requests
from bs4 import BeautifulSoup
from get_recipe_details import get_recipe_details
import json
import subprocess
# Количество страниц
total_pages = 1

# Функция для извлечения URL рецептов с одной страницы
def get_recipe_urls(page_number):
    url = f'https://food.ru/recipes?page={page_number}'
    response = requests.get(url)
    recipe_urls = []
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        recipe_links = soup.find_all('a', class_='card_card__YG0I9')
        recipe_urls = ['https://food.ru' + link['href'] for link in recipe_links]
    else:
        print(f"Не удалось получить доступ к странице {page_number}. Статус-код: {response.status_code}")
   
    return recipe_urls

# Главная логика
all_recipe_urls = []

for page in range(1, total_pages + 1):
    print(f"Извлечение рецептов со страницы {page}")
    page_recipe_urls = get_recipe_urls(page)
    all_recipe_urls.extend(page_recipe_urls)

print(f"Всего найдено рецептов: {len(all_recipe_urls)}")

# Извлечение информации для каждого рецепта
all_recipe_details = []
for recipe_url in all_recipe_urls:
    details = get_recipe_details(recipe_url)
    if details:
        # print(json.dumps(details, indent=4, ensure_ascii=False)) // вывод в консоль
        all_recipe_details.append(details)

# Сохранение данных в JSON-файл
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "recipes.json")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_recipe_details, f, ensure_ascii=False, indent=4)

print(f"Данные сохранены в {output_file}, внутри {output_dir}")
# Запрос подтверждения перед отправкой данных в базу данных
confirm = input("Вы уверены, что хотите отправить данные в базу данных? (y/n): ").strip().lower()
if confirm == 'y':
    result = subprocess.run(['python', 'upload_to_db.py'], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
else:
    print("Отправка данных в базу данных отменена.")