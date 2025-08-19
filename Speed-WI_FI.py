import speedtest
import threading
import time 
from tqdm import tqdm

# Функция запуска теста на загрузку в отдельном потоке
def run_download(st, results):
    results['download'] = st.download()

# Функция запуска теста на выгрузку в отдельном потоке
def run_upload(st, results):
    results['upload'] = st.upload()
    
def show_progress(event, desc):
    with tqdm(total=100, desc=desc) as pbar:
        while not event.is_set():
            pbar.update(5)
            if pbar.n >= 100:
                pbar.n = 0
                pbar.refresh()
            time.sleep(0.1)
        pbar.n = 100
        pbar.refresh()

def test_internet_speed_with_progress():
    st = speedtest.Speedtest() 
    print("Выбираем лучший сервер...")
    best = st.get_best_server()

    print(f"Тестируемый сервер: {best['sponsor']} ({best['name']}, {best['country']}) — {best['host']}")

    download_event = threading.Event()
    upload_event = threading.Event()
    results = {}

    download_thread = threading.Thread(target=run_download, args=(st, results))
    download_thread.start()

    download_progress_thread = threading.Thread(target=show_progress, args=(download_event, "Тестируем загрузку"))
    download_progress_thread.start()

    download_thread.join()  # join - дожидаемся завершения потока
    download_event.set()    # set - флаг для условного продлжения
    download_progress_thread.join()

    upload_thread = threading.Thread(target=run_upload, args=(st, results))
    upload_thread.start()

    upload_progress_thread = threading.Thread(target=show_progress, args=(upload_event, "Тестируем выгрузку"))
    upload_progress_thread.start()

    upload_thread.join() 
    upload_event.set()
    upload_progress_thread.join()

    ping = st.results.ping
    download_speed = results['download'] / 1_000_000  # переводим в Мбит/с
    upload_speed = results['upload'] / 1_000_000      # переводим в Мбит/с

    print(f"\nРезультаты теста скорости интернета:")
    print(f"Ping: {ping:.2f} ms")
    print(f"Скорость загрузки: {download_speed:.2f} Мбит/с")
    print(f"Скорость выгрузки: {upload_speed:.2f} Мбит/с")

if __name__ == "__main__":
    test_internet_speed_with_progress()
