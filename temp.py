class Class:
    @staticmethod
    def init():
        print('Hello World')


def function():
    raise NotImplementedError


if __name__ == '__main__':
    function = Class().init
    function()