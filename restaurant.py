#coding:utf-8
from allItem import FoodItem, ToolItem, OrderItem
from orderException import FoodException, OrderFoodException, TableOpenException, StateException

class Menu(object):

    def __init__(self, myMenuFile, myToolFile):
        self.listMenuItems = {}
        self.listToolItems = {}
        self.initMenu(myMenuFile)
        self.initTool(myToolFile)
        
    def showFood(self):
        result = []
        for item in self.listMenuItems.itervalues():
            data = '%s|%s' % (item.getName(), item.getPrice())
            result.append(data)
            #print 'name:%s price:%s' % (item.getName(), item.getPrice())
        return result
            
    def showTool(self):
        result = []
        for item in self.listToolItems.itervalues():
            data = '%s|%s' % (item.getName(), item.getNum())
            result.append(data)
            #print 'name:%s num:%s' % (item.getName(), item.getNum())
        return result

    def getMenuItem(self, name):
        return self.listMenuItems.get(name)

    def getToolItem(self, name):
        return self.listToolItems.get(name)

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
        item = self.menu.getMenuItem(name)
        if item:
            if name in self.orderItems:
                self.orderItems[name].addNum(num)
            else:
                self.orderItems[name] = OrderItem(item, num)
        else:
            raise FoodException(name)

    def subOrderItem(self, name, num=1):
        if name in self.orderItems:
            self.orderItems[name].subNum(num)
        else:
            raise OrderFoodException(name)

    def cencelOrderItem(self,name):
        if name in self.orderItems:
            self.orderItems[name].setStatus(OrderItem.CANCEL)
        else:
            raise OrderFoodException(name)

    def downItem(self):
        strList = []
        strList.append('------down menu------')
        for item in self.orderItems.itervalues():
            if item.getStatus() == OrderItem.STATUS_ORDER:
                item.setStatus(OrderItem.STATUS_DOWN)
                temp = "name: %s price: %.2f count: %d" % (item.getName(),
                                                           item.getPrice(),
                                                           item.getNum())
                strList.append(temp)
        return strList

    def getSumPrice(self):
        strList = []
        sumPrice = 0
        strList.append('--------------bill--------------')
        for item in self.orderItems.itervalues():
            if item.getStatus() == OrderItem.STATUS_DOWN:
                sumPrice += item.getAllPrice()
                item.setStatus(OrderItem.STATUS_CANCEL)
                temp = "name: %s price: %.2f count: %d" % (item.getName(),
                                                           item.getPrice(),
                                                           item.getNum())
                strList.append(temp)
        if sumPrice > 0:
            toolItem = self.menu.getToolItem('tableware')
            strList.appned('name: tableware price: %.2f count: %d' %
                           (toolItem.getPrice(), self.getTablewareCount))
            sumPrice += toolItem.getPrice() * self.getTablewareCount()
        strList.append('sum price: %.2f' % sumPrice)

        return sumPrice, strList

    def cancleOrderItem(self, name):
        self.orderItems[name].setStauts(OrderItem.STATUS_CANCEL)

    def clearOrderItem(self):
        self.orderItems = {}
        self.setTablewareCount(0)
    
    def setTablewareCount(self, count):
        self.tablewareCount = count

    def getTablewareCount(self):
        return self.tablewareCount

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
        self.tableOrderList.cancleOrderItem(name)

    def downItems(self):
        temp = self.tableOrderList.downItem()
        self.currentState = self.STATUS_DOWN_ORDER
        return temp

    def getBill(self):
        sumPrice, bill = self.tableOrderList.getSumPrice()
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
            raise StateException(str(self))

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

    def __str__(self):
        return self.name + ' ' + self.STATUS[self.currentState] + '| chair %d' % self.chairCount

