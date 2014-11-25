import errno
import fcntl
import os
import select
import socket

def set_nonblock(s):
    flags = fcntl.fcntl(s, fcntl.F_GETFL)
    fcntl.fcntl(s, fcntl.F_SETFL, flags|os.O_NONBLOCK)

def new_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    set_nonblock(s)

    try:
        s.connect(('127.0.0.1', 9000))
    except socket.error as e:
        if e.errno == errno.EINPROGRESS:
            pass

    return s

socks = {}
poll = select.epoll()

requests = 40000
concurrent = 4000

for i in range(concurrent):
    requests = requests - 1
    s = new_connection()
    socks[s.fileno()] = s
    poll.register(s, select.EPOLLOUT)


while True:
    for fd, event in poll.poll():
        sock = socks[fd]

        if event == select.EPOLLOUT:
            poll.modify(fd, select.EPOLLIN | select.EPOLLPRI)
            sock.send("a"*12)
        else:
            data = sock.recv(4096)
            poll.unregister(fd)
            socks.pop(fd)
            sock.close()

            if requests:
                requests = requests - 1
                s = new_connection()
                socks[s.fileno()] = s
                poll.register(s, select.EPOLLOUT)

    if not socks:
        break
