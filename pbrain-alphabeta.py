# Special thanks to Yiwei Ding as well as his GitHub repo
# https://github.com/suncerock/AI_final_project

# the command to build an executable file
# pyinstaller pbrain-alphabeta.py pisqpipe.py --name pbrain-alphabeta.exe --onefile


import pisqpipe as pp
# from pisqpipe import DEBUG_EVAL, DEBUG
from board import AlphaBetaBoard


if __name__ == '__main__':
    board = AlphaBetaBoard()

    pp.infotext = "pbrain-alphabeta, Wang Yiqun"
    pp.brain_init = board.init
    pp.brain_restart = board.restart
    pp.brain_turn = board.turn
    pp.brain_my = board.my
    pp.brain_opponents = board.opponents
    pp.brain_block = board.block
    pp.brain_takeback = board.takeback
    pp.brain_end = board.end
    pp.brain_eval = board.eval
    pp.brain_about = board.about

    pp.main()
