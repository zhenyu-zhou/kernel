#coding:utf-8

import socket
import pygtk
pygtk.require('2.0')
import gtk
import urllib2
import base64

from ctypes import *
lib = cdll.LoadLibrary('./libzzy.so')

class Link(object):
    def __init__(self):
        self.obj = lib.Link_new()

    def connect(self):
        return lib.Link_connect(self.obj)

def main():

    l = Link()
    s = c_char_p(l.connect())
    data = s.value
    buf = ""
    while data.find("&zzytail") < 0:
        s = c_char_p(l.connect())
        data = s.value
        if cmp(data, "Hello from zzy") == 0:
            continue
        buf = buf+data
    # print "data: ", data
    myset = buf.split('&')
    print "set: ", myset
    ip = myset[0]
    port = myset[1]
    message = myset[2]
    timestamp = myset[3]
    signature = myset[4]
    verify = myset[5]
    image_data = myset[6]
    for i in range(7, len(myset)-1):
        image_data = image_data+myset[i]
    print "image: ", image_data

    mw = MainWin(image_data, "http://localhost:55555/verify")
    mw.main()

class MainWin:

    def destroy(self, widget, data=None):
        print "destroy signal occured"
        gtk.main_quit()

    def on_submitbtn_clicked(self, widget, event=None):
        solution = self.entry.get_text()
        urllib2.urlopen(self.verify)
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
