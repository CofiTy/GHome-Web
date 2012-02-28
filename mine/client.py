import socket
import simplejson as json

class Server(object):
    """
    """
    __shared_state = {}
    def __init__(self, host='localhost', port=5003):
        """
        
        Arguments:
        - `host`:
        - `port`:
        """
        #Borgs !!
        self.__dict__ = self.__shared_state

        try:
            self._exists
        except AttributeError: 
            print "Create"
            self._host = host
            self._port = port
            self.mk_sock()
            self.connect()
            self._exists = True
            self._rest = ""
            self.op = 0
            self.cl = 0

    def mk_sock(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(3.0)

        
    def connect(self):
        self._sock.connect((self._host, self._port))


    def send(self, d={}):
        try:
            self._sock.send(json.dumps(d))
        except IOError:
            self._sock.close()
            self.mk_sock()
            self.connect()
            self.send(d)


    def send_n_receive(self, d={}):
        self.send(d)
        print "Sent " + str(d)
        recv = self._rest
        finished = False
        parsed = False
        i = 0

        while not finished:
            
            recv += self._sock.recv(8192)
            
            print len(recv)

            #Debug
            recv.replace('$', '')

            if len(recv) == 0:
                finished = True
                ans = ""

            while not parsed and len(recv) != 0:
                if recv[i] == '{':
                    self.op += 1
                elif recv[i] == '}':
                    self.cl += 1
                        
                if self.op == self.cl:
                    finished = True
                    parsed = True
                    try:
                        self._rest = recv[i+1:]
                        ans = recv[:i+1]
                    except IndexError:
                        self._rest = ""
                        ans = recv

                    self.op = 0
                    self.cl = 0

                elif i+1 == len(recv):
                    parsed = False

                i += 1
        
        return ans

    def build_mess(self, num, message=None):
        mess = {}
        mess["type"] = num
        mess["message"] = message
        
        return mess



    def initialise(self):
        mess = self.build_mess(1)
        ans= self.send_n_receive(mess)
        print ans

        return json.loads(ans)['message']
            


    def command(self, command):
        mess = self.build_mess(3, command)
        self.send(mess)



    def update(self, sensors=[]):
        mess = self.build_mess(4, sensors)
        ans = self.send_n_receive(mess)
        print ans

        return json.loads(ans)['message']



    def history(self, sensor, rollback):
        mess = self.build_mess(7, {"id": sensor, "rollback": rollback})
        ans = self.send_n_receive(mess)

        return json.loads(ans)['message']



    def logs(self):
        mess = self.build_mess(9)
        ans = self.send_n_receive(mess)

        return json.loads(ans)['message']



    def edits(self, name):
        mess = self.build_mess(11, name)
        ans = self.send_n_receive(mess)

        return json.loads(ans)['message']



    def edata(self, name, blob):
        mess = self.build_mess(12, {"name": name, "file": blob})
        ans = self.send_n_receive(mess)

        return json.loads(ans)['message']



    def close(self):
        mess = self.build_mess(6)
        self.send(mess)


if __name__ == '__main__':
    s = Server()
    s2 = Server()
    print s.initialise()
