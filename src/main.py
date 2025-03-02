import game as g
import database as db
import input
import buzzer

if __name__ == '__main__':
    input.setup()
    buzzer.setup()
    db.init()
    # db.clean_db()
    game = g.Game()
    game.run()
    db.close()
    # here we should have sudo shutdown
    print('TURNING OFF.....')