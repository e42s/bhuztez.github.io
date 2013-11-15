#include <fcntl.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/epoll.h>
#include <unistd.h>


void set_nonblock(int fd) {
  int flags = fcntl(fd, F_GETFL);
  fcntl(fd, F_SETFL, flags|O_NONBLOCK);
}

int main() {
  int server = socket(AF_INET, SOCK_STREAM, 0);
  int opt = 1;

  setsockopt(server, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
  set_nonblock(server);

  struct sockaddr_in addr = {0};
  addr.sin_family = AF_INET;
  addr.sin_port = htons(9000);
  addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

  bind(server, (struct sockaddr *)&addr, sizeof(addr));
  listen(server, SOMAXCONN);

  struct epoll_event event = {0};
  event.events = EPOLLIN | EPOLLPRI;

  int poll = epoll_create(4096);

  event.data.fd = server;
  epoll_ctl(poll, EPOLL_CTL_ADD, server, &event);


  struct epoll_event events[4096];
  char buf[4096];

  for(;;) {
    int nfds = epoll_wait(poll, events, 4096, -1);
    for(int i=0; i<nfds; i++) {
      int fd = events[i].data.fd;

      if (fd == server) {
	for(;;) {
	  struct sockaddr connaddr;
	  socklen_t length = sizeof(connaddr);
	  int conn = accept(server, &connaddr, &length);

	  if (conn < 0) {
	    break;
	  }

	  event.data.fd = conn;
	  set_nonblock(conn);
	  epoll_ctl(poll, EPOLL_CTL_ADD, conn, &event);
	}
      } else {

	int length = recv(fd, buf, 4096, 0);
	if (length == 0) {
	  epoll_ctl(poll, EPOLL_CTL_DEL, fd, NULL);
	  close(fd);
	} else {
	  send(fd, buf, length, 0);
	}
      }
    }
  }

  return 0;
}
