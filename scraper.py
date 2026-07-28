import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def parse_all_quotes():
    # Стартовый URL сайта
    base_url = "https://toscrape.com"
    current_page = "/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    parsed_data = []
    page_number = 1
    
    print("=== Запуск многостраничного парсера ===")
    
    # Цикл работает до тех пор, пока есть ссылка на следующую страницу
    while current_page:
        full_url = f"{base_url}{current_page}"
        print(f"Парсим страницу {page_number}: {full_url}")
        
        try:
            response = requests.get(full_url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к странице {page_number}: {e}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quote_blocks = soup.find_all("div", class_="quote")
        
        for block in quote_blocks:
            text = block.find("span", class_="text").text.strip("“”")
            author = block.find("small", class_="author").text.strip()
            tags_meta = block.find_all("a", class_="tag")
            tags = ", ".join([tag.text for tag in tags_meta])
            
            parsed_data.append({
                "Цитата": text,
                "Автор": author,
                "Теги": tags
            })
        
        # НАХОДИМ КНОПКУ «NEXT» (След. страница)
        # На сайте она выглядит как <li class="next"><a href="/page/2/">Next →</a></li>
        next_button = soup.find("li", class_="next")
        
        if next_button:
            # Если кнопка есть, берем из нее относительную ссылку (например, '/page/2/')
            current_page = next_button.find("a")["href"]
            page_number += 1
            time.sleep(1)  # Делаем паузу в 1 секунду, чтобы не перегружать сайт (хороший тон в парсинге)
        else:
            # Если кнопки «Next» нет — мы дошли до конца сайта
            current_page = None 
            print("Все страницы успешно обработаны!")
    
    # Сохраняем все собранные данные в Excel
    if parsed_data:
        df = pd.DataFrame(parsed_data)
        output_file = "all_quotes_portfolio.xlsx"
        df.to_excel(output_file, index=False)
        print(f"\nСбор завершен! Всего собрано {len(parsed_data)} цитат.")
        print(f"Результат сохранен в: {output_file}")
    else:
        print("Данные не были собраны.")

if __name__ == "__main__":
    parse_all_quotes()
