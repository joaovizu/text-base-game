from logging import critical
from random import randint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hero.hero import Hero
from ui_helper import UI


class Enemy:
    def __init__(self, name: str, hp: int, damage: int, xp_drop: int):
        self.damage = damage
        self.name = name
        self.hp = hp
        self.xp_drop = xp_drop

    def appear(self):
        print(f'A wild {self.name.upper()} has appeared!')

    def attack(self, hero: Hero) -> None:
        self.critic_attack(hero)
        hero.hp -= self.damage
        UI.announce(f'{self.name} attacks for {self.damage} damage! Your HP is now {hero.hp}', UI.ERROR)

    def critic_attack(self, hero: Hero) -> None:
        if randint(1, 10) == 2:
            hero.hp = self.damage * 2
            UI.announce(f'{self.name} CRITIC ATTACK for {self.damage * 2} damage! Your HP is now {hero.hp}', UI.ERROR)
            return


    def is_alive(self):
        return self.hp > 0

