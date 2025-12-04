Est=0
NthEst=1
Nth=2
NthWst=3
Wst=4
SthWst=5
Sth=6
SthEst=7

dir45 = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]

class WallData:
    def __init__(self):
        self.MAZE_SIZE = 16
        self.wall_ver = [0 for _ in range(self.MAZE_SIZE)]
        self.wall_hor = [0 for _ in range(self.MAZE_SIZE)]
        # self.wall = [[0x0 for _ in range(self.MAZE_SIZE)] for _ in range(self.MAZE_SIZE)]
    
    # けりさんのやつ
    # def set_wall(self, wall_list):
    #     for y in range(self.MAZE_SIZE):
    #         for x in range(self.MAZE_SIZE):
    #             self.wall[x][y] = int(wall_list[y][x], 16)


    # def get_wall_abs(self, posx, posy, dir) -> bool:
    #     if ((not (0 <= posx < 16)) or (not (0 <= posy < 16))):
    #         return True
    #     return (self.wall[posx][posy] >> (dir//2)) & 1

    def get_wall_abs(self, x, y, dir):
        if (x < 0 or x >= 16 or y < 0 or y >= 16):
            return True
        if (x == 0 and dir == Wst):
            return True
        elif (x == 16 - 1 and dir == Est):
            return True
        elif (y == 0 and dir == Sth):
            return True
        elif (y == 16 - 1 and dir == Nth):
            return True

        if (dir == Est):
            return (self.wall_ver[y] >> (x)) & 1
        elif (dir == Wst):
            return (self.wall_ver[y] >> (x-1)) & 1
        elif (dir == Nth):
            return (self.wall_hor[x] >> (y)) & 1
        elif (dir == Sth):
            return (self.wall_hor[x] >> (y-1)) & 1
        
        return True


    def print_wall(self):

        print("+", end="")
        for i in range(self.MAZE_SIZE):
            print("---+", end="")
        print("")

        for y in range(0, self.MAZE_SIZE).__reversed__():
            print("|", end="")
            for x in range(self.MAZE_SIZE):
                if (self.get_wall_abs(x, y, Est)):
                    print("   |", end="")
                else:
                    print("    ", end="")
            print("")
            print("+", end="")
            for x in range(self.MAZE_SIZE):
                if (self.get_wall_abs(x, y, Sth)):
                    print("---+", end="")
                else:
                    print("   +", end="")
            print("")

