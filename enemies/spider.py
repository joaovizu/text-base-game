from random  import randint

from enemies.enemy import Enemy

class Spider(Enemy):

    def __init__(self):
        #Using super to fill the parents class requirements
        super().__init__(name='Spider', hp=10, damage=3, xp_drop=randint(1, 10))
