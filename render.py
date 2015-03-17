import socket
import pygtk
pygtk.require('2.0')
import gtk
import urllib2

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
    challenge, verify = data.split(',')

    print "chanllenge:", challenge
    print "verify:", verify

    mw = MainWin(challenge, verify)
    mw.main()

'''
    while True:
        data, addr = sock.recvfrom(1024)
        if data == '':
            continue
        print "received message: ", data
        challenge, verify = data.split(',')
        mw = MainWin(challenge, verify)
        mw.main()
'''

class MainWin:

    def destroy(self, widget, data=None):
        print "destroy signal occured"
        gtk.main_quit()

    def on_submitbtn_clicked(self, widget, event=None):
        solution = self.entry.get_text()
        urllib2.urlopen(self.verify)
        self.window.destroy()

    def __init__(self, path, verify):
        self.path = path
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
        response = urllib2.urlopen(path)
        image = response.read()
        loader = gtk.gdk.PixbufLoader()
        loader.write(image)
        loader.close()
        print "captcha image downloaded"
        self.image.set_from_pixbuf(loader.get_pixbuf())
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

