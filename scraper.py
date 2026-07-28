import requests
from bs4 import BeautifulSoup
import pandas as pd


def parse_quotes():
    # URL учебного сайта для парсинга
    url = "https://dzen.ru/"

    # Имитируем реальный браузер (User-Agent), чтобы сайт не заблокировал запрос
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(head := "=== Запуск парсера цитат ===")

    try:
        # Отправляем запрос к сайту
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Вызовет ошибку, если сайт недоступен
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к сайту: {e}")
        return

    # Передаем HTML-код страницы в BeautifulSoup для анализа
    soup = BeautifulSoup(response.text, "html.parser")

    # Находим все блоки с цитатами на странице
    quote_blocks = soup.find_all("div", class_="quote")

    # Список, где будем хранить структурированные данные
    parsed_data = []

    # Обходим каждый блок и извлекаем текст, автора и теги
    for block in quote_blocks:
        # Извлекаем текст цитаты и убираем лишние кавычки
        text = block.find("span", class_="text").text.strip("“”")

        # Извлекаем имя автора
        author = block.find("small", class_="author").text.strip()

        # Собираем все теги цитаты в одну строку через запятую
        tags_meta = block.find_all("a", class_="tag")
        tags = ", ".join([tag.text for tag in tags_meta])

        # Формируем словарь с данными одной цитаты
        quote_info = {
            "Цитата": text,
            "Автор": author,
            "Теги": tags
        }

        # Добавляем в общий список
        parsed_data.append(quote_info)

    # Создаем DataFrame из полученных данных
    df = pd.DataFrame(parsed_data)

    # Сохраняем результат в Excel-файл
    output_file = "quotes_portfolio.xlsx"
    df.to_excel(output_file, index=False)

    print(f"Успешно собрано {len(parsed_data)} цитат.")
    print(f"Данные сохранены в файл: {output_file}")


if __name__ == "__main__":
    parse_quotes()
