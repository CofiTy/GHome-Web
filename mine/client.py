import socket
import simplejson as json

class Server(object):
    """
    """
    __shared_state = {}
    def __init__(self, host='localhost', port=8080):
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
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect()
            self._exists = True
        
    def connect(self):
        self._sock.connect((self._host, self._port))


    def send(self, d={}):
        
        self._sock.send(json.dumps(d)+'$')


    def send_n_receive(self, d={}):
        self.send(d)
        print "Sent " + str(d)
        ans = ""
        while '$' not in ans:
            ans += self._sock.recv(1024)
        
        ans, t = ans.split('$')
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



    def close(self):
        mess = self.build_mess(6)
        self.send(mess)


if __name__ == '__main__':
    s = Server()
    s2 = Server()
    print s.initialise()
