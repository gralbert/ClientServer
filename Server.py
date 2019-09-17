import socket
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process


class Server:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind(('127.0.0.1', 10001))
        self.sock.listen(socket.SOMAXCONN)
        self.m = 2
        self.n = 3

    def process(self, conn):
        print('Установлено соединение')
        conn.settimeout(5)
        with conn:
            with ThreadPoolExecutor(max_workers=self.m) as pool:
                pool.submit(self.handler, conn)
        print('Отправили клиенту ответ')

    @staticmethod
    def handler(conn):
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                info = data.decode('utf-8')
                print('Принята информация')
                current_time = time.ctime(time.time())
                if info == 'hour':
                    conn.sendall(current_time[-13:current_time.find(':')].encode('utf-8'))
                elif info == 'minutes':
                    conn.sendall(current_time[current_time
                                 .find(':') + 1:current_time.rfind(':')].encode('utf-8'))
                elif info == 'seconds':
                    conn.sendall(current_time[current_time
                                 .rfind(':') + 1:current_time.rfind(' ')].encode('utf-8'))
                elif info == 'stop':
                    conn.sendall('Connection closed.'.encode('utf-8'))
                    break
                else:
                    conn.sendall('ERROR'.encode('utf-8'))

            except socket.timeout:
                print('close connection by timeout')
                break

    def run(self):
        while True:
            print('Выполнение')
            conn, addr = self.sock.accept()
            process = Process(target=self.process, args=(conn,))
            process.start()
            print('Запущен процесс')
            conn.close()


server = Server()
server.run()
