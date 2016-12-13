#coding:utf-8
class Item(object):

    def __init__(self, name):
        self.name = name

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def __str__(self):
        return self.name

class FoodItem(Item):

    def __init__(self, name, price):
        super(FoodItem, self).__init__(name)
        self.setPrice(price)

    def setPrice(self, price):
        self.price = price

    def getPrice(self):
        return self.price

class ToolItem(Item):

    def __init__(self, name, num, price):
        super(ToolItem, self).__init__(name)
        self.setNum(num)
        self.setPrice(price)

    def addTool(self, num):
        self.num += num

    def subTool(self, num):
        temp = self.num - num
        if temp <= 0:
            return 0
        self.num = temp
        return 1

    def setNum(self, num):
        if num <= 0:
            self.num = 0
        else:
            self.num = num

    def getNum(self):
        return self.num

    def setPrice(self, price):
        self.price = price

    def getPrice(self):
        return self.price

class OrderItem(Item):

    STATUS = {1:"order", 2:"down", 3:"cooking", 4:"cancel"} 
    STATUS_ORDER = 1
    STATUS_DOWN = 2
    STATUS_COOKING = 3
    STATUS_CANCEL = 4

    def __init__(self, item, num=1):
        super(OrderItem, self).__init__(item.getName())
        self.foodItem = item
        self.setStatus(self.STATUS_ORDER)
        self.setNum(num)

    def setNum(self, num):
        if num <= 0:
            self.num = 0
            self.setStatus(self.STATUS_CANCLE)
        else:
            self.num = num

    def getNum(self):
        return self.num

    def addNum(self, num):
        self.num += num

    def subNum(self, num):
        temp = self.num - num
        if temp <= 0:
            self.num = 0
            self.setStatus(self.STATUS_CANCLE)
        else:
            self.num = temp

    def getPrice(self):
        return self.foodItem.getPrice()

    def getAllPrice(self):
        return self.getPrice() * self.getNum()
    
    def getStatus(self):
        return self.status

    def setStatus(self, status):
        if 0 < status <= len(self.STATUS):
            self.status = status
        else:
            print 'order items status(%d) error!' % status

    def __str__(self):
        return  self.STATUS[self.status] + '|' + self.num
