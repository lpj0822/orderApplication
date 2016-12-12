#coding:utf-8
from optparse import OptionParser
from orderException import CommandException

class CommandParse(object):

    def __init__(self):
        self.listParser = {}
        self.initInputOptionParser()

    def showParse(self, args):
        options = self.optionsParse('show', args)
        if options and (options.tableName or options.menu):
            return options.tableName, options.menu
        else:
            raise CommandException('show')

    def openTableParse(self, args):
        options = self.optionsParse('openTable', args)
        if options and options.tableName and options.peopleNum:
            return options.tableName, options.peopleNum
        else:
            raise CommandException('openTable')

    def orderParse(self, args):
        options = self.optionsParse('order', args)
        if options and options.tableName and options.foodName and options.foodNum:
            return options.tableName, options.foodName, options.foodNum
        else:
            raise CommandException('order')

    def cancelOrderParse(self, args):
        options = self.optionsParse('cancelOrder', args)
        if options and options.tableName and options.foodName:
            return options.tableName, options.foodName
        else:
            raise CommandException('cancelOrder')

    def downOrderParse(self, args):
        options = self.optionsParse('downOrder', args)
        if options and options.tableName:
            return options.tableName
        else:
            raise CommandException('downOrder')

    def checkoutParse(self, args):
        options = self.optionsParse('checkout', args)
        if options and options.tableName:
            return options.table
        else:
            raise CommandException('checkout')

    def optionsParse(self, commandName, args):
        parser = self.getParser(commandName)
        (options, args) = parser.parse_args(args)
        if options.help:
            parser.print_help()
            return None
        return options

    def printCommandHelp(self, commandName):
        pass

    def getParser(self, commandName):
        parser = self.listParser.get(commandName)
        if not parser:
            raise CommandException('not exit')
        return parser

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

