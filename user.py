from ctypes import *

lib = cdll.LoadLibrary('./libzzy.so')

class Link(object):
	def __init__(self):
		self.obj = lib.Link_new()

	def connect(self):
		return lib.Link_connect(self.obj)

l = Link()
s = c_char_p(l.connect())
print "Python: ", s.value
