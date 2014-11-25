#include <fcntl.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/epoll.h>
#include <unistd.h>

#include <stdio.h>

int new_connection(struct sockaddr_in *addr) {
    int s = socket(AF_INET, SOCK_STREAM, 0);
    int flags = fcntl(s, F_GETFL);
    fcntl(s, F_SETFL, flags|O_NONBLOCK);
    connect(s, (struct sockaddr *)addr, sizeof(struct sockaddr_in));
    return s;
}

int main() {
  int requests = 800000;
  int n = requests;
  int concurrent = 4000;
  int poll = epoll_create(4096);

  struct epoll_event event = {0};
  event.events = EPOLLOUT;

  struct sockaddr_in addr = {0};
  addr.sin_family = AF_INET;
  addr.sin_port = htons(9000);
  addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

  for(int i=0; i<concurrent; i++) {
    requests -= 1;
    int s = new_connection(&addr);
    event.data.fd = s;
    epoll_ctl(poll, EPOLL_CTL_ADD, s, &event);
  }

  struct epoll_event events[4096];
  char buf[4096];

  for(;;) {
    int nfds = epoll_wait(poll, events, 4096, -1);
    for(int i=0; i<nfds; i++) {
      int fd = events[i].data.fd;

      if (events[i].events == EPOLLOUT) {
	event.events = EPOLLIN | EPOLLPRI;
	event.data.fd = fd;
	epoll_ctl(poll, EPOLL_CTL_MOD, fd, &event);
	if (send(fd, buf, 12, 0) == -1) {
	  perror("send");
	};

      } else {
	if(recv(fd, buf, 4096, 0) == -1) {
	  perror("recv");
	};

	epoll_ctl(poll, EPOLL_CTL_DEL, fd, NULL);
	close(fd);
	n -= 1;

	if (requests) {
	  requests -= 1;
	  int s = new_connection(&addr);
	  event.events = EPOLLOUT;
	  event.data.fd = s;
	  epoll_ctl(poll, EPOLL_CTL_ADD, s, &event);
	}

      }
    }

    if (!n) break;
  }


  return 0;
}
