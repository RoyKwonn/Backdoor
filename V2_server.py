import socket
import zlib
HOST = ''
PORT = 31337
s = socket.socket()
s.bind((HOST, PORT))
s.listen(10)
conn, addr = s.accept()
conn.settimeout(1,0)
while True:
    cmd = zlib.compress(raw_input('>>'))
    try:
        conn.send(cmd)
        data = ""
        while True:
            chunk = conn.recv(1024)
            data += chunk
            try:
                out = zlib.decompress(data)
            except:
                pass
            else:
                break
            print out
    except:
        pass
s.close()
