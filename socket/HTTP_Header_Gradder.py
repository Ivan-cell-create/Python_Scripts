import requests 
import argparse

def get_headers(url):
    try:
        response = requests.head(url, timeout=5)
        if response.status_code >=400:
            response.request.get(url, timeout=5)
        return response.headers
    except requests.RequestException as e:
        print(f"[✗] Ошибка запроса {url}: {e}")
        return None
    
def main():
    parser = argparse.ArgumentParser(description="HTTP Header Grabber")
    parser.add_argument("urls", nargs="+", help="Список URL или IP для проверки")
    parser.add_argument("-f", "--file", help="Файл с URL/IP по одному на строку")
    args = parser.parse_args()

    targets = args.urls

    if args.file:
        try:
            with open(args.file, "r") as f:
                file_urls = [line.strip() for line in f if line.strip()]
            targets.extend(file_urls)
        except Exception as e:
            print(f"[✗] Не удалось прочитать файл: {e}")
            return

    targets = list(set(targets))

    for url in targets:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url  # добавляем схему по умолчанию
        print(f"\n[+] Заголовки для {url}:")
        headers = get_headers(url)
        if headers:
            for key, value in headers.items():
                print(f"{key}: {value}")

if __name__ == "__main__":
    main()