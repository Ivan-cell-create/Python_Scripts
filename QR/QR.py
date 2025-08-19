import qrcode
from PIL import Image

def generate_qr():
    data = input("Введите ссылку для генерации QR-кода: ").strip()
    
    if not data.startswith("http"):
        return
        
    filename = "qr_code.png"
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

    print(f"QR-код сохранён в файл: {filename}")
    Image.open(filename).show()
    
if __name__ == "__main__":
    generate_qr()