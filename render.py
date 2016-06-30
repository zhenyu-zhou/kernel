#coding:utf-8

import socket
import pygtk
pygtk.require('2.0')
import gtk
import urllib2
import base64
import rsa

import pcap, dpkt, socket
import scapy
from scapy.layers.ssl_tls import *
from scapy.all import *

from ctypes import *
lib = cdll.LoadLibrary('./libzzy.so')

class Link(object):
    def __init__(self):
        self.obj = lib.Link_new()

    def connect(self, s):
        return lib.Link_connect(self.obj, s)

    def recv(self):
        return lib.Link_recv(self.obj)

def dump_packets(fname,goals,local="152.3.136.107"):
    writer = dpkt.pcap.Writer(open(fname,"wb"))
    for ts,pkt in pcap.pcap():
        ether = dpkt.ethernet.Ethernet(pkt)
        if ether.type != dpkt.ethernet.ETH_TYPE_IP:
            continue

        ip = ether.data
	tcp = ip.data
	if tcp.sport == 443 or tcp.dport == 443:
            print "find 443"
            writer.writepkt(pkt,ts)

	"""
        src = socket.inet_ntoa(ip.src)
        dst = socket.inet_ntoa(ip.dst)
        for goal in goals:
            if (src == goal and dst == local) or (src == local and dst == goal):
                print "yes!"
                writer.writepkt(pkt,ts)
                print src,dst,goal
                break
	"""

    writer.close()

def main():

    # dump_packets("myserver.pcap",["192.168.0.137"])
    
    l = Link()
    s = c_char_p(l.connect("wolaishishikan"))
    data = s.value
    print "data1: ", data
    if data:
        buf = data
    else:
        buf = ""
    while not data or data.find("&zzytail") < 0:
        print "data2: ", data
        #if data:
        #    print "data3: ", data
        # print "data4: ", data
        s = c_char_p(l.recv())
        data = s.value
        if not data:
            continue
        if cmp(data, "Hello from zzy") == 0:
            continue
	# print "data buf: ", data
        buf = buf+data

    # print "data out: ", data
    print "buf: ", buf
    myset = buf.split('&')
    # print "set: ", myset
    ip = myset[0]
    port = myset[1]
    print "addr - ", ip, ": ", port
    

    ip = "127.0.0.1"
    port = 23333
    s = socket.socket()
    s.connect((ip, port))

    key_len = 4096
    (pub, priv) = rsa.newkeys(key_len)
    s.send("0770")
    # s.send(pub.e)
    s.send(pub.n)

    image_data = s.recv(4096)
    image_data = rsa.decrypt(image_data, priv)

    """
    message = myset[2]
    timestamp = myset[3]
    signature = myset[4]
    verify = myset[5]
    image_data = myset[6]
    for i in range(7, len(myset)-1):
        image_data = image_data+myset[i]
    # if image_data.find("@#$captchatail@#$") > 0:
    #    image_data = image_data[:-len("@#$captchatail@#$")]
    # print "image: ", image_data

    """
    """

    f = open("/home/zzy/Maca/code/new-captcha-website/images/jemh5lp4.b64")
    image_data = f.read()
    s = socket.socket()
    s.connect(("152.3.144.156", 80))

    """

    mw = MainWin(image_data, s)
    mw.main()

    # page = s.recv(65535)
    # print page

    s.close()

class MainWin:

    def destroy(self, widget, data=None):
        print "destroy signal occured"
        gtk.main_quit()

    def on_submitbtn_clicked(self, widget, event=None):
        solution = self.entry.get_text()
        # print solution
        # urllib2.urlopen(self.verify)
        self.verify.send(solution)
        self.window.destroy()

    def __init__(self, image, verify):
        self.verify = verify
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        #setup vbox
        self.vbox = gtk.VBox(False, 0)
        self.window.add(self.vbox)
        self.vbox.show()
        #setup label
        self.label = gtk.Label("This captcha is used for user registration of "
"example.com")
        self.vbox.add(self.label)
        self.label.show()
        #setup image
        self.image = gtk.Image()
        print "begin to download captcha image"
        loader = gtk.gdk.PixbufLoader()
        # convert b64 to png
        image = image.decode('base64')
        loader.write(image)
        loader.close()
        print "captcha image downloaded"
        self.image.set_from_pixbuf(loader.get_pixbuf().scale_simple(150, 150, gtk.gdk.INTERP_BILINEAR))
        self.vbox.add(self.image)
        self.image.show()
        #setup entry
        self.entry = gtk.Entry()
        self.entry.set_max_length(50)
        self.entry.set_text("put solution here")
        self.entry.select_region(0, len(self.entry.get_text()))
        self.vbox.add(self.entry)
        self.entry.show()
        #setup button
        self.submitbtn = gtk.Button(stock=gtk.STOCK_OK)
        self.submitbtn.set_label("Submit")
        self.submitbtn.connect("clicked", self.on_submitbtn_clicked)
        self.vbox.add(self.submitbtn)
        self.submitbtn.show()
        self.window.show()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    main()
