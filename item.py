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


