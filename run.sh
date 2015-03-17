make clean
make
gcc netlink_user.c -o netlink_user
sudo insmod netlink_kernel.ko
./netlink_user > user_output
dmesg | tail -12 > kernel_output
sudo rmmod netlink_kernel

