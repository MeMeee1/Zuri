class Category():
    def __init__(self, name, total):
        self._name = name
        self._balance = total

    def showBalance(self):
        print('%s has a current balance of, %d' %(self._name, self._balance))

    def depositAmount(self, amount):
        self._balance += amount

    def withdrawAmount(self, amount):
        self._balance -= amount
        
    def transferAmount(self, amount, receiver):
        try:
            receiver.total += amount
            self._balance -= amount
        except:
            print('Transfer of funds was unsuccessful')
    

class Budget(Category):
    def __init__(self, names, amounts):
        self.names = names
        self.amounts = amounts
        self.categories = []
        for items in self.names:
            items=Category(items,self.amounts[self.names.index(items)])
            self.categories.append(items)

    def balance(self):
        for name in self.names:
            posIndx = self.names.index(name)
            self.categories[posIndx].showBalance()
    def deposit(self, name, amt):
        if name in self.names:
            posIndx = self.names.index(name)
            self.categories[posIndx].depositAmount(amt)
    def withdraw(self, name, amt):
        if name in self.names:
            posIndx = self.names.index(name)
            self.categories[posIndx].withdrawAmount(amt)
    def transfer(self, name, amt, target):
        try:
            posIndx = self.names.index(name)
            self.categories[posIndx].withdrawAmount(amt)
            posIndx= self.names.index(target)
            self.amounts[posIndx].depositAmount(amt)
        except:
            print('Unsuccessful transfer of funds')
