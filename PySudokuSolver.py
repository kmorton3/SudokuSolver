import sys
import time
import collections

from functools import partial

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QApplication, QDialog, QDialogButtonBox
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QPushButton

__version__ = '0.1'
__author__ = 'Keith Morton'


starting_board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

practice_board = [
    [0, 0, 6, 0, 0, 0, 0, 0, 1],
    [0, 7, 0, 0, 6, 0, 0, 5, 0],
    [8, 0, 0, 1, 0, 3, 2, 0, 0],
    [0, 0, 5, 0, 4, 0, 8, 0, 0],
    [0, 4, 0, 7, 0, 2, 0, 9, 0],
    [0, 0, 8, 0, 1, 0, 7, 0, 0],
    [0, 0, 1, 2, 0, 5, 0, 0, 3],
    [0, 6, 0, 0, 7, 0, 0, 8, 0],
    [2, 0, 0, 0, 0, 0, 4, 0, 0]
]


def fill_in_board(board):
    new_board = []
    for i in range(len(board)):
        new_board.append(board[i].copy())
        # for j in range(len(board[0])):
        #     new_board[i].append(board[i][j])
    return new_board


def is_empty_square(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                # print("Found empty square at %i, %i" % (i, j))
                return True
    return False


def empty_square(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j
    return None


def is_valid(board, square, value):
    # Row
    for i in range(len(board)):
        if board[square[0]][i] == value:
            # print("Value %i doesn't work in row %i" % (value, square[0]))
            return False

    # Column
    for j in range(len(board[square[0]])):
        if board[j][square[1]] == value:
            # print("Value %i doesn't work in column %i" % (value, square[1]))
            return False

    # Big Square
    row = square[0] // 3
    column = square[1] // 3

    for i in range(row * 3, row * 3 + 3):
        for j in range(column * 3, column * 3 + 3):
            if board[i][j] == value:
                # print("Value %i doesn't work in big square range %i, %i" % (value, row, column))
                return False

    return True


def fill_square(board, square):
    solved = False
    for i in range(1, len(board) + 1):
        if is_valid(board, square, i):
            # print("Putting value: %i at location %i, %i" % (i, square[0], square[1]))
            board[square[0]][square[1]] = i
            if is_empty_square(board):
                new_square = empty_square(board)
                solved = fill_square(board, new_square)
            else:
                return True
    if solved:
        return solved
    else:
        # print("No value worked at %i, %i. Going back." % (square[0], square[1]))
        board[square[0]][square[1]] = 0


def sudoku_solver():
    solved = False
    ending_board = fill_in_board(practice_board)
    if is_empty_square(ending_board):
        square = empty_square(ending_board)
        solved = fill_square(ending_board, square)
    if solved:
        print("Solved puzzle and here is the puzzles:")
        for r in range(len(practice_board)):
            print(practice_board[r])
        print("")
        for row in range(len(ending_board)):
            print(ending_board[row])
    else:
        print("Couldn't solve puzzle.")


class PySudokuSolverDialog(QDialog):
    """Dialog"""
    def __init__(self, parent=None):
        """Initializer"""
        super().__init__(parent)
        self.setWindowTitle('Sudoku Solver Error')
        dlgLayout = QVBoxLayout()
        self.lineEdit = QLineEdit()
        self.lineEdit.setReadOnly(True)

        btn = QDialogButtonBox.StandardButton.Ok
        self.buttonBox = QDialogButtonBox(btn)
        self.buttonBox.accepted.connect(self.accept)

        dlgLayout.addWidget(self.lineEdit)
        dlgLayout.addWidget(self.buttonBox)
        self.setLayout(dlgLayout)


    def addText(self, text):
        self.lineEdit.setText(text)


class PySudokuSolverUi(QMainWindow):
    """PySudokuSolver's View (GUI)"""
    def __init__(self):
        """View initializer"""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('PySudokuSolver')
        self.setFixedSize(290, 400)
        # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # Create the buttons and board
        self.createBoard()
        self.createButtons()

    def createBoard(self):
        """Create the board"""
        boardLayout = QGridLayout()
        boardLayout.setSpacing(0)
        validator = QIntValidator(1, 9)
        self.boardSpaces = collections.OrderedDict()
        for i in range(9):
            for j in range(9):
                self.boardSpaces[(i, j)] = QLineEdit()
                self.boardSpaces[(i, j)].setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.boardSpaces[(i, j)].setFixedSize(30, 30)
                self.boardSpaces[(i, j)].setFrame(True)
                #self.boardSpaces[(i, j)].setText(f'{i}{j}')
                self.boardSpaces[(i, j)].setMaxLength(1)
                # self.boardNumbers[con].setInputMask("D")
                self.boardSpaces[(i, j)].setValidator(validator)
                self.applyDefaultColoringToSpace((i, j), self.boardSpaces[(i, j)])
                boardLayout.addWidget(self.boardSpaces[(i, j)], i, j)
        # Add board layout to the general layout
        self.generalLayout.addLayout(boardLayout)
        self.setUpBoardColors()

    def setUpBoardColors(self):
        for i in range(9):
            for j in range(9):
                self.applyDefaultColoringToSpace((i, j), self.boardSpaces[i, j])

    def applyDefaultColoringToSpace(self, coord, space):
        if coord[0] // 3 in (0, 2) and coord[1] // 3 in (0, 2):
            space.setStyleSheet('background-color: rgb(200, 200, 200);'
                                'color: black;')
        elif coord[0] // 3 == 1 and coord[1] // 3 == 1:
            space.setStyleSheet('background-color: rgb(200, 200, 200);'
                                'color: black;')
        else:
            space.setStyleSheet('background-color: white;'
                                'color: black')

    def applySolvedColoringToSpace(self, coord, space):
        if coord[0] // 3 in (0, 2) and coord[1] // 3 in (0, 2):
            space.setStyleSheet('background-color: red;'
                                'color: black')
        elif coord[0] // 3 == 1 and coord[1] // 3 == 1:
            space.setStyleSheet('background-color: red;'
                                'color: black')
        else:
            space.setStyleSheet('background-color: rgb(255, 255, 0);'
                                'color: black')

    def buildSingleBorderOnSpecificSpace(self, space, location):
        space.setStyleSheet(f'border-{location}-width: 1px;'
                            f'border-{location}-color: black;'
                            f'border-{location}-style: solid;')

    def createButtons(self):
        """Create the buttons"""
        self.buttons = {}
        self.solve = 'Solve'
        self.reset = 'Reset'
        self.clear = 'Clear'
        self.buttons[self.solve] = QPushButton('Solve Board')
        self.buttons[self.reset] = QPushButton('Reset Board')
        self.buttons[self.clear] = QPushButton('Clear User Input')
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.buttons[self.solve])
        buttonLayout.addWidget(self.buttons[self.reset])
        buttonLayout.addWidget(self.buttons[self.clear])
        self.generalLayout.addLayout(buttonLayout)

    def resetBoard(self):
        """Reset board"""
        for coord, boardSpot in self.boardSpaces.items():
            boardSpot.setText("")
            boardSpot.setReadOnly(False)
            self.applyDefaultColoringToSpace(coord, boardSpot)

    def clearBoard(self):
        """Clears board of input from user"""
        for coord, boardSpot in self.boardSpaces.items():
            if not boardSpot.isReadOnly():
                boardSpot.setText("")
                self.applyDefaultColoringToSpace(coord, boardSpot)


class PySudokuSolverMdl:
    """PySudokuSolver's Model class"""
    def __init__(self):
        pass


class PySudokuSolverCtrl:
    """PySudokuSolver's Controller class"""
    def __init__(self, model, view):
        """Controller initializer"""
        self.model = model
        self.view = view
        # Connect signals and slots
        self.connectSignals()

    def hasEmptySquare(self, boardSpaces):
        for coord, space in boardSpaces.items():
            if len(space.text()) < 1 or int(float(space.text())) < 1:
                return True
        return False

    def getEmptySquare(self, boardSpaces):
        for coord, space in boardSpaces.items():
            if len(space.text()) < 1 or int(float(space.text())) < 1:
                return coord, space
        return None

    def isValid(self, coord, value, boardSpaces):
        # Row
        for i in range(9):
            if coord[1] != i:
                if len(boardSpaces[coord[0], i].text()) > 0 and int(float(boardSpaces[coord[0], i].text())) == value:
                    return False

        # Column
        for j in range(9):
            if coord[0] != j:
                if len(boardSpaces[j, coord[1]].text()) > 0 and int(float(boardSpaces[j, coord[1]].text())) == value:
                    return False

        # Big Square
        row = coord[0] // 3
        column = coord[1] // 3

        for i in range(row * 3, row * 3 + 3):
            for j in range(column * 3, column * 3 + 3):
                if coord[0] != i and coord[1] != j:
                    if len(boardSpaces[i, j].text()) > 0 and int(float(boardSpaces[i, j].text())) == value:
                        return False

        return True

    def changeColor(self, space, bgColor, fColor):
        space.setStyleSheet("""QLineEdit { background-color: %s; color: %s }""" % (bgColor, fColor))
        space.update()
        space.setFocus()
        time.sleep(0.005)
        b = QLineEdit




    def fillInSpace(self, coord, space, boardSpaces):
        solved = False
        for i in range(1, 10):
            if self.isValid(coord, i, boardSpaces):
                space.setText(str(i))
                self.view.applySolvedColoringToSpace(coord, space)

                if self.hasEmptySquare(boardSpaces):
                    newCoord, newSpace = self.getEmptySquare(boardSpaces)
                    solved = self.fillInSpace(newCoord, newSpace, boardSpaces)
                else:
                    return True

        if solved:
            return solved
        else:
            space.setText("")
            self.view.applyDefaultColoringToSpace(coord, space)

    def changeReadOnlyOnFilledInSquares(self, spaces, readOnly):
        for coord, space in spaces.items():
            if len(space.text()) > 0 and float(space.text()) > 0:
                space.setReadOnly(readOnly)

    def canContinueAfterPreCheck(self, boardSpaces):
        print('Checking Puzzle')
        for coord, space in boardSpaces.items():
            if len(space.text()) > 0 and float(space.text()) > 0:
                if not self.isValid(coord, int(float(space.text())), boardSpaces):
                    return False
        return True


    def solvePuzzle(self, boardSpaces):
        solved = False
        if not self.canContinueAfterPreCheck(boardSpaces):
            print('Error out')
            dialog = PySudokuSolverDialog()
            dialog.addText('ERROR with puzzle can\'t solve')
            dialog.exec()
        elif self.hasEmptySquare(boardSpaces):
            self.changeReadOnlyOnFilledInSquares(boardSpaces, True)
            coord, space = self.getEmptySquare(boardSpaces)
            solved = self.fillInSpace(coord, space, boardSpaces)

            if solved:
                dialog = PySudokuSolverDialog()
                dialog.addText('Complete and solved')
                dialog.exec()
            else:
                self.changeReadOnlyOnFilledInSquares(boardSpaces, False)
                dialog = PySudokuSolverDialog()
                dialog.addText('ERROR, could not solve')
                dialog.exec()

    # def checkPuzzleBeforeSolving(self):
    #     print('Checking Puzzle')
    #     boardSpaces = self.view.boardSpaces
    #     notFirstTime = False
    #     canContinueToSolve = True
    #     for coord, space in boardSpaces.items():
    #         if len(space.text()) > 0 and float(space.text()) > 0:
    #             notFirstTime = True
    #             if not self.model.isValid(coord, int(float(space.text())), boardSpaces):
    #                 canContinueToSolve = False
    #
    #     if notFirstTime and canContinueToSolve:
    #         print('Solving Puzzle')
    #         self.model.solvePuzzle(boardSpaces)
    #     elif notFirstTime:
    #         print('Error out')
    #         dialog = PySudokuSolverDialog()
    #         dialog.addText('ERROR, did not try to solve puzzle because'
    #                        '\nthere is an error with board as is. '
    #                        '\nFix error and try again.')
    #         dialog.close(dialog.show)
    #     else:
    #         print('First Time')
    #         pass

    def connectSignals(self):
        """Connect signals and slots"""
        boardSpaces = self.view.boardSpaces
        # Buttons
        self.view.buttons[self.view.solve].clicked.connect(partial(self.solvePuzzle, boardSpaces))
        # self.view.buttons[self.view.solve].clicked.connect(self.checkPuzzleBeforeSolving())
        self.view.buttons[self.view.clear].clicked.connect(self.view.clearBoard)
        self.view.buttons[self.view.reset].clicked.connect(self.view.resetBoard)

        # Board squares
        for number, boardSpot in self.view.boardSpaces.items():
            pass


# Client code
def main():
    """Main Function"""
    # Create an instance of QApplication
    pysudoku = QApplication(sys.argv)
    # Show the sudoku's GUI
    view = PySudokuSolverUi()
    view.show()
    # Create instances of the model and the controller
    model = PySudokuSolverMdl()
    PySudokuSolverCtrl(model, view)
    # Execute the sudoku's main loop
    sys.exit(pysudoku.exec())


if __name__ == '__main__':
    main()
    # sudoku_solver()
