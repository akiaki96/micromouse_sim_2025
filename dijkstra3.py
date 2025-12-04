from WallData import *
import heapq
from enum import IntEnum
import copy
from functools import total_ordering
import time

dir45 = [
(1,0),
(1,1),
(0,1),
(-1,1),
(-1,0),
(-1,-1),
(0,-1),
(1,-1),
(0,0)]

class Dir(IntEnum):
    Est    = 0
    NthEst = 1
    Nth    = 2
    NthWst = 3
    Wst    = 4
    SthWst = 5
    Sth    = 6
    SthEst = 7
    Center = 8

@total_ordering
class Pos():
    def __init__(self, dist, x, y, hv):
        self.dist = dist
        self.x    = x
        self.y    = y
        self.hv   = hv

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.x == other.x) and (self.y == other.y) and (self.hv % 2 == other.hv % 2)
        # return (self.x == other.x) and (self.y == other.y)
    
    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.dist < other.dist
    
    def __repr__(self):
        return f"({self.dist}, {self.x}, {self.y}, {self.hv})"
    
class TurnWall():
    def __init__(self, diffx, diffy, lookdir):
        self.diffx   = diffx
        self.diffy   = diffy
        self.lookdir = lookdir

class GenPath:
    def __init__(self):
        self.TIME_COR = 1000
        self.EX_STRAIGHT  = [int(item * self.TIME_COR) for item in 
                             [0.2948136734570638, 0.5184259223087452, 0.7060840187982667, 0.8710083459561062, 1.019881418756469, 1.156639244156979, 1.2838318451103723, 1.40322329283467, 1.51609407249932, 1.6234085383090224, 1.7259144593235147, 1.825925925925926, 1.9259259259259258, 2.025925925925926, 2.1259259259259258, 2.225925925925926, 2.325925925925926, 2.425925925925926, 2.525925925925926,]]
        self.EX_DIAGONALT = [int(item * self.TIME_COR) for item in 
                             [0.218689588980735, 0.39317622470145036, 0.5427456738330791, 0.6757525913606516, 0.7967200625652743, 0.9084244336388686, 1.0127151330534698, 1.1108975330743123, 1.203933701977136, 1.2925569025412664, 1.3773412220435053, 1.4587461177305097, 1.5371461110094458, 1.612851267901527, 1.6861217362687921, 1.757296775824402, 1.8280074539430569, 1.8987181320617117, 1.969428810180366, 2.040139488299021, 2.1108501664176758, 2.1815608445363304, 2.2522715226549854, 2.32298220077364, 2.3936928788922947, 2.4644035570109497, 2.5351142351296043, 2.605824913248259, 2.676535591366914, 2.7472462694855686, 2.817956947604223, 2.888667625722878, 2.9593783038415324, 3.030088981960188, ]]
        self.S90 = int(303 / 500 * self.TIME_COR)
        self.S180 = int(407 / 500 * self.TIME_COR)
        self.S45 = int(210 / 500 * self.TIME_COR)
        self.S135 = int(323.5 / 500 * self.TIME_COR)
        self.V90 = int(219.5 / 500 * self.TIME_COR)
        
        self.Est_R = TurnWall(1, -1, Dir.Nth)
        self.Est_L = TurnWall(1, 0, Dir.Nth)
        self.Nth_R = TurnWall(0, 1, Dir.Est)
        self.Nth_L = TurnWall(-1, 1, Dir.Est)
        self.Wst_R = TurnWall(0, 0, Dir.Nth)
        self.Wst_L = TurnWall(0, -1, Dir.Nth)
        self.Sth_R = TurnWall(-1, 0, Dir.Est)
        self.Sth_L = TurnWall(0, 0, Dir.Est)

        self.dist    = [[[0xFFFF for _ in range(4)] for _ in range(16)] for _ in range(16)]
        self.visited = [[[False for _ in range(4)] for _ in range(16)] for _ in range(16)]
        self.prv     = [[[None for _ in range(4)] for _ in range(16)] for _ in range(16)]
        self.dirl    = [[[Dir.Center for _ in range(4)] for _ in range(16)] for _ in range(16)]

        self.que = [Pos(0, 0, 0, 0)]





    def cv_01(self, num):
        if num == 0:
            return 1
        else:
            return 0
    
    def cv_23(self, num):
        if num == 2:
            return 3
        else:
            return 2

    def straight_dia(self, now:Pos, tpos:Pos, tw:TurnWall, nxtdir:Dir, tcnt:int) -> bool:
        tpos.x  += tw.diffx
        tpos.y  += tw.diffy
        tpos.hv  = self.cv_23(tpos.hv)
        if not walldata.get_wall_abs(tpos.x, tpos.y, tw.lookdir):
            if (self.dist[tpos.x][tpos.y][tpos.hv] > self.dist[now.x][now.y][now.hv] + self.EX_DIAGONALT[tcnt]):
                self.dist[tpos.x][tpos.y][tpos.hv] = self.dist[now.x][now.y][now.hv] + self.EX_DIAGONALT[tcnt]
                heapq.heappush(self.que, Pos(self.dist[tpos.x][tpos.y][tpos.hv], tpos.x, tpos.y, tpos.hv))
                self.prv[tpos.x][tpos.y][tpos.hv]  = now
                self.dirl[tpos.x][tpos.y][tpos.hv]  = nxtdir
                return True
        return False

    def turn_grid_90(self, now:Pos, tw:TurnWall, nxtdir:Dir):
        if not walldata.get_wall_abs(now.x + tw.diffx, now.y + tw.diffy, tw.lookdir):
            if (self.dist[now.x + tw.diffx][now.y + tw.diffy][self.cv_01(now.hv)] > self.dist[now.x][now.y][now.hv] + self.S90):
                self.dist[now.x + tw.diffx][now.y + tw.diffy][self.cv_01(now.hv)] = self.dist[now.x][now.y][now.hv] + self.S90
                heapq.heappush(self.que, Pos(self.dist[now.x+tw.diffx][now.y+tw.diffy][self.cv_01(now.hv)], now.x+tw.diffx, now.y+tw.diffy, self.cv_01(now.hv)))
                self.prv[now.x + tw.diffx][now.y + tw.diffy][self.cv_01(now.hv)]  = now
                self.dirl[now.x + tw.diffx][now.y + tw.diffy][self.cv_01(now.hv)] = nxtdir
    
    def turn_grid_180(self, now:Pos, tw1:TurnWall, tw2:TurnWall, nxtdir:Dir):
        tw2 = copy.copy(tw2)
        tw2.diffx += tw1.diffx
        tw2.diffy += tw1.diffy
        if not walldata.get_wall_abs(now.x + tw1.diffx, now.y + tw1.diffy, tw1.lookdir) and not walldata.get_wall_abs(now.x + tw2.diffx, now.y + tw2.diffy, tw2.lookdir):
            if (self.dist[now.x + tw2.diffx][now.y + tw2.diffy][now.hv] > self.dist[now.x][now.y][now.hv] + self.S180):
                self.dist[now.x + tw2.diffx][now.y + tw2.diffy][now.hv] = self.dist[now.x][now.y][now.hv] + self.S180
                heapq.heappush(self.que, Pos(self.dist[now.x + tw2.diffx][now.y + tw2.diffy][now.hv], now.x + tw2.diffx, now.y + tw2.diffy, now.hv))
                self.prv[now.x + tw2.diffx][now.y + tw2.diffy][now.hv]  = now
                self.dirl[now.x + tw2.diffx][now.y + tw2.diffy][now.hv] = nxtdir


    def turn_45_in(self, now:Pos, tw:TurnWall, nxtdir:Dir):
        if not walldata.get_wall_abs(now.x + tw.diffx, now.y + tw.diffy, tw.lookdir):
            if (self.dist[now.x + tw.diffx][now.y + tw.diffy][self.cv_01(now.hv)+2] > self.dist[now.x][now.y][now.hv] + self.S45):
                self.dist[now.x + tw.diffx][now.y + tw.diffy][self.cv_01(now.hv)+2] = self.dist[now.x][now.y][now.hv] + self.S45
                heapq.heappush(self.que, Pos(self.dist[now.x+tw.diffx][now.y+tw.diffy][self.cv_01(now.hv)+2], now.x+tw.diffx, now.y+tw.diffy, self.cv_01(now.hv)+2))
                self.prv[now.x + tw.diffx][now.y + tw.diffy][self.cv_01(now.hv)+2]  = now
                self.dirl[now.x + tw.diffx][now.y + tw.diffy][self.cv_01(now.hv)+2] = nxtdir

    def turn_45_out(self, now:Pos, tw:TurnWall, nxtdir:Dir):
        if not walldata.get_wall_abs(now.x + tw.diffx, now.y + tw.diffy, tw.lookdir):
            if (self.dist[now.x + tw.diffx][now.y + tw.diffy][self.cv_23(now.hv)-2] > self.dist[now.x][now.y][now.hv] + self.S45):
                self.dist[now.x + tw.diffx][now.y + tw.diffy][self.cv_23(now.hv)-2] = self.dist[now.x][now.y][now.hv] + self.S45
                heapq.heappush(self.que, Pos(self.dist[now.x+tw.diffx][now.y+tw.diffy][self.cv_23(now.hv)-2], now.x+tw.diffx, now.y+tw.diffy, self.cv_23(now.hv)-2))
                self.prv[now.x + tw.diffx][now.y + tw.diffy][self.cv_23(now.hv)-2]  = now
                self.dirl[now.x + tw.diffx][now.y + tw.diffy][self.cv_23(now.hv)-2] = nxtdir
    
    def turn_135_in(self, now:Pos, tw1:TurnWall, tw2:TurnWall, nxtdir:Dir):
        tw2 = copy.copy(tw2)
        tw2.diffx += tw1.diffx
        tw2.diffy += tw1.diffy
        if not walldata.get_wall_abs(now.x + tw1.diffx, now.y + tw1.diffy, tw1.lookdir) and not walldata.get_wall_abs(now.x + tw2.diffx, now.y + tw2.diffy, tw2.lookdir):
            if (self.dist[now.x + tw2.diffx][now.y + tw2.diffy][now.hv+2] > self.dist[now.x][now.y][now.hv] + self.S135):
                self.dist[now.x + tw2.diffx][now.y + tw2.diffy][now.hv+2] = self.dist[now.x][now.y][now.hv] + self.S135
                heapq.heappush(self.que, Pos(self.dist[now.x + tw2.diffx][now.y + tw2.diffy][now.hv+2], now.x + tw2.diffx, now.y + tw2.diffy, now.hv+2))
                self.prv[now.x + tw2.diffx][now.y + tw2.diffy][now.hv+2]  = now
                self.dirl[now.x + tw2.diffx][now.y + tw2.diffy][now.hv+2] = nxtdir

    def turn_135_out(self, now:Pos, tw1:TurnWall, tw2:TurnWall, nxtdir:Dir):
        tw2 = copy.copy(tw2)
        tw2.diffx += tw1.diffx
        tw2.diffy += tw1.diffy
        if not walldata.get_wall_abs(now.x + tw1.diffx, now.y + tw1.diffy, tw1.lookdir) and not walldata.get_wall_abs(now.x + tw2.diffx, now.y + tw2.diffy, tw2.lookdir):
            if (self.dist[now.x + tw2.diffx][now.y + tw2.diffy][now.hv-2] > self.dist[now.x][now.y][now.hv] + self.S135):
                self.dist[now.x + tw2.diffx][now.y + tw2.diffy][now.hv-2] = self.dist[now.x][now.y][now.hv] + self.S135
                heapq.heappush(self.que, Pos(self.dist[now.x + tw2.diffx][now.y + tw2.diffy][now.hv-2], now.x + tw2.diffx, now.y + tw2.diffy, now.hv-2))
                self.prv[now.x + tw2.diffx][now.y + tw2.diffy][now.hv-2]  = now
                self.dirl[now.x + tw2.diffx][now.y + tw2.diffy][now.hv-2] = nxtdir

    def turn_V90(self, now:Pos, tw1:TurnWall, tw2:TurnWall, nxtdir:Dir):
        tw2 = copy.copy(tw2)
        tw2.diffx += tw1.diffx
        tw2.diffy += tw1.diffy
        if not walldata.get_wall_abs(now.x + tw1.diffx, now.y + tw1.diffy, tw1.lookdir) and not walldata.get_wall_abs(now.x + tw2.diffx, now.y + tw2.diffy, tw2.lookdir):
            if (self.dist[now.x + tw2.diffx][now.y + tw2.diffy][now.hv] > self.dist[now.x][now.y][now.hv] + self.V90):
                self.dist[now.x + tw2.diffx][now.y + tw2.diffy][now.hv] = self.dist[now.x][now.y][now.hv] + self.V90
                heapq.heappush(self.que, Pos(self.dist[now.x + tw2.diffx][now.y + tw2.diffy][now.hv], now.x + tw2.diffx, now.y + tw2.diffy, now.hv))
                self.prv[now.x + tw2.diffx][now.y + tw2.diffy][now.hv]  = now
                self.dirl[now.x + tw2.diffx][now.y + tw2.diffy][now.hv] = nxtdir


    def dijkstra(self, walldata, goalx, goaly, acc:bool, show = False):
        
        # 0,1: on grid, 2,3: diagnal
        self.dist[0][0][0]    = 0
        self.dirl[0][0][0]    = Dir.Nth

        dbg_quelen = len(self.que)

        while self.que:
            now = heapq.heappop(self.que)

            if show:
                print(f"added :{len(self.que) - dbg_quelen + 1}")
                dbg_quelen = len(self.que)
                self.show_path_map(0,0,0, self.que, now)
                print("")
                input()
                # time.sleep(1)

            if self.visited[now.x][now.y][now.hv]:
                continue
            else:
                self.visited[now.x][now.y][now.hv] = True
            
            tpos = copy.copy(now)
            tcnt = 0
            nowdir = self.dirl[now.x][now.y][now.hv]

            if tpos.hv == 0 or tpos.hv == 1:
                while True:
                    tpos.x += dir45[nowdir][0]
                    tpos.y += dir45[nowdir][1]
                    if (not walldata.get_wall_abs(tpos.x, tpos.y, nowdir % 4)
                    and self.dist[tpos.x][tpos.y][tpos.hv] > self.dist[now.x][now.y][now.hv] + self.EX_STRAIGHT[tcnt]):
                            self.dist[tpos.x][tpos.y][tpos.hv] = self.dist[now.x][now.y][now.hv] + self.EX_STRAIGHT[tcnt]
                            heapq.heappush(self.que, Pos(self.dist[tpos.x][tpos.y][tpos.hv], tpos.x, tpos.y, tpos.hv))
                            # heapq.heappush(self.que, Pos())
                            self.prv[tpos.x][tpos.y][tpos.hv]   = now
                            self.dirl[tpos.x][tpos.y][tpos.hv]  = nowdir
                            tcnt += 1
                    
                            if not acc:
                                break
                    else:
                        break

            flag = True
            while flag:
                if tpos.hv == 2:
                    if nowdir == Dir.NthEst:
                        flag = self.straight_dia(now, tpos, self.Nth_R, Dir.NthEst, tcnt)
                    elif nowdir == Dir.NthWst:
                        flag = self.straight_dia(now, tpos, self.Nth_L, Dir.NthWst, tcnt)
                    elif nowdir == Dir.SthWst:
                        flag = self.straight_dia(now, tpos, self.Sth_R, Dir.SthWst, tcnt)
                    elif nowdir == Dir.SthEst:
                        flag = self.straight_dia(now, tpos, self.Sth_L, Dir.SthEst, tcnt)
                elif tpos.hv == 3:
                    if nowdir == Dir.NthEst:
                        flag = self.straight_dia(now, tpos, self.Est_L, Dir.NthEst, tcnt)
                    elif nowdir == Dir.NthWst:
                        flag = self.straight_dia(now, tpos, self.Wst_R, Dir.NthWst, tcnt)
                    elif nowdir == Dir.SthWst:
                        flag = self.straight_dia(now, tpos, self.Wst_L, Dir.SthWst, tcnt)
                    elif nowdir == Dir.SthEst:
                        flag = self.straight_dia(now, tpos, self.Est_R, Dir.SthEst, tcnt)
                else:
                    break
                if not acc:
                    break
                tcnt += 1


            if (nowdir == Dir.Est):
                # S90 Right
                self.turn_grid_90(now, self.Est_R, Dir.Sth)
                self.turn_grid_180(now, self.Est_R, self.Sth_R, Dir.Wst) # Right (Est), Right (Sth)
                self.turn_135_in(now, self.Est_R, self.Sth_R, Dir.SthWst)
                self.turn_45_in(now, self.Est_R, Dir.SthEst)
                # S90 Left
                self.turn_grid_90(now, self.Est_L, Dir.Nth)
                self.turn_grid_180(now, self.Est_L, self.Nth_L, Dir.Wst) # Left (Est), Left (Nth)
                self.turn_135_in(now, self.Est_L, self.Nth_L, Dir.NthWst)
                self.turn_45_in(now, self.Est_L, Dir.NthEst)

            elif (nowdir == Dir.Nth):
                # S90 Right
                self.turn_grid_90(now, self.Nth_R, Dir.Est)
                self.turn_grid_180(now, self.Nth_R, self.Est_R, Dir.Sth) # Right (Nth), Right (Est)
                self.turn_135_in(now, self.Nth_R, self.Est_R, Dir.SthEst)
                self.turn_45_in(now, self.Nth_R, Dir.NthEst)
                # S90 Left
                self.turn_grid_90(now, self.Nth_L, Dir.Wst)
                self.turn_grid_180(now, self.Nth_L, self.Wst_L, Dir.Sth) # Left (Nth), Left (Wst)
                self.turn_135_in(now, self.Nth_L, self.Wst_L, Dir.SthWst)
                self.turn_45_in(now, self.Nth_L, Dir.NthWst)

            elif (nowdir == Dir.Wst):
                # S90 Right
                self.turn_grid_90(now, self.Wst_R, Dir.Nth)
                self.turn_grid_180(now, self.Wst_R, self.Nth_R, Dir.Est) # Right (Wst), Right (Nth)
                self.turn_135_in(now, self.Wst_R, self.Nth_R, Dir.NthEst)
                self.turn_45_in(now, self.Wst_R, Dir.NthWst)
                # S90 Left
                self.turn_grid_90(now, self.Wst_L, Dir.Sth)
                self.turn_grid_180(now, self.Wst_L, self.Sth_L, Dir.Est) # Left (Wst), Left (Sth)
                self.turn_135_in(now, self.Wst_L, self.Sth_L, Dir.SthEst)
                self.turn_45_in(now, self.Wst_L, Dir.SthWst)

            elif (nowdir == Dir.Sth):
                # S90 Right
                self.turn_grid_90(now, self.Sth_R, Dir.Wst)
                self.turn_grid_180(now, self.Sth_R, self.Wst_R, Dir.Nth) # Right (Sth), Right (Wst)
                self.turn_135_in(now, self.Sth_R, self.Wst_R, Dir.NthWst)
                self.turn_45_in(now, self.Sth_R, Dir.SthWst)
                # S90 Left
                self.turn_grid_90(now, self.Sth_L, Dir.Est)
                self.turn_grid_180(now, self.Sth_L, self.Est_L, Dir.Nth) # Left (Sth), Left (Est)
                self.turn_135_in(now, self.Sth_L, self.Est_L, Dir.NthEst)
                self.turn_45_in(now, self.Sth_L, Dir.SthEst)
            

            elif (nowdir == Dir.NthEst):
                if now.hv == 2:
                    # Right (hv: 2 -> 1)
                    self.turn_45_out(now, self.Nth_R, Dir.Est) # turn right (Nth)
                    self.turn_135_out(now, self.Nth_R, self.Est_R, Dir.Sth)
                    self.turn_V90(now, self.Nth_R, self.Est_R, Dir.SthEst)
                else:
                    # Left (hv : 3 -> 0)
                    self.turn_45_out(now, self.Est_L, Dir.Nth) # turn left (Est)
                    self.turn_135_out(now, self.Est_L, self.Nth_L, Dir.Wst)
                    self.turn_V90(now, self.Est_L, self.Nth_L, Dir.NthWst)

            elif (nowdir == Dir.NthWst):
                if now.hv == 2:
                    # Left (hv: 2 -> 1)
                    self.turn_45_out(now, self.Nth_L, Dir.Wst) # turn left (Nth)
                    self.turn_135_out(now, self.Nth_L, self.Wst_L, Dir.Sth)
                    self.turn_V90(now, self.Nth_L, self.Wst_L, Dir.SthWst)
                else:
                    # Right (hv : 3 -> 0)
                    self.turn_45_out(now, self.Wst_R, Dir.Nth) # turn right (Wst)
                    self.turn_135_out(now, self.Wst_R, self.Nth_R, Dir.Est)
                    self.turn_V90(now, self.Wst_R, self.Nth_R, Dir.NthEst)
                
            elif (nowdir == Dir.SthWst):
                if now.hv == 2:
                    # Right (hv: 2 -> 1)
                    self.turn_45_out(now, self.Sth_R, Dir.Wst) # turn right (Sth)
                    self.turn_135_out(now, self.Sth_R, self.Wst_R, Dir.Nth)
                    self.turn_V90(now, self.Sth_R, self.Wst_R, Dir.NthWst)
                else:
                    # Left (hv : 3 -> 0)
                    self.turn_45_out(now, self.Wst_L, Dir.Sth) # turn left (Wst)
                    self.turn_135_out(now, self.Wst_L, self.Sth_L, Dir.Est)
                    self.turn_V90(now, self.Wst_L, self.Sth_L, Dir.SthEst)
                
            elif (nowdir == Dir.SthEst):
                if now.hv == 2:
                    # Left (hv: 2 -> 1)
                    self.turn_45_out(now, self.Sth_L, Dir.Est) # turn left (Sth)
                    self.turn_135_out(now, self.Sth_L, self.Est_L, Dir.Nth)
                    self.turn_V90(now, self.Sth_L, self.Est_L, Dir.NthEst)
                else:
                    # Right (hv : 3 -> 0)
                    self.turn_45_out(now, self.Est_R, Dir.Sth) # turn right (Est)
                    self.turn_135_out(now, self.Est_R, self.Sth_R, Dir.Wst)
                    self.turn_V90(now, self.Est_R, self.Sth_R, Dir.SthWst) 
        return

    def show_path(self, goalx, goaly, goalhv, printtf):
        now = Pos(0, goalx, goaly, goalhv)
        l = []
        while now != None:
            if printtf:
                print("({:2d} {:2d} {:1d})".format(now.x, now.y, now.hv), end=" -> ")
            l.append(now)
            now = self.prv[now.x][now.y][now.hv]
        if printtf:
            print()
        return l
    
    def gen_motion(self, goalx, goaly, goalhv, printtf:bool):
        l = reversed(self.show_path(goalx, goaly, goalhv, False))


    def show_path_map(self, goalx, goaly, goalhv, l = None, blue = None):
        time = 0
        if l == None:
            l = self.show_path(goalx, goaly, goalhv, False)
            time = self.dist[goalx][goaly][goalhv] / self.TIME_COR

        res = ""

        # print("+", end="")
        res += "+"
        for i in range(16):
            # print..i("---+", end="")
            res += "---+"
        # print("")
        res += "\n"

        for y in range(0, 16).__reversed__():
            # print("|", end="")
            res += "|"
            for x in range(16):

                tmpl = list(filter(lambda p: p == Pos(0,x,y,1), l + [blue]))
                char = " "
                if len(tmpl) == 0:
                    ...
                elif len(tmpl) >= 2:
                    char = str(len(tmpl))
                elif self.dirl[x][y][tmpl[0].hv] % 4 == 0:
                    char = "-"
                elif self.dirl[x][y][tmpl[0].hv] % 4 == 1:
                    char = "/"
                elif self.dirl[x][y][tmpl[0].hv] % 4 == 2:
                    char = "|"
                else:
                    char = "\\"

                if (walldata.get_wall_abs(x, y, Est)):
                    # print("   |", end="")
                    res += "   |"
                else:
                    if Pos(0, x, y, 1) == blue:
                        # print("   " + "\033[44m" + char + "\033[0m", end="")
                        res += "   " + "\033[44m" + char + "\033[0m"
                    else:
                        # print("   " + "\033[31m" + char + "\033[0m", end="")
                        res += "   " + "\033[31m" + char + "\033[0m"
            # print("")
            res += "\n"
            # print("+", end="")
            res += "+"
            for x in range(16):

                tmpl = list(filter(lambda p: p == Pos(0,x,y-1,0), l + [blue]))
                char = " "
                if len(tmpl) == 0:
                    ...
                elif len(tmpl) >= 2:
                    char = str(len(tmpl))
                elif self.dirl[x][y-1][tmpl[0].hv] % 4 == 0:
                    char = "-"
                elif self.dirl[x][y-1][tmpl[0].hv] % 4 == 1:
                    char = "/"
                elif self.dirl[x][y-1][tmpl[0].hv] % 4 == 2:
                    char = "|"
                else:
                    char = "\\"
                

                if (walldata.get_wall_abs(x, y, Sth)):
                    # print("---+", end="")
                    res += "---+"
                else:
                    if Pos(0, x, y-1, 0) == blue:
                        # print(" " + "\033[44m" + char + "\033[0m" + " +", end="") 
                        res += " " + "\033[44m" + char + "\033[0m" + " +"
                    else:
                        # print(" " + "\033[31m" + char + "\033[0m" + " +", end="")
                        res += " " + "\033[31m" + char + "\033[0m" + " +"
            # print("")
            res += "\n"


        if blue != None:
            char = ""
            if self.dirl[blue.x][blue.y][blue.hv] == 0:
                char = "→"
            elif self.dirl[blue.x][blue.y][blue.hv] == 1:
                char = "↗"
            elif self.dirl[blue.x][blue.y][blue.hv] == 2:
                char = "↑"
            elif self.dirl[blue.x][blue.y][blue.hv] == 3:
                char = "↖"
            elif self.dirl[blue.x][blue.y][blue.hv] == 4:
                char = "←"
            elif self.dirl[blue.x][blue.y][blue.hv] == 5:
                char = "↙"
            elif self.dirl[blue.x][blue.y][blue.hv] == 6:
                char = "↓"
            elif self.dirl[blue.x][blue.y][blue.hv] == 7:
                char = "↘"


            res = res[:-1]
            res += str(blue) + f"\t{char} " + str(self.dirl[blue.x][blue.y][blue.hv]) + "\n"
        
        elif time != 0:
            res = res[:-1]
            res += " " +str(time) + " sec\n"
        print(res, end="")
        return

