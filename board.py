# from logger import Logger


class Board:
    shape_score = {
        'one'           : 10,
        'two'           : 100,
        'three'         : 1000,
        'four'          : 10000,
        'five'          : 100000,
        'blocked_one'   : 1,
        'blocked_two'   : 10,
        'blocked_three' : 100,
        'blocked_four'  : 1000
    }
    # logger = Logger()

    def __init__(self, width = 20, height = 20):
        self.height = height
        self.width = width

        self.chess1 = []
        self.chess2 = []

        self.board = [[0 for i in range(height)] for j in range(width)]
        self.score1 = [[0 for i in range(height)] for j in range(width)]
        self.score2 = [[0 for i in range(height)] for j in range(width)]

        for i in range(width):
            for j in range(height):
                if i == 0 and j == 0 or i == 0 and j == self.height or \
                        j == 0 and i == self.width or i == self.width and j == self.height:
                    self.score1[i][j] = 3 * self.shape_score['blocked_one']
                    self.score2[i][j] = 3 * self.shape_score['blocked_one']
                elif i == 0 or j == 0 or i == self.width or j == self.height:
                    self.score1[i][j] = self.shape_score['one'] + 3 * self.shape_score['blocked_one']
                    self.score2[i][j] = self.shape_score['one'] + 3 * self.shape_score['blocked_one']
                else:
                    self.score1[i][j] = 4 * self.shape_score['one']
                    self.score2[i][j] = 4 * self.shape_score['one']

    def valid_move(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height and self.board[x][y] == 0

    def make_move(self, x, y, z):
        assert z == 1 or z == 2
        if z == 1:
            self.chess1.append((x, y))
        else:  # z == 2
            self.chess2.append((x, y))
        self.board[x][y] = z
        return self.update_score_around(x, y)

    def take_back(self, z, original_score1, original_score2):
        assert z == 1 or z == 2
        if z == 1:
            x, y = self.chess1.pop()
        else:  # z == 2
            x, y = self.chess2.pop()
        self.board[x][y] = 0
        for x, y in original_score1.keys():
            self.score1[x][y] = original_score1[(x, y)]
        for x, y in original_score2.keys():
            self.score2[x][y] = original_score2[(x, y)]

    def update_score_around(self, x, y):
        r = 4
        original_score1 = {}
        original_score2 = {}

        for i in range(-r, r + 1):
            if x + i < 0:
                continue
            elif x + i >= self.width:
                break
            else:
                original_score1[(x + i, y)] = self.score1[x + i][y]
                original_score2[(x + i, y)] = self.score2[x + i][y]
                self.update_score(x + i, y)

        for i in range(-r, r + 1):
            if y + i < 0:
                continue
            elif y + i >= self.height:
                break
            else:
                original_score1[(x, y + i)] = self.score1[x][y + i]
                original_score2[(x, y + i)] = self.score2[x][y + i]
                self.update_score(x, y + i)

        for i in range(-r, r + 1):
            if x + i < 0 or y + i < 0:
                continue
            elif x + i >= self.width or y + i >= self.height:
                break
            else:
                original_score1[(x + i, y + i)] = self.score1[x + i][y + i]
                original_score2[(x + i, y + i)] = self.score2[x + i][y + i]
                self.update_score(x + i, y + i)

        for i in range(-r, r + 1):
            if x + i < 0 or y - i >= self.height:
                continue
            elif x + i >= self.width or y - i < 0:
                break
            else:
                original_score1[(x + i, y - i)] = self.score1[x + i][y - i]
                original_score2[(x + i, y - i)] = self.score2[x + i][y - i]
                self.update_score(x + i, y - i)

        return original_score1, original_score2

    def update_score(self, x, y):
        if self.board[x][y] == 0:
            self.score1[x][y] = self.compute_score(x, y, 1)
            self.score2[x][y] = self.compute_score(x, y, 2)
        elif self.board[x][y] == 1:
            self.score1[x][y] = self.compute_score(x, y, 1)
            self.score2[x][y] = 0
        else:  # self.board[x][y] == 2
            self.score1[x][y] = 0
            self.score2[x][y] = self.compute_score(x, y, 2)

    def compute_score(self, x, y, z):
        assert z == 1 or z == 2

        if z == 1:
            t = 2
        else:  # z == 2
            t = 1

        score = 0
        mine = 1
        block = 0
        length = 1

        i = 1
        while x + i < self.width and self.board[x + i][y] == z:
            mine += 1
            length += 1
            i += 1
        if x + i < self.width and self.board[x + i][y] == 0:
            while x + i < self.width and self.board[x + i][y] != t:
                length += 1
                i += 1
        else:
            block += 1

        i = 1
        while x - i >= 0 and self.board[x - i][y] == z:
            mine += 1
            length += 1
            i += 1
        if x - i >= 0 and self.board[x - i][y] == 0:
            while x - i >= 0 and self.board[x - i][y] != t:
                length += 1
                i += 1
        else:
            block += 1

        score += self.direct_score(mine, block, length)

        mine = 1
        block = 0
        length = 1

        i = 1
        while y + i < self.height and self.board[x][y + i] == z:
            mine += 1
            length += 1
            i += 1
        if y + i < self.height and self.board[x][y + i] == 0:
            while y + i < self.height and self.board[x][y + i] != t:
                length += 1
                i += 1
        else:
            block += 1

        i = 1
        while y - i >= 0 and self.board[x][y - i] == z:
            mine += 1
            length += 1
            i += 1
        if y - i >= 0 and self.board[x][y - i] == 0:
            while y - i >= 0 and self.board[x][y - i] != t:
                length += 1
                i += 1
        else:
            block += 1

        score += self.direct_score(mine, block, length)

        mine = 1
        block = 0
        length = 1

        i = 1
        while x + i < self.width and y + i < self.height and self.board[x + i][y + i] == z:
            mine += 1
            length += 1
            i += 1
        if x + i < self.width and y + i < self.height and self.board[x + i][y + i] == 0:
            while x + i < self.width and y + i < self.height and self.board[x + i][y + i] != t:
                length += 1
                i += 1
        else:
            block += 1

        i = 1
        while x - i >= 0 and y - i >= 0 and self.board[x - i][y - i] == z:
            mine += 1
            length += 1
            i += 1
        if x - i >= 0 and y - i >= 0 and self.board[x - i][y - i] == 0:
            while x - i >= 0 and y - i >= 0 and self.board[x - i][y - i] != t:
                length += 1
                i += 1
        else:
            block += 1

        score += self.direct_score(mine, block, length)

        mine = 1
        block = 0
        length = 1

        i = 1
        while x + i < self.width and y - i >= 0 and self.board[x + i][y - i] == z:
            mine += 1
            length += 1
            i += 1
        if x + i < self.width and y - i >= 0 and self.board[x + i][y - i] == 0:
            while x + i < self.width and y - i >= 0 and self.board[x + i][y - i] != t:
                length += 1
                i += 1
        else:
            block += 1

        i = 1
        while x - i >= 0 and y + i < self.height and self.board[x - i][y + i] == z:
            mine += 1
            length += 1
            i += 1
        if x - i >= 0 and y + i < self.height and self.board[x - i][y + i] == 0:
            while x - i >= 0 and y + i < self.height and self.board[x - i][y + i] != t:
                length += 1
                i += 1
        else:
            block += 1

        score += self.direct_score(mine, block, length)

        return score

    def direct_score(self, mine, block, length):
        if length < 5:
            return 0

        elif mine == 1:
            if block == 0:
                return self.shape_score['one']
            elif block == 1:
                return self.shape_score['blocked_one']
            else:  # block == 2
                return 0

        elif mine == 2:
            if block == 0:
                return self.shape_score['two']
            elif block == 1:
                return self.shape_score['blocked_two']
            else:  # block == 2
                return 0

        elif mine == 3:
            if block == 0:
                return self.shape_score['three']
            elif block == 1:
                return self.shape_score['blocked_three']
            else:  # block == 2
                return 0

        elif mine == 4:
            if block == 0:
                return self.shape_score['four']
            elif block == 1:
                return self.shape_score['blocked_four']
            else:  # block == 2
                return 0

        else:  # mine >= 5
            return self.shape_score['five']

    def get_actions(self, z):
        assert z == 1 or z == 2

        five1 = []
        five2 = []
        four1 = []
        four2 = []
        three1 = []
        three2 = []
        two1 = []
        two2 = []

        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y] == 0:
                    if self.score1[x][y] >= self.shape_score['five']:
                        five1.append((x, y))
                    elif self.score2[x][y] >= self.shape_score['five']:
                        five2.append((x, y))
                    elif self.score1[x][y] >= self.shape_score['four']:
                        four1.append((x, y))
                    elif self.score2[x][y] >= self.shape_score['four']:
                        four2.append((x, y))
                    elif self.score1[x][y] >= self.shape_score['three']:
                        three1.append((x, y))
                    elif self.score2[x][y] >= self.shape_score['three']:
                        three2.append((x, y))
                    elif self.score1[x][y] >= self.shape_score['two']:
                        two1.append((x, y))
                    elif self.score2[x][y] >= self.shape_score['two']:
                        two2.append((x, y))

        if z == 1 and five1:
            return five1
        elif z == 2 and five2:
            return five2
        elif z == 1 and five2:
            return five2
        elif z == 2 and five1:
            return five1

        elif z == 1 and four1:
            return four1
        elif z == 2 and four2:
            return four2
        elif z == 1 and four2:
            return four2
        elif z == 2 and four1:
            return four1

        elif z == 1 and three1:
            return three1
        elif z == 2 and three2:
            return three2
        elif z == 1 and three2:
            return three2
        elif z == 2 and three1:
            return three1

        elif z == 1 and two1:
            return two1
        elif z == 2 and two2:
            return two2
        elif z == 1 and two2:
            return two2
        elif z == 2 and two1:
            return two1

        else:
            x = self.width // 2
            y = self.height // 2
            if self.board[x][y] == 0:
                return [(x, y)]
            else:
                return []

    def get_utility(self):
        utility = 0
        for x, y in self.chess1:
            utility += self.score1[x][y]
        for x, y in self.chess2:
            utility -= self.score2[x][y]
        return utility

    def get_status(self):
        for x, y in self.chess1:
            if self.score1[x][y] >= self.shape_score['five']:
                return 1
        for x, y in self.chess2:
            if self.score2[x][y] >= self.shape_score['five']:
                return 2
        return 0