from BoardGraph import BoardGraph
from Board import Board


def main():
    board_graph = BoardGraph()

    board = Board(board_graph)

    board.render()


if __name__ == "__main__":
    main()
