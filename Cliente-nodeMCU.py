
import socket

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.0.27", 7070))
    while(True):
        m=input("m")
        s.send(m.encode("utf-8"))
        if(m=="close"):
            break
        
    print("Bye.")
    s.close()
