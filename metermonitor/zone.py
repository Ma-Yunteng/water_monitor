class Zone:
    def __init__(self, x, y, size):
        self.__x = x
        self.__y = y
        self.__w = size
        self.__h = size
        self.__hot = None

    def __repr__(self):
        return '[' + str(self.__x) + ',' + str(self.__y) + '] (' + str(self.__w) + 'x' + str(self.__h) + ')' + str(self.__hot)

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

    def raw(self):
        return self.x(), self.y(), self.w(), self.h()
