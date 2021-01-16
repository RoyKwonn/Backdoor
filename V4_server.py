import socket
import paramiko
import threading
import sys
host_key = paramiko.RSAKey(filename = 'test_rsa.key')
class Server (paramiko.ServerInterface):
    def _init_(self):
        self.event = threading.Event()
        def check_channel_request(self, kind, chanid):
            if kind == 'session':
                return paramiko.OPEN_SUCCEEDED
            return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
        def check_auth_password(self, username, password):
            if (username == 'root') and (password == 'hwan986200'):
                return paramiko.AUTH_SUCCESSFUL
            return paramiko.AUTH_FAILED
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 31337))
    sock.listen(100)
    print '[+] Listening for connection ...'
    client, addr = sock.accept()
except Exception, e:
    print '[-] Listen/bind/accept failed: ' + str(e)
    sys.exit(1)
try:
    t = paramiko.Transport(client)
    try:
        t.load_server_moduli()
    except:
        raise
    t.add_server_key(host_key)
    server = Server()
    try:
        t.start_server(server=server)
    except paramiko.SSHException, x:
        print '[-] SSH negotiation failed.'
    chan = t.accept(20)
    chan.settimeout(1)
    print '[+] Authenticated!'
    while True:
        command = raw_input("Enter command: ").strip('\n')
        chan.send(command)
        try:
            print chan.recv(2048) + '\n'
        except:
            pass
except Exception, e:
    print '[-] Caught exception: ' + str(e) + ': ' + str(e)
    try:
        t.close()
    except:
        pass
    sys.exit(1)
