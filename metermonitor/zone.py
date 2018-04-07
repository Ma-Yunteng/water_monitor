class Zone:
    def __init__(self, x, y, size):
        self.__x = x
        self.__y = y
        self.__w = size
        self.__h = size
        self.__hot = None

    def x(self):
        return self.__x

    def y(self):
        return self.__y

    def w(self):
        return self.__w

    def h(self):
        return self.__h

    def is_hot(self):
        return self.__hot

    def update(self, is_hot):
        self.__hot = is_hot
