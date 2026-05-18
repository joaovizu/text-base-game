# THE MAIN SCRIPT, HERE WE START AND END GAME
import config
import database.game_db as db
from game import GameManager

db.init_db()

while True:
    if config.IS_GAME_OVER: break
    else:
        game = GameManager()
        game.run()
