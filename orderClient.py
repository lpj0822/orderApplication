#coding:utf-8
import socket

class OrderClient(object):

    def _init__(self, serverHost, serverPort):
        self.serverHost = serverHost
        self.serverPort = serverPort
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connectServer(self, sock, host, port):
        sock.connect((host, port))

    def close(self, sock):
        sock.close()
        
    def addHead(self, data):
        return data + '\n'

    def readData(self, sockFile):
        while True:
            data = sockFile.readline()
            if not data:
                break
            print data

    def start(self):
        while True:
            data = raw_input('请输入指令:')
            res= self.addHead(data)
            self.connectServer(self.clientSocket, self.serverHost,
                               self.serverPort)
            sockFile = self.clientSocket.makefile(bufsize=1)
            sockFile.write(res)
            self.readData(sockFile)
            self.close()

if __name__ == '__main__':
    client = OrderClient('127.0.0.1', 9999)
    client.start()
