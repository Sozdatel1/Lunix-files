import chess  # Если у вас нет библиотеки, см. примечание ниже

import random
from typing import List, Tuple, Optional

class SimpleChessEngine:
    """
    Простой шахматный движок на Python.
    Использует оценку материала и базовую эвристику.
    """

    # Оценка фигур (в сантипешках)
    PIECES_VALUE = {
        chess.PAWN: 100,
        chess.KNIGHT: 300,
        chess.BISHOP: 300,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0  # Король бесценен
    }

    def __init__(self, color: bool = chess.WHITE):
        self.color = color  # Цвет движка (WHITE/BLACK)

    def evaluate_board(self, board: chess.Board) -> int:
        """
        Оценивает позицию: разница материала + простые эвристики.
        Положительное число — преимущество белых.
        """
        score = 0

        # Материал
        for piece_type in self.PIECES_VALUE:
            score += len(board.pieces(piece_type, chess.WHITE)) * self.PIECES_VALUE[piece_type]
            score -= len(board.pieces(piece_type, chess.BLACK)) * self.PIECES_VALUE[piece_type]

        # Эвристика: активность (количество доступных ходов)
        if board.turn == chess.WHITE:
            score += len(list(board.legal_moves)) * 10
        else:
            score -= len(list(board.legal_moves)) * 10

        # Бонус за рокировку
        if board.has_kingside_castling_rights(chess.WHITE):
            score += 50
        if board.has_queenside_castling_rights(chess.WHITE):
            score += 50
        if board.has_kingside_castling_rights(chess.BLACK):
            score -= 50
        if board.has_queenside_castling_rights(chess.BLACK):
            score -= 50

        return score

    def get_legal_moves(self, board: chess.Board) -> List[chess.Move]:
        """Возвращает список легальных ходов."""
        return list(board.legal_moves)

    def sort_moves(self, board: chess.Board, moves: List[chess.Move]) -> List[chess.Move]:
        """
        Сортирует ходы по эвристике:
        1. Взятия фигур.
        2. Шахи.
        3. Остальные.
        """
        def move_score(move: chess.Move) -> int:
            score = 0
            # Взятие
            if board.is_capture(move):
                captured_piece = board.piece_at(move.to_square)
                if captured_piece:
                    score += self.PIECES_VALUE[captured_piece.piece_type]
            # Шах
            if board.gives_check(move):
                score += 100
            return score

        return sorted(moves, key=move_score, reverse=True)


    def minimax(self, board: chess.Board, depth: int, is_maximizing: bool) -> int:
        """
        Минимакс с фиксированной глубиной.
        Возвращает оценку позиции.
        """
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        legal_moves = self.get_legal_moves(board)
        if is_maximizing:
            max_eval = -float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, False)
                board.pop()
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, True)
                board.pop()
                min_eval = min(min_eval, eval)
            return min_eval

    def choose_move(self, board: chess.Board, depth: int = 2) -> Optional[chess.Move]:
        """
        Выбирает лучший ход по минимаксу.
        depth: глубина поиска (2–3 для быстрой игры).
        """
        legal_moves = self.sort_moves(board, self.get_legal_moves(board))
        best_move = None
        best_value = -float('inf') if board.turn == self.color else float('inf')


        for move in legal_moves:
            board.push(move)
            board_value = self.minimax(board, depth - 1, board.turn != self.color)
            board.pop()

            if board.turn == self.color:  # Наш цвет
                if board_value > best_value:
                    best_value = board_value
                    best_move = move
            else:  # Противник
                if board_value < best_value:
                    best_value = board_value
                    best_move = move

        return best_move



# Пример использования
if __name__ == "__main__":
    # Создаём доску
    board = chess.Board()

    # Создаём движок (играет за белых)
    engine = SimpleChessEngine(color=chess.WHITE)

    print("Начальная позиция:")
    print(board)

    # Делаем 5 ходов
    for i in range(5):
        if board.is_game_over():
            break

        move = engine.choose_move(board, depth=2)
        if move:
            print(f"Ход {i+1}: {move}")
            board.push(move)
            print(board)
        else:
            print("Нет доступных ходов")
            break
