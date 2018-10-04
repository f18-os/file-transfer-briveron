#! /usr/bin/env python3

# Echo client program
import socket, sys, re

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)

    #--------------
#        with open('Test.txt', 'wb') as f:
#            print ('file opened')
#            while True:
#                #print('receiving data...')
#                data = s.recv(1024)
#                print('data=%s', (data))
#                if not data:
#                    f.close()
#                    print ('file close')
#                    break
#                # write data to a file
#                f.write(data)
#
#        print('Successfully get the file')
#        s.close()
#        print('connection closed')
    #--------------
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

while True:
    userIN=input('What is the name of the file you would like to send:')
    framedSend(s,b"Filename="+userIN.encode(),debug)
    with open(userIN,'rb')as f:
        data=f.read()
        data=data.replace(b'\n',b'@')
        framedSend(s,data,debug)
        f.close()
        print(framedReceive(s,data+userIN.encode()))
