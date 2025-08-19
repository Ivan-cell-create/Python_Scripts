import qrcode
from PIL import Image

def generate_wifi_qr():
    ssid = input("Введите имя Wi-Fi сети (SSID): ").strip()
    security = input("Введите тип безопасности (WPA, WEP, None): ").strip().upper()
    password = ''
    
    if security in ("WPA", "WEP"):
        password = input("Введите пароль: ").strip()
    elif security == "NONE":
        security = "nopass"
    else:
        return
    
     
    hidden = input("Скрытая сеть? (да/нет): ").strip().lower()
    hidden_flag = "true" if hidden == "да" else "false"
    
    wifi_string = f"WIFI:T:{security};S:{ssid};"
    if security != "nopass":
        wifi_string += f"P:{password};"
    wifi_string += f"H:{hidden_flag};;"

    qr = qrcode.make(wifi_string)
    filename = "wifi_qr.png"
    qr.save(filename)
    
    print(f"QR-код Wi-Fi сохранён в файл: {filename}")
    Image.open(filename).show()
    
if __name__ == "__main__":
    generate_wifi_qr()