#coding:utf-8
import sys
import socket
from restaurant import Table
from commandParse import CommandParse

class OrderServer(object):
    
    MENU_FILE = 'food.txt'
    TOOL_FILE = 'tool.txt'
    TABLE_FILE = 'table.txt'
    SERVER_PORT = 9999

    def __init__(self):
       self.myMenu = Menu(self.MENU_FILE, self.TOOL_FILE)
       self.listTables = {}
       self.flag = True
       parse = CommandParse()
       self.initSocket(self.SERVER_PORT)
       self.initTables(self.TABLE_FILE)
       
    def start(self):
        while self.flag:
            res = raw_input('请输入指令:')
            self.inputParser(res)

    def acceptClient(self, serverSock):
        sock, addr = 

    def recvData(self, sockFile):
        result = []
        while True:
            data = sockFile.readline()
            if not data:
                break
            result.append(data)
        return result

    def inputParser(self, inputResult):
        inputResult = inputResult.strip()
        listResult = inputResult.split()
        if len(listResult) <= 0:
            return
        elif listResult[0] == "show":
            options = parse.optionsParser("show", listResult[1:])
            if options:
                self.showInformation(options)
        elif listResult[0] == "openTable":
            options = parse.optionsParser("openTable", listResult[1:])
            if options:
                self.openTable(options)
        elif listResult[0] == "order":
            options = parse.optionsParser("order", listResult[1:])
            if options:
                self.order(options)
        elif listResult[0] == "cancelOrder":
            options = parse.optionsParser("cancelOrder", listResult[1:])
            if options:
                self.cancelOrder(options)
        elif listResult[0] == "downOrder":
            options = parse.optionsParser("downOrder", listResult[1:])
            if options:
                self.downOrder(options)
        elif listResult[0] == "checkout":
            options = parse.optionsParser("checkout", listResult[1:])
            if options:
                self.checkout(options)
        elif listResult[0] == "quit":
            self.quit()
        else:
            print '指令输入有误!'

    def showInformation(self, options):
        if options.tableName:
            self.showTable(options.tableName)
        if options.menu:
            self.myMenu.showFood()

    def openTable(self, options):
        if options.tableName and options.peopleNum:
            table = self.getTable(options.tableName)
            if table and table.maybe(Table.STATUS_CLOSE, Table.STATUS_CLOSE):
                table.openTab(options.peopleNum)
            else:
                print 'open table fail!'

    def order(self, options):
        if options.tableName and options.foodName:
            table = self.getTable(options.tableName)
            if table and table.maybe(Table.STATUS_OPEN):
                table.addOrderItems(options.foodName, options.foodNum)
            else:
                print 'order fail!'

    def cencelOrder(self, options):
        if options.tableName and options.foodName:
            table = self.getTable(options.tableName)
            if table and table.maybe(Table.STATUS_ORDERING):
                table.cancelOrderItems(options.foodName)
            else:
                print 'cancel fail!'

    def downOrder(self, options):
        if options.tableName:
            table = self.getTable(options.tableName)
            if table and table.maybe(Table.STATUS_ORDERING, Table.STATUS_ORDERING):
                table.addDownItems()
            else:
                print 'down order fail!'

    def checkout(self, options):
        if options.tableName:
            table = self.getTable(options.tableName)
            if table and table.maybe(Table.STATUS_DOWN_ORDER):
                sumPrice = table.getBill()
                table.clearTable()
            else:
                print 'checkout fail!'
        
    def quit(self):
        self.flag = False
        print '退出点菜系统!'

    def showTable(self, name):
        result = []
        result.append('-' * 10 + '餐桌信息' + '-' * 10)
        if name == "all":
            for tab in sorted(self.listTables.itervalues()):
                result.append(str(tab))
        else:
            table = self.getTable(name)
            if table:
                result.append(str(table))
        result.append('-' * 26)
        return result

    def getTableCount(self):
        return len(self.listTables)

    def initSocket(self, port):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(('', port))
        self.serverSocket.listent(5)

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
    #print sys.argv
