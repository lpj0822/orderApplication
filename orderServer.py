#coding:utf-8
import sys
from optparse import OptionParser
from restaurant import Table

class OrderServer(object):
    
    MENU_FILE = 'food.txt'
    TOOL_FILE = 'tool.txt'
    TABLE_FILE = 'table.txt'

    def __init__(self):
       self.myMenu = Menu(self.MENU_FILE, self.TOOL_FILE)
       self.listParser = {}
       self.listTables = {}
       self.flag = True
       self.initTables()
       self.initInputOptionParser()

    def start(self):
        self.showFuntion()
        while self.flag:
            res = raw_input('请输入指令:')
            res = res.strip() 
            self.inputParser(res)

    def inputParser(self, inputResult):
        listResult = inputResult.split()
        if len(listResult) <= 0:
            return
        elif listResult[0] == "show":
            options = self.optionsParser("show", listResult[1:])
            if options:
                self.showInformation(options)
        elif listResult[0] == "openTable":
            options = self.optionsParser("openTable", listResult[1:])
            if options:
                self.openTable(options)
        elif listResult[0] == "order":
            options = self.optionsParser("order", listResult[1:])
            if options:
                self.order(options)
        elif listResult[0] == "cancelOrder":
            options = self.optionsParser("cancelOrder", listResult[1:])
            if options:
                self.cancelOrder(options)
        elif listResult[0] == "downOrder":
            options = self.optionsParser("downOrder", listResult[1:])
            if options:
                self.downOrder(options)
        elif listResult[0] == "checkout":
            options = self.optionsParser("checkout", listResult[1:])
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
        print '-' * 10 + '餐桌信息' + '-' * 10
        if name == "all":
            for tab in sorted(self.listTables.itervalues()):
                print tab
        else:
            table = self.getTable(name)
            if table:
                print table
        print '-' * 26

    def optionsParser(self, functionName, args):
        parser = self.listParser[functionName]
        (options, args) = parser.parse_args(args)
        if options.help:
            parser.print_help()
            return None
        return options

    def showFuntion(self):
        print '**' * 5 + '点菜系统' + '**' *5
        print '显示餐桌信息(show)'
        print '开台(openTable)'
        print '点菜(order)'
        print '取消菜品(cancelOrder)'
        print '下单(downOrder)'
        print '结账(checkout)'
        print '退出系统(quit)'
        print '**' * 14

    def getTable(self, name):
        return self.listTables.get(name)

    def getTableCount(self):
        return len(self.listTables)

        
    def initTables(self):
        try:
            f = open(self.TABLE_FILE)
            for line in f.readlines():
                name, count = line.split()
                item = Table(name, int(count))
                item.setMenu(self.myMenu)
                self.listTables[name] = item
        except ValueError:        
            print '%s data error' % self.TABLE_FILE
        except IOError:
            print '%s open fail!' % self.TABLE_FILE

    def initInputOptionParser(self):
        #show
        showUsage = "usage: show [options] arg"
        showParser = OptionParser(usage=showUsage, add_help_option=False)
        showParser.add_option("-t", "--table", action="store", type="string",
                              dest="tableName", help="show table information.")
        showParser.add_option("-m", "--menu", action="store_true", 
                              dest="menu", help="show menu information.")
        showParser.add_option("-h", "--help", action="store_true",
                              dest="help", help="show this help message")
        self.listParser["show"] = showParser
        #openTable
        openTableUsage = "usage: openTable [options] arg"
        openTableParser = OptionParser(usage=openTableUsage, add_help_option=False)
        openTableParser.add_option("-t", "--table", action="store",type="string", 
                                   dest="tableName", help="open table.")
        openTableParser.add_option("-n", "--peopleNum", action="store", type="int", 
                                   dest="peopleNum", help="people number.")
        openTableParser.add_option("-h", "--help", action="store_true",
                              dest="help", help="show this help message")
        self.listParser["openTable"] = openTableParser
        #order
        orderUsage = "usage: order [options] arg1 arg2"
        orderParser = OptionParser(usage=orderUsage, add_help_option=False)
        orderParser.add_option("-t", "--table", action="store", type="string",
                               dest="tableName", help="order table.")
        orderParser.add_option("-f", "--food", action="store", type="string",
                               dest="foodName", help="order food.")
        orderParser.add_option("-n", "--num", action="store", type="int",
                              dest="foodNum", default=1, help="order food number.")
        orderParser.add_option("-h", "--help", action="store_true",
                              dest="help", help="show this help message")
        self.listParser["order"] = orderParser
        #cancelOrder
        cancelOrderUsage = "usage: cancelOrder [options] arg"
        cancelOrderParser = OptionParser(usage=cancelOrderUsage, add_help_option=False)
        cancelOrderParser.add_option("-t", "--table", action="store", type="string",
                               dest="tableName", help="cancel order table.")
        cancelOrderParser.add_option("-f", "--food", action="store", type="string",
                               dest="foodName", help="cancel order food.")
        cancelOrderParser.add_option("-n", "--num", action="store", type="int",
                              dest="foodNum",default=1, help="cancel order food number.")
        cancelOrderParser.add_option("-h", "--help", action="store_true",
                              dest="help", help="show this help message")
        self.listParser["cancelOrder"] = cancelOrderParser
        #downOrder
        downOrderUsage = "usage: downOrder [options] arg"
        downOrderParser = OptionParser(usage=downOrderUsage, add_help_option=False)
        downOrderParser.add_option("-t", "--table", action="store",type="string", 
                                   dest="tableName", help="down order table.")
        downOrderParser.add_option("-h", "--help", action="store_true",
                              dest="help", help="show this help message")
        self.listParser["downOrder"] = downOrderParser
        #checkout
        checkoutUsage = "usage: checkout [options] arg"
        checkoutParser = OptionParser(usage=checkoutUsage, add_help_option=False)
        checkoutParser.add_option("-t", "--table", action="store",type="string", 
                                   dest="tableName", help="checkout table.")
        checkoutParser.add_option("-p", "--print", action="store_true",
                                  dest="printBill", help="print table's bill.")
        checkoutParser.add_option("-h", "--help", action="store_true",
                              dest="help", help="show this help message")
        self.listParser["checkout"] = checkoutParser
        #quit
        quitUsage = "usage: quit [options] arg"
        quitParser = OptionParser(usage=quitUsage)
        self.listParser["quit"] = quitParser


if __name__ == "__main__":
    #start
    app = OrderServer()
    app.start()
    #print sys.argv
