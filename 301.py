import socket
import threading
import time


def pipe(sock_in, sock_out):
    try:
        while True:
            b = sock_in.recv(65536)
            if not b:
                break
            sock_out.sendall(b)
    except socket.error:
        pass
    finally:
        time.sleep(1)
        sock_in.close()
        sock_out.close()


def connecting(cli_sock, _):
    cli_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65535)
    httpd_sock = socket.socket()
    try:
        httpd_sock.connect(('20.247.108.101', 443))
    except socket.error:
        cli_sock.close()
        return
    httpd_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    threading.Thread(target=pipe, args=(cli_sock, httpd_sock)).start()
    pipe(httpd_sock, cli_sock)


def main():
    serv_sock = socket.socket()
    serv_sock.bind(('0.0.0.0', 443))
    serv_sock.listen(50)
    serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
    serv_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    while True:
        threading.Thread(target=connecting, args=serv_sock.accept()).start()


if __name__ == '__main__':
    main()
