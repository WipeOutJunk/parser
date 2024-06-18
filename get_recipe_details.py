import requests
from bs4 import BeautifulSoup

def get_recipe_details(recipe_url):
    response = requests.get(recipe_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Извлекаем название рецепта
        title = soup.find('h1', class_='title_main__ok7t1').text.strip()

        # Извлекаем список ингредиентов
        ingredients_table = soup.find('table', class_='ingredientsTable_table__pamnR ingredientsCalculator_ingredientsTable__hwuQx')
        ingredients = ingredients_table.find_all('tr', class_='ingredient')

        ingredients_list = []
        for ingredient in ingredients:
            name_tag = ingredient.find('span', class_='name')
            name = name_tag.text.strip() if name_tag else 'Unknown'

            quantity_tag = ingredient.find('span', class_='value')
            quantity = quantity_tag.text.strip() if quantity_tag else 'Unknown'

            unit_tag = ingredient.find('span', class_='type')
            unit = unit_tag.text.strip() if unit_tag else 'Unknown'

            ingredients_list.append(f"{name}: {quantity} {unit}")

         # Извлекаем БЖУ и калории по атрибуту itemprop
        nutrition_info = {
            'calories': '',
            'proteins': '',
            'fats': '',
            'carbohydrates': ''
        }

        nutrition_info['calories'] = soup.find('div', itemprop='calories').find('span', class_='nutrient_value__dd48k').text.strip()
        nutrition_info['proteins'] = soup.find('div', itemprop='proteinContent').find('span', class_='nutrient_value__dd48k').text.strip()
        nutrition_info['fats'] = soup.find('div', itemprop='fatContent').find('span', class_='nutrient_value__dd48k').text.strip()
        nutrition_info['carbohydrates'] = soup.find('div', itemprop='carbohydrateContent').find('span', class_='nutrient_value__dd48k').text.strip()

        recipe_details = {
            'title': title,
            'ingredients': ingredients_list,
            'proteins': nutrition_info['proteins'],
            'fats': nutrition_info['fats'],
            'carbohydrates': nutrition_info['carbohydrates'],
            'calories': nutrition_info['calories']
        }


        return recipe_details
    else:
        print(f"Не удалось получить доступ к странице рецепта. Статус-код: {response.status_code}")
        return None
