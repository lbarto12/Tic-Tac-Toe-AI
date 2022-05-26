import numpy
import sys
from tqdm import tqdm

class BoardNode:

    # board node construtor, takes previous board
    def __init__(self, previous_board = None):
        self.slots = previous_board or [[' '] * 3] * 3
        self.children = []
        self.turn = 'X'



    def check_state(self):
        if self.size() == 9 and not self.has_winner():
            return 'tie'
        if self.has_winner() and not self.x_won():
            return 'O'
        if self.has_winner():
            return 'X'
        return None

    def x_won(self):
        b = self.slots
        return (
                b[0][0] == b[0][1] == b[0][2] == 'X' or
                b[1][0] == b[1][1] == b[1][2] == 'X' or
                b[2][0] == b[2][1] == b[2][2] == 'X' or
                b[0][0] == b[1][0] == b[2][0] == 'X' or
                b[0][1] == b[1][1] == b[2][1] == 'X' or
                b[0][2] == b[1][2] == b[2][2] == 'X' or
                b[0][0] == b[1][1] == b[2][2] == 'X' or
                b[2][0] == b[1][1] == b[0][2] == 'X'
        )

    # checks if the board has a winner
    def has_winner(self):
        b = self.slots
        return (
            b[0][0] == b[0][1] == b[0][2] != ' ' or
            b[1][0] == b[1][1] == b[1][2] != ' ' or
            b[2][0] == b[2][1] == b[2][2] != ' ' or
            b[0][0] == b[1][0] == b[2][0] != ' ' or
            b[0][1] == b[1][1] == b[2][1] != ' ' or
            b[0][2] == b[1][2] == b[2][2] != ' ' or
            b[0][0] == b[1][1] == b[2][2] != ' ' or
            b[2][0] == b[1][1] == b[0][2] != ' '
        )

    # gets number of slots filled on board, used later for determining ties
    def size(self):
        return len([j for i in self.slots for j in i if j in {'X', 'O'}])

    def __eq__(self, other):
        return numpy.array_equal(self.slots, other)

    # convert board to visual print-out
    def __str__(self):
        return '\n' + f'\n{"-" * 9}\n'.join([' | '.join(i) for i in self.slots]) + '\n'


    # joins multiple boards, so they are diplayed horizontally
    # this was really fun to program
    @staticmethod
    def join(nodes):
        nodes = [str(i).split('\n') for i in nodes]
        result = ""
        for i in range(6):
            result += '     '.join([nodes[j][i] for j in range(len(nodes))]) + '\n'
        return result




# DS that stores the node tree
class GameTree:

    # constructor init root and size, builds tree
    def __init__(self):
        self.root = BoardNode()
        self.size = 0
        self.build_tree(self.root)
        self.current_state = self.root

    # build tree function, recursive
    def build_tree(self, node: BoardNode):
        if node.size() == 9 or node.has_winner():
            return

        for i, row in enumerate(node.slots):
            for j, val in enumerate(row):
                if val == ' ':
                    new = [row[:] for row in node.slots]
                    new[i][j] = node.turn
                    new = BoardNode(new)
                    new.turn = 'O' if node.turn == 'X' else 'X'
                    self.build_tree(new)
                    node.children += [new]
                    self.size += 1


    # breadth first traversal
    # queue makes it kinda wonky
    def breadth_first(self):
        q = [self.root]
        while q:
            current = q.pop(0)
            print(current)
            if input('Next node? (y/n): ').lower() == 'n':
                terminate()

            for child in current.children:
                q.append(child)


    # depth first traversal
    def depth_first(self, node = None):
        if not node:
            node = self.root

        print(f'\n\ncurrent node:\n'
              f'{"=" * 30}\n'
              f'{node}\n'
              f'{"=" * 30}\n')

        if input('See Children? (y/n): ').lower() == 'n':
            terminate()

        print(BoardNode.join(node.children))

        for child in node.children:
            self.depth_first(child)



    def get_best_move(self, board):
        best_score = -10000
        best_move = None
        for child in board.children:
            score = self.minimax(child, 1, False)
            if score > best_score:
                best_score = score
                best_move = child
        return best_move

    scores = {
        'O': 1,
        'X': -1,
        'tie': 0
    }

    def minimax(self, board, depth, is_maxim):
        if not board.children:
            return GameTree.scores.get(board.check_state()) / (depth + 1)

        bestscore = -100 if is_maxim else 100
        for child in board.children:
            score = self.minimax(child, depth + 1, not is_maxim)
            bestscore = max(bestscore, score) if is_maxim else min(bestscore, score)

        return bestscore


    def play(self):
        board = self.root

        print(board)

        opts = {
            'X': ('X wins!', True),
            'O': ('O wins!', True),
            'tie': ('Tie!', True),
            None: ('', False)
        }

        def checkwinandexec():
            state = board.check_state()
            print(opts.get(state)[0], '\n\n')
            return opts.get(state)[1]



        while True:
            print('Your Turn:')
            move = input('move: ')
            move = [int(i) - 1 for i in move.split(' ')]
            new = [row[:] for row in board.slots]
            new[move[1]][move[0]] = 'X'
            new = BoardNode(new)

            for i in board.children:
                if new.slots == i.slots:
                    board = i
                    print(board)
                    break

            if checkwinandexec():
                break


            # print("+" * 50)
            # print("moved board to: ")
            # print(board)
            # print("children are: ")
            # print(BoardNode.join(board.children))
            # for i in board.children:
            #     print(self.minimax(i, 0, True), end='\t')
            # print("+" * 50)

            board = self.get_best_move(board)
            print('AIs turn:')
            print(board)


            if checkwinandexec():
                break















# termination function, because for some unknown reason exit takes a while.
def terminate():
    print('terminating...')
    sys.exit(1)



if __name__ == '__main__':
    print('Building Tree...')
    tree = GameTree()
    print('Done!\n')

    # 'Game' loop
    while True:
        traversal_style = input("how would you like to continue? (breadth | depth | play | exit): ")
        {
            'breadth': tree.breadth_first,
            'depth': tree.depth_first,
            'play': tree.play,
            'exit': terminate
        }.get(traversal_style.lower())()
