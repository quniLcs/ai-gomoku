import traceback


class Logger:
    def __init__(self):
        self.path = 'D:/AI/ProjectFinal/mine/pbrain-alphabeta.log'
        with open(self.path, 'w') as file:
            pass

    def info(self, text):
        with open(self.path, 'a') as file:
            file.write(text)
            file.write('\n')
            file.flush()

    def exception(self):
        with open(self.path, 'a') as file:
            traceback.print_exc(file = file)
            file.flush()
        raise Exception


if __name__ == '__main__':
    logger = Logger()
    logger.info('Hello World!')