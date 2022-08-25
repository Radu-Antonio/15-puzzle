import pygame, random, time, os

pygame.init()
HELP = DONE = False
offset = 125
imageSize = 250
pygame.display.set_caption('15 puzzle')
screen = pygame.display.set_mode((1000, 1000))
font = pygame.font.Font(pygame.font.get_default_font(), 68)
solution = [[ 1,  2,  3,  4],
            [ 5,  6,  7,  8],
            [ 9, 10, 11, 12],
            [13, 14, 15, 16]]
table = {}
os.chdir(os.path.dirname(__file__) + '\\images')

def isSolvable(arr):
    inversions = 0
    poz16 = arr.index(16)
    for i in range(16):
        for j in range(i + 1, 16):
            if j == poz16 or i == poz16:
                continue
            if arr[i] > arr[j]:
                inversions += 1

    even_rows = arr[:4] + arr[8:12]
    odd_rows = arr[4:8] + arr[12:]
    return bool(inversions % 2 and 16 in even_rows or inversions % 2 == 0 and 16 in odd_rows)

def setBoard():
    global table
    image = pygame.image.load(random.choice(os.listdir()))
    slices = [image.subsurface((imageSize * j + 5, imageSize * i + 5, imageSize - 5, imageSize - 5)) for i in range(4) for j in range(4)]
    table = {i + 1: slices[i] for i in range(len(slices))}

    board = []
    arr = list(range(1, 17))
    random.shuffle(arr)

    while not isSolvable(arr):
        random.shuffle(arr)

    for i in range(4):
        board.append(arr[i * 4:(i + 1) * 4])
    return board

def isWin(board):
    global DONE
    DONE = (board == solution)
    return DONE

def get16poz(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 16:
                return i, j

def updateBoard(board, pos):
    y, x = pos[0] // 250, pos[1] // 250
    if board[x][y] == 16:
        return

    x_0, y_0 = get16poz(board)
    if x_0 == x:
        inc = 1 if y_0 < y else -1
        for i in range(y_0, y, inc):
            board[x][i] = board[x][i + inc]
        board[x][y] = 16
    elif y_0 == y: 
        inc = 1 if x_0 < x else -1
        for i in range(x_0, x, inc):
            board[i][y] = board[i + inc][y]
        board[x][y] = 16

def draw(board):
    global table, imageSize, HELP
    screen.fill((41, 91, 137))
    textSize = 250

    for i in range(4):
        for j in range(4):
            index = board[i][j]
            if index == 16:
                continue

            screen.blit(table[index], (j * imageSize + 3, i * imageSize + 3))
            if HELP:
                text = font.render(str(index), True, (255, 255, 255))
                textRect = text.get_rect()
                textRect.center = (textSize * j + offset, textSize * i + offset)
                screen.blit(text, textRect)

def displayTime(start, curr):
    minute, sec = int((curr - start) // 60), int((curr - start) % 60)
    minute, sec = '0'+ str(minute) if minute < 10 else minute, '0' + str(sec) if sec < 10 else sec
    text = pygame.font.Font(pygame.font.get_default_font(), 30).render(f"{minute}:{sec}", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (55, 25)
    screen.blit(text, textRect)

def drawWin():
    text = pygame.font.Font(pygame.font.get_default_font(), 80).render('Click to play again', True, (32, 149, 5))
    textRect = text.get_rect()
    textRect.center = (500, 500)
    screen.blit(text, textRect)

def main():
    global DONE, table, imageSize, HELP
    board = setBoard()
    start = time.time()
    
    while True:
        if not DONE:
            draw(board)
            displayTime(start, time.time())
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                HELP = not HELP

            if event.type == pygame.MOUSEBUTTONUP:
                if not DONE:
                    pos = pygame.mouse.get_pos()
                    updateBoard(board, pos)

                    if isWin(board):
                        draw(board)
                        displayTime(start, time.time())
                        drawWin()
                else:
                    board = setBoard()
                    start = time.time()
                    DONE = False
        pygame.display.update()

if __name__ == '__main__':
    main()