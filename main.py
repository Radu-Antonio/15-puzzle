import pygame, random, time

pygame.init()

LIGHT_GREEN = (40, 180, 51)
GRAY = (110, 110, 110)
DONE = False
WIDTH, HEIGHT = 1000, 1000
offset = HEIGHT // 8
pygame.display.set_caption('15 puzzle')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(pygame.font.get_default_font(), 72)

solution = [[ '1',  '2',  '3',  '4'],
            [ '5',  '6',  '7',  '8'],
            [ '9', '10', '11', '12'],
            ['13', '14', '15',  '0']]

def isSolvable(arr):
    inversions = 0
    poz0 = arr.index('0')
    for i in range(16):
        for j in range(i + 1, 16):
            if j == poz0:
                continue
            if int(arr[i]) > int(arr[j]):
                inversions += 1

    even_rows = arr[:4] + arr[8:12]
    odd_rows = arr[4:8] + arr[12:]
    return bool(inversions % 2 and '0' in even_rows) or bool(inversions % 2 == 0 and '0' in odd_rows)

def setBoard():
    board, n = [], 4
    arr = list(map(str, range(16)))
    random.shuffle(arr)

    while not isSolvable(arr):
        random.shuffle(arr)

    for i in range(n):
        board.append(arr[i * n:(i + 1) * n])
    return board

def isWin(board):
    global DONE
    DONE = (board == solution)
    return DONE

def get0poz(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == '0':
                return i, j

def updateBoard(board, pos):
    y, x = pos[0] // 250, pos[1] // 250
    if board[x][y] == '0':
        return

    x_0, y_0 = get0poz(board)
    if x_0 == x: 
        inc = 1 if y_0 < y else -1
        for i in range(y_0, y, inc):
            board[x][i] = board[x][i + inc]
        board[x][y] = '0'
        return

    if y_0 == y: 
        inc = 1 if x_0 < x else -1
        for i in range(x_0, x, inc):
            board[i][y] = board[i + inc][y]
        board[x][y] = '0'

def draw(board):
    screen.fill((255, 255, 255))
    n = len(board)
    textSize = HEIGHT / n

    for x in range(n):
        for y in range(n):
            if board[x][y] == '0':
                continue

            color = LIGHT_GREEN if x * 4 + y + 1 == int(board[x][y]) else GRAY
            pygame.draw.rect(screen, color, (250 * y + 3, 250 * x + 3, 244, 244))
            text = font.render(board[x][y], True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (textSize * y + offset, textSize * x + offset)
            screen.blit(text, textRect)

def displayTime(start, curr):
    minute, sec = int((curr - start) // 60), int((curr - start) % 60)
    minute, sec = '0' + str(minute) if minute < 10 else minute, '0' + str(sec) if sec < 10 else sec
    text = pygame.font.Font(pygame.font.get_default_font(), 30).render(f"{minute}:{sec}", True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (55, 25)
    screen.blit(text, textRect)

def drawWin():
    text = pygame.font.Font(pygame.font.get_default_font(), 80).render('Click to play again', True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (500, 500)
    screen.blit(text, textRect)

def main():
    global DONE
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