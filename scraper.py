from bs4 import BeautifulSoup
import pandas as pd
import os


def parse_local_file():
    file_name = "page.html"

    print("=== Запуск локального парсера (Автономный режим) ===")

    # Проверяем, сохранили ли вы файл в папку
    if not os.path.exists(file_name):
        print(f"❌ Ошибка: Файл '{file_name}' не найден в папке проекта!")
        print("Пожалуйста, сохраните страницу с сайта как page.html в D:\\мои проекты")
        return

    # Открываем и читаем сохраненный HTML-код
    with open(file_name, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Передаем код в BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Ищем блоки с цитатами
    quote_blocks = soup.find_all("div", class_="quote")
    print(f"Найдено блоков с цитатами в файле: {len(quote_blocks)}")

    parsed_data = []

    for block in quote_blocks:
        text = block.find("span", class_="text").text.strip("“”")
        author = block.find("small", class_="author").text.strip()
        tags_meta = block.find_all("a", class_="tag")
        tags = ", ".join([tag.text for tag in tags_meta])

        parsed_data.append({
            "Цитата": text,
            "Autor": author,
            "Теги": tags
        })

    # Сохраняем в Excel
    if parsed_data:
        df = pd.DataFrame(parsed_data)
        output_file = "quotes_portfolio.xlsx"
        df.to_excel(output_file, index=False, engine="openpyxl")
        print(f"✅ Успешно обработано {len(parsed_data)} цитат из файла.")
        print(f"Таблица создана и сохранена в: {output_file}")
    else:
        print("❌ Ошибка: Внутри файла page.html не найдены нужные HTML-теги.")


if __name__ == "__main__":
    parse_local_file()
