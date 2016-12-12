#coding:utf-8
import sys
import socket
import threading
import json
from restaurant import Table, Menu
from commandParse import CommandParse
from orderException import TableException, CommandException, StateException, TableOpenException, FoodException, OrderFoodException

class ProcessThread(threading.Thread):

    def __init__(self):
        pass

class OrderServer(object):
    
    MENU_FILE = 'food.txt'
    TOOL_FILE = 'tool.txt'
    TABLE_FILE = 'table.txt'
    SERVER_PORT = 9999

    def __init__(self):
       self.myMenu = Menu(self.MENU_FILE, self.TOOL_FILE)
       self.listTables = {}
       self.flag = True
       self.parse = CommandParse()
       self.initSocket(self.SERVER_PORT)
       self.initTables(self.TABLE_FILE)
       
    def start(self):
        print 'Order Server start...'
        while self.flag:
            sock = self.acceptClient(self.serverSocket)
            self.processClient(sock)
        print 'Server End!'

    def acceptClient(self, serverSock):
        sock, addr = serverSock.accept()
        print addr, 'connected'
        return sock

    def processClient(self, sock):
        sockFile = sock.makefile(bufsize=1)
        result = self.recvData(sockFile)
        self.allDataParse(result, sockFile)
        sockFile.close()
        sock.close()

    def recvData(self, sockFile):
        result = []
        data = sockFile.readline()
        result.append(data)
        return result

    def sendData(self, sockFile, data):
        data += '\n'
        sockFile.write(data)

    def allDataParse(self, dataList, sockFile):
        for data in dataList:
            messageDict = {}
            try:
                messageDict = self.inputParse(data)
            except (CommandException, TableException, StateException,
                    TableOpenException, FoodException, OrderFoodException) as e:
                messageDict['Error'] = str(e)
            except Exception as e:
                print 'server error:', e
            if messageDict:
                self.sendData(sockFile, json.dumps(messageDict, encoding='utf-8'))

    def inputParse(self, data):
        messageDict = {}
        data = data.strip()
        listResult = data.split()
        if len(listResult) <= 0:
            raise CommandException('input')
        elif listResult[0] == "show":
            tableName, menu = self.parse.showParse(listResult[1:])
            messageDict = self.showInformation(tableName, menu)
        elif listResult[0] == "openTable":
            tableName, peopleNum = self.parse.openTableParse(listResult[1:])
            messageDict = self.openTable(tableName, peopleNum)
        elif listResult[0] == "order":
            tableName, foodName, foodNum = self.parse.orderParse(listResult[1:])
            messageDict = self.order(tableName, foodName, foodNum)
        elif listResult[0] == "cancelOrder":
            tableName, foodName = self.parse.cancelOrderParse(listResult[1:])
            messageDict = self.cancelOrder(options)
        elif listResult[0] == "downOrder":
            tableName = self.parse.downOrderParse(listResult[1:])
            messageDict = self.downOrder(tableName)
        elif listResult[0] == "checkout":
            tableName = self.parse.checkoutParse(listResult[1:])
            messageDict = self.checkout(tableName)
        elif listResult[0] == "quit":
            messageDict = self.quit()
        else:
            raise CommandException('not exit')
        return messageDict

    def showInformation(self, tableName, menu):
        result = {'show':{}}
        if tableName:
            result['show']['table'] = self.showTable(tableName)
        if menu:
            result['show']['food'] = self.myMenu.showFood()
        return result

    def openTable(self, tableName, peopleNum):
        table = self.getTable(tableName)
        if table and table.maybe(Table.STATUS_CLOSE, Table.STATUS_CLOSE):
            table.openTab(peopleNum)
        result['openTable'] = '%s 开台成功' % tableName 
        return result

    def order(self, tableName, foodName, foodNum):
        table = self.getTable(tableName)
        if table.maybe(Table.STATUS_OPEN):
            table.addOrderItems(foodName, foodNum)
        result['order'] = '%s 点菜成功' % tableName
        return result

    def cancelOrder(self, tableName, foodName):
        table = self.getTable(tableName)
        if table.maybe(Table.STATUS_ORDERING):
            table.cancelOrderItems(foodName)
        result['cancelOrder'] = '%s 取消菜品成功'
        return result

    def downOrder(self, tableName):
        result = {}
        table = self.getTable(tableName)
        if table.maybe(Table.STATUS_ORDERING, Table.STATUS_ORDERING):
            result['downOrder'] = table.downItems()
        return result

    def checkout(self, tableName):
        result = {}
        table = self.getTable(tableName)
        if table.maybe(Table.STATUS_DOWN_ORDER):
            result['checkout'] = table.getBill()
            table.clearTable()
        return result

    def quit(self):
        self.flag = False
        result['quit'] = '服务器关闭'
        return result

    def showTable(self, name):
        result = []
        if name == "all":
            for tab in sorted(self.listTables.itervalues()):
                result.append(str(tab))
        else:
            table = self.getTable(name)
            if table:
                result.append(str(table))
        return result

    def getTable(self, name):
        table = self.listTables.get(name)
        if not table:
            raise TableException(name)
        return table

    def initSocket(self, port):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(('', port))
        self.serverSocket.listen(5)

    def initTables(self, tableFile):
        try:
            f = open(tableFile)
            for line in f.readlines():
                name, count = line.split()
                item = Table(name, int(count))
                item.setMenu(self.myMenu)
                self.listTables[name] = item
        except ValueError:        
            print '%s data error' % self.TABLE_FILE
        except IOError:
            print '%s open fail!' % self.TABLE_FILE


if __name__ == "__main__":
    #start
    app = OrderServer()
    app.start()
