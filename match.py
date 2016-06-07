'''
Created on 7 de jun de 2016

@author: fvj
'''
from game import Game

game = Game()

while(True):
    game.board._print()
    
    # PC moves
    while(True):
        pos1 = input()
        pos2 = input()
        if game.move(pos1, pos2):
            break;
        print('Invalid move!')
    
    # NPC moves
    game.aiMove()