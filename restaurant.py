#coding:utf-8
from allItem import FoodItem, ToolItem, OrderItem
from orderException import FoodException, ToolException, OrderFoodException, TableOpenException, StateException

class Menu(object):

    def __init__(self, myMenuFile, myToolFile):
        self.listMenuItems = {}
        self.listToolItems = {}
        self.initMenu(myMenuFile)
        self.initTool(myToolFile)
        
    def showFood(self):
        result = {}
        for item in self.listMenuItems.itervalues():
            result[item.getName()] = item.getPrice()
        return result
            
    def showTool(self):
        result = {}
        for item in self.listToolItems.itervalues():
            result[item.getName()] = item.getNum()
        return result

    def getMenuItem(self, name):
        item = self.listMenuItems.get(name)
        if not item:
            raise FoodException(name)
        return item

    def getToolItem(self, name):
        item = self.listToolItems.get(name)
        if not item:
            raise ToolException(name)
        return item

    def initMenu(self, myMenuFile):
        try:
            f = open(myMenuFile)
            for line in f.readlines():
                name, price = line.split()
                item = FoodItem(name, float(price))
                self.listMenuItems[name] = item
        except ValueError:        
            print '%s data error' % myMenuFile
        except IOError:
            print '%s open fail!' % myMenuFile

    def initTool(self, myToolFile):
        try:
            f = open(myToolFile)
            for line in f.readlines():
                name, num , price= line.split()
                item = ToolItem(name, int(num), float(price))
                self.listToolItems[name] = item 
        except ValueError:        
            print '%s data error' % myToolFile
        except IOError:
            print '%s open fail!' % myToolFile

class OrderList(object):

    def __init__(self, menu):
        self.menu = menu
        self.orderItems = {}
        self.tablewareCount = 0

    def addOrderItem(self, name, num=1):
        try:
            item = self.getOrderItem(name)
            if item.getStatus() != OrderItem.STATUS_ORDER:
                item.setStatus(OrderItem.STATUS_ORDER)
                item.setNum(num)
            else:
                item.addNum(num)
        except OrderFoodException:
            item = self.menu.getMenuItem(name)
            self.orderItems[name] = OrderItem(item, num)

    def subOrderItem(self, name, num=1):
        item = self.getOrderItem(name)
        item.subNum(num)

    def cancelOrderItem(self, name):
        item = self.getOrderItem(name)
        item.setStatus(OrderItem.STATUS_CANCEL)

    def downItems(self):
        resultDict = {}
        for item in self.orderItems.itervalues():
            if item.getStatus() == OrderItem.STATUS_ORDER:
                item.setStatus(OrderItem.STATUS_DOWN)
                resultDict[item.getName()] = '%.2f|%d' % (item.getPrice(),
                                                          item.getNum())
        return resultDict

    def getSumPrice(self):
        resultDict = {}
        sumPrice = 0
        for item in self.orderItems.itervalues():
            if item.getStatus() == OrderItem.STATUS_DOWN:
                sumPrice += item.getAllPrice()
                item.setStatus(OrderItem.STATUS_CANCEL)
                resultDict[item.getName()] = '%.2f|%d' % (item.getPrice(),
                                                          item.getNum())
        if sumPrice > 0:
            toolItem = self.menu.getToolItem('tableware')
            resultDict['tableware'] = '%.2f|%d' % (toolItem.getPrice(),
                                                   self.getTablewareCount())
            sumPrice += toolItem.getPrice() * self.getTablewareCount()
        resultDict['sumPrice'] = sumPrice
        return resultDict

    def clearOrderItem(self):
        self.orderItems = {}
        self.setTablewareCount(0)
    
    def setTablewareCount(self, count):
        self.tablewareCount = count

    def getTablewareCount(self):
        return self.tablewareCount

    def getOrderItem(self, name):
        item = self.orderItems.get(name)
        if not item:
            raise OrderFoodException(name)
        return item

    def countOrderList(self):
        return len(self.orderItems)

class Table(object):

    STATUS = {1:'close table', 2:'open table', 3:'ordering', 4:'down order', 5:'check out'}
    STATUS_CLOSE = 1
    STATUS_OPEN = 2
    STATUS_ORDERING = 3
    STATUS_DOWN_ORDER = 4
    STATUS_CHECK_OUT = 5

    def __init__(self, name, count):
        self.name = name
        self.chairCount = count
        self.menu = None
        self.peopleNum = 0
        self.tableOrderList = None
        self.currentState = self.STATUS_CLOSE 

    def openTab(self, peopleNum):
       ware = self.menu.getToolItem('tableware')
       chopsticks = self.menu.getToolItem('chopsticks')
       if 0 < peopleNum <= self.chairCount:
           self.peopleNum = peopleNum
           self.tableOrderList.setTablewareCount(peopleNum)
           self.currentState = self.STATUS_OPEN
       else:
           raise TableOpenException(self.name)
    
    def addOrderItems(self, name, num=1):
        self.tableOrderList.addOrderItem(name,num)
        self.currentState = self.STATUS_ORDERING

    def cancelOrderItems(self, name):
        self.tableOrderList.cancelOrderItem(name)

    def downItems(self):
        itemsDict = self.tableOrderList.downItems()
        self.currentState = self.STATUS_DOWN_ORDER
        return itemsDict

    def getBill(self):
        bill = self.tableOrderList.getSumPrice()
        self.currentState = self.STATUS_CHECK_OUT
        return bill 

    def clearTable(self):
        self.closeTab()
        self.tableOrderList.clearOrderItem()

    def closeTab(self):
        self.currentState = self.STATUS_CLOSE

    def maybe(self, startState, endState=None):
        if endState is None:
            endState = self.STATUS_CHECK_OUT
        if startState <= self.currentState <= endState: 
            return True
        else:
            raise StateException('%s %s' % (self.name, str(self)))

    def setPeopleNum(self, count):
        if 0< count <= self.chairCount:
            self.peopleNum = count

    def getPeopleNum(self):
        return self.peopleNum

    def setCurrentState(self, state):
        if 0 < state <= len(self.STATUS):
            self.currentState = state

    def getCurrentState(self):
        return self.currentState

    def setMenu(self, menu):
        self.menu = menu
        self.tableOrderList = OrderList(menu)

    def getName(self):
        return self.name

    def __str__(self):
        return self.STATUS[self.currentState] + '|chair %d' % self.chairCount

