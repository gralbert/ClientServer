import socket

with socket.create_connection(('127.0.0.1', 10001)) as sock:
    sock.settimeout(2)
    try:
        sock.sendall(b'hour')
        data = sock.recv(1024)
        print('Часы:', data.decode('utf-8'))

        sock.sendall(b'minutes')
        data = sock.recv(1024)
        print('Минуты:', data.decode('utf-8'))

        sock.sendall(b'seconds')
        data = sock.recv(1024)
        print('Секунды:', data.decode('utf-8'))

        sock.sendall(b'hhh')
        data = sock.recv(1024)
        print(data.decode('utf-8'))

        sock.sendall(b'stop')
        data = sock.recv(1024)
        print(data.decode('utf-8'))

    except socket.timeout:
        print('send to timeout')
    except socket.error as err:
        print('send data error ', err)
