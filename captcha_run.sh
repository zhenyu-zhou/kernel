make clean
sudo dmesg --clear

g++ -c -fPIC netlink_user_lib.c  -o netlink_user_lib.o
g++ -shared -Wl,-soname,libzzy.so -o libzzy.so netlink_user_lib.o

echo "zzy: Ready to receive CAPTCHA"

python render.py #> user_output_captcha
dmesg > kernel_output_captcha

