import requests
from bs4 import BeautifulSoup
from get_recipe_details import get_recipe_details
import json

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
for recipe_url in all_recipe_urls:
    details = get_recipe_details(recipe_url)
    if details:
        print(json.dumps(details, indent=4, ensure_ascii=False))
