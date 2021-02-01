from game_objects import  Game

game = Game(['Pl1','Pl2','Pl3','Pl4'])

game.conn_to_platform('Pl3')
game.ball.set_random_speed_direction()
game.start_game()