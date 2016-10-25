from allItem import FoodItem, ToolItem, OrderItem

class Menu(object):

    def __init__(self, myMenuFile, myToolFile):
        self.listMenuItems = {}
        self.listToolItems = {}
        #Menu
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
        #Tool
        try:
            f = open(myToolFile)
            for line in f.readlines():
                name, num = line.split()
                item = ToolItem(name, int(num))
                self.listToolItems[name] = item 
        except ValueError:        
            print '%s data error' % myToolFile
        except IOError:
            print '%s open fail!' % myToolFile

    def showMenu(self):
        print '------------Menu--------------'
        for index, item in enumerate(self.listMenuItems.itervalues()):
            print '%d. name:%s price:%s' % (index, item.getName(),
                                            item.getPrice())
        print '------------------------------'

    def showTool(self):
        print '------------Tools--------------'
        for index, item in enumerate(self.listToolItems.itervalues()):
            print '%d. name:%s num:%s' % (index, item.getName(),
                                            item.getNum())
        print '------------------------------'

    def isInMenu(self, name):
        return name in self.listMenuItems

    def isInTool(self, name):
        return name in self.listToolItems

    def getMenuItem(self, name):
        return self.listMenuItems[name]

    def getToolItem(self, name):
        return self.listToolItems[name]

class OrderList(object):

    def __init__(self, menu):
        self.menu = menu
        self.orderItems = {}

    def addOrderItem(self, name, num=1):
        if self.menu.isInMenu(name):
            if name in self.orderItems:
                self.orderItems[name].addNum(num)
            else:
                self.orderItems[name] = OrderItem(self.menu.getMenuItem(name), num)
        else:
            print '%s not exit menu!' % name

    def subOrderItem(self, name, num=1):
        if name in self.orderItems:
            self.orderItems[name].subNum(num)
        else:
            print '%s order item not exit' % name

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

        return '\n'.join(strList)

    def getSumPrice(self):
        strList = []
        sumPrice = 0
        strList.append('--------------bill--------------')
        for item in self.orderItems.itervalues():
            if item.getStatus() == OrderItem.STATUS_DOWN:
                sumPrice += item.getPrice() * item.getNum()
                item.setStatus(OrderItem.STATUS_CANCEL)
                temp = "name: %s price: %.2f count: %d" % (item.getName(),
                                                           item.getPrice(),
                                                           item.getNum())
                strList.append(temp)
        strList.append('sum price: %.2f' % sumPrice)

        return sumPrice, '\n'.join(strList)

    def cancleOrderItem(self, name):
        self.orderItems[name].setStauts(OrderItem.STATUS_CANCEL)

    def clearOrderItem(self):
        self.orderItems = {}

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
       if peopleNum <= self.chairCount and ware.subTool(peopleNum) and chopsticks.subTool(peopleNum):
           self.menu.showTool()
           self.peopleNum = peopleNum
           self.currentState = self.STATUS_OPEN
           print 'open success!'
       else:
           print 'open fail!'

    def closeTab(self):
        self.currentState = self.STATUS_CLOSE
        print 'close success!'

    def maybe(self, startState, endState=None):
        if endState is None:
            endState = self.STATUS_CHECK_OUT
        if startState <= self.currentState <= endState: 
            return True
        else:
            print self
            return False

    def addOrderItems(self, name):
        self.tableOrderList.addOrderItem(name)
        self.currentState = self.STATUS_ORDERING

    def addDownItems(self):
        temp = self.tableOrderList.downItem()
        print temp
        self.currentState = self.STATUS_DOWN_ORDER
   
    def clearTable(self):
        self.closeTab()
        self.tableOrderList.clearOrderItem()

    def getBill(self):
        sumPrice, bill = self.tableOrderList.getSumPrice()
        print bill
        self.currentState = self.STATUS_CHECK_OUT
        return sumPrice 

    def setPeopleNum(self, count):
        if 0<= count <= self.chairCount:
            self.peopleNum = count
        else:
            print 'people num (%d) error!' % count

    def getPeopleNum(self):
        return self.peopleNum

    def setCurrentState(self, state):
        if 0 < state <= len(self.STATUS):
            self.currentState = state
        else:
            print '%s state error!' % state 

    def getCurrentState(self):
        return self.currentState

    def setMenu(self, menu):
        self.menu = menu
        self.tableOrderList = OrderList(menu)

    def __str__(self):
        return self.name + ' ' + self.STATUS[self.currentState] + '| chair %d' % self.chairCount

