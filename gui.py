'''
Created on 2 de set de 2016

@author: fvj
'''
import sys, pygame
pygame.init()

size = width, height = 400, 400

clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)

square_size = (50,50)

dark_square = pygame.image.load("images/gray_square.png")

b_king   = pygame.transform.scale(pygame.image.load("images/black_king.png"), square_size)
b_queen  = pygame.transform.scale(pygame.image.load("images/black_queen.png"), square_size)
b_rook   = pygame.transform.scale(pygame.image.load("images/black_rook.png"), square_size)
b_bishop = pygame.transform.scale(pygame.image.load("images/black_bishop.png"), square_size)
b_knight = pygame.transform.scale(pygame.image.load("images/black_knight.png"), square_size)
b_pawn   = pygame.transform.scale(pygame.image.load("images/black_pawn.png"), square_size)

w_king   = pygame.transform.scale(pygame.image.load("images/white_king.png"), square_size)
w_queen  = pygame.transform.scale(pygame.image.load("images/white_queen.png"), square_size)
w_rook   = pygame.transform.scale(pygame.image.load("images/white_rook.png"), square_size)
w_bishop = pygame.transform.scale(pygame.image.load("images/white_bishop.png"), square_size)
w_knight = pygame.transform.scale(pygame.image.load("images/white_knight.png"), square_size)
w_pawn   = pygame.transform.scale(pygame.image.load("images/white_pawn.png"), square_size)

white = 255,255,255
screen.fill(white)

init_square = dark_square.get_rect()

for col in range(8):
    square_rect = init_square.move(col*50, (col+1)%2*50)
    for row in range(4):
        screen.blit(dark_square, square_rect)
        square_rect = square_rect.move([0,100])
        
square_rect = init_square
screen.blit(b_rook, square_rect)
square_rect = square_rect.move(50,0)
screen.blit(b_knight, square_rect)
square_rect = square_rect.move(50,0)
screen.blit(b_bishop, square_rect)
square_rect = square_rect.move(50,0)
screen.blit(b_queen, square_rect)
square_rect = square_rect.move(50,0)
screen.blit(b_king, square_rect)
square_rect = square_rect.move(50,0)
screen.blit(b_bishop, square_rect)
square_rect = square_rect.move(50,0)
screen.blit(b_knight, square_rect)
square_rect = square_rect.move(50,0)
screen.blit(b_rook, square_rect)

square_rect = init_square
square_rect = square_rect.move(0,50)
for _ in range(8):
    screen.blit(b_pawn, square_rect)
    square_rect = square_rect.move(50,0)
    
square_rect = init_square
square_rect = square_rect.move(0,350)
screen.blit(w_rook, square_rect)
square_rect = square_rect.move(50,0)
screen.blit(w_knight, square_rect)
square_rect = square_rect.move(50,0)
screen.blit(w_bishop, square_rect)
square_rect = square_rect.move(50,0)
screen.blit(w_queen, square_rect)
square_rect = square_rect.move(50,0)
screen.blit(w_king, square_rect)
square_rect = square_rect.move(50,0)
screen.blit(w_bishop, square_rect)
square_rect = square_rect.move(50,0)
screen.blit(w_knight, square_rect)
square_rect = square_rect.move(50,0)
screen.blit(w_rook, square_rect)

square_rect = init_square
square_rect = square_rect.move(0,300)
for _ in range(8):
    screen.blit(w_pawn, square_rect)
    square_rect = square_rect.move(50,0)
 
while True:
    clock.tick(15)
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
         
    pygame.display.flip()