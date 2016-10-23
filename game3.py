class Item(object):

    def __init__(self, name):
        self.name = name

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

class FoodItem(Item):

    def __init__(self, name, price):
        super(MenuItem, self).__init__(name)
        self.price = price

    def setPrice(self, price):
        self.price = price

    def getPrice(self):
        return self.price

class ToolItem(Item):

    def __init__(self, name, num):
        super(ToolItem, self).__init__(name)
        self.num = num

    def addTool(self, num):
        self.num += num

    def subTool(self, num):
        temp = self.num - num
        if temp <= 0:
            return 0
        self.num = temp
        return 1

    def getNum(self):
        return self.num

class OrderItem(Item):

    def __init__(self):
        pass

class OrderList(object):

    def __init__(self):
        self.orderItems = {}

class Menu(object):

    def __init__(self, myMenuFile, myToolFile):
        self.listMenuItems = {}
        self.listToolItems = {}
        #Menu
        try:
            f = open(myMenuFile)
            for line in f.readlines():
                name, price = line.split()
                item = MenuItem(name, float(price))
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

class Table(object):

    STATE = {1:'close tab', 2:'open tab', 3:'ordering', 4:'down order',
             5:'check out'}


    def __init__(self, num):
        self.num = num
        self.tabMenu = None
        self.downItems = {}
        self.peopleNum = 0
        self.currentState = 1 

    def openTab(self, peopleNum):
        if self.currentState == 1:
            if self.tabMenu:
               self.tabMenu.showTool()
               if self.tabMenu.isInTool('tableware') and self.tabMenu.isInTool('chopsticks'):
                   ware = self.tabMenu.getToolItem('tableware')
                   chopsticks = self.tabMenu.getToolItem('chopsticks')
                   if ware.subTool(peopleNum) and chopsticks.subTool(peopleNum):
                       self.peopleNum = peopleNum
                       self.currentState = 2
                       print 'open success!'
                   else:
                        print 'open fail'
               else:
                    print 'open fail'
            else:
                print 'not exit menu!'
        else:
            print self

    def closeTab(self):
        self.currentState = 1
        print 'close success!'

    def addOrderItems(self, name):
        if self.currentState >= 2: 
            if self.tabMenu:
                if self.tabMenu.isInMenu(name):
                    if name in self.orderItems:
                        self.orderItems[name] += 1
                    else:
                        self.orderItems[name] = 1
                    self.currentState = 3
                print '%s not exit menu!' % name
            else:
                print 'not exit menu!'
        else:
            print self

    def addDownItems(self):
        if self.currentState == 3:
            print '-' * 7 + 'order items' + '-' * 7
            for name, num in self.orderItems.iteritems():
                print 'name: %s price: %s num: %s' %(name,
                                                     self.tabMenu.getMenuItem(name).getPrice(), num)
                if name in self.downItems:
                    self.downItems[name] += num
                else:
                    self.downItems[name] = num
            self.currentState = 4
            self.orderItems = {}
        else:
            print self
   
    def printBill(self):
        if self.currentState >= 4:
            print '-' * 7 + 'bill' + '-' * 7
            for name, num in self.downItems.iteritems():
                print 'name: %s price: %s num: %s' %(name,
                                                     self.tabMenu.getMenuItem(name).getPrice(),
                                                     num)
            print 'sum price: %s' % self.getSumPrice(self.downItems)
            self.currentState = 5
        else:
            print self

    def clearTable(self):
        self.closeTab()
        self.orderItems = {}
        self.downItems = {}

    def getSumPrice(self, items):
        sumPrice = 0
        for name, num in self.items.iteritems():
            sumPrice += self.tabMenu.getMenuItem(name).getPrice() * num
        return sumPrice 

    def setPeopleNum(self, count):
        if count >= 0:
            self.peopleNum = count

    def getPeopleNum(self):
        return self.peopleNum

    def setCurrentState(self, state):
        if 0 < state <= len(self.STATE):
            self.currentState = state
        else:
            print '%s state error!' % state 

    def getCurrentState(self):
        return self.currentState

    def getOrderCount(self):
        return len(self.listMenuItems)

    def setTabMenu(self, menu):
        self.tabMenu = menu

    def __str__(self):
        return str(self.num) + ' ' + self.STATE[self.currentState]

class OrderServer(object):

    def __init__(self, myMenuFile, myToolFile, count):
       self.myMenu = Menu(myMenuFile, myToolFile)
       self.listTables = []
       self.count = count
       for x in xrange(count):
           temp = Table(x)
           temp.setTabMenu(self.myMenu)
           self.listTables.append(temp)

    def start(self):
        while True:
            self.showFuntion()
            res = input('you want to enter:')
            if res == 1:
                self.showTable()
                index = self.inputTableNum()
                if index or index == 0:
                    peopleNum = self.inputPeopleNum()
                    self.listTables[index].openTab(peopleNum)
            elif res == 2:
                index = self.inputTableNum()
                if index or index == 0:
                    self.order(index)
            elif res == 3:
                index = self.inputTableNum()
                if index or index == 0:
                    self.downMenu(index)
            elif res == 4:
                 index = self.inputTableNum()
                 if index or index == 0:
                     self.checkout(index)
            elif res == 5:
                print 'exit app.'
                break

    def order(self, tableNum):
        self.myMenu.showMenu()
        while True:
            name = raw_input('input menuItem name:')
            self.listTables[tableNum].addOrderItems(name)
            res = raw_input('Do you want to continue (y/n)?')
            if res == 'n':
                break
        print 'order end!'
        
    def checkout(self, tableNum):
        self.listTables[tableNum].printBill()
        sumPrice = self.listTables[tableNum].getOrderSumPrice()
        while True:
            res = raw_input('input price:')
            if sumPrice - 0.1 <= float(res) <= sumPrice + 0.1:
                self.listTables[tableNum].clearTable()
                print 'checkout success!'
                break
            else:
                print 'checkout fail!'
            res = raw_input('Do you want to continue (y/n)?')
            if res == 'n':
                break

    def downMenu(self, tableNum):
        self.listTables[tableNum].addDownItems()

    def inputTableNum(self):
        try:
            index = input('input table num:')
            if 0 <= index < self.count:
                return index
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
                print 'input error'

    def showTable(self):
        print '-' * 7 + 'Tables' + '-' * 7
        for tab in self.listTables:
            print tab
        print '-' * 20

    def showFuntion(self):
        print '**' * 10
        print '1. open tab'
        print '2. order dishes'
        print '3. down menu'
        print '4. check out'
        print '5. exit'
        print '**' * 10

app = OrderServer('gameMenu.txt', 'gameTool.txt', 5)
app.start()
