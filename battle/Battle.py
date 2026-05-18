"""
Battle system module - handles turn-based combat between heroes and enemies.
"""
from enum import Enum
from random import randint

import config
from enemies.enemy import Enemy
from hero.hero import Hero
from ui_helper import UI


class PlayerAction(Enum):
    """Available actions for the player during battle."""
    ATTACK = '1'
    ITEMS = '2'


class Battle:
    """Manages turn-based battle between a player and an enemy."""
    
    def __init__(self, enemy_instance: Enemy, player_instance: Hero):
        """
        Initialize a battle.
        
        Args:
            enemy_instance: The enemy to battle against.
            player_instance: The hero/player character.
        """
        self.enemy_instance = enemy_instance
        self.player_instance = player_instance
    
    def is_battle_active(self) -> bool:
        """Check if both player and enemy are still alive."""
        return self.player_instance.is_alive() and self.enemy_instance.is_alive()
    
    def player_turn(self) -> None:
        """Execute the player's turn - get input and perform action."""
        UI.announce(f"{self.player_instance.name.upper()}'s turn", UI.ERROR)
        UI.announce("1 - ATTACK", UI.INFO)
        UI.announce("2 - ITEMS", UI.INFO)
        
        choice = input("Choose action: ").strip()
        self._handle_player_action(choice)
    
    def _handle_player_action(self, choice: str) -> None:
        """
        Process the player's chosen action.
        
        Args:
            choice: The player's input choice ('1' for attack, '2' for items).
        """
        try:
            action = PlayerAction(choice)
            if action == PlayerAction.ATTACK:
                self.player_instance.attack(self.enemy_instance)
            elif action == PlayerAction.ITEMS:
                self.player_instance.inspect_inventory()
        except ValueError:
            # Invalid choice - show menu again
            UI.announce("Invalid choice! Please select 1 or 2.", UI.ERROR)
            self.player_turn()
    
    def enemy_turn(self) -> None:
        """Execute the enemy's turn - attack the player."""
        self.enemy_instance.attack(self.player_instance)
    
    def display_battle_status(self) -> None:
        """Display current HP for both player and enemy."""
        status = (f'-> {self.player_instance.name} HP: {self.player_instance.hp} | '
                  f'{self.enemy_instance.name} HP: {self.enemy_instance.hp}')
        UI.announce(status, UI.INFO)
    
    def battle_start(self) -> None:
        """Start the battle and manage turn order until one combatant falls."""
        # Enemy appears at start of battle
        self.enemy_instance.appear()
        
        while self.is_battle_active():
            # Random turn order
            if randint(1, 2) == 1:
                # PLAYER'S TURN
                self.player_turn()
                if not self.enemy_instance.is_alive():
                    break
            else:
                # ENEMY'S TURN
                self.enemy_turn()
                if not self.player_instance.is_alive():
                    break
            
            self.display_battle_status()
        
        # Display battle results
        self._display_battle_result()
    
    def _display_battle_result(self) -> None:
        """Display the outcome of the battle."""
        if self.player_instance.is_alive():
            # Player victory
            UI.announce(f"\nVICTORY! The {self.enemy_instance.name} has been defeated.", UI.SUCCESS)
            self.player_instance.gain_xp(self.enemy_instance.xp_drop)
        else:
            # Player defeat
            config.IS_GAME_OVER = True
            UI.announce("\nGAME OVER... You were slain.", UI.ERROR)
