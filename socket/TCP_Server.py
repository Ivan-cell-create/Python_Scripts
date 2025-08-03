import socket
import threading #модуль для многопоточности 

IP = '0.0.0.0'
PORT = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.bind((IP, PORT)) #bind - привязка сокета к кокнретному адресу 
    server.listen(5) #listen - переводит сокет в режим прослушивания входящих соединений
    print(f'[*] Listening on {IP}:{PORT}')
    
    while True:
        client, address = server.accept() #accept ожидание входящего подлючения от клиента 
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        client_handler =  threading.Thread(target=handler_client, args=(client))
        
        client_handler.start()
        
def handler_client(client_socked):
    with client_socked as sock:
     request = sock.recv(1024)#recv - прием данных от другого пк 
     print(f'[*] Received: {request.decode("utf-8")}') 
     sock.send(b"ACK")#send - отправка данных через сокет на другую сторону
     
if __name__ == '__main__':
    main()  
