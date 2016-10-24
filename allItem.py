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

    STATUS = {1:"order item", 2:"down item", 3:"cooking", 4:"cancel item"} 
    STATUS_ORDER = 1
    STATUS_DOWN = 2
    STATUS_COOKING = 3
    STATUS_CANCEL = 4

    def __init__(self, item, num=1):
        self.foodItem = item
        self.num = num
        self.status = STATUS_ORDER

    def getPrice(self):
        return self.foodItem.getPrice()

    def getNum(self):
        return self.num

    def addNum(self, num):
        self.num += num

    def subNum(self, num):
        temp = self.num - num
        if temp < 0:
            self.num = 0
        else:
            self.num = temp
    
    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status

    def __str__(self):
        return self.foodItem.name + " " + self.STATUS[self.status]
