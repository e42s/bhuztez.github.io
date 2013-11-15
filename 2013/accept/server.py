import errno
import fcntl
import os
import select
import socket

def set_nonblock(s):
    flags = fcntl.fcntl(s, fcntl.F_GETFL)
    fcntl.fcntl(s, fcntl.F_SETFL, flags|os.O_NONBLOCK)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

set_nonblock(server)
server.bind(('127.0.0.1', 9000))
server.listen(socket.SOMAXCONN)

poll = select.epoll()

socks = {server.fileno(): server}

poll.register(server, select.EPOLLIN|select.EPOLLPRI)

while True:
    for fd, event in poll.poll():
        sock = socks[fd]

        if sock == server:
            while True:
                try:
                    conn, addr = server.accept()
                    set_nonblock(conn)
                    socks[conn.fileno()] = conn
                    poll.register(conn, select.EPOLLIN|select.EPOLLPRI)
                except socket.error as e:
                    if e.errno  == errno.EAGAIN:
                        break
        else:
            data = sock.recv(4096)
            if data == '':
                socks.pop(fd)
                poll.unregister(fd)
                sock.close()
                del sock
            else:
                sock.send(data)
