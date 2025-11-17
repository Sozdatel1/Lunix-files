import pygame
import chess

pygame.init()

# Размеры окна и клетки
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (245, 222, 179)
DARK_BROWN = (139, 69, 19)
HIGHLIGHT = (0, 255, 0)

# Инициализация дисплея
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Шахматы")

# Загрузка изображений фигур
piece_images = {}

def load_images():
    pieces = ['p', 'r', 'n', 'b', 'q', 'k']
    for piece in pieces:
        piece_images[piece + 'w'] = pygame.transform.scale(pygame.image.load(f'images/{piece}w.png'), (SQUARE_SIZE, SQUARE_SIZE))
        piece_images[piece + 'b'] = pygame.transform.scale(pygame.image.load(f'images/{piece}b.png'), (SQUARE_SIZE, SQUARE_SIZE))
        
# Обратите внимание: Убедитесь, что у вас есть папка 'images' с изображениями фигур
# Например: 'images/pw.png', 'images/rb.png' и т.д.
# Или замените путь на свои изображения

# Для теста, если изображений нет, можно оставить заглушки или рисовать фигуры позже

board = chess.Board()
selected_square = None
legal_moves = []

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)
            
            # Подсветка выбранной клетки
            if selected_square == (row, col):
                pygame.draw.rect(screen, HIGHLIGHT, rect, 3)

            # Отрисовка фигур
            square_index = row * 8 + col
            square = chess.square(col, 7 - row)  # chess использует поле с a1 внизу
            piece = board.piece_at(square)
            if piece:
                color_prefix = 'w' if piece.color == chess.WHITE else 'b'
                symbol = piece.symbol().lower()
                key = symbol + color_prefix
                if key in piece_images:
                    screen.blit(piece_images[key], rect.topleft)
                else:
                    # Заглушка: рисуем кружочек для фигуры
                    pygame.draw.circle(screen, BLACK, rect.center, SQUARE_SIZE//3)

def get_square(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    # Обратный порядок, так как chess использует a1 внизу
    square = chess.square(col, 7 - row)
    return (row, col), square

def main():
    load_images()
    global selected_square, legal_moves
    running = True
    clock = pygame.time.Clock()

    while running:
        draw_board()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                (row, col), square = get_square(pos)
                piece = board.piece_at(square)

                # Выбор фигуры
                if piece:
                    selected_square = (row, col)
                # Попытка сделать ход
                elif selected_square:
                    move = chess.Move.from_uci(
                        chess.square_name(chess.square(selected_square[1], 7 - selected_square[0])) +
                        chess.square_name(square)
                    )
                    # Проверяем легальный ли ход
                    if move in board.legal_moves:
                        # Проверка на ход за текущего игрока
                        if (board.turn == chess.WHITE and board.piece_at(chess.square(selected_square[1], 7 - selected_square[0])).color == chess.WHITE) or \
                           (board.turn == chess.BLACK and board.piece_at(chess.square(selected_square[1], 7 - selected_square[0])).color == chess.BLACK):
                            board.push(move)
                    selected_square = None

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
