#coding:utf-8
import socket
import json
from commandParse import CommandParse
from orderException import CommandException

class OrderClient(object):

    def __init__(self, serverHost, serverPort):
        self.serverHost = serverHost
        self.serverPort = serverPort

    def start(self):
        self.showFunction()
        while True:
            try:
                data = raw_input('请输入指令:')
                if data == 'quit':
                    break
                res = self.commandParse(data)
                if res:
                    sock, sockFile = self.connectServer(self.serverHost, self.serverPort)
                    data = self.addHead(data)
                    sockFile.write(data)
                    self.readData(sockFile)
                    self.close(sockFile, sock)
            except CommandException as e:
                print e
            except Exception as e:
                print 'client error:', e
            finally:
                pass

    def connectServer(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sockFile = sock.makefile(bufsize=1)
        return sock, sockFile

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
            print json.loads(data)

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
