import traceback


class Logger:
    def __init__(self):
        self.path = 'D:/AI/ProjectFinal/mine/pbrain-alphabeta.log'
        with open(self.path, 'w') as file:
            pass

    def log(self, text):
        with open(self.path, 'a') as file:
            file.write(text)
            file.write('\n')
            file.flush()

    def crash(self):
        with open(self.path, 'a') as file:
            traceback.print_exc(file = file)
            file.flush()
        raise Exception