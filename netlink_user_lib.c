#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <linux/netlink.h>
// #include <cstring>
// #include <Python.h>

#define NETLINK_USER 31

#define MAX_PAYLOAD 1024 /* maximum payload size*/

// using namespace std;

struct sockaddr_nl src_addr, dest_addr;
struct nlmsghdr *nlh = NULL;
struct iovec iov;
int sock_fd;
struct msghdr msg;
char* end_tag = "&zzytail";

class Link{
public:
char* connect(char *hello_msg)
{
    // printf("hello_msg: %s\n", hello_msg);
    // return NULL;

    sock_fd = socket(PF_NETLINK, SOCK_RAW, NETLINK_USER);
    while (sock_fd < 0)
    {
	sock_fd = socket(PF_NETLINK, SOCK_RAW, NETLINK_USER);
    }

    memset(&src_addr, 0, sizeof(src_addr));
    src_addr.nl_family = AF_NETLINK;
    src_addr.nl_pid = getpid(); /* self pid */

    bind(sock_fd, (struct sockaddr *)&src_addr, sizeof(src_addr));

    memset(&dest_addr, 0, sizeof(dest_addr));
    dest_addr.nl_family = AF_NETLINK;
    dest_addr.nl_pid = 0; /* For Linux Kernel */
    dest_addr.nl_groups = 0; /* unicast */

    nlh = (struct nlmsghdr *)malloc(NLMSG_SPACE(MAX_PAYLOAD));
    memset(nlh, 0, NLMSG_SPACE(MAX_PAYLOAD));
    nlh->nlmsg_len = NLMSG_SPACE(MAX_PAYLOAD);
    nlh->nlmsg_pid = getpid();
    nlh->nlmsg_flags = 0;

    strcpy((char*)NLMSG_DATA(nlh), hello_msg); // "Hello from zzy");

    iov.iov_base = (void *)nlh;
    iov.iov_len = nlh->nlmsg_len;
    msg.msg_name = (void *)&dest_addr;
    msg.msg_namelen = sizeof(dest_addr);
    msg.msg_iov = &iov;
    msg.msg_iovlen = 1;

    sendmsg(sock_fd, &msg, 0);
    // printf("Waiting for message from kernel\n");

    /* Read message from kernel */
    recvmsg(sock_fd, &msg, 0);
    return (char *)NLMSG_DATA(nlh);
}

char* recv()
{
    recvmsg(sock_fd, &msg, 0);
    // printf("Received message payload in recv: %s\n", (char *)NLMSG_DATA(nlh));
    if(strstr((char *)NLMSG_DATA(nlh), end_tag) != NULL)
        close(sock_fd);
    return (char *)NLMSG_DATA(nlh);
}

};

extern "C" {
    Link* Link_new(){ return new Link(); }
    void Link_connect(Link* l, char *hello_msg){ l->connect(hello_msg); }
    void Link_recv(Link* l){l->recv();}
}