class OrderServer(object):
    
    MENU_FILE = 'food.txt'
    TOOL_FILE = 'tool.txt'
    TABLE_FILE = 'table.txt'

    def __init__(self):
       self.myMenu = Menu(self.MENU_FILE, self.TOOL_FILE)
       self.listTables = {}
       self.count = 0 
       self.initTables()

    def start(self):
        while True:
            self.showFuntion()
            res = input('you want to enter:')
            if res == 0:
                self.showTables()
            if res == 1:
                name = self.inputTableName()
                if name:
                    self.openTable(name)
            elif res == 2:
                name = self.inputTableName()
                if name:
                    self.order(name)
            elif res == 3:
                name = self.inputTableName()
                if name:
                    self.downOrder(name)
            elif res == 4:
                 name = self.inputTableName()
                 if name:
                     self.checkout(name)
            elif res == 5:
                print 'exit app.'
                break

    def openTable(self, tableName):
        if self.listTables[tableName].maybe(Table.STATUS_CLOSE, Table.STATUS_CLOSE):
            peopleNum = self.inputPeopleNum()
            self.listTables[tableName].openTab(peopleNum)
        else:
            print 'open table fail!'

    def order(self, tableName):
        if self.listTables[tableName].maybe(Table.STATUS_OPEN):
            self.myMenu.showMenu()
            while True:
                name = raw_input('input menuItem name:')
                self.listTables[tableName].addOrderItems(name)
                res = raw_input('Do you want to continue (y/n)?')
                if res == 'n':
                    break
            print 'order end!'
        else:
            print 'order fail!'
        
    def checkout(self, tableName):
        if self.listTables[tableName].maybe(Table.STATUS_DOWN_ORDER):
            sumPrice = self.listTables[tableName].getBill()
            self.inputSumPrice(sumPrice)
            self.listTables[tableName].clearTable()
        else:
            print 'checkout fail!'
        

    def downOrder(self, tableName):
        if self.listTables[tableName].maybe(Table.STATUS_ORDERING, Table.STATUS_ORDERING):
            self.listTables[tableName].addDownItems()
        else:
            print 'down order fail!'

    def inputTableName(self):
        try:
            name = raw_input('input table name:')
            if name in self.listTables:
                return name
            else:
                print 'input table name not exit!'
        except:
            print 'not exit table!'
        return None

    def inputPeopleNum(self):
        while True:
            try:
                peopleNum = input('please input people num:')
                if peopleNum > 0:
                    return peopleNum
            except:
                print 'input error!'

    def inputSumPrice(self, sumPrice):
        while True:
            res = raw_input('input price:')
            if sumPrice - 0.1 <= float(res) <= sumPrice + 0.1:
                print 'checkout success!'
                break
            else:
                print 'checkout fail!'


    def showTables(self):
        print '-' * 10 + 'Tables' + '-' * 10
        for tab in sorted(self.listTables.itervalues()):
            print tab
        print '-' * 26

    def showFuntion(self):
        print '**' * 5 + 'function' + '**' *5
        print '0. show tables'
        print '1. open tab'
        print '2. order dishes'
        print '3. down menu'
        print '4. check out'
        print '5. exit'
        print '**' * 14
    
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
        self.count = len(self.listTables)


#start
app = OrderServer()
app.start()
