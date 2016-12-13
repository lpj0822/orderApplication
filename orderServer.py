#coding:utf-8
import sys
import socket
import threading
import json
import collections
from restaurant import Table, Menu
from commandParse import CommandParse
from orderException import TableException, CommandException, StateException, TableOpenException, FoodException, ToolException, OrderFoodException, CancelOrderFoodException

class ProcessThread(threading.Thread):

    def __init__(self, sock, semaphore, listTables):
        super(ProcessThread, self).__init__()
        self.parse = CommandParse()
        self.sock = sock
        self.semaphore = semaphore
        self.listTables = listTables
        self.setDaemon(True)

    def run(self):
        self.semaphore.acquire()
        sockFile = self.sock.makefile(bufsize=1)
        result = self.recvData(sockFile)
        self.dataProcess(result, sockFile)
        sockFile.close()
        self.sock.close()
        self.semaphore.release()

    def recvData(self, sockFile):
        data = sockFile.readline()
        return data

    def sendData(self, sockFile, data):
        data += '\n'
        sockFile.write(data)

    def dataProcess(self, data, sockFile):
        messageDict = {}
        try:
            messageDict = self.inputParse(data)
        except CommandException as e:
            messageDict['Error'] = str(e)
        # except Exception as e:
        #     print 'server error:', e
        if messageDict:
            self.sendData(sockFile, json.dumps(messageDict, ensure_ascii=False))

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
            messageDict = self.cancelOrder(tableName, foodName)
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
        try:
            if tableName:
                result['show']['table'] = self.showTable(tableName)
            if menu:
                result['show']['food'] = Table.menu.showFood()
        except TableException as e:
            result.clear()
            result['Error'] = str(e)
        return result

    def openTable(self, tableName, peopleNum):
        result = {}
        table = None
        try:
            table = self.getTable(tableName)
            if table.maybe(Table.STATUS_CLOSE, Table.STATUS_CLOSE):
                table.openTab(peopleNum)
            result['openTable'] = '%s 开台成功' % tableName 
        except (TableException, StateException, ToolException, TableOpenException) as e:
            result['Error'] = str(e) 
        finally:
            if table:
                table.releaseLock()
        return result

    def order(self, tableName, foodName, foodNum):
        result = {}
        table = None
        try:
            table = self.getTable(tableName)
            if table.maybe(Table.STATUS_OPEN):
                table.addOrderItems(foodName, foodNum)
            result['order'] = '%s 点菜成功' % tableName
        except (TableException, StateException, FoodException) as e:
            result['Error'] = str(e)
        finally:
            if table:
                table.releaseLock()
        return result

    def cancelOrder(self, tableName, foodName):
        result = {}
        table = None
        try:
            table = self.getTable(tableName)
            if table.maybe(Table.STATUS_ORDERING):
                table.cancelOrderItems(foodName)
            result['cancelOrder'] = '%s 取消菜品成功' % tableName
        except (TableException, StateException, OrderFoodException,
                CancelOrderFoodException) as e:
            result['Error'] = str(e)
        finally:
            if table:
                table.releaseLock()
        return result

    def downOrder(self, tableName):
        result = {}
        table = None
        try:
            table = self.getTable(tableName)
            if table.maybe(Table.STATUS_ORDERING, Table.STATUS_ORDERING):
                result['downOrder'] = table.downItems()
        except (TableException, StateException) as e:
            result['Error'] = str(e)
        finally:
            if table:
                table.releaseLock()
        return result

    def checkout(self, tableName):
        result = {}
        table = None
        try:
            table = self.getTable(tableName)
            if table.maybe(Table.STATUS_DOWN_ORDER):
                result['checkout'] = table.getBill()
                table.clearTable()
        except (TableException, StateException) as e:
            result['Error'] = str(e)
        finally:
            if table:
                table.releaseLock()
        return result

    def showTable(self, name):
        result = {}
        if name == "all":
            for name, table in self.listTables.iteritems():
                result[name] = str(table)
        else:
            table = self.getTable(name)
            result[name] = str(table)
            table.releaseLock()
        return result

    def getTable(self, name):
        table = self.listTables.get(name)
        if not table:
            raise TableException(name)
        table.acquireLock()
        return table

class OrderServer(object):
    
    MENU_FILE = 'food.txt'
    TOOL_FILE = 'tool.txt'
    TABLE_FILE = 'table.txt'
    SERVER_PORT = 9999

    def __init__(self):
       self.flag = True
       self.initSocket(self.SERVER_PORT)
       self.initTables(self.TABLE_FILE)
       self.semaphore = threading.Semaphore(len(self.listTables))
       
    def start(self):
        print 'Order Server start...'
        while self.flag:
            sock = self.acceptClient(self.serverSocket)
            self.clientProcessThread(sock)
        print 'Server End!'

    def acceptClient(self, serverSock):
        sock, addr = serverSock.accept()
        print addr, 'connected'
        return sock

    def clientProcessThread(self, sock):
        processThread = ProcessThread(sock, self.semaphore, self.listTables)
        processThread.start()
        return processThread

    def quit(self):
        result = {}
        self.flag = False
        result['quit'] = '服务器关闭'
        return result

    def initSocket(self, port):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(('', port))
        self.serverSocket.listen(5)

    def initTables(self, tableFile):
        self.myMenu = Menu(self.MENU_FILE, self.TOOL_FILE)
        Table.setMenu(self.myMenu)
        self.listTables = collections.OrderedDict()
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
