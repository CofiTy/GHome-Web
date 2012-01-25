from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint
import simplejson as json

class GHomeProtocol(Protocol):
    def __init__(self, end_marker):
        """        
        Arguments:
        - `self`:
        - `end_marker`:
        """
        self.end_marker = end_marker


    def sendMessage(self, mess_type, msg):
        to_send = {'type' : mess_type, 'message': msg}
        self.transport.write(json.dumps(to_send) + self.end_marker)


class GHomeProtocolFactory(Factory):
    def buildProtocol(self, addr):
        return GHomeProtocol('#')


def test_got_protocol(p):
    p.sendMessage('test', '{}')

class GHomeClient(object):
    def __init__(self, host, port):
        """
        
        Arguments:
        - `self`:
        - `host`:
        - `port`:
        """
        self.host = host
        self.port = port

    
    def send_mess(self, mess_type, msg):
        self.protocol.sendMessage(mess_type, msg)

    def __got_protocol(self, p):
        self.protocol = p
        p.sendMessage('test', [])

    def __error(self):
        pass
    
    def launch(self):
        self.point = TCP4ClientEndpoint(reactor, self.host, self.port)
        d = self.point.connect(GHomeProtocolFactory())
        d.addCallbacks(self.__got_protocol, self.__error)

        reactor.run()

def twisted_main(host, port):
    gh_client = GHomeClient('localhost', 8080)
    gh_client.launch()


if __name__ == '__main__':
    twisted_main('localhost', 8080)
