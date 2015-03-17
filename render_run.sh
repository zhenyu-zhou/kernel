make clean

g++ -c -fPIC netlink_user_lib.c  -o netlink_user_lib.o
g++ -shared -Wl,-soname,libzzy.so -o libzzy.so netlink_user_lib.o

make
sudo insmod netlink_kernel.ko
python render.py > user_output_render
sudo rmmod netlink_kernel
dmesg > kernel_output_render
