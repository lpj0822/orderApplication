#coding:utf-8
import socket
from commandParse import CommandParse
from orderException import CommandException

class OrderClient(object):

    def __init__(self, serverHost, serverPort):
        self.serverHost = serverHost
        self.serverPort = serverPort
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.showFunction()
        while True:
            try:
                data = raw_input('请输入指令:')
                if data == 'quit':
                    break
                res = self.commandParse(data)
                if res:
                    res = self.addHead(data)
                    self.connectServer(self.clientSocket, self.serverHost,
                                   self.serverPort)
                    sockFile = self.clientSocket.makefile(bufsize=1)
                    sockFile.write(res)
                    self.readData(sockFile)
                    self.close(sockFile, self.clientSocket)
            except CommandException as e:
                print e
            except Exception as e:
                print e
            finally:
                pass

    def connectServer(self, sock, host, port):
        sock.connect((host, port))

    def close(self, sockFile, sock):
        sockFile.close()
        sock.close()
        
    def addHead(self, data):
        return data + '\n'

    def readData(self, sockFile):
        while True:
            data = sockFile.readline()
            if not data:
                break
            print data

    def showFunction(self):
        print '**' * 5 + '点菜系统' + '**' *5
        print '显示餐桌信息(show)'
        print '开台(openTable)'
        print '点菜(order)'
        print '取消菜品(cancelOrder)'
        print '下单(downOrder)'
        print '结账(checkout)'
        print '**' * 14

    def commandParse(self, data):
        parse = CommandParse()
        data = data.strip()
        listResult = data.split()
        if len(listResult) <= 0:
            raise CommandException('input')
        else:
            result = parse.optionsParse(listResult[0], listResult[1:])
            if result:
                return True
            else:
                return False


if __name__ == '__main__':
    client = OrderClient('127.0.0.1', 9999)
    client.start()
