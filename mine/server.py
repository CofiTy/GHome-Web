import SocketServer
import socket
import simplejson as json
import random

sensor_list = [{"id":1, "name":"tempi", "type": "Temperature"}, 
{"id":4, "name":"cuisine", "type": "Temperature"}, 
{"id":2, "name":"humi", "type": "Humidity"},
{"id":3, "name":"lumi", "type": "Luminosity"},
{"id":1, "name":"lumi2", "type": "Luminosity"}]


class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print self.data

        self.data, l = self.data.split('$')
        
    def finish(self):
        print "finish"

class Server(object):
    
    def __init__(self, host='localhost', port=8080):
        self._host = host
        self._port = port

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self._host, self._port))



    def serve(self):
        self.s.listen(1)
        self.conn, addr = self.s.accept()
        while True:
            ans = ""
            while '$' not in ans:
                ans += self.conn.recv(1024)
                
            ans, t = ans.split('$')
            print "received : " + ans
            parsed = json.loads(ans)
            
        #initialize
            if parsed["type"] == 1:
                print "initialise"
                config = {"sensors": [
                        {"id":1, "name":"tempi", "type": "Temperature"}, 
                        {"id":4, "name":"cuisine", "type": "Temperature"}, 
                        {"id":2, "name":"humi", "type": "Humidity"},
                        {"id":3, "name":"lumi", "type": "Luminosity"},
                        {"id":1, "name":"lumi2", "type": "Luminosity"}, 
                        ], 
                          "commands":["shutdown", "cooldown", "light-off"]}
                ans = {"type": 2, "message": config}
                self.send(ans)
        #update
            elif parsed["type"] == 4:
                print "update"
                try:
                    self.value += random.randint(-4, 4)
                except:
                    self.value = 21
                    
                data = []
                for sensor_id in parsed["message"]:
                    l = filter(lambda obj: obj["id"] == sensor_id, sensor_list)
                    sensor_type = l[0]["type"]
                    data += [{"id": sensor_id, "value": self.value, "type": sensor_type}]
                    
                ans = {"type": 5, "message": data}
                self.send(ans)



    def send(self, mess):
        to_send = json.dumps(mess)
        print 'sent ' + to_send
        self.conn.send(to_send)

        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    # server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    # server.serve_forever()
    server = Server()
    server.serve()
