make clean

g++ -c -fPIC netlink_user_lib.c  -o netlink_user_lib.o
g++ -shared -Wl,-soname,libzzy.so -o libzzy.so netlink_user_lib.o

python render.py #> user_output_captcha
dmesg > kernel_output_captcha

