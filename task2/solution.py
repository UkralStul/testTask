import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"

def get_animal_pages():
    # Словарь для хранения количества животных на каждую букву
    animal_counts = {}
    # Добавил счетчик страниц, чтобы пока скрипт выполняется не смотреть в пустой терминал
    page_count = 0

    next_page = BASE_URL
    while next_page:
        # Получаем данные с начальной страницы
        response = requests.get(next_page)
        if response.status_code != 200:
            print(f"Ошибка загрузки страницы: {next_page}")
            break

        soup = BeautifulSoup(response.content, "html.parser")

        groups = soup.select(".mw-category-columns ul li a")
        for link in groups:
            animal_name = link.text.strip()  # Название животного
            first_letter = animal_name[0].upper()  # Первая буква

            animal_counts[first_letter] = animal_counts.get(first_letter, 0) + 1

        # Поиск ссылки на следующую страницу
        next_link = soup.find("a", string="Следующая страница")
        if next_link:
            next_page = 'https://ru.wikipedia.org' + next_link['href']
            page_count += 1
            print('Перехожу на следующую страницу: ', page_count)
        else:
            next_page = None

    with open("animals.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Буква", "Количество"])
        for letter, count in sorted(animal_counts.items()):
            writer.writerow([letter, count])

    print("Данные успешно записаны в animals.csv")

get_animal_pages()
