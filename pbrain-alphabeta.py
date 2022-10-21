# Special thanks to Yiwei Ding as well as his GitHub repo
# https://github.com/suncerock/AI_final_project

# the command to build an executable file
# pyinstaller pbrain-alphabeta.py pisqpipe.py --name pbrain-alphabeta.exe --onefile


import pisqpipe as pp
# from pisqpipe import DEBUG_EVAL, DEBUG
# from logger import Logger
from board import Board
from agent import AlphaBetaAgent


def brain_init():
    global board
    board = Board(pp.width, pp.height)
    if board.width < 5 or board.height < 5:
        pp.pipeOut("ERROR size of the board")
    else:
        pp.pipeOut("OK")


def brain_restart():
    global board
    del board
    brain_init()


def brain_turn():
    agent = AlphaBetaAgent(board)
    x, y = agent.search()
    pp.do_mymove(x, y)


def brain_my(x, y):
    if board.valid_move(x, y):
        board.make_move(x, y, 1)
    else:
        pp.pipeOut("ERROR my move (%d, %d)" % (x, y))


def brain_opponents(x, y):
    if board.valid_move(x, y):
        board.make_move(x, y, 2)
    else:
        pp.pipeOut("ERROR opponent's move (%d, %d)" % (x, y))


def brain_block(x, y):
    pass


def brain_takeback(x, y):
    raise NotImplementedError


def brain_end():
    pass


def brain_eval(x, y):
    pass


def brain_about():
    pp.pipeOut(pp.infotext)


if __name__ == '__main__':
    # logger = Logger()

    pp.infotext = 'pbrain-alphabeta, Wang Yiqun'
    pp.brain_init = brain_init
    pp.brain_restart = brain_restart
    pp.brain_turn = brain_turn
    pp.brain_my = brain_my
    pp.brain_opponents = brain_opponents
    pp.brain_block = brain_block
    pp.brain_takeback = brain_takeback
    pp.brain_end = brain_end
    pp.brain_eval = brain_eval
    pp.brain_about = brain_about

    pp.main()
    # try:
    #     pp.main()
    # except:
    #     logger.error()
