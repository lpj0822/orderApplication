#coding:utf-8

class FoodException(Exception):

    def __init__(self, name):
        super(FoodException, self).__init__()
        self.name = name

    def __str__(self):
        return '%s not exit menu!' % self.name


class OrderFoodException(Exception):

    def __init__(self, name):
        super(OrderFoodException, self).__init__()
        self.name = name

    def __str__(self):
        return '%s not exit order items' % self.name

class TableException(Exception):

    def __init__(self, name):
        super(TableException, self).__init__()
        self.name = name

    def __str__(self):
        return '%s table not exit' % self.name

class TableOpenException(Exception):

    def __init__(self, name):
        super(TableOpenException, self).__init__()
        self.name = name

    def __str__(self):
        return '%s table open fail!' % self.name

class StateException(Exception):
    
    def __init__(self, message):
        super(StateException, self).__init__()
        self.message = message

    def __str__(self):
        return 'Error State! current state: %s' % self.message

class CommandException(Exception):

    def __init__(self, commandName):
        super(CommandException, self).__init__()
        self.commandName = commandName

    def __str__(self):
        return '%s command error!' % self.commandName
