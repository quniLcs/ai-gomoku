class Class:
    @staticmethod
    def init():
        print("Hello World in a class")


def function():
    print("Hello World in a function")


if __name__ == '__main__':
    function = Class().init
    function()