from scapy.all import *
from scapy.layers import ssl_tls
from scapy.layers.ssl_tls import *
from scapy.layers.ssl_tls_crypto import *

def load_packet(p, i = 1):
    ssl = p.payload.payload.payload
    if not isinstance(ssl,ssl_tls.SSL):
        return
    print "#####################"
    print len(ssl.records),i,p.payload.src,p.payload.payload.dport
#    if i!=7:
 #       return
    for record in ssl.records:
        if record.content_type != TLSContentType.HANDSHAKE:
            continue
        handshake = record.payload
        certs = handshake.payload
        if not isinstance(certs,TLSCertificateList):
            continue
	# print "######################################"
        # certs.show()
	# print "######################################"
        for cert in certs.certificates:
	    print "######################################"
	    # print cert.data
	    print type(cert)
	    print "######################################"
	    try:
            	pk = x509_extract_pubkey_from_der(cert.data)
	    except Exception, ex:
		print "zzy: exception: ",ex
		continue

            print "pk: %r" % (pk)
            for k in pk.keydata:
                try:
                    print "k: ", k,getattr(pk,k)
                except:
                    print "k: ", k
            print "cipher of (hello world):",pk.encrypt("hello world",1234)
            x509 = cert.data
            # x509.show()
           # print "subject: %r" % x509.subject
            break
            #record.payload
#    if i==10:
 #       ssl.show()
       # record.show()
        
def read_packets(fname,callback,count = -1):
    print "########################%s######################" % fname
    pkts = rdpcap(fname)
    for i,p in enumerate(pkts):
        callback(p,i)

if __name__ == "__main__":
    #sniff(prn = load_packet)
    read_packets("myserver.pcap",load_packet)
   # read_packets("alipay.pcap",load_packet)
   # read_packets("alipay2.pcap",load_packet)
    #read_packets("163.pcap",load_packet)
   # read_packets("qq.pcap",load_packet)
