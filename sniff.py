import pcap, dpkt, socket
import scapy
from scapy.layers.ssl_tls import *
from scapy.all import *
import socket
import time

def dump_packets(fname,goals,local="127.0.0.1"):
    writer = dpkt.pcap.Writer(open(fname,"wb"))
    time.sleep(5)
    for ts,pkt in pcap.pcap("lo"):
        ether = dpkt.ethernet.Ethernet(pkt)
        if ether.type != dpkt.ethernet.ETH_TYPE_IP:
            continue
        ip = ether.data
        src = socket.inet_ntoa(ip.src)
        dst = socket.inet_ntoa(ip.dst)
	writer.writepkt(pkt,ts)
	"""
        for goal in goals:
            if (src == goal and dst == local) or (src == local and dst == goal):
                print "yes!"
                writer.writepkt(pkt,ts)
                print src,dst,goal
                break
	"""
    writer.close()


def load_certificate(packet):
    data = dpkt.ethernet.Ethernet(packet)
    ip = data.data
    tcp = ip.data
    data = list(tcp.data)
    if not (len(data)>0 and ord(data[0]) in [23,22]):
        return
    print socket.inet_ntoa(ip.src),tcp.sport,tcp.dport
    print type(tcp),len(tcp),len(tcp.data)
    print "%d" % (ord(data[0]))
    rdpcap(packet).show()
    for k,v in dpkt.ssl.HANDSHAKE_TYPES.values():
        try:
            ssl = v(tcp.data)
            print "success",type(ssl)
            break
        except Exception(e):
            print "fail:",e

def load_packets(fname,callback):
    for ts,packet in dpkt.pcap.Reader(file(fname,"rb")):
        callback(packet)


if __name__ == "__main__":
    dump_packets("myserver.pcap",["127.0.0.1"])
   # dump_packets("163.pcap",["36.250.87.32"])
    # dump_packets("qq.pcap",["115.25.209.29","115.25.209.42"])
   # load_packets("qq.pcap",load_certificate)
  #  pkts = sniff(count=2)
  #  for p in pkts:
   #     p.show()
  #  for p in rdpcap("qq.pcap"):
   #     p.show()


