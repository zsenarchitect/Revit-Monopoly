



class Bank:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.global_balance = 5000
        return cls._instance
    
    def pay_player(self, player):
        amount = getattr(player, 'pay_check', 100)
        if self.global_balance >= amount:
            self.global_balance -= amount
            player.money += amount
            return True
        else:
            return False
        

    def collect_property_tax(self, players):
        for player in players:
            tax = 0
            for property in player.properties:
                tax += property.charge * property.level * 0.1
                player.money -= tax
                self.global_balance += tax