KDIR := /lib/modules/$(shell uname -r)/build

obj-m += netlink_kernel.o

default:
	$(MAKE) -C $(KDIR) SUBDIRS=$(PWD) modules

userspace:
	$(CC) netlink_user.c -o netlink_user

clean:
	rm -rf *.o *.ko *.mod.* *.cmd .module* modules* Module* .*.cmd .tmp* netlink_user kernel_output* user_output* *.so

