# importing libraries
import pygame
import time
import random

class Game():
    def __init__(self, size):
        # Window size
        self.window_x, self.window_y = 10*size, 10*size
        
        # color setting
        self.bg_color = pygame.Color(255, 255, 249) # ivory
        self.agent_color = pygame.Color(220, 20, 60) # crimson
        self.obstacle_color = pygame.Color(47, 79, 79) # dark slate gray
        self.hole_color = pygame.Color(50, 205, 50) # lime green
        
        # initialising pygame
        pygame.init()
        pygame.display.set_caption(f'')
        self.game_window = pygame.display.set_mode((self.window_x, self.window_y))
        self.game_window.fill(self.bg_color)
        self.fps = pygame.time.Clock()
        self.fps.tick(10)
    
    def display_all(self, boards):
        for board in boards:
            self.display(board)
        
    def display(self, board):
        self.game_window.fill(self.bg_color)
        for i in range(board.size):
            for j in range(board.size):
                if board.board[i][j] == 1:
                    pygame.draw.rect(self.game_window, self.agent_color, [10*i, 10*j, 10, 10])
                elif board.board[i][j] == 2:
                    pygame.draw.rect(self.game_window, self.obstacle_color, [10*i, 10*j, 10, 10])
                elif board.board[i][j] == 3:
                    pygame.draw.rect(self.game_window, self.hole_color, [10*i, 10*j, 10, 10])
        pygame.display.update()
        time.sleep(0.6) # update one frame per 0.6 seconds
                
        
        
    

# snake_speed = 15

# # Window size
# window_x = 720
# window_y = 480

# # defining colors
# black = pygame.Color(0, 0, 0)
# white = pygame.Color(255, 255, 255)
# red = pygame.Color(255, 0, 0)
# green = pygame.Color(0, 255, 0)
# blue = pygame.Color(0, 0, 255)

# # Initialising pygame
# pygame.init()

# # Initialise game window
# pygame.display.set_caption('GeeksforGeeks Snakes')
# game_window = pygame.display.set_mode((window_x, window_y))

# # FPS (frames per second) controller
# fps = pygame.time.Clock()

# # defining snake default position
# snake_position = [100, 50]

# # defining first 4 blocks of snake body
# snake_body = [[100, 50],
# 			[90, 50],
# 			[80, 50],
# 			[70, 50]
# 			]
# # fruit position
# fruit_position = [random.randrange(1, (window_x//10)) * 10,
# 				random.randrange(1, (window_y//10)) * 10]

# fruit_spawn = True

# # setting default snake direction towards
# # right
# direction = 'RIGHT'
# change_to = direction

# # initial score
# score = 0

# # displaying Score function
# def show_score(choice, color, font, size):

# 	# creating font object score_font
# 	score_font = pygame.font.SysFont(font, size)
	
# 	# create the display surface object
# 	# score_surface
# 	score_surface = score_font.render('Score : ' + str(score), True, color)
	
# 	# create a rectangular object for the text
# 	# surface object
# 	score_rect = score_surface.get_rect()
	
# 	# displaying text
# 	game_window.blit(score_surface, score_rect)

# # game over function
# def game_over():

# 	# creating font object my_font
# 	my_font = pygame.font.SysFont('times new roman', 50)
	
# 	# creating a text surface on which text
# 	# will be drawn
# 	game_over_surface = my_font.render(
# 		'Your Score is : ' + str(score), True, red)
	
# 	# create a rectangular object for the text
# 	# surface object
# 	game_over_rect = game_over_surface.get_rect()
	
# 	# setting position of the text
# 	game_over_rect.midtop = (window_x/2, window_y/4)
	
# 	# blit will draw the text on screen
# 	game_window.blit(game_over_surface, game_over_rect)
# 	pygame.display.flip()
	
# 	# after 2 seconds we will quit the program
# 	time.sleep(2)
	
# 	# deactivating pygame library
# 	pygame.quit()
	
# 	# quit the program
# 	quit()


# # Main Function
# while True:
	
# 	# handling key events
# 	for event in pygame.event.get():
# 		if event.type == pygame.KEYDOWN:
# 			if event.key == pygame.K_UP:
# 				change_to = 'UP'
# 			if event.key == pygame.K_DOWN:
# 				change_to = 'DOWN'
# 			if event.key == pygame.K_LEFT:
# 				change_to = 'LEFT'
# 			if event.key == pygame.K_RIGHT:
# 				change_to = 'RIGHT'

# 	# If two keys pressed simultaneously
# 	# we don't want snake to move into two
# 	# directions simultaneously
# 	if change_to == 'UP' and direction != 'DOWN':
# 		direction = 'UP'
# 	if change_to == 'DOWN' and direction != 'UP':
# 		direction = 'DOWN'
# 	if change_to == 'LEFT' and direction != 'RIGHT':
# 		direction = 'LEFT'
# 	if change_to == 'RIGHT' and direction != 'LEFT':
# 		direction = 'RIGHT'

# 	# Moving the snake
# 	if direction == 'UP':
# 		snake_position[1] -= 10
# 	if direction == 'DOWN':
# 		snake_position[1] += 10
# 	if direction == 'LEFT':
# 		snake_position[0] -= 10
# 	if direction == 'RIGHT':
# 		snake_position[0] += 10

# 	# Snake body growing mechanism
# 	# if fruits and snakes collide then scores
# 	# will be incremented by 10
# 	snake_body.insert(0, list(snake_position))
# 	if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
# 		score += 10
# 		fruit_spawn = False
# 	else:
# 		snake_body.pop()
		
# 	if not fruit_spawn:
# 		fruit_position = [random.randrange(1, (window_x//10)) * 10,
# 						random.randrange(1, (window_y//10)) * 10]
		
# 	fruit_spawn = True
# 	game_window.fill(black)
	
# 	for pos in snake_body:
# 		pygame.draw.rect(game_window, green,
# 						pygame.Rect(pos[0], pos[1], 10, 10))
# 	pygame.draw.rect(game_window, white, pygame.Rect(
# 		fruit_position[0], fruit_position[1], 10, 10))

# 	# Game Over conditions
# 	if snake_position[0] < 0 or snake_position[0] > window_x-10:
# 		game_over()
# 	if snake_position[1] < 0 or snake_position[1] > window_y-10:
# 		game_over()

# 	# Touching the snake body
# 	for block in snake_body[1:]:
# 		if snake_position[0] == block[0] and snake_position[1] == block[1]:
# 			game_over()

# 	# displaying score countinuously
# 	show_score(1, white, 'times new roman', 20)

# 	# Refresh game screen
# 	pygame.display.update()

# 	# Frame Per Second /Refresh Rate
# 	fps.tick(snake_speed)
