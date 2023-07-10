import pygame

#pygame initialization
pygame.init()

#initial variables
WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Chess')
font = pygame.font.Font('freesansbold.ttf', 20)
big_font = pygame.font.Font('freesansbold.ttf', 50)
medium_font = pygame.font.Font('freesansbold.ttf', 35)
timer = pygame.time.Clock()
fps = 60

#game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_location = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
                  (0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_location = [(0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7),
                  (0,6), (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (7,6)]
white_captured_pieces = []
black_captured_pieces = []

#0-white not selected, 1-white selected, 2-black not selected, 3-black selected
turn_step = 0
selection = 100
valid_moves = []

#load in game pieces as images
white_king = pygame.image.load('assets/pieces/white king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))

white_queen = pygame.image.load('assets/pieces/white queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))

white_rook = pygame.image.load('assets/pieces/white rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))

white_bishop = pygame.image.load('assets/pieces/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))

white_knight = pygame.image.load('assets/pieces/white knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))

white_pawn = pygame.image.load('assets/pieces/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))

black_king = pygame.image.load('assets/pieces/black king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))

black_queen = pygame.image.load('assets/pieces/black queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))

black_rook = pygame.image.load('assets/pieces/black rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))

black_bishop = pygame.image.load('assets/pieces/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))

black_knight = pygame.image.load('assets/pieces/black knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))

black_pawn = pygame.image.load('assets/pieces/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))

white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
white_images_small = [white_pawn_small, white_queen_small, white_king_small, white_knight_small, white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
black_images_small = [black_pawn_small, black_queen_small, black_king_small, black_knight_small, black_rook_small, black_bishop_small]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

#check variables/flashing counter
counter = 0
winner = ''
game_over = False

#draw main game board
def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [700 - (column * 200), row * 100, 100, 100])
        #draw lines
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)

    pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
    pygame.draw.rect(screen, 'gray', [800, 0, 200, HEIGHT])
    pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
    pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)
    status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                    'Black: Select a Piece to Move!', 'Black: Select a Destination!']
    
    screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 820))
    #forefeit button
    screen.blit(medium_font.render('FOREFEIT', True, 'black'), (812, 830))

#draw the pieces
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_location[i][0] * 100 + 18, white_location[i][1] * 100 + 20))
        else:
            screen.blit(white_images[index], (white_location[i][0] * 100 + 10, white_location[i][1] * 100 + 10))
        #selection highlight
        if turn_step < 2:
            if  selection == i:
                pygame.draw.rect(screen, 'red', [white_location[i][0] * 100 + 1, white_location[i][1] * 100 + 1, 100, 100], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_location[i][0] * 100 + 18, black_location[i][1] * 100 + 20))
        else:
            screen.blit(black_images[index], (black_location[i][0] * 100 + 10, black_location[i][1] * 100 + 10))
        #selection highlight
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [black_location[i][0] * 100 + 1, black_location[i][1] * 100 + 1, 100, 100], 2)

#check function
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []

    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'knight':
             moves_list = check_knight(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list

#check valid king moves
def check_king(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_location
        friends_list = white_location
    else:
        enemies_list = white_location
        friends_list = black_location
    #8 tiles to check for king
    targets = [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)

    return moves_list

#check valid queen moves
def check_queen(position, color):
    #combination of bishop and rook valid moves
    moves_list = check_bishop(position, color)
    rook_list = check_rook(position, color)
    for i in rook_list:
        moves_list.append(i)
    return moves_list

#check valid bishop moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_location
        friends_list = white_location
    else:
        enemies_list = white_location
        friends_list = black_location
    
    for i in range(4): #up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False

    return moves_list

#check valid knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_location
        friends_list = white_location
    else:
        enemies_list = white_location
        friends_list = black_location
    #8 tiles to check for knights
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <=7:
            moves_list.append(target)

    return moves_list


#check valid rook moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_location
        friends_list = white_location
    else:
        enemies_list = white_location
        friends_list = black_location
    
    for i in range(4): #up, down, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = -1
        elif i == 1:
            x = 0
            y = 1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

    return moves_list
#check valid pawn moves
def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        #one tile move to front
        if (position[0], position[1] + 1) not in white_location and \
            (position[0], position[1] + 1) not in black_location and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
            #two tile move front from the starting position
            if (position[0], position[1] + 2) not in white_location and \
                (position[0], position[1] + 2) not in black_location and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
        #take diagonal left piece
        if (position[0] + 1, position[1] + 1) in black_location:
            moves_list.append((position[0] + 1, position[1] + 1))
        #take diagonal right piece
        if (position[0] - 1, position[1] + 1) in black_location:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        #one tile move to the front
        if (position[0], position[1] - 1) not in white_location and \
            (position[0], position[1] - 1) not in black_location and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
            #two tile move front from the starting position
            if (position[0], position[1] - 2) not in white_location and \
                (position[0], position[1] - 2) not in black_location and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
        #take diagonal left piece
        if (position[0] - 1, position[1] - 1) in white_location:
            moves_list.append((position[0] - 1, position[1] - 1))
        #take diagonal right piece
        if (position[0] + 1, position[1] - 1) in white_location:
            moves_list.append((position[0] + 1, position[1] - 1))
    return moves_list

#checkfor valid moves for selected piece
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options

#drawe valid moves on screen
def draw_valid(moves):
    for i in range(len(moves)):
        pygame.draw.circle(screen, 'red', (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)

#draw captured pieces
def draw_captured_pieces():
    for i in range(len(white_captured_pieces)):
        captured_piece = white_captured_pieces[i]
        index = piece_list.index(captured_piece)
        screen.blit(black_images_small[index], (825, 5 + 50 * i))
    for i in range(len(black_captured_pieces)):
        captured_piece = black_captured_pieces[i]
        index = piece_list.index(captured_piece)
        screen.blit(white_images_small[index], (925, 5 + 50 * i))

#draw check
def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_location[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_location[king_index][0] * 100 + 1, white_location[king_index][1] * 100 + 1, 100, 100], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_location[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [black_location[king_index][0] * 100 + 1, black_location[king_index][1] * 100 + 1, 100, 100], 5)

#draw game over
def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(f'{winner} Won the Game!', True, 'White'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart', True, 'White'), (210, 240))


    
black_options = check_options(black_pieces, black_location, 'black')
white_options = check_options(white_pieces, white_location, 'white')

#game loop
run = True
while run:
    #limiting the number of frames per second
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark grey')
    draw_board()
    draw_pieces()
    draw_captured_pieces()
    draw_check()

    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        #mousebuttondown handler
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coord = (x_coord, y_coord)

            if turn_step < 2:
                #forefeit button click
                if click_coord == (8, 8) or click_coord == (9, 8):
                    winner = 'black'
                if click_coord in white_location:
                    selection = white_location.index(click_coord)
                    if turn_step == 0:
                        turn_step = 1
                if click_coord in valid_moves and selection != 100:
                    white_location[selection] = click_coord
                    if click_coord in black_location:
                        black_piece = black_location.index(click_coord)
                        white_captured_pieces.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_location.pop(black_piece)
                    black_options = check_options(black_pieces, black_location, 'black')
                    white_options = check_options(white_pieces, white_location, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []

            else:
                #forefeit button click
                if click_coord == (8, 8) or click_coord == (9, 8):
                    winner = 'white'
                if click_coord in black_location:
                    selection = black_location.index(click_coord)
                    if turn_step == 2:
                        turn_step = 3
                if click_coord in valid_moves and selection != 100:
                    black_location[selection] = click_coord
                    if click_coord in white_location:
                        white_piece = white_location.index(click_coord)
                        black_captured_pieces.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_location.pop(white_piece)
                    black_options = check_options(black_pieces, black_location, 'black')
                    white_options = check_options(white_pieces, white_location, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
            
        #restart
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_location = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
                                (0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1)]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_location = [(0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7),
                                (0,6), (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (7,6)]
                white_captured_pieces = []
                black_captured_pieces = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_location, 'black')
                white_options = check_options(white_pieces, white_location, 'white')

    
    if winner != '':
            game_over = True
            draw_game_over()
                
    #updating screen
    pygame.display.flip()

#exiting out of pygame
pygame.quit()