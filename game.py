"""
Main game module - orchestrates game flow and initialization.
"""
import config
import database.game_db as db
from battle.Battle import Battle
from enemies.spider import Spider
from hero.hero import Hero
from inventory.inventory import Inventory
from ui_helper import UI
from weapon.weapon import Weapon


class GameManager:
    """Manages game state and flow."""
    
    def __init__(self):
        """Initialize game with default weapon, inventory, and hero."""
        self.weapon = Weapon(name='AXE', damage=2)
        self.inventory = Inventory(weapon=self.weapon)
        self.hero = Hero(inventory=self.inventory, equipped_weapon=self.weapon)
    
    def battle(self) -> None:
        """Start a battle between hero and a spider enemy."""
        spider = Spider()
        battle_instance = Battle(spider, self.hero)
        battle_instance.battle_start()
        UI.clear_console()
    
    def select_weapon(self) -> None:
        """Equip the hero with a starting weapon."""
        print('To battle those enemies you need a weapon.')
        UI.announce('Take this AXE', UI.INFO)
        self.hero.equipped_weapon = self.weapon
        self.inventory.weapon = self.weapon
    
    def introduction(self) -> None:
        """Display introduction story and collect hero name."""
        UI.announce('Welcome to my text based game! Like in the old times!!', UI.GOLD)
        print('Now imagine you are in the medieval era. You\'re just a normal person walking')
        print('But something is wrong in the whole city! People are running and screaming, the sky is grey,'
              ' and in the horizon you see a lot of enemies approaching')
        print('Well, what do you do now?')
        print('First we need to know your hero name, tell me what is it:')
        hero_name = input('Input here your hero name: ')
        self.hero.name = hero_name.upper()
        db.save_game(self.hero)
        UI.clear_console()
        UI.announce(f'WELCOME {self.hero.name}! Let\'s start your adventure!', UI.SUCCESS)
        print(f'You are at level {self.hero.level}')
    
    def run(self) -> None:
        """Main game loop - load/create hero, select weapon, and battle."""
        # Load existing game data or start new game
        save_data = db.load_game()
        
        if save_data:
            self.hero.level, self.hero.hp, self.hero.name, self.hero.base_dmg, self.hero.xp = save_data
            UI.announce(f"WELCOME BACK {self.hero.name}", UI.SUCCESS)
        else:
            self.introduction()
        
        self.select_weapon()
        UI.clear_console()
        self.battle()
        UI.clear_console()
        
        # Save progress
        db.save_game(self.hero)


def main() -> None:
    """Entry point for the game."""
    game_manager = GameManager()
    game_manager.run()


if __name__ == "__main__":
    main()