if __name__ == "__main__":

    walldata = WallData()
    flag = False
    try:
        al = input().split(" ")
        if al != "":
            for i in range(16):
                walldata.wall_hor[i] = int(al[i], 2)
            for i in range(16):
                walldata.wall_ver[i] = int(al[i+16], 2)
    except:
        print("No input")
        al = ""

        walldata.wall_hor[0]  = 0b010000000000000
        walldata.wall_hor[1]  = 0b100010010001010
        walldata.wall_hor[2]  = 0b100010100000101
        walldata.wall_hor[3]  = 0b101001010100001
        walldata.wall_hor[4]  = 0b110010011110010
        walldata.wall_hor[5]  = 0b111000011110111
        walldata.wall_hor[6]  = 0b011100000101011
        walldata.wall_hor[7]  = 0b110101101011111
        walldata.wall_hor[8]  = 0b111110001110110
        walldata.wall_hor[9]  = 0b101100000111101
        walldata.wall_hor[10] = 0b011100000101101
        walldata.wall_hor[11] = 0b100010000000110
        walldata.wall_hor[12] = 0b110000000000011
        walldata.wall_hor[13] = 0b100000100000011
        walldata.wall_hor[14] = 0b100000010000001
        walldata.wall_hor[15] = 0b000000001000010

        walldata.wall_ver[0]  = 0b000000000000001
        walldata.wall_ver[1]  = 0b000010100001010
        walldata.wall_ver[2]  = 0b011001000000101
        walldata.wall_ver[3]  = 0b110100000001101
        walldata.wall_ver[4]  = 0b111110000010110
        walldata.wall_ver[5]  = 0b111100001000011
        walldata.wall_ver[6]  = 0b010110001000111
        walldata.wall_ver[7]  = 0b011101101000110
        walldata.wall_ver[8]  = 0b101111101100101
        walldata.wall_ver[9]  = 0b110110100111011
        walldata.wall_ver[10] = 0b111101001110101
        walldata.wall_ver[11] = 0b101010000101010
        walldata.wall_ver[12] = 0b011100000010111
        walldata.wall_ver[13] = 0b110100000000110
        walldata.wall_ver[14] = 0b000010000000010
        walldata.wall_ver[15] = 0b000000000000000

    # walldata.print_wall()
    genpath = GenPath()
    genpath.dijkstra(walldata, 7, 7, True, True)
    genpath.show_path(7,7,0,True)
    genpath.show_path_map(7, 7, 0)